# Condensing without losing the argument

The owner has asked for reasoning to be condensed, not only for duplication to
be removed. That is a sharper instrument than it sounds, because the reasoning
in this repo is doing a job: it stops a future session reopening a question that
was already settled, and it records conditions nobody has met yet. Cut the wrong
sentence and the repo forgets why, which is the one failure mode that compounds.

So: cut words, keep facts. This document is the method.

## A closed decision keeps almost nothing

*Sharpened by the owner 2026-08-08, and it is the most aggressive rule here.*

When a decision is **made** — the supplier is chosen, the name is settled, the
option is picked — the comparison that produced it has no further job. Delete
it. Not "condense": delete. A reader who will never reopen the question gains
nothing from the case against the option that lost, and pays to read it every
time.

**A comparison closes when the choice is made, not when the money moves.** This
is the distinction that lets dead weight survive, so read it twice. "We are
buying UK Postbox's Street Address, £12/month" kills the case against V LOT and
Icon Offices *the moment it is written*, whether or not the card has been
charged. The purchase being outstanding keeps the **task** live; it does not
keep the **argument** live. Three paragraphs on rejected providers sat under an
unticked box for a week for exactly this reason — the box being unticked read
as "still open", when the only thing still open was an errand.

Ask which of these an unfinished item is:

- **The choice is still open** — two options are genuinely still in play, or the
  owner has not chosen. Keep the comparison; that is what rule two below governs.
- **The choice is made, the errand is outstanding** — keep what the errand needs
  (what to buy, what it costs, the traps, the runbook it lives in) and delete
  the comparison entirely. This is the common case and the one most often got
  wrong.

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
it.** `ops/session-log.md` is the archive of why, and git holds every prior
version besides. Stripping a live document is not destroying the record — it is
moving the reader to the one place the record actually lives. Before deleting an
argument, check the log carries it. If it does not, put a dated line there first.

**And the log itself is trimmed on the same rule, which makes the pointer a
dependency rather than a courtesy.** It was cut from 3,539 lines to 1,430 on
2026-08-08; entries whose decision is settled *and* recorded elsewhere go, and
entries a live document points at by date stay for that reason alone. So when
you strip an argument out of a live file and send the reader to the log, **write
the dated pointer** — it is what marks that entry as load-bearing and stops the
next trim taking it.

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

- **Narrative colour.** Sentences that editorialise a decision — its weight, its
  irony, its cost, who has to live with it — without stating a fact, a
  constraint or an outstanding condition. They read as the most serious writing
  on the page, which is why they survive pass after pass, and they are the
  purest waste in the repo: nobody's next action changes because they were read.

  The tell is that you cannot answer "what would I do differently?" from the
  sentence. Real examples, all deleted from `ROADMAP.md` §1c:

  > the cost of the decision, and the owner's to carry

  > both weaker than nine visible pages were

  > which is the exact fault the product finds on other people's

  The last one is the hardest to part with, because it is *true* and it is
  well-made. It is still a rhetorical flourish about a decision already taken.
  If a point like it is genuinely load-bearing — a standing rule the business
  works by — it belongs in `CLAUDE.md` as a rule, stated once, not in a
  roadmap item as a reflection.

  **Where this rule stops.** Colour describes a decision; a constraint governs
  the next one. "Never the home address — the footer can be edited, indexes and
  archives cannot" *is* a constraint on all future action and stays, in full.
  When unsure, ask whether deleting the sentence could let someone do the wrong
  thing later. If yes, it is a constraint. If it would only make them feel less,
  it is colour.

- **Justification of an executed decision.** Once a thing is done and nobody is
  proposing to undo it, the case for having done it is history — it goes to
  `ops/session-log.md` and out of the live document. What stays is the state it
  left behind and any commitment it created. The footer-placeholder removal ran
  to ten lines of justification in `ROADMAP.md` for a change the owner made,
  agreed with, and had already shipped.

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

  **This protects the rule, not the passage around it.** "Never the home
  address, because indexes and archives cannot be edited" is the protected
  thing, and it survives at that length. The three paragraphs of history that
  happened to precede it are not covered by this bullet and are governed by
  everything above. A rule buried in narrative is also easier to miss than a
  rule standing alone, so cutting the narrative usually strengthens it.

- A commitment with no date, in place of a completed task. "The address is
  published before the first customer is onboarded" is the only thing standing
  between an unticked box and a legal duty going unmet. It is a falsifiable
  outstanding condition (rule 3) and it is the last line anyone should cut.

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

## Worked example 2 — an unfinished item carrying a finished argument

*Added 2026-08-08, from `ROADMAP.md` §1c. This is the pattern the rules above
were sharpened to catch, and it survived a full condensing pass before them.*

311 words on an unticked checkbox, of which the errand needed about 60. It
looked live because the box was unticked; almost all of it was closed.

**Before** (abridged — the three trailing paragraphs are the point):

> - [ ] **Address for service of documents — not bought. Buy UK Postbox's
>       Business Street Address, Poole, £12/month inc VAT.** […]
>
>       **The comparison is closed** — V LOT took payment ~29 July and delivered
>       nothing (refund requested); Icon Offices was rejected on the numbers; the
>       two best-reviewed providers are annual-only and the owner needs monthly
>       or quarterly billing. […]
>
>       **The footer placeholder was removed 2026-08-06 by the owner, reversing
>       this instruction.** It had published the literal token `[PLACEHOLDER`,
>       named an internal repo file, and stated in writing on all nine pages that
>       a legal disclosure requirement was unmet — a red flag handed to a
>       prospect by the business's own site, which is the exact fault the product
>       finds on other people's. **What replaces it is a commitment, not a tick:
>       the address is published before the first customer is onboarded.**
>       Nothing takes a payment yet, which is what makes that defensible. The
>       reminder is now a comment in `Base.astro` and this paragraph, both weaker
>       than nine visible pages were — the cost of the decision, and the owner's
>       to carry.
>
>       **Never the home address.** This site is built so crawlers read the
>       business facts and repeat them confidently, which works against us on
>       this field, and it is a one-way door: the footer can be edited, indexes
>       and archives cannot.

Reading it against the rules:

| Passage | Verdict |
|---|---|
| What to buy, price, the PO Box trap, "don't tick until post arrives" | **Keep** — the errand and its outstanding condition |
| The V LOT / Icon Offices comparison | **Delete** — choice made 2026-08-07; `third-party-services.md` B1a–B1b owns it, refund included |
| Why the footer placeholder was removed | **Delete** — executed, uncontested; the log and the `Base.astro` comment both carry it |
| "the address is published before the first customer is onboarded" | **Keep** — outstanding condition, and the only thing holding a legal duty open |
| "both weaker than nine visible pages were", "the owner's to carry" | **Delete** — colour |
| "which is the exact fault the product finds on other people's" | **Delete** — colour, and true, and a rule that belongs in `CLAUDE.md` if it belongs anywhere |
| "Never the home address" + the one-way-door reason | **Keep** — constraint on all future action |

**After:**

> - [ ] **Address for service of documents — not bought. Buy UK Postbox's
>       Business Street Address, Poole, £12/month inc VAT.** Trading under a
>       business name as a sole trader carries a legal duty to show a name and
>       an address where documents can be served, including on the website. A
>       virtual office satisfies it. **Buy the *Street* address, not their
>       cheaper Business PO Box — a PO Box is not a valid address for this.**
>       Don't tick this off until post through the address is confirmed working.
>       Runbook — both traps, the ID check, the order the downstream work happens
>       in — is `ops/third-party-services.md` B1c. The provider comparison is
>       closed in B1a–B1b, along with the V LOT refund still outstanding; don't
>       reopen it.
>
>       **The footer carries no address, and what stands in its place is a
>       commitment: it is published before the first customer is onboarded.**
>       Defensible only while nothing on the site takes a payment. The reminder
>       is a comment in `Base.astro`.
>
>       **Never the home address.** The footer can be edited; indexes and
>       archives cannot, and this site is built so crawlers repeat its business
>       facts confidently.

311 → 185 words, 40% off. Every instruction, trap, condition and constraint is
still on the page; what left was one closed comparison, one justification of a
change already shipped, and four sentences of colour.

**The transferable tell:** an item whose *first* paragraph is an instruction and
whose *remaining* paragraphs are all history. Scan for that shape. The box being
unticked says the errand is open; it says nothing about the argument.

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
