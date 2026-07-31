# The audit report template

**Internal document.** The report the client receives, and the rules for writing
it. Copy the template below into the client's audit folder, fill it in, export to
PDF, attach to a short email.

Written 2026-07-30 as part of roadmap 3a. Companion to `ops/audit-method.md`.

---

## How to write it

**Length: 800 to 1,200 words.** The site promises "a short written report in
plain English" on three separate pages. A twenty-page document with a cover
sheet would break that promise while appearing to over-deliver, and it would
take three hours to write against a £125 fee. Short is the product, not a
shortcut.

**The nine rules.**

1. **No jargon, at all.** Not softened jargon, not jargon-with-a-definition.
   `CLAUDE.md` bans the industry's vocabulary outright. Write "the code that
   tells a machine what your business is" rather than the name of the format.
2. **No score, no index, no grade.** Argued in `ops/audit-method.md` section 4.
   Every competitor prints one; ours would be an invented statistic.
3. **Bands with the raw count beside them**, never a percentage.
4. **Quote the assistants directly.** One or two short verbatim quotes carry
   more than a page of description, and they are checkable. Quote the wrong ones
   as well as the flattering ones.
5. **Three findings, not ten.** Ranked. A long list gets nothing done.
6. **Say what it costs them, not what it is.** "Nobody asking about price can be
   pointed at you, because you don't publish one" beats a description of the
   fix.
7. **Never invent a number.** No traffic estimates, no "you're missing X
   enquiries a month", no market sizing. We have run counts. That is what we
   have.
8. **If the honest answer is "you're fine", the report says that and stops.**
   Four pages of the site promise this outcome. It has to be real often enough
   that it is not a slogan.
9. **No second sales pitch.** One recommendation, once, at the end. `CLAUDE.md`
   bans repeated calls to action, and a £125 report that reads as a £750 pitch
   destroys the thing the £125 bought.

**Anything unknown is written as `[PLACEHOLDER]` and raised with the owner
before the report is sent.** Standard rule, and it applies hardest here — this
is the one document that leaves the building with our name and a number on it.

**Before sending, check three things:** every figure in the report traces to a
row in `runs.csv`; every quote is verbatim; the verdict in the report matches
the verdict on the checklist.

---

## The template

Everything below this line is the client-facing document. Replace anything in
`{braces}`. Delete the guidance in *italics*.

---

# What AI assistants say about {business}

**Prepared for {contact name} · {date}**

## What we did

Between {start date} and {end date} we asked the AI assistants your customers
use — ChatGPT, Google's Gemini, Microsoft Copilot and Perplexity — ten questions
of the kind someone looking for {trade} in {area} would actually ask. We asked
each question five times, because these systems do not give the same answer
twice, and we recorded every answer.

We then looked at your website and at the places these systems draw information
from, to work out *why* the answers came back the way they did.

Two things worth knowing before you read the rest:

- **Their answers vary.** The same question asked five times can produce five
  different answers. That is why we ask everything several times and report a
  range rather than a verdict. Anyone who gives you a single confident score is
  reporting one roll of a dice.
- **We check through the developer versions of these systems.** The apps on your
  phone answer slightly differently and take your own history into account, so
  if you ask ChatGPT about yourself you may see something different from what we
  saw. Both are real. Neither is the whole picture.

## Where you show up today

*The headline sentence first, in plain words. Then the table.*

Across {n} checks, {business} was named {n} times.

| What we asked | ChatGPT | Gemini | Perplexity |
|---|---|---|---|
| {q01} | {band} ({n} of 5) | | |
| {q02} | | | |
| {q03} | | | |
| ... | | | |

Copilot and Google's AI results can't be checked automatically, so we asked those
by hand — the three questions above that matter most to you, three times each.
{What happened.}

*Bands: never appeared (0 of 5), occasionally (1–2), often (3–4), consistently
(5). Say this once, here, in a line.*

## What they believe about you

*What the assistants actually think {business} is, and whether it's right.
Verbatim quotes. This is where a wrong fact goes, and a wrong fact leads the
section — it matters more than absence and clients react to it.*

> "{verbatim quote}" — {assistant}, {date}

{Accurate / inaccurate, and what specifically.}

## Who gets recommended instead

*Named competitors and how often, straight from the runs. No commentary on
whether they deserve it — we don't know, and guessing would be inventing.*

| Business | Times named |
|---|---|
| {competitor} | {n} |

{One sentence on anything the named businesses visibly have that {business}
doesn't — published prices, a page about the specific service, more reviews.
Only what we can see. Nothing inferred.}

## What's holding you back

*Three, ranked. Each one: what it is in plain words, what it costs them, what
fixing it involves. No more than three.*

**1. {Finding}.** {What it means in plain words.} {What it costs them.} {What
fixing it involves.}

**2. {Finding}.**

**3. {Finding}.**

## What we'd do about it

*One of three, and the honest one.*

**If they're in good shape:** Nothing, and you don't need us. {What is already
working, specifically.} We'd suggest checking again in six months or if
something about the business changes. That's the whole recommendation — we'd
rather say it than sell you something you don't need.

**If the Foundation would help:** {The specific things, tied to the three
findings above, and what changes if they're done.} That's our Foundation work,
which is £750 one-off, on the website you already have. {If the honest answer is
"one of these three matters and the other two don't", say that and quote for the
one.}

**If something else has to happen first:** {What, why, and what to do about it.}
We're not the right spend until that's sorted, and we'd rather tell you now than
take £750 for work that wouldn't hold.

## What this doesn't tell you

- These answers are from {dates}. They will be different next month — that is
  the nature of the systems, not a flaw in the checking.
- Five runs is enough to tell "never" from "sometimes" from "usually". It is not
  enough to read a small change as a trend.
- We can't see inside these systems, and nobody outside the companies that run
  them can. What we can see is what they say and what they draw on, and we've
  reported exactly that.
- We haven't checked {anything skipped, and why}.

If you'd like the raw record — every question, every run, every answer in full —
just ask and we'll send it over.

---

**{Kieran Smith} · Noven · {email}**

*Noven is one person. The person who wrote this report is the person who did the
work.*

---

## The covering email

Short. The report is the document; the email is a note attached to it.

> Subject: Your Noven audit — {business}
>
> Hi {name},
>
> Your audit's attached. The short version: {one sentence — the single most
> important finding, good or bad}.
>
> {One line on the recommendation, including "you don't need us" where that's
> the answer.}
>
> Anything you want to go through, just reply.
>
> Kieran

**No follow-up sequence.** `contact.astro` says so publicly, and it is true.
