# Prospect compiler

`qualification_coverage.py` provides a separate, non-mutating census-wide
coverage check. It keeps zero-visibility and census-only businesses visible,
separates current incumbents from genuine exclusions, and reports the exact
research blockers for every review candidate. It never sends outreach and does
not turn a historical `ready_to_email` value into fresh approval.

```
python3 qualification_coverage.py --input campaign.json --census census.csv --output coverage.json --require-complete
```

The output path must be new. `--require-complete` saves the diagnostic report
then returns exit 1 if any census/cohort assessment is missing or unfinished,
or the new-run zero-floor policy was not used. Historical review can omit the
flag; an incomplete diagnostic report is not a qualified campaign.

Turns a validated, structured market-run dataset — prepared during a Wardith
sector × local-market campaign — into a consistent Excel workbook.

**This script does not research businesses or decide who is a prospect.**
Claude or human judgement prepares the structured input, following
`playbook/outreach-process.md`. This script deterministically renders it into
a workbook: sorting, sheet layout and formatting only.

**No real prospect names or campaign data belong in this repository.** The
only data here is `sample/sample-campaign.json`, a fictitious dataset used to
test the renderer.

## Requirements

```
pip install xlsxwriter openpyxl
```

`xlsxwriter` builds the workbook (chosen specifically because it can write a
genuine cached value alongside every formula — see "Portable downstream
handoff" in `CAMPAIGN-HANDOFF.md` §3a). `openpyxl` is used only by the test
suite, to reopen a built workbook in data-only mode and confirm formula
cells came out populated. Python 3.9+.

## Input

A JSON file matching `schema.json` — five top-level keys: `run`, `market`,
`outreach`, `excluded`, `sources`. See `sample/sample-campaign.json` for a
complete, fictitious example of the shape.

**If any business sets `service_scope`**, run the scoring engine first — it
mechanically fills in every derived scoring field (`final_score`,
`overall_rank`, `opportunity_type`, the readiness gates, and more — see
`CAMPAIGN-HANDOFF.md` §3a) from the evidence-backed value fields Claude
already set:

```
python3 scoring_engine.py --input campaign.json --in-place
```

Then render. Both scripts validate required fields and enum values before
doing anything, and fail with a specific error rather than guessing:

```
python3 build_workbook.py --input campaign.json --output workbook.xlsx
```

A campaign where nothing sets `service_scope` can skip straight to
`build_workbook.py`, exactly as pre-v2 — this is how a historical/legacy
campaign JSON stays readable. The rendered workbook labels a campaign like
this `LEGACY / UNSCORED` (Methodology sheet) and reports its QC checks as
`NOT APPLICABLE` rather than a vacuous `PASS` over an empty scored pool.

**As of 2026-08-17, `/qualify` requires canonical scoring for every newly
generated campaign** (`.claude/skills/qualify/SKILL.md`) — that mandate is
enforced at render time with `--require-scored`:

```
python3 build_workbook.py --input campaign.json --output workbook.xlsx --require-scored
```

This fails closed (no workbook written) unless the campaign has
`run.service_scopes`, complete `run.question_relevance`, an explicit
`run.scoring_cohort` covering every business that meets
`run.cohort_inclusion_min_appearances`, and every `outreach[]` entry scored
— see `CAMPAIGN-HANDOFF.md` §3a. Only pass this flag for a campaign this
skill is generating fresh; never for a historical file being merely
re-rendered, since that would (correctly) reject it.

## Output

An `.xlsx` workbook with five sheets:

| Sheet | Content |
|---|---|
| **Methodology** | Every scale, weight, threshold, formula and tie-break rule this campaign's scoring used, documented before any score is shown, including the campaign's own service-scope and question-relevance classifications |
| **Scoring** | Every business that opted into scoring (`service_scope` set), all 14 scored fields, full live-formula chain with cached values |
| **Shortlist** | The subset with `ready_to_email=YES`, ranked by both `Overall rank` and `Outreach rank` — plain values, no formulas, the primary downstream handoff |
| **Evidence** | The source register — stable IDs (`S001`…) with an optional `fact_category` so evidence for different kinds of claims about the same business (legal identity, service scope, decision-maker identity, contact route, ...) can be told apart at a glance |
| **QC** | The validation checklist run against this specific workbook — reconciliation, formula reproduction, ranking rules, readiness gates — pass/fail with the detail behind each result |

Every sheet has a frozen header row, sensible column widths, and wrapped
long-text columns. `priority` (A/B/C/REVIEW) and `opportunity_type`
(GAP/GROWTH/DEFEND/REVIEW, or legacy NO OPPORTUNITY) are *proposed* by
`scoring_engine.py` from the documented formula — the owner still approves
both before either is treated as final, per `CAMPAIGN-HANDOFF.md` §5.

Every scored `outreach[]`/`market[]` row also carries `accessibility_grade`
(a 6-tier scale from `CONFIRMED_DIRECT` down to `NO_USABLE_ROUTE`, derived
automatically from `direct_dm_route`) — the likely route to the actual
decision-maker. It materially affects `final_score` and `priority` through
the weighted-sum formula and the `ready_to_email` gate, not just a note — a
generic inbox is never treated as equivalent to a confirmed direct route.
See `CAMPAIGN-HANDOFF.md` §3a.

The legacy `accessibility` field (DIRECT/IDENTIFIABLE/GATEKEPT/CORPORATE/
REVIEW) is unchanged and still required on every `outreach[]` entry — kept
for backward compatibility, since `/outreach` and every already-completed
campaign depend on it.

## Testing the renderer

```
python3 scoring_engine.py --input sample/sample-campaign.json --output /tmp/sample-scored.json  # only if the sample sets service_scope
python3 build_workbook.py --input sample/sample-campaign.json --output /tmp/sample-workbook.xlsx
```

Regression tests (`validate()`'s required/enum checks, `scoring_engine.py`'s
formula outputs, and the rendered workbook's shape and data-only
readability) live in `test_build_workbook.py` and `test_scoring_engine.py`:

```
python3 test_build_workbook.py -v
python3 test_scoring_engine.py -v
```
