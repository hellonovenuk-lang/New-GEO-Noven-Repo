#!/usr/bin/env python3
"""
Mention count — matches a market census against a completed trade-run CSV,
producing per-business AI-mention counts by provider and question.

Generalised from the matching logic proven on two real runs:
wardith-runs/estate-agents-wirral/crossref.py (the original — name-variant
handling for &/and, apostrophes, Ltd/Estate Agents suffixes) and its Chester
evolution (adds a stopword floor so a stripped-down variant can't collapse
into a common word, a manual-override file for a model's own misspellings,
per-question counts, and skips errored rows). This script is that second
version, with the hardcoded paths and Chester-only stopword replaced by
flags so it works against any completed run.

Nothing here decides who is a prospect. It counts mentions; the qualification
skill and CAMPAIGN-HANDOFF.md do the judgement.

Stdlib only, no pip install needed. Requires Python 3.9+.

Usage:
  python3 mention_count.py --run ~/wardith-runs/{trade}-{area}.csv \
      --census market-census-{trade}-{area}.csv --area {area} \
      --out mention-counts.json

  # with a model-misspelling override file (see --variants-file below):
  python3 mention_count.py --run ... --census ... --area {area} \
      --out ... --variants-file variant-overrides.json
"""

import argparse
import csv
import json
import re
import sys
from collections import Counter

# Generic stopwords a suffix-stripped variant can collapse into — matched
# against real false positives found on the Wirral and Chester runs (e.g.
# "Home Estate Agents" stripping to "Home" matched almost every answer).
GENERIC_STOPWORDS = {
    "home", "homes", "property", "properties", "estate", "estates",
    "agents", "agent", "group", "key", "let", "lets", "letting",
    "lettings", "move", "rent", "centre", "center", "house", "houses",
    "residential", "management", "services", "sales", "premium",
    "the", "partnership", "partners",
}


def variants(brand, extra_stopwords):
    v = {brand.strip()}
    base_noparen = re.sub(r"\s*\([^)]*\)", "", brand).strip()
    v.add(base_noparen)
    for b in [brand.strip(), base_noparen]:
        v.add(b.replace(" & ", " and "))
        v.add(b.replace(" and ", " & "))
    more = set()
    for b in list(v):
        more.add(re.sub(r"\s+Ltd\.?$", "", b, flags=re.I))
        more.add(re.sub(r"\s+Limited$", "", b, flags=re.I))
        more.add(re.sub(r"\s+LLP$", "", b, flags=re.I))
        more.add(re.sub(r"\s+Estate Agents?$", "", b, flags=re.I))
        more.add(re.sub(r"\s+Estates?$", "", b, flags=re.I))
        more.add(re.sub(r"\s+Property( Group)?$", "", b, flags=re.I))
        more.add(re.sub(r"\s+Sales( & | and )Lettings$", "", b, flags=re.I))
    v |= more
    stopwords = GENERIC_STOPWORDS | extra_stopwords
    safe = {x.strip() for x in v if x.strip() and len(x.strip()) > 2}
    safe = {x for x in safe if x.lower() not in stopwords}
    return safe


def to_pattern(v):
    # straight and curly apostrophes are equivalent; single-pass substitution
    # so it doesn't rescan and corrupt the bracket expression it just inserted
    esc = re.escape(v)
    esc = re.sub(r"'|’", "['’]", esc)
    return re.compile(esc, re.I)


def load_census(path, business_column):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if rows and business_column not in rows[0]:
        sys.exit(
            f"--business-column '{business_column}' not found in {path}. "
            f"Columns present: {', '.join(rows[0].keys())}"
        )
    return rows


def load_run(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_manual_variants(path):
    if not path:
        return {}
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    return {k: set(v) for k, v in raw.items()}


def count_mentions(census, run_rows, business_column, extra_stopwords, manual_variants):
    results = {}
    for entry in census:
        brand = entry[business_column]
        vs = variants(brand, extra_stopwords) | manual_variants.get(brand, set())
        patterns = [to_pattern(v) for v in vs]
        total = 0
        per_provider = Counter()
        per_question = Counter()
        matched_rows = []
        for row in run_rows:
            if row.get("errors"):
                continue
            text = row.get("answer_text", "") or ""
            if any(p.search(text) for p in patterns):
                total += 1
                per_provider[row.get("assistant", "")] += 1
                per_question[row.get("question_id", "")] += 1
                matched_rows.append({
                    "assistant": row.get("assistant", ""),
                    "question_id": row.get("question_id", ""),
                    "run_no": row.get("run_no", ""),
                })
        results[brand] = {
            "total": total,
            "openai": per_provider.get("openai", 0),
            "gemini": per_provider.get("gemini", 0),
            "perplexity": per_provider.get("perplexity", 0),
            "per_question": dict(per_question),
            "variants_used": sorted(vs),
            "matched_rows": matched_rows,
        }
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True, help="Completed trade-run CSV (tools/trade-run/ output)")
    ap.add_argument("--census", required=True, help="Market census CSV — one row per business")
    ap.add_argument("--area", required=True, help="Campaign geography (e.g. 'Chester'). Added to the stopword list automatically — a variant that strips down to just the area name is a guaranteed false-positive risk, not a real match")
    ap.add_argument("--out", required=True, help="Where to write mention-counts.json")
    ap.add_argument("--business-column", default="business", help="Census CSV column holding the business name (default: business). Older census files may use 'brand' instead")
    ap.add_argument("--variants-file", default=None, help="Optional JSON file of {business_name: [extra misspellings/variants]}, for a model's own recurring misspelling of a brand — spot-checked and added per run, not guessed in advance")
    args = ap.parse_args()

    census = load_census(args.census, args.business_column)
    if not census:
        sys.exit(f"No rows in {args.census}")
    run_rows = load_run(args.run)
    if not run_rows:
        sys.exit(f"No rows in {args.run}")

    extra_stopwords = {args.area.strip().lower()}
    manual_variants = load_manual_variants(args.variants_file)

    print(f"Loaded {len(run_rows)} run rows, {len(census)} census businesses", file=sys.stderr)

    results = count_mentions(census, run_rows, args.business_column, extra_stopwords, manual_variants)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\n{'business':38s} {'total':>5s} {'oai':>4s} {'gem':>4s} {'ppx':>4s}  questions")
    for brand, r in sorted(results.items(), key=lambda x: -x[1]["total"]):
        qs = ",".join(sorted(r["per_question"].keys()))
        print(f"{brand:38s} {r['total']:5d} {r['openai']:4d} {r['gemini']:4d} {r['perplexity']:4d}  {qs}")
    print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()
