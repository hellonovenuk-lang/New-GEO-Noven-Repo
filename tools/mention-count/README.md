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

## Alias generation and overlap-safe matching

Every census business is matched by a set of auto-generated aliases (the
brand as given, `&`/`and` swapped — case-insensitively, so a Title-Case
"And" still generates the "&" form a model's answer actually used — and
`Ltd`/`Limited`/`LLP`/`Estate Agents` suffixes stripped) plus any aliases
supplied via `--variants-file`.

Matching itself is overlap-aware: every alias, across every census
business, is searched for within one answer first; only afterwards are
overlapping matches resolved, longest span wins. This means a short
business name that happens to be a literal substring of a longer one (e.g.
"Builders Wirral" inside "Abbey Builders Wirral") is credited to the
longer, more specific business wherever the two overlap, while a genuinely
independent, non-overlapping mention of the short name elsewhere in the
same or another answer still counts normally. A permanent, campaign-wide
drop of the shorter name was deliberately rejected as a fix — it would
undercount every answer where the short business is genuinely named on its
own. Manual aliases from `--variants-file` go through the exact same
overlap resolution as auto-generated ones; a human vouching for an alias's
identity doesn't exempt it from the "don't double-count an overlapping
match" rule.

Matching is **not** word-boundary-anchored — a real run showed why: a
census brand can be spelled slightly differently in real answer text (e.g.
singular vs. plural, "Home Improvement" vs. "Home Improvements"), and an
unanchored substring match is what catches that. `GENERIC_STOPWORDS`
already guards against the class of false positive a word-boundary anchor
would otherwise help with (a short generic variant matching mid-word).

## Output

`mention-counts.json` — one entry per census business, plus a top-level
`_overlap_log` array recording every suppressed candidate (for audit — see
below):

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
  },
  "_overlap_log": [
    {
      "assistant": "perplexity", "question_id": "q04", "run_no": "2",
      "suppressed_business": "Builders Wirral", "suppressed_alias": "Builders Wirral",
      "winning_business": "Abbey Builders Wirral", "winning_alias": "Abbey Builders Wirral"
    }
  ]
}
```

`variants_used` and `matched_rows` are there so a wrong count can be
diagnosed by inspection, not by re-running the whole thing and guessing.
`_overlap_log` is the same idea for overlap resolution specifically — every
suppressed candidate names both the business that lost the match and the
one that won it, for the same reason.
