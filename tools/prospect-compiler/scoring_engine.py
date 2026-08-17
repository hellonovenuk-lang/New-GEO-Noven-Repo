#!/usr/bin/env python3
"""
Deterministic computation only - the counterpart to build_workbook.py's
deterministic rendering-only rule. This script does not research businesses,
does not decide who is a prospect, and does not set the 9 evidence-backed
VALUE fields (commercial_fit, service_relevance, business_credibility,
ability_to_buy, decision_maker_identified, direct_dm_route,
contact_route_quality, contact_identity_confidence, research_completeness) -
those are Claude's judgement calls, made from research, written into the
campaign JSON before this script runs. What this script does is take those
value fields plus each business's service_scope and question_appearances,
plus the campaign's run.service_scopes[] / run.question_relevance[]
definitions, and mechanically fill in every DERIVED field: relevance-
normalized visibility, gap strength, the final qualification score, the
evidence-confidence and readiness gates, opportunity type, and both ranks.

No sector, geography, business name, or question text is hard-coded
anywhere in this file - every rule reads its inputs from the campaign JSON
itself. See tools/prospect-compiler/CAMPAIGN-HANDOFF.md Section 3a for the
full documented methodology this script implements.

Usage:
  python3 scoring_engine.py --input campaign.json --output campaign.scored.json
  python3 scoring_engine.py --input campaign.json --in-place
"""
import argparse
import json
import sys

# ---------------------------------------------------------------------------
# Narrative generation - mandatory, not an optional helper. Every scored
# outreach[] entry gets competitive_gap_finding/why_prospect deterministically
# derived from its own final structured values (scores, ranks, opportunity
# type, nearest competitor - computed earlier in score_pool()), every time
# those values change. See CAMPAIGN-HANDOFF.md Section 3a's narrative
# subsection for the full rationale; the short version: a hand-typed
# "13 of the 90 raw answers" sentence for a kitchen-only specialist whose
# real relevant denominator is 60 is exactly the defect this exists to make
# structurally impossible for a newly-generated campaign.
# ---------------------------------------------------------------------------

NARRATIVE_SIGNATURE_FIELDS = [
    "relevant_appearances", "relevant_opportunities", "visibility_rate",
    "opportunity_type", "nearest_competitor", "group_top_visibility_rate",
    "relative_position", "question_coverage", "service_scope",
    "business_credibility", "gap_strength",
]


def narrative_signature(entry):
    """A deterministic, human-readable fingerprint of the structured values
    a narrative was (or would be) generated from. score_pool() recomputes
    and compares this on every run, so a re-score (a corrected mention
    count, a changed VALUE field, ...) can never leave a stale narrative
    behind just because the field already happened to be non-empty -
    fingerprint mismatch forces regeneration. Deliberately a readable
    "field=value|field=value" string, not an opaque hash - auditable by
    inspection, the same standard as everything else in this pipeline."""
    return "|".join(f"{f}={entry.get(f)}" for f in NARRATIVE_SIGNATURE_FIELDS)


def _fmt_num(x):
    """13.0 -> "13", 13.5 -> "13.5" - clean, auditable numeric text. A
    weighted relevant_appearances/relevant_opportunities value can be
    fractional (an AMBIGUOUS question's partial weight), so this can't
    just always print an integer."""
    if x is None:
        return "0"
    try:
        xf = float(x)
    except (TypeError, ValueError):
        return str(x)
    return str(int(xf)) if xf == int(xf) else f"{xf:g}"


def _provider_split_note(entry):
    """Provider split mentioned only where mechanically material: this
    business was never named at all by at least one provider despite
    appearing elsewhere, or one provider alone accounts for >=70% of its
    total raw mentions. Neither condition holding means no note - not every
    business's finding needs a provider-split sentence."""
    total = entry.get("total_ai_appearances") or 0
    if not total:
        return ""
    counts = {
        "OpenAI": entry.get("openai_appearances") or 0,
        "Gemini": entry.get("gemini_appearances") or 0,
        "Perplexity": entry.get("perplexity_appearances") or 0,
    }
    absent = [p for p, c in counts.items() if c == 0]
    if absent and len(absent) < 3:
        return f" It was never named by {' or '.join(sorted(absent))}, despite appearing elsewhere."
    dominant = max(counts, key=counts.get)
    if counts[dominant] / total >= 0.7:
        return f" {counts[dominant]} of its {_fmt_num(total)} raw mentions are on {dominant} alone."
    return ""


def generate_competitive_gap_finding(entry, run):
    """Deterministic, relevance-aware competitive_gap_finding for a scored
    outreach entry.

    The opening clause ("appears in N of M relevant opportunities") is a
    fixed, machine-recognizable shape - build_workbook.py's
    detect_narrative_contradictions() depends on exactly this phrasing to
    locate and check the PRIMARY visibility claim. Every other figure in
    this text (competitor rate, question coverage, provider split) uses
    deliberately different phrasing so it is never confused with the
    primary measure, per CAMPAIGN-HANDOFF.md's contradiction-detection rule.
    """
    business = entry["business"]
    ra, ro = entry.get("relevant_appearances", 0), entry.get("relevant_opportunities", 0)
    rate = entry.get("visibility_rate", 0)
    scope = entry.get("service_scope", "")
    raw_total = (run.get("responses_per_question") or 0) * len(run.get("questions") or [])
    same_as_raw = raw_total and round(ro) == raw_total

    opening = (
        f"{business} appears in {_fmt_num(ra)} of {_fmt_num(ro)} relevant opportunities "
        f"in its {scope} scope ({rate:.1f}% relevance-aware visibility)"
    )
    if same_as_raw:
        opening += (
            " — every one of this campaign's questions was relevant to this business, "
            "so this is also its raw total"
        )
    elif raw_total:
        opening += f", out of {raw_total} raw answers collected across the whole campaign"

    nearest = entry.get("nearest_competitor")
    if nearest:
        top_rate = entry.get("group_top_visibility_rate", 0)
        relpos = entry.get("relative_position", 0)
        competitor_clause = (
            f" {nearest}, the strongest same-scope competitor, sits at {top_rate:.1f}% "
            f"({relpos * 100:.0f}% of the leader's rate)."
        )
    else:
        competitor_clause = " No comparable same-scope competitor is in this pool."

    coverage_clause = (
        f" It answered {entry.get('question_coverage', 0) * 100:.0f}% of its own "
        f"relevant questions at least once."
    )

    return opening + "." + competitor_clause + coverage_clause + _provider_split_note(entry)


def generate_why_prospect(entry, run):
    """Deterministic why_prospect for a scored outreach entry, branched by
    opportunity_type - always the commercial case (why this opportunity
    type, evidenced), never just a restatement of service_scope or
    business_type_notes. business_type_notes may be cited as one further,
    clearly separate clause for context - it is never the whole field."""
    business = entry["business"]
    ra, ro = entry.get("relevant_appearances", 0), entry.get("relevant_opportunities", 0)
    rate = entry.get("visibility_rate", 0)
    nearest = entry.get("nearest_competitor") or "the nearest same-scope competitor"
    top_rate = entry.get("group_top_visibility_rate", 0)
    opp = entry.get("opportunity_type")
    cred = entry.get("business_credibility", 0)
    gap = entry.get("gap_strength", 0)
    relpos = entry.get("relative_position", 0)

    core = f"{business} appears in {_fmt_num(ra)} of {_fmt_num(ro)} relevant opportunities ({rate:.1f}%)"

    if opp == "DEFEND":
        text = (
            f"{core}, already one of the strongest AI-recommendation positions in its service scope "
            f"— {relpos * 100:.0f}% of {nearest}'s leading {top_rate:.1f}% rate. The opportunity is "
            f"understanding what supports that position and monitoring whether it holds."
        )
    elif opp == "GAP":
        text = (
            f"{core}, materially underrepresented against {nearest} at {top_rate:.1f}% despite evidenced "
            f"credibility ({cred}/5). This is a real, actionable gap, not explained by being new, tiny, "
            f"specialist, or out of market."
        )
    elif opp == "GROWTH":
        text = (
            f"{core}, real and worth having, but sitting materially behind {nearest} at {top_rate:.1f}% "
            f"(gap strength {gap}/5). There is clear, evidenced room to strengthen this position."
        )
    else:  # REVIEW or unset
        text = (
            f"{core}. Evidence is not yet sufficient to classify this business's commercial opportunity "
            f"with confidence (business credibility {cred}/5)."
        )

    notes = (entry.get("business_type_notes") or "").strip()
    if notes:
        text += f" ({notes})"
    return text

# ---------------------------------------------------------------------------
# Weights and thresholds - the ONE place these live. Change them here, not
# per-call, so every campaign that uses this engine is governed by the same
# documented rule. See CAMPAIGN-HANDOFF.md Section 3a for the rationale
# behind every number below.
# ---------------------------------------------------------------------------
FINAL_SCORE_WEIGHTS = {
    "commercial_fit": 3, "service_relevance": 2, "visibility_score": 2,
    "gap_strength": 4, "business_credibility": 3, "ability_to_buy": 2,
    "decision_maker_identified": 2, "direct_dm_route": 3, "contact_route_quality": 1,
}
FINAL_SCORE_MAX_RAW = sum(w * 5 for w in FINAL_SCORE_WEIGHTS.values())  # 110

VISIBILITY_BANDS = [(0, 0), (10, 1), (25, 2), (40, 3), (60, 4), (100, 5)]

DEFEND_MIN_VISIBILITY_SCORE = 3
DEFEND_MIN_RELATIVE_POSITION = 0.85
DEFEND_MIN_QUESTION_COVERAGE = 0.75
GAP_MIN_CREDIBILITY = 3
GAP_MAX_VISIBILITY_SCORE = 1

BUSINESS_VERIFIED_MIN_CREDIBILITY = 3
CONTACT_ROUTE_VERIFIED_MIN_QUALITY = 3
NAMED_DM_VERIFIED_MIN = 4
NAMED_DM_PROBABLE_MIN = 3
IDENTITY_CONFIRMED_MIN = 4
IDENTITY_PROBABLE_EXACT = 3
RESEARCH_COMPLETE_MIN = 4
ELIGIBLE_MIN_FIT = 2
ELIGIBLE_MIN_RELEVANCE = 2
READY_MIN_DM_IDENTIFIED = 3
READY_MIN_IDENTITY_CONFIDENCE = 3
READY_MIN_EVIDENCE_CONFIDENCE = 3

PRIORITY_A_MIN_SCORE = 70
PRIORITY_B_MIN_SCORE = 50

ACCESSIBILITY_GRADE_BY_DM_ROUTE = {
    5: "CONFIRMED_DIRECT", 4: "CONFIRMED_GENERIC_ROUTE", 3: "PROBABLE_UNCONFIRMED",
    2: "GENERIC_INBOX_ONLY", 1: "CONTACT_FORM_OR_PHONE_ONLY", 0: "NO_USABLE_ROUTE",
}

SCORED_VALUE_FIELDS = [
    "commercial_fit", "service_relevance", "business_credibility", "ability_to_buy",
    "decision_maker_identified", "direct_dm_route", "contact_route_quality",
    "contact_identity_confidence", "research_completeness",
]


class ScoringError(Exception):
    pass


def band_visibility(rate_pct):
    for threshold, score in VISIBILITY_BANDS:
        if rate_pct <= threshold:
            return score
    return 5


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def build_relevance_index(run):
    """question_id -> {'type', 'service', 'weight'}. Raises if a question has
    no relevance entry at all - a silently-defaulted-to-full-relevance
    question is exactly what CAMPAIGN-HANDOFF.md Section 3a forbids."""
    question_ids = {q["question_id"] for q in run.get("questions", [])}
    relevance = run.get("question_relevance", [])
    index = {}
    for entry in relevance:
        qid = entry["question_id"]
        if qid not in question_ids:
            raise ScoringError(f"question_relevance references unknown question_id '{qid}'")
        rtype = entry["type"]
        if rtype == "SERVICE_ONLY" and not entry.get("service"):
            raise ScoringError(f"question_relevance[{qid}]: type SERVICE_ONLY requires 'service'")
        if rtype == "AMBIGUOUS" and "weight" not in entry:
            raise ScoringError(f"question_relevance[{qid}]: type AMBIGUOUS requires an explicit 'weight' "
                                f"(0 to exclude, or a documented fraction) - it must never silently default "
                                f"to full relevance")
        index[qid] = entry
    missing = question_ids - set(index)
    if missing:
        raise ScoringError(f"question_relevance is missing entries for: {sorted(missing)} - "
                            f"every campaign question must be classified, per CAMPAIGN-HANDOFF.md Section 3a")
    return index


def build_scope_index(run):
    """service_scope label -> set(applicable_services)."""
    scopes = run.get("service_scopes", [])
    if not scopes:
        raise ScoringError("run.service_scopes is empty - required wherever any business sets service_scope")
    return {s["label"]: set(s["applicable_services"]) for s in scopes}


def question_weight_for_business(rel_entry, applicable_services):
    """The relevance weight (0-1) of one question for a business with the
    given set of applicable_services, per CAMPAIGN-HANDOFF.md Section 3a's
    4 rules. A business with no applicable_services (an unscoped/uncertain
    candidate) gets 0 everywhere - it should not be scored at all yet."""
    if not applicable_services:
        return 0.0
    rtype = rel_entry["type"]
    if rtype == "SERVICE_ONLY":
        return 1.0 if rel_entry["service"] in applicable_services else 0.0
    if rtype == "EXPLICITLY_COMBINED":
        # Only a genuine multi-service provider - i.e. its applicable_services
        # covers more than one real service - gets full relevance here.
        return 1.0 if len(applicable_services) > 1 else 0.0
    if rtype == "SINGLE_SERVICE_INCLUSIVE":
        return 1.0
    if rtype == "AMBIGUOUS":
        return float(rel_entry.get("weight", 0.0))
    raise ScoringError(f"unknown question_relevance type '{rtype}'")


def compute_visibility(entry, run, relevance_index, scope_index):
    scope_label = entry.get("service_scope")
    if not scope_label:
        return None  # not opted into scoring
    if scope_label not in scope_index:
        raise ScoringError(f"{entry.get('business')!r}: service_scope '{scope_label}' not defined in run.service_scopes")
    applicable = scope_index[scope_label]
    responses_per_q = run.get("responses_per_question")
    if not responses_per_q:
        raise ScoringError("run.responses_per_question is required to compute weighted relevant opportunities")

    question_appearances = entry.get("question_appearances", {})
    relevant_appearances = 0.0
    relevant_opportunities = 0.0
    covered = 0
    applicable_question_count = 0
    for qid, rel_entry in relevance_index.items():
        w = question_weight_for_business(rel_entry, applicable)
        if w <= 0:
            continue
        applicable_question_count += 1
        appearances = question_appearances.get(qid, 0)
        relevant_appearances += w * appearances
        relevant_opportunities += w * responses_per_q
        if appearances > 0:
            covered += 1

    visibility_rate = round((relevant_appearances / relevant_opportunities * 100), 1) if relevant_opportunities > 0 else 0.0
    visibility_score = band_visibility(visibility_rate)
    coverage = round(covered / applicable_question_count, 3) if applicable_question_count > 0 else 0.0
    return dict(
        relevant_appearances=round(relevant_appearances, 3),
        relevant_opportunities=round(relevant_opportunities, 3),
        visibility_rate=visibility_rate,
        visibility_score=visibility_score,
        question_coverage=coverage,
        scope_label=scope_label,
    )


def score_pool(run, entries):
    """entries: list of (array_name, index, entry_dict) for every market[]/
    outreach[] entry that has service_scope set. Mutates entry_dict in place
    with every derived field, returns the same list for ranking."""
    relevance_index = build_relevance_index(run)
    scope_index = build_scope_index(run)

    scored = []
    for array_name, i, entry in entries:
        vis = compute_visibility(entry, run, relevance_index, scope_index)
        if vis is None:
            continue
        for k in ("relevant_appearances", "relevant_opportunities", "visibility_rate", "visibility_score", "question_coverage"):
            entry[k] = vis[k]
        missing_values = [f for f in SCORED_VALUE_FIELDS if f not in entry]
        if missing_values:
            raise ScoringError(f"{entry.get('business')!r} has service_scope set but is missing value field(s) "
                                f"required before scoring: {missing_values}")
        scored.append((array_name, i, entry))

    # group top visibility rate + relative position, grouped by service_scope label
    group_top = {}
    group_size = {}
    for _, _, entry in scored:
        label = entry["service_scope"]
        group_top[label] = max(group_top.get(label, 0.0), entry["visibility_rate"])
        group_size[label] = group_size.get(label, 0) + 1
    for _, _, entry in scored:
        scope_label = entry["service_scope"]
        top = group_top[scope_label]
        entry["group_top_visibility_rate"] = top
        entry["relative_position"] = round(entry["visibility_rate"] / top, 3) if top > 0 else 0.0
        # A business that is the sole member of its service_scope in this
        # pool has no real peer to be "leading" - relative_position=1.0
        # against itself is not market leadership, per CAMPAIGN-HANDOFF.md
        # Section 3a's explicit rule that a business leading an extremely
        # weak (here, nonexistent) comparison group must not automatically
        # become DEFEND.
        entry["_has_comparable_peer"] = group_size[scope_label] >= 2

    for _, _, entry in scored:
        cred, vis_score = entry["business_credibility"], entry["visibility_score"]
        entry["gap_strength"] = clamp(cred - vis_score + 3, 0, 5)

        raw_points = sum(entry[field] * weight for field, weight in FINAL_SCORE_WEIGHTS.items())
        entry["final_score"] = round(raw_points / FINAL_SCORE_MAX_RAW * 100, 1)

        entry["overall_evidence_confidence"] = min(
            entry["business_credibility"], entry["decision_maker_identified"],
            entry["contact_identity_confidence"], entry["research_completeness"],
        )

        entry["business_verified"] = "YES" if cred >= BUSINESS_VERIFIED_MIN_CREDIBILITY else "REVIEW"
        entry["contact_route_verified"] = "YES" if entry["contact_route_quality"] >= CONTACT_ROUTE_VERIFIED_MIN_QUALITY else "REVIEW"
        dmid = entry["decision_maker_identified"]
        entry["named_decision_maker_verified"] = (
            "YES" if dmid >= NAMED_DM_VERIFIED_MIN else "PROBABLE" if dmid >= NAMED_DM_PROBABLE_MIN else "NO"
        )
        idconf = entry["contact_identity_confidence"]
        entry["identity_confidence"] = (
            "CONFIRMED" if idconf >= IDENTITY_CONFIRMED_MIN else
            "PROBABLE" if idconf == IDENTITY_PROBABLE_EXACT else
            "POSSIBLE" if idconf >= 1 else "UNKNOWN"
        )
        entry["research_complete"] = "YES" if entry["research_completeness"] >= RESEARCH_COMPLETE_MIN else "NO"
        entry["eligible_for_outreach"] = (
            "YES" if (entry["business_verified"] == "YES" and entry["contact_route_verified"] == "YES"
                      and entry["commercial_fit"] >= ELIGIBLE_MIN_FIT and entry["service_relevance"] >= ELIGIBLE_MIN_RELEVANCE)
            else "REVIEW"
        )
        ready = (entry["eligible_for_outreach"] == "YES" and dmid >= READY_MIN_DM_IDENTIFIED
                 and idconf >= READY_MIN_IDENTITY_CONFIDENCE and entry["research_complete"] == "YES"
                 and entry["overall_evidence_confidence"] >= READY_MIN_EVIDENCE_CONFIDENCE)
        entry["_ready_recommendation"] = "YES" if ready else "REVIEW"
        if array_name == "outreach":
            entry["ready_to_email"] = entry["_ready_recommendation"]

        entry["accessibility_grade"] = ACCESSIBILITY_GRADE_BY_DM_ROUTE[entry["direct_dm_route"]]

        relpos, cov = entry["relative_position"], entry["question_coverage"]
        if (entry["_has_comparable_peer"] and vis_score >= DEFEND_MIN_VISIBILITY_SCORE
                and relpos >= DEFEND_MIN_RELATIVE_POSITION and cov >= DEFEND_MIN_QUESTION_COVERAGE):
            opp = "DEFEND"
        elif cred >= GAP_MIN_CREDIBILITY and vis_score <= GAP_MAX_VISIBILITY_SCORE:
            opp = "GAP"
        elif vis_score == 0 and cred < GAP_MIN_CREDIBILITY:
            opp = "REVIEW"
        else:
            opp = "GROWTH"
        entry["opportunity_type"] = opp

        if entry["eligible_for_outreach"] != "YES" or entry["research_complete"] != "YES":
            priority = "REVIEW"
        elif entry["final_score"] >= PRIORITY_A_MIN_SCORE:
            priority = "A"
        elif entry["final_score"] >= PRIORITY_B_MIN_SCORE:
            priority = "B"
        else:
            priority = "C"
        entry["_priority_recommendation"] = priority
        if array_name == "outreach":
            entry["priority"] = priority
            entry["disposition_recommendation"] = "OUTREACH" if entry["eligible_for_outreach"] == "YES" else "REVIEW"

    # nearest same-scope competitor + leadership evidence text
    for _, _, entry in scored:
        peers = [e for _, _, e in scored if e is not entry and e["service_scope"] == entry["service_scope"]]
        if not peers:
            entry["nearest_competitor"] = ""
            entry["leadership_evidence"] = "No comparable same-scope competitor in this pool."
            continue
        nearest = min(peers, key=lambda p: abs(p["visibility_rate"] - entry["visibility_rate"]))
        entry["nearest_competitor"] = nearest["business"]
        leader = max(peers + [entry], key=lambda p: p["visibility_rate"])
        if leader is entry:
            runner_up = max(peers, key=lambda p: p["visibility_rate"])
            lead = entry["visibility_rate"] - runner_up["visibility_rate"]
            entry["leadership_evidence"] = (
                f"Leads its service-scope group at {entry['visibility_rate']}% relevance-normalized visibility, "
                f"{lead:.1f}pp ahead of {runner_up['business']} ({runner_up['visibility_rate']}%). "
                f"Question coverage {entry['question_coverage']*100:.0f}%."
            )
        else:
            trail = leader["visibility_rate"] - entry["visibility_rate"]
            entry["leadership_evidence"] = (
                f"Trails its service-scope group leader {leader['business']} ({leader['visibility_rate']}%) "
                f"by {trail:.1f}pp, at {entry['relative_position']*100:.0f}% of the leader's rate. "
                f"Question coverage {entry['question_coverage']*100:.0f}%."
            )

    # Mandatory narrative generation - runs for every scored outreach[] entry,
    # every time score_pool() runs, using the final structured values just
    # computed above (opportunity_type, nearest_competitor, and everything
    # else). Not an optional step a caller might forget: regeneration is
    # forced whenever narrative_signature(entry) no longer matches what's
    # stored, so a re-score (e.g. a corrected mention count) can never leave
    # a stale narrative behind merely because the field was already
    # non-empty. A signature match means the narrative is already current -
    # possibly hand-refined afterward with real evidence on top of the
    # generated baseline - and is left untouched; build_workbook.py's
    # detect_narrative_contradictions() is the separate, independent check
    # that such a hand-edit didn't introduce a numeric contradiction.
    # market[] entries are excluded: competitive_gap_finding/why_prospect
    # are not valid market_entry properties in schema.json.
    for array_name, _, entry in scored:
        if array_name != "outreach":
            continue
        current_sig = narrative_signature(entry)
        if entry.get("narrative_generated_from") != current_sig:
            entry["competitive_gap_finding"] = generate_competitive_gap_finding(entry, run)
            entry["why_prospect"] = generate_why_prospect(entry, run)
            entry["narrative_generated_from"] = current_sig

    tiebreak_key = lambda e: (-e["final_score"], -e["gap_strength"], -e["business_credibility"], -e["visibility_score"], e["business"])
    overall_ordered = sorted((e for _, _, e in scored), key=tiebreak_key)
    for i, entry in enumerate(overall_ordered, 1):
        entry["overall_rank"] = i

    ready_ordered = sorted((e for _, _, e in scored if e.get("_ready_recommendation") == "YES"), key=tiebreak_key)
    for i, entry in enumerate(ready_ordered, 1):
        entry["outreach_rank"] = i

    for _, _, entry in scored:
        entry.pop("_ready_recommendation", None)
        entry.pop("_priority_recommendation", None)
        entry.pop("_has_comparable_peer", None)

    return scored


def run_engine(data):
    run = data["run"]
    entries = []
    for i, e in enumerate(data.get("market", [])):
        entries.append(("market", i, e))
    for i, e in enumerate(data.get("outreach", [])):
        entries.append(("outreach", i, e))
    scored = score_pool(run, entries)
    return len(scored)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", help="Path to write the scored campaign JSON")
    ap.add_argument("--in-place", action="store_true", help="Overwrite --input instead")
    args = ap.parse_args()
    if not args.output and not args.in_place:
        print("Specify --output PATH or --in-place", file=sys.stderr)
        sys.exit(2)

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    try:
        n = run_engine(data)
    except ScoringError as e:
        print(f"Scoring error: {e}", file=sys.stderr)
        sys.exit(1)

    out_path = args.input if args.in_place else args.output
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Scored {n} candidate(s). Wrote {out_path}")


if __name__ == "__main__":
    main()
