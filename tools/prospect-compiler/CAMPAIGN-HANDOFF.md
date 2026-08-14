# Campaign JSON handoff

*How a trade run's findings become a compiler-ready campaign JSON file. Read
this before writing a campaign JSON, for any sector × market.*

**Written after the Wirral run built its own JSON format instead of targeting
`schema.json`** — the compiler already existed when that run was processed,
and it went unused because nobody had written down what the schema actually
requires. This document exists so that never happens again.

---

## 1. Purpose

Three things do three separate jobs. Do not blur them:

- **`schema.json` defines the machine contract.** It is the only shape a
  campaign JSON file is allowed to take.
- **`build_workbook.py` is deterministic rendering only.** It does not
  research businesses, does not decide who is a prospect, and does not fix
  bad data — it fails loudly on it.
- **Claude and the owner produce the data.** Research, evidence-gathering and
  analytical synthesis are Claude's job; final prospect priority and
  send-readiness are the owner's.

**DO NOT invent an alternative campaign JSON structure.** If the data does not
fit `schema.json`, the data or the process that produced it is wrong, not the
schema. See §8.

**Three separate questions, never conflated** (calibrated against the
completed Chester and Wirral retrospective, 2026-08-14):

- **Opportunity type** (`GAP` / `GROWTH` / `DEFEND` / `REVIEW` / `NO
  OPPORTUNITY`) — *why* a business is worth approaching. Low AI visibility is
  not the only commercially interesting condition — a business with real
  existing visibility can be a stronger prospect than a zero-mention one. See
  §3's opportunity-type subsection.
- **Commercial priority** (`A` / `B` / `C` / `REVIEW`) — how much a business
  is worth pursuing. Visibility count alone does not set this — a `DEFEND`
  business can be Priority A, a zero-visibility `GAP` business can be
  Priority C.
- **Send-readiness** (`ready_to_email`: `YES` / `REVIEW`) — whether *this*
  email is ready to go today: verified contact, correct numbers, a truthful
  angle.

**The Audit is the default entry product for every opportunity type.** `GAP`,
`GROWTH` and `DEFEND` all start with the Audit — the type changes *why*
Wardith approaches a business, never the first thing it sells. "Start with
the audit. If there is genuinely nothing to fix, we will tell you" holds for
all three. What happens after the audit is not fixed either — see §3.

---

## 2. Input checklist

Before writing a single line of campaign JSON, have all of this in hand:

- sector and geography (the run's own scope, as chosen in
  `playbook/outreach-process.md` step 1)
- campaign date and slug
- the question set actually run (`questions-{trade}-{area}.csv`)
- the raw trade-run CSV (`tools/trade-run/`) and its provider/run statistics
  (planned vs. successful queries, from the CSV itself)
- a market census — the real competitive market, built per
  `playbook/outreach-process.md` step 3, **not** a Companies House sweep
- mention counts for every census business against the raw run
- research sources for every factual claim (register, portal, official site)
- Companies House / legal-entity verification, where a business is a
  candidate for `outreach[]`
- competitive-gap analysis per `playbook/outreach-process.md` step 4

**If something on this list is missing, mark it and stop rather than
fabricate it.** `CLAUDE.md`'s rule is absolute: never invent a business fact.
A business with a gap in its evidence stays in `market[]` as `REVIEW`, or
moves to `excluded[]`, rather than being written into `outreach[]` with a
guessed field.

**Geography is decided by evidence against the campaign's boundary rule, not
by search result.** A business belongs in the market census only where
evidence shows it genuinely operates in the defined campaign geography under
that campaign's agreed boundary rule — appearing in search results, or a
generic claim to serve the area, is not sufficient on its own. This is a
general rule for every campaign; the boundary rule itself is set per
campaign, not defined here. Where the geographic fit is genuinely unclear,
record it as `REVIEW` (`market_entry.disposition`) with the ambiguity stated
in `notes` — do not resolve the ambiguity by silently including or excluding
the business.

---

## 3. Field-by-field schema mapping

Every field in the current `tools/prospect-compiler/schema.json`, and who
populates it:

- **AUTO** — mechanically derivable from run data, no judgement involved
- **RESEARCH** — requires external factual verification
- **CLAUDE** — analytical synthesis or judgement, grounded in evidence already gathered
- **HUMAN** — the owner's explicit approval

### Market position and opportunity type

Every business with a real mention count sits at some **relative market
position** — Leader / Upper-mid / Mid / Low / Absent, judged against that
market's own distribution, never a fixed count (89 successful answers means
something different from 900). Consider total appearances, share relative to
the leaders, provider split, question/intent spread where useful, and
consistency across OpenAI, Gemini and Perplexity — a business strong on one
provider and absent from another is a different story from one evenly weak
across all three. **No proprietary score, visibility percentage or invented
precision** — this is a qualitative call, the same as `disposition` always
has been.

From that position, classify `opportunity_type`:

- **`GAP`** — credible, materially underrepresented relative to genuine
  competitors. Zero mentions is the clearest case, but low counts alone are
  not sufficient — the gap has to be real, not just small.
- **`GROWTH`** — meaningful existing visibility that sits materially below
  the genuine leaders, is inconsistent between models, absent from one
  provider despite presence elsewhere, or concentrated on a narrow set of
  questions. **Never describe a `GROWTH` business as invisible.**
- **`DEFEND`** — already a strong or leading position. The opportunity is
  understanding what supports it, where it's weaker, how it differs by
  model, and whether it holds over time. **Do not manufacture a problem a
  strongly-visible business doesn't have.**
- **`REVIEW`** / **`NO OPPORTUNITY`** — market fit unclear, legal/trading
  status unresolved, geography ambiguous, the gap explained by being
  new/specialist/out-of-market, local decision-making unrealistic, or the
  only available angle would be misleading.

**Being strongly visible is no longer, by itself, grounds for `EXCLUDED`.**
A business named as often as its competitors is very often a `DEFEND`
candidate, not a dead end — see `sample-campaign.json`'s Northgate Pipeworks
for the shape. `excluded_entry.reason`'s `ALREADY STRONGLY VISIBLE` value
stays in the schema (removing it would break every already-completed
campaign that used it) but should now be the exception, paired with another
real disqualifying factor, not the default response to high visibility.

**Do not force every census business into an opportunity type.** Most of a
census will have too little individual research behind it (no legal check,
no credibility read) to classify responsibly — leave `opportunity_type` off
entirely rather than guess. It is optional on both `market_entry` and
`outreach_entry` for exactly this reason.

### Post-audit routing

`opportunity_type` describes why Wardith approaches a business; it does not
pick the service. Every type starts at the Audit (£250, `playbook/services.md`).
What follows the audit is a separate, later decision, made from what the
audit actually finds, not predicted here:

- **No action** — the audit found nothing worth changing. A valid, statable
  outcome for any type, including `DEFEND`.
- **Foundation** (£800 one-off) — fixed-scope remediation work.
- **An ongoing monthly plan** — Maintain, Grow or Lead (`playbook/services.md`);
  there is no product literally called "Retainer". `[PLACEHOLDER: none of
  these three has been delivered to a real client yet — playbook/README.md,
  "no monthly-plan record template exists."]`
- **Foundation, then a monthly plan.**

**Foundation does not have to precede a monthly plan.** A `DEFEND` client with
little to structurally fix may go straight from Audit to an ongoing plan. If a
prospect explicitly asks to start directly on ongoing work, Wardith may agree
to skip the Audit by agreement — the exception, not the default sales path.

### `run` (required: `sector`, `geography`, `campaign_slug`, `date`, `questions`, `providers`)

| Field | Required | Source |
|---|---|---|
| `sector` | yes | AUTO — the trade named when the run was set up |
| `geography` | yes | AUTO to populate, copied from the run's own scope — but see §2: if the market's boundary was ambiguous, that was a HUMAN call made *before* Stage A, not something to resolve here |
| `campaign_slug` | yes | AUTO — matches the `--client` value used in `trade_run.py` |
| `date` | yes | AUTO — the date the campaign JSON is compiled |
| `questions` | yes | AUTO — the `question_text` values from the question CSV, in order |
| `providers` | yes | AUTO — a list of `{provider, model}` objects. `provider` is one of the schema's fixed enum (`openai`, `gemini`, `perplexity`, `copilot`, `ai-overviews`) — a trade run currently produces the first three. `model` is the exact `model_version` string the raw CSV actually recorded, per `playbook/models-and-schemas.md` ("record the exact model version string on every single run") — not the nominal `OPENAI_MODEL` env var, the string the provider actually returned |
| `expected_responses` | no | AUTO — the planned query count (e.g. 90) |
| `successful_responses` | no | AUTO — count of raw CSV rows with an empty `errors` column |
| `raw_data_path` | no | AUTO — the `--out` path the run was written to |
| `methodology_notes` | no | CLAUDE — anything methodological worth flagging: errored/retried rows, a geography-ambiguity note, anything that would make a later reader distrust a naive comparison |

### `market[]` — `market_entry` (required: `business`, `area`, `disposition`, `total_ai_appearances`)

| Field | Required | Source |
|---|---|---|
| `business` | yes | RESEARCH — from the market census |
| `area` | yes | RESEARCH — the specific branch/trading location, from the census |
| `disposition` | yes | CLAUDE — `OUTREACH` / `EXCLUDED` / `REVIEW`, against the five-point check in `playbook/outreach-process.md` step 4. **The schema has no separate approval field for this** — see §5 for exactly which fields carry the formal human gate |
| `opportunity_type` | no | CLAUDE — `GAP` / `GROWTH` / `DEFEND` / `REVIEW` / `NO OPPORTUNITY`, per the subsection above. Separate from `disposition`: a business can be `EXCLUDED` from this campaign's outreach and still carry a `DEFEND` opportunity type for later |
| `total_ai_appearances` | yes | AUTO — once mention counts exist for this run |
| `openai_appearances` / `gemini_appearances` / `perplexity_appearances` | no | AUTO |
| `notes` | no | CLAUDE — legal-entity ambiguity, geography ambiguity, anything a later reader needs |

### `outreach[]` — `outreach_entry` (required: `priority`, `business`, `area`, `total_ai_appearances`, `strongest_competitor`, `competitor_appearances`, `competitive_gap_finding`, `why_prospect`, `legal_entity`, `company_number`, `company_status`, `ready_to_email`, `evidence_source_ids`)

| Field | Required | Source |
|---|---|---|
| `priority` | yes | **HUMAN** — Claude recommends `A` / `B` / `C` / `REVIEW`, the owner approves. Commercial priority, not a visibility-size ranking — weighs evidence quality, market relevance, credibility, competitive position, commercial value and decision-maker accessibility. A `DEFEND` business can be Priority A; a zero-visibility `GAP` business can be Priority C. The gate — see §5 |
| `opportunity_type` | no | CLAUDE — carried from the `market_entry`, or set here directly if this business wasn't individually classified earlier. Distinct from `priority` and from `ready_to_email` — see §1 |
| `business` | yes | RESEARCH — carried from the market census entry |
| `area` | yes | RESEARCH — carried from the market census entry |
| `website` | no | RESEARCH |
| `total_ai_appearances` | yes | AUTO |
| `openai_appearances` / `gemini_appearances` / `perplexity_appearances` | no | AUTO |
| `strongest_competitor` | yes | CLAUDE — the strongest genuine direct competitor by appearance count in this market |
| `competitor_appearances` | yes | AUTO — once `strongest_competitor` is identified, its count is a lookup |
| `competitive_gap_finding` | yes | CLAUDE — one factual sentence stating the counts, per the letter templates in `playbook/outreach-process.md` |
| `why_prospect` | yes | CLAUDE — the case for this business against `playbook/outreach-process.md`'s definition of a strong prospect |
| `legal_entity` | yes | RESEARCH — Companies House. **No confirmed active Ltd/LLP match, no entry in `outreach[]`** — the business stays `REVIEW` in `market[]` or moves to `excluded[]` (`NO RELIABLE LEGAL MATCH`) instead. This is the PECR rule in `CLAUDE.md`, enforced at the schema boundary, not worked around with a placeholder |
| `company_number` | yes | RESEARCH — Companies House |
| `company_status` | yes | RESEARCH — Companies House |
| `contact_person` | no | RESEARCH — `[PLACEHOLDER]` is permitted here (see `sample-campaign.json`) precisely because this field is optional; never invent a name |
| `role` | no | RESEARCH — same as above |
| `contact_email` | no | RESEARCH — same as above |
| `ready_to_email` | yes | **HUMAN** — `YES` / `REVIEW`. The other half of the gate — see §5 |
| `evidence_source_ids` | yes | CLAUDE — at least one `source_id` from `sources[]`, referencing the entries that support this record |

### `excluded[]` — `excluded_entry` (required: `business`, `area`, `reason`)

| Field | Required | Source |
|---|---|---|
| `business` | yes | RESEARCH — carried from the market census |
| `area` | yes | RESEARCH — carried from the market census |
| `reason` | yes | CLAUDE — one of the fixed enum values (`SOLE TRADER`, `ORDINARY PARTNERSHIP`, `CHAIN / NO LOCAL DECISION-MAKER`, `DUPLICATE BRAND`, `NOT GENUINELY IN MARKET`, `CLOSED / DORMANT`, `ALREADY STRONGLY VISIBLE`, `NO RELIABLE LEGAL MATCH`, `OTHER / REVIEW`), chosen from the research already gathered — never invented to fill a gap |
| `notes` | no | CLAUDE |

### `sources[]` — `source_entry` (required: `source_id`, `business`, `publisher`, `fact_supported`, `url`, `access_date` — every field is required, there are no optional fields on a source)

| Field | Required | Source |
|---|---|---|
| `source_id` | yes | CLAUDE — assigned sequentially (`S001`, `S002`, …) as sources are used, matching the pattern `^S[0-9]{3,}$` |
| `business` | yes | CLAUDE — which business this source supports |
| `publisher` | yes | RESEARCH — e.g. `Companies House`, `Rightmove`, or, for a fact rooted in the raw run itself, `{provider} run answer, {question_id}, run {run_no}` (see `sample-campaign.json` `S002`) |
| `fact_supported` | yes | CLAUDE — one line stating exactly what this source proves |
| `url` | yes | RESEARCH — see §4 for what to put here when the fact comes from a trade-run answer rather than a published page |
| `access_date` | yes | AUTO/RESEARCH — the date the page was checked, or the run's own date for a raw-run-derived fact |

---

## 4. Evidence rules

- **`outreach[]` formally links its supporting sources through
  `evidence_source_ids`.** The field is required and must be non-empty; it
  must reference IDs that exist in `sources[]` — `build_workbook.py` checks
  this and fails on an unknown ID.
- **`market[]` and `excluded[]` have no equivalent field in `schema.json`** —
  do not add `evidence_source_ids` or any other invented linking field to
  either. The research behind a `disposition` or `reason` call must still be
  evidence-backed and kept in the source/research record (the `sources[]`
  register and/or the working notes for the run), but the schema neither
  requires nor permits a per-entry link for these two arrays. `schema.json`
  remains the machine contract — a field it doesn't define does not get added
  to satisfy this rule. `opportunity_type` follows the identical rule — it
  rests on the same mention-count and competitor evidence that already backs
  `disposition` and `competitive_gap_finding`; it does not get its own
  linking field either.
- **`sources[].url` must point somewhere real.** For a fact from an
  authoritative register or directory, the URL is that page. For a fact whose
  only evidence is that a business was named in a trade-run answer, there is
  no per-answer URL — use the raw run's own file path
  (`run.raw_data_path`), following the pattern already in
  `sample/sample-campaign.json`'s `S002`. If the assistant's own answer cited
  an external source for that mention (the raw CSV's `sources_cited` column),
  prefer that URL instead — it is stronger evidence.
- **No invented Companies House facts.** A `legal_entity` / `company_number` /
  `company_status` triple is either a confirmed lookup or the business does
  not go in `outreach[]`. See the `legal_entity` row in §3.
- **No invented contact names or emails.** `contact_person`, `role` and
  `contact_email` are optional precisely so `[PLACEHOLDER]` can stand in
  honestly instead of a guess — never fill these with anything unverified.
- **Placeholders belong only where the schema makes a field optional.** A
  required field with incomplete research is not a placeholder problem — it
  means the business is not ready for `outreach[]` yet. Leave it in
  `market[]` as `REVIEW`, or move it to `excluded[]`, rather than inventing a
  value to satisfy the schema's `required` list.

---

## 5. Priority gate

**`outreach_entry.priority` (`A`/`B`/`C`/`REVIEW`) and
`outreach_entry.ready_to_email` (`YES`/`REVIEW`) are the two fields the owner
must approve before a campaign JSON is treated as outreach-ready.** Claude
may — should — propose values for both, backed by the evidence already
gathered, but the file is not final until the owner has reviewed and
confirmed them.

**`priority` is not `opportunity_type`, and it is not a visibility ranking.**
A business's opportunity type (§3) says why it's worth approaching; priority
says how much, weighing evidence quality, market relevance, credibility,
competitive position, commercial value and decision-maker accessibility. A
`DEFEND` business with a strong ongoing-monitoring story can outrank a `GAP`
business with a thin one — raw appearance count does not decide priority by
itself.

**One accuracy note, since the schema is the source of truth here rather than
the pipeline audit's phrasing:** `schema.json` has no separate `approved`
field, and `build_workbook.py` does not check whether a human has signed off
— it only checks that `priority` and `ready_to_email` hold a valid enum
value. The approval gate is a **process step**, enforced by not running the
compiler in anger (or not sending anything from the resulting workbook) until
the owner has reviewed those two fields per business — not something the JSON
file itself can prove happened. Treat a campaign JSON with Claude-proposed but
not-yet-reviewed `priority`/`ready_to_email` values as a draft, even though it
will pass validation.

---

## 6. End-of-analysis procedure

1. Complete research: market census, mention counts, legal verification,
   competitive-gap analysis (§2).
2. Determine AI market position for businesses with enough evidence to
   support it, and classify `opportunity_type` (`GAP`/`GROWTH`/`DEFEND`/
   `REVIEW`/`NO OPPORTUNITY`) — §3. Not every census business gets one.
3. Produce proposed classifications: `disposition` for every market entry,
   `reason` for every exclusion, `priority` and `ready_to_email` for every
   outreach candidate.
4. Present the HUMAN fields — `priority` and `ready_to_email` — for the
   owner's approval before treating anything as final.
5. Populate the final JSON against `schema.json` exactly, using §3 as the
   field-by-field checklist.
6. Save the campaign JSON in the run's canonical location. There is no
   formal folder rule for prospecting runs yet (only client audits have one,
   in `playbook/records-and-data.md`) — until one exists, follow the pattern
   the Wirral run already used: `~/wardith-runs/<sector>-<geography>/`
   holding the campaign JSON and workbook, next to the raw CSV at
   `~/wardith-runs/<sector>-<geography>.csv`. Never inside this repository.
7. Run the existing Prospect Compiler (§7).
8. **If validation fails, fix the data or this handoff, not the tooling.**
   See §8.
9. Contact verification and outreach sending happen after this procedure,
   not as part of it — see `playbook/outreach-process.md`. Every opportunity
   type routes to the Audit first (§1); what follows the audit is decided
   from what the audit finds, not predicted at qualification time.

---

## 7. Validation command

The one command, exactly as documented in `tools/prospect-compiler/README.md`:

```
python3 build_workbook.py --input campaign.json --output workbook.xlsx
```

`build_workbook.py`'s own `validate()` function is the final machine gate —
it checks every required field, every enum value, and that every
`evidence_source_ids` entry resolves to a real source, and it fails with a
specific error rather than guessing. There is no separate validation
framework to reach for; a failure here is read and fixed, not routed around.

---

## 8. Anti-detour rule

**If the JSON does not satisfy `schema.json`, do not:**

- create a new schema;
- create a bespoke renderer (a `build_xlsx.py`-shaped script);
- create a parallel campaign JSON format;
- weaken or skip `build_workbook.py`'s validation to make the data pass.

**Correct the research-to-schema handoff instead** — go back to §2 or §3, work
out which field the data doesn't yet support, and fix the research or the
JSON. This is the exact mistake the Wirral run made: the compiler already
existed, and the run built `crossref.py` → `build_campaign.py` →
`build_xlsx.py` as a parallel pipeline instead of targeting it. Those three
files are kept as historical record, not as a pattern to repeat.

---

## 9. Using this document in a fresh session

Read this file together with `tools/prospect-compiler/schema.json` and
`playbook/outreach-process.md`. Nothing else is required to know what output
a prospecting run is expected to produce: a single campaign JSON file
matching `schema.json`, built by working through §2 → §3 → §6, gated by §5,
rendered by §7.
