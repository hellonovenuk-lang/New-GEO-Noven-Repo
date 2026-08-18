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

- **Opportunity type** (`GAP` / `GROWTH` / `DEFEND` / `NO OPPORTUNITY`) —
  *why* a business is worth approaching. `REVIEW` is not a fifth value here —
  it belongs to `disposition` and `priority`, which already carry it; an
  unclassifiable business simply has no `opportunity_type` set, or a
  `disposition`/`priority` of `REVIEW`. Low AI visibility is not the only
  commercially interesting condition — a business with real existing
  visibility can be a stronger prospect than a zero-mention one. See §3's
  opportunity-type subsection.
- **Commercial priority** (`A` / `B` / `C` / `REVIEW`) — how much a business
  is worth pursuing. Visibility count alone does not set this — a `DEFEND`
  business can be Priority A, a zero-visibility `GAP` business can be
  Priority C.
- **Decision-maker accessibility** (`DIRECT` / `IDENTIFIABLE` / `GATEKEPT` /
  `CORPORATE` / `REVIEW`) — the likely route to the person who can actually
  say yes. A research finding, recorded per prospect, distinct from
  commercial opportunity — see the subsection below. It is one input to
  priority, never a rule that sets or overrides it by itself: a strong `GAP`
  or `DEFEND` business stays high priority even when `GATEKEPT`.
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
- decision-maker / contact-route research for every `outreach[]` candidate,
  sufficient to place it in one of the accessibility categories below —
  `REVIEW` is an acceptable outcome of this research, an untouched field is
  not

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
- **`NO OPPORTUNITY`** — market fit unclear, legal/trading status
  unresolved, geography ambiguous, the gap explained by being
  new/specialist/out-of-market, local decision-making unrealistic, or the
  only available angle would be misleading. **This is not `REVIEW`** —
  `REVIEW` is a state of `disposition` and `priority` (unresolved, needs a
  human look), not a kind of opportunity. A business can be `NO OPPORTUNITY`
  and cleanly settled (there is definitely nothing to sell it) or it can
  simply have no `opportunity_type` at all, with the ambiguity carried by
  `disposition: REVIEW` instead.

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

### Decision-maker accessibility

Commercial attractiveness alone doesn't say how easy a business is to
actually reach. Some strong prospects are heavily gatekept behind
reception/admin; some owner-led businesses with a thinner opportunity are
much easier to sell to. Every business that reaches `outreach[]` gets an
`accessibility` classification recording which situation it's in:

- **`DIRECT`** — a named decision-maker (owner, director, or the plausible
  operational/marketing lead) with an obvious direct professional contact
  route: a personal business email, or a named contact the site itself
  routes enquiries to.
- **`IDENTIFIABLE`** — the decision-maker is confidently identified (a
  Companies House director/PSC record, a LinkedIn profile that matches on
  name, role and location, a named principal on the business's own site) but
  the only working contact route is a generic company channel — an
  `info@`/`enquiries@` inbox, a contact form with no named recipient.
- **`GATEKEPT`** — the business is a genuine prospect, but contact appears
  filtered through reception/admin with no clear route to a named
  decision-maker at all.
- **`CORPORATE`** — the real purchasing or marketing decision sits above the
  local business or branch, or inside a larger group (a franchise head
  office, a national chain's marketing team) — the local contact, even if
  findable, isn't who decides.
- **`REVIEW`** — the research is genuinely ambiguous: a candidate LinkedIn
  match that isn't confident, conflicting signals about who's actively
  running the business, or not enough public information to place it in any
  of the four categories above. **This is the required outcome when a match
  can't be made confidently — never guess to force a cleaner-looking
  category.**

**What to look for, all from public sources, none of it invented:**

- company directors, owners, or founders (Companies House officers/PSC
  pages, the business's own "About" or team page);
- who is the likely operational or marketing decision-maker, where that
  differs from the registered director (e.g. a practice manager named on
  the site);
- whether that person appears **actively associated with the business now**
  — a director record alone doesn't confirm this; check the business's own
  site or a recent, dated public mention;
- a LinkedIn profile, **only where confidently matched** on name, current
  role, and business/location together — never a same-name profile that
  doesn't corroborate on role or place;
- whether a direct, named business email is publicly available, versus only
  a generic/reception/admin address;
- any other legitimate public business contact route that materially
  improves the odds of reaching this person (a named contact on a trade
  register profile, a direct phone line attributed to them, and similar) —
  worth recording in `accessibility_notes`, not a reason to invent a new
  schema field for every possible route.

**Do not invent or infer personal contact details.** A phone number,
personal email, or home address that isn't published by the business itself
or a trusted register never goes in `accessibility_notes`,
`decision_maker_linkedin`, or anywhere else in the record — the same rule
`legal_entity`/`contact_email` already follow, extended to this field. An
inferred email pattern (`firstname.lastname@` guessed from a naming
convention seen elsewhere) is exactly this kind of invention and is
forbidden here too.

**Decision-maker accessibility informs priority; it does not decide it.** A
`GATEKEPT` business with a strong `GAP`/`DEFEND` story and real commercial
weight can and should stay Priority A — the workbook makes the access
problem visible (see the OUTREACH sheet's colour-filled accessibility
column) precisely so a different route (LinkedIn, a trade-register listing,
a second attempt via a different page) can be found later, not so the
business gets silently deprioritised.

**`decision_maker_linkedin` is a research field, not an outreach channel.**
`playbook/decisions.md` still holds "LinkedIn outreach is later, not now" —
that decision is about *sending*, unchanged by this. Recording a confidently
matched profile here is what makes a future, separately-decided LinkedIn
approach possible; it is not itself a green light to use it.

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

### 3a. Auditable scoring (candidate pool, service scope, question relevance, ranking)

**Added 2026-08-16, generalized from the approved Kitchen and Bathroom Design
& Installation, Wirral v2.1 regression test.** This subsection adds a
documented, formula-driven, auditable *why* behind `opportunity_type` and
`priority`'s proposed values, computed by `scoring_engine.py`, never
hand-typed. **These fields supersede the "no proprietary score, visibility
percentage or invented precision" line in the "Market position and
opportunity type" subsection above for any business that opts in** — that
line's caution was well-founded for a hand-eyeballed score; it does not
apply to a fully documented, mechanically reproduced one.

**Schema-optional vs. process-mandatory — as of 2026-08-17, these are two
different questions, deliberately kept apart.** At the `schema.json` level,
every field in this subsection remains additive and optional, exactly as
shipped 2026-08-16 — that is what keeps a pre-2026-08-17 campaign JSON file
loadable and renderable forever, and it is not changing. Separately, as a
*process* decision recorded in `.claude/skills/qualify/SKILL.md`, every
newly-invoked `/qualify` run is now required to use this scoring layer —
there is no qualitative-only production path for a new campaign. The
distinction lives in the tooling, not the schema: `build_workbook.py`'s
default (no flag) validation stays exactly as permissive as before, so a
historical file still renders; a new `--require-scored` flag adds the
stricter, mandatory-for-new-runs checks on top, including the candidate
cohort below. A business that doesn't set `service_scope` in an *old*
campaign is still governed by Section 3 alone, exactly as before — the two
philosophies still coexist per business within a single historical file.

**The candidate cohort — making "no cohort member silently disappears"
machine-verifiable.** `run.cohort_inclusion_min_appearances` states, as
data, the mechanical floor of this campaign's inclusion rule (any finer
qualitative nuance stays in `methodology_notes`). `run.scoring_cohort` is
the complete, explicit list of every business selected for canonical
qualification, each an entry with `business` and `status` —
`SCORED` (has `service_scope` set and appears in the scored pool),
`EXCLUDED` (with a `reason`), or `INCOMPLETE` (with `missing_evidence`
stating exactly what's needed). `--require-scored` cross-checks both
mechanically: every `market[]`/`outreach[]` business meeting the stated
floor must have a `scoring_cohort` entry, and every entry marked `SCORED`
must actually have `service_scope` set. This is the fix for a real failure
mode: a business with a high appearance count (found late, or that looked
harder to research than the others) staying an ordinary, unflagged
`market[]` record while every other business in its own tier got the full
scoring pass — the gap was invisible before because nothing forced it to be
named.

**Narrative generation — added 2026-08-17, mandatory, not an optional
helper.** `competitive_gap_finding` and `why_prospect` on every scored
`outreach[]` entry are generated deterministically by
`scoring_engine.py`'s `generate_competitive_gap_finding()`/
`generate_why_prospect()`, automatically, as the last step of `score_pool()`
— after `opportunity_type`, `nearest_competitor`, `group_top_visibility_rate`
and every rank are already final. This exists because a real campaign
(Kitchen and Bathroom Design & Installation, Wirral) shipped a specialist's
`competitive_gap_finding` stating "13 of the 90 raw answers" when that
business's real relevance-aware denominator was 60, and a `why_prospect`
that was a verbatim copy of `business_type_notes` — neither defect was
mechanically possible to catch before this existed, because nothing
connected the prose to the structured values it was supposed to describe.

- **The primary visibility claim always uses `relevant_appearances`/
  `relevant_opportunities`, never the raw campaign total, unless the two
  genuinely coincide** (a business relevant to every campaign question) —
  and even then the text says so explicitly ("every one of this campaign's
  questions was relevant to this business"), never silently reusing
  ambiguous "N of 90" language indistinguishable from the bug. Per-question,
  competitor, and provider-split figures use clearly different phrasing
  precisely so they are never confused with the primary claim (see the
  contradiction-detection rule below).
- **Provider split is mentioned only where mechanically material** — absent
  from a provider entirely, or one provider carrying ≥70% of the total —
  not appended to every finding as boilerplate.
- **`why_prospect` is branched by `opportunity_type`** (DEFEND/GROWTH/GAP/
  REVIEW) and states the actual commercial case; `business_type_notes` may
  be cited as one further, clearly separate clause for context, never as
  the entire field.
- **Regeneration is forced by a signature mismatch, not skipped because the
  field is already non-empty.** `narrative_generated_from` fingerprints the
  structured inputs a narrative was generated from; `score_pool()` recomputes
  and compares it on every run and only regenerates when it no longer
  matches. This is what makes a corrected mention count (or any other
  re-score) automatically update the narrative — a stale sentence can never
  survive purely because nobody remembered to rewrite it by hand.
- **A signature match means "already current," not "must be exactly the
  generated text."** A human/Claude may refine the generated baseline
  afterward with real, specific evidence — a named competitor's actual
  differentiator, a detail surfaced during research — and that refinement
  survives an unrelated re-score untouched, since the signature doesn't
  change. What it does not survive is a contradiction: `build_workbook.py`'s
  `detect_narrative_contradictions()` independently checks the *text* of
  both fields (not just whether they were regenerated) for exactly two
  mechanical problems — the primary claim's numbers not matching
  `relevant_appearances`/`relevant_opportunities`, or `why_prospect` equal
  to `business_type_notes` — regardless of who wrote the words or when.
  `--require-scored` rejects both; the default render flags them as QC
  warnings instead, so a historical file stays readable while still being
  honestly labelled.
- **Structured fields are the source of truth for any downstream numeric
  claim, prose is for human-readable drafting only.** Any consumer of a
  campaign JSON — `/outreach` included — should prefer
  `relevant_appearances`/`relevant_opportunities`/`visibility_rate`/
  `opportunity_type` etc. directly over parsing a sentence out of
  `competitive_gap_finding`/`why_prospect` for anything that needs to be
  numerically reliable, precisely because the prose can (rarely, and now
  detectably) drift from the numbers it describes.

**Two scripts, two jobs, same separation of concerns Section 1 already
establishes for `build_workbook.py`:**

- **`scoring_engine.py` is deterministic computation only.** Given the 9
  evidence-backed VALUE fields (below) plus `service_scope` and the
  campaign's `run.service_scopes[]` / `run.question_relevance[]`
  definitions, it mechanically fills in every DERIVED field. It does not
  research businesses and does not decide the VALUE fields — Claude does,
  from evidence, before running it.
- **`build_workbook.py` renders whatever `scoring_engine.py` computed** as
  live Excel formulas with genuine cached values (Section 7 below covers the
  render/validate command) — it does not recompute anything itself.

**Candidate-pool inclusion — apply one documented, consistent threshold to
everyone.** Before scoring anyone, state the campaign's inclusion rule (e.g.
"every census business with total_ai_appearances >= 5, plus every business
the owner named explicitly") and apply the SAME research depth to every
business that meets it — never promote a business into the scored pool
merely because it happened to get researched first or was easy to verify. A
business that meets the threshold but whose research is still incomplete
stays in `market[]` at `disposition: REVIEW` (or in `outreach[]` at
`priority: REVIEW` / `ready_to_email: REVIEW` if it progressed that far) —
distinguish "not resolved yet" from "commercially rejected" and never
present the researched subset as if it were the whole ranked market.

**Service-scope classification** (`service_scope`, `business_structure`,
`business_type_notes`) — RESEARCH/CLAUDE, from evidence, never inferred from
the business name alone. `service_scope` is a short campaign-defined label
(e.g. `kitchen_only` / `bathroom_only` / `combined` for a kitchen-and-bathroom
campaign — a different vocabulary entirely for a different sector) declared
once in `run.service_scopes[]` with its `applicable_services` (which of the
campaign's real-world services it genuinely offers — this is what
question-relevance weighting keys off, not the label string). `structure`
records ownership shape at the service-scope level where it's uniform
(`INDEPENDENT_LOCAL` / `LOCALLY_OWNED_FRANCHISE` / `CENTRALLY_CONTROLLED_CHAIN`)
or per-business via `business_structure` where it varies within a scope. A
business whose scope isn't yet resolved should not set `service_scope` at
all rather than guessing — it stays unscored (Section 3's qualitative path
still applies to it).

**Question-relevance classification** (`run.question_relevance[]`) —
CLAUDE, from ordinary customer meaning, one entry per `question_id`,
required and documented before any business is scored:

- `SERVICE_ONLY` (+ `service`) — the question only makes sense answered by a
  business offering that one named service. Full relevance only to
  businesses whose `applicable_services` includes that service.
- `EXPLICITLY_COMBINED` — the question's own wording excludes single-service
  businesses (e.g. "not just one trade"). Full relevance only to a business
  whose `applicable_services` covers more than one service.
- `SINGLE_SERVICE_INCLUSIVE` — the question names multiple services but,
  read as an ordinary customer would, doesn't require any one business to
  offer all of them (e.g. "best kitchen and bathroom fitters" reads as "who's
  good at kitchen fitting, and who's good at bathroom fitting"). Full
  relevance to every business with at least one real applicable service.
  Corroborate this reading empirically where possible — if a single-service
  specialist genuinely got named on this question in the real run answers,
  that is evidence for an inclusive reading, not just a semantic guess.
- `AMBIGUOUS` (+ required `weight`, 0–1) — neither of the above cleanly
  applies. `weight: 0` excludes the question from relevant-question scoring
  entirely; a documented fraction applies a partial weight uniformly to
  every business with a real applicable service. This field must never be
  omitted for an `AMBIGUOUS` question — an omitted weight silently
  defaulting to full relevance is exactly what this rule exists to prevent.

A specialist is never penalized for absence from a question outside its
verified scope — that question is simply excluded from its denominator, not
counted as a miss.

**The 14 scored fields** (all optional, all on both `market_entry` and
`outreach_entry` — see `schema.json`'s `scoring_fields` definition for the
authoritative shape/range of every field named below):

| Field | Nature | Who/what sets it |
|---|---|---|
| `commercial_fit` (0–5) | VALUE | CLAUDE — ownership/structure fit for a marketing customer, independent of trade |
| `service_relevance` (0–5) | VALUE | CLAUDE — how closely the actual offer matches this campaign's sector |
| `visibility_score` (0–5) | DERIVED | scoring_engine.py — banded from `visibility_rate` |
| `gap_strength` (0–5) | DERIVED | scoring_engine.py — `CLAMP(business_credibility - visibility_score + 3, 0, 5)` |
| `business_credibility` (0–5) | VALUE | CLAUDE, from RESEARCH — verifiable evidence of genuine, active, established trading |
| `ability_to_buy` (0–5) | VALUE | CLAUDE — scale proxy only (sites/premises/marketing signals), never presented as a financial fact |
| `decision_maker_identified` (0–5) | VALUE | CLAUDE, from RESEARCH — existence/identification of a named owner/director |
| `direct_dm_route` (0–5) | VALUE | CLAUDE, from RESEARCH — the 6-tier scale below |
| `contact_route_quality` (0–5) | VALUE | CLAUDE, from RESEARCH — mechanism quality, independent of who it reaches |
| `contact_identity_confidence` (0–5) | VALUE | CLAUDE, from RESEARCH — confidence in WHO the route reaches |
| `overall_evidence_confidence` (0–5) | DERIVED | scoring_engine.py — `MIN(business_credibility, decision_maker_identified, contact_identity_confidence, research_completeness)` |
| `research_completeness` (0–5) | VALUE | CLAUDE — how many material fields are actually resolved with direct evidence |
| `final_score` (0–100) | DERIVED | scoring_engine.py — weighted sum of 9 components (see below), never a visibility-size ranking |
| `overall_rank` / `outreach_rank` | DERIVED | scoring_engine.py — see "Ranking" below |

`final_score` weights: `commercial_fit`×3, `service_relevance`×2,
`visibility_score`×2, `gap_strength`×4, `business_credibility`×3,
`ability_to_buy`×2, `decision_maker_identified`×2, `direct_dm_route`×3,
`contact_route_quality`×1 (max raw points 110) →
`ROUND(raw_points / 110 * 100, 1)`.

**Decision-maker accessibility — the 6-tier `direct_dm_route` scale, used
verbatim, and materially affecting rank via `final_score` and `priority`,
not just recorded in notes:**

`5` confirmed named owner/director, direct route · `4` confirmed named
owner/director, generic business route · `3` probable contact, identity
supported but not confirmed · `2` generic business inbox only · `1` contact
form or telephone only · `0` no usable route. `accessibility_grade`
(`CONFIRMED_DIRECT` / `CONFIRMED_GENERIC_ROUTE` / `PROBABLE_UNCONFIRMED` /
`GENERIC_INBOX_ONLY` / `CONTACT_FORM_OR_PHONE_ONLY` / `NO_USABLE_ROUTE`) is
the same tier as a machine-readable label, derived automatically from
`direct_dm_route` — never set independently of it. **A generic inbox
(`2`/`GENERIC_INBOX_ONLY`) is never treated as equivalent to a direct route
(`5`) just because an email address technically exists** — this is the
specific flaw the v2.1 test found and fixed: `ready_to_email` cannot reach
`YES` on a generic-inbox-only, unconfirmed-identity record any more, however
plausible the commercial case.

**Structured confidence labels**, distinct from `direct_dm_route`'s route
quality — `identity_confidence` (`CONFIRMED` / `PROBABLE` / `POSSIBLE` /
`UNKNOWN`) answers *who* the contact reaches, kept separate from
`business_verified`/`contact_route_verified`/`named_decision_maker_verified`/
`research_complete`/`eligible_for_outreach` (all derived, all distinct
booleans-as-enums — see `scoring_engine.py`'s gate constants for the exact
threshold each one uses). **An inferred identity is never presented as
`CONFIRMED`** — `contact_identity_confidence` must independently be ≥4 for
the `CONFIRMED` label to appear; a same-name coincidence or an unopened
LinkedIn search result stays `PROBABLE` or `POSSIBLE`.

**`ready_to_email` gate** (on `outreach_entry` only) — YES only if ALL of:
`eligible_for_outreach=YES` (itself `business_verified=YES` AND
`contact_route_verified=YES` AND `commercial_fit>=2` AND
`service_relevance>=2` — this is what keeps a centrally-controlled chain out,
via the `commercial_fit` gate, without a separate hand-rule) AND
`decision_maker_identified>=3` AND `contact_identity_confidence>=3` AND
`research_complete=YES` AND `overall_evidence_confidence>=3`. `priority` is
`REVIEW` whenever `eligible_for_outreach != YES` or `research_complete !=
YES`, regardless of `final_score` — **a high-scoring candidate with
unresolved material evidence is never promoted on the strength of its score
alone.** Both remain `scoring_engine.py`'s *proposed* values — the Section 5
approval gate below is unchanged: the owner still approves `priority` and
`ready_to_email` before either is final.

**Opportunity type, generalized** (supersedes the qualitative-only framing
above wherever `service_scope` is set — `NO OPPORTUNITY` remains a valid
legacy value on old, unscored records; the engine itself only ever produces
`DEFEND` / `GROWTH` / `GAP` / `REVIEW`):

```
DEFEND   if a comparable same-scope peer exists (>=2 businesses share this
             service_scope in the pool)
         AND visibility_score >= 3
         AND relative_position >= 0.85   (own visibility_rate / the highest
             visibility_rate among OTHER businesses sharing this exact
             service_scope - never compared across scopes with different
             denominators)
         AND question_coverage >= 0.75   (share of the business's OWN
             relevant questions it appears on at least once - a breadth
             check independent of raw volume)
GAP      elif business_credibility >= 3 AND visibility_score <= 1
REVIEW   elif visibility_score == 0 AND business_credibility < 3
GROWTH   otherwise
```

Three deliberate safeguards baked into this rule, each added because an
earlier version of it got a real case wrong: **(1)** DEFEND requires a real
peer — a business alone in its `service_scope` cannot be "leading" a
group of one, however high its own `visibility_score`. **(2)** DEFEND still
needs `visibility_score >= 3` in absolute terms even when `relative_position`
is 1.0 — leading a weak field is not the same as meaningful visibility.
**(3)** GAP requires `business_credibility >= 3` — a business with
near-zero visibility AND unresolved credibility is not a confident
commercial opportunity in either direction; it is `REVIEW`.

**Ranking** — `overall_rank`: dense rank across every scored business in
this campaign (`market[]` and `outreach[]` combined) by `final_score`, tied
broken by (`gap_strength` desc, `business_credibility` desc,
`visibility_score` desc, `business` A–Z). `outreach_rank`: the identical
tie-break, computed only among `outreach[]` entries with
`ready_to_email=YES`, consecutive from 1 — **`build_workbook.py`'s
`validate()` rejects a file where `outreach_rank` values have a gap, or
where any entry without `ready_to_email=YES` carries one.** A business can
have a high `overall_rank` and no `outreach_rank` at all — that gap in the
sequence is the intended, self-explaining signal that evidence is still
unresolved, not a bug to paper over.

**Evidence separation** — `sources[].fact_category` (optional; one of
`LEGAL_IDENTITY` / `SERVICE_SCOPE` / `LOCAL_OWNERSHIP` /
`DECISION_MAKER_IDENTITY` / `CONTACT_ROUTE` / `AI_APPEARANCE` /
`COMPETITOR_COMPARISON` / `COMMERCIAL_CLAIM`) lets evidence for different
kinds of claims about the same business be told apart at a glance instead of
being one undifferentiated list. Record a correction explicitly (a new
source entry stating what was previously believed and what the current
evidence shows) rather than silently overwriting an earlier finding — see
`sample/sample-campaign.json` for the general pattern; a real example is the
Wirral v2.1 run's Kutchenhaus Wirral correction (a director who had
resigned was still being described as the current owner).

**Portable downstream handoff** — `build_workbook.py` is built with
`xlsxwriter`, not `openpyxl`, specifically so every formula cell carries a
genuine cached value. Verify this after building: reopen the output file
with `openpyxl.load_workbook(path, data_only=True)` and confirm ranks,
scores, visibility measures, statuses, accessibility grades, and opportunity
types are populated, not `None`. (One narrow, documented exception:
`Outreach rank`'s cached value for a non-ready business is a real, present
empty string — the mathematically correct result of that formula's ELSE
branch — which `openpyxl`'s reader happens to surface as `None`
indistinguishably from a genuinely missing calculation; check the saved XML
directly if this specific distinction ever matters.) The `Shortlist` sheet
is written as plain values with no formulas at all, so it needs no formula
engine whatsoever — this is `/outreach`'s primary handoff even though, today,
`/outreach` actually reads the campaign JSON directly and never opens the
workbook.

**Known limitation, stated plainly rather than hidden:** the weighted-
denominator formula assumes every question in a campaign was run the same
number of times across the same providers (`run.responses_per_question`,
uniform) — true of every `trade_run.py` campaign to date. A campaign that
genuinely varies run-count per question is not yet supported by
`scoring_engine.py` and would need that formula extended first.

### `run` (required: `sector`, `geography`, `campaign_slug`, `date`, `questions`, `providers`)

| Field | Required | Source |
|---|---|---|
| `sector` | yes | AUTO — the trade named when the run was set up |
| `geography` | yes | AUTO to populate, copied from the run's own scope — but see §2: if the market's boundary was ambiguous, that was a HUMAN call made *before* Stage A, not something to resolve here |
| `campaign_slug` | yes | AUTO — matches the `--client` value used in `trade_run.py` |
| `date` | yes | AUTO — the date the campaign JSON is compiled |
| `questions` | yes | AUTO — a list of `{question_id, text}` objects (schema v2; was a list of plain strings pre-v2). `question_id` matches the raw CSV's own `question_id` column (e.g. `q01`) — the join key `question_relevance[]` and every business's `question_appearances` key off |
| `providers` | yes | AUTO — a list of `{provider, model}` objects. `provider` is one of the schema's fixed enum (`openai`, `gemini`, `perplexity`, `copilot`, `ai-overviews`) — a trade run currently produces the first three. `model` is the exact `model_version` string the raw CSV actually recorded, per `playbook/models-and-schemas.md` ("record the exact model version string on every single run") — not the nominal `OPENAI_MODEL` env var, the string the provider actually returned |
| `expected_responses` | no | AUTO — the planned query count (e.g. 90) |
| `successful_responses` | no | AUTO — count of raw CSV rows with an empty `errors` column |
| `responses_per_question` | no (required if any business sets `service_scope`) | AUTO — runs × providers for one question (e.g. 5×3=15). Assumes a uniform count per question — see Section 3a's limitation note |
| `raw_data_path` | no | AUTO — the `--out` path the run was written to |
| `methodology_notes` | no | CLAUDE — anything methodological worth flagging: errored/retried rows, a geography-ambiguity note, anything that would make a later reader distrust a naive comparison |
| `service_scopes` | no (required if any business sets `service_scope`) | CLAUDE, from RESEARCH — see Section 3a |
| `question_relevance` | no (required if any business sets `service_scope`) | CLAUDE — see Section 3a; one entry per `question_id`, all questions must be covered |

### `market[]` — `market_entry` (required: `business`, `area`, `disposition`, `total_ai_appearances`)

| Field | Required | Source |
|---|---|---|
| `business` | yes | RESEARCH — from the market census |
| `area` | yes | RESEARCH — the specific branch/trading location, from the census |
| `disposition` | yes | CLAUDE — `OUTREACH` / `EXCLUDED` / `REVIEW`, against the five-point check in `playbook/outreach-process.md` step 4. **The schema has no separate approval field for this** — see §5 for exactly which fields carry the formal human gate |
| `opportunity_type` | no | CLAUDE — `GAP` / `GROWTH` / `DEFEND` / `NO OPPORTUNITY`, per the subsection above — not `REVIEW`, which belongs to `disposition`. Separate from `disposition`: a business can be `EXCLUDED` from this campaign's outreach and still carry a `DEFEND` opportunity type for later |
| `accessibility` | no | CLAUDE, from RESEARCH — `DIRECT` / `IDENTIFIABLE` / `GATEKEPT` / `CORPORATE` / `REVIEW`, per the "Decision-maker accessibility" subsection. Optional here — most census entries don't get individual contact-route research; it becomes required once a business reaches `outreach[]` |
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
| `competitive_gap_finding` | yes | **AUTO for a scored entry** (`scoring_engine.py`'s `generate_competitive_gap_finding()` — see Section 3a's narrative subsection), mandatory and unconditional, never hand-written first. CLAUDE for an unscored/legacy-path entry: one factual sentence stating the counts, per the letter templates in `playbook/outreach-process.md` |
| `why_prospect` | yes | **AUTO for a scored entry** (`generate_why_prospect()`, same subsection) — the DEFEND/GROWTH/GAP commercial case, from structured values, mandatory and unconditional. CLAUDE for an unscored/legacy-path entry: the case for this business against `playbook/outreach-process.md`'s definition of a strong prospect. Either way, never a copy of `business_type_notes` |
| `narrative_generated_from` | no (AUTO-only for a scored entry) | AUTO — a fingerprint of the values the two fields above were generated from, written only by `scoring_engine.py`. Never hand-set: doing so to make a hand-written narrative look machine-verified is exactly the defect this field exists to catch |
| `legal_entity` | yes | RESEARCH — Companies House. **No confirmed active Ltd/LLP match, no entry in `outreach[]`** — the business stays `REVIEW` in `market[]` or moves to `excluded[]` (`NO RELIABLE LEGAL MATCH`) instead. This is the PECR rule in `CLAUDE.md`, enforced at the schema boundary, not worked around with a placeholder |
| `company_number` | yes | RESEARCH — Companies House |
| `company_status` | yes | RESEARCH — Companies House |
| `contact_person` | no | RESEARCH — `[PLACEHOLDER]` is permitted here (see `sample-campaign.json`) precisely because this field is optional; never invent a name |
| `role` | no | RESEARCH — same as above |
| `contact_email` | no | RESEARCH — same as above |
| `accessibility` | **yes** | CLAUDE, from RESEARCH — `DIRECT` / `IDENTIFIABLE` / `GATEKEPT` / `CORPORATE` / `REVIEW`, per the "Decision-maker accessibility" subsection. Required once a business is in `outreach[]` — an ambiguous match is `REVIEW`, not an omitted field |
| `decision_maker_linkedin` | no | RESEARCH — only where confidently matched on name, role and business/location together; omit rather than record an unconfident guess |
| `accessibility_notes` | no | CLAUDE — one or two sentences: who was found, whether they're actively associated with the business now, and why the classification landed where it did (e.g. "generic inbox only", "regional group, no local purchasing authority") |
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
- **No invented directors, LinkedIn matches, or contact routes.**
  `decision_maker_linkedin` goes in only where the match is confident on
  name, role and business/location together — a same-name profile that
  doesn't corroborate on the other two is not a match, it's a coincidence.
  An ambiguous person-match is `accessibility: REVIEW`, never a guessed
  `DIRECT`/`IDENTIFIABLE` to make the record look more complete than the
  research supports.
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
   `NO OPPORTUNITY`) — §3. Not every census business gets one.
3. For every business heading toward `outreach[]`, research and classify
   `accessibility` (`DIRECT`/`IDENTIFIABLE`/`GATEKEPT`/`CORPORATE`/`REVIEW`)
   — §3's "Decision-maker accessibility" subsection. Required, not optional,
   once a business is in `outreach[]`.
4. Produce proposed classifications: `disposition` for every market entry,
   `reason` for every exclusion, `priority` and `ready_to_email` for every
   outreach candidate — weighing `accessibility` as one factor among several,
   never as an automatic override of commercial opportunity.
5. Present the HUMAN fields — `priority` and `ready_to_email` — for the
   owner's approval before treating anything as final.
6. Populate the final JSON against `schema.json` exactly, using §3 (and §3a
   for any business opting into scoring) as the field-by-field checklist.
6a. If any business sets `service_scope`, run `scoring_engine.py` before
   `build_workbook.py` — see §7. It fills in every DERIVED field in §3a;
   trying to hand-type `final_score`, `overall_rank`, `opportunity_type`, or
   any other DERIVED field instead of running the engine defeats the entire
   point of an auditable, reproducible score.
7. Save the campaign JSON in the run's canonical location. There is no
   formal folder rule for prospecting runs yet (only client audits have one,
   in `playbook/records-and-data.md`) — until one exists, follow the pattern
   the Wirral run already used: `~/wardith-runs/<sector>-<geography>/`
   holding the campaign JSON and workbook, next to the raw CSV at
   `~/wardith-runs/<sector>-<geography>.csv`. Never inside this repository.
8. Run the existing Prospect Compiler (§7).
9. **If validation fails, fix the data or this handoff, not the tooling.**
   See §8.
10. Contact verification and outreach sending happen after this procedure,
    not as part of it — see `playbook/outreach-process.md`. Every opportunity
    type routes to the Audit first (§1); what follows the audit is decided
    from what the audit finds, not predicted at qualification time.

---

## 7. Validation command

Two commands, exactly as documented in `tools/prospect-compiler/README.md`.
If any business in the campaign sets `service_scope`, run the scoring engine
first — it fills in every §3a DERIVED field the render step then displays:

```
python3 scoring_engine.py --input campaign.json --in-place
python3 build_workbook.py --input campaign.json --output workbook.xlsx
```

A campaign with no scored businesses (nothing sets `service_scope`) can skip
straight to `build_workbook.py`, exactly as before.

`build_workbook.py`'s own `validate()` function is the final machine gate —
it checks every required field, every enum value, that every
`evidence_source_ids` entry resolves to a real source, that every scored
entry has both its VALUE and DERIVED fields populated (i.e. the engine
actually ran), and that `outreach_rank` values are consecutive and confined
to `ready_to_email=YES` entries — and it fails with a specific error rather
than guessing. There is no separate validation framework to reach for; a
failure here is read and fixed, not routed around.

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
