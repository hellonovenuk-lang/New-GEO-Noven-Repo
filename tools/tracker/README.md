# Campaign tracker and CRM workbook

The canonical, cross-campaign record: every prospect that has come out of a
`/qualify` run, whether it's had `/outreach` prepared for it yet, and what
actually happened next — sent, replied, followed up, a meeting booked, an
audit sold — plus the revenue once a sale happens. `/90qrun`, `/qualify` and
`/outreach` each produce one campaign's worth of output; this is the layer
that sits across all of them, in two stages:

1. **`import_tracker.py`** reads every campaign's source files and writes
   `tracker.json`/`tracker.csv` — the flat, canonical *research* record.
2. **`build_crm.py`** reads `tracker.json` and renders **`wardith-crm.xlsx`**
   — the daily-operating-system workbook: `Today`, `Prospects`, `Activities`,
   `Campaigns`, `Pipeline`, `Revenue`, `Settings`, `Import Log`. This is the
   file to actually work from day to day; `tracker.json`/`tracker.csv` are
   the machine-readable layer underneath it.

Full field-by-field shape: `SCHEMA.md`. Cadence/stage rules: `cadence.py`.

## Where the data lives

**`~/wardith-runs/tracker/` — never in this repository**: `tracker.json`,
`tracker.csv`, and `wardith-crm.xlsx`. `CLAUDE.md`'s "no client or prospect
names in this repository" rule is absolute, and this tracker's whole purpose
is to hold prospect names, contacts and outreach content. `tools/tracker/`
in this repo holds only the import/build code and the schema documentation
— no business data, same split `tools/prospect-compiler/` already keeps.

## Importing a completed campaign

```
python3 tools/tracker/import_tracker.py
```

With no arguments this scans every slug under `~/wardith-runs/` (raw run
CSVs, campaign folders, and their `outreach/` subfolders), upserts
`~/wardith-runs/tracker/tracker.json` by stable ID, and regenerates
`~/wardith-runs/tracker/tracker.csv` from it. **Safe to run at any time,
including while `/qualify` or `/outreach` is mid-run on a different (or the
same) campaign** — it only reads from `~/wardith-runs/`, never writes there,
and a source file caught mid-write is reported as a warning and skipped,
not treated as a failure.

To import just one campaign:

```
python3 tools/tracker/import_tracker.py --slug estate-agents-chester
```

Both flags compose (`--slug` can repeat); `--runs-dir` and `--tracker-dir`
override the default locations for testing or an alternate machine;
`--no-csv` skips the CSV regeneration.

## Building or refreshing the CRM workbook

```
python3 tools/tracker/build_crm.py
```

Run this **after** `import_tracker.py` (it reads `tracker.json`, not the raw
campaign files). With no arguments it reads `~/wardith-runs/tracker/tracker.json`
and writes `~/wardith-runs/tracker/wardith-crm.xlsx`. `--tracker-dir` and
`--output` override the defaults; `--today` overrides the date used for
cached formula values (`Settings` sheet aside, everything is a real Excel
formula that recalculates against the actual clock once opened — the
override only matters for the values baked into the file at build time).

**Safe to re-run at any time — this is how the CRM "refreshes" from a new
`/90qrun`/`/qualify`/`/outreach` output.** It reads the *existing*
`wardith-crm.xlsx` first (if one exists) and carries its `Activities` log and
`Prospects` sheet's manual columns (`Do Not Contact (Manual)`, `Notes`)
forward untouched, before overwriting the research columns from the fresh
`tracker.json` and rebuilding every sheet. The write is temp-file-then-
replace, so a crash mid-build never leaves a half-written workbook in place
of a good one.

## Recording an email, call, or LinkedIn touch

**Directly in `wardith-crm.xlsx`, on the `Activities` sheet — never in
`tracker.json`.** Add a row: pick the `Prospect ID` from the dropdown (its
business/campaign is visible enough to find it), pick the `Activity Type`
from the dropdown, set the date, and — for a sale — the `Amount (GBP)`. Save.
`Prospects`' `Current Stage` / `Next Action` / `Next Action Due Date` for
that row recalculate immediately; nothing needs re-running. The only
activity this tool ever logs *for* you is `Outreach prepared`, and only when
`/outreach` genuinely drafted (never withheld) it — everything past that is
the owner's own record of what actually happened.

## How Next Action / Due Date are calculated

Every activity type has a row in the `Settings` sheet's cadence table:
what it recommends next, how many days until it's due, what pipeline stage
it represents, and whether it stops cold-follow-up recommendations or
permanently blocks outreach. `Prospects`' formulas look up a prospect's most
recent `Activities` row against this table — **editing a cadence value in
Settings changes every prospect's Next Action / Due Date immediately, no
formula or code change needed.** A due date that lands on a Saturday or
Sunday moves to the following Monday. A reply, a meeting, a sale, or a loss
each carry their own next action (e.g. "Respond to reply", "Deliver the
audit") rather than looping back into "send a follow-up email" — see
`cadence.py` for the full rule set and `tools/tracker/test_cadence.py` for
what's verified. `Do Not Contact (Manual)`, or an `Opted out` activity
(`Blocks Outreach = TRUE` in Settings), permanently blocks a prospect from
every automated recommendation — visibly, as its own `Do Not Contact`
pipeline stage — and nothing in this tool ever clears it.

## What a re-run does and does not touch

**`import_tracker.py`** (`tracker.json`):

- **Research fields** (business, contact route, priority, accessibility,
  the drafted email, everything `/qualify` and `/outreach` produced) are
  overwritten every time from the latest source files. If a campaign gets
  re-qualified or re-run through `/outreach`, importing again picks up the
  correction — unless the incoming source is *older* than what's already
  stored (`run.date`), in which case it's skipped and logged to `import_log`
  as a conflict rather than silently overwriting newer canonical data.
- `tracker.json`'s own `activity.outreach_status` field only ever reaches
  `PREPARED` (importer-managed, self-correcting if a fresher `/outreach` run
  withholds a previously-drafted business) — everything past that
  (`SENT`/`REPLIED`/...) is a legacy hand-edit path superseded by the
  `Activities` sheet below; new work should use the workbook, not this field.
- A business's disappearance from a re-qualified campaign's `outreach[]`
  does not delete its tracker record — nothing is ever deleted by this
  script.

**`build_crm.py`** (`wardith-crm.xlsx`):

- **Research columns on `Prospects`** (business, contact route, priority,
  `Research Pipeline Stage`, `Ready To Email`, ...) refresh from
  `tracker.json` on every rebuild.
- **The `Activities` log and `Prospects`' `Do Not Contact (Manual)` /
  `Notes` columns are manual truth and are never regenerated** — a rebuild
  reads them out of the existing workbook first and carries them forward
  unchanged, only adding rows for genuinely new `Outreach prepared` facts.
  `Current Stage` / `Next Action` / `Next Action Due Date` are always
  recomputed (from `Activities` + `Settings`, live formulas), never
  hand-edited.

## Limitations, on purpose

- **No sending, no external CRM sync, no web dashboard.** Recording an
  email/LinkedIn/call/sale is a manual row on `wardith-crm.xlsx`'s
  `Activities` sheet — see above.
- **`Today`'s block sizes are a fixed 25-row spill allowance, not the exact
  count.** A block header shows how many matched *at the last rebuild*, for
  orientation only — the actual list below it recalculates live and can
  differ (that's the point). If any single block (Overdue, Due today, ...)
  ever needs more than 25 live rows, widen `TODAY_BLOCK_SPILL_CAPACITY` in
  `build_crm.py` and rebuild — sizing it to the historical count risked a
  larger live result colliding with the next block's own content.
- **`Activities`/`Settings` cadence-rule lookups use fixed absolute ranges
  (500 / 60 rows), not unlimited Table growth**, for a real reason: a
  structured self-reference (`[@[Column]]`) combined with a reference to
  another sheet in the same formula corrupts the file for Excel's own
  automation loader — reproduced while building this tool. Raise
  `ACTIVITIES_CAPACITY` / `CADENCE_CAPACITY` in `build_crm.py` well before
  either fills up.
- **Prospect identity is the business name.** `prospect_id` is
  `<campaign_slug>::<slugified business name>`. If a business's name in the
  campaign JSON changes between one `/qualify` run and the next (a typo
  fixed, a trading-name correction), the tracker sees a new prospect rather
  than an update to the old one — the old record is left in place, not
  merged. This matches `/qualify`'s own Stage 1.4 assumption that a
  business's name is stable across a re-run; it has not yet been tested
  against a real rename.
- **`market[]` and `excluded[]` entries are not imported.** Only
  `outreach[]` — the qualified, verified, contactable set — becomes a
  tracker prospect. A business researched but not qualified isn't in the
  tracker yet.
- **No JSON Schema validation of `tracker.json` itself.** `SCHEMA.md`
  documents the shape by hand, the way `tools/prospect-compiler/` did before
  `schema.json` existed. Worth revisiting if the tracker outgrows a single
  import script.
- **CSV export is a flattened view, not round-trippable.** Editing
  `tracker.csv` and expecting it to merge back into `tracker.json` isn't
  supported — edit `tracker.json` directly for now.
- **A campaign JSON that predates `schema.json` imports as a campaign row
  with no prospects, not an error.** `estate-agents-wirral` is the one
  historical case — `CAMPAIGN-HANDOFF.md` records that it "built its own
  JSON format instead of targeting `schema.json`" (custom
  `campaign_metadata`/`market_census`/`prospect_summary` keys, no `run` or
  `outreach` array). The importer looks for the standard shape only; it
  does not guess at a different one. Re-running `/qualify` on that slug
  through the current schema would let it import normally.
- **A `/90qrun` run-log's `**Trade:**`/`**Geography:**` header lines are a
  recent addition.** Older run-logs (e.g. `accountants-wirral`,
  `wirral-dentists`) don't have them, so a `RESEARCHED`-stage campaign from
  before that convention started imports with `sector`/`geography` left
  `null` rather than a guess. Once such a campaign reaches `/qualify`, its
  campaign JSON supplies both fields directly and this resolves itself.

## Tests

```
python3 -m unittest tools.tracker.test_import_tracker tools.tracker.test_cadence tools.tracker.test_build_crm -v
```

Every test builds a throwaway `wardith-runs`-shaped directory, tracker dict,
or workbook per test — never touches the real `~/wardith-runs/`.
