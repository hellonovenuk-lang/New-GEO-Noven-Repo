---
name: outreach
description: >-
  Take an already-qualified Wardith campaign (a `/qualify` output — a
  validated campaign JSON with disposition, opportunity_type, priority and
  ready_to_email already set) and prepare first-touch outreach for every
  business approved for contact: the strongest business-specific reason to
  approach them, a light re-check of the contact route, a personalised email
  draft, a draft-only LinkedIn note where a named contact exists, and a
  structured record linking back to the source campaign and evidence. Use
  this whenever the owner asks to prepare, draft or get ready outreach/emails
  for a qualified campaign, or names a campaign slug and asks what's
  send-ready. Does not rerun research or qualification, does not re-decide
  priority or ready_to_email, and never sends or posts anything — every
  email is pushed into the owner's Zoho Mail account as a draft for human
  review, and sending it stays a separate human action there.
---

# /outreach

## GitHub Actions remote adapter

When `WARDITH_REMOTE=true`, the workflow has already used
`scripts/wardith-secrets.sh`'s allowlisted implementation to load the approved
values. `BWS_ACCESS_TOKEN` is deliberately absent by this stage. Do not call
PowerShell, the Claude session hook, or Bitwarden again. Use `python3` directly
and `$WARDITH_RUNS_DIR`. Before the Zoho draft tool runs, write
`$WARDITH_ZOHO_CREDENTIALS_JSON` to a mode-600 temporary file, set
+`WARDITH_ZOHO_CREDENTIALS` to that path, and remove the file immediately after
the tool exits. Treat `$WARDITH_DATA_REPO` as the only repository that may be
committed and pushed. Never modify or commit the core checkout, and never send
or transmit outreach; Zoho drafts remain the maximum external effect.


Invoked as `/outreach <campaign>`, where `<campaign>` is the same slug
`/qualify` used (e.g. `estate-agents-chester`), or a direct path to a
campaign JSON. From the slug, the canonical locations follow `/qualify`'s
own convention:

```
campaign JSON:     ~/wardith-runs/<slug>/<slug>-campaign.json
mention counts:     ~/wardith-runs/<slug>/mention-counts.json  (optional, see Stage 2)
output folder:      ~/wardith-runs/<slug>/outreach/
```

**Source of truth for everything commercial here:**
`playbook/outreach-process.md` (why — the process, the letter shapes, the
legal rules) and `tools/prospect-compiler/CAMPAIGN-HANDOFF.md` (how the
campaign JSON's fields are defined). This file is the procedure that turns
an already-approved campaign into outreach drafts; it does not restate their
content, and if this file and either of them disagree, they win.

**This skill is stage three.** `/90qrun` collects the raw data, `/qualify`
turns it into a validated, human-approved campaign JSON. This skill only
ever reads that finished JSON and drafts from it — it does not gather new
evidence, does not re-run mention counting or legal verification, and does
not change `priority`, `ready_to_email`, `disposition` or `opportunity_type`.
If any of those look wrong, that's a `/qualify` problem — stop and say so
rather than silently correcting it here.

## Stage 0 — Scope the run and ask for approval once

Before touching anything, state plainly what this run is about to do, so the
necessary tool approvals can be granted once, up front, rather than
interrupting for every individual file read, web check, or file write:

- **Read-only** against everything under `~/wardith-runs/<slug>/` — the
  campaign JSON, `mention-counts.json` if present, and nothing else in that
  folder (never the raw run CSV, never the census, never the workbook).
- **A small number of outbound web checks** (`WebFetch`/`WebSearch`), one
  or two per eligible business, to reconfirm a contact route is still live —
  see Stage 4. Nothing is submitted to any site; these are page reads only.
- **Writes**, confined to a new `~/wardith-runs/<slug>/outreach/` folder —
  never inside this repository, never anywhere else on disk.
- **Creates/updates Zoho Mail drafts, never sends.** Stage 7.5 pushes each
  drafted email into the owner's Zoho Mail Drafts folder via
  `tools/zoho-draft-push/`. In Zoho's API, saving a draft and sending are the
  *same* endpoint under the same `ZohoMail.messages.CREATE` scope — the only
  difference is the `mode` field in the request body — so what guarantees no
  send is that tool's own payload construction: a closed dict of six literal
  keys with `mode` hardcoded to `"draft"`, never derived from campaign data,
  asserted by its tests. Reply, delete and folder-move are separate API
  surfaces this code never calls — not surfaces the scope is incapable of
  reaching (delete and folder-move do need scopes this token lacks, but
  reply is documented under this same `ZohoMail.messages.CREATE` scope,
  same as send above). Nothing in this
  skill contacts a business, submits a form, connects on LinkedIn, or posts
  anywhere else. Actually sending an email is still a separate, explicit,
  later action the owner takes inside Zoho Mail after reviewing the draft
  there. **If the owner asks this skill to actually send — not just draft —
  stop and say that's out of scope for `/outreach`.** Stage 7.5 only ever
  creates a draft; sending is a separate, later, explicitly human step the
  owner takes in Zoho Mail themselves. Don't route around that with a
  different tool, a changed `mode`, or a mail client.

Say this once at the start in one message, then run the rest of the stages
straight through without pausing for approval again — the same pattern
`/90qrun` and `/qualify` already use. Only stop mid-run for a genuine
blocker (Stage 1's gate, a missing required field, a contact route that no
longer resolves at all) — not for routine reads, checks or writes already
covered by the scope above.

## Stage 1 — Load the campaign and gate the working set

Load the campaign JSON. Confirm it validates against
`tools/prospect-compiler/schema.json` in shape (it should already, as
`/qualify`'s own output) — if it doesn't, stop; this skill does not fix a
malformed campaign file, `/qualify` does.

**The working set is exactly `outreach[]` entries where
`ready_to_email == "YES"`.** Nothing else in the file gets drafted:

- `ready_to_email == "REVIEW"` — withheld. Not a lesser version of the
  pipeline, entirely out of scope.
- Anything in `excluded[]`, or a `market[]` entry that never reached
  `outreach[]` — withheld, no exceptions, regardless of how strong its
  `opportunity_type` looks.
- If `outreach[]` is empty or nothing has `ready_to_email: YES`, stop and
  report that plainly — there is nothing for this skill to do yet.

Report the working set before drafting anything: business name, priority,
opportunity_type (or "not set" — see Stage 2), and area. This is the list
Stage 2 onward will process, one business at a time. **Read every business
name straight off the file — for the working set and for whatever's being
left out (`REVIEW`, `excluded[]`).** Do not reconstruct or guess a withheld
business's name from memory of a similar campaign; a wrong name in a report
about who *wasn't* contacted is exactly the kind of invented fact
`CLAUDE.md` forbids.

## Stage 2 — The strongest business-specific reason to approach them

For each business in the working set, the angle comes from fields the
campaign JSON already carries — never from a generic "AI visibility" claim
invented fresh:

- `competitive_gap_finding` — the one factual sentence already written
  during qualification. This is the anchor claim.
- `why_prospect` — the commercial case already made.
- `strongest_competitor` / `competitor_appearances` / the business's own
  `total_ai_appearances` (and the per-provider breakdown where it sharpens
  the point) — the comparison that makes the finding checkable.
- `opportunity_type`, **when it's set** — GAP / GROWTH / DEFEND shapes the
  angle (see Stage 5). **It is often not set** (optional field, per
  `CAMPAIGN-HANDOFF.md` — most census entries don't get one). When it's
  missing, read the shape directly off the numbers instead of guessing a
  label: zero or near-zero appearances against a strong competitor reads as
  the GAP/absent shape; meaningful-but-behind appearances read as the
  GROWTH shape; a sharp single-provider gap (strong on one assistant,
  almost silent on another) reads as the per-assistant shape. Do not write
  `opportunity_type` back into the file either way — that's a `/qualify`
  field, not this skill's to set.
- `mention-counts.json`, **only if it exists and only when the campaign
  JSON's own prose doesn't already give a specific enough hook** — it has a
  `per_question` breakdown per business that can sharpen a claim (e.g.
  "absent from the emergency-dentist question specifically"). Don't
  parse the raw run CSV directly; if the finding isn't already in the
  campaign JSON or `mention-counts.json`, it isn't evidence this skill has
  — don't reach further for it.

**Never invent a finding, a number, or a form of words the evidence doesn't
support.** If a business's evidence is thin, the angle stays thin too —
that's a caveat to record (Stage 7), not a gap to paper over.

**Two specific checks worth doing every time, because both have already
caught a real problem in this skill's first run:**

- **A per-question "absence" is only a gap if the comparator actually
  scores on that question.** Check `mention-counts.json`'s `per_question`
  for the `strongest_competitor` on the same question before citing it — a
  question nobody in the market gets named on (this happens; some question
  phrasings produce generic, no-business-named answers from every
  assistant) isn't evidence of a competitive gap, just a dead question.
- **A named individual credited with a fact in `why_prospect` or
  `competitive_gap_finding` is not necessarily `contact_person`.** Trace
  the claim back to its actual source in `sources[]` (via
  `evidence_source_ids`) and confirm the source names the *same* person the
  campaign JSON put in `contact_person` before repeating the claim in an
  email addressed to that person. Qualification prose can conflate two
  different named people at the same business (an owner and an unrelated
  named staff member, say) — attributing the wrong person's credential to
  the person you're emailing is a factual error in a legal document, not a
  style problem.

## Stage 3 — Opportunity signal shapes the framing, never the literal label

`playbook/outreach-process.md` step 4 defines the framing principle per
type — write the actual sentence from this business's real evidence, never
reuse another business's wording with the nouns swapped:

- **GAP-shaped** (absent or materially underrepresented): *"You appear
  materially less often than businesses you directly compete with."*
- **GROWTH-shaped** (meaningful visibility, still behind): *"You already
  have meaningful AI visibility, but our research shows clear room to
  strengthen that position."*
- **DEFEND-shaped** (already a leader): *"You currently hold one of the
  strongest AI recommendation positions in your local market. We can show
  you what is supporting it and monitor whether that changes."*

**Do not literally write "GAP", "GROWTH" or "DEFEND" into a prospect-facing
email** unless there's a specific reason a customer-facing sentence would
need that exact word (there normally isn't) — these are internal labels for
picking the shape, not marketing copy.

**Commercial rules, all binding:**

- **The Audit (£250, `playbook/services.md`) is the only thing on offer.**
  Every opportunity type routes through it first. Do not mention Foundation,
  Maintain, Grow or Lead — not even to preview them.
- **Do not overclaim.** The free part is what was asked, how many times, who
  got named, whether this business did — all independently checkable. The
  paid part is *why*, and what to do about it. Never imply the free finding
  already explains the cause.
- **No invented case studies, results, stats, or outcomes.** If Wardith
  hasn't published or verified something, it doesn't go in the email.
- **Human, concise, commercially direct.** The aim is to start a
  conversation and sell the Audit — not to explain AI visibility, Wardith's
  methodology, or the difference between GAP/GROWTH/DEFEND.

**Letter shapes already drafted and approved live in
`playbook/outreach-process.md`** — the absent letter and the ChatGPT-gap
letter are GAP-shaped templates ready to adapt. A GROWTH letter is drafted
there too as of this skill's first run (see the file for the current text);
if a business's shape doesn't match any letter drafted there yet (most
likely: a genuine DEFEND case), draft one from the framing principle above,
follow the structural rules below, and flag it in the caveats (Stage 7) as
a first-of-its-kind letter for the owner to read with extra care.

## Stage 4 — Verify the contact route, bounded

A campaign can be a day or weeks old by the time this runs. For each
business in the working set, one bounded check — not a re-run of
`/qualify`'s own contact-discovery stage:

1. `WebFetch` the website/contact-page URL already recorded in this
   business's evidence (`website`, or the source whose `fact_supported`
   describes the contact route). Confirm it still resolves and still shows
   the same contact route (same named person, if one was recorded; same
   generic inbox, if that's what's on file).
2. **If that fetch fails or the URL doesn't resolve, don't conclude the
   route is dead on one attempt.** Check whether this business's own
   `evidence_source_ids` include a *different* URL (a second page already
   cited as a source) and try that before giving up — a campaign's
   top-level `website` field and its evidence sources have already
   disagreed once in testing (two live domains for one practice). If an
   alternate evidenced URL confirms the contact route, use it and record
   the mismatch as a caveat (Stage 7) rather than silently picking one.
   Only if nothing in this business's own evidence resolves at all does the
   route count as genuinely dead.
3. If nothing resolves, or the named contact has visibly changed, **do not
   silently use the stale value** — record it as a caveat (Stage 7) and
   drop `ready_to_email` to withheld for this business in this skill's own
   output only (never edit the campaign JSON itself).
4. If `contact_person` is `[PLACEHOLDER]`, make one bounded look at the same
   page(s) already fetched for a named owner/manager/director/principal —
   someone plausibly able to say yes to a £250 audit. If nothing verifiable
   turns up, leave it as `[PLACEHOLDER]` and address the email to the
   generic inbox per Stage 6's gatekeeper form — never invent a name.
   **A real named person who isn't a plausible decision-maker (a
   complaints contact, reception, an unrelated named staff member) doesn't
   count either** — keep `contact_person` as `[PLACEHOLDER]`, record why in
   a caveat, and don't draft a LinkedIn note to them (Stage 6 requires a
   sensible contact, not merely an available name).
5. Do not widen this into new legal-entity or geography checks. That work
   already happened in `/qualify`; repeating it here is scope creep, not
   diligence.

## Stage 5 — Draft the email

One email per business in the working set (unless Stage 4 withheld it).

**Structure, per `playbook/outreach-process.md` and `playbook/voice.md`:**

- **Subject: the business's own name, plus routing, no claim, no
  technology word.** `{Business} — for {named person}`, or
  `{Business} — for the practice owner` (or equivalent) on a generic inbox.
- **Say who you are before what was found** — `playbook/voice.md`'s single
  most important rule. Open "I'm Kieran Smith. I run a small business [...]
  that checks what the AI assistants say [...]", not "I asked ChatGPT...".
- **Writing to a named person:** address them directly.
- **Writing to a generic inbox with no named contact:** use the gatekeeper
  opening in `playbook/outreach-process.md` — ask reception to pass it on,
  say what it is in one line, drop the second greeting.
- **The finding**, in the business's own real numbers and (where the
  question set supports it) a real quoted question from
  `run.questions` — never a paraphrase of the question actually asked.
  **For "how many answers came back" framing, use `run.expected_responses`
  and `run.successful_responses` directly** (both are plain structured
  fields on every campaign) rather than re-deriving the figure from
  `methodology_notes` free text — say "ninety questions, all ninety came
  back" when they're equal, or the honest split ("ninety questions, N came
  back with an answer") when they're not.
- **The offer**: the Audit only, £250, what it covers, "yours to act on
  with me or without me" — the existing letters' own phrasing is already
  approved copy, reuse its shape.
- **The self-audit link** (`wardith.co.uk/ask-your-ai/self-audit/`) as the
  "see one first" proof point.
- **The GDPR Article 14 line** — "I found {business} on {X}, and the rest
  from your own website." **{X} must be the actual publisher of this
  business's own evidence** (check `evidence_source_ids` → `sources[]` →
  `publisher` for this specific business) — never assume a directory name
  from a different campaign or a different business in the same campaign.
  If no directory/portal source is actually recorded for this business
  (only Companies House, its own site, and/or the raw run itself), say so
  honestly instead — e.g. "I found {business} through my own research into
  {sector} in {area}, and checked it against Companies House and your own
  website." Do not name a source that isn't in this business's own
  `evidence_source_ids`.
- **The opt-out line** and a note that the normal Wardith signature
  (`assets/brand/email-signature.html`) is appended when this is actually
  sent — do not hand-copy the signature markup into the draft.
- **Run it against `playbook/voice.md` before finishing** — the rule-of-
  three, staccato rhythm, em dashes and machine vocabulary this skill's own
  drafting is as prone to as any other written-by-a-model text.

## Stage 6 — Draft LinkedIn outreach, never send

`playbook/decisions.md` records "LinkedIn outreach is later, not now" —
that decision is about *sending*, not about having a draft ready. This
skill prepares LinkedIn material exactly like the email: never dispatched,
clearly marked as a draft awaiting a separate, later decision to actually
use the channel.

- **Only where a real named contact exists** (`contact_person` not
  `[PLACEHOLDER]` after Stage 4). No named person, no LinkedIn draft — do
  not draft a note to a company page or a guessed name.
- Draft a short connection-request note carrying the same real finding as
  the email, in the same voice, same commercial rules (Audit only, no
  overclaiming). **Count the characters and keep it at or under 300** —
  LinkedIn's connection-note limit is a hard cap, not a stylistic target,
  and a first draft written to "roughly 300" ran over it twice in testing.
  Trim before finalizing, don't leave it for the owner to notice.
- Label it unmistakably in the output: `LINKEDIN DRAFT — NOT SENT. Prepared
  under playbook/decisions.md's "LinkedIn outreach is later, not now" —
  requires a separate, later decision before any send.`

## Stage 7 — Record the structured output

Write two files per campaign to `~/wardith-runs/<slug>/outreach/`:

**`outreach-prep-<slug>-<date>.json`** — one array, one object per business
processed (including any withheld at Stage 4, so the record explains why),
with exactly these fields:

```
{
  "campaign_slug": "...",
  "business": "...",
  "area": "...",
  "opportunity_type": "... or null",
  "priority": "A/B/C",
  "ready_to_email_source": "YES",        // the campaign JSON's own value, carried through unchanged
  "withheld": false,                      // true if Stage 4 dropped it, with "withheld_reason"
  "withheld_reason": null,
  "contact_route": {
    "person": "... or [PLACEHOLDER]",
    "role": "... or [PLACEHOLDER]",
    "email": "...",
    "route_verified_date": "YYYY-MM-DD"
  },
  "outreach_angle": "one or two sentences, the Stage 2/3 synthesis",
  "email_subject": "...",
  "email_body": "...",
  "linkedin_draft": "... or null",
  "caveats": ["..."],
  "evidence_source_ids": ["..."],          // carried from the campaign entry, unchanged
  "source_campaign_json": "~/wardith-runs/<slug>/<slug>-campaign.json",
  "zoho_draft_id": "... or absent, written by Stage 7.5",
  "zoho_push_status": "OK / FAILED: ... / SKIPPED (withheld) / DRY-RUN (...), written by Stage 7.5",
  "zoho_push_action": "created / updated / create / update, written by Stage 7.5",
  "zoho_pushed_at": "YYYY-MM-DDThh:mm:ssZ or absent, written by Stage 7.5"
}
```

**`outreach-prep-<slug>-<date>.md`** — the same content, rendered for a
human to actually read: one section per business, the email shown in full
(subject + body, as it would be sent), the LinkedIn draft if any, and the
caveats. This is the file the owner reviews before anything is ever sent —
render it in full, not summarised.

**Never write into the campaign JSON, the workbook, or anywhere inside this
repository.** This skill's only writes are the two files above.

## Stage 7.5 — Push drafts to Zoho Mail

On Windows, run the command below through `scripts/wardith-secrets.ps1 run`;
the wrapper supplies a temporary Zoho credential file from Bitwarden and
removes it when the process exits.

Immediately after writing both Stage 7 files, push every drafted email into
Zoho Mail as a real draft:

```
python3 tools/zoho-draft-push/zoho_draft_push.py \
    --input ~/wardith-runs/<slug>/outreach/outreach-prep-<slug>-<date>.json \
    --in-place
```

This is the one point in this skill's pipeline that touches an external
API — see `tools/zoho-draft-push/README.md` and the script's own docstring
for the exact, narrow set of calls it's capable of making (create/update a
draft only; never send, reply, or delete). `--in-place` writes
`zoho_draft_id`/`zoho_push_status`/`zoho_push_action`/`zoho_pushed_at` back
into each processed entry in the same JSON file, so re-running `/outreach`
on this campaign later updates the existing Zoho draft instead of creating
a duplicate.

**If `tools/zoho-draft-push/README.md`'s one-time setup hasn't been run
yet**, this step will fail with a clear message pointing at that file — stop
and tell the owner, don't silently skip Stage 7.5 or fall back to leaving
drafts local-only without saying so.

**A single business's push failing (a stale contact address Zoho rejects, a
transient network error) does not stop this stage** — it's recorded in the
script's summary and carried into Stage 8's report; every other business's
draft still gets pushed.

## Stage 8 — Report

- The campaign processed, and the working set size (how many
  `ready_to_email: YES` entries existed, how many were actually drafted,
  how many withheld at Stage 4 and why).
- File paths for both output files.
- The full text of every email drafted, shown directly in the response —
  this is the point at which the owner reviews before any send.
- Any LinkedIn drafts, clearly marked not-sent.
- **Zoho push results** from Stage 7.5: how many drafts created, how many
  updated, how many failed and why (business name + reason for each
  failure), how many skipped as withheld.
- A one-line reminder: **nothing has been sent; the drafts are sitting in
  Zoho Mail's Drafts folder for review, and sending is a separate,
  explicit, later action the owner takes there.**

## What this skill does not do

- **Does not rerun `/90qrun` or `/qualify`.** It reads their finished output
  only. A gap in the evidence is a reason to flag a caveat, not a reason to
  go research it from scratch.
- **Does not set or change `disposition`, `opportunity_type`, `priority` or
  `ready_to_email`.** Those are `/qualify`'s fields, human-approved there.
  This skill can *withhold* a business from its own output (Stage 4), but
  never edits the campaign JSON to do it.
- **Does not send email, reply to email, delete email, or post to
  LinkedIn.** Stage 7.5 creates/updates a Zoho Mail *draft*. Because Zoho
  saves a draft and sends through the same endpoint and the same
  `ZohoMail.messages.CREATE` scope, what rules a send out is not the scope
  but `tools/zoho-draft-push/`'s payload: a closed set of literal keys with
  `mode` hardcoded to `"draft"` and never taken from campaign data, enforced
  by that tool's tests. Reply, delete and folder-move are separate Zoho API
  surfaces nothing in this pipeline calls. Every output remains a draft for
  human review; sending is still a separate, explicit, later human action.
- **Does not sell Foundation, Maintain, Grow or Lead.** The Audit is the
  only offer this skill ever drafts.
- **Does not process `REVIEW` or `EXCLUDED` businesses**, regardless of how
  strong their evidence looks — that gate is `/qualify`'s and the owner's,
  not something this skill second-guesses.
