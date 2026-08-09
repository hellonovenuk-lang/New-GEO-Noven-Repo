# Third-party services — what we need, and who to use

**Status: Live** — prices restated against the repricing on 2026-08-01; some sections predate decisions made later in the same file, and say so.

**Internal document.** This is a working note for the owner, not client-facing
copy. It names products and categories plainly so decisions can be made quickly.

**What this is:** every outside service the roadmap implies we need, with a
recommendation for each, the cost, and the reason. Ordered by *when we need it*,
not by topic — same principle the roadmap now follows.

**How to read it.** Each item has a **Pick**, a **Cost**, and a **Why**. If you
only read the Picks, you have the shortlist. The reasoning is there so a decision
doesn't get re-litigated in three months.

**A caution on the prices.** All figures were researched on **28 July 2026** and
are what providers publicly advertised that day. Software pricing moves, free
tiers get withdrawn, and introductory rates expire. Confirm the price on the
provider's own site before committing. Dollar prices are the providers' own;
where a rough pound figure is given it assumes about $1.30 to £1 — check the rate
when you actually budget.

Already in place: **Netlify** (hosting), **Zoho Mail** (`hello@wardith.co.uk`
since 2026-08-06, with `hello@novenstudio.co.uk` kept as an alias — Zoho
replaced Gmail on 29 July, see A1), **Zoho Books** (invoicing and revenue),
**GitHub** (this repo). Those are treated as settled and the recommendations build
on them rather than replacing them.

---

## The shortlist

| What | Pick | Cost | When |
|---|---|---|---|
| Business bank account | Revolut Pro (set up) | Free | Before first payment |
| Address for service | **UK Postbox** — Business Street Address, Poole. Monthly, on the owner's cash-flow constraint. V LOT dead — refund requested 2026-08-07 | **£12/mo inc VAT** (£144/yr) | Before visibly trading |
| Email on the domain | Zoho Mail (Mail Lite) | £14.40/yr inc VAT | Any time — cheap win |
| Data protection registration | ICO, direct — **registered 30 Jul 2026** | £47/yr (Direct Debit) | Done |
| Privacy notice | ICO's own free generator | Free | Before first client data |
| Professional indemnity insurance | Compare via Simply Business / Markel | ~£8–25/mo | Before first delivery |
| Site analytics | Cloudflare Web Analytics | Free | Any time |
| Assistant answer checking | Do it ourselves via the APIs | Under £2 per audit | Now — it's the product |
| Client tracking | Zoho Bigin free tier | Free (1 user) | At client 2 or 3 |
| Password manager | Bitwarden | Free | Now |
| Payment collection — £250 audit | Own order page → Revolut Pro payment link. **Built 2026-08-09, switched off** — C2 | ~£1.45–£3.70 per sale | Blocked on terms + privacy + address |
| Payment collection — £800 Foundation and monthly | Invoice + bank transfer | Free | Revisit monthly at client 5 |

**Total committed spend before the first client pays: about £0–5 a month**, and
most of that is the service address, which is an annual bill. That fits the
near-zero brief. Everything with a real monthly cost is deliberately deferred
until there's revenue to judge it against. The audit's card fee doesn't change
that figure — it's charged per successful sale, so it only ever comes out of
money that has already arrived.

---

## A. Things worth doing now (free, or nearly)

### A1. Email on the domain — Zoho Mail

**Pick:** Zoho Mail Lite, on `wardith.co.uk`. Live since 2026-08-06.

**Cost:** about £1 per user per month on annual billing — £12/yr plus VAT,
**£14.40 actually charged**, 10 GB, with IMAP/POP so it works in a normal mail
client. Under Zoho's wizard this is "Mail Only → Mail Lite", not "Workplace".
Zoho's Forever Free plan is not offered to new sign-ups on the EU data centre,
so it was never actually available to us.

**Why Zoho rather than Google Workspace or Microsoft 365:** the owner already
has Zoho Books — same login, same billing, no new vendor.

### A2. Site analytics — Cloudflare Web Analytics

**Pick:** Cloudflare Web Analytics. Free, no page-view ceiling.

**Why:** cookieless, so it needs no cookie banner — and a banner is the one
thing that would put a consent dialog in front of the crawlers and readers this
site is built to serve.

**Revisit only if** we need to know which page an enquiry came from; Plausible,
Fathom and Umami are better products at £100+/yr. **Don't buy Netlify's
analytics add-on** — same job, real monthly cost.

### A3. Password manager — Bitwarden

**Pick:** Bitwarden, free tier — single user, unlimited passwords and devices.

**Why:** we hold credentials for a bank, a registrar, Netlify, Zoho, HMRC and
the ICO, and shortly after that **access to client websites**. Those are the
ones that matter: "it was in a note on my phone" is not a defensible answer if
something goes wrong.

---

## B. Before we're visibly trading

### B1. Address for service — a virtual office

**Decision, 7 August 2026: UK Postbox, Business Street Address, Poole,
£12/month inc VAT.** Working in B1b, purchase runbook in B1c.

**The market splits into two products, and buying the wrong one buys nothing:**

1. **Director's / registered-office service address** — ~£22–39/yr. Companies
   House use only; several providers return other mail to sender. It is a
   limited-company concept and **does not satisfy a sole trader's
   trading-disclosure duty at all.**
2. **Business / trading address service** — ~£72–£300/yr, explicitly licensed
   for publishing on a website, invoices and stationery. **This is the one we
   need.**

**Every provider charges per item on top of the headline and none leads with
it** — scanning is £0.50–£1.20 an item, forwarding is postage plus a handling
fee. At a handful of statutory letters a year these are pennies, but the next
comparison should start from the all-in number.

**The lesson worth keeping.** Six providers were compared on annual cost before
anyone established that an annual payment was affordable; the owner then set a
monthly-billing constraint that ruled out the two best-reviewed providers
outright. **Ask what shape the money has to be in before pricing anything.**

#### B1a. Rejected: V LOT and Icon Offices

**V LOT** took payment ~29 July 2026, delivered nothing, refund requested.
**Icon Offices** is a real ACSP-registered company, but its £45.76 tier does not
forward post at all and the first tier that does costs £120.12 — more than the
annual providers, on a 4.0 Trustpilot score against 4.8–4.9. Neither is being
revisited. `ops/session-log.md`, 7 August 2026.

**Four things to check in any provider's terms**, because they are standard
across this market and each has a failure mode that matters here:

1. **"Free" forwarding means no handling fee, not free delivery** — typically
   cheapest postage, no tracking, no insurance, 100g limit, and liability
   disclaimed for post lost or never delivered. The address is a place documents
   can be *served*, not a guarantee they arrive.
2. **Providers reserve the right to change your allocated address or cancel at
   any time.** For an address that goes into JSON-LD and gets cached and copied
   by assistants, that is real exposure.
3. **Watch for carve-outs on legal correspondence** — Icon's clause 3 barred
   using the address "where it may not be legally appropriate such as court
   summons or subpoenas", which rubs against the point of an address for
   service. **Ask in writing before signing and keep the answer.**
4. **Register the trading name with the provider.** Post arriving for a name
   they hold no record of may be destroyed or returned. Register **Wardith**
   explicitly, not just the owner's own name.

#### B1b. UK Postbox — chosen by the owner, 7 August 2026

**Status: ordered Friday 7 August 2026, pending approval.** Identity
verification is with UK Postbox and the owner is waiting on the outcome and on
the confirmed address — expected Monday 10 August. **Nothing downstream moves
until the address is confirmed in writing**, because it is published in the
footer, in the Organization structured data, in the terms, in the privacy notice
and in every cold email. Runbook is **B1c** below. Steps 1 to 4 are in flight;
**steps 5 to 9 are the ones still owed**, and step 5 — registering the trading
name "Wardith" on the account as its own verified step — is the one worth a
wasted month if it is skipped.

**Product:** Business Street Address, **Lytchett House, Poole, Dorset, BH16**.
**£10/month exc VAT, £12/month inc VAT (£144/yr), billed monthly, cancel any
time.** Mail plan is a separate component and can be £0 on pay-as-you-go; page
scans are £1.20 each; forwarding is charged at postage cost. At a handful of
statutory letters a year the £12 is substantially the whole cost.

**Credentials:** UK Postbox Ltd, company **06723381**, trading since 2008. HMRC
anti-money-laundering supervision **MLR XLML00000192390** — the registration
that makes a virtual address provider lawful, and the thing to demand of anyone
selling one. ICO **ZA038907**, VAT GB 456 8521 65. Their own page sells a
"Business Trading Address" to sole traders explicitly, so no inference is
required that this is the disclosure-duty product.

**One cost could not be pinned down.** Their user agreement mentions "the
standard setup fee" but none is published anywhere. **Treat the first month as
`[PLACEHOLDER: setup fee, if any]` + £12 and read the checkout total before
confirming.** If there is one, record it in `ops/accounts.md` and here.

**Three things to know before signing up:**

1. **A PO Box will not do.** Their Business PO Box is cheaper and marketed at
   sole traders, but their own FAQ confirms a PO Box is not a valid registered
   office, and the same objection applies to an address for service.
   **Buy the Business *Street* Address.**
2. **Identity verification is required** — biometric, typically approved within
   24 hours, and it leaves a soft ID-check footprint on the owner's credit file.
   Steps in B1c.
3. **No in-person collection, by policy.** Everything is scanned or forwarded.

**Switching later is not free.** Monthly costs about £29/yr more than the
annual providers; that is the price of not paying £115 up front, and it is
reasonable. But once the address is in the footer and the JSON-LD, changing it
is a change of address. **Prefer to make this choice once.**

**The locality question this does not solve.** `ROADMAP.md` records that a
`PostalAddress` in the structured data was tried on 2026-08-06 and reverted,
partly because it would commit us to "Merseyside" before the address existed.
It still would: **none of the credible providers is in the north-west**, and the
address that lands says Dorset. Decide deliberately when it arrives — publish
the real locality, or publish none — and do not pick a worse provider for
geography.

#### B1c. Buying it — the runbook

*Written 2026-08-07, after the owner confirmed the choice. Everything here is
checked against UK Postbox's own pricing page, business address page, identity
verification page and user agreement (reviewed 27 February 2024). Anything not
checkable in advance is marked `[PLACEHOLDER]` rather than guessed.*

**Before you start, have ready:** photo ID, proof of home address, a card, and
about half an hour. **Download their "Sole Trader" verification guide first** —
they publish a separate guide per legal status and it tells you exactly which
documents that route needs, which is faster than uploading and being rejected.

**The order of operations, which matters:**

1. **Buy the Business *Street* Address, Poole (Lytchett House, BH16), £12/month
   inc VAT.** Not the Business PO Box — cheaper, marketed at sole traders, and
   invalid for this. Not a London address unless you want to pay £18–42 for a
   postcode nobody will check.
2. **Choose the pay-as-you-go mail plan (£0/month)** unless there's a reason
   not to. Page scans are £1.20 each; at a handful of letters a year that beats
   any monthly plan.
3. **Read the checkout total before confirming** — see the setup-fee note in
   B1b. If a fee appears, it is a fact for `ops/accounts.md`, not a surprise
   to absorb.
4. **Complete identity verification.** It is biometric and AI-led, most people
   finish in minutes, and **approval is typically within 24 hours** during
   their operating hours. **It leaves a soft footprint on the owner's credit
   file** — an ID check only; their terms state it does not affect the credit
   report or the ability to borrow. Recorded because it is the owner's personal
   credit file and should not be discovered afterwards.
5. **Register the trading name "Wardith" on the account.** They publish a
   separate **"Add Business Names"** verification guide, so this is its own
   step with its own checks — not a free-text field. **Post arriving for a name
   they hold no record of is the standard way mail gets returned in this
   industry.** Do this before publishing the address anywhere.
6. **Record it in `ops/accounts.md` the same day** — account email, the full
   allocated address, monthly cost, billing date, and any setup fee. This is a
   recurring charge on a card and belongs in the register, not in a chat log.

**Then, and only then, the downstream work it unblocks:**

7. **Put the address in the site footer**, replacing the gap left when the
   `[PLACEHOLDER]` was removed on 2026-08-06.
8. **Change the ICO registration `C1995412` to the new address** — this is the
   original reason the address became urgent. The home address is on a
   bulk-downloadable public register.
9. **Decide the `PostalAddress` / locality question deliberately** — see the
   note above. The honest answer is now "Poole, Dorset", not "Merseyside".

**Five terms worth knowing, all from their user agreement:**

1. **They open and scan everything.** "You authorise us to open all physical
   mail we receive on your behalf, whether or not the mail is addressed to
   you." That is how a scanning service works, but it means client
   correspondence sent by post is read by a third party — relevant to the
   privacy notice, which is still to be written.
2. **Do not let the account lapse.** Inactive accounts have mail held one
   month, then **returned to sender**; after six months the account is purged,
   physical mail shredded and digital deleted. A failed card payment on a £12
   subscription could quietly break the legal disclosure on the site.
3. **You must move the address off before closing the account** — including
   with HMRC — or "the time using a UK Postbox address will be chargeable" for
   as long as it is still in use. The same trap Icon Offices sets. **Exiting
   this service is a project, not a cancel button**, which is the real argument
   for choosing once and staying.
4. **No refund of unused plan time** on cancellation, only any account credit.
   At £12/month that is trivial, which is a further point for monthly.
5. **Service is "AS-IS"** with no liability for "timeliness, deletion,
   mis-delivery or failure to store". Every provider in this market says this.
   It is the reason the address is a place documents can be *served*, not a
   guarantee they arrive.

**One thing to check before paying, carried over from B1:** their Trustpilot
score is reported as both 4.0 and 4.7 by different sources and we could not
resolve it — Trustpilot blocks automated fetching. **Look at the recent reviews
on the day.** This file's history is that V LOT's poor reviews were correctly
flagged and it was bought anyway; the check is five minutes and has already
been skipped once at a cost.

**Why now rather than later.** The roadmap already makes this call in 1a and 1c
and the reasoning holds: a sole trader using a business name that isn't their own
surname must disclose their name and an address where documents can be served,
including on the website. That is a trading disclosure requirement, not an
optional nicety, and it bites once we are visibly trading — which is the moment
the site goes live, not the moment someone pays.

The roadmap's argument for not using the home address is the important part and
worth restating: this site is deliberately built to be read and repeated by AI
assistants, with crawler permissions, structured data and a sitemap. Everything
that makes it good at that makes a home address in the footer harder to take
back. The footer can be edited; indexes, caches and archives cannot.

**At £12 a month this is a small item on the list and the one with the longest
tail if you get it wrong.** This sentence has now been wrong twice: it first
said "£30 a year", which was the corrected-away Hoxton Mix figure and never a
real price for this product, and then "~£115 a year", which was right about the
market and wrong about how we can pay. **The pattern in both errors is quoting
a number without checking what it buys or how it is billed.** Buy the
credentialled one — see B1b.

### B2. Professional indemnity insurance

**Pick:** Compare rather than pick blind. **Simply Business** and **Markel
Direct** both quote online for freelance and consultancy work; **Hiscox** and
**Superscript** are the other established names. Fifteen minutes with two quote
forms will settle it.

**Cost:** Advertised entry points cluster around **£6–8 a month** for basic
cover. Realistic annual premiums for marketing and consultancy work are more
often quoted in the **£100–500/year** range depending on cover level, turnover
and the specific activity described. Expect the honest number to be nearer
£10–25/month than the headline £6.

**Why it belongs here and not in "nice to have":** we will be making changes to
other businesses' live websites. The Foundation is explicitly "on the client's
existing site". If a change we make breaks something that costs a client money,
professional indemnity is the cover that responds. The site already says we don't
guarantee outcomes, which helps, but a disclaimer on a web page is not insurance.

**How to describe the business on the quote form** is the part that needs care —
premiums vary enormously by stated profession, and the honest description is
something like "marketing and web consultancy, making technical changes to client
websites". Don't understate it to get a cheaper quote; an inaccurate description
is the standard reason a claim gets declined.

**[PLACEHOLDER: owner to confirm]** — whether any existing policy (home,
contents, or a policy from previous self-employment) already provides cover, and
whether the roadmap's £800 Foundation work is better described to an insurer as
consultancy or as web development. The two attract different premiums.

---

## C. Before the first payment

### C1. Business bank account — Revolut Pro (decided and set up)

**Revolut Pro**, opened 30 July 2026. Free to open and hold, its own sort code
and account number, and Revolut's own sole-trader product — registered companies
are not eligible for it. Covers invoices, payment links, QR codes and Tap to Pay.

**The one caveat that affects anything:** FSCS cover is £120,000 **shared**
across Pro and the owner's personal balance, not doubled — they are one legal
entity for this purpose. No practical risk at £250–£800 a transaction, but do not
assume two full limits.

**Unverified — check before relying on it:** Revolut's Zoho Books bank-feed
documentation is written against Revolut *Business*, not Pro. Pro has its own
account number so an Open Banking aggregator should find it, but nobody has
tried. If it will not connect, entry is manual at our volume.

Mettle, Starling and Tide were the earlier research and are not being revisited.
`ops/session-log.md`, 30 July 2026.

### C2. Getting paid — split by price, decided 30 July 2026

| What | How it gets paid | Fee on that amount |
|---|---|---|
| £250 audit | Revolut Pro payment link, on the website, upfront | ~£2.70 personal card, ~£7.20 commercial |
| £800 Foundation | Invoice, contract sent alongside, on agreement | £0 (bank transfer) |
| £150–700/month | Manual invoice, revisit at client five | £0 (bank transfer) |

**Why the audit is the exception.** An invoice loop — they email, we scope, we
raise it, we wait, we chase — costs days on a product that promises the report
within two working days of scope and payment being confirmed, and the client
experiences those days as our turnaround. A few pounds buys that away and takes
the money before the work. **The chase risk goes to zero, which is worth more
than the fee.** At £800 the arithmetic inverts and there is already a
conversation running, so the Foundation stays on invoice.

**Revolut Pro fees, checked 30 July 2026 — confirm before relying on them.**
Nothing to create or send links and invoices; on successful payment **1.0% +
£0.20** domestic personal card or Revolut Pay, 1.5% + £0.20 personal Amex,
**2.8% + £0.20 international and commercial**. **The worst case is the likely
one** — we sell to businesses, and a business paying on a company card is a
commercial card. Fees may carry VAT we cannot reclaim, so the real cost may run
20% above the headline.

**The details get collected on our own page, not on Revolut's — do not
"simplify" this back.** Revolut's custom fields surface only against a
*successful* payment, so anyone who fills them in and abandons at the card
screen is invisible to us. Our form submits before the handoff, so an abandoned
checkout still leaves a lead, and we control the validation (a required, checked
website field).

So: **our order page collects and validates → hands off to a Revolut Pro payment
link for the money only.** The site stays static; the form goes to Netlify
Forms, whose free tier covers 100 submissions a month. Carry the email address
across so payments can be matched to submissions — a manual, by-eye job at our
volume, and it should stay one.

**Built 2026-08-09, and switched off.** `/order/` and `/order/pay/` exist in the
repo behind the switch in `site/src/data/order.ts`: with it off the two pages
are not built at all, are in no sitemap, and every "order the audit" button on
the site still points at the contact page. What turns it on is the payment link
existing, `/terms/` and `/privacy/` existing — those two check themselves — and
one line confirming the footer carries the address for service.

**Netlify Forms makes Netlify a processor of customer data**, because
submissions are stored and shown in their dashboard before they reach the inbox.
That is a sentence the privacy notice has to carry, and it is the only thing
about how the page was built that changes what that document says.

**Still to verify:** Revolut's payment-link documentation is written against
Revolut *Business*, and Pro is the retail-app product. The link itself still has
to exist, and it has to be fixed-amount — an open "enter any amount" link
contradicts the price printed next to the button.

**What starts the Foundation's delivery clock is settled:** the pricing page
reads *within two working days of your payment clearing*, so it cannot be
started by someone who signed and didn't pay.

**The trigger to revisit, and it has not happened.** Manual invoicing stops
being viable around **client five** on monthly plans — the work is not the
invoice, it is the chasing: five monthly clients is sixty payment events a year
to notice, match and follow up. The shape of the answer then is **GoCardless or
Direct Debit through Zoho Books** — far cheaper on recurring payments and better
retention, since there is no card to expire. Setup time is the only thing left
standing in the way. **Don't build it yet.**

### C3. Registering with HMRC — nothing to buy

The roadmap covers this in 1c and the position there is sound: registration for
Self Assessment is generally due by 5 October following the end of the tax year
in which trading began, and there is a £1,000 trading allowance below which
registration may not be required at all. **Both worth confirming against current
HMRC guidance rather than taking from a document.** No third-party service is
needed — you register directly with HMRC, free.

**An accountant is not recommended yet.** At this revenue there is nothing for
one to do that Zoho Books and an evening won't cover. Revisit when turnover makes
the VAT threshold a live question, which roadmap 1d already flags.

---

## D. Before we hold a client's information

### D1. Data protection fee — registered with the ICO

**Done, 30 July 2026.** Registered directly, Direct Debit, so **£47/year**
rather than £52. Application number **`C1995412`**.

**Renews annually, and the diary reminder is the part that matters** — missing a
renewal carries a penalty of up to £4,000 against a £47 fee.

**One thing left open**, tracked in roadmap 1c: the ICO publishes the
controller's name and address on a public, bulk-downloadable register, and its
own advice to home-based sole traders is to supply an alternative address. Fix
it at the source rather than seeking removal later.

### D2. Privacy notice — the ICO's own generator

**Pick:** The ICO's free privacy notice generator, at
`ico.org.uk/create-your-own-privacy-notice`.

**Cost:** Free.

**Why this over a paid template or generator:** it is written by the regulator
that enforces the rules, it is built specifically for small organisations and
sole traders, and it was updated in 2026 to reflect the Data (Use and Access) Act
2025. Paid privacy-policy generators charge for something demonstrably worse.

It produces two notices — one for customers and suppliers, which is the one that
goes on the website, and one for staff, which we don't need yet.

**Where it goes:** a new page on the site, linked from the footer. Roadmap 1c
already has this scheduled correctly — due before the first client sends us
anything, not before launch, since the site itself collects nothing.

**Written 2026-08-09, by hand rather than generated, and the generator is still
worth running.** Two disclosures decide this. An audit works by typing a client's
business name into systems run by OpenAI, Google, Perplexity and Microsoft, and
this site loads its typefaces from Google, which hands them every reader's IP
address. No generator can know either, and a notice that omits them is wrong in
the two places that are specific to this business. **Use the ICO's generator as a
checklist against the finished page** — it is the regulator's own view of what a
notice must cover, and it costs twenty minutes to read the output beside ours.

**The Google Fonts line is a disclosure standing in for a fix.** Self-hosting the
two typefaces would remove the third-party request entirely, take about an hour,
and make the page slightly faster as a side effect. Until that happens the notice
tells the truth about it.

### D3. Terms of service — nothing to buy

The roadmap's framing here is right and no supplier is needed: most of what we
promise is already written across the site — the cancellation terms, "we don't
guarantee outcomes", "we don't build websites". This is a job of collecting what
we've already committed to into one page, in the same plain voice, not a job of
buying a template.

**One caution if a template is ever used anyway:** generic terms templates are
written for businesses that make guarantees and have minimum terms. Ours does
neither, deliberately. A template would contradict the pricing page, the FAQ and
the how-it-works page simultaneously, and the site's whole argument rests on
those three agreeing with each other.

---

## E. Delivery — the tools for actually doing the work

This is the section with the most money at stake and the clearest answer.

### E1. The category exists, and we are not buying it

A mature market of platforms tracks how assistants answer questions about a
brand — Otterly.ai, Peec AI, Profound, Scrunch AI, and add-ons from Ahrefs and
Semrush — from roughly $25 to $250+ a month.

**The objection is the pricing model, not the price, which is why the repricing
did not change it.** They price **per brand tracked**, so cost scales with our
client count exactly as fast as revenue does and never amortises. Running the
questions ourselves costs about £1.20 an audit (E2) and that number does not
move when we add a client. **Settled; not revisited unless the shape changes.**

### E2. What to do instead — run the questions ourselves

**Pick:** Ask the assistants directly through their own APIs, and record the
answers. This is the recommendation, and not merely on cost.

**What it costs.** The token cost of these questions is close to nothing — they
are short questions with short answers. The meaningful cost is the web-search or
grounding fee, because a question like "who's a good accountant in Birkenhead"
only means anything if the model actually searches:

- **Google (Gemini)** — grounding with Google Search gives **5,000 free
  grounded prompts a month** on the Gemini 3.x family, then about $14 per 1,000.
  Flash-tier models remain on the free tier. **One request can trigger several
  billable search queries**, so budget 1.5–2× the query count, not 1×.
- **OpenAI** — the small models are cheap per token (GPT-5 Mini at roughly
  $0.25 per million input tokens and $2 per million output); the web search tool
  is charged separately, at **$10 per 1,000 calls — one penny a query**
  (confirmed 2026-07-30). Note that on OpenAI, unlike Google, **the retrieved
  search content is billed as input tokens on top of the per-call fee.**
- **Perplexity** — the Sonar model is about $1 per million tokens both ways,
  plus a **per-request search fee on every call** of roughly **$5–14 per 1,000
  depending on mode** (secondary sources, 2026-07-30; the official pricing page
  was unreachable, so **confirm against Perplexity's own documentation before
  relying on it**). It dominates the token cost at our volume.
- **Anthropic (Claude)** — Haiku 4.5 is $1 per million input and $5 per million
  output; Sonnet 5 is $3/$15 (with an introductory $2/$10 running to 31 August
  2026). The web search tool is charged separately, at **$10 per 1,000 searches**
  (confirmed 2026-07-30), with the results then billed as input tokens. The Batch
  API halves token costs for work that isn't time-sensitive, which describes
  every audit we will ever run. **Not currently used** — the site promises four
  assistants and Claude is not one of them; see `ops/audit-method.md` section 2.

**A worked estimate for one audit.** Four assistants, ten questions each, run
three to five times per question for reasons explained below: **120 to 200
grounded queries**. Google's free grounding allowance alone covers roughly 25 to
40 complete audits a month at zero cost. Even paying full grounding rates
everywhere, an audit's tool cost lands **comfortably under £2** against a £250
fee. That is a sustainable cost of goods; £23/month per client is not.

**Costed properly against the method as designed** — 150 API queries across
three providers, the rest by hand — an audit is **about £1.20 at full rate and
nearer £0.60 while Google's free allowance covers it**, or roughly 4% of the fee.
The full breakdown is in `ops/audit-method.md` section 6. The conclusion for this
document is unchanged and now has real numbers behind it: **cost is not the
constraint on the audit. Time is.**

**Set a spend cap on every provider account before the first real run**, low
enough that a loop bug costs pounds rather than hundreds.

**The strategic reason, which matters more than the cost.** The audit *is* the
product. If we outsource the asking to a platform, we own nothing: no method, no
history, no ability to answer "why did you ask it that way", and no way to
differentiate from anyone else who bought the same subscription. Building our own
question set is the thing that compounds — after twenty audits we have a library
of questions that work by trade and by area, which is an asset a subscription
never becomes.

**The limit found while designing the method, 2026-07-30: two of the four
assistants we promise cannot be checked this way at all.** Microsoft retired the
Bing Search APIs on 11 August 2025 and offers no Copilot API; the replacement it
points developers at, Grounding with Bing Search inside Azure AI Foundry, is an
Azure project rather than an endpoint and would measure a model we assembled, not
Copilot. Google's AI Overviews have the same gap — the Gemini API is a fair proxy
for Gemini and is not the AI Overview block a customer sees. Both are therefore
checked **by hand at a reduced run count, labelled as such in the report**, and
Copilot's real diagnostic becomes whether the client is in Bing's index at all —
which is a better finding anyway, because indexation is fixable and model
behaviour isn't. Full reasoning in `ops/audit-method.md` section 2. This does not
change the pick above; it narrows what the pick covers, and it is the sort of
thing a bought platform would have hidden behind a dashboard.

### E3. The methodology point that must not be skipped

**Assistant answers are not deterministic, and a single run is noise.**

This is the most important technical finding in this whole document and it
affects what we can honestly sell. Published testing found the same brand query
run ten times against ChatGPT produced mention rates anywhere from **20% to 80%**
for the same brand; broader testing found AI tools returned an identical brand
recommendation list **less than 1% of the time**. Consumer assistants run at
higher randomness than the APIs precisely to make conversation feel natural.

Three consequences, all of which shape the product:

1. **Every question must be asked several times and reported as a rate**, not as
   a yes or no. "You appeared in 3 of 5 runs" is a true statement. "You don't
   appear" — from one run — may simply be false, and a client can disprove it in
   thirty seconds by asking ChatGPT themselves. That's a refund conversation and
   a reputation problem in one.

2. **API answers and consumer-app answers differ.** The API version tends to be
   more constrained, and the consumer apps add personalisation and their own
   search grounding. If we check via the API and the client checks in the app,
   the answers will not match. **We should say so plainly in the report** — it
   costs us nothing, it pre-empts the objection, and it is exactly the kind of
   honesty the rest of the site trades on.

3. **It's a competitive advantage if we're honest about it.** Any tool that runs
   a query once and reports a score is reporting noise. Saying so — and showing
   our run counts — is a genuine differentiator against competitors selling
   confident single-run dashboards, and it costs us only the discipline of doing
   it properly.

**Record everything, dated.** Roadmap 1e already asks for our own before-and-after
as our first proof, and 2d makes recorded before-and-after the priority of the
first engagements. The recording format should be decided once, now, and reused:
question, assistant, date, number of runs, number of mentions, and the raw answer
text. A spreadsheet is fine. What matters is that it's consistent from audit one,
because retro-fitting a format across twenty inconsistent records is miserable.

### E4. Knowing whether the crawlers actually came — Cloudflare

**Pick:** Put client sites behind **Cloudflare's free plan** where the client
already uses Cloudflare or is willing to, and read the bot analytics.

**Cost:** Free.

**Why this is worth more than it looks:** the Foundation's first promise is
crawler access. Cloudflare's dashboard shows which AI crawlers hit a site and
how often — GPTBot, ClaudeBot, PerplexityBot, the search-specific bots and the
live agent traffic, categorised. Every Cloudflare customer including the free
plan can see and control AI crawler traffic by category.

That turns "we opened up crawler access" from a claim into a dated, checkable
before-and-after: no crawler visits before, crawler visits after. For a business
with no case studies, **evidence that costs nothing is worth a great deal.**

**Two cautions.** First, Cloudflare rolled out AI crawler verification with
default-on enforcement across free and pro plans during 2026 — meaning a site
may now be *blocking* crawlers it didn't intend to. That's a real thing to check
during an audit, and possibly a finding in its own right. Second, moving a
client's DNS to Cloudflare is a change to their infrastructure, not just their
website. Don't do it casually, and don't do it without the client understanding
what's changing.

**Where the client won't or can't use Cloudflare**, their existing host's access
logs answer the same question if they'll share them. Netlify, which we know, does
not expose this on the free tier.

### E5. Free tools that do real work

None of these cost anything and all of them are part of delivery:

- **Google Search Console** and **Bing Webmaster Tools** — for our own site and,
  with permission, for clients'. Bing feeds Copilot, so it matters more here than
  its market share implies.
- **Google's Rich Results Test** and **Schema.org's validator** — for checking
  the structured data the Foundation adds actually parses. We already do this for
  our own site; same check, client's site.
- **The assistants' own consumer apps** — free tiers of ChatGPT, Claude, Copilot
  and Perplexity. Worth using alongside the API checks precisely because they
  give different answers, which is itself part of the finding (see E3).

### E6. Client tracking — Zoho Bigin, but not yet

**Pick:** **Zoho Bigin** free tier — 1 user, 500 records, one pipeline — when a
spreadsheet stops working. Same Zoho account as Books, so client records and
invoices live in one place.

**Not yet.** At one to three clients a spreadsheet is genuinely better: faster to
change, no schema to fight, and it lets the real data model emerge from real work
instead of being guessed at. **The trigger to switch** is when you cannot answer
"who's due a visibility check this week" by looking — usually five to eight
clients.

**What to record from client one, whatever the tool** (roadmap 3d): business,
contact, what they want to be found for, area served, stage, plan, what we have
done, and dated visibility checks. Getting the fields right in a spreadsheet now
makes the eventual import trivial.

---

## F. Deliberately not recommending

Worth writing down so they don't get re-proposed:

- **A paid AI-visibility monitoring platform** — see E1. Revisit when there are
  around ten monthly-plan clients and an agency plan can be spread across them.
- **Google Workspace / Microsoft 365** — Zoho Mail does the job for a tenth of
  the cost and we're already in Zoho.
- **Paid analytics (Plausible, Fathom, Netlify Analytics)** — better products,
  but nothing they tell us changes a decision at current traffic.
- **A card payment processor** — see C2. Fees are material at our price points
  and invoicing works until roughly client five.
- **An accountant or bookkeeper** — nothing for one to do yet.
- **Scheduling tools (Cal.com, Calendly)** — the site is deliberately email-only
  and says so. Adding a booking link would contradict the contact page.
- ~~**A contact form service (Netlify Forms, Formspree)**~~ — **superseded by C2
  on 30 July.** The order page decision needs a form, and C2 picks Netlify Forms
  for it. The reasoning here still holds for why the site had no form until then,
  and it names the consequence correctly: a form means the privacy notice can no
  longer wait.
- **E-signature (Zoho Sign, Dropbox Sign)** — at £250 to £800 an emailed
  confirmation is proportionate. Revisit if a client ever asks for a signed
  agreement.
- **Anything with an annual contract.** Everything above is monthly or annual-
  but-cheap, deliberately, because we don't yet know what the work needs.

---

## What to actually do, in order

1. **Bitwarden** — free, ten minutes, and everything below creates a credential.
2. **Zoho Mail on the domain (Mail Lite, £14.40/yr inc VAT)** — the free plan isn't
   offered to new sign-ups on the EU/US/AU data centres, found while actually
   setting this up. Do it in the same sitting as the Netlify DNS work in
   roadmap 1b.
3. **Virtual office address** — **UK Postbox Business Street Address, Poole,
   £12/month inc VAT.** V LOT was ordered on 29 July and delivered nothing;
   written off with a refund requested on 7 August. Monthly billing was the
   owner's constraint and it ruled out the better-reviewed annual-only
   providers. Confirm mail actually arrives before relying on it, and register
   the trading name **Wardith** with the provider. Should land *before* the
   domain switches over, not after — see B1, B1a and B1b.
4. **Cloudflare Web Analytics** — free, one script tag.
5. ~~Business bank account~~ — **done**, Revolut Pro, see C1.
6. ~~ICO self-assessment, then the fee if due~~ — **done**, 30 July 2026,
   £47/yr by Direct Debit, application `C1995412`. See D1.
7. **Insurance quotes from two providers** — before the first Foundation, not
   before launch.
8. **ICO privacy notice generator** — free, before the first client sends
   anything.
9. **Build the audit question set and the recording format** — no cost, and it's
   the actual product.

Items 1–4 total roughly **£160 for the year, but only ~£27 to start** — the
address is now £12/month rather than a lump sum, which is the whole point of
choosing it. The £30–65 figure that stood here assumed V LOT's pricing, and
that supplier is gone. Items 5–9 are gated on real events rather than dates.

---

## Open questions for the owner

Written down rather than guessed at, in the roadmap's own style:

- **Insurance:** does any existing policy already provide cover, and should the
  Foundation be described to an insurer as consultancy or as web development?
  The two attract materially different premiums (see B2).
- **Cloudflare on client sites:** are we willing to ask clients to move their
  DNS? It's the cheapest source of hard evidence we have, but it's a change to
  their infrastructure, not just their website (see E4).
- ~~**Audit depth:** how many questions, and how many runs per question, is one
  audit?~~ — **decided 2026-07-30 in `ops/audit-method.md`.** Ten questions; five
  runs each on the three API assistants, three runs each on the two hand-checked
  ones. The E2 estimate assumed three to five runs and holds. What is still open
  is whether five runs is *enough*, and the self-audit's one experiment
  (`audit-setup.md` section 9) is designed to answer it.
