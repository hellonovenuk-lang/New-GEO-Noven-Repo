# The audit report template

**Status: Decided, unvalidated** — written down, never yet performed.

**Internal document.** The report the client receives, and the rules for writing
it. Copy the template below into the client's audit folder, fill it in, export to
PDF, attach to a short email.

Written 2026-07-30 as part of roadmap 3a. Companion to `archive/audit-method.md`.

---

## How to write it

**Length: 1,200 to 1,800 words.** The site promises "a short written report in
plain English" on three separate pages, and 1,800 words is about five pages —
still short against the twenty-page decks with a cover sheet this competes with.
But the cap is real: past about 1,800 it stops being read, and it stops being
writable in the time a £250 fee pays for.

**Length has to be earned by findings, never by padding.** If the honest report
is 1,200 words, it is 1,200 words. Writing to the top of the range to look
thorough is the same failure as a twenty-page deck, just cheaper.

*Amended 2026-08-03, from 800–1,200. Two reasons. The owner read the first full
report and found the longer form "a real consultancy report with enough detail to
show we actually did the work, not just a checklist with vague scoring out of
100". And rule 10 adds a mandatory section that runs 300–400 words on its own —
a range that doesn't accommodate its own required sections is just a rule that
gets broken every time. The first band tried was 1,000–1,600 and was wrong for
exactly that reason: it left less room for the other seven sections than the
pre-rule-10 report already used.*

**The ten rules.**

1. **No jargon, at all.** Not softened jargon, not jargon-with-a-definition.
   `CLAUDE.md` bans the industry's vocabulary outright. Write "the code that
   tells a machine what your business is" rather than the name of the format.
2. **No score, no index, no grade.** Argued in `archive/audit-method.md` section 4.
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
   bans repeated calls to action, and a £250 report that reads as an £800 pitch
   destroys the thing the £250 bought.
10. **Say what they are doing right, not only what is wrong. Every report, in
    its own section, whatever the verdict.** Three reasons, and the third is the
    commercial one. *Credibility:* a client cannot tell "your site is in good
    order" from "we didn't look at your site" if the report only lists problems,
    and those are very different pieces of work. *Accuracy:* on a site that
    passes, the good news is a finding — it is what makes the one real gap read
    as a small fix rather than the tip of something. *And it is where the
    Foundation quote comes from.* `archive/audit-method.md`'s companion checklist
    already says the audit list and the Foundation list are the same list, one
    diagnosing and one fixing, and that the client seeing them line up "is most
    of why they believe the second one". Going group by group through what is
    already right is what makes the £800 quote legible instead of asserted.

*Rule 10 added 2026-08-03, after the first full report was written without it.
The gap was invisible on that report because the site being audited passed
nearly everything — the atypical case. On a normal client, whose site has real
problems, this section is most of the Foundation scope.*

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

## What we found on your website

*Rule 10. This section is not optional and it is not padding — it goes in every
report, whatever the verdict.*

*Work the four checklist groups in order, one short block each, and for every
group say **both** what is right and what is missing. Not the good news here and
the bad news later — the whole picture of the site, group by group:*

1. *Can the assistants get to the site at all?*
2. *Can they read it once they're in?*
3. *Are the business facts written where a machine can find them?*
4. *Does any page answer the questions customers actually ask?*

*Name what passes. "Nothing here is blocking them" is a sentence worth writing
when it's true, and a client cannot infer it from silence. Then name what fails
in the same block, in plain words, and point forward: "that's finding 2 below".*

**Never write a group as a flat pass when one assistant fails it.** "The
assistants can reach you" is false if Copilot can't, and a client who later
discovers that reads the whole report differently. Say which, and how many.

*This is not diagnosing twice. **This section describes the state of the site;
the findings rank what to do about it and what it costs.** The findings also
draw on things that aren't the website at all — a name, a missing listing, a bad
review — so the two sections are not the same list and shouldn't read as one.*

*Close with a one-line summary of the four: how many are in good order, how many
have a single gap, how many are genuinely absent.*

*On a typical client this section is longer than the findings, because most
sites have four or five things right and two badly wrong. That is the correct
shape. It is also, group by group, the Foundation scope — so a client who reads
this section and then reads the quote should recognise the same list.*

**But "in the Foundation scope" is not the same as "worth one of the three
findings", and structured data is the case that proves it.** Added 2026-08-10.
Group 3 turns up missing JSON-LD on most small sites, and it is genuinely worth
a developer's hour — **it is also the thing we measured and found does not
predict whether the assistants name you** (`playbook/audit-site-checklist.md`, "What
structured data is worth"). So it belongs here, described plainly, and it
belongs in the quote as housekeeping. **It should almost never be finding 1, 2
or 3**, because with only three slots it has to beat things the run actually
evidenced — directory presence, and whether their own domain gets cited.

**The reason to be strict about this is that markup is the perfect thing to pad
a quote with.** It is technical, the client cannot evaluate it, and it demos
beautifully in a validator. A £800 Foundation whose visible bulk is schema the
audit itself called low-impact is the mirror image of the failure
`archive/outreach.md` §5 warns about, and it is worse, because here we would be the
ones who knew.

**So the quote says which items are evidenced and which are housekeeping**, and
prices accordingly. If housekeeping is all there is, the honest branch below is
"you don't need us" — not a Foundation with the schema written large.

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
which is £800 one-off, on the website you already have. {If the honest answer is
"one of these three matters and the other two don't", say that and quote for the
one.}

**If something else has to happen first:** {What, why, and what to do about it.}
We're not the right spend until that's sorted, and we'd rather tell you now than
take £800 for work that wouldn't hold.

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

**{Kieran Smith} · Wardith · {email}**

*Wardith is one person. The person who wrote this report is the person who did the
work.*

---

## The covering email

Short. The report is the document; the email is a note attached to it.

> Subject: Your Wardith audit — {business}
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
