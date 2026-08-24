---
name: qualify
description: >-
  Take a completed Wardith trade run (tools/trade-run/ output — a raw
  `assistant × question × run` CSV, nothing further done to it) through the
  full qualification pipeline and produce a schema-valid campaign JSON plus
  a rendered workbook: market census, mention-count analysis, relative
  market-position analysis, legal/business verification, contact-route
  discovery, decision-maker accessibility (who to reach, and how),
  opportunity classification (GAP/GROWTH/DEFEND), and a proposed
  disposition/priority/ready_to_email per business, gated by the owner's
  approval before anything is outreach-ready. This is the canonical stage
  that runs immediately after a completed `/90qrun`. Use this whenever the
  owner asks to qualify, process, or turn a completed 90-question run into
  prospects, or names a run slug and asks what came out of it commercially.
  Does not run the paid trade-run stage, does not send outreach, and does
  not touch a completed run's raw data.
---

# /qualify

Invoked as `/qualify <run>`, where `<run>` is either the client slug used
when the run was made (e.g. `estate-agents-chester`, matching `trade_run.py
--client`) or a direct path to the raw run CSV. From the slug, the canonical
locations follow the pattern already established by prior runs:

```
raw run CSV:      ~/wardith-runs/<slug>.csv
campaign folder:  ~/wardith-runs/<slug>/
```

**If no `<run>` is given**, look for a single unambiguous candidate: exactly
one `~/wardith-runs/*.csv` that has no matching `~/wardith-runs/<slug>/`
campaign folder yet (i.e. a completed run nobody has qualified). If there's
exactly one, use it and say so. If there's more than one, or none, list what
was found and ask which slug — this is the one genuinely ambiguous input
this skill cannot infer, the same posture `/90qrun` takes on a missing
industry or geography.

**Source of truth for every judgement call in this skill:**
`playbook/outreach-process.md` (why — the business process) and
`tools/prospect-compiler/CAMPAIGN-HANDOFF.md` (how — the field-by-field
schema mapping, including the "Decision-maker accessibility" subsection).
This file is the procedure that walks through them in order; it does not
restate their content, and if this file and either of them disagree, they
win — fix this file, not the other way round.

## Stage 0 — Scope and permissions, then run straight through

Before touching anything, state plainly what this run is about to do, so the
necessary tool approvals can be granted once, up front, rather than
interrupting for every individual file read, web check, or file write — the
same broad-permission pattern `/90qrun` and `/outreach` already use:

- **Read-only** against the completed run's raw CSV
  (`~/wardith-runs/<slug>.csv`) and anything already present in
  `~/wardith-runs/<slug>/` from an earlier attempt at this same run (Stage 1
  checks for this explicitly).
- **A number of outbound web checks** (`WebFetch`/`WebSearch`) — market
  sources, Companies House, business websites, and the contact-route and
  decision-maker research in Stage 6, including LinkedIn profile matching.
  Nothing is submitted to any site; these are page reads and searches only.
- **Writes**, confined to `~/wardith-runs/<slug>/` — the market census CSV,
  `mention-counts.json`, the campaign JSON, the rendered workbook, and the
  completion report. **Never inside this repository** — `CLAUDE.md`'s "no
  client or prospect names in this repository" rule is absolute.
- **No sends.** Nothing in this skill contacts a business, submits a form,
  connects on LinkedIn, or posts anywhere. That is `/outreach`'s job, later,
  after the owner has separately reviewed and approved this campaign.

Say this once, then run Stages 1–12 straight through with no further
approval prompts for routine reads/writes already covered above. **Only
stop mid-run for a genuine blocker**: Stage 1's validation gate fails, a
schema-required field genuinely can't be populated from real evidence, or
`build_workbook.py` rejects the finished JSON. Anything smaller (a slow
source, an ambiguous but resolvable name variant, one business needing a
second lookup) gets handled and folded into the final report, not raised as
a mid-run question.

**Safe to run alongside an independent `/90qrun`.** This skill never touches
`trade_run.py` and never writes to a raw run CSV — it only reads one already
flagged complete, and only writes inside its own `~/wardith-runs/<slug>/`
folder. A `/qualify` run and an unrelated `/90qrun` (different slug, or even
the same slug at a different stage) touch no shared files and cannot
corrupt each other. If a `/90qrun` for the *same* slug is still mid-run, the
raw CSV won't pass Stage 1's completeness check yet — that stops this skill
cleanly before any writes happen, rather than racing it.

## Stage 1 — Validate the input, before anything else

Fail clearly here rather than discovering a gap four stages in.

1. **Resolve `<run>` to the raw CSV.** A slug resolves to
   `~/wardith-runs/<slug>.csv`; a direct path is used as given. If neither
   exists, stop and say so.
2. **Reuse the existing validator instead of re-deriving the check by eye.**
   If `tools/trade-run/questions-<slug>.csv` is present in this repo
   (committed by the `/90qrun` run that produced this CSV — check the
   working tree, it may live on an unmerged branch), run it:
   ```
   python3 .agents/skills/90qrun/scripts/validate_run.py \
       --csv ~/wardith-runs/<slug>.csv --questions tools/trade-run/questions-<slug>.csv
   ```
   Exit 0 confirms every planned `(provider, question, run_no)` identity is
   present, no smoke rows leaked, and model versions are consistent per
   provider — the same check `/90qrun` itself runs before it reports `PASS`.
   **If it exits 1, stop.** This skill does not patch, resume, or work
   around a broken run — that is `/90qrun` territory.
3. **If the question file isn't in the working tree**, fall back to reading
   the raw CSV directly: every planned `(provider, question, run_no)`
   identity present, no `notes` field containing "smoke". State plainly
   that the fallback path was used, since it is a weaker check than the
   validator script.
4. **Check the target folder for existing output before writing anything.**
   If `~/wardith-runs/<slug>/<slug>-campaign.json` already exists, this is a
   re-run of a previously qualified campaign — say so explicitly, and treat
   the session as correcting or extending that existing campaign (per
   `CAMPAIGN-HANDOFF.md` and "What this skill does not do" below), never as
   a silent full regeneration. A market census or `mention-counts.json`
   already present from an earlier, interrupted attempt at *this* run
   should be read and reused once confirmed still valid, not recomputed
   from scratch — this keeps a resumed qualify run cheap the same way
   `trade_run.py`'s own resume logic does.

## Stage 2 — Market census

Build (or confirm an existing) market census CSV, per
`outreach-process.md` step 3: the real customer-facing competitive market,
from the strongest sources for the trade — never a Companies House sweep.
Companies House is a filter applied later (Stage 5), not the source here.

Output: a census CSV with at minimum a `business` column, saved alongside
the raw run in the campaign folder (`market-census-<slug>.csv`, matching
the existing naming convention).

## Stage 3 — Mention-count analysis

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

## Stage 4 — Relative market-position analysis, and mandatory canonical scoring

**As of 2026-08-17, auditable scoring is mandatory for every newly invoked
`/qualify` run — it is no longer optional per business.** This is a
forward-looking product decision, distinct from `schema.json`'s own
backward-compatible shape: the schema still marks every scoring field
optional so a *historical* campaign JSON (written before this date) stays
loadable and renderable, but a *new* campaign generated by this skill must
use the full canonical pipeline below. There is no qualitative-only
production path for a new run — see the INCOMPLETE behaviour at the end of
this stage for what happens when the canonical inputs can't be completed.

**Candidate-pool consistency first.** State this campaign's inclusion
threshold before researching anyone (e.g. "every census business with
`total_ai_appearances >= 5`"), and record it as data, not just prose:
`run.cohort_inclusion_min_appearances` (the mechanical floor) plus a fuller
description in `methodology_notes` if the real rule is more nuanced than a
single number. Apply the same research depth to every business that meets
it — never let selection bias (researching whoever's easiest first) decide
who reaches `outreach[]`.

**Every business that meets the stated floor must get an explicit
`run.scoring_cohort` entry** — `{business, status}` where `status` is one
of:

- **`SCORED`** — fully scored, `service_scope` set, every VALUE field
  populated.
- **`EXCLUDED`** — a documented `reason` rules it out of scoring (it can
  still exist elsewhere in `market[]`/`excluded[]`).
- **`INCOMPLETE`** — research isn't sufficient yet; state exactly what's
  missing in `missing_evidence`.

**No cohort member may silently disappear into an unscored, un-flagged
`market[]` record.** This is the mechanism that stops a high-appearance
business (found late, or that looked hard to research) from quietly missing
the qualification pass every lower-appearance business got —
`build_workbook.py --require-scored` mechanically cross-checks this; see
Stage 11.

**Question relevance is required, not optional, for a new run**
(`run.question_relevance[]` — §3a) — every question classified before any
business is scored, so a specialist is never penalized for absence from a
question outside its verified scope. Once the 9 evidence-backed value
fields (§3a) are set for every `SCORED` cohort member, run:

```
python3 tools/prospect-compiler/scoring_engine.py --input <campaign>.json --in-place
```

This mechanically computes `visibility_score`, `gap_strength`,
`final_score`, `overall_rank`, `outreach_rank`, every readiness gate, and a
proposed `opportunity_type` per §3a's general rule (2026-08-24: `DEFEND` is
`most_named_cohort` — an absolute visibility floor, a relative-position band,
and a rank-within-group cap, no longer a real-peer requirement; `GAP` is
unconditional at zero visibility). These remain *proposals*: the owner still
approves `priority` and `ready_to_email` exactly as the approval gate below
already requires — and, new as of 2026-08-24, `disposition_recommendation`
for a `most_named_cohort` business (defaults to `EXCLUDED`, reason `ALREADY
STRONGLY VISIBLE`) is a proposal in exactly the same sense, not an automatic
drop from this campaign.

**This same command also mandatorily generates `competitive_gap_finding` and
`why_prospect`** for every scored `outreach[]` entry — not a separate step,
and not optional. It runs automatically after the derived fields above
(scores, ranks, opportunity type, nearest competitor) are final, using
`relevant_appearances`/`relevant_opportunities` — never the raw 90-answer
total for a business scoped to fewer questions than that — plus
`opportunity_type`, `nearest_competitor`, `group_top_visibility_rate`, and
question coverage. **Do not hand-write `competitive_gap_finding` or
`why_prospect` for a scored business before this step runs** — the
generated baseline is the source of truth for the primary visibility claim,
and writing prose first only means it gets silently overwritten (or, if
you set `narrative_generated_from` yourself to dodge that, produces exactly
the defect this exists to prevent). Refining the generated text afterward
with real, specific evidence (a named competitor's actual differentiator,
a detail from the audit conversation) is allowed — but the refinement must
still pass `build_workbook.py`'s narrative-consistency checks (see Stage
11), and structured fields remain the source of truth for any numeric claim
regardless of how the prose reads.

**`outreach[]` may not contain a qualitative-only entry in a new campaign.**
Every business reaching `outreach[]` must have `service_scope` set and be
`SCORED` in `run.scoring_cohort` — the old "business not opting in falls
back to the pre-existing qualitative path" behaviour is now a *historical
reader* concern only (`CAMPAIGN-HANDOFF.md` §3's qualitative
Leader/Upper-mid/Mid/Low/Absent judgement is still exactly how a pre-2026-08-17
campaign is read), not something a new run may produce.

**If the canonical inputs genuinely can't be completed** — evidence is
missing, a business can't be researched to the required depth, the
candidate pool can't be resolved — **do not fall back to the qualitative
path to finish the run anyway.** Stop, record the gap (`INCOMPLETE` status
in `run.scoring_cohort`, or a `REVIEW` disposition with the reason stated),
and report the run as `INCOMPLETE` in Stage 12, naming exactly what's
unresolved. This is a legitimate stopping point, not a failure to route
around.

## Stage 5 — External business verification

For any business that survives Stage 4 as a credible candidate: verify it
genuinely operates in the sector and geography, and — before it can reach
`outreach[]` — a defensible active Ltd/LLP match at Companies House.
`outreach-process.md` step 3's rule is absolute: no verified active company
or LLP, no entry in `outreach[]`, full stop. Search by name, never by
postcode or SIC-code sweep.

## Stage 6 — Contact-route, decision-maker discovery, and accessibility classification

For businesses heading toward `outreach[]`: find the best verified contact
route, preferring in order — named owner/director/manager with a business
email, named decision-maker with a contact form or business inbox, a
verified generic business inbox, an official website contact form, then a
trusted portal enquiry route only if nothing better exists. Never invent a
name, role, or email, and never infer an email pattern that hasn't been
independently confirmed on the business's own site or a trusted source.

**Then classify decision-maker accessibility** — the full method,
categories, and evidence rules live in `CAMPAIGN-HANDOFF.md`'s
"Decision-maker accessibility" subsection; this is the summary for the
research pass itself:

1. Identify company directors, owners, or founders (Companies House
   officers/PSC pages, the business's own site) and, where it differs, the
   likely operational or marketing decision-maker.
2. Check whether that person appears **actively associated with the
   business now** — a stale director record alone doesn't confirm this.
3. Look for a LinkedIn profile, but record `decision_maker_linkedin` only
   where it's **confidently matched** on name, current role, and
   business/location together. A same-name profile that doesn't corroborate
   on the other two is not a match — leave the field unset.
4. Note whether a named, direct business email is publicly available, or
   only a generic/reception/admin address, and any other legitimate public
   contact route worth recording in `accessibility_notes`.
5. Assign `accessibility` — `DIRECT` / `IDENTIFIABLE` / `GATEKEPT` /
   `CORPORATE` / `REVIEW` (definitions in `CAMPAIGN-HANDOFF.md`). **An
   ambiguous match is `REVIEW`, not a guess** — this is the same discipline
   as an ambiguous legal-entity match staying `REVIEW` rather than being
   silently resolved either way.
6. **If this business opted into auditable scoring (Stage 4),** also set
   `direct_dm_route` on the same 6-tier scale used verbatim in
   `CAMPAIGN-HANDOFF.md` §3a (5=confirmed direct route down to 0=no usable
   route), plus `contact_route_quality` and `contact_identity_confidence`.
   A generic inbox is never scored as equivalent to a confirmed direct
   route just because an email address exists — this is what makes
   `ready_to_email` a genuine gate rather than "an address was found".

**Never invent or infer personal contact details.** No phone number,
personal email, or address that isn't published by the business itself or a
trusted register — the same rule already governing `contact_person` and
`contact_email` applies to every accessibility field too.

**Recording a LinkedIn match here is research, not outreach.**
`playbook/decisions.md`'s "LinkedIn outreach is later, not now" is
unaffected — this stage never sends a connection request or message, it
only records where one could later go, for a separate, later decision.

## Stage 7 — Current-status / rebrand checks

Light-touch, not a repeat of Stage 5: confirm the business's site/contact
route is still live, its local presence is still current, and there's no
obvious closure, acquisition, or rebrand since the census was built. If a
status check produces a result that contradicts an earlier one in the same
session (this has happened before — a false "dissolved" reading on a live
company), don't take either on faith; cross-check against a second signal
(e.g. Companies House officers/PSC pages, not just the overview page) before
deciding.

## Stage 8 — Assign commercial opportunity

One of exactly four values — **`GAP`**, **`GROWTH`**, **`DEFEND`**, or
**`NO OPPORTUNITY`** — per the definitions in `outreach-process.md` step 4
and `CAMPAIGN-HANDOFF.md`. Rules that must hold:

- **High visibility alone is not grounds for silent, unrecorded exclusion —
  but a scored business in the small cluster already dominating its market
  (`most_named_cohort`) now defaults to `EXCLUDED`, stated as a reason
  (`ALREADY STRONGLY VISIBLE`), not a dead end.** (2026-08-24: this reverses
  the 2026-08-14 "DEFEND candidate by default, not excluded" default — see
  `playbook/decisions.md`'s "Outreach" section.) It is still a *proposal*:
  `DEFEND` remains a real, valid opportunity type for that business (a
  monitoring/retention play), and the owner can override the disposition for
  a specific business at the approval gate.
- **`GAP` / `GROWTH` / `DEFEND` describe commercial opportunity, not
  outreach priority.** Setting `opportunity_type` says nothing about how
  urgently a business should be approached — only `disposition_recommendation`
  (above) ties `DEFEND` to a default campaign disposition, and only for the
  `most_named_cohort` subset of it.
- **`REVIEW` is not a value here.** It is not a fifth (or fourth)
  opportunity type. An unclassifiable business simply gets no
  `opportunity_type` set, with the ambiguity carried by `disposition`
  and/or `priority` being `REVIEW` instead — those two fields already exist
  for exactly this.
- **A business can have a valid opportunity type while still being excluded
  from this particular campaign.** `opportunity_type` and `disposition` are
  independent — see `sample-campaign.json`'s Northgate Pipeworks for the
  shape: `DEFEND`, `EXCLUDED` from this round, both true at once.
- **A business scored per Stage 4's auditable model gets its
  `opportunity_type` from `scoring_engine.py`, not hand judgement** —
  `CAMPAIGN-HANDOFF.md` §3a's general rule (2026-08-24: `DEFEND` is
  `most_named_cohort` — an absolute visibility floor, a relative-position
  band, and a rank-within-group cap, no real-peer requirement; `GAP` is
  unconditional at zero visibility; `GROWTH` is everything else). The engine
  never produces `REVIEW` as a scored business's `opportunity_type` any
  more — an unresolved-evidence business still carries that state on
  `disposition`/`priority` instead, same as the unscored path above.

## Stage 9 — Assign disposition, reason, priority, ready_to_email

- `disposition` (`market_entry`): `OUTREACH` / `EXCLUDED` / `REVIEW`.
- `reason` (`excluded_entry`), only for `EXCLUDED`: the fixed enum in
  `schema.json` — `ALREADY STRONGLY VISIBLE` is `scoring_engine.py`'s
  proposed reason for exactly the `most_named_cohort` subset of `DEFEND`
  (Stage 8); for an unscored business, it's still a legitimate hand-judged
  reason where genuinely true.
- **`priority`** (`A`/`B`/`C`/`REVIEW`) — commercial value, not a
  visibility-size ranking. Weighs evidence quality, market relevance,
  credibility, competitive position, commercial value, and decision-maker
  accessibility (Stage 6). **Accessibility informs priority; it never
  automatically sets or overrides it.** A `GATEKEPT` business with a strong
  `GAP`/`DEFEND` case can and should stay Priority A — the workbook's
  colour-coded accessibility column exists precisely so the access problem
  is visible without silently deprioritising a genuinely strong prospect. A
  `DEFEND` business can be Priority A; a zero-visibility `GAP` business can
  be Priority C.
- **`ready_to_email`** (`YES`/`REVIEW`) — whether *this* email is
  send-ready today: verified contact, correct numbers, a truthful,
  non-misleading angle for this specific opportunity type (the framing
  principles in `outreach-process.md` step 4 — not fixed copy). For a
  business scored per Stage 4, `scoring_engine.py` proposes this value from
  `CAMPAIGN-HANDOFF.md` §3a's explicit gate (verified business, adequate
  commercial fit, sufficient evidence confidence, completed research,
  verified contact route, acceptable identity confidence) — still a
  proposal for the owner to approve, same as always, but no longer a vibes
  call: a generic inbox with an unconfirmed name can no longer read `YES`.

Every `outreach[]` entry must also carry `accessibility` by this point —
it's a required field on the schema, not an optional extra (Stage 6).

Propose values for all four `market_entry`/`outreach_entry` fields above.
Do not treat them as final yet — see the approval gate below.

## Stage 10 — Write the campaign JSON

Populate `schema.json` exactly, field by field, using
`CAMPAIGN-HANDOFF.md` §3 as the checklist and §4 for evidence rules (every
`outreach[]` claim traceable to a real `source_id`; no invented Companies
House facts, contact names, emails, director records, or LinkedIn matches;
placeholders only where the schema makes a field optional). Save to
`~/wardith-runs/<slug>/<slug>-campaign.json` — never inside this
repository.

## Stage 11 — Score, validate, and render

Run the scoring engine first — it must run before the renderer, since
`build_workbook.py`'s `validate()` requires every scored entry's derived
fields to already be populated:

```
python3 tools/prospect-compiler/scoring_engine.py \
    --input ~/wardith-runs/<slug>/<slug>-campaign.json --in-place
```

Then render **with `--require-scored`** — always, for a run produced by
this skill, since (per Stage 4) a newly-generated campaign is never
qualitative-only:

```
python3 tools/prospect-compiler/build_workbook.py \
    --input ~/wardith-runs/<slug>/<slug>-campaign.json \
    --output ~/wardith-runs/<slug>/<slug>-prospects.xlsx \
    --require-scored
```

`--require-scored` fails closed — no workbook is written — if canonical
scoring wasn't actually completed: missing `service_scopes`, missing or
incomplete `question_relevance`, a missing or incomplete `scoring_cohort`,
a cohort member that met the inclusion floor but has no cohort entry, any
`outreach[]` entry without `service_scope`, a missing
`competitive_gap_finding`/`why_prospect`, a narrative that was never
(re)generated from the entry's current scored values (`narrative_generated_from`
doesn't match — including after a re-score, e.g. a corrected mention count,
that the narrative wasn't regenerated for), `why_prospect` identical to
`business_type_notes`, or a primary visibility claim in either field that
doesn't match `relevant_appearances`/`relevant_opportunities`. **Do not omit the flag to
get a campaign to render** — an error here means the canonical inputs
genuinely aren't complete yet (Stage 4's INCOMPLETE path), not a reason to
fall back to an unflagged, permissive render. `--require-scored` is never
used when merely re-rendering a historical/legacy campaign — this skill
doesn't do that (see "What this skill does not do" below); the flag exists
specifically for this skill's own, always-new output.

If validation fails for a genuine data reason (not a canonical-scoring
gap): fix the data or this skill's output, per `CAMPAIGN-HANDOFF.md` §8's
anti-detour rule. Never create a parallel renderer or weaken the compiler's
validation to make bad data pass. After a successful render, confirm the
workbook reopens with populated calculated values in data-only mode —
`CAMPAIGN-HANDOFF.md` §3a's "Portable downstream handoff" note explains the
one narrow, documented exception (a non-ready business's `Outreach rank`
cell).

## Stage 12 — Report

Close every run with a concise completion summary — this is the one
checkpoint the owner sees, the same posture `/90qrun`'s own Step 7 takes:

- **Verdict**, stated plainly: `PASS` (every stage completed, nothing left
  ambiguous), `PASS WITH REVIEW` (a valid, `--require-scored`-passing
  campaign JSON exists, but one or more businesses are `REVIEW` on
  disposition, priority, or accessibility and need the owner's eyes), or
  `INCOMPLETE` (a stage couldn't complete, or `build_workbook.py
  --require-scored` rejected the campaign — say exactly which requirement
  is unmet, per Stage 1's fail-clearly rule and Stage 4's canonical-inputs
  gate). A campaign that only validates *without* `--require-scored` is not
  `PASS` or `PASS WITH REVIEW` for a new run — it's `INCOMPLETE`, since
  canonical scoring is mandatory going forward.
- **Total businesses assessed** — the market census count.
- **Number qualified** — the `outreach[]` count.
- **Priority breakdown** — counts of A / B / C / REVIEW among `outreach[]`.
- **Accessibility breakdown** — counts of DIRECT / IDENTIFIABLE / GATEKEPT /
  CORPORATE / REVIEW among `outreach[]`, so the access-problem shape of the
  campaign is visible in the report, not just buried in the workbook.
- **Unresolved / manual-review items** — every business left at
  `disposition: REVIEW`, `priority: REVIEW`, or `accessibility: REVIEW`,
  named individually with the one-line reason, so the owner knows exactly
  what still needs a human look and why.
- File paths: the census CSV, `mention-counts.json`, the campaign JSON, and
  the rendered workbook — all under `~/wardith-runs/<slug>/`.
- The Human Approval Table from the gate below, for the owner's actual
  review.

## The approval gate — stop here

A campaign JSON that passes validation is not the same as one that's
outreach-ready. `build_workbook.py` only checks that `priority`,
`ready_to_email` and `accessibility` hold a valid enum value — it cannot
check whether the owner has actually reviewed them. **Present the proposed
`priority` and `ready_to_email` for every `outreach[]` business for
explicit owner approval before treating any of it as final** — the same
gate `CAMPAIGN-HANDOFF.md` §5 already defines; this skill does not add a
new one or skip it because the compiler ran successfully. Show
`accessibility` alongside them in that same table for context (it shapes
how the owner might sequence contact, e.g. trying LinkedIn first on a
`GATEKEPT` Priority A) — it is a Claude-proposed research finding, not a
second formal HUMAN-gated field the way `priority`/`ready_to_email` are.

## What this skill does not do

- **Does not run or resume `tools/trade-run/`.** The 90-question stage is
  separate, paid, and manually invoked — this skill only ever reads a
  completed run's output.
- **Does not send outreach**, draft emails, connect on LinkedIn, or touch
  anything past the rendered workbook and report.
- **Does not modify `schema.json`, `build_workbook.py`, `scoring_engine.py`,
  or the playbook.** If the schema genuinely can't represent something this
  skill needs to record, that's a real blocker — stop and say so rather than
  working around it with an invented field or a notes-field workaround.
- **Does not invent or infer contact details of any kind** — names, emails,
  phone numbers, or LinkedIn matches. An ambiguous person-match is
  `accessibility: REVIEW`, never a guess dressed up as a confident one.
- **Does not touch a completed run's raw CSV, census, mention counts, or
  campaign JSON once written**, except to correct a verified factual error
  the owner has approved — the same rule already governing every
  qualification session this pipeline has run. A re-run on an
  already-qualified slug (Stage 1) extends or corrects the existing
  campaign rather than silently starting over.
