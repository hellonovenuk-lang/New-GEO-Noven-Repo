# Condensing without losing the argument

The owner has asked for reasoning to be condensed, not only for duplication to
be removed. That is a sharper instrument than it sounds, because the reasoning
in this repo is doing a job: it stops a future session reopening a question that
was already settled, and it records conditions nobody has met yet. Cut the wrong
sentence and the repo forgets why, which is the one failure mode that compounds.

So: cut words, keep facts. This document is the method.

## A closed decision keeps almost nothing

*Sharpened by the owner 2026-08-08, and it is the most aggressive rule here.*

When a decision is **made and acted on** — the account is open, the supplier is
paid, the name is bought — the comparison that produced it has no further job.
Delete it. Not "condense": delete. A reader who will never reopen the question
gains nothing from the case against the option that lost, and pays to read it
every time.

What survives a closed decision:

- **What we use**, in one line.
- **Facts that change a future action**: what it costs, when it renews, account
  and reference numbers, caps and limits, the traps in using it.
- **Anything still unverified** about the thing we chose.
- **One line naming what was rejected**, and nothing more — enough that nobody
  re-proposes it, without re-running the argument.

What goes, however well written:

- The merits of options not taken. `C1` carried five paragraphs on Mettle,
  Starling and Tide *after* the Revolut account was open and in use.
- "Superseded reasoning, kept for context." If it is superseded it is history,
  and history lives in `ops/session-log.md`.
- Advice about how to make the decision — lead times, what to check before
  choosing — once it is made.
- The argument that the decision "still holds up". It holds up; it is in force.

**This is safe here for one specific reason, and it stops being safe without
it.** `ops/session-log.md` is the archive of why, it is never condensed, and git
holds every prior version besides. Stripping a live document is not destroying
the record — it is moving the reader to the one place the record actually lives.
Before deleting an argument, check the log carries it. If it does not, put a
dated line there first.

## The four things a passage must survive with

*These apply to decisions still in force, still contested, or not yet acted on.
A closed one is governed by the rule above.*

Before rewriting anything, find these in the original. If your rewrite has lost
one, it is wrong however much shorter it is.

1. **The decision, and its date.** "Flipped to the live domain 2026-08-06."
   Dates are how a reader tells current reasoning from superseded reasoning.
2. **The constraint that stops it being reopened.** Not the conclusion — the
   thing that makes the conclusion non-obvious. "A stale `sameAs` is not a
   broken link, it is a false statement." Without that sentence, the next
   session sets the value and feels helpful.
3. **The falsifiable condition still outstanding.** "Nobody has confirmed mail
   *from* this address passes DMARC." These are the highest-value sentences in
   the repo: they are the difference between a thing that works and a thing that
   has merely been decided, and they are invisible from the outside.
4. **Who decided it, where a person chose.** "Round numbers, decided by the
   owner 2026-08-05." An owner's decision is not a candidate for revision by an
   assistant tidying up.

## What goes

- **Restated context.** The paragraph that explains the situation, followed by
  the paragraph that explains the same situation before making the point.
- **The second example.** Two illustrations of one idea; keep the better one.
- **Narration of structure.** "The short version is", "what follows is",
  "as discussed above" — unless the pointer genuinely saves a reader a search.
- **Hedging that carries no information.** "Arguably", "it is worth noting
  that", "in some sense". If a claim is uncertain, say what would settle it —
  that is a falsifiable condition and it stays.
- **Throat-clearing before the claim.** Move the claim to the front of the
  paragraph and much of what preceded it stops being needed.

## What never goes

- Anything in `ops/session-log.md`, `ops/audits/**` or `ops/rename-to-wardith.md`.
  Those files *are* the record. Length is the point.
- A `[PLACEHOLDER]`, or the sentence explaining what it is waiting for.
- The reason a value is null, empty or deliberately absent. Absence with no
  explanation reads as an oversight and gets "fixed".
- A statement about what the business will not do, and why. Those are the most
  frequently re-litigated lines in any repo.

## Worked example

From `site/src/data/business.ts`, the comment above `email`. Thirty lines,
carrying five distinct facts. Here it is at fourteen, with all five intact.

**Before** (abridged, the shape is what matters):

> **Flipped to the live domain 2026-08-06, once mail actually arrived.**
>
> This held `hello@novenstudio.co.uk` for two days after the site published as
> Wardith, deliberately: the value goes into the structured data and the contact
> page on *every* page, and it is the only inbound channel on a business with no
> phone and no contact form. A working address on the dead domain was a smaller
> fault than a bouncing one on the live domain, because an enquiry lost to a
> bounce is lost silently — nobody tells you.
>
> **The condition for flipping it was "the alias exists and a test message has
> arrived", and both were met before this changed.** The owner confirmed mail to
> `hello@wardith.co.uk` lands in the Zoho inbox, and the zone was read
> independently: MX to `mx.zoho.eu`, exactly one `v=spf1` record, a
> `zmail._domainkey` DKIM key, and DMARC `p=none` whose `rua` now points at a
> mailbox that exists. […]

**After:**

> **Flipped to the live domain 2026-08-06, once mail actually arrived.** Held
> the old address two days after the rename went live, deliberately: this value
> is the only inbound channel — no phone, no form — and it reaches every page
> and the structured data. A working address on the dead domain beat a bouncing
> one on the live domain, because an enquiry lost to a bounce is lost silently.
>
> Flipped only once the alias existed and a test message had arrived. Both
> confirmed: mail lands in Zoho, and the zone reads MX `mx.zoho.eu`, one
> `v=spf1`, a `zmail._domainkey` DKIM key, DMARC `p=none` with a live `rua`.
>
> `hello@novenstudio.co.uk` must keep receiving for twelve months — it is in the
> ICO record, on both LinkedIn pages and in whatever is cached. Alias, not a
> second user (`ops/rename-to-wardith.md` E3).
>
> **Still owed:** nobody has confirmed mail sent *from* here passes SPF, DKIM and
> DMARC at the far end. DNS present is not authentication passing, and a new
> domain that fails it is filtered silently — which looks exactly like nobody
> replying. Test: `ops/rename-to-wardith.md` D0.4 step 5.

Roughly 45% fewer words. Every decision, date, condition and outstanding test is
still there; what went was the second telling of each one.

## Deduplicating across files

When the same fact is written in several places, do not simply delete the
copies — a reader arriving at the wrong file needs to get somewhere.

- Pick the file that **owns** the fact. Usually the one whose subject it is.
- Leave a one-line pointer in the others: what it says, and where it lives.
  A pointer that only says "see X" makes the reader open X to find out whether
  they needed to.
- If three entry points repeat a banner on purpose so no reader misses it, keep
  it — but keep it byte-identical, and note in each copy that it is a copy.

## Measure it

Report the saving as words before and after, per file. It is the only honest
way to say whether a condensing pass achieved anything, and it keeps the work
from drifting into rewriting for its own sake.

```
wc -w <file>          # before and after
```

If a file came down by less than about 10%, it probably did not need the pass —
say so rather than reporting motion as progress.
