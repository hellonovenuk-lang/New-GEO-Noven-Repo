# The monthly record

**Internal document.** The one-page written record every monthly client receives,
and the rules for writing it. Copy the template below into the client's folder,
fill it in, export to PDF, attach to a short email. Written 2026-07-31.

Read `ops/audit-method.md` first — it decides the outcomes, the bands and the
no-percentages rule, and this file inherits all three. Where the two disagree,
the method wins.

**Why this file exists.** The audit runs once per client. This runs every month,
for every client, for as long as they stay — it is the entire deliverable at
Maintain and the spine of the other two. It had a price and no format, which is
the fastest route to month one being improvised and month three being
inconsistent. Inconsistency is fatal to a product whose whole claim is comparable
measurement over time.

---

## How to write it

**Budget: 20 minutes, after the runs are done and classified.** If it is taking
longer than that, the template is wrong or something bespoke has crept in. At
£150 a month there is no room for either.

**One page. Four sections, always in this order, even when a section is dull.** A
client who gets a long record in a good month and a short one in a bad month
learns to read length as news.

**Same rules as the audit report:**

- A band with the raw count beside it. **Never a percentage.** Five runs cannot
  tell 3 from 2, and a client reading 60% then 40% sees a decline that isn't
  there.
- No score, no index, no grade.
- Quote verbatim. A sentence an assistant actually said about their business is
  worth more than any summary of it.
- "Named wrongly" is reported separately and loudly. It is worse than absence
  and it is what owners react to hardest.

**The rule that prevents the worst failure:** if a provider shipped a new model
version this month, say so at the top, in one line, before the table. Otherwise
the first month an assistant changes its behaviour reads to the client as their
own decline — and they will have been paying us to prevent exactly that.

**Do not sell in it.** Grow and Lead sell themselves through section 3: the
record reports the gap and does not close it. A client reading the same unclosed
gap for three months either asks us to fix it or is content to hold position, and
both are honest outcomes. Adding a pitch converts a report into an advert and
costs the trust the report was earning.

---

## The template

> ## {business} — visibility record, {month} {year}
>
> {If a model version changed this month: "One thing to note before the numbers:
> {provider} moved to a new version of its model on {date}. Changes in the table
> below may reflect that rather than anything about your business. We flag this
> whenever it happens."}
>
> ### 1. Where you appeared
>
> | Question | This month | Last month |
> |---|---|---|
> | {question, in the client's own words} | {band} ({n} of {runs}) | {band} ({n}) |
>
> {One sentence naming the standout, good or bad. Then, if anything was named
> wrongly, its own short paragraph — what was said, which assistant, and what
> the true fact is.}
>
> ### 2. What changed
>
> {Two or three sentences. What moved and, where we know it, why. If nothing
> moved, say that plainly — "no meaningful change this month" is a legitimate
> result for a plan called Maintain and pretending otherwise trains the client
> to expect drama.}
>
> ### 3. What you're still missing from
>
> {The questions where the band is Never or Occasionally, listed. One line each
> on what would have to be true for that to change. No pitch — the list is the
> prompt.}
>
> ### 4. What we did
>
> {Facts corrected, drift fixed, pages published this month. Specific and
> checkable: "corrected your opening hours on {source}" beats "maintained your
> business information".}
>
> ---
>
> Answers vary between runs, which is why we ask everything {runs} times and
> report a range rather than a single figure. We check {n} questions for you each
> month; the assistants are asked in the same way every time so the months are
> comparable.
>
> — {sender}, Wardith

---

## What changes by tier

The format does not change. Three things inside it do:

| | Maintain | Grow | Lead |
|---|---|---|---|
| Questions in section 1 | 10 | 15 | 25 |
| Section 4 includes | facts and drift only | + the page published this month | + both pages |
| Quarterly | — | — | + the competitor review, sent separately |

**The quarterly competitor review is not part of this record.** It is its own
document, sent in the third month of each quarter, and it is the only thing at
Lead that isn't simply more. Its format is not yet written — no Lead client
exists, and writing it before one does would be guessing at what they want to
know. `ROADMAP.md` 3c carries it.

---

## Still open

- **The time budget is an estimate**, like every other in this repo. Time the
  first three and correct it here.
- **Month-on-month comparison assumes the questions are frozen.** They are, for
  twelve months from the point the client agrees them
  (`ops/audit-questions.md`). The first client to want a question changed
  mid-year is the test of whether that rule survives contact.
- **Whether "last month" should be "last month" or "three months ago"** once
  there is enough history. A single month of movement is mostly noise; a
  quarter is signal. Revisit at month four, with real data rather than an
  opinion.
