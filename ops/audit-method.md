# How we do the audit

**Internal document.** Decides how the £30 audit is actually delivered: which
assistants we check, how many times, how we record it, what it costs us, and how
long it is allowed to take. Written 2026-07-30.

**Status: decided on paper, unvalidated in practice.** Nothing below has been
run against a real business yet. Every time figure is an estimate until the
first audit is done and timed — see section 8, which says how to do that without
waiting for a client.

This closes the decision half of roadmap 3a. What remains is doing one.

Companion documents:

- `ops/audit-questions.md` — the ten questions and how they change by trade
- `ops/audit-site-checklist.md` — what we look at on their website and off it
- `ops/audit-report-template.md` — what the client receives
- `ops/audit-setup.md` — the practical setup: accounts, keys, spend caps, where
  the data lives, and the order to do it in on the day

---

## 1. What the audit is for, and what it is worth

The audit is sold as an honest diagnosis, and it has to be one. But it is worth
being straight internally about the second thing it is: **the qualifier for the
£350 Foundation.**

`ops/service-tiers.md` section 6 already establishes that the Foundation is the
income in year one, and that converting audits into Foundations matters more
than upgrading monthly clients. That has a consequence for this document. At
£30, an audit that takes 90 minutes earns about £20 an hour, which is not a wage.
**The audit does not stand alone as profitable work and should not be judged as
if it does.** It is judged on two things: whether the report is good enough that
the client believes the next £350, and whether it can be delivered inside its
time budget without cutting corners.

Two consequences that follow directly:

- **Never soften a finding to protect a Foundation sale.** The site promises "you
  don't need us" as an outcome, on four separate pages. An audit that never
  produces that outcome is a sales document, and the whole position collapses.
  The honest version converts better anyway, because it is the only reason
  anyone pays a stranger £350 next.
- **If an audit takes more than two hours, the process is wrong, not the price.**
  Roadmap 3a says this and it is right. The response is to cut scope from the
  method, not to raise £30 — £30 is doing a specific job, which is making trying
  us a small decision.

---

## 2. Which assistants we check — and the Copilot problem

The site promises four, on the FAQ page: ChatGPT, Google's AI results and
Gemini, Microsoft Copilot, and Perplexity. We check all four. **But we cannot
check them all the same way, and pretending otherwise would be the first
dishonest thing in the product.**

### The finding that forces the split

**Microsoft Copilot has no API, and the route that used to substitute for one is
gone.** Microsoft retired the Bing Search APIs on 11 August 2025 and now directs
developers to Grounding with Bing Search inside Azure AI Foundry — which is an
Azure project with resource groups and a deployed model, not a drop-in endpoint,
and which is *Bing grounding on an Azure model*, not Copilot. It would not tell
us what Copilot says. It would tell us what a different assistant we built says.

**Google AI Overviews have the same problem for the same reason.** The Gemini
API with Grounding by Google Search is a good proxy for Gemini. It is not the
AI Overview block a customer sees above the search results, and no API exposes
that.

So the four promised assistants divide into two groups, and the report says so
in plain words.

### The decision

| Assistant | How we check it | Runs |
|---|---|---|
| ChatGPT | OpenAI API with the web search tool | 10 questions × 5 |
| Google (Gemini) | Gemini API with Grounding by Google Search | 10 questions × 5 |
| Perplexity | Sonar API (search is built into the model) | 10 questions × 5 |
| Microsoft Copilot | **By hand, in the consumer app** | top 3 questions × 3 |
| Google AI Overviews | **By hand, logged out** | top 3 questions × 3 |

**150 API queries and 18 by hand.** The hand-checked pair get the three questions
that matter most to that client — normally the discovery questions — because
eighteen manual lookups is about twelve minutes and sixty would be an hour.

### Why not just drop Copilot

Because Copilot is the one assistant a UK business owner's *staff* are most
likely to have in front of them at work, and because dropping it means changing
the FAQ's list, which weakens the offer for a delivery reason the client should
not have to care about. A reduced-confidence check, clearly labelled, is worth
more than a silent omission. What we must never do is present three hand runs
as though they carried the same weight as five API runs — hence the bands in
section 4, which make the difference visible without arithmetic.

### The better Copilot diagnostic is not a mention rate at all

Copilot answers are grounded in Bing's index. **If the client's site is not in
Bing's index, Copilot cannot cite it, and that is a harder, more useful finding
than any mention rate.** So the Copilot section of the report leans on the Bing
Webmaster Tools check in `ops/audit-site-checklist.md` and treats the three hand
runs as illustration. This is a better answer than the one we would have got
from an API, and it is actionable — indexation is fixable, model behaviour is
not.

### Not checking Claude

Anthropic's API is the easiest of all of them to run and Claude is deliberately
**not** in the standard audit, because the site does not promise it and a fifth
assistant is 50 more queries and more report to read. Revisit if a client asks
for it, or if UK usage makes it a normal thing for a customer to have used.

### Which model, per provider

**Use each provider's current default consumer-facing tier, not the cheapest
model.** Representativeness is the entire point of the exercise, and section 6
shows cost is not the binding constraint — the whole audit is under £3 either
way. Saving £1 by measuring a model no customer uses would be false economy.

**Record the exact model version string on every single run.** When a provider
ships a new model the numbers move for reasons that have nothing to do with the
client, and the record has to be able to say so. A month-on-month comparison
across a model change is not a comparison, and the monthly record must flag it
rather than report it as progress or decline.

---

## 3. How many times we ask, and the settings

**Five runs per question per assistant on the API checks. Three on the hand
checks.** Five is the number `ops/third-party-services.md` section E3 arrived at
from the variance research, and it stays until we have evidence about it — the
experiment that produces that evidence is in section 8.

Fixed rules, so that two audits are comparable:

- **A fresh conversation for every run.** No accumulated context, ever.
- **No system prompt** beyond whatever the provider imposes. We are not
  measuring what an assistant can be steered into saying.
- **Provider default sampling settings, not temperature 0.** Zero would be
  quieter and would flatter the report, but the consumer apps run hot on
  purpose. We are measuring the variance, not suppressing it.
- **UK locale** wherever it can be set, and the area named in the question
  rather than relied on from IP.
- **The client's business name never appears in a discovery question.** Naming
  them contaminates the answer — an assistant handed a name will use it. The
  named questions are a separate group for exactly this reason.
- **Hand checks in a logged-out or temporary session**, so the owner's own
  history does not personalise the answer.
- **Same day, or as close as possible.** An audit spread over a week is
  measuring the week as much as the business.

---

## 4. What counts as appearing, and how we report it

### The four outcomes

A yes/no on "were they mentioned" throws away the most valuable half of what
comes back. Every run is recorded as one of four:

| Outcome | Meaning |
|---|---|
| **Not named** | The business does not appear in the answer. |
| **Named** | The name appears, with nothing specific attached. |
| **Named with detail** | The name appears with a correct fact — a service, an area, a price, a link, a phone number. |
| **Named wrongly** | The name appears attached to something untrue. |

"Appeared" in the headline means named at all. **"Named wrongly" is reported
separately and loudly**, because it is worse than absence and clients do not
expect it. It is also the single most persuasive finding an audit can produce:
an assistant confidently telling customers the wrong opening hours is a problem
the owner feels immediately, in a way that "you appeared in 1 of 5" is not.

**Record every competitor named, in every discovery answer, from audit one.** It
costs nothing at the point of collection and it is the raw material for the Lead
tier's quarterly review. Not capturing it means re-running the whole audit later
to get it.

### Bands, not percentages

**We report a band with the raw count beside it, and we do not report a
percentage.**

| Band | Runs |
|---|---|
| Never appeared | 0 of 5 |
| Occasionally | 1–2 of 5 |
| Often | 3–4 of 5 |
| Consistently | 5 of 5 |

The reason is arithmetic honesty. Five runs is enough to tell "never" from
"sometimes" from "usually". It is nowhere near enough to distinguish 3 of 5 from
2 of 5 — that difference is well inside what chance produces from an unchanged
business. Publishing "60%" invites a client to read next month's "40%" as a
decline, when both are the same underlying reality. **A number we cannot defend
is a number we should not print**, and every competitor product in this category
prints one.

Same rule, stated as a hard line for the report: **no score out of ten, no
visibility index, no grade.** `CLAUDE.md` forbids inventing statistics, and a
composite score assembled from 150 noisy runs is an invented statistic wearing a
suit. The band table *is* the score, and it is checkable.

### The two honesty notes, in every report

Both are already argued in `ops/third-party-services.md` E3. They go in the
report as standing text, not as a caveat we add when the news is bad:

1. Answers vary between runs, which is why we ask everything five times and
   report a range rather than a verdict.
2. We check through the assistants' developer interfaces. The consumer apps
   answer slightly differently and add personalisation, so if you ask ChatGPT
   yourself you may see something different from what we saw. Both are real.

Saying this before the client discovers it is the difference between a
methodology and an excuse.

---

## 5. How we record it

**One row per run.** Not per question, not per assistant — per run, or the rate
cannot be reconstructed and the raw answers are lost.

`runs.csv`:

| Column | Notes |
|---|---|
| `audit_id` | `slug-YYYY-MM-DD` |
| `client` | Business name |
| `run_at` | ISO 8601, UTC |
| `assistant` | `chatgpt` / `gemini` / `perplexity` / `copilot` / `ai-overviews` |
| `surface` | `api` or `app` — never blank, this is what the bands depend on |
| `model_version` | Exact string the provider reports |
| `question_id` | `q01`–`q10` |
| `run_no` | 1–5 |
| `outcome` | `not_named` / `named` / `named_detail` / `named_wrong` |
| `competitors` | Semicolon-separated, as written in the answer |
| `errors` | What was said that is untrue, if anything |
| `sources_cited` | URLs the assistant cited, semicolon-separated |
| `answer_text` | The full answer, verbatim |
| `notes` | Anything odd — refusals, a question misread, an outage |

`questions.csv`: `audit_id, question_id, category, question_text, frozen_from`.
Separate file because the questions outlive the audit — they become the client's
tracked set if they take a monthly plan (see `ops/audit-questions.md`).

**Verbatim answer text is not optional.** It is what lets us answer "why did you
conclude that" six months later, it is where the quotes in the report come from,
and re-running is not a substitute because the answer will have changed.

### Where it lives — and why not here

**Client audit data does not go in this repository.** This repo is public, and
the recorded answers will contain business contact details and, for sole traders
and partnerships, personal data — a sole trader's name and business address is
personal data under UK GDPR. Noven registered with the ICO on 2026-07-30; this
is precisely the obligation that registration attaches to.

So: one folder per client in the owner's own storage, backed up, not in git.

```
clients/<slug>/audit-YYYY-MM-DD/
  runs.csv
  questions.csv
  checklist.md      (filled copy of ops/audit-site-checklist.md)
  report.md         (filled copy of ops/audit-report-template.md)
  report.pdf        (what the client receives)
```

**Two things this hands to the owner as decisions, flagged rather than assumed:**

- **Retention.** Recommendation: keep audit records for the life of the
  relationship plus twelve months, then delete. Twelve months because a client
  who comes back inside a year is well served by having their baseline; beyond
  that it is stale data we are holding for no reason. This needs to match
  whatever the privacy notice ends up saying (roadmap 1c, `third-party-services`
  D2) — **write it into the privacy notice rather than deciding it twice.**
- **The client's own copy.** Recommendation: offer the raw `runs.csv` to any
  client who asks and say so in the report. Nobody will ask. Offering it is the
  cheapest credibility in the whole product, and it is only credible if it is
  true, so the format has to be legible to a stranger — which it is.

---

## 6. What one audit costs us

Confirmed 2026-07-30, replacing the two `[PLACEHOLDER]` figures in
`ops/third-party-services.md` E2. Rates move; re-check before relying on this to
change a price.

| Provider | Search charge | Token charge | 50 queries |
|---|---|---|---|
| OpenAI | $10 per 1,000 web search calls ($0.01 each) | Retrieved search content billed as input tokens on top | ~$0.65 |
| Google | 5,000 free grounded prompts/month on the Gemini 3 family, then $14 per 1,000 | Retrieved context not billed as input tokens | $0 to ~$1.40 |
| Perplexity | Per-request fee, roughly $5–14 per 1,000 depending on mode — **confirm before relying on it** | ~$1 per million tokens each way on base Sonar | ~$0.25–0.70 |
| Anthropic | $10 per 1,000 searches | Standard token rates | Not used — see section 2 |

**An audit's tool cost is about £1.20 at full rate, and closer to £0.60 while
Google's free allowance covers it.** Against £30 that is a cost of goods of
around 4%. This confirms the E2 conclusion with real numbers, and it settles the
build-versus-buy question permanently at our volume: the cheapest monitoring
subscription is £20–23 a month *per brand tracked*, which is most of the fee for
one client for one month.

**One billing trap worth knowing:** on Google, a single request can trigger
several billable search queries, so budget 1.5–2× the query count rather than
1×. It does not change the conclusion, but it is the kind of thing that turns a
free tier into a bill without warning. **Set a spend cap on every provider
account before the first real run**, low enough that a bug costs pounds rather
than hundreds.

**Cost is not the constraint on this product. Time is.** Which is the next
section.

---

## 7. The time budget, and the one thing that has to be built

Target: **90 minutes of the owner's time per audit.** Not because 90 minutes is
comfortable at £30 — it isn't, see section 1 — but because it is the number at
which the promise on the site ("the report within one working day") is keepable
alongside everything else in a day.

| Step | Budget |
|---|---|
| Read the order, build the ten questions from the client's own words | 15 min |
| Start the API runs | 5 min (then unattended) |
| Copilot and AI Overviews by hand | 15 min |
| Website checklist, on-site | 20 min |
| Off-site facts and consistency checks | 15 min |
| Write the report | 20 min |
| Send it | 5 min |
| **Total** | **95 min** |

### The thing that decides whether this works

**150 API queries cannot be typed by hand.** At thirty seconds a query that is
75 minutes of typing and pasting before a single word of the report is written,
and it destroys the budget above on its own. So the method as designed depends
on one small piece of software:

**A runner.** Reads `questions.csv` and a config naming the assistants, models
and run count; calls the three APIs; writes `runs.csv` with the answer text and
model version; prints a per-assistant count at the end. Non-negotiable
properties: a **hard cap on queries per invocation** so a loop bug costs pence;
**resume**, so a provider outage halfway through does not mean starting again;
**verbatim answer text**; and **client data written outside the repo** by
default.

Everything the runner cannot do stays manual on purpose — deciding the outcome
of each run, spotting a wrong fact, reading the website. Those are the judgement
and they are what the client is paying for.

**Deliberately not built in this session, for two reasons.** The three provider
APIs need confirming against live documentation rather than written from memory
— the no-invented-facts rule applies to code as much as to copy, and half the
provider docs were unreachable from this session. And more importantly: **the
first audit should be run half by hand so that we find out what the runner
actually needs to record.** A runner written before audit one is a guess at a
format; written after, it is a transcription of something that worked. That is
the same principle the rest of the roadmap runs on.

---

## 8. Do the first audit on Noven

Roadmap 3a says "do the first one end to end and time it", which reads as though
it waits for a paying client. **It does not have to, and it should not.**

**Audit number one is Noven's own**, and it does four jobs at once:

1. **It times the process** against a real business, which is the input roadmap
   3c is waiting on to validate the Maintain hour — the number
   `ops/service-tiers.md` section 6 says decides the ceiling of the whole
   business.
2. **It is roadmap 1e's outstanding launch check** — "ask the assistants what
   they say about Noven" — done properly and recorded rather than glanced at.
3. **It creates the dated before-and-after baseline** that roadmap 2d wants as
   the first proof. Today's answer is almost certainly "they have never heard of
   Noven", and that is exactly the baseline worth having, taken now while it is
   still true.
4. **The report becomes the sample we show prospects.** "Here is what you get for
   £30 — this is ours, including the bit where the assistants had never heard of
   us" is a genuinely strong answer to the FAQ's own question about having no
   case studies. It is honest, it is free, and it proves the deliverable exists.

**Run one experiment while doing it, and only one:** take three questions to ten
runs instead of five, and check whether the band changes. If the bands hold, five
runs is validated and `ops/service-tiers.md` section 8 can be closed. If they
move, five is too few and both the audit and every monthly plan need the higher
number — which is a cost and time change worth knowing before a client is
depending on it, not after.

The one thing the Noven audit cannot test is the intake: building ten good
questions out of a stranger's description of their own business is the step most
likely to take longer than budgeted, and we already know our own answers. Expect
the first real client's audit to run over, and time that one too.

---

## 9. What is deliberately left undecided

- **Anything about how the Foundation follows on.** That is roadmap 3b, and it
  should be written after an audit has produced a real list of findings.
- **Whether the ten questions are the right number** for the audit specifically.
  Ten matches the Maintain plan so the audit's set carries over intact, which is
  worth more than optimising the audit in isolation. Revisit only if intake
  keeps producing more good questions than the set can hold.
- **Whether the report is a PDF or an email.** Going with a PDF attached to a
  short email: it is the thing a client can forward to a business partner, and
  the site calls it a written report. Trivially reversible.
- **What we do about a client with no website.** The order page will require a
  website address, which handles it at the front door — see roadmap 1c. What is
  left is the case where the URL passes validation and the site turns out to be
  a parked domain or a Facebook page, which is a refund, and is covered by the
  refund line already decided for the terms.

---

## 10. One thing to fold into the order page before it is built

The order page is blocked behind the terms, the privacy notice and the address
for service, so it does not exist yet — which makes this cheap to add now and
expensive to add later.

`contact.astro` collects four things: business name, website, services to be
found for, area served. Those four are enough to *start*, and the FAQ says so.
But building ten good questions from them is the 15-minute step above, and it is
the step most likely to overrun.

**Add a fifth field: "What do people usually ask when they first get in touch?"**
Optional, free text, two lines. It is the only question whose answer we cannot
derive ourselves, it is the difference between questions in the client's
customers' words and questions in ours, and a business owner can answer it in
fifteen seconds without thinking. It also improves the report, because a question
the client recognises as one their customers actually ask is the one they read
the result of first.
