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

## GitHub Actions remote adapter

When `WARDITH_REMOTE=true`, the workflow has already used
`scripts/wardith-secrets.sh`'s allowlisted implementation to load the approved
provider and Companies House values. `BWS_ACCESS_TOKEN` is deliberately absent
by this stage. Do not call PowerShell, the Claude session hook, or Bitwarden
again. Use `python3` directly, use `$WARDITH_RUNS_DIR` instead of assuming
`~/wardith-runs`, and treat `$WARDITH_DATA_REPO` as the only repository that
may be committed and pushed. Never modify or commit the core checkout.


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

For interrupted, missing, or conflicting research, also use
`tools/prospect-compiler/REVIEW-EVIDENCE.md`. Its evidence-led routing governs bounded
missing-only resumption, request records, timing, and the final digest.

Use its **Repeatable execution contract** to open/resume a run and close the
handoff. Reuse already completed research and separately prepared content;
qualification does not recreate content or enable a weekly sending schedule.

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

If the user explicitly selects evidence-led mode with no CRM mutations,
pushes, or deploys, that instruction takes precedence over the cloud sync/CRM
adapter defaults. It does not weaken the legal-entity, scoring, readiness, or
remote credential boundaries.

For an explicitly offline/local-only evidence-led review, skip Stage 0 sync and
all CRM fetches: use the supplied local artifacts and report any missing input.

**Before Stage 1, sync `~/wardith-runs/` against the private
`hellonovenuk-lang/wardith-crm-data` repo** — this holds every trade-run
CSV, campaign folder and the CRM db, so a run started on one machine/session
picks up what an earlier run on a *different* one already produced (see
`scripts/wardith-runs-sync.sh`'s own header for the full mechanism and why
it's a separate repo from this one):

- **Cloud session** (`$CLAUDE_CODE_REMOTE` is `true`): attach the repo with
  `add_repo` (`access: "push"`, needed for the push-back after Stage 11.5)
  and run the clone command it returns, cloning to `~/.wardith-runs-repo/`.
  Then run `bash scripts/wardith-runs-sync.sh pull`.
- **Local session**: just run `bash scripts/wardith-runs-sync.sh pull` — it
  clones the repo itself on first use, using credentials already on this
  machine.

**Entirely optional and must never block the run**: if the repo doesn't
exist yet, isn't reachable, or `add_repo` fails, the script says so on
stderr and exits 0 — note that once in this stage's summary and continue
exactly as if no prior data existed, same posture as a missing
`COMPANIES_HOUSE_API_KEY`.

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
   python3 .claude/skills/90qrun/scripts/validate_run.py \
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
5. **Resume only recorded gaps.** Read the evidence register and follow
   `tools/prospect-compiler/REVIEW-EVIDENCE.md`: retain verified facts and published inboxes,
   reserve/save the exact missing fact before each external request, and do
   not reset completed research. Missing email or external corroboration is a
   parked, precise `REVIEW`/`INCOMPLETE` reason, not an owner question.

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

**Candidate-pool consistency first.** The default target is the majority of
relevant businesses outside the current most-named cohort, including
zero-appearance businesses. Set `run.cohort_inclusion_min_appearances` to `0`
before researching anyone, so every census business receives an explicit
cohort status. Apply enough initial research to every census business to
establish service/geography relevance and whether a genuine exclusion applies.
Then apply the same full qualification depth to every relevant business that is
not a centrally controlled chain or a confirmed current `most_named_cohort`
member. Do not stop after finding a small convenient shortlist or only research
businesses with five or more appearances.

Set the legacy `gap_cohort_min_appearances` and `gap_cohort_cap` fields to `0`
for this full-cohort policy. There is no below-main-floor research band when
the main floor is zero; the old lighter-research cap must not limit coverage.

**Historical policy only (2026-08-23, superseded for new qualifications on
2026-09-03): a second, lighter, capped floor existed for GAP eligibility.**
The following explains historical records, not the current research scope.
The floor above governed full canonical scoring — real
appearance-count evidence justifies that depth of research. But a
zero-appearance business is the strongest GAP case there is ("named by
nobody", `outreach-process.md` step 4), and researching only businesses that
already clear a visibility floor meant a business's own absence from the
answers silently excluded it from ever being classified as the opportunity
its absence represents. So: `run.gap_cohort_min_appearances` may be stated
as `0`, and any below-the-main-floor business up to that governs a lighter
research pass — `active_entity_verified`, `live_website_verified`,
`contact_route_exists` — instead of deep credibility/accessibility research.
(2026-08-24: `GAP` is unconditional at `visibility_score == 0`, so these
three fields no longer feed `opportunity_type` directly — the cohort
floor/cap discipline below still applies, as the mechanical budget on how
many below-floor businesses get *any* research pass this run, light or not.)
**State a cap on this
cohort before researching anyone, as data** — `run.gap_cohort_cap`, the
maximum number of below-the-main-floor businesses researched this way in
this run — same discipline as the main floor: a real number chosen for this
campaign from real cost evidence, never invented in advance and never left
unstated. (Worked example: the kitchen-and-bathroom census has 39
businesses total, only 13 clear a floor of 5 — an uncapped lighter gate
could add up to 26 more real per-business lookups in one run.) A
below-the-main-floor business beyond the stated cap stays `INCOMPLETE` in
`run.scoring_cohort` (`missing_evidence: "below this run's GAP-cohort
cap"`) — a legitimate, explicit stopping point, not a silent drop.
`build_workbook.py --require-scored` mechanically cross-checks the cap
(counts `SCORED` cohort members whose `total_ai_appearances` falls in
`[gap_cohort_min_appearances, cohort_inclusion_min_appearances)` and fails
if that count exceeds `gap_cohort_cap`) — this is not a convention to
remember, it fails the render. **`SCORED`
still means all 9 VALUE fields are set, even for a lighter-gate business**
— the Stage 6 contact/accessibility fields
(`decision_maker_identified`/`direct_dm_route`/`contact_identity_confidence`/
`research_completeness`) are honestly low rather than skipped. A low
`decision_maker_identified` or `contact_identity_confidence` records that no
named contact was found; it does not withhold the send (2026-09-05). A
`direct_dm_route` below 2 or a `research_completeness` below 3 does, because
those are the route and the evidence themselves — see §3a's gate.

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
proposed `opportunity_type` per §3a's general rule (`DEFEND` is
`most_named_cohort` — an absolute visibility floor, a relative-position band,
and, since 2026-09-05, being among the two most-mentioned businesses
campaign-wide; `GAP` is unconditional at zero visibility). These remain
*proposals*: the owner still approves `priority` and `ready_to_email` exactly as the approval gate below
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

**Check the CRM for a prior record before researching from zero.** The same
business can turn up in more than one campaign (overlapping geographies, a
re-qualified slug, a business excluded before and now reconsidered). If
`~/wardith-runs/crm/wardith.db` exists, look up this business —
`tools/crm/models.py`'s `find_prospect(conn, business=..., company_number=...)`,
matching the same `business_key` `ingest.business_key_for()` computes
(a verified `company_number` first, a slugified business name otherwise),
across every campaign, returning the most recently imported match:

```python
import sys; sys.path.insert(0, "tools/crm")
import db, models
conn = db.connect()  # default path; skip this whole check if the DB file doesn't exist yet
prior = models.find_prospect(conn, business="<business>")
```

If `~/wardith-runs/crm/wardith.db` doesn't exist yet, this check is simply
unavailable — skip it and research fresh, same as always; never treat a
missing database as a blocker.

For an offline/local-only evidence-led review, this lookup is not required;
consult a permitted local database only when it is in scope.

**On a hit:** use the record's `legal_entity`/`company_number`/
`company_status` (this stage) and `contact_person`/`role`/`contact_email`/
`decision_maker_linkedin`/`accessibility`/`accessibility_notes` (Stage 6) as
a verified starting point instead of researching from zero — but this is a
starting point, not a silent trust: Stage 7's existing light current-status
check still applies to these reused values (a director can leave, a generic
inbox can replace a named one), and a record whose `last_imported_at` is
more than roughly 90 days old should be treated as a strong hint to
re-verify in full rather than reused outright, since accessibility and
contact routes go stale faster than legal-entity status does. Record the
reuse explicitly — a `sources[]` entry or a `notes` line, e.g. "contact/
legal data reused from CRM record, originally researched `<date>`" — so it's
auditable, not a silent shortcut, matching `CAMPAIGN-HANDOFF.md` §4's
evidence-traceability rules.

**On a miss, or no CRM database yet**, research fresh, unchanged.

**Use `tools/companies-house/company_lookup.py` for fresh research, not manual
browsing, when `COMPANIES_HOUSE_API_KEY` is set:**

On Windows, invoke it through `scripts/wardith-secrets.ps1 run` so the key is
retrieved from Bitwarden for this process rather than read from a plaintext
local file.

```
python3 tools/companies-house/company_lookup.py --name "<business>" --json
```

Review the returned candidates and apply exactly the same judgement this
stage has always required — a same-name chain, a dissolved-then-
reincorporated entity, or several plausible matches is still not a defensible
match; **the API returns candidates, it does not pick one.** Confirm a match
with `--number <company_number>` when the profile detail (status, type,
registered office) is needed to settle it. If `COMPANIES_HOUSE_API_KEY`
isn't set (see `tools/companies-house/README.md` for the free one-time
setup), fall back to the existing `WebFetch`/`WebSearch` method against the
Companies House website unchanged — this is never a reason to stop or block
a `/qualify` run.

## Stage 6 — Contact-route, decision-maker discovery, and accessibility classification

**If Stage 5's CRM check found a prior record for this business**, start
from its `contact_person`/`role`/`contact_email`/`decision_maker_linkedin`/
`accessibility`/`accessibility_notes` per that stage's reuse rule (still
subject to Stage 7's light current-status check, and to full re-research if
the record is stale) rather than researching this section from zero.

For businesses heading toward `outreach[]` with no reusable prior record:
find the best verified contact route, preferring in order — named
owner/director/manager with a business email, named decision-maker with a
contact form or business inbox, a verified generic business inbox, an
official website contact form, then a trusted portal enquiry route only if
nothing better exists. Never invent a name, role, or email, and never infer
an email pattern that hasn't been independently confirmed on the business's
own site or a trusted source.

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
   A generic inbox is never *scored* as equivalent to a confirmed direct
   route just because an email address exists — it grades lower and ranks
   lower. It is still a valid route to send on (2026-09-05): `direct_dm_route
   >= 2` is the floor `ready_to_email` requires, so a verified business inbox
   with no named contact qualifies, while a contact form or phone number
   alone (`1`) or no route at all (`0`) does not.

**Never invent or infer personal contact details.** No phone number,
personal email, or address that isn't published by the business itself or a
trusted register — the same rule already governing `contact_person` and
`contact_email` applies to every accessibility field too.

Use the evidence routing reference for a missing email or unresolved route:
retain a verified generic inbox with its actual route quality, otherwise park
the business with the exact missing evidence. Do not promote it, repeat
completed searches, or ask the owner to supply an external fact.

**Missing optional information never blocks a prospect.** A name, a role, a
LinkedIn profile, a phone number, a registered address: absent, the field
stays unset and the record proceeds on what is verified. What is never done
is filling the gap — no invented or inferred contact name, address or
finding, ever, and no name in an email that was not confirmed.

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
  but the two most-mentioned businesses in the campaign (`most_named_cohort`)
  default to `EXCLUDED`, stated as a reason (`ALREADY STRONGLY VISIBLE`), not
  a dead end.** They keep every scored field and stay in the market analysis;
  only their default disposition changes. (2026-09-05: the hold-out is a
  campaign-wide count of two, replacing a rank-within-service-scope cap that
  could hold out five businesses per scope group — see
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
  `CAMPAIGN-HANDOFF.md` §3a's general rule (`DEFEND` is `most_named_cohort`
  — an absolute visibility floor, a relative-position band, and being among
  the two most-mentioned campaign-wide; `GAP` is unconditional at zero
  visibility; `GROWTH` is everything else). The engine never produces `REVIEW` as a scored business's `opportunity_type` any
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
  commercial fit, sufficient evidence confidence, completed research, a
  verified contact route, and a usable route to the business) — still a
  proposal for the owner to approve, same as always, but no longer a vibes
  call. As of 2026-09-05 a named decision-maker is **not** part of this gate:
  a verified business inbox is enough to send to the business, and where no
  name is confirmed, no name goes in the email.

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

**Recalculate before release.** Follow the live-recalculation acceptance check
in `tools/prospect-compiler/REVIEW-EVIDENCE.md`. Correct saved values and a
strict-validator PASS do not prove live formulas are correct. Hold only the
affected workbook if recalculation fails; preserve campaign data and report
the precise repair needed. Do not restart business research for a renderer bug.

## Stage 11.5 — Auto-ingest into the CRM

Skip this entire stage when the user explicitly selected evidence-led mode
with no CRM mutations, pushes, or deploys. Record the intentional skip in the
final digest; it does not affect the campaign verdict.

Immediately after a successful render, pull this campaign into the CRM so
its data is live there without a separate manual refresh:

```
python3 tools/crm/main.py ingest --slug <slug>
```

`tools/crm/ingest.py` is stdlib-only (`requirements.txt`'s `flask`
dependency is used only by `serve`, never by `ingest`) and is documented as
safe to run at any time, including mid-run on another campaign
(`tools/crm/README.md`). It reads only files already written by this skill
under `~/wardith-runs/<slug>/`, and its only write is to the CRM's own
SQLite database (`~/wardith-runs/crm/wardith.db`) — never back into the
campaign JSON or workbook.

**Never let this stage affect this run's verdict.** The campaign JSON and
workbook are already correct and complete before this stage runs; a failure
here (the CRM not yet set up, `pip install -r tools/crm/requirements.txt`
never run, whatever) is recorded as one line in Stage 12's report — ingested
OK, or failed and why — and never downgrades `PASS`/`PASS WITH
REVIEW`/`INCOMPLETE`.

**Where Stage 0 synced against `wardith-crm-data`** (cloud or local), and
evidence-led mode has not prohibited pushes: once
`ingest` above succeeds, run
`bash scripts/wardith-runs-sync.sh push "qualify <slug>"` to commit and push
everything this run wrote — the campaign folder and the updated `wardith.db`
— back to that repo. In a cloud session this is the only thing standing
between this run's output and it being lost when the VM is reclaimed. Same
non-blocking rule as the ingest step itself: a push failure is one more line
in Stage 12's report, never a reason to downgrade the verdict. Skip silently
if Stage 0 never found or attached the repo.

## Stage 11.6 — Deliver the workbook to the owner's phone, in a cloud session

`~/wardith-runs/<slug>/<slug>-prospects.xlsx` lives only on the session's own
disk, which is wiped when a cloud session's VM is reclaimed — there is no
local machine for the owner to walk over to. If `$CLAUDE_CODE_REMOTE` is
`true`, send the rendered workbook to the owner with the `SendUserFile` tool
(`status: normal`, since this is the direct answer to a run they triggered)
immediately after Stage 11.5, before writing the Stage 12 report. This is a
convenience copy for the owner to read or save locally later — it is not
the system of record; the durable campaign JSON and the CRM update from
Stage 11.5 remain the system of record. Skip this step entirely in a local
session (`$CLAUDE_CODE_REMOTE` unset or `false`) — the owner already has the
file on their own disk there.

## Stage 12 — Report

Include the close-out fields from the repeatable execution contract. A bounded
review pass may be finished while full-market qualification is INCOMPLETE.
Keep factual gaps, execution-control failures, file validation, owner approval
and deployment status separate. Deliver the verified subset with its exceptions
and stop; reopening parked research requires a recorded new reason, not another
generic `continue` or an attempt to fill the shortlist artificially.

Close every run with a concise completion summary — this is the one
checkpoint the owner sees, the same posture `/90qrun`'s own Step 7 takes:

- **Verdict**, stated plainly: `PASS` (every stage completed, nothing left
  ambiguous), `PASS WITH REVIEW` (a valid, `--require-scored`-passing
  campaign JSON exists, but one or more businesses remain `REVIEW` with a
  precise parked-evidence reason or await the final policy digest), or
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
- **Parked evidence items** — every business left at
  `disposition: REVIEW`, `priority: REVIEW`, or `accessibility: REVIEW`,
  named individually with the exact missing or conflicting evidence and the
  next source or stop reason.
- File paths: the census CSV, `mention-counts.json`, the campaign JSON, and
  the rendered workbook — all under `~/wardith-runs/<slug>/`. In a cloud
  session, note that the workbook was also sent directly via Stage 11.6.
- **CRM ingest result** from Stage 11.5: ingested OK, or failed and why —
  never affects the verdict above.
- The Human Approval Table from the gate below, for the owner's actual
  review.

Also produce the census-wide selection coverage report before assigning the
verdict:

```
python3 tools/prospect-compiler/qualification_coverage.py \
    --input ~/wardith-runs/<slug>/<slug>-campaign.json \
    --census ~/wardith-runs/<slug>/market-census-<slug>.csv \
    --output ~/wardith-runs/<slug>/qualification-coverage-<slug>.json \
    --require-complete
```

Report its `SEND NOW`, `SECONDARY`, `REVIEW`, `EXCLUDE`, and `INCUMBENT`
counts, plus `potential_non_top` and every missing census business. `SEND NOW`
is a proposal for owner approval, never permission to send. A suitable active
Ltd/LLP reached through a verified general business inbox now reaches `SEND
NOW` on its own evidence; a named person is never invented to get it there.

**Aim for 10–15 `SEND NOW` prospects per market — a target, not a quota.**
Where a market holds fewer suitable businesses than that, the honest number
is the answer. When fewer than 10 qualify, **state the actual blockers** —
the coverage report names them per business, so report which ones recur and
how many businesses each accounts for. Do **not** automatically commission
more research, re-run searches already completed, relax a gate, or promote a
parked business to close the gap: reopening parked research needs a recorded
new reason, exactly as this stage already requires.

If coverage is `INCOMPLETE` or the command exits nonzero, the overall verdict
is `INCOMPLETE`, even if workbook validation passed. Name each missing or
unfinished cohort assessment from `completion_blockers`. On a repeat review,
use a new dated/attempt-suffixed report path; never overwrite the prior report.

## The approval gate — one final digest

A campaign JSON that passes validation is not the same as one that's
outreach-ready. `build_workbook.py` only checks that `priority`,
`ready_to_email` and `accessibility` hold a valid enum value — it cannot
check whether the owner has actually reviewed them. **Present one final digest
containing the proposed `priority` and `ready_to_email` for every `outreach[]`
business for explicit owner policy approval before treating any of it as
final.** Do not stop for individual approval questions about missing emails or
external facts. The final digest is the same gate `CAMPAIGN-HANDOFF.md` §5
defines; this skill does not add a new one or skip it because the compiler ran
successfully. Show
`accessibility` alongside them in that same table for context (it shapes
how the owner might sequence contact, e.g. trying LinkedIn first on a
`GATEKEPT` Priority A) — it is a Claude-proposed research finding, not a
second formal HUMAN-gated field the way `priority`/`ready_to_email` are.

## Content handoff — offer, do not run

Once the owner has responded to the approval table and the campaign has a
`PASS` or `PASS WITH REVIEW` verdict, check the evidence already loaded for one
genuinely publishable market finding. This is a light handoff assessment, not a
new research stage.

- If there is a worthwhile finding, state it in one sentence and offer the exact
  next action: `/content <campaign-slug>`. Do not invoke `/content`, create a
  content folder or draft a post until the owner explicitly accepts the offer.
- If there is no finding strong enough to publish, say so plainly and make no
  content offer. A completed qualification does not create a content quota.

Judge usefulness separately from outreach priority. Prefer a clear market-wide
pattern that can be explained without exposing a prospect negatively. A named
business is suitable only under the positive-recognition rule in
`playbook/decisions.md`. The later `/content` run owns the final evidence,
editorial and brand checks; this handoff only identifies the opportunity.

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
