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
| **Noven Maintain** | **£75** |
| **Noven Lead** | **£250** |

**We are roughly a fifth of the UK market floor, and Lead is still cheaper than
the cheapest agency's entry package.**

This is a position, not a mistake. It serves the businesses agencies have priced
themselves out of — the sole-trader trades, the two-partner firms, the
independent clinics who will never spend £400 a month on marketing. Nobody is
serving them, and they are the businesses most likely to be invisible to an
assistant in the first place.

**But it means agency tier logic does not transfer.** An agency separates its
tiers by how many hours of expensive human work go in, because a client paying
£1,500 can absorb a £1,000 step. Our client is weighing £125 against a phone
bill. We cannot sell more hours at these prices — there aren't enough hours in a
month to service twenty clients that way.

So our levels are separated by **how much of the owner's time each one is allowed
to consume**, by design.

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

### Maintain — £75/month

- **10 questions** tracked, chosen with the client from what their customers
  actually ask
- Asked **5 times each, monthly**, across the four assistants
- Business facts kept current in the structured data as the business changes
- Drift fixed when facts go stale or go wrong
- A **one-page written record**: where you appeared, what changed since last
  month, which questions you are still missing from

**Time budget: about 1 hour a month after setup. This is the number that decides
whether the business works** — see section 6.

**What it deliberately does not include:** closing any of the gaps it reports.
Maintain tells you where you're missing. It doesn't fix it. That is not a
withheld feature, it's the honest boundary of what £75 buys, and it is also the
upgrade engine (section 5).

### Grow — £125/month

- Everything in Maintain, across **25 questions** instead of 10
- **One new answer page per month**, written properly and published on the
  client's own site, chosen from the gaps the record identified

**Time estimate: 3–4 hours a month.**

### Lead — £250/month

- Everything in Grow, across **50 questions**, checked **fortnightly**
- **Two answer pages per month**
- **A quarterly written review** naming the competitors the assistants put ahead
  of the client, and an honest read on why

**Time estimate: 7–8 hours a month.**

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
customer question. *How does Noven get you found? What does Noven cost? Why is
the audit only £30?*

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
risk: a £125/month deliverable sitting unpublished in someone's inbox for three
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

## 4. The copy, as published

Applied to the site on 2026-07-28. Two versions of each, because the visible copy
and the machine-readable description come from the same source and must agree —
`business.ts` feeds both the pricing page and the structured data. **Change a
level here and change it in both places**, or a client and an assistant end up
being told different things, which is the one failure this business cannot have.

### Pricing page — the intro to the "Ongoing" block

Current wording, with one sentence sharpened to name the three verbs:

> The assistants change constantly, so staying visible is maintenance, not magic.
> All three levels are the same service at different intensities — hold your
> position, close the gaps, or lead your field — and you can move between them at
> any time. Each one includes everything above it.

### Pricing page — the three levels

**Maintain**

> Holds the position the Foundation built. Every month we ask the assistants ten
> questions your customers actually ask — five times each, because their answers
> vary — and send you a short written record: where you appeared, what changed
> since last month, and which questions you're still missing from. Your business
> facts stay current, and we fix them when they drift.

**Grow**

> Everything in Maintain, across twenty-five questions instead of ten. Each month
> we take one of the questions you're missing from and write the page that
> answers it properly, on your own site. That's how you go from showing up
> sometimes to showing up for the things people actually ask.

**Lead**

> For businesses that want to be the first name mentioned, not just a name
> mentioned. Fifty questions, checked every two weeks, and two new answer pages a
> month. Every quarter you also get a written review of the competitors the
> assistants are naming ahead of you, and our honest read on why.

### `business.ts` — the `schemaDescription` fields

These are what an assistant reads. They have to stand alone without the
surrounding page, and they carry the price.

**Maintain**

> Monthly plan to hold your position: ten questions your customers ask, put to
> the AI assistants five times each every month, with a written record of where
> you appeared and which questions you are still missing from. Business facts
> kept current and corrected when they drift. £75 per month.

**Grow**

> Monthly plan to close the gaps: everything in Maintain across twenty-five
> questions, plus one new page each month answering a question you are currently
> missing from. £125 per month.

**Lead**

> Monthly plan for businesses that want to be the first name an assistant gives:
> fifty questions checked fortnightly, two new answer pages each month, and a
> quarterly written review of the competitors being named ahead of you and why.
> £250 per month.

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
you" is the sentence that moves someone from £125 to £250. It is not about
volume, it is about a rival. This is why the competitive review belongs at Lead
and nowhere else — it is the only thing at that price that isn't just more.

**Do not expect fast upgrades.** Some clients move in months, some in years, some
never. The published pattern is that offering an upgrade path retains clients
**40–60% longer even when nobody upgrades** — so the tiers earn their keep
through retention, not conversion. Judge them on that.

---

## 6. The arithmetic that decides whether this works

**Maintain will dominate early.** Plan for it rather than hoping otherwise.

Twenty Maintain clients is £1,500 a month. Reaching £3,000 on Maintain alone
means forty clients, and forty relationships is more than one person holds well —
the commonly cited ceiling for a solo operator is four to eight clients at agency
scope, and even at our much lighter scope forty is a stretch.

Two things follow, and they change what to work on.

**The Foundation is the income in year one, not the monthlies.** At £350, one
Foundation is nearly five months of a Maintain client's revenue delivered in one
go. Five Foundations is £1,750. Early on this is a project business with a
subscription tail. **So converting audits into Foundations matters more in year
one than converting Maintain clients into Grow clients** — that's where the
effort should go, and it is a different activity from upselling.

**Maintain's delivery time is the single number that decides the ceiling.** At
one hour a month it scales to twenty-plus clients. At three hours it caps the
business at eight and there is no growth without a price rise.

So **systematise Maintain from client one.** Same questions, same format, same
record, every time. Resist doing anything bespoke inside it. That is not
corner-cutting — it is the only thing that makes £75 possible at all. Anything
genuinely bespoke a client wants is a reason to talk about Grow, not a reason to
quietly do it for free.

**Not recommending a price change.** £75 is defensible as a deliberate position
in a segment agencies have abandoned. It works only if delivery cost matches it.

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

- **Question counts.** 10 / 25 / 50 is a proposal. It doubles cleanly and it is
  easy to say out loud. Not yet tested against how long the checking actually
  takes.
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
  month three. The published copy in section 4 above says "five times each" and
  is unaffected.
- **Whether Lead's fortnightly checking is worth the doubling of effort**, or
  whether the quarterly competitive review alone carries the tier. Fortnightly
  doubles our query volume and our time for a benefit the client may not feel.
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
