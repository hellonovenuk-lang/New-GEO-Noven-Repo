#!/usr/bin/env python3
"""
Benchmark metrics — one named client, measured against the businesses the
assistants actually named beside it.

Turns a completed `tools/trade-run/` CSV plus a `mention-counts.json` into
`baseline.json`: the machine-readable record a Monthly Review is diffed
against. Everything here is mechanical. No judgement, no research, no
network. Reading what the numbers mean is the analyst's job and happens in
the report.

  python3 benchmark_metrics.py --run ~/wardith-runs/<slug>.csv \
      --questions <questions>.csv \
      --mention-counts ~/wardith-runs/<slug>/mention-counts.json \
      --client "Example Ltd" --out ~/wardith-runs/<slug>/baseline.json

**Bands, never a composite score.** `playbook/decisions.md`: no score out of
ten, no visibility index, no percentage as a headline. A band only means
anything against a fixed number of runs, so a band is reported per question
per assistant — where the denominator genuinely is `--runs-per-question` —
and never invented for an aggregate. Aggregates carry raw counts, a rate,
and how many of the underlying cells sat in each band.

**Why this does not emit GAP / GROWTH / DEFEND.** Those are prospecting
labels: they describe a commercial opportunity to approach a stranger, and
two of the three thresholds behind them depend on `business_credibility`,
a research judgement about whether a business is real and trading. An
agency's existing client is not a stranger and needs no such judgement. So
this reuses `scoring_engine.py`'s *visibility* thresholds directly — imported,
not copied, so they cannot drift — and reports a `visibility_shape` of
LEADING / COMPETITIVE / BEHIND / ABSENT instead.

Stdlib only, Python 3.9+.
"""

import argparse
import csv
import json
import os
import sys
from collections import defaultdict
from datetime import date

# Import the thresholds rather than restating them. If CAMPAIGN-HANDOFF.md
# Section 3a's methodology is revised, this file follows automatically —
# a second copy of the numbers would quietly disagree instead.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "prospect-compiler"))
from scoring_engine import (  # noqa: E402
    band_visibility,
    DEFEND_MIN_VISIBILITY_SCORE,
    DEFEND_MIN_RELATIVE_POSITION,
    DEFEND_MIN_QUESTION_COVERAGE,
)

# playbook/audit-process.md, "Bands, never percentages". Five runs
# distinguishes never from sometimes from usually and nothing finer.
BANDS = [
    (0, 0, "Never appeared"),
    (1, 2, "Occasionally"),
    (3, 4, "Often"),
    (5, 5, "Consistently"),
]

# The high-intent subset defaults to these two categories: the questions where
# a customer has described work they want done rather than browsing. The agency
# can override with --high-intent when their client's own priorities differ.
DEFAULT_HIGH_INTENT_CATEGORIES = ("qualified-discovery", "buying-intent")

# A question whose own wording names the client is a prompted question: the
# assistant was handed the name and used it. Counting that as visibility
# inflates the headline with an artefact of the question set.
#
# playbook/audit-process.md's wording rule 3 says no business name outside the
# named-business pair, but its own q08 template ("Who are the main alternatives
# to {business}...") is a comparison question that does name the business.
# Both readings are defensible - a comparison question genuinely needs the name
# to mean anything - so this splits rather than forbids: prompted questions are
# measured and reported, just never inside the unprompted headline. The split
# is recorded per question so it can be checked, not assumed.
PROMPTED_CATEGORIES = ("named-business",)

# Suffixes stripped when checking whether a question's text names the client,
# so "Sampleford Glazing" in a question is recognised as naming
# "Sampleford Glazing Ltd". Same idea as mention_count.py's alias generation,
# kept deliberately small because a false positive here silently removes a
# question from the headline.
LEGAL_SUFFIXES = (" limited", " ltd", " ltd.", " llp", " plc")


def band_for(appearances, runs_per_question):
    """A band is only meaningful against the fixed run count it was defined
    for. Anything else returns None rather than a stretched label."""
    if runs_per_question != 5:
        return None
    for low, high, label in BANDS:
        if low <= appearances <= high:
            return label
    return None


def question_names_client(question_text, category, client):
    """True where the assistant was handed the client's name in the question
    itself, by wording or by category."""
    if (category or "").strip() in PROMPTED_CATEGORIES:
        return True
    text = (question_text or "").lower()
    name = client.lower().strip()
    for suffix in LEGAL_SUFFIXES:
        if name.endswith(suffix):
            name = name[: -len(suffix)].strip()
            break
    return bool(name) and name in text


def load_questions(path):
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        raise SystemExit(f"{path} has no question rows.")
    return rows


def load_run(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_mention_counts(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return {k: v for k, v in data.items() if not k.startswith("_")}


def run_integrity(rows, questions, runs_per_question):
    """What actually came back, and whether it can be compared to anything.
    A model-version change is the one that matters most: per
    playbook/models-and-schemas.md a month-on-month comparison across a
    model change is not a comparison, so the string is recorded per provider
    and a provider carrying more than one is flagged here rather than
    averaged over."""
    successful, errored, smoke = [], 0, 0
    for row in rows:
        if "smoke" in (row.get("notes") or "").lower():
            smoke += 1
        elif (row.get("errors") or "").strip():
            errored += 1
        else:
            successful.append(row)

    versions = defaultdict(set)
    for row in successful:
        version = (row.get("model_version") or "").strip()
        if version:
            versions[row["assistant"]].add(version)

    providers = sorted(versions) or sorted({r["assistant"] for r in successful})
    expected = len(questions) * len(providers) * runs_per_question
    return successful, {
        "providers": providers,
        "model_versions": {p: sorted(versions.get(p, [])) for p in providers},
        "providers_with_mixed_model_versions": sorted(p for p in providers if len(versions.get(p, [])) > 1),
        "expected_responses": expected,
        "successful_responses": len(successful),
        "errored_rows": errored,
        "smoke_rows": smoke,
        "complete": len(successful) == expected and errored == 0 and smoke == 0,
    }


def appearances_by_identity(matched_rows):
    """(assistant, question_id) -> count of runs naming this business."""
    counts = defaultdict(int)
    for m in matched_rows:
        counts[(str(m.get("assistant", "")), str(m.get("question_id", "")))] += 1
    return counts


def summarise(appearances, opportunities):
    rate = round(appearances / opportunities * 100, 1) if opportunities else 0.0
    return {
        "appearances": appearances,
        "opportunities": opportunities,
        "rate_percent": rate,
        "visibility_score": band_visibility(rate),
    }


def build(run_rows, questions, counts, client, runs_per_question, high_intent_ids):
    successful, integrity = run_integrity(run_rows, questions, runs_per_question)
    providers = integrity["providers"]
    if not providers:
        raise SystemExit("No successful rows with a provider — nothing to measure.")
    if client not in counts:
        raise SystemExit(
            f"--client {client!r} is not in the mention counts. The peer census must "
            f"include the client itself. Present: {sorted(counts)}"
        )

    question_meta = {}
    for q in questions:
        qid = q["question_id"]
        category = (q.get("category") or "").strip()
        text = q.get("question_text", "")
        question_meta[qid] = {
            "question_id": qid,
            "category": category,
            "text": text,
            "high_intent": qid in high_intent_ids,
            "prompted": question_names_client(text, category, client),
        }
    unprompted_ids = {qid for qid, m in question_meta.items() if not m["prompted"]}
    if not unprompted_ids:
        raise SystemExit(
            "Every question in this set names the client, so there is no unprompted "
            "visibility to measure. A framework needs discovery questions that do not "
            "hand the assistant the name."
        )

    client_cells = appearances_by_identity(counts[client].get("matched_rows", []))

    per_question = []
    band_tally = defaultdict(int)
    for qid, meta in question_meta.items():
        by_provider = {}
        for provider in providers:
            got = client_cells.get((provider, qid), 0)
            band = band_for(got, runs_per_question)
            if band and not meta["prompted"]:
                band_tally[band] += 1
            by_provider[provider] = {
                "appearances": got,
                "opportunities": runs_per_question,
                "band": band,
            }
        total = sum(v["appearances"] for v in by_provider.values())
        row = dict(meta)
        row["by_provider"] = by_provider
        row.update(summarise(total, runs_per_question * len(providers)))
        row["providers_never_naming_client"] = sorted(
            p for p, v in by_provider.items() if v["appearances"] == 0)
        per_question.append(row)
    per_question.sort(key=lambda r: r["question_id"])

    def subset(predicate):
        rows = [r for r in per_question if predicate(r)]
        return summarise(
            sum(r["appearances"] for r in rows),
            sum(r["opportunities"] for r in rows),
        ) | {"questions": [r["question_id"] for r in rows]}

    # The headline is unprompted only. Prompted questions are reported beside
    # it, never folded into it.
    unprompted = [r for r in per_question if not r["prompted"]]
    overall = summarise(
        sum(r["appearances"] for r in unprompted),
        sum(r["opportunities"] for r in unprompted),
    )
    overall["basis"] = "unprompted questions only"
    overall["questions"] = [r["question_id"] for r in unprompted]
    overall["band_cell_counts"] = {label: band_tally.get(label, 0) for _, _, label in BANDS}
    prompted = subset(lambda r: r["prompted"])
    prompted["basis"] = "questions whose own wording names the client"

    by_provider = {}
    for provider in providers:
        got = sum(r["by_provider"][provider]["appearances"] for r in unprompted)
        by_provider[provider] = summarise(got, runs_per_question * len(unprompted))

    categories = sorted({r["category"] for r in unprompted if r["category"]})
    by_category = {c: subset(lambda r, c=c: r["category"] == c and not r["prompted"])
                   for c in categories}
    high_intent = subset(lambda r: r["high_intent"] and not r["prompted"])

    # The peer table. The census these counts were built from is the set of
    # businesses the answers themselves named, so this is "who the assistants
    # put in front of this client's customers", not a researched market list.
    #
    # Counted on the unprompted questions only, for the same reason the
    # headline is: a question that hands over the client's name is not a fair
    # denominator for anyone, and mixing the two would make the client's rank
    # a property of the question wording.
    total_opportunities = runs_per_question * len(unprompted) * len(providers)
    peers = []
    for business, entry in counts.items():
        cells = appearances_by_identity(entry.get("matched_rows", []))
        covered = sorted({qid for (_, qid), n in cells.items()
                          if n > 0 and qid in unprompted_ids})
        appearances = sum(n for (_, qid), n in cells.items() if qid in unprompted_ids)
        by_prov = {p: sum(n for (prov, qid), n in cells.items()
                          if prov == p and qid in unprompted_ids) for p in providers}
        peers.append({
            "business": business,
            "is_client": business == client,
            "appearances": appearances,
            "by_provider": by_prov,
            "questions_appeared_on": covered,
            "question_coverage": round(len(covered) / len(unprompted), 3) if unprompted else 0.0,
            "rate_percent": round(appearances / total_opportunities * 100, 1)
            if total_opportunities else 0.0,
        })
    peers.sort(key=lambda p: (-p["appearances"], p["business"]))
    for i, peer in enumerate(peers, 1):
        peer["rank"] = i

    client_row = next(p for p in peers if p["is_client"])
    others = [p for p in peers if not p["is_client"]]
    top_other = others[0] if others else None
    top_rate = top_other["rate_percent"] if top_other else 0.0
    relative_position = round(client_row["rate_percent"] / top_rate, 3) if top_rate > 0 else None

    coverage = client_row["question_coverage"]
    vis_score = overall["visibility_score"]
    if not others:
        shape = "NO_PEER"          # nobody else was named; nothing to compare against
    elif client_row["appearances"] == 0:
        shape = "ABSENT"
    elif (vis_score >= DEFEND_MIN_VISIBILITY_SCORE
          and relative_position is not None
          and relative_position >= DEFEND_MIN_RELATIVE_POSITION
          and coverage >= DEFEND_MIN_QUESTION_COVERAGE):
        shape = "LEADING"
    elif vis_score >= DEFEND_MIN_VISIBILITY_SCORE:
        shape = "COMPETITIVE"
    else:
        shape = "BEHIND"

    return {
        "schema": "wardith-benchmark-baseline/1",
        "generated": date.today().isoformat(),
        "client": client,
        "runs_per_question": runs_per_question,
        "question_count": len(per_question),
        "run": integrity,
        "unprompted_question_count": len(unprompted),
        "questions": [
            {k: v for k, v in q.items()
             if k in ("question_id", "category", "text", "high_intent", "prompted")}
            for q in per_question
        ],
        "client_visibility": {
            "overall": overall,
            "prompted": prompted,
            "by_provider": by_provider,
            "by_category": by_category,
            "high_intent": high_intent,
            "per_question": per_question,
            "question_coverage": coverage,
        },
        "peers": peers,
        "position": {
            "rank": client_row["rank"],
            "businesses_named": len(peers),
            "top_competitor": top_other["business"] if top_other else None,
            "top_competitor_appearances": top_other["appearances"] if top_other else None,
            "top_competitor_rate_percent": top_rate if top_other else None,
            "relative_position": relative_position,
            "visibility_shape": shape,
        },
        "thresholds_used": {
            "source": "tools/prospect-compiler/scoring_engine.py (imported, not copied)",
            "min_visibility_score": DEFEND_MIN_VISIBILITY_SCORE,
            "min_relative_position": DEFEND_MIN_RELATIVE_POSITION,
            "min_question_coverage": DEFEND_MIN_QUESTION_COVERAGE,
        },
    }


def render_text(b):
    v, pos = b["client_visibility"], b["position"]
    out = [
        f"{b['client']} — {b['question_count']} questions, "
        f"{b['runs_per_question']} runs, {len(b['run']['providers'])} assistants.",
        f"Run: {b['run']['successful_responses']}/{b['run']['expected_responses']} answers"
        + (" — COMPLETE" if b["run"]["complete"] else " — INCOMPLETE"),
    ]
    if b["run"]["providers_with_mixed_model_versions"]:
        out.append(
            "  WARNING: more than one model version recorded for "
            + ", ".join(b["run"]["providers_with_mixed_model_versions"])
            + " — this run cannot be compared month-on-month for those providers."
        )
    o, p = v["overall"], v["prompted"]
    nq = b["unprompted_question_count"]
    out.append("")
    out.append(f"Unprompted ({nq} of {b['question_count']} questions — the ones that do not "
               f"hand over the name):")
    out.append(f"  Named in {o['appearances']} of {o['opportunities']} answers ({o['rate_percent']}%).")
    out.append("  Band spread across question x assistant cells: " + ", ".join(
        f"{label} {n}" for label, n in o["band_cell_counts"].items()))
    out.append(f"  Appeared at least once on {round(v['question_coverage'] * nq)} of {nq}.")
    if p["opportunities"]:
        out.append(f"Prompted ({', '.join(p['questions'])}): named in {p['appearances']} of "
                   f"{p['opportunities']} answers ({p['rate_percent']}%). Reported separately, "
                   f"never inside the figure above.")
    out.append("")
    out.append("By assistant:")
    for provider, s in v["by_provider"].items():
        out.append(f"  {provider:<12} {s['appearances']:>3} of {s['opportunities']:>3}  ({s['rate_percent']}%)")
    out.append("")
    out.append("By question category:")
    for category, s in v["by_category"].items():
        out.append(f"  {category:<22} {s['appearances']:>3} of {s['opportunities']:>3}  ({s['rate_percent']}%)")
    h = v["high_intent"]
    out.append(f"  {'HIGH INTENT':<22} {h['appearances']:>3} of {h['opportunities']:>3}  ({h['rate_percent']}%)")
    out.append("")
    out.append("Per question ('*' high intent, '(prompted)' names the client in the question):")
    for q in v["per_question"]:
        flag = " *" if q["high_intent"] else "  "
        cells = "  ".join(f"{name} {d['appearances']}/{d['opportunities']}"
                          for name, d in q["by_provider"].items())
        tag = " (prompted)" if q["prompted"] else ""
        out.append(f" {flag}{q['question_id']} [{q['category']}] {cells}{tag}")
    out.append("")
    out.append(f"Position (unprompted questions only): rank {pos['rank']} of "
               f"{pos['businesses_named']} businesses named.")
    if pos["top_competitor"]:
        out.append(f"  Most-named: {pos['top_competitor']} "
                   f"({pos['top_competitor_appearances']} appearances, "
                   f"{pos['top_competitor_rate_percent']}%).")
        out.append(f"  Relative position: {pos['relative_position']}")
    out.append(f"  Visibility shape: {pos['visibility_shape']}")
    out.append("")
    out.append("Peer table:")
    for p in b["peers"]:
        mark = "<- client" if p["is_client"] else ""
        out.append(f"  {p['rank']:>2}. {p['business']:<40} {p['appearances']:>3}  "
                   f"({p['rate_percent']}%)  {mark}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True, help="Completed trade-run CSV")
    ap.add_argument("--questions", required=True, help="The frozen question CSV this run used")
    ap.add_argument("--mention-counts", required=True, help="mention-counts.json from tools/mention-count/")
    ap.add_argument("--client", required=True, help="The focal business, exactly as it appears in the counts")
    ap.add_argument("--runs-per-question", type=int, default=5,
                    help="Runs per question per assistant (default 5). Bands are only "
                         "emitted at 5, which is what they were defined against")
    ap.add_argument("--high-intent", default=None,
                    help="Comma-separated question ids for the high-intent subset. Defaults to "
                         "every question in the " + "/".join(DEFAULT_HIGH_INTENT_CATEGORIES) + " categories")
    ap.add_argument("--out", default=None, help="Write baseline.json here (outside this repo)")
    args = ap.parse_args()

    questions = load_questions(args.questions)
    if args.high_intent:
        high_intent = {q.strip() for q in args.high_intent.split(",") if q.strip()}
        known = {q["question_id"] for q in questions}
        unknown = high_intent - known
        if unknown:
            sys.exit(f"--high-intent names question ids not in the question file: {sorted(unknown)}")
    else:
        high_intent = {q["question_id"] for q in questions
                       if (q.get("category") or "").strip() in DEFAULT_HIGH_INTENT_CATEGORIES}

    baseline = build(
        load_run(args.run), questions, load_mention_counts(args.mention_counts),
        args.client, args.runs_per_question, high_intent,
    )
    print(render_text(baseline))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(baseline, fh, indent=2, ensure_ascii=False)
        print(f"\nWritten to {args.out}")


if __name__ == "__main__":
    main()
