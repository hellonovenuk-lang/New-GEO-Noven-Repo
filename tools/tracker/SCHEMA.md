# Tracker schema

*What `tracker.json` contains, field by field. Read this before changing
`import_tracker.py`'s output shape.*

## Where the data lives

**`~/wardith-runs/tracker/tracker.json`, never in this repository.**
`CLAUDE.md` and `playbook/records-and-data.md` are absolute on this: no
client or prospect name goes in the repo. Every business, contact and
sales-activity fact this tracker holds lives next to the campaign folders
it was built from — `~/wardith-runs/tracker/`, the same disk the owner's
full-disk encryption and backup already cover per
`playbook/records-and-data.md`.

`tracker.csv` is a flat, one-row-per-prospect rendering of the same file,
written alongside it, for opening in a spreadsheet. `tracker.json` is
canonical; the CSV is a view and is regenerated from it on every import.

## Two kinds of field, never blurred

Every prospect record has a `research` object and an `activity` object.

- **`research`** — mechanically derived from `/qualify` and `/outreach`
  output. Overwritten on every import so it always reflects the latest
  qualified campaign JSON and outreach-prep files. Never hand-edit this
  half; edit the source campaign and re-run the import instead.
- **`activity`** — sales activity the owner enters by hand: sent, replied,
  followed up, converted, rejected, opted out, and the revenue fields.
  **The importer only ever fills a missing (`null`) activity field — it
  never overwrites one that already holds a value.** This is what lets a
  re-import after a new `/qualify` or `/outreach` run pull in fresher
  research without erasing where a prospect actually is in the pipeline.

## Top level

```
{
  "schema_version": 1,
  "campaigns": { "<campaign_id>": { ... } },
  "prospects": { "<prospect_id>": { ... } },
  "import_log": [ { "timestamp": "...", "message": "..." }, ... ]
}
```

Both `campaigns` and `prospects` are objects keyed by stable ID, not
arrays — an import is an upsert by key, never an append. `import_log` is a
flat, append-only (capped at 500 entries, oldest dropped first) list of
every warning/conflict a run produced — a stale/superseded campaign JSON
skipped in favour of newer canonical data, an orphaned outreach-prep entry,
a file caught mid-write. Rendered as `wardith-crm.xlsx`'s `Import Log` sheet.

## Stable IDs

- **`campaign_id`** is the campaign slug itself (e.g.
  `estate-agents-chester`) — already the stable identifier `/90qrun`,
  `/qualify` and `/outreach` all key their own output off.
- **`prospect_id`** is `"<campaign_slug>::<slugified business name>"`
  (lowercase, non-alphanumeric runs collapsed to a single `-`, trimmed).
  This depends on a business's name staying stable across a re-qualified
  campaign, which is already how `/qualify` Stage 1.4 treats a re-run —
  see "Limitations" in `README.md` for what happens if a name changes.

## `campaigns[<campaign_id>]`

| Field | Meaning |
|---|---|
| `campaign_id` | Same as the key; the slug. |
| `sector` | From the campaign JSON's `run.sector`, or parsed from the `/90qrun` run-log's `**Trade:**` line if no campaign JSON exists yet. |
| `geography` | Same pattern, `run.geography` / run-log `**Geography:**`. |
| `run_date` | `run.date`, or the run-log's `**Date:**`. |
| `pipeline_stage` | `RESEARCHED` (raw run CSV only) → `QUALIFIED` (`<slug>-campaign.json` exists) → `OUTREACH_PREPARED` (an `outreach-prep-<slug>-*.json` exists). Derived from which files exist, not tracked by hand. |
| `market_count` / `outreach_count` / `excluded_count` | Straight counts from the campaign JSON's `market[]` / `outreach[]` / `excluded[]`, once one exists. |
| `source_run_csv` | `~/wardith-runs/<slug>.csv`, if found. |
| `source_campaign_json` | `~/wardith-runs/<slug>/<slug>-campaign.json`, if found. |
| `source_run_log` | The `/90qrun` run-log markdown, if that's where sector/geography came from. |
| `first_imported_at` / `last_imported_at` | UTC timestamps, importer-managed. |

## `prospects[<prospect_id>].research`

Populated from a campaign JSON's `outreach[]` entry (the qualified,
verified, contactable set — never `market[]` or `excluded[]`, which are
not prospects in the sales-pipeline sense this tracker exists for), merged
with the matching `/outreach` prep record where one exists:

`business`, `area`, `website`, `campaign_id`, `priority`, `opportunity_type`,
`outreach_rank` (only present on a scored campaign — see
`tools/prospect-compiler/CAMPAIGN-HANDOFF.md` §3a), `accessibility`,
`accessibility_notes`, `contact_person`, `role`, `contact_email`,
`contact_phone`, `decision_maker_linkedin`, `ready_to_email`,
`competitive_gap_finding`, `why_prospect`, `legal_entity`, `company_number`,
`company_status`, `outreach_angle`, `email_subject`, `email_body`,
`linkedin_draft`, `caveats`, `evidence_source_ids`, `source_campaign_json`,
`source_outreach_prep_json`, `withheld_at_outreach` (boolean; `true` when
the matched outreach-prep entry's own `withheld` flag is `true` — Stage 4
of `/outreach` dropped it, e.g. `ready_to_email` wasn't `YES` or the contact
route died on re-check), `withheld_reason` (that entry's `withheld_reason`
text, or `null`).

A prospect found in an outreach-prep file with no matching `outreach[]`
entry in the campaign JSON (a name mismatch between the two files) is still
recorded, with `research.orphaned_outreach_prep: true` and a note — never
silently dropped, never silently guessed into a match.

## `prospects[<prospect_id>].activity`

Hand-maintained. All start `null` and are left alone by every re-import
once set:

- `outreach_status` — importer-managed, and the only value it ever sets is
  `PREPARED`: the first time a *genuinely drafted, non-withheld* outreach-prep
  record appears for this prospect (an entry with `withheld: true`, or no
  `email_body`, is never marked `PREPARED` — see `README.md`'s import bug
  history). Uniquely among activity fields, this one **can** move backward:
  if a fresher `/outreach` run now withholds a previously-drafted business,
  a still-`PREPARED` (not yet manually advanced) status resets to `null`.
  Any other value here (`SENT`/`REPLIED`/...) is a legacy hand-edit path —
  `wardith-crm.xlsx`'s `Activities` sheet is the current way to record real
  sales activity, and its `Activities` log is authoritative, not this field.
- `prepared_date` — importer-set alongside `PREPARED`, cleared alongside it.
  `sent_date`, `replied_date`, `followed_up_date`, `converted_date`,
  `rejected_date`, `opted_out_date`, `audit_revenue`, `foundation_revenue`,
  `ongoing_plan`, `ongoing_plan_revenue`, `next_action`, `next_action_due_date`
  — legacy hand-edit fields, superseded by the workbook.
- `do_not_contact` — boolean, entered by hand, permanent per
  `playbook/records-and-data.md`'s retention table. **The importer never
  clears this field once set**, regardless of what a re-import finds.
  (The workbook's own `Do Not Contact (Manual)` column and `Opted out`
  activity type are the current way to set this — see `README.md`.)

## What this tool does not do

No sending, no external CRM sync, no web dashboard, no scoring of its own
— see `README.md`. Cadence/stage computation lives in `cadence.py`, used by
both `build_crm.py` and its own tests, never hand-derived here.
