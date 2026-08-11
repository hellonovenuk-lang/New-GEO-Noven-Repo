#!/usr/bin/env python3
"""
Name-collision check — does a candidate business name already belong to
somebody else in the eyes of the assistants?

This is the test the Noven audit accidentally ran. Two questions, asked of
all three assistants, twice each:

  "What do you know about {name}?"
  "Is {name} any good, and what do they do?"

The failure it is looking for is not "no answer". No answer is the GOOD
result for an unused name. The failure is a confident answer about a
business that isn't yours — the Noven Pharmaceuticals / Noven Build
problem, which cost nothing to discover here and a rebrand to discover
later.

Reads candidate names from names.txt, one per line. Blank lines and lines
starting with # are ignored, so you can keep rejected names in the file
with a # in front of them.

Sits next to audit_query.py and reuses its provider callers, so the UK
locale settings are identical to the ones the audit ran with.

Usage:
  python audit_query.py --help     # (env must already be loaded)
  python name_check.py             # reads names.txt, writes names-runs.csv
  python name_check.py --cap 60    # raise the safety cap
"""

import argparse
import csv
import os
import sys
import time
from datetime import datetime, timezone

# Reuses the audit's provider callers so the UK locale settings are identical
# to the ones the 2026-08-02 baseline ran with. That script is archived beside
# the audit it belongs to, not duplicated here — one copy, one behaviour.
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "audits", "noven-2026-08-02"))
try:
    from audit_query import CALLERS, PROVIDERS, FIELDS, append_row, ensure_header
except ImportError:
    sys.exit(
        "Can't find audit_query.py. Expected it at "
        "archive/audits/noven-2026-08-02/audit_query.py relative to this file."
    )

QUESTIONS = [
    ("n1", "What do you know about {name}?"),
    ("n2", "Is {name} any good, and what do they do?"),
]

RUNS_PER_QUESTION = 2


def load_names(path):
    if not os.path.exists(path):
        sys.exit(
            f"No {path} found. Make a plain text file called {path} in this "
            f"folder with one candidate name per line, then run this again."
        )
    names = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                names.append(line)
    if not names:
        sys.exit(f"{path} has no names in it (blank lines and # lines don't count).")
    return names


def load_done(path):
    done = set()
    if os.path.exists(path):
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("errors"):
                    continue
                done.add((row["assistant"], row["question_id"], row["run_no"]))
    return done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--names", default="names.txt")
    ap.add_argument("--out", default="names-runs.csv")
    ap.add_argument("--cap", type=int, default=60,
                    help="Hard cap on total queries this invocation")
    args = ap.parse_args()

    names = load_names(args.names)
    done = load_done(args.out)
    ensure_header(args.out)

    total = len(names) * len(QUESTIONS) * RUNS_PER_QUESTION * len(PROVIDERS)
    if total > args.cap:
        sys.exit(
            f"Planned {total} queries exceeds cap {args.cap} — stopping before "
            f"the first call. Either cut names.txt down or pass a higher --cap."
        )

    print(f"{len(names)} name(s): {', '.join(names)}")
    print(f"Plan: {total} queries across {len(PROVIDERS)} providers. Cap {args.cap}.")

    count = 0
    for provider in PROVIDERS:
        caller = CALLERS[provider]
        for name in names:
            slug = "".join(c.lower() if c.isalnum() else "-" for c in name).strip("-")
            for qid, template in QUESTIONS:
                question = template.format(name=name)
                for run_no in range(1, RUNS_PER_QUESTION + 1):
                    question_id = f"{slug}-{qid}"
                    key = (provider, question_id, str(run_no))
                    if key in done:
                        print(f"skip (already in {args.out}): {key}")
                        continue
                    count += 1
                    print(f"[{count}/{total}] {provider} {question_id} run {run_no}")
                    try:
                        model_version, answer, sources = caller(question)
                        errors = ""
                    except Exception as e:  # noqa: BLE001 — log and keep going
                        model_version, answer, sources = "", "", []
                        errors = repr(e)
                        print(f"  ERROR: {e}", file=sys.stderr)
                    append_row(args.out, {
                        "audit_id": "name-check",
                        "client": name,
                        "run_at": datetime.now(timezone.utc).isoformat(),
                        "assistant": provider,
                        "surface": "api",
                        "model_version": model_version,
                        "question_id": question_id,
                        "run_no": run_no,
                        "outcome": "",
                        "competitors": "",
                        "errors": errors,
                        "sources_cited": ";".join(sources),
                        "answer_text": answer,
                        "notes": question,
                    })
                    time.sleep(0.5)

    print("\nDone. Open names-runs.csv and read the answer_text column.")
    print("What you're looking for, per name:")
    print("  - Nothing found / 'I don't have information'  = clear, the name is free")
    print("  - A confident answer about a different business = collision, reject it")
    print("  - Sources cited from a real company site        = collision, reject it")


if __name__ == "__main__":
    main()
