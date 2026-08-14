---
name: qualify
description: >-
  Take a completed Wardith trade run (tools/trade-run/ output — a raw
  `assistant × question × run` CSV, nothing further done to it) through the
  full qualification pipeline and produce a schema-valid campaign JSON plus
  a rendered workbook: market census, mention-count analysis, relative
  market-position analysis, legal/business verification, contact-route
  discovery, opportunity classification (GAP/GROWTH/DEFEND), and a proposed
  disposition/priority/ready_to_email per business, gated by the owner's
  approval before anything is outreach-ready. Use this whenever the owner
  asks to qualify, process, or turn a completed 90-question run into
  prospects, or names a run slug and asks what came out of it commercially.
  Does not run the paid trade-run stage, does not send outreach, and does
  not touch a completed run's raw data.
---

# /qualify

Invoked as `/qualify <run>`, where `<run>` is either the client slug used
when the run was made (e.g. `estate-agents-chester`, matching `trade_run.py
--client`) or a direct path to the raw run CSV. From the slug, the canonical
locations follow the pattern already established by the Wirral and Chester
runs:

```
raw run CSV:      ~/wardith-runs/<slug>.csv
campaign folder:  ~/wardith-runs/<slug>/
```

**Source of truth for every judgement call in this skill:**
`playbook/outreach-process.md` (why — the business process) and
`tools/prospect-compiler/CAMPAIGN-HANDOFF.md` (how — the field-by-field
schema mapping). This file is the procedure that walks through them in
order; it does not restate their content, and if this file and either of
them disagree, they win — fix this file, not the other way round.

**Before starting, confirm the run is actually complete.** Read the raw CSV:
every planned `(provider, question, run_no)` identity should be present with
no lingering smoke rows (`notes` containing "smoke"). If it isn't, stop and
say so — this skill does not run or resume `tools/trade-run/`.

## The ten stages

### 1. Market census

Build (or confirm an existing) market census CSV, per
`outreach-process.md` step 3: the real customer-facing competitive market,
from the strongest sources for the trade — never a Companies House sweep.
Companies House is a filter applied later (stage 4), not the source here.

Output: a census CSV with at minimum a `business` column, saved alongside
the raw run in the campaign folder (`market-census-<slug>.csv`, matching
the existing Wirral/Chester naming).

### 2. Mention-count analysis

Mechanical — run the tool, don't hand-count:

```
python3 tools/mention-count/mention_count.py \
    --run ~/wardith-runs/<slug>.csv \
    --census ~/wardith-runs/<slug>/market-census-<slug>.csv \
    --area <geography> \
    --out ~/wardith-runs/<slug>/mention-counts.json
```

If a model's own answers show a recurring misspelling of a real business
name (spot-check a sample before assuming this), write a small
`--variants-file` for it — see `tools/mention-count/README.md`. Don't guess
variants in advance.

### 3. Relative market-position analysis

Judgement, not arithmetic. Using the mention counts against *this market's
own distribution* (not a fixed count — see `CAMPAIGN-HANDOFF.md`'s "Market
position and opportunity type" subsection), place each credible business:
Leader / Upper-mid / Mid / Low / Absent. Consider total appearances, share
relative to the leaders, provider split, question/intent spread where
useful, and cross-model consistency. No proprietary score, visibility
percentage, or hard band like "0–5 = GAP" — that is exactly the invented
precision the methodology forbids.

**Do not force every census business through this.** Most of a census won't
have enough individual research behind it yet to classify responsibly —
that's what stages 4–6 are for, and even then, some will stay unclassified.

### 4. External business verification

For any business that survives stage 3 as a credible candidate: verify it
genuinely operates in the sector and geography, and — before it can reach
`outreach[]` — a defensible active Ltd/LLP match at Companies House.
`outreach-process.md` step 3's rule is absolute: no verified active company
or LLP, no entry in `outreach[]`, full stop. Search by name, never by
postcode or SIC-code sweep.

### 5. Contact-route / decision-maker discovery

For businesses heading toward `outreach[]`: find the best verified contact
route, preferring in order — named owner/director/manager with a business
email, named decision-maker with a contact form or business inbox, a
verified generic business inbox, an official website contact form, then a
trusted portal enquiry route only if nothing better exists. Never invent a
name, role, or email, and never infer an email pattern that hasn't been
independently confirmed on the business's own site or a trusted source.

### 6. Current-status / rebrand checks

Light-touch, not a repeat of stage 4: confirm the business's site/contact
route is still live, its local presence is still current, and there's no
obvious closure, acquisition, or rebrand since the census was built. If a
status check produces a result that contradicts an earlier one in the same
session (this has happened before — a false "dissolved" reading on a live
company), don't take either on faith; cross-check against a second signal
(e.g. Companies House officers/PSC pages, not just the overview page) before
deciding.

### 7. Assign commercial opportunity

One of exactly four values — **`GAP`**, **`GROWTH`**, **`DEFEND`**, or
**`NO OPPORTUNITY`** — per the definitions in `outreach-process.md` step 4
and `CAMPAIGN-HANDOFF.md`. Rules that must hold:

- **High visibility alone is never grounds for automatic exclusion.** A
  business named as often as its competitors is a `DEFEND` candidate by
  default, not a dead end — the old "already strongly visible → exclude"
  rule is gone.
- **`GAP` / `GROWTH` / `DEFEND` describe commercial opportunity, not
  outreach priority or campaign disposition.** Setting `opportunity_type`
  says nothing about whether this business is in this campaign's
  `outreach[]`, or how urgently.
- **`REVIEW` is not a value here.** It is not a fifth (or fourth)
  opportunity type. An unclassifiable business simply gets no
  `opportunity_type` set, with the ambiguity carried by `disposition`
  and/or `priority` being `REVIEW` instead — those two fields already exist
  for exactly this.
- **A business can have a valid opportunity type while still being excluded
  from this particular campaign.** `opportunity_type` and `disposition` are
  independent — see `sample-campaign.json`'s Northgate Pipeworks for the
  shape: `DEFEND`, `EXCLUDED` from this round, both true at once.

### 8. Assign disposition, reason, priority, ready_to_email

- `disposition` (`market_entry`): `OUTREACH` / `EXCLUDED` / `REVIEW`.
- `reason` (`excluded_entry`), only for `EXCLUDED`: the fixed enum in
  `schema.json` — `ALREADY STRONGLY VISIBLE` still exists for the rare case
  it's genuinely the only real reason, but per stage 7 it should no longer
  be the default outcome of high visibility.
- **`priority`** (`A`/`B`/`C`/`REVIEW`) — commercial value, not a
  visibility-size ranking. Weighs evidence quality, market relevance,
  credibility, competitive position, commercial value, and decision-maker
  accessibility. A `DEFEND` business can be Priority A; a zero-visibility
  `GAP` business can be Priority C.
- **`ready_to_email`** (`YES`/`REVIEW`) — whether *this* email is
  send-ready today: verified contact, correct numbers, a truthful,
  non-misleading angle for this specific opportunity type (the framing
  principles in `outreach-process.md` step 4 — not fixed copy).

Propose values for all four. Do not treat them as final yet — see the gate
below.

### 9. Write the campaign JSON

Populate `schema.json` exactly, field by field, using
`CAMPAIGN-HANDOFF.md` §3 as the checklist and §4 for evidence rules (every
`outreach[]` claim traceable to a real `source_id`; no invented Companies
House facts, contact names, or emails; placeholders only where the schema
makes a field optional). Save to
`~/wardith-runs/<slug>/<slug>-campaign.json` — never inside this
repository.

### 10. Validate and render

```
python3 tools/prospect-compiler/build_workbook.py \
    --input ~/wardith-runs/<slug>/<slug>-campaign.json \
    --output ~/wardith-runs/<slug>/<slug>-prospects.xlsx
```

If validation fails: fix the data or this skill's output, per
`CAMPAIGN-HANDOFF.md` §8's anti-detour rule. Never create a parallel
renderer or weaken the compiler's validation to make bad data pass.

## The approval gate — stop here

A campaign JSON that passes validation is not the same as one that's
outreach-ready. `build_workbook.py` only checks that `priority` and
`ready_to_email` hold a valid enum value — it cannot check whether the
owner has actually reviewed them. **Present the proposed `priority` and
`ready_to_email` for every `outreach[]` business for explicit owner
approval before treating any of it as final.** This is the same gate
`CAMPAIGN-HANDOFF.md` §5 already defines; this skill does not add a new
one or skip it because the compiler ran successfully.

## What this skill does not do

- **Does not run or resume `tools/trade-run/`.** The 90-question stage is
  separate, paid, and manually invoked — this skill only ever reads a
  completed run's output.
- **Does not send outreach**, draft emails, or touch anything past the
  rendered workbook.
- **Does not modify `schema.json`, `build_workbook.py`, or the playbook.**
  If the schema genuinely can't represent something this skill needs to
  record, that's a real blocker — stop and say so rather than working
  around it with an invented field or a notes-field workaround.
- **Does not touch a completed run's raw CSV, census, mention counts, or
  campaign JSON once written**, except to correct a verified factual error
  the owner has approved — the same rule already governing every
  qualification session this pipeline has run.
