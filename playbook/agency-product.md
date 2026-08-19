# Wardith for Agencies

*The agency product line: a research layer SEO agencies buy for their own
clients. Designed 2026-08-19. **Nothing here has been sold, delivered or
timed.** Prices below are targets, not published prices — `services.md`
holds what is actually on the site.*

---

## What it is

An SEO agency keeps the client relationship and does the SEO work. Wardith
researches how that client's market is represented across AI assistants,
benchmarks the client against the competitors the assistants actually name,
turns the findings into work the agency's own team can do, and re-runs the
same measurement monthly so the agency can show what moved.

**The agency is the customer. The agency's client is the subject.** Wardith
never contacts the end client. Every output is written to be handed on by
the agency, under the agency's name where they want that.

## The three products

| | Price target | Cadence | Queries |
|---|---|---|---|
| **The Benchmark** | £495 one-off | Once, at the start | 12 questions x 3 assistants x 5 runs = 180 |
| **The Monthly Review** | £149/month | Monthly | The same 180, re-run |
| **The Quarterly Review** | Included while subscribed | Every third month, in place of that month's review | The same 180, plus a refreshed framework check |

Agency volume discounts are a later decision, not designed here.

---

## 1. The Benchmark

The first audit. Establishes what everything afterwards is measured against.

### 1.1 The query framework

**Twelve questions, frozen.** Not the trade run's six (which deliberately
never names a business) and not the £250 audit's ten (which has no relevance
weighting). Built from the client's real services, real geography and real
customer buying situations, confirmed with the agency before anything runs.

| Category | What it answers | Count |
|---|---|---|
| `discovery` | Do they get named at all for the thing they sell? | 3 |
| `qualified-discovery` | Do they get named for the specific work they want more of? | 3 |
| `buying-intent` | Do they get named when a customer describes a problem, not a service? | 2 |
| `comparison` | Who gets named instead of them? | 2 |
| `named-business` | What do the assistants believe about them, and is it true? | 2 |

`audit-process.md`'s four wording rules apply unchanged: the customer's word
not the industry's word, a named town plus one wider area and never a
postcode, no business name outside the `named-business` pair, and written the
way a person says it out loud.

**High-intent subset.** The agency nominates which questions represent work
they actually want more of — normally the `qualified-discovery` and
`buying-intent` rows. Recorded as data, reported separately, and it is the
subset the Monthly weights most heavily.

**Question relevance is classified before anything is scored**, using the
same four types `CAMPAIGN-HANDOFF.md` §3a already defines
(`SERVICE_ONLY` / `EXPLICITLY_COMBINED` / `SINGLE_SERVICE_INCLUSIVE` /
`AMBIGUOUS` plus an explicit weight). A client that only does half of what
the framework asks about is never scored as absent from the other half.

### 1.2 Measurement

`tools/trade-run/trade_run.py`, unchanged, against the three assistants with
an API: OpenAI, Gemini, Perplexity. Five runs per question per assistant.
Every model version string recorded per `models-and-schemas.md`.

**Copilot and AI Overviews are hand-checked at reduced sample on the
Benchmark and the Quarterly only, never monthly.** Neither has an API, the
Azure route measures something else, and a hand step does not survive
multiplication by an agency's client list. The report says this plainly.

Run completeness is gated by `.claude/skills/90qrun/scripts/validate_run.py`
before any analysis begins.

### 1.3 What gets reported

Bands with raw counts. **No score out of ten, no visibility index, no
percentage presented as a headline** — `decisions.md`, unchanged, and it
matters more here than in the audit because a monthly product is exactly
where an invented composite would take hold.

| Band | Runs |
|---|---|
| Never appeared | 0 of 5 |
| Occasionally | 1-2 of 5 |
| Often | 3-4 of 5 |
| Consistently | 5 of 5 |

Sections, each of which has to survive the implementability test in §5:

1. **Visibility and recommendation frequency** — banded, per question, with
   the raw counts beside them.
2. **Visibility by assistant** — where the client is strong on one and
   silent on another. Reported only where the split is material
   (absent from one assistant entirely, or one carrying 70% or more of the
   total), not as boilerplate on every finding.
3. **Visibility by question category** — discovery versus qualified
   discovery versus buying intent is a different diagnosis each time.
4. **High-intent visibility** — the nominated subset, on its own.
5. **Competitor benchmark** — the peer set is the businesses the answers
   themselves named, not a market census researched from scratch. Counted
   mechanically by `tools/mention-count/mention_count.py`.
6. **Citation and source analysis** — which domains the assistants built
   these answers from, which name the client, and which name a competitor
   but not the client. See §1.4.
7. **Meaningful competitor advantages** — what the cited sources show a
   better-represented competitor has that the client does not. Evidence,
   then inference, kept apart.
8. **Client site, entity and evidence inspection** —
   `tools/site-check/site_check.py` for crawler access and machine-readable
   facts, plus an entity check: is the business's name, address and
   description the same everywhere a cited source repeats it.
9. **Five to ten prioritised actions**, each tagged with the finding it
   answers and who does it (agency dev, agency content, client).
10. **Confidence and limitations**, including anything the run could not
    establish.
11. **Baseline metrics** — the machine-readable `baseline.json` the Monthly
    diffs against.

### 1.4 Citation and source analysis

The genuinely new half. `sources_cited` has been collected on every Wardith
run since the first and never once analysed.

Per assistant and per question, aggregated by domain:

- Which domains the answers are built from at all.
- Which of those the client appears on.
- **Which name a competitor and not the client** — the actionable one. A
  directory, a "best X in Y" listicle or a trade body page that three
  assistants cite and the client is missing from is a specific, checkable
  piece of work for the agency's team, not a general recommendation.
- Whether the client's own site is cited, and on which questions.

This is deterministic and mechanical: `tools/benchmark/citation_analysis.py`.

### 1.5 Evidence, inference, recommendation

Every statement in a Benchmark carries one of three labels, and the report
says what they mean:

- **Observed** — it is in the run data or a fetched page. A count, a band, a
  cited URL, a `robots.txt` line.
- **Inferred** — a reading of the observed data that is probably right and is
  not itself measured. "The assistants appear to be building these answers
  from directory pages rather than the client's own site."
- **Recommended** — what to do about it.

An inference never inherits an observation's confidence, and the report
never presents one as the other.

### 1.6 What the Benchmark deliberately is not

Not a technical SEO audit. Ahrefs, Semrush and Screaming Frog do that
better, the agency already owns them, and duplicating them is how this
product becomes a commodity. A technical finding earns its place only when
it explains something in the AI visibility evidence — a `robots.txt` line
that blocks the crawler whose assistant never names the client is in scope;
a general crawl-depth report is not.

---

## 2. The Monthly Review

**The question it answers: what materially changed since last time, and what
should the SEO team do about it.**

Not another audit. The framework is frozen, the peer set is carried forward,
the site is not re-inspected. The same 180 queries are re-run and diffed.

Reported:

- Material visibility changes, per question and in aggregate.
- Gains and losses by question group, with the high-intent subset separated.
- Meaningful competitor movement.
- New and lost citations and sources.
- Change in recommendation frequency.
- Whether the previous run's priority areas appear to have moved.
- Three to five actions or investigations for the coming month.
- Confidence, including which changes are inside expected variation.

### 2.1 The stochasticity rule

**`[PLACEHOLDER: needs the owner's decision before the Monthly is sold.]`**
The proposal below is what the design assumes; it is not settled.

`audit-process.md` is explicit that five runs cannot distinguish 3 of 5 from
2 of 5, because that difference is inside what chance produces from an
unchanged business. A monthly product that reports that difference as
progress is selling noise. So:

- Change is reported at **band** level, not count level.
- A single question moving by **one run in five** is labelled *inside
  expected variation* and is never a headline.
- A change is called **material** only when the same direction shows across
  **three or more questions**, or when a **high-intent question changes
  band**.
- Everything else is shown in the data and explicitly not claimed.

**The noise floor has never been measured.** Nobody has run one question set
twice. Until that happens the rule above is reasoned, not evidenced — the
first pilot should run its Benchmark twice, two weeks apart, with nothing
changed in between, which measures the floor for the cost of one extra run.

### 2.2 The model-change gate

**A month-on-month comparison across a provider model change is not a
comparison.** `models-and-schemas.md` already requires flagging it. In this
product the diff **fails closed**: where a provider's `model_version` differs
from the baseline's, that provider's month-on-month movement is reported as
unmeasurable and no progress or decline is claimed for it. The other two
providers still report normally.

---

## 3. The Quarterly Review

Runs in place of that month's review, not in addition to it.

Refreshes the strategic picture without rebuilding everything:

- **Is the framework still right?** Has the client added a service, changed
  geography, or started chasing different work. Questions may be retired or
  added — and any change is recorded, because a changed framework breaks
  comparability with the earlier baseline for those questions specifically.
- **Refresh the peer set.** New businesses appear in answers; some stop.
- **Full citation analysis**, not the month's delta.
- **Re-run `site_check`** and the entity consistency check.
- **Three-month trend**, not the month-on-month delta — a trend across three
  runs survives the noise floor that a single month's move does not.
- **Copilot and AI Overviews hand spot-check.**
- Revised priorities for the coming quarter.

---

## 4. Naming, facing and white label

**Umbrella: Wardith for Agencies.** Products are "the Benchmark", "the
Monthly Review", "the Quarterly Review". Plain, no acronym — `decisions.md`'s
rule that Wardith never describes itself with an industry acronym applies to
what it sells too, and generic names are also what makes a white-label
version possible without renaming anything.

| | Agency-facing | Client-facing | Never leaves Wardith |
|---|---|---|---|
| Findings summary, bands, counts | yes | yes | |
| Competitor benchmark | yes | yes | |
| What changed this month | yes | yes | |
| Citation and source analysis | yes | summary only | |
| Prioritised actions with implementation notes | yes | | |
| Query framework rationale | yes | | |
| Confidence and limitations, in full | yes | short form | |
| Methodology detail, model versions | yes | | |
| Raw evidence appendix | yes | | |
| Wardith's own pricing | | | yes |
| Unexplained-finding working notes | | | yes |

**White label, MVP definition.** The client-facing document is a `.docx`
with a neutral cover, no Wardith name in the body text, and no Wardith
branding — the agency puts their own header on it and exports the PDF. That
is the entire mechanism. No portal, no branding configuration, no per-agency
theming. `CLAUDE.md` already requires client-facing documents in Office
formats, so this costs nothing extra.

---

## 5. The test every section has to pass

**Can an SEO professional implement something, investigate something,
explain something to their client, or measure something next month because
of this finding?**

If not, it does not go in. This is the line that keeps the product from
drifting into a generic audit, and it is worth applying to a section as a
whole, not only to individual sentences.

---

## 6. Data

Everything lives outside this repository, under
`~/wardith-runs/agency/<agency-slug>/<client-slug>/`. `CLAUDE.md`'s rule that
no client or prospect name enters this repo is absolute and applies to
question files too — **which is why an agency-product question set is never
committed, unlike a generic `/90qrun` trade question set.**

**Retained between runs:** the frozen framework, the raw runs CSV with
verbatim answer text, per-provider model version strings, the mention
counts, the peer census, the citation index, and `baseline.json`.

Verbatim answers are not optional. They are what lets a conclusion be
defended six months later, and re-running is not a substitute because the
answer will have changed.

**Not stored:** personal data about the client's staff or the agency's staff
beyond the single agency contact the relationship needs; the client's own
customer data; anything the agency has not authorised us to hold.

**Retention:** relationship plus twelve months, matching
`records-and-data.md`. Do-not-contact requests permanently.

---

## 7. What is reused, and what is new

**Reused unchanged.** `tools/trade-run/trade_run.py`;
`.claude/skills/90qrun/scripts/validate_run.py`;
`tools/mention-count/mention_count.py`; `tools/site-check/site_check.py`;
`audit-process.md`'s wording rules, four outcomes and four bands;
`models-and-schemas.md`'s run schema and model-version rule; `voice.md` for
everything anyone reads; and the visibility half of
`tools/prospect-compiler/scoring_engine.py` — relevance weighting, question
coverage, relative position and the GAP/GROWTH/DEFEND thresholds, taken as
constants rather than reinvented.

**Not reused.** The contact-route, decision-maker-accessibility and
`ready_to_email` half of the campaign schema. A client the agency already
owns has no decision-maker to score and nobody to email.

**New.** The client-anchored twelve-question framework; the citation and
source analysis; benchmark metrics for one focal business against a peer set
rather than a census ranked for prospecting; and change detection with a
stated noise floor.

---

## 8. Open, and needed before this is sold

- **The free sample contradicts a settled decision.** `decisions.md`: *"No
  free audits, no introductory rate, no first-five discount, no bundling."*
  `/agencysample` is not an audit, is not for the end client, and is a
  condensed version of a different product — but it is a free piece of paid
  work and needs an explicit decision either way.
  `[PLACEHOLDER: owner's decision.]`
- **The stochasticity rule in §2.1.** `[PLACEHOLDER: owner's decision.]`
- **Nothing here has been timed**, and neither has the £250 audit. Both
  budgets are guesses. Time the first one.
- **The economics need more than one client per agency.** At £495 plus
  £149 x 12 = £2,283 a year against roughly 35 owner-hours, the model works
  at about £65/hour — but only because the framework, peer set and citation
  index are reusable across an agency's clients in the same sector and
  geography. A single-client agency is worse than selling that client a
  £250 audit directly. Consider a floor of two or three clients per agency.
  `[PLACEHOLDER: no real timings exist to check this against.]`
- **The Monthly's API cost is real.** 180 queries at the self-audit's
  observed OpenAI rate is roughly £24 a month against £149, before any owner
  time.
- **Authority for the site inspection.** The paid Benchmark makes live
  requests to the client's site. The agency should confirm they have their
  client's authority. The free sample does not need this — it reads public
  pages the way any crawler does — but it must say plainly that the end
  client was never contacted.
