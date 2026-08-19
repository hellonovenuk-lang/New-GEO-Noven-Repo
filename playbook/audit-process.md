# Audit process

*The £250 product, end to end. Run once, on our own business, 2026-08-02.
Never yet sold.*

**This is Audit v1. Keep the format fixed for the first five paid audits
unless a material flaw appears. Review it after five paid deliveries using
actual timings, costs, client reactions and findings.**

**Target: under three hours of owner time. Promise on the site: the report
within two working days of confirming scope and payment.**

---

## 1. Build the ten questions

Ten questions, five jobs. Dropping a category to fit more of another leaves a
hole in the report.

| Category | What it tells us | Count |
|---|---|---|
| **Discovery** | Do they get named at all, unprompted, for the thing they sell? | 3 |
| **Qualified discovery** | Do they get named for the *specific* work they want? | 2 |
| **Named business** | What do the assistants believe about them, and is it true? | 2 |
| **Comparison** | Who gets named instead of them? | 1 |
| **Buying intent** | Do they get named when someone describes a problem rather than a service? | 2 |

**Discovery is what the product exists for** — usually the answer is no, and the
client reads it first. **The named-business questions are where the money finding
usually is:** not absence, which is expected, but an assistant stating something
*untrue* with confidence. Owners react to that in a way they never react to a
mention rate. Ask them even when discovery came back empty.

### The templates

- `q01` Who's a good {trade} in {town}?
- `q02` Can you recommend a {trade} near {town}?
- `q03` I need a {trade} in {region} — who should I look at?
- `q04` Who's a good {trade} in {town} for {segment}?
- `q05` Which {trade}s in {region} deal with {segment}?
- `q06` What do you know about {business}?
- `q07` Is {business} in {town} any good, and what do they do?
- `q08` Who are the main alternatives to {business} in {region}?
- `q09` {trigger} — who do I call in {town}?
- `q10` I'm looking for someone in {region} to {trigger}. What are my options and roughly what should it cost?

`q10` earns its place by asking about price. Assistants answer price questions
badly, which makes a business with published prices unusually easy to recommend
— and most small businesses publish none. It produces an honest Foundation
recommendation on nearly every audit.

### The four wording rules

1. **Their customers' word, never their industry's word.** "Accountant", not
   "chartered accountancy practice". The single most common way a question set
   gets built wrong.
2. **A named town and one wider area. Never a postcode.**
3. **No business name in discovery, qualified discovery, comparison or buying
   intent.** An assistant handed a name will use it and the run is worthless as
   a measure of discovery. Naming happens only in the named-business pair.
   **This rule and the `q08` template above disagree, and `q08` is right** —
   "who are the main alternatives to {business}" needs the name to mean
   anything. So three of the ten questions are prompted, not two. That is
   fine as long as their runs are never counted inside a discovery figure:
   `models-and-schemas.md`, "Prompted and unprompted visibility". Noted
   2026-08-19; the question set itself is unchanged.
4. **Write it as a person would say it out loud**, including the untidiness.

**Show the client the ten before running them.** That is why turnaround is two
working days, not one.

## 2. Run them

| Assistant | How | Runs |
|---|---|---|
| ChatGPT | OpenAI API, web search tool | 10 × 5 |
| Google (Gemini) | Gemini API, Grounding by Google Search | 10 × 5 |
| Perplexity | Sonar API | 10 × 5 |
| Microsoft Copilot | **By hand, consumer app** | top 3 × 3 |
| Google AI Overviews | **By hand, logged out** | top 3 × 3 |

**150 API queries and 18 by hand.** Copilot and AI Overviews have no API, and
the Azure route would measure a different assistant we built rather than the one
the customer sees. The report says this in plain words.

**Fixed settings, so two audits are comparable:** fresh conversation every run;
no system prompt; provider default sampling, not temperature 0 (the consumer
apps run hot on purpose and we are measuring the variance, not suppressing it);
UK locale; hand checks logged out; all on the same day.

## 3. Classify every run

Four outcomes, not yes/no:

| Outcome | Meaning |
|---|---|
| **Not named** | Does not appear |
| **Named** | Name appears, nothing specific attached |
| **Named with detail** | Name appears with a correct fact |
| **Named wrongly** | Name appears attached to something untrue |

**"Named wrongly" is reported separately and loudly.** It is worse than absence,
clients do not expect it, and it is the single most persuasive finding an audit
can produce.

**Record every competitor named in every discovery answer, from audit one.** It
is free at collection and it is the raw material for Lead's quarterly review.

### Bands, never percentages

| Band | Runs |
|---|---|
| Never appeared | 0 of 5 |
| Occasionally | 1–2 of 5 |
| Often | 3–4 of 5 |
| Consistently | 5 of 5 |

Five runs distinguishes never from sometimes from usually. It cannot distinguish
3 of 5 from 2 of 5 — that is inside what chance produces from an unchanged
business. **No percentage, no score out of ten, no visibility index, no grade.**
A composite score assembled from 150 noisy runs is an invented statistic wearing
a suit, and every competitor in this category prints one.

## 4. Check the website

Four groups, in order. Full list: `audit-site-checklist.md`.

1. Can the assistants get to the site at all? (`robots.txt`, blocks, Cloudflare)
2. Can they read it once they're in? (Is the visible text in the source?)
3. Are the business facts written where a machine can find them?
4. Does any page answer the questions customers actually ask?

**Say what passes as well as what fails.** "Nothing here is blocking them" is
worth writing when it's true, and a client cannot infer it from silence.

## 5. Write the report

Template: `audit-report-template.md`. Three findings, ranked, no more than
three. The site section describes the state of the site; the findings rank what
to do about it and what it costs.

**One of three closing recommendations, and the honest one:** they're in good
shape and don't need us; the Foundation would help, tied to the named findings;
or something else has to happen first and we're not the right spend yet.

## The time budget

| Step | Budget |
|---|---|
| Build the ten questions from the client's own words | 15 min |
| Send them, get them confirmed | 5 min + waiting |
| Start the API runs | 5 min, then unattended |
| Copilot and AI Overviews by hand | 15 min |
| **Read and classify all 168 runs** | **60–110 min** |
| Website checklist | 20 min |
| Off-site facts and consistency | 15 min |
| Write the report | 20 min |
| Send it | 5 min |
| **Total** | **2h40 – 3h30** |

**Nobody has ever timed this.** The classification step has no prior estimate
behind it at all and it is the one that decides whether £250 holds. Time it
separately on the first real audit.

## What it costs us to run

**$12.63 on OpenAI alone for ~75 queries** on the self-audit — roughly $0.17 a
query. Gemini and Perplexity totals were never recorded. **Get all three real
figures on the first paid audit.** Every audit spends real money on the day.

## Where the work lives

One folder per client per audit, **outside this repository**, holding the filled
site checklist, `runs.csv`, `questions.csv`, the report and the timings. Client
names never enter the repo.
