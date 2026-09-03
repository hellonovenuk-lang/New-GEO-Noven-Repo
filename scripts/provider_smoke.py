#!/usr/bin/env python3
"""Fixed three-provider cloud smoke test; no agent, CRM or mail operations."""
import argparse
import csv
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "trade-run"))
import trade_run as runner


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path, help="New directory in the private data checkout")
    args = parser.parse_args(argv)
    # Validate all credentials before the first paid request. Print names only.
    for provider in ("OPENAI", "GEMINI", "PERPLEXITY"):
        runner.env(provider + "_API_KEY")
        runner.env(provider + "_MODEL")
    try:
        args.out.mkdir(parents=True, exist_ok=False)
    except OSError as error:
        print(f"Cannot create a new smoke result directory ({type(error).__name__}); no requests made.", file=sys.stderr)
        return 2
    results = args.out / "results.csv"
    code = runner.main([
        "--questions", str(ROOT / "tools/trade-run/questions-wirral-dentists.csv"),
        "--out", str(results), "--client", "smoke-only-wirral-dentists",
        "--location", "Wirral", "--audit-id", "provider-smoke",
        "--smoke", "--cap", "3",
    ])
    with results.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    providers = [{
        "provider": row["assistant"], "model": row["model_version"],
        "passed": not row["errors"] and bool(row["answer_text"].strip()) and bool(row["sources_cited"]),
        "source_count": len(set(filter(None, row["sources_cited"].split(";")))),
    } for row in rows]
    passed = code == 0 and [row["provider"] for row in providers] == ["openai", "gemini", "perplexity"] and all(row["passed"] for row in providers)
    summary = {"passed": passed, "providers": providers}
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    for item in providers:
        print(f"{item['provider']}: {'PASS' if item['passed'] else 'FAIL'}, sources={item['source_count']}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
