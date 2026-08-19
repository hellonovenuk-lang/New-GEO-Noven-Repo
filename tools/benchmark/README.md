# Benchmark

The measurement half of **Wardith for Agencies** — `playbook/agency-product.md`
is the product, this is the arithmetic under it. Two scripts, both
deterministic, both stdlib-only, neither of which makes a judgement.

| File | What it is |
|---|---|
| `benchmark_metrics.py` | One named client against the businesses the answers named beside it. Writes `baseline.json`, the record a Monthly Review is diffed against |
| `citation_analysis.py` | What the assistants built those answers out of, and which domains name a competitor and never the client |
| `tests/make_fixture.py` | Rebuilds the test fixture. Every name and domain in it is invented |
| `test_benchmark.py` | `python3 test_benchmark.py -v` |

**Nothing here researches, decides or writes prose.** Same split
`tools/prospect-compiler/` already keeps: `scoring_engine.py` computes,
`build_workbook.py` renders, and the judgement happens in the skill.

## The pipeline these two sit in

```
trade_run.py                    → raw run CSV        (unchanged)
validate_run.py                 → completeness gate  (unchanged)
mention_count.py                → mention-counts.json (unchanged)
benchmark_metrics.py            → baseline.json      (here)
citation_analysis.py            → citation-analysis.json (here)
site_check.py                   → site-check.json    (unchanged)
```

**No output goes in this repository.** A benchmark names a real client and
its real competitors, so everything lands under
`~/wardith-runs/agency/<agency-slug>/<client-slug>/`. `CLAUDE.md`'s rule about
client and prospect names is absolute and applies to the question file too —
which is why an agency-product question set is never committed, unlike a
generic `/90qrun` trade set.

## Usage

```
python3 benchmark_metrics.py \
    --run ~/wardith-runs/agency/<agency>/<client>/run.csv \
    --questions ~/wardith-runs/agency/<agency>/<client>/questions.csv \
    --mention-counts ~/wardith-runs/agency/<agency>/<client>/mention-counts.json \
    --client "Example Ltd" \
    --out ~/wardith-runs/agency/<agency>/<client>/baseline.json

python3 citation_analysis.py \
    --run ~/wardith-runs/agency/<agency>/<client>/run.csv \
    --mention-counts ~/wardith-runs/agency/<agency>/<client>/mention-counts.json \
    --client "Example Ltd" --client-domain example.co.uk \
    --out ~/wardith-runs/agency/<agency>/<client>/citation-analysis.json
```

`--client` must match the census name exactly. **The peer census has to
include the client itself** or there is nothing to compare against; both
scripts stop rather than silently reporting a client with no row.

`--high-intent` overrides which questions count as high intent. The default
is every `qualified-discovery` and `buying-intent` question.

## Three rules the numbers follow

**Bands, never a composite score.** `playbook/decisions.md`: no score out of
ten, no visibility index, no percentage as a headline. A band only means
something against the run count it was defined for, so `band_for()` returns
a band at five runs and `None` at any other. Aggregates carry raw counts, a
rate, and how many of the underlying cells sat in each band — never a
stretched label.

**Prompted questions never enter the headline.** A question whose own wording
names the client was answered by an assistant that was handed the name.
Counting it as visibility measures the question set, not the business. In the
test fixture it is the difference between 13.3% and 40%.

`playbook/audit-process.md`'s wording rule 3 says no business name outside the
named-business pair, but its own `q08` template ("Who are the main
alternatives to `{business}`…") is a comparison question that does name the
business, and it needs the name to mean anything. **Both readings are
defensible, so this splits rather than forbids:** every question is flagged
`prompted` or not, the headline and the peer table use the unprompted set,
and the prompted figure is reported beside them. The flag is recorded per
question so it can be checked rather than assumed.

**Thresholds are imported, not copied.** `benchmark_metrics.py` imports
`band_visibility` and the three position thresholds from
`tools/prospect-compiler/scoring_engine.py`. A second copy of those numbers
would quietly disagree the first time the methodology in
`CAMPAIGN-HANDOFF.md` §3a is revised.

## Why this does not emit GAP / GROWTH / DEFEND

Those are prospecting labels. They describe the commercial case for
approaching a stranger, and two of the three thresholds behind them turn on
`business_credibility` — a research judgement about whether a business is
genuinely trading. An agency's existing client is not a stranger and needs no
such judgement. `benchmark_metrics.py` reuses the visibility thresholds and
reports `visibility_shape` instead:

| Shape | Meaning |
|---|---|
| `LEADING` | Meaningful visibility in absolute terms, close to the best-represented peer, across most of its own questions |
| `COMPETITIVE` | Meaningful visibility, not at the front |
| `BEHIND` | Named, but materially less often than the peers named beside it |
| `ABSENT` | Never named on an unprompted question |
| `NO_PEER` | Nobody else was named at all — there is nothing to compare against, and this is not leadership |

## `baseline.json`

Versioned by its own `schema` field (`wardith-benchmark-baseline/1`) so a
future Monthly Review diff can refuse to compare across a shape change.

| Key | What it holds |
|---|---|
| `run` | Providers, model version strings per provider, expected vs successful responses, and `providers_with_mixed_model_versions` |
| `questions` | Each question's id, category, text, `high_intent` and `prompted` flags |
| `client_visibility.overall` | The headline. Unprompted questions only |
| `client_visibility.prompted` | The prompted questions, reported separately |
| `client_visibility.by_provider` / `by_category` / `high_intent` | The splits |
| `client_visibility.per_question` | Per question per assistant, with the band |
| `peers` | Every business the answers named, ranked, on the unprompted denominator |
| `position` | Rank, top competitor, relative position, `visibility_shape` |
| `thresholds_used` | Which thresholds were applied and where they came from |

**`providers_with_mixed_model_versions` is the field a Monthly Review has to
read before claiming anything moved.** `playbook/models-and-schemas.md`: a
month-on-month comparison across a provider model change is not a comparison.
The diff must fail closed on that provider rather than report progress.

## What is not here yet

**The Monthly Review diff.** `baseline.json` is designed as its input and the
`schema` field is its compatibility gate, but the diff itself is not written —
it needs the stochasticity rule in `playbook/agency-product.md` §2.1 settled
first, and that is an owner decision, not a coding one. Building it against a
guessed noise floor would produce a tool that reports noise with confidence,
which is the specific failure the whole product has to avoid.
