# What each level actually is

**Internal document.** Decides what we deliver at each price, how long each one
is allowed to take, and why a client would move up. Written 2026-07-28.

**Status: proposed, not live.** The copy in section 4 has not been applied to the
site. Nothing here is committed until the owner says so.

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

"Faster pace and broader coverage" — the current Lead wording — is not a verb. A
client cannot self-select against it, which means every upgrade becomes a
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

**The question counts roughly double at each step.** That is a number a business
owner understands instantly, it maps directly to our real costs in both API
calls and time, and it is honest — unlike "faster pace", it can be checked.

---

## 4. Proposed copy

Not yet applied to the site. Two versions of each, because the visible copy and
the machine-readable description come from the same source and must agree —
`business.ts` feeds both the pricing page and the structured data.

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

### Files this touches, if approved

1. `site/src/data/business.ts` — the three `schemaDescription` fields, and the
   `summary` fields if we want those to match the new verbs
2. `site/src/pages/pricing.astro` — the three `.level` descriptions and the
   "Ongoing" intro paragraph
3. `site/src/pages/faq.astro` — **check before editing.** Anything in the `faqs`
   array is published into the FAQPage structured data as well as the visible
   page, so a half-updated answer gets repeated by the assistants themselves.
4. `site/src/pages/how-it-works.astro` — check for any description of what the
   monthly plans include

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
is a communication skill, not a technical one. Nearly ten years of operations at
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
  audit.
- **Whether Lead's fortnightly checking is worth the doubling of effort**, or
  whether the quarterly competitive review alone carries the tier. Fortnightly
  doubles our query volume and our time for a benefit the client may not feel.
- **[PLACEHOLDER: owner to decide]** whether the answer pages at Grow and Lead
  are written by us and published by the client, or published by us directly.
  That changes the access we need and the time each page takes, and it is the
  same open question roadmap 3b raises about client website access.
