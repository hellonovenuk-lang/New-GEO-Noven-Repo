#!/usr/bin/env python3
"""
Validates a trade_run.py output CSV against the plan implied by its own
questions CSV. Generalises the manual health-check performed by hand on the
first real run (estate-agents-chester, 2026-08) into something repeatable.

This script only reads. It never writes to the run CSV, never calls a
provider API, and never makes a judgement call about who was named — that
stays human/qualification-stage work, per playbook/models-and-schemas.md.

Exit code 0 = clean (every planned identity present, no problems).
Exit code 1 = incomplete or problems found - see the printed detail.

Usage:
    python3 validate_run.py --csv <path> --questions <path> [--runs 5]
"""
import argparse
import csv
import sys
from collections import Counter

PROVIDERS = ["openai", "gemini", "perplexity"]


def load_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="trade_run.py output CSV to validate")
    ap.add_argument("--questions", required=True, help="the questions CSV the run was planned from")
    ap.add_argument("--runs", type=int, default=5, help="runs per question per provider (default 5, matches the established 6x3x5=90 shape)")
    args = ap.parse_args()

    questions = load_csv(args.questions)
    if not questions:
        sys.exit(f"FAIL: no questions found in {args.questions}")
    question_ids = [q["question_id"] for q in questions]
    expected_total = len(question_ids) * len(PROVIDERS) * args.runs

    rows = load_csv(args.csv)

    problems = []
    notes = []

    # Smoke-row leakage
    smoke_rows = [r for r in rows if "smoke" in (r.get("notes") or "").lower()]
    if smoke_rows:
        problems.append(f"{len(smoke_rows)} smoke-tagged row(s) still present - delete before this run counts as final.")
    live_rows = [r for r in rows if r not in smoke_rows]

    # Row count
    if len(live_rows) != expected_total:
        problems.append(f"Row count {len(live_rows)} != expected {expected_total} ({len(question_ids)} questions x {len(PROVIDERS)} providers x {args.runs} runs).")

    # Provider distribution
    provider_counts = Counter(r.get("assistant", "") for r in live_rows)
    for p in PROVIDERS:
        expected_p = len(question_ids) * args.runs
        got = provider_counts.get(p, 0)
        if got != expected_p:
            problems.append(f"Provider '{p}': {got} rows, expected {expected_p}.")
    unknown_providers = set(provider_counts) - set(PROVIDERS)
    if unknown_providers:
        problems.append(f"Unexpected provider value(s) in 'assistant' column: {sorted(unknown_providers)}.")

    # Question distribution
    question_counts = Counter(r.get("question_id", "") for r in live_rows)
    expected_per_q = len(PROVIDERS) * args.runs
    for qid in question_ids:
        got = question_counts.get(qid, 0)
        if got != expected_per_q:
            problems.append(f"Question '{qid}': {got} rows, expected {expected_per_q}.")
    unknown_questions = set(question_counts) - set(question_ids)
    if unknown_questions:
        problems.append(f"Row(s) reference question_id(s) not in the questions file: {sorted(unknown_questions)}.")

    # run_no distribution
    run_no_counts = Counter(r.get("run_no", "") for r in live_rows)
    expected_per_run = len(question_ids) * len(PROVIDERS)
    for n in range(1, args.runs + 1):
        got = run_no_counts.get(str(n), 0)
        if got != expected_per_run:
            problems.append(f"run_no {n}: {got} rows, expected {expected_per_run}.")

    # Duplicate successful identities: (assistant, question_id, run_no) must be unique among rows with no error
    successful = [r for r in live_rows if not r.get("errors")]
    key_counts = Counter((r.get("assistant"), r.get("question_id"), r.get("run_no")) for r in successful)
    dups = {k: v for k, v in key_counts.items() if v > 1}
    if dups:
        problems.append(f"Duplicate successful (assistant, question_id, run_no) identities: {dups}")

    # Errored rows. A physical row existing for every planned identity is not
    # enough - trade_run.py's own resume logic only treats a row as "done"
    # when it has no error, so an unretried errored row means the dataset is
    # short a real answer even though the row count looks right. Treat this
    # as blocking: it is exactly the gap an automatic retry pass exists to
    # close, and the orchestrating skill decides whether to retry or stop
    # based on this verdict.
    errored = [r for r in live_rows if r.get("errors")]
    if errored:
        problems.append(f"{len(errored)} errored row(s) with no successful retry yet - successful count {len(successful)} < planned {expected_total}.")
        for r in errored:
            notes.append(f"  errored: {r.get('assistant')} / {r.get('question_id')} / run {r.get('run_no')}: {r.get('errors')[:200]}")

    # Empty answer_text on a row with no error is a real (if odd) result - flag, don't fail
    empty_ok = [r for r in successful if not (r.get("answer_text") or "").strip()]
    if empty_ok:
        notes.append(f"{len(empty_ok)} successful row(s) have empty answer_text (no error recorded) - verify this is a genuine ungrounded response, not silent data loss.")

    # Empty sources_cited on a successful row - grounding may not have fired
    no_sources = [r for r in successful if not (r.get("sources_cited") or "").strip()]
    if no_sources:
        by_provider = Counter(r.get("assistant") for r in no_sources)
        notes.append(f"{len(no_sources)} successful row(s) with no sources_cited (by provider: {dict(by_provider)}) - not a failure by itself, but worth a look if concentrated in one provider.")

    # Model version consistency per provider
    model_versions = {}
    for p in PROVIDERS:
        versions = {r.get("model_version") for r in successful if r.get("assistant") == p and r.get("model_version")}
        model_versions[p] = sorted(versions)
        if len(versions) > 1:
            problems.append(f"Provider '{p}' recorded more than one model_version in this run: {sorted(versions)} - a mid-run model change makes counts non-comparable.")
        elif not versions:
            notes.append(f"Provider '{p}' has no successful rows with a model_version recorded.")

    completeness_pct = 100.0 * len(successful) / expected_total if expected_total else 0.0

    print(f"Run:        {args.csv}")
    print(f"Questions:  {args.questions}  ({len(question_ids)} questions: {', '.join(question_ids)})")
    print(f"Plan:       {expected_total} queries ({len(question_ids)} x {len(PROVIDERS)} providers x {args.runs} runs)")
    print(f"Rows found: {len(live_rows)} live" + (f" (+ {len(smoke_rows)} smoke rows present)" if smoke_rows else ""))
    print(f"Successful: {len(successful)}/{expected_total} ({completeness_pct:.1f}%)")
    print(f"Errored:    {len(errored)}")
    print(f"Model versions recorded: {model_versions}")

    if notes:
        print("\n--- Notes (non-blocking) ---")
        for n in notes:
            print(n)

    if problems:
        print("\n--- PROBLEMS (blocking) ---")
        for p in problems:
            print(f"- {p}")
        print(f"\nVERDICT: INCOMPLETE - {len(problems)} problem(s) found.")
        sys.exit(1)
    else:
        print("\nVERDICT: PASS - every planned identity present, no structural problems.")
        sys.exit(0)


if __name__ == "__main__":
    main()
