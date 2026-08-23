#!/usr/bin/env python3
"""
Builds the benchmark test fixture: a 90-row synthetic trade-run CSV shaped
exactly like real `tools/trade-run/` output, plus its question file and peer
census.

Checked in alongside its own output so the fixture is reproducible and
auditable rather than 90 hand-typed rows nobody can verify. Run it from this
directory:

    python3 make_fixture.py

**Every business, place and domain here is invented**, on the `.example` TLD
reserved by RFC 2606 so no row can accidentally point at a real site. Same
convention as `tools/prospect-compiler/sample/sample-campaign.json` — this
repo is written as though public and holds no real client or prospect name.

The data is shaped to exercise the findings the product has to be able to
produce, not to flatter it:

- the client is named on discovery, almost never on the high-intent
  questions, which is the gap an SEO team can act on;
- one assistant carries most of its visibility and another barely names it;
- one competitor is named far more often, on more questions;
- the client's own domain is cited only when it is asked about by name,
  never on a discovery answer;
- two directory domains are cited repeatedly beside a competitor and never
  beside the client.
"""

import csv
import os
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, "fixtures")

CLIENT = "Sampleford Glazing Ltd"
AREA = "Sampleford"
SLUG = "sampleford-glazing"
AUDIT_ID = f"{SLUG}-2026-08-19"

PROVIDERS = [
    ("openai", "gpt-5.6-luna-2026-05-01"),
    ("gemini", "gemini-3.6-flash"),
    ("perplexity", "sonar"),
]
RUNS = 5

QUESTIONS = [
    ("q01", "discovery", "Who's a good double glazing company in Sampleford?"),
    ("q02", "discovery", "Can you recommend someone near Sampleford to replace old windows?"),
    ("q03", "qualified-discovery", "Which double glazing companies in Sampleford do sash window replacements?"),
    ("q04", "buying-intent", "My conservatory roof leaks every winter. Who do I call in Sampleford?"),
    ("q05", "comparison", "Who are the main alternatives to Sampleford Glazing in the Sampleford area?"),
    ("q06", "named-business", "What do you know about Sampleford Glazing?"),
]

PEERS = [
    CLIENT,
    "Northgate Windows Ltd",
    "Meadowbank Glass Ltd",
    "Fictional Conservatories Ltd",
    "Testville Window Repairs Ltd",
]

# (question_id, provider) -> {business: [run numbers naming it]}
NAMED = {
    ("q01", "openai"): {CLIENT: [1, 2, 4], "Northgate Windows Ltd": [1, 2, 3, 4, 5], "Meadowbank Glass Ltd": [2, 5]},
    ("q01", "gemini"): {"Northgate Windows Ltd": [1, 2, 3, 4, 5], "Meadowbank Glass Ltd": [1, 3, 4]},
    ("q01", "perplexity"): {CLIENT: [3], "Northgate Windows Ltd": [1, 2, 3, 4], "Fictional Conservatories Ltd": [2, 5]},

    ("q02", "openai"): {CLIENT: [1, 3], "Northgate Windows Ltd": [1, 2, 3, 4, 5], "Testville Window Repairs Ltd": [4]},
    ("q02", "gemini"): {"Northgate Windows Ltd": [1, 2, 3, 5], "Meadowbank Glass Ltd": [2, 4]},
    ("q02", "perplexity"): {CLIENT: [2], "Northgate Windows Ltd": [1, 2, 3, 4, 5], "Meadowbank Glass Ltd": [3]},

    # The high-intent pair. The client is absent from both on every assistant
    # bar one run, while two competitors are named consistently.
    ("q03", "openai"): {"Northgate Windows Ltd": [1, 2, 3, 4, 5], "Meadowbank Glass Ltd": [1, 2, 4, 5]},
    ("q03", "gemini"): {"Northgate Windows Ltd": [1, 2, 3, 4], "Meadowbank Glass Ltd": [1, 2, 3, 5]},
    ("q03", "perplexity"): {"Northgate Windows Ltd": [1, 2, 3, 4, 5], "Meadowbank Glass Ltd": [2, 3]},

    ("q04", "openai"): {"Northgate Windows Ltd": [1, 2, 4, 5], "Fictional Conservatories Ltd": [1, 2, 3, 4, 5]},
    ("q04", "gemini"): {"Fictional Conservatories Ltd": [1, 2, 3, 4, 5], "Northgate Windows Ltd": [2, 3]},
    ("q04", "perplexity"): {CLIENT: [4], "Fictional Conservatories Ltd": [1, 2, 3, 4, 5], "Northgate Windows Ltd": [1, 5]},

    ("q05", "openai"): {CLIENT: [1, 2, 3, 4, 5], "Northgate Windows Ltd": [1, 2, 3, 4, 5], "Meadowbank Glass Ltd": [1, 2, 3]},
    ("q05", "gemini"): {CLIENT: [1, 2, 3, 4, 5], "Northgate Windows Ltd": [1, 2, 3, 4, 5], "Testville Window Repairs Ltd": [2, 4]},
    ("q05", "perplexity"): {CLIENT: [1, 2, 3, 4, 5], "Northgate Windows Ltd": [1, 2, 3, 4], "Meadowbank Glass Ltd": [1, 5]},

    ("q06", "openai"): {CLIENT: [1, 2, 3, 4, 5]},
    ("q06", "gemini"): {CLIENT: [1, 2, 4]},
    ("q06", "perplexity"): {CLIENT: [1, 2, 3, 4, 5]},
}

CLIENT_DOMAIN = "sampleford-glazing.example"

# (question_id, provider) -> domains cited on every run of that cell.
SOURCES = {
    ("q01", "openai"): ["bestof-sampleford.example", "northgatewindows.example"],
    ("q01", "gemini"): ["bestof-sampleford.example", "which-glazing.example"],
    ("q01", "perplexity"): ["trustedtraders.example", "northgatewindows.example"],
    ("q02", "openai"): ["bestof-sampleford.example", "trustedtraders.example"],
    ("q02", "gemini"): ["which-glazing.example", "northgatewindows.example"],
    ("q02", "perplexity"): ["trustedtraders.example", "bestof-sampleford.example"],
    ("q03", "openai"): ["sashwindow-guide.example", "northgatewindows.example"],
    ("q03", "gemini"): ["sashwindow-guide.example", "which-glazing.example"],
    ("q03", "perplexity"): ["sashwindow-guide.example", "meadowbankglass.example"],
    ("q04", "openai"): ["conservatory-repairs.example", "trustedtraders.example"],
    ("q04", "gemini"): ["conservatory-repairs.example"],
    ("q04", "perplexity"): ["conservatory-repairs.example", "which-glazing.example"],
    ("q05", "openai"): ["bestof-sampleford.example", "northgatewindows.example"],
    ("q05", "gemini"): ["which-glazing.example", "northgatewindows.example"],
    ("q05", "perplexity"): ["trustedtraders.example", "northgatewindows.example"],
    # Only when asked by name does anything cite the client's own site.
    ("q06", "openai"): [CLIENT_DOMAIN, "companies-register.example"],
    ("q06", "gemini"): [CLIENT_DOMAIN],
    ("q06", "perplexity"): [CLIENT_DOMAIN, "trustedtraders.example"],
}

FIELDS = [
    "audit_id", "client", "run_at", "assistant", "surface", "model_version",
    "question_id", "run_no", "errors",
    "sources_cited", "answer_text", "notes",
]


def answer_text(named_here, question_text):
    """Readable prose naming exactly the businesses this cell names, so
    mention_count.py has real text to match against rather than a name list.

    The no-business answer deliberately does not quote the question back. An
    earlier version did, and on the two questions whose own wording names the
    client that echo registered as a mention — which is exactly the artefact
    benchmark_metrics.py's prompted/unprompted split exists to handle, and
    not something the fixture should also smuggle in by accident."""
    del question_text
    if not named_here:
        return (f"There are several firms in {AREA} that do this, "
                f"though I don't have a specific one to point you at.")
    if len(named_here) == 1:
        return (f"{named_here[0]} is the one that comes up most for this in {AREA}. "
                f"Worth checking recent reviews before you commit.")
    body = ", ".join(named_here[:-1]) + f" and {named_here[-1]}"
    return (f"In {AREA}, {body} are the names that come up for this. "
            f"{named_here[0]} is mentioned most consistently.")


def main():
    os.makedirs(FIXTURES, exist_ok=True)
    stamp = datetime(2026, 8, 19, 9, 0, tzinfo=timezone.utc)

    with open(os.path.join(FIXTURES, f"questions-{SLUG}.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["audit_id", "question_id", "category", "question_text", "frozen_from"])
        for qid, category, text in QUESTIONS:
            w.writerow([AUDIT_ID, qid, category, text, ""])

    with open(os.path.join(FIXTURES, f"census-{SLUG}.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["business", "area"])
        for business in PEERS:
            w.writerow([business, AREA])

    rows = []
    for qid, _category, text in QUESTIONS:
        for provider, model in PROVIDERS:
            named_map = NAMED.get((qid, provider), {})
            for run_no in range(1, RUNS + 1):
                named_here = [b for b, runs in named_map.items() if run_no in runs]
                rows.append({
                    "audit_id": AUDIT_ID,
                    "client": SLUG,
                    "run_at": stamp.isoformat(),
                    "assistant": provider,
                    "surface": "api",
                    "model_version": model,
                    "question_id": qid,
                    "run_no": run_no,
                    "errors": "",
                    "sources_cited": ";".join(
                        f"https://{d}/{qid}-{run_no}" for d in SOURCES.get((qid, provider), [])),
                    "answer_text": answer_text(named_here, text),
                    "notes": "",
                })

    out = os.path.join(FIXTURES, f"run-{SLUG}.csv")
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} rows written to {out}")


if __name__ == "__main__":
    main()
