# Mention count

Matches a market census against a completed trade-run CSV, producing
per-business AI-mention counts by provider and question. The mechanical
half of qualification — see `/qualify` (`.claude/skills/qualify/`) for the
judgement half, and `tools/prospect-compiler/CAMPAIGN-HANDOFF.md` for where
the output goes next.

**This script does not decide who is a prospect.** It counts name matches.
Everything downstream of the counts — market position, opportunity type,
priority — is judgement, done elsewhere.

## Where this came from

Generalised from `crossref.py` (the original Wirral matching logic — name
variants for `&`/`and`, apostrophes, `Ltd`/`Estate Agents` suffixes) by way
of its Chester evolution (a stopword floor so a stripped variant can't
collapse into a common word, per-question counts, a manual-override file for
a model's own misspellings). Verified against the real completed Chester run
before this file was written: reproduces all 69 businesses' counts exactly,
zero mismatches on any provider field, against the trusted
`mention-counts.json` that run already produced by hand.

## Requirements

Python 3.9+, stdlib only. Nothing to `pip install`.

## Input

- **`--run`** — a completed `tools/trade-run/` output CSV.
- **`--census`** — a market census CSV, one row per business. Needs a column
  holding the business name; `--business-column` defaults to `business`
  (older census files may use `brand` instead — pass it explicitly).
- **`--area`** — the campaign geography, e.g. `Chester`. Added to the
  stopword list automatically: a name variant that strips down to just the
  area itself is a guaranteed false-positive risk (the area name appears in
  almost every answer), not a real match.
- **`--variants-file`** (optional) — a JSON file of
  `{"Business Name": ["Misspelling One", "Misspelling Two"]}` for a model's
  own recurring misspelling of a brand. Spot-check the raw answers for these
  after a first pass; don't guess them in advance.

## Usage

```
python3 mention_count.py --run ~/wardith-runs/{trade}-{area}.csv \
    --census market-census-{trade}-{area}.csv --area {area} \
    --out mention-counts.json
```

## Output

`mention-counts.json` — one entry per census business:

```json
{
  "Example Estate Agents": {
    "total": 5,
    "openai": 5,
    "gemini": 0,
    "perplexity": 0,
    "per_question": {"q01": 1, "q03": 1, "q06": 3},
    "variants_used": ["Example Estate Agents", "Example"],
    "matched_rows": [{"assistant": "openai", "question_id": "q01", "run_no": "5"}]
  }
}
```

`variants_used` and `matched_rows` are there so a wrong count can be
diagnosed by inspection, not by re-running the whole thing and guessing.
