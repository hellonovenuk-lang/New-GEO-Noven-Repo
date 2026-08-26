# Wardith CRM

The daily-operating-system app: every prospect that has come out of a
`/qualify` run, whether `/outreach` has prepared it yet, what actually
happened next - sent, replied, followed up, a meeting booked, an audit
sold - the revenue once a sale happens, and, once a prospect becomes a
client, their own structured record and service history.

This replaces `tools/tracker/`'s Excel workbook (`wardith-crm.xlsx`) with
a local web app backed by a real database, for the reasons `tools/tracker/README.md`
already documents as that workbook's own known ceiling: Excel-only,
single-machine, and no client-servicing view at all.

## Where the data lives

**`~/wardith-runs/crm/wardith.db` - never in this repository.** Same rule
as `tools/tracker/`: `AGENTS.md`'s "no client or prospect names in this
repository" is absolute, and this database's whole purpose is to hold
prospect and client names, contacts and sales history. This directory
holds only the app's code - no business data.

## Running it

```
pip install -r tools/crm/requirements.txt   # once - installs Flask

python3 tools/crm/main.py serve             # start the local web app
```

Open `http://127.0.0.1:8420/`. The app binds to `127.0.0.1` only - it is
never reachable from the network. Stop it with Ctrl+C.

The "Refresh from campaigns" button on every page (or
`python3 tools/crm/main.py ingest`) scans `~/wardith-runs/` for the latest
`/qualify` and `/outreach` output and upserts it into the database - safe
to run at any time, including mid-run on another campaign. Research
fields are overwritten on every refresh; hand-entered activity, notes and
`do_not_contact` are never touched by it.

**`/qualify` and `/outreach` now call this automatically** at the end of
their own run (`/qualify`'s Stage 11.5, `/outreach`'s Stage 7.6), scoped to
just the campaign that finished - so a fresh prospect or outreach record is
already here without a manual refresh. The button and the bare `ingest`
command still exist for an on-demand full re-sync (e.g. after hand-editing
a campaign JSON, or pulling in campaigns from another machine).

**Using this alongside phone-triggered cloud runs?** `wardith.db` only
exists on whichever machine last had it - a cloud session's VM is wiped
when it's reclaimed. `scripts/wardith-runs-sync.sh` (repo root) syncs the
whole `~/wardith-runs/` tree, this db included, against the private
`hellonovenuk-lang/wardith-runs-data` repo, and `/90qrun`/`/qualify`/`/outreach`
already call it automatically in a cloud session. On the laptop, run
`bash scripts/wardith-runs-sync.sh pull` before opening `serve` (or running
`ingest`) to pick up anything a phone-triggered run added, and
`bash scripts/wardith-runs-sync.sh push "laptop CRM update"` after you make
changes here - `pull` refuses to overwrite a local `wardith.db` that's
changed since the last sync, so a forgotten `push` is a stop, not a silent
loss of hand-entered notes.

## What's in it

- **Today** - overdue/due-today/upcoming/outreach-ready/replies-needing-action,
  computed live from `cadence.py`'s rules against real database rows.
- **Prospects** - one page per prospect, full research plus an inline
  activity log.
- **Activities** - the sales-activity log (append-only; this is what
  actually happened, never overwritten by a refresh).
- **Campaigns / Pipeline** - per-campaign rollups and a stage funnel.
- **Revenue** - a display-only sum of amounts typed in against a
  sold/started activity. Not invoicing, not payment processing - see
  "What this doesn't do" below.
- **Settings** - the editable cadence table (`cadence_settings`). Editing
  a row changes every prospect's next-action recommendation on the next
  page load, no code change or restart needed.
- **Clients** - once a prospect converts, a structured record (contact,
  plan tier, key dates, retention/deletion-due date) plus its own
  append-only service-activity log, deliberately separate from the sales
  Activities log. "Convert to client" on a prospect's page pre-fills it
  from that prospect's research data.
- **Import Log** - warnings from every refresh (a stale campaign JSON
  skipped, an orphaned outreach-prep entry, a file caught mid-write).

Prospect identity (`prospect_id`) prefers a verified Companies House
`company_number` over a slugified business name when one is known, so a
business rename doesn't silently create a duplicate row - see
`business_key_for()` in `ingest.py`.

**`models.find_prospect()` is a second, read-only consumer of that same
`business_key`:** `/qualify` Stages 5-6 call it before researching a
business's legal entity or contact route from scratch, to reuse a prior
campaign's already-researched record for the same business (still subject
to `/qualify`'s own current-status re-check and staleness threshold - see
`.claude/skills/qualify/SKILL.md`). It never writes anything; only `ingest`
writes to `prospects`.

## What this doesn't do

No payment processing, invoicing, or Zoho Books/Revolut integration - the
Revenue view is a record of an amount typed in, nothing more. No
multi-user auth (single user, localhost only). No ticketing/helpdesk for
clients - a structured record and an activity log, not a support system.
No automated reminders beyond the Today page being correct when opened.
No automatic retention deletion - a client's `retention_deletion_due_date`
is stored so deleting it is something you do by looking, per
`playbook/records-and-data.md`, never something the software does
unattended.

## Files

- `schema.sql` / `db.py` - the SQLite schema and connection/init helpers.
- `cadence.py` - ported unchanged from `tools/tracker/cadence.py`; keep
  both in sync until `tools/tracker/` is retired.
- `ingest.py` - ported from `tools/tracker/import_tracker.py`; writes SQL
  rows instead of merging into a `tracker.json` dict, since that
  intermediate file existed only for `build_crm.py` to render Excel from
  in one pass.
- `models.py` - query/write helper functions, one per table/view. No ORM.
- `app.py` - the Flask app and every route.
- `main.py` - CLI entry point (`serve` / `ingest`).
- `test_cadence.py`, `test_db.py`, `test_ingest.py`, `test_app.py` - run
  with `python3 -m unittest tools.crm.test_cadence tools.crm.test_db tools.crm.test_ingest tools.crm.test_app -v`
  from the repo root.

## Migrating from `tools/tracker/`

If a real `~/wardith-runs/tracker/tracker.json` already exists with
prospects in it, it is not read by this tool automatically - write a
one-time script to insert its `prospects`/`campaigns` (and any legacy
hand-entered `activity.*` fields, as a synthetic activity row) directly
into `wardith.db`, then discard the script. Otherwise, the first
`ingest` run builds the database fresh from whatever campaign JSON
already exists - there is nothing to migrate. Either way, leave
`tracker.json`/`wardith-crm.xlsx` in place until you trust this system.
