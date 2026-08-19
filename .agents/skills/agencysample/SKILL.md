---
name: agencysample
description: >-
  Produce a free sample AI-visibility benchmark for one publicly evidenced
  client of a named SEO agency, and the outreach preparation to approach that
  agency with it. Establishes the agency as a live limited company or LLP and
  the agency-client relationship from public evidence, builds a client-specific
  six-question framework, runs the existing 90-query trade-run pipeline against
  it, counts mentions against the peer set the answers themselves named,
  analyses the cited sources, and writes a condensed sample report plus an
  outreach brief and email draft. Use this whenever the owner asks to prepare a
  sample, demo or pilot benchmark for an SEO agency, or names an agency and one
  of its clients. Never contacts the end client, never sends anything, and
  never gives away the full paid Benchmark.
---

# /agencysample

Invoked as `/agencysample <SEO agency> - <client>`, optionally
`/agencysample <SEO agency> - <client> - <geography>`. Split on ` - ` or
` | ` specifically, never a bare hyphen, so `Stoke-on-Trent` and
`Smith-Hollis Digital` still parse as one token each — the same rule
`/90qrun` uses.

**The product this is a sample of:** `playbook/agency-product.md`. Read §1
and §8 before the first run. This file is the procedure; that file is the
product, and if the two disagree it wins.

**Who this is for.** Wardith approaches the **agency**. The agency's client
is the subject of the research and is never contacted, never emailed, and
never told this happened. Everything produced here goes to Wardith, for
Wardith to send to the agency.

## Where things go

```
work folder:   ~/wardith-runs/agency/<agency-slug>/<client-slug>/
  questions.csv            the six-question framework  (NEVER committed)
  run.csv                  raw trade-run output
  census.csv               the peer set
  mention-counts.json
  baseline.json
  citation-analysis.json
  site-check.json
  sample-report-<date>.md  the condensed report, agency-facing
  outreach-brief-<date>.md the approach, for Wardith
  outreach-prep-<date>.json
```

**Nothing here enters this repository, including the question file.**
`/90qrun` commits its question set because a trade run names no business;
this one names a real client on at least two questions, and `CLAUDE.md`'s
rule about client and prospect names is absolute.

## Stage 0 — Scope the run, ask once

State plainly what this run will do, so approvals are granted once rather
than per file — the same posture `/90qrun`, `/qualify` and `/outreach` take:

- **Outbound web reads** — Companies House, the agency's own site, the
  client's own site, and whatever public source evidences the relationship.
  Page reads and searches only; nothing is submitted to any site.
- **Paid API calls** — 90 queries across the three providers, roughly $15.
  Confirm the spend caps in `playbook/records-and-data.md` are set before
  Stage 4 spends anything.
- **Writes**, confined to the work folder above.
- **No sends.** No email, no form, no LinkedIn, nothing that transmits
  anywhere. This skill prepares. Sending is a separate, later, human act —
  `playbook/outreach-process.md`, unchanged.
- **No contact with the end client**, in any form, at any stage.

Then run Stages 1–9 straight through. Stop only for a genuine blocker: the
Stage 1 gate fails, preflight finds a missing key, or a provider fails
outright. Anything smaller is handled and folded into the report.

## Stage 1 — The gate: agency, and evidenced relationship

**Both halves must pass before any money is spent.** This is the stage that
fails most often and it is meant to.

1. **The agency is a live limited company or LLP**, verified by name at
   Companies House. `playbook/decisions.md`: never contact anyone without a
   live limited company or LLP — PECR, not a preference. A sole trader
   agency is a stop, however good the research would be.
2. **The agency–client relationship is publicly evidenced.** Record the URL,
   the publisher and the access date for each piece. Acceptable evidence, in
   descending strength:
   - the agency's own case study, portfolio or client page naming the client;
   - the client's site crediting the agency, or a shared press release;
   - a trade-press or awards listing naming both.

   **A guess is not evidence.** An agency that lists "clients in the glazing
   sector" does not evidence a particular glazier. No evidence, no run — say
   so and stop, rather than researching a business the agency may not work
   with, which would make the whole approach wrong in its first sentence.
3. **The client is a real, currently trading business** with a live site.

Record all of this before Stage 2. It becomes the report's provenance
section and the email's Article 14 line.

## Stage 2 — Client scope

From the client's own site, not from assumption: what they actually sell,
where they actually work, and which customer buying situations are real for
them. A services page and a locations page usually settle it.

Note the client's own domain — `citation_analysis.py` needs it in Stage 6.

If the client's real geography turns out to be materially different from
what the invocation implied, use the real one and say so in the report.

## Stage 3 — The six-question framework

Write `questions.csv` in the work folder with the exact columns
`audit_id,question_id,category,question_text,frozen_from`, `frozen_from`
blank, `audit_id` set to `<client-slug>-<today, YYYY-MM-DD>`.

**Six questions.** The paid Benchmark uses twelve
(`playbook/agency-product.md` §1.1); this is the condensed half, and the
difference is one of the things held back.

| Category | Count |
|---|---|
| `discovery` | 2 |
| `qualified-discovery` | 1 |
| `buying-intent` | 1 |
| `comparison` | 1 |
| `named-business` | 1 |

`playbook/audit-process.md`'s four wording rules apply unchanged: the
customer's word rather than the industry's word, a named town plus one wider
area and never a postcode, no business name in the discovery,
qualified-discovery or buying-intent questions, and written the way a person
says it out loud. Every question names the geography — Gemini's grounding
has no locale parameter at this tier.

**Two of the six name the client** — the comparison question and the
named-business question. That is deliberate and it is measured separately:
`benchmark_metrics.py` flags them `prompted` and keeps them out of the
headline, because an assistant handed the name will use it. Do not try to
avoid this by writing a comparison question that omits the name; a
comparison question needs it.

Show the six in your own output before running them.

## Stage 4 — Run it

Preflight exactly as `/90qrun` Step 2 does — all six env vars set in the
**same** shell call as the script, `PERPLEXITY_MODEL` bare not
provider-prefixed, models cross-checked against the most recent prior run.
Do not restate those checks here; go and read that file's Step 2, it is the
source of truth for them.

Smoke test first, one query per provider, and apply `/90qrun` Step 4's three
blocking checks (an `errors` value, an empty `sources_cited`, a missing
`model_version`). Delete every row tagged smoke before the full run.

```
python3 tools/trade-run/trade_run.py \
    --questions ~/wardith-runs/agency/<agency>/<client>/questions.csv \
    --client <client-slug> --location <geography> \
    --out ~/wardith-runs/agency/<agency>/<client>/run.csv --cap 90
```

Then gate on completeness with the existing validator, which needs no
change for this:

```
python3 .agents/skills/90qrun/scripts/validate_run.py \
    --csv ~/wardith-runs/agency/<agency>/<client>/run.csv \
    --questions ~/wardith-runs/agency/<agency>/<client>/questions.csv
```

Retry the identical run command **once** if it exits 1 for errored rows
only — `trade_run.py` resumes and retries just those, for pennies. Retry
once, never loop. A structural failure is not something a retry fixes.

## Stage 5 — The peer set

Read the answers and list every business named across them. That list, plus
the client itself, is `census.csv` (columns `business,area`).

**The peer set is who the assistants actually put in front of this client's
customers**, not a researched market. That is the whole point of it here:
it costs no extra research and it is the comparison the agency will find
hardest to argue with. Do not go and build a market census — that is
`/qualify`'s job for a different product.

Include the client itself or Stage 6 stops. Spot-check a sample of answers
for a recurring misspelling of a real name before assuming the counts are
right; if one exists, write a `--variants-file` per
`tools/mention-count/README.md` rather than accepting the undercount.

```
python3 tools/mention-count/mention_count.py \
    --run .../run.csv --census .../census.csv \
    --area <geography> --out .../mention-counts.json
```

## Stage 6 — Measure

Three commands, all deterministic, none of them a judgement:

```
python3 tools/benchmark/benchmark_metrics.py \
    --run .../run.csv --questions .../questions.csv \
    --mention-counts .../mention-counts.json \
    --client "<Client Legal/Trading Name>" --out .../baseline.json

python3 tools/benchmark/citation_analysis.py \
    --run .../run.csv --mention-counts .../mention-counts.json \
    --client "<Client Legal/Trading Name>" --client-domain <client-domain> \
    --out .../citation-analysis.json

python3 tools/site-check/site_check.py --url https://<client-site> \
    --out .../site-check.json
```

`--client` must match the census name exactly.

**`site_check.py` is run in full but reported in one line.** The sample says
whether the assistants can reach and read the site at all; what is missing
from it, and what to do about it, is the paid Benchmark. Reading the whole
thing now costs one command and means the outreach brief knows whether
there is a site problem worth mentioning at all.

**Read `baseline.json`'s `run.providers_with_mixed_model_versions` before
writing anything.** A provider carrying more than one model version cannot
be reported as a single measurement.

## Stage 7 — The strongest two or three findings

Pick two or three. Not five, not one. Each has to pass the test in
`playbook/agency-product.md` §5: **can an SEO professional implement,
investigate, explain or measure something because of this?**

The findings this data usually supports, in rough order of how well they
land:

- **A high-intent absence.** Named on discovery, absent from the questions
  describing the work they actually want. Check the peers were named on
  that question before calling it a gap — a question nobody gets named on
  is a dead question, not a competitive finding. (`/outreach` learned this
  one the hard way; it is the same check.)
- **A single-assistant silence.** Present on one, never named on another.
  Report it only where it is mechanically material — absent from a provider
  entirely, or one provider carrying 70% or more of the total — never as
  boilerplate.
- **A source the competitors are on and the client is not.**
  `citation-analysis.json`'s `competitor_cited_client_absent`. This is
  normally the most actionable single thing in the whole sample, because it
  names a specific page rather than a general direction.
- **Position against the peer set**, using `baseline.json`'s `position`
  block and the peer table.

**Label every statement.** `playbook/agency-product.md` §1.5: **observed**
(it is in the run data or a fetched page), **inferred** (a reading of the
data that is probably right and is not itself measured), **recommended**
(what to do). An inference never inherits an observation's confidence.

**Never invent a number, a cause or a competitor's advantage.** Anything
unknown is `[PLACEHOLDER]` and flagged. The primary visibility claim always
uses the unprompted figures from `baseline.json`, never a raw
answers-total that includes the prompted questions.

**Then check every figure back against the JSON before Stage 8 finishes.**
Not a formality: the first test run of this skill wrote "named the leader in
twenty of twenty" for a comparison that was fifteen of twenty, because the
peer's *campaign* total was reused where its *per-provider unprompted* count
was meant. Both numbers are in `baseline.json`. A competitor comparison in
particular has three plausible denominators — campaign total, unprompted
total, per-provider unprompted — and reaching for the wrong one produces a
sentence that reads fine and is false.

## Stage 8 — The sample report

`sample-report-<date>.md` in the work folder. Agency-facing: this is written
for an SEO professional, so it can be technical, but it is still governed by
`playbook/voice.md` — read it back for the rule of three, staccato drama, em
dashes and machine vocabulary before finishing.

Sections, in this order and no longer than they need to be:

1. **What this is** — a sample of the Benchmark, run on one of their
   clients, from public information, with the end client never contacted.
2. **What was asked** — the six questions, verbatim, with their categories,
   and which two named the client.
3. **How it was run** — three assistants, five runs each, 90 answers, the
   exact model version strings, the date. Say plainly that Copilot and AI
   Overviews were not included and why.
4. **Where the client shows up** — bands with raw counts. The unprompted
   headline, the prompted figure beside it and clearly labelled, the split
   by assistant, and the high-intent subset.
5. **Who gets named instead** — the peer table.
6. **What the answers were built from** — the citation finding.
7. **Two or three findings**, each labelled observed / inferred /
   recommended.
8. **What this sample does not tell you** — honestly, and this section is
   what makes the paid product legible rather than being a sales pitch:
   six questions rather than twelve, no full source map, no site
   investigation beyond whether the assistants can read it at all, no
   implementation prioritisation, and no second run to separate change from
   noise.
9. **Confidence and limits** — including that five runs cannot distinguish
   three from two, and that a single run measures a moment.

**What is held back.** Roughly a third of the paid Benchmark, and
deliberately the third that turns observation into work: the full twelve
questions, the complete source map, the site and entity investigation, the
prioritised action list, and the recurring baseline. The finding is free;
the diagnosis is the product — `playbook/outreach-process.md`, unchanged.

**Never publish this.** `playbook/decisions.md`: never publish a ranked
table of named local businesses. Sending it privately to the agency that
works for the client named in it is a different act and is in scope.

## Stage 9 — Outreach preparation, never a send

Two files, both drafts.

**`outreach-brief-<date>.md`** — for Wardith, not for the agency:

- the agency, its company number and status, and the evidence for the
  client relationship with URLs and access dates;
- the one finding worth leading with, and why that one;
- what the agency plausibly gets out of it, in their terms — they keep the
  client and do the work, Wardith does the research layer;
- the commercial ask: the Benchmark at £495 and the Monthly Review at
  £149 per client per month (`playbook/agency-product.md`), with the
  volume position left open;
- **anything that would make this approach wrong**, stated plainly. A
  relationship that may have ended, a finding the data does not really
  support, an agency that appears to already do this.

**`outreach-prep-<date>.json` and the email draft.** Follow `/outreach`
Stage 5's structure and every rule in it — this skill does not restate them
and does not get its own variant:

- say who you are before what you found (`playbook/voice.md`'s single most
  important rule);
- one recipient per email, never a BCC list;
- the subject names the thing and makes no claim;
- the finding in real numbers, with a real quoted question;
- the Article 14 line naming the actual publisher of the evidence used for
  **this** agency, never a source from a different one;
- the opt-out line, and a note that the signature is appended at send time
  rather than pasted into the draft;
- **no invented case studies, results, statistics or outcomes.**

Two things specific to this skill:

- **Say the end client was not contacted**, in the email, in plain words.
  It is the first thing a competent agency will wonder.
- **The offer is the agency product**, not the £250 audit. `/outreach`'s
  "the Audit is the only thing on offer" rule governs the direct-to-business
  campaigns it was written for; this is a different product line and a
  different buyer.

**Nothing is sent.** No email client, no LinkedIn, no form, no webhook. If
asked to send, stop and say that is out of scope here.

## Stage 10 — Report

One checkpoint, the only one the owner sees:

- **Verdict**: `PASS` (gate cleared, 90/90 clean, findings supported),
  `PASS WITH RETRY` (some rows failed, the retry fixed them),
  `INCOMPLETE` (still short, or the data does not support a finding worth
  sending — which is a legitimate outcome, not a failure to route around),
  or `STOPPED AT GATE` (Stage 1 failed — say which half).
- The six questions, the model versions recorded, the row counts.
- The headline unprompted figure, the prompted figure beside it, the peer
  rank, and the visibility shape.
- The two or three findings, in one line each.
- Every file path.
- The email draft in full, in the response, for review before any send.
- One line: **nothing has been sent, and the end client was not contacted.**

## What this skill does not do

- **Does not contact the end client**, ever, in any form.
- **Does not send or post anything.** Drafts only.
- **Does not run `/qualify`** or build a market census. The peer set here is
  who the answers named, which is a different and cheaper thing.
- **Does not modify** `trade_run.py`, `mention_count.py`, `site_check.py`,
  `validate_run.py`, `benchmark_metrics.py` or `citation_analysis.py`. If
  one genuinely cannot represent what this run needs, that is a real
  blocker — say so rather than working around it.
- **Does not write anything into this repository**, including the question
  file.
- **Does not give away the paid Benchmark.** If a finding needs the full
  twelve questions, the site investigation or a second run to stand up, it
  belongs in the paid product and the sample says so.
