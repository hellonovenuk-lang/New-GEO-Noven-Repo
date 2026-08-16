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
