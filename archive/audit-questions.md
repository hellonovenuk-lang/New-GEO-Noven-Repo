# The questions we ask the assistants

**Status: Decided, unvalidated** — written down, never yet performed.

**Internal document.** The ten-question frame used in every audit, how it changes
by trade and area, and the rules that keep two audits comparable. Written
2026-07-30 as part of roadmap 3a.

Read `ops/audit-method.md` first — it decides how many times each question is
asked and how the answers are recorded.

**Why this file matters more than it looks.** `ops/third-party-services.md` E2
makes the strategic argument for running the questions ourselves rather than
renting a platform: *"building our own question set is the thing that compounds —
after twenty audits we have a library of questions that work by trade and by
area, which is an asset a subscription never becomes."* This file is that asset.
Add to it after every audit.

---

## 1. The frame — ten questions, five jobs

Every audit asks ten questions. They are not ten variations on one thing; they
are five different jobs, and dropping a category to fit more of another leaves a
hole in the report.

| # | Category | What it tells us | Count |
|---|---|---|---|
| 1 | **Discovery** | Do they get named at all, unprompted, for the thing they sell? | 3 |
| 2 | **Qualified discovery** | Do they get named for the *specific* work they want? | 2 |
| 3 | **Named business** | What do the assistants believe about them, and is it true? | 2 |
| 4 | **Comparison** | Who gets named instead of them, and why? | 1 |
| 5 | **Buying intent** | Do they get named when a real person describes a problem rather than a service? | 2 |

**Discovery is the one that matters.** It is the question the whole product
exists for, it is the one where the answer is usually "no", and it is the one the
client will read first. Three of them, worded differently, because a single
phrasing tells you about a phrasing rather than about a business.

**The named-business questions are where the money finding usually is.** Not
absence — absence is expected and undramatic. It is an assistant stating
something *untrue* with confidence, which owners react to in a way they never
react to a mention rate. Ask them on every audit even when the discovery
questions have already come back empty.

---

## 2. The slots

Every question is built from the same five slots. Fill them from the client's
own words, not ours.

| Slot | What goes in it | Where it comes from |
|---|---|---|
| `{trade}` | What a customer would call them | The order form's "services you want to be found for", translated into customer language |
| `{town}` | The specific place | "Area served" |
| `{region}` | The wider area a stranger would say | Judgement — "the Wirral", "Merseyside", "north Wales" |
| `{segment}` | Who they want, or the specialism | The order form, or the intake question |
| `{trigger}` | The event that makes someone go looking | The intake question — this is the slot that needs the client |
| `{business}` | Their trading name, exactly as they write it | The order form |

### The four wording rules

1. **Their customers' word, never their industry's word.** "Accountant", not
   "chartered accountancy practice". "Boiler repair", not "domestic heating
   solutions". "Physio", not "musculoskeletal rehabilitation". Assistants answer
   the question a customer asks, and customers do not use trade vocabulary. This
   is the single most common way a question set gets built wrong.
2. **A named town, and one wider area. Never a postcode.** "Birkenhead" and "the
   Wirral". Nobody types CH41 into ChatGPT, and results for a postcode tell us
   about the postcode.
3. **No business name in categories 1, 2, 4 or 5.** An assistant handed a name
   will use it, and the run is then worthless as a measure of discovery. Naming
   happens only in category 3.
4. **Write it as a person would say it out loud**, including the untidiness.
   "who's a good accountant in Birkenhead" beats "best accountant Birkenhead" —
   the second is a search box query, and the whole point of this business is that
   people have stopped typing those.

---

## 3. The ten, as templates

**Discovery — 3**

- `q01` Who's a good {trade} in {town}?
- `q02` Can you recommend a {trade} near {town}?
- `q03` I need a {trade} in {region} — who should I look at?

**Qualified discovery — 2**

- `q04` Who's a good {trade} in {town} for {segment}?
- `q05` Which {trade}s in {region} deal with {segment}?

**Named business — 2**

- `q06` What do you know about {business}?
- `q07` Is {business} in {town} any good, and what do they do?

**Comparison — 1**

- `q08` Who are the main alternatives to {business} in {region}?

**Buying intent — 2**

- `q09` {trigger} — who do I call in {town}?
- `q10` I'm looking for someone in {region} to {trigger}. What are my options and roughly what should it cost?

`q10` earns its place by asking about price. Assistants answer price questions
badly and evasively, which makes any business with published prices unusually
easy to recommend — and most small businesses publish none. It produces a
Foundation recommendation on nearly every audit, and an honest one.

---

## 4. Two worked examples

Illustrations of the frame, not real clients. `{business}` stays a placeholder —
nothing in this file invents a business.

### An accountant in Birkenhead, wanting small limited companies

| # | Question |
|---|---|
| q01 | Who's a good accountant in Birkenhead? |
| q02 | Can you recommend an accountant near Birkenhead? |
| q03 | I need an accountant in the Wirral — who should I look at? |
| q04 | Who's a good accountant in Birkenhead for a small limited company? |
| q05 | Which accountants in the Wirral deal with contractors and one-person companies? |
| q06 | What do you know about {business}? |
| q07 | Is {business} in Birkenhead any good, and what do they do? |
| q08 | Who are the main alternatives to {business} in the Wirral? |
| q09 | I've just set up a limited company and need someone to do the accounts — who do I call in Birkenhead? |
| q10 | I'm looking for someone in the Wirral to do my company's year-end accounts and payroll. What are my options and roughly what should it cost? |

### A physiotherapy clinic in Heswall

| # | Question |
|---|---|
| q01 | Who's a good physio in Heswall? |
| q02 | Can you recommend a physiotherapist near Heswall? |
| q03 | I need a physio in the Wirral — who should I look at? |
| q04 | Who's a good physio in Heswall for sports injuries? |
| q05 | Which physiotherapy clinics in the Wirral treat back pain without a GP referral? |
| q06 | What do you know about {business}? |
| q07 | Is {business} in Heswall any good, and what do they do? |
| q08 | Who are the main alternatives to {business} on the Wirral? |
| q09 | I've hurt my shoulder and can't lift my arm — who do I call in Heswall? |
| q10 | I'm looking for someone in the Wirral for physio after a knee operation. What are my options and roughly what should it cost? |

Note what changed between them and what didn't. The frame is identical. Only the
slots moved, plus the phrasing of `q05` and `q09`, which have to sound like the
sort of thing that trade's customers actually say. **That is the whole variation
by trade and area** — it is deliberately not a different set per industry,
because a different set per industry cannot be compared, cannot be reused, and
cannot be built in fifteen minutes.

---

## 5. The rules that protect the record

**The set is frozen for twelve months once the client has seen it.** Changing a
question resets its history — a mention rate against a new wording is not
comparable with the old one, and month five of a Maintain plan is worthless if
half the set has quietly drifted. If a question genuinely has to change, it gets
a **new** id, the old one is retired with a date, and the monthly record says so
in a sentence.

**The audit's ten become the Maintain ten.** Deliberate. It means the client's
first monthly record is directly comparable with the audit they already paid for
— they can see movement in month one instead of waiting for month two, and we
never re-do intake. It also means the audit's questions must be good enough to
live with for a year, which is worth the fifteen minutes.

**Show the client the ten before running them**, in the order confirmation. Not
for approval — for correction. They will fix a word we got wrong about their own
trade, and that fix is worth more than anything we would have reasoned our way
to. It costs one email that is being sent anyway.

**Growing to 25 and 50.** Grow and Lead do not invent new categories; they widen
the existing ones in a fixed priority order, so a client moving up gets more
coverage rather than a different product:

1. More towns — the same discovery questions in each place they actually serve.
   Usually the largest single gain, because assistants are strongly local.
2. More segments — one qualified pair per service line they sell.
3. More triggers — the specific problems that send someone looking.
4. More comparison questions, one per named competitor that keeps appearing.

Which means the ceiling on a client's question count is set by how many real
towns, services and problems they have, not by the price they pay. **A sole
trader in one town with one service should be told Grow will not help them yet,
and sold Maintain.** Selling 25 questions to a business that only has 12 real
ones produces filler, and filler is how a monthly record stops being read.

---

## 6. Questions that look useful and aren't

Written down so they don't get re-proposed after someone reads a competitor's
marketing.

- **"How do I improve my visibility with AI assistants?"** Asks the assistant to
  describe our job. Tells us nothing about the client.
- **Anything with "best" in it.** "Best accountant in Birkenhead" invites a
  ranked list the assistant has no basis for, and the answer is dominated by
  whoever writes listicles. Real people ask for a good one, not the best one.
- **Questions naming a competitor without naming the client**, outside `q08`. It
  measures the competitor, and we are not being paid for that.
- **Anything about the client's website** ("is {business}'s site any good"). The
  assistant has not evaluated their site; it will confabulate a plausible answer,
  and that answer will end up in a report as if it were a finding. The website is
  assessed by us, against `ops/audit-site-checklist.md`, by looking at it.
- **Yes/no questions.** "Do you know {business}?" gets a polite yes far more
  often than the business deserves. `q06`'s open wording is what exposes whether
  anything real is behind it.

---

## 7. What to add here after every audit

Two minutes at the end of each audit, and it is the compounding part:

- Any question the **client** suggested that turned out to be better than ours.
- Any wording that produced a noticeably different answer from its neighbours —
  those are the ones worth keeping.
- The trade's actual customer vocabulary, where it differed from what we guessed.
- Competitor names that keep recurring in that area, with the trade. After a
  handful of audits in one trade this is a genuinely valuable local picture, and
  it arrives for free.
