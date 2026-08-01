# What each level actually is

**Internal document.** Decides what we deliver at each price, how long each one
is allowed to take, and why a client would move up. Written 2026-07-28.

**Status: live as of 2026-07-28.** The copy in section 4 is applied to the
site. The question counts and time budgets remain estimates until the first
delivery is timed — see section 8.

This closes the open item in roadmap 3c — "define what actually happens each
month at each level, concretely enough that a client would recognise the value."

---

## 1. Where we sit in the market

Researched 2026-07-28. Confirm before quoting any of it publicly.

| | Monthly price |
|---|---|
| UK local search agencies, entry package | ~£395 + VAT |
| UK local search agencies, typical small-business client | £500–£1,500 |
| Agencies doing AI-assistant visibility work | $1,500–$10,000, entry retainers $2,000–5,000 |
| **Noven Maintain** | **£95** |
| **Noven Lead** | **£495** |

**We are still well under the UK market floor at Maintain, and Lead now sits at
roughly the cheapest agency's entry package rather than a third of it** —
against a deliverable of two permanent pages a month, which an entry package
does not include. Repriced 2026-07-31; see section 9.

This is a position, not a mistake. It serves the businesses agencies have priced
themselves out of — the sole-trader trades, the two-partner firms, the
independent clinics who will never spend £400 a month on marketing. Nobody is
serving them, and they are the businesses most likely to be invisible to an
assistant in the first place.

**But it means agency tier logic does not transfer.** An agency separates its
tiers by how many hours of expensive human work go in, because a client paying
£1,500 can absorb a £1,000 step. Our client is weighing a monthly fee against a
phone bill. We cannot sell more hours at these prices — there aren't enough hours
in a month to service twenty clients that way.

So our levels are separated by **how many permanent answer pages each one
produces**, and only secondarily by how many questions we track. Section 9
explains why that replaced separating them by question volume, which was the
original design and was quietly charging us more per pound at every step up.

---

## 2. The three verbs

Each level is a different thing the client wants, not more of the same thing.

| Level | Verb | What the client is buying |
|---|---|---|
| Maintain | **Hold** | Stop the Foundation decaying. Stay where you are. |
| Grow | **Expand** | Close the gaps — show up for questions you currently miss. |
| Lead | **Compete** | Be named *instead of* the competitors currently named ahead of you. |

"Faster pace and broader coverage" — the wording Lead used to carry — is not a
verb. A client cannot self-select against it, which means every upgrade becomes a
conversation we have to have. Hold, expand, compete can be chosen from the page
without asking us anything.

---

## 3. What we deliver, and what it may cost us

**The time figures are estimates and are not yet validated.** Roadmap 3a and 3b
both say to do the first one end to end and time it. Do that before treating any
number below as real.

### Maintain — £95/month

- **10 questions** tracked, chosen with the client from what their customers
  actually ask
- Asked **5 times each, monthly** — by API on ChatGPT, Gemini and Perplexity,
  and by hand on Copilot and Google's AI Overviews at the reduced sample
  `ops/audit-method.md` section 2 sets. **Not "across the four assistants"**,
  which is what this file used to say and which the method has never supported:
  taken literally it meant 100 manual lookups per client per month.
- Business facts kept current in the structured data as the business changes
- Drift fixed when facts go stale or go wrong
- A **one-page written record** — the format is
  `ops/monthly-record-template.md`

**Time budget: about 1 hour a month after setup. This is the number that decides
whether the business works** — see section 6.

**What it deliberately does not include:** closing any of the gaps it reports.
Maintain tells you where you're missing. It doesn't fix it. That is not a
withheld feature, it's the honest boundary of what £95 buys, and it is also the
upgrade engine (section 5).

### Grow — £250/month

- Everything in Maintain, across **15 questions** instead of 10
- **One new answer page per month**, written properly and published on the
  client's own site, chosen from the gaps the record identified

**Time estimate: 3–4 hours a month.**

### Lead — £495/month

- Everything in Grow, across **25 questions**, checked **monthly**
- **Two answer pages per month**
- **A quarterly written review** naming the competitors the assistants put ahead
  of the client, and an honest read on why

**Time estimate: 6–7 hours a month.**

**Lead's fortnightly cadence was removed on 2026-07-31**, along with the drop
from 50 questions to 25. Fortnightly checking of 50 questions is roughly 1,500
runs a month — an estimated 13–23 hours for £250, which made the premium tier
the worst-paid work in the business. Section 8 of this file had already flagged
the cadence as an open question while the site sold it as a firm commitment.
Nobody had bought Lead, so the change cost nothing.

### What an answer page actually is

Decided 2026-07-28, because "answer page" was doing a lot of undefined work.

**It is not a blog post.** A blog post is dated, sits in a feed, and gets buried
by the next one. Its value decays and the client's site slowly accumulates a
graveyard.

**It is not an FAQ entry.** An FAQ entry is one short answer among twenty on a
single page, which leaves that page strongly *about* nothing. An assistant asked
a specific question has to pull a fragment out of a list.

**It is one question, one permanent page, one URL.** The heading is the question
or close to it. The body answers it properly, using facts only that business has
— its prices, its areas, its timescales, what is actually included. Undated, and
linked from the part of the site it belongs to rather than from a feed.

This is not a new product. It is the Foundation's fourth bullet — *"writing or
restructuring key pages so they directly answer the questions your customers
ask"* (`how-it-works.astro`) — continued one page a month. **Every Foundation we
deliver is practice for Grow.**

Our own site is the working example: no blog, and every page heading is a
customer question. *How does Noven get you found? What does Noven cost? Why does
the audit cost £125?*

**The guard rail.** Two pages a month at Lead is twenty-four pages a year, which
can sprawl into thin filler that actively hurts. The test: if we cannot write
around 400 words of genuinely specific content *that only this business could
write*, it is not an answer page — it is an FAQ line. Put it there and move to
the next gap.

**Where the time actually goes:** not the writing. Verifying the facts with the
client before publishing, because the no-invented-facts rule in `CLAUDE.md`
binds hardest here. That is what makes a page two to three hours rather than
one.

### Who publishes it — we do

Decided 2026-07-28. **We publish directly. The client approves the words; we
publish them.** The site already promises this shape of arrangement — the FAQ
says *"You will not need to write anything yourself unless you want to."*

The argument that settles it: **structured data does not survive copy-paste.**
The JSON-LD, the heading hierarchy and the internal links are stripped the
moment a client pastes our text into a visual editor. What lands on their site
is prose with the product removed. We would have to verify it afterwards
regardless, so the client-publishes path costs *more* of our time, not less, and
delivers a worse page. It is also the exact mechanism by which facts drift,
which is the one failure this business cannot have. Add to that the delivery
risk: a £250/month deliverable sitting unpublished in someone's inbox for three
weeks is a level that visibly fails.

The honest arguments the other way, recorded because they shape how we ask:

- **Foundation access and ongoing access are different asks.** Foundation access
  can be a one-off afternoon. Publish rights held for a year is materially
  bigger, and some who say yes to the first will say no to the second.
- **Credential hygiene at twenty clients.** Live admin logins to twenty small
  business sites is a real security surface, and several will hold customer
  enquiry data — which pulls on the ICO obligations in roadmap 1c.
- **Blame attaches to whoever touched it last.** If their site breaks the week
  after we publish, for unrelated reasons, we own it in their mind. Professional
  indemnity cover handles the money, not the relationship.
- **Some sites will not allow it** — franchise templates, trade-body site
  packages, agency-managed sites that redeploy from a master and would silently
  wipe the page.
- **Regulated clients cannot let us** — clinics, financial advisers, solicitors
  often have change-control duties over anything published in their name.

So the decision comes with two things built around it:

1. **A named fallback, written into onboarding.** Where we cannot get publish
   rights, we supply the page as a complete file with the structured data
   intact, plus a one-page paste instruction, and we verify it live afterwards.
   That verification is billable time inside the plan, not a favour.
2. **Access asked for in two stages.** The Foundation asks for access *to do the
   setup*. Taking a monthly plan is where we ask to keep it. Separating them
   means a "no" to the second does not threaten the first.

**The question counts roughly double at each step.** That is a number a business
owner understands instantly, it maps directly to our real costs in both API
calls and time, and it is honest — unlike "faster pace", it can be checked.

---

## 4. Where the published copy lives

**This section used to transcribe the live site copy in full. It no longer
does** (changed 2026-07-31). Two copies of the same sentences in two files is
the mechanism by which documentation goes stale, and the repricing proved it —
every quoted block here was wrong within an hour of the site changing. The site
is the canonical text. This section says where it is and what must stay true
about it.

**The one rule that matters:** the visible copy and the machine-readable
description come from the same source and must agree. `business.ts` feeds both
the pricing page and the structured data. **Change a level in one place and
change it in all of them**, or a client and an assistant end up being told
different things, which is the one failure this business cannot have.

### Where this copy lives

1. `site/src/data/business.ts` — the three `schemaDescription` fields. **Done.**
2. `site/src/pages/pricing.astro` — the three `.level` descriptions and the
   "Ongoing" intro paragraph. **Done.**
3. `site/src/pages/how-it-works.astro` — the sentence summarising the three
   levels in stage 03. **Done.**
4. `site/src/pages/faq.astro` — checked, no change needed. No FAQ answer
   describes what a level includes; the only mention is that moving between
   levels works like cancelling. **Keep it that way** — anything written into
   the `faqs` array is published into the FAQPage structured data as well as the
   visible page, so a level description added there is a third place that can
   drift out of step.

Verified after the change: the build is clean at 7 pages, all JSON-LD parses,
and both homepage code panels are still byte-identical to the JSON-LD in the
head — the property the homepage's whole argument rests on.

---

## 5. Why a client moves up

**The monthly record is the upgrade prompt, and it is honest.** No selling is
required and none should be done.

**Maintain → Grow.** The Maintain record says, every month, which questions the
client is missing from. It reports the gap and does not close it. A client reads
the same unclosed gap thirty days running. Some are content to hold position —
that is a perfectly good outcome and we should not treat it as a failure. Some
get irritated and ask us to fix it. The report told the truth either way.

**Grow → Lead.** A different trigger, and a stronger one: **a named competitor.**
"For your most valuable question, the assistants named three other firms and not
you" is the sentence that moves someone from £250 to £495. It is not about
volume, it is about a rival. This is why the competitive review belongs at Lead
and nowhere else — it is the only thing at that price that isn't just more.

**Do not expect fast upgrades.** Some clients move in months, some in years, some
never. The published pattern is that offering an upgrade path retains clients
**40–60% longer even when nobody upgrades** — so the tiers earn their keep
through retention, not conversion. Judge them on that.

---

## 6. The arithmetic that decides whether this works

**Maintain will dominate early.** Plan for it rather than hoping otherwise.

Twenty Maintain clients is £1,900 a month. Reaching £3,000 on Maintain alone
means thirty-two clients, and thirty-two relationships is more than one person
holds well — the commonly cited ceiling for a solo operator is four to eight
clients at agency scope, and even at our much lighter scope thirty-two is a
stretch. **This is the arithmetic the repricing was mostly for:** the old £75
needed forty clients for the same figure.

Two things follow, and they change what to work on.

**The Foundation is the income in year one, not the monthlies.** At £750, one
Foundation is nearly eight months of a Maintain client's revenue delivered in one
go. Five Foundations is £3,750. Early on this is a project business with a
subscription tail. **So converting audits into Foundations matters more in year
one than converting Maintain clients into Grow clients** — that's where the
effort should go, and it is a different activity from upselling.

**Maintain's delivery time is the single number that decides the ceiling.** At
one hour a month it scales to twenty-plus clients. At three hours it caps the
business at eight and there is no growth without a further price rise.

So **systematise Maintain from client one.** Same questions, same format, same
record, every time — the format is `ops/monthly-record-template.md` and it exists
so that this can actually be done. Resist doing anything bespoke inside it. That
is not corner-cutting — it is the only thing that makes £95 possible at all.
Anything genuinely bespoke a client wants is a reason to talk about Grow, not a
reason to quietly do it for free.

---

## 7. Why this order suits a novice operator

Worth writing down because it is true and it affects sequencing.

**Maintain is a checklist.** Run the questions, compare to last month, fix what
drifted, send the record. Deliverable competently from client one, and doing it
twenty times is how the pattern recognition gets built.

**Grow is writing.** Producing a clear page that answers a real customer question
is a communication skill, not a technical one. Eight years of operations at
Maersk is better preparation for "state this business's facts accurately and
consistently" than most marketing backgrounds are.

**Lead needs judgment** about *why* an assistant favours a competitor. That is
the hard one — and nobody buys it in month one. By the time someone does, we will
have done twenty-odd audits.

**The levels are sequenced roughly in the order the owner will become good at
them.** That is lucky, and it is a reason not to disturb the structure.

---

## 8. Decisions still open

- **Closed 2026-07-31 — question counts.** Now **10 / 15 / 25**, replacing
  10 / 25 / 50. Doubling was easy to say out loud and was the wrong axis: it
  doubled our cost per step while adding little the client could feel. See
  section 9.
- **Run count.** Five runs per question is what the variance research implies is
  the minimum honest number (see `ops/third-party-services.md`, section E3). It
  may need to be higher for confidence, or lower for time. Validate on the first
  audit. **The experiment is now specified** in `ops/audit-method.md` section 8:
  during the Noven self-audit, take three questions to ten runs instead of five
  and see whether the reported band moves. If it holds, five is validated and
  this item closes. If it moves, five is too few — and that changes the cost and
  the time budget of every monthly plan, not just the audit.
- **Reporting five runs as a band, not a percentage** (decided 2026-07-30,
  `ops/audit-method.md` section 4). It applies to the monthly record as much as
  to the audit, and it is what stops a client reading noise as a decline in
  month three. The published copy says "five times each" and is unaffected.
- **Closed 2026-07-31 — Lead's fortnightly checking.** Removed. It doubled our
  query volume and our time for a benefit the client could not feel, and it made
  the premium tier the worst-paid work in the business. Lead is monthly.
- **Closed 2026-07-28 — who publishes the answer pages.** We publish directly,
  with a defined fallback where we cannot get access. Full reasoning in section
  3, along with what an answer page is. Left as a pointer here because this file
  and roadmap 3b/3c both carried it as open. What remains is build work, not a
  decision: write the fallback into onboarding, and split the access request
  into two stages.
- **Found while applying the copy:** every plan in `business.ts` carries a
  `summary` field, documented as "used in the record panels", and **nothing
  reads it.** Left alone rather than churned — the existing values still fit the
  new framing — but it is either dead code to delete or a panel someone intended
  and never built. Worth five minutes next time that file is open.

---

## 9. The repricing — 2026-07-31

**What changed.** Audit £30 → **£125**. Foundation £350 → **£750**, with the
scope fixed. Maintain £75 → **£95**, Grow £125 → **£250**, Lead £250 → **£495**.
Question counts 10 / 25 / 50 → **10 / 15 / 25**. Lead's fortnightly checking
removed. Confirmed by the owner before the copy was applied.

### The finding that forced it: the ladder was inverted

Price against the estimated true effort — the estimates are from documented step
counts, not measurement, and the self-audit replaces them:

| Product | Old price | Est. hours | Est. £/hour |
|---|---|---|---|
| Audit | £30 | 2.5–3.5 | £9–12 |
| Foundation | £350 | 10–20 | £17–35 |
| Maintain | £75/mo | 1.8–2.8 | £27–42 |
| Grow | £125/mo | 4.5–7 | £18–28 |
| Lead | £250/mo | 13–23 | £11–19 |

**Every step up earned less per hour than the one below it.** Lead — the premium
tier — paid roughly the same as the loss leader. Success at selling made the
business worse, which is not a pricing level problem. It is a pricing *axis*
problem: the tiers were separated by question volume, and question volume is
pure cost to us with no leverage. Selling more of it sold more of the owner's
hours at a discount.

### The fix: price on answer pages, not questions

A page is a permanent asset that keeps working after it is written. Twenty-five
extra questions is a longer spreadsheet. So the tiers now separate on pages
(0 / 1 / 2 a month), question counts rise gently rather than doubling, and each
step up pays more per hour than the last. Section 5's upgrade logic is
unaffected and arguably strengthened — the trigger for Grow → Lead was never
volume, it was a named competitor.

### Why the audit went to £125 rather than staying a loss leader

Three reasons, in order of weight:

1. **Price is a quality signal where the buyer cannot judge the product in
   advance.** £30 for a bespoke report reads as automated. The barrier at £125
   is trust, not money, and trust is answered by the sample audit and a plain
   refund line — not by a low number.
2. **It selects the wrong buyer.** The audit's job is to convert to a Foundation.
   A £30 buyer is not the same person as a £750 buyer.
3. **It consumed the scarcest resource in the business.** At an estimated 2.5–3.5
   hours, thirty-three audits a month — the volume needed to reach £1,000 —
   is ~53 hours of near-minimum-wage work.

The pricing page section that asked *"Why is the audit only £30?"* is now
*"Why does the audit cost £125?"* and answers it with the method: repeated runs,
verbatim quotes, competitors named, read by a person.

**No founding rate.** Considered and declined by the owner. Launching flat at
the new prices avoids running a discount game on a brand built on plain dealing.

### Why the Foundation had to be capped as well as raised

`how-it-works.astro` promised "writing or restructuring key **pages**" — plural,
unbounded — and no time budget for the Foundation existed anywhere in this repo.
Raising the price without fixing the scope would have raised the ceiling on an
open-ended commitment. The scope is now four fixed pieces of work, of which the
fourth is **two** answer pages, and the page says so. If the audit finds work
outside those four, we say so rather than absorbing it.

### The bundle that was proposed, applied, and backed out the same day

**Proposed:** the Foundation included free with twelve months of Grow — £750
given away against £3,000 committed, converting a one-off buyer into a
subscriber without discounting the standalone price.

**Why it was wrong, and it is worth recording rather than quietly deleting:
nothing commits anyone to twelve months.** The monthly plans roll month to month
with no minimum term, and that is published in four places — `faq.astro` ("Am I
locked into a contract?" "No."), which feeds the FAQPage structured data;
`pricing.astro` and `how-it-works.astro` in the cancellation paragraph; and the
pricing page's own meta description, which ends "No lock-ins."

So the offer as written let a client take the £750 Foundation, pay £250 for one
month of Grow, and cancel before the next payment date — £1,000 of work for
£250, entirely within our published terms. The "£3,000 committed" figure was
simply false. **The cancellation policy is the older and better-argued decision
(roadmap 1a) and it wins.**

**Backed out of the site and this document on 2026-07-31**, the same day it went
in. The lesson generalises: any offer phrased as "for N months" is incompatible
with no-minimum-term, and the terms are not the thing to bend.

### Standing decision: we do not bundle services — 2026-07-31

**Settled by the owner. Not an open question, and not to be reopened by a future
session looking for a way to lift conversion.**

Every product is bought and priced on its own. No combined offers, no "free with",
no discount for taking two, no minimum-term-in-exchange-for-something. Alternatives
were put forward — crediting the Foundation back monthly, a half-price first three
months — and **all of them were declined.** The question was not which bundle to
run. It was whether to bundle at all, and the answer is no.

**Why it holds up, beyond being the owner's call:**

- **It is the only version that needs no asterisk.** Every bundle discovered so
  far ends in a qualification on the cancellation terms, and those terms are
  published in four places including the structured data. A business whose
  product is machine-readable accuracy should not have a pricing page that needs
  a footnote.
- **The prices are already the argument.** Section 9 repriced each product to
  stand on its own effort. A discount for combining says the standalone price was
  soft, which is exactly the impression the repricing was meant to remove.
- **The upgrade engine is the monthly record, not an offer** (section 5). The
  record reports gaps it does not close. That is what moves a client up a tier,
  and it works without anyone selling anything — a bundle would be doing a job
  that is already done.
- **One person cannot service a promotion.** Anything with a window, a
  qualifying period or a clawback needs tracking per client, and the client
  record has no column for it because it should not need one.

**What this rules out in practice**, so it does not get re-litigated in pieces:
Foundation-with-a-plan offers, first-month-free, annual-payment discounts,
introductory or founding rates (already declined separately), referral discounts,
and any "N months for the price of M". A client who buys more pays more.

The only combination that remains, and it is not a bundle: **the tiers are
cumulative by design** — Grow contains Maintain, Lead contains Grow. That is one
product at three sizes, priced accordingly, and it is what section 2 means by
three verbs.

### Why now, before the first client

Because it is free now and expensive later. Nobody has bought anything, so there
is no client to upset and no invoice to amend. The monthly plans have no minimum
term by design (roadmap 1a), which means a later price rise on existing clients
is a churn event with nothing holding them. Launch prices are the only prices
that can be set without cost.

**Still true and still the constraint:** these prices work only if delivery cost
matches them, and delivery cost is currently an estimate. The self-audit
(`ops/audit-setup.md`) produces the real numbers. If Maintain turns out to take
three hours rather than one, this section gets rewritten, not defended.
