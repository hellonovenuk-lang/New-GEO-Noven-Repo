# Prospect compiler

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
pip install openpyxl
```

The only non-stdlib dependency. Python 3.9+.

## Input

A JSON file matching `schema.json` — five top-level keys: `run`, `market`,
`outreach`, `excluded`, `sources`. See `sample/sample-campaign.json` for a
complete, fictitious example of the shape.

The script validates required fields and enum values before writing anything,
and fails with a specific error rather than guessing:

```
python3 build_workbook.py --input campaign.json --output workbook.xlsx
```

## Output

An `.xlsx` workbook with five sheets:

| Sheet | Content |
|---|---|
| **OUTREACH** | Outreach-ready prospects only, sorted priority A → B → C, strongest cases first within each band (the order already set in the input) |
| **MARKET** | The full competitive census, including businesses not eligible for outreach |
| **EXCLUDED** | Investigated businesses excluded from outreach, with a fixed reason code |
| **SOURCES** | The source register — stable IDs (`S001`…) that OUTREACH and MARKET reference instead of repeating URLs |
| **RUN** | Campaign provenance: sector, geography, campaign slug, date, questions, provider/model identifiers, response counts, raw-data path, methodology notes |

Every sheet has a frozen header row, an autofilter, sensible column widths,
and wrapped long-text columns. No numeric prospect score is calculated
anywhere — priority is A/B/C, set by the judgement that prepared the input.

## Testing the renderer

```
python3 build_workbook.py --input sample/sample-campaign.json --output /tmp/sample-workbook.xlsx
```
