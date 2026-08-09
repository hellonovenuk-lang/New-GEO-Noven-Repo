# Cold outreach — how the first clients are found

**Status: Decided, unvalidated.** Written 2026-08-09. Nobody has been contacted.
Every number in the "what actually happens" section is a guess until a batch has
been sent, and is marked as one.

**Internal document.** Read `ops/audit-method.md` and `ops/audit-questions.md`
before running the assistant queries this depends on. Read
`ops/competitor-analysis.md` for why the finding in the email works.

---

## 1. The decision this document exists to record

**The owner has no business network, so the first clients are cold.** Settled
2026-08-09. Everything written before that date assumed warm introductions
first — `HANDOVER.md` step 6, `ROADMAP.md` 2c — and that route is closed, not
deferred.

**Target, settled the same day: private clinics on the Wirral.** Dental,
cosmetic, physiotherapy, veterinary. One trade, one area, per `ROADMAP.md` 2a.

Why this trade, in the order the reasons matter:

- **Almost all of them are limited companies**, which is a legal requirement of
  cold email rather than a preference. Section 2.
- **Their customers genuinely ask an assistant to recommend one.** "Best dentist
  near me", "Invisalign Wirral", "emergency vet Wirral" are real questions a real
  person types. A trade whose customers arrive by referral has nothing for us to
  find.
- **They already buy marketing**, so the £250 audit is a familiar kind of spend
  rather than a new category of one.
- **The Wirral is small enough that one assistant run covers the whole market**,
  which is the entire economic basis of section 4.

---

## 2. The legal frame — read this before building any list

*Not legal advice. It is the position this business is operating on, and it
should be checked.*

**Cold email is lawful to companies and unlawful to people.** Under PECR, limited
companies and LLPs are *corporate subscribers* and may be sent unsolicited
marketing email without prior consent. Sole traders and unincorporated
partnerships are treated as individuals and need consent we do not have.

**That turns the target definition into a filter, not a preference:**

> **Nobody is contacted unless Companies House shows a live limited company or
> LLP at that trading name.** No company number, no email.

This is free to check and it builds the list at the same time — see section 3.

**Three things every outreach email must carry**, all of them consequences of
the above rather than good manners:

1. **Who we are.** Wardith, the trading name, and the address for service.
2. **Where we got their details**, in one line. Under UK GDPR, when you hold
   someone's details from a source other than them you have to tell them, in
   practice at first contact.
3. **A working opt-out**, honoured permanently. A reply saying "don't contact me
   again" is the mechanism; we do not need an unsubscribe system for batches this
   size, we need a record that cannot be lost. See section 6.

**Two published pages are now blockers on the first email, not on launch.**

- **`/privacy/`** already carries the paragraph this needs — the "If we contact
  you first" section names legitimate interest and permanent opt-out recording.
  It does not publish, because it is waiting on the address for service and on
  the client-record storage decision (`ops/client-record.md`).
- **The address for service** is what points 1 and 2 above require. UK Postbox,
  £12/month, `ops/third-party-services.md` B1c. **Order it early:** identity
  verification usually clears within 24 hours and then post has to travel, so it
  is the one blocker here that cannot be closed on the day it is noticed.

**A warm route would have sidestepped both. Cold cannot.** This is the single
biggest cost of the change of plan and it is worth saying plainly: the first cold
email cannot be sent until `business.addressForService` and
`business.clientDataStorage` are set in `site/src/data/business.ts`. One edit
publishes both pages and fills the footer.

---

## 3. Building the list

**Source: Companies House, free, and the filter and the list are the same
operation.** Search by SIC code, then by registered-office postcode.

| Trade | SIC code | Confirm before trusting |
|---|---|---|
| Dental practices | 86230 | Yes |
| General medical practice | 86210 | Yes |
| Specialist medical practice | 86220 | Yes |
| Other human health activities — physio, chiropractic, podiatry | 86900 | Yes |
| Veterinary | 75000 | Yes |

**The codes above are from memory and must be checked against Companies House's
own list on the day.** A wrong code produces a list that looks right and is not,
which is exactly the failure this business is sold to find in other people's
data.

**Wirral postcodes: CH41–CH49, CH60–CH63.** CH64 is Neston, on the peninsula but
in Cheshire West, so it is a judgement call rather than an obvious yes. **Check
this list too** — a postcode district that turns out to be Chester puts the
"we're local" line in the email into an outright false claim.

**The registered office is not always the clinic.** Many use their accountant's
address. Match on trading address from the clinic's own website, and use
Companies House only to answer "is this a company".

**What we record per prospect** is in `ops/client-record.md` — the prospect
fields are already decided there. Do not invent a second schema.

**Size of the first batch: [PLACEHOLDER: how many Wirral clinics exist per
trade].** Unknown until the search is run, and it decides whether one trade is
enough or whether the first batch spans all four.

### What makes a good first client

Written now so it is not rationalised backwards after the first reply.

- **A limited company**, per section 2. Not negotiable.
- **Owner-run, or with a named person who can say yes.** A practice manager
  reporting to a group board is a long sale we cannot afford yet.
- **Has a website we can actually assess.** No site at all is a different
  product and a much harder conversation.
- **Not already visible.** If the assistants already name them first for their
  own trade, we have nothing to sell them and should say so rather than pitch.
- **On the Wirral**, so the first case study says something specific.

---

## 4. The pre-work — one run per trade, not one per business

**`ROADMAP.md` 2b says to run a mini audit on each prospect before contacting
them. That is right for warm and unaffordable for cold.** The self-audit's
recorded cost was **$12.63 on OpenAI alone for roughly 75 queries**
(`ops/audits/noven-2026-08-02/README.md`), so roughly $0.17 a query. A hundred
prospects at three questions each is real money during a spending freeze.

**The fix is better than the thing it replaces.** Ask the discovery questions
once for the *trade and area*, not once per business:

> "Who is the best dentist on the Wirral?"
> "I need an emergency dentist in Birkenhead, who should I call?"
> "Which Wirral dental practices do Invisalign?"

**One run answers the question for every clinic in the area at once.** For each
prospect it produces two facts, and the second one is the one that sells:

- whether they were named, and
- **which of their competitors was named instead of them, by name.**

`ops/competitor-analysis.md` established the mechanism on our own market: a third
of answers name nobody at all, and listicles carry most of the names. Being able
to tell a clinic owner which three practices come up ahead of them, with the
question that produced it, is a far sharper opening than "you are not mentioned".

**Cost of a batch run:** six questions, three assistants, five runs each is 90
queries, on the order of **$15 for the whole batch** rather than per prospect.
Derived from the one recorded figure above, so treat it as an order of magnitude.

**Use the frozen question rules in `ops/audit-questions.md`.** A trade run is not
a client audit and does not go in `ops/audits/`, but the wording rules are the
same, and a question that works here becomes part of the library that file
describes as the compounding asset.

**Never send the trade run to a prospect as if it were their audit.** It is one
finding, and the paid audit is ten questions on their own business. Blurring that
is how the £250 stops being worth paying.

---

## 5. The email

**One finding, one offer, no sequence.** No chasing email, no "just bumping this
up your inbox", no three-touch cadence. If the finding is not interesting enough
to answer once, sending it again does not improve it.

**Send in batches of ten to twenty**, so the wording can change based on what
comes back. `ROADMAP.md` 2b already required this and it survives the change to
cold.

**Draft, to fill in per clinic:**

> Subject: What ChatGPT says when someone asks for a dentist on the Wirral
>
> Hello [name],
>
> I asked ChatGPT, Google's Gemini and Perplexity who the best dentist on the
> Wirral is, a few different ways. [Practice A], [Practice B] and [Practice C]
> came up. [Their practice] did not, on any of the three.
>
> That is worth knowing because it is quietly becoming how people choose. It is
> also fixable, and not by doing more of whatever an SEO agency is already doing
> for you.
>
> I run a small business on the Wirral that does one thing: find out what the AI
> assistants say about a business, tell you exactly where the answer comes from,
> and give you the list of what to change. The audit is £250 and it is a fixed
> price. You get a written report and you can act on it yourself. Nothing is
> tied to a monthly plan.
>
> I have published one of these in full, run on my own business, findings and
> all: wardith.co.uk/ask-your-ai/self-audit/
>
> If it is useful, reply and I will send the questions I would ask about
> [practice]. If not, say so and I will not contact you again.
>
> [Owner name]
> Wardith, [address for service]
>
> I found your practice through Companies House and your website. If you would
> rather I did not hold your details, say so and I will delete them.

**What the draft is doing, so it is not edited into a pitch by accident:**

- **The competitor names are the whole email.** Everything else is context for
  them.
- **It gives the price in the second paragraph.** A cold email that hides the
  price reads as the beginning of a funnel, which is the exact thing
  `ops/session-log.md` records the homepage being rewritten to avoid.
- **It links the self-audit rather than attaching a PDF.** An attachment from a
  stranger is a security prompt; the published page is checkable and is the only
  proof we have.
- **It says "you can act on it yourself".** True, already published on the site,
  and it is the line that separates us from an agency retainer.
- **No jargon**, per `CLAUDE.md`. The email never names the industry acronym.

**Never offered, and this is a standing rule rather than a style note:** no free
audits, no introductory rate, no "first five clients" discount, no bundling the
audit with a monthly plan. Settled 2026-07-31, `ops/service-tiers.md` section 9.
A free audit is an introductory rate wearing a different hat.

---

## 6. The record, and the do-not-contact list

**Everything goes in the client record** (`ops/client-record.md`): who was
contacted, when, what the finding was, what came back. Nothing goes in this
repository — it is public in principle and a clinic owner's name and email are
personal data.

**The do-not-contact record is the one that must survive everything.** A reply
asking not to be contacted is recorded permanently, because the only way to
honour it is to still have it when the list is rebuilt in six months. `/privacy/`
already commits us to this in writing.

**This is the second reason `business.clientDataStorage` blocks the first send.**
There is currently nowhere to put the record, and an outreach batch with no
record of who was contacted is worse than no batch.

---

## 7. What actually happens — the numbers, and what we do not know

**Nobody has sent one of these.** Everything here is a hypothesis with a place to
write the real number next to it.

| What | Guess | Real |
|---|---|---|
| Clinics on the Wirral, per trade | Unknown | `[PLACEHOLDER]` |
| Reply rate | Low single figures | `[PLACEHOLDER]` |
| Replies per paid audit | Unknown | `[PLACEHOLDER]` |
| Approaches per paid audit | **The number the whole plan rests on** | `[PLACEHOLDER]` |

### Capacity, and the batch size that comes out of it

**Answered by the owner 2026-08-09: three hours a day comfortably, and more than
that for a paid audit**, because one £250 audit offsets a whole day of his other
earnings.

That second half is the more useful number, and it is worth stating on its own:
**an audit is budgeted at 2h40–3h30** (`ops/audit-method.md` §7), so at £250 it
pays roughly two and a half times what an hour of the owner's alternative work
does. **Delivery is not where the money is lost. Selling is.**

The arithmetic, so a later session does not redo it:

| | |
|---|---|
| Hours available | ~21/week at three a day, and flexible upward for paid work |
| Running the business | ~2.5/week (`HANDOVER.md` §8: daily inbox, weekly batch, monthly reconciliation) |
| Left for delivery | ~18/week, so **six audits a week**, or four without touching the flex |

**So the batch size is twenty, sent weekly**, and the binding constraint is not
what it was assumed to be:

- **Twenty is safe on delivery.** An implausibly good cold outcome — one in four
  replying *and buying* — is five audits, comfortably inside a week.
- **Twenty is barely enough to learn from.** Two or three conversations and
  possibly no sale is the realistic first batch. That is not failure, it is the
  sample size.
- **The real cap is the list, not the diary.** If the Wirral turns out to hold
  forty clinics across the four trades, we run out of prospects before we run out
  of hours. **The answer to that is to widen the area — Liverpool and Chester
  were the runners-up when the Wirral was chosen — not to send more per week.**

**The one stop rule:** do not send batch two while batch one has more than four
audits still owed. Everything else is judgement.

**Two things this exposes rather than settles.**

- **Nobody has timed an audit.** 2h40–3h30 is a budget, and the classification
  step inside it (60–110 minutes) has no prior estimate behind it at all —
  `ops/audit-method.md` §7 says so and asks for it to be timed separately.
  **Everything above is arithmetic on an estimate.** Time the Wardith run
  (`HANDOVER.md` step 4) before the batch size is treated as a fact.
- **Four audits a week is when the runner stops being deferrable.** The only
  thing that fires the API queries today is
  `ops/audits/noven-2026-08-02/audit_query.py`, which is marked throwaway and
  says to delete it. Deferring the real runner was deliberate and correct
  (`ROADMAP.md` 3a, `ops/audit-method.md` §7: written before audit one it is a
  guess at a spec) — but its release condition is the first real audit, and the
  first real audit is what this document is for.

**Weekly, per `HANDOVER.md` section 8:** send the next batch, record what came
back. Thirty minutes.

---

## 8. What replies unlock

Four copy changes are deliberately parked waiting on real outreach evidence
(`ROADMAP.md` 2g). They are listed here as well because this is the document that
produces their evidence:

- **Real objections become FAQ entries.** Only ones that were actually raised.
- **Which businesses reply and buy** decides whether the homepage's list of who
  this is for — accountants, solicitors, private clinics, consultancies,
  agencies — is right. It is currently a hypothesis, and this batch tests one
  fifth of it.
- **The first client's written permission** unlocks the case study that replaces
  the "we have no case studies" messaging everywhere it appears.
- **Standing constraint:** no new services or pages for completeness until 100
  prospects have been approached.

---

## 9. Considered and not done

- **Warm introductions first.** Closed 2026-08-09: the owner does not have the
  network. Not a deferral.
- **Buying a list.** Illegal in practice for anything but corporate subscribers,
  and worthless for a batch of twenty on one peninsula. Companies House is free
  and better.
- **LinkedIn outreach as the opening move.** `ROADMAP.md` 2e keeps it for later,
  and it stays there. Connection requests to strangers are a slower version of
  this email with less room for the finding.
- **A multi-step chasing sequence.** Rejected above, on the grounds that it is
  the thing that makes a cold email feel like spam rather than a message from a
  person down the road.
- **Cold calling.** Not ruled out, but PECR's rules on unsolicited calls and the
  TPS/CTPS registers are a separate piece of work, and nothing in this document
  covers it. Do not start it on the assumption that the email position applies.
