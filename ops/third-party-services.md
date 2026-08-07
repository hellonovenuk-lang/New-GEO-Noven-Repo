# Third-party services — what we need, and who to use

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
| Payment collection — £250 audit | Own order page → Revolut Pro payment link | ~£1.45–£3.70 per sale | Blocked on terms + privacy + address |
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

**Pick:** Zoho Mail, on `novenstudio.co.uk`.

**Cost:** The Forever Free plan covers up to 5 users on one custom domain with
5 GB each — **but Zoho no longer offers it to new sign-ups on the EU, US or AU
data centres**, found when actually setting this up rather than assumed from
the pricing page. An account created on `zoho.eu` (as ours was) goes straight
to a paid plan or a 15-day trial, with no free option shown. **Mail Lite is
the real number to use: about £1 per user per month on annual billing
(£12/yr plus VAT — £14.40 actually charged, 10 GB), which also adds IMAP/POP
so it works in a normal mail
client** — a plan we'd already earmarked as the fallback, now the only
option in practice. Under Zoho's setup wizard, this is "Mail Only → Mail
Lite", not "Workplace" (that tier bundles shared team drive storage nobody
here needs).

**Why:** The roadmap already flags this ("an address on the Noven domain reads as
more established"). It matters more for us than for most businesses — we sell
consistent, credible business information, and a Gmail address on the contact
page of a site arguing for exactly that is a visible contradiction. It is the
cheapest credibility improvement available.

Zoho specifically, over Google Workspace or Microsoft 365, for one reason: **you
already have Zoho Books.** Same login, same account, same billing, no new vendor
relationship. Google Workspace and Microsoft 365 both start around £5–7 per user
per month — sixty to eighty pounds a year to solve a problem Zoho solves for
twelve or nothing.

**The catch worth knowing:** the free plan is web and mobile-app access only —
no IMAP, so it won't work in Apple Mail or Outlook. If that matters, Mail Lite
is a dollar a month. Not a reason to pick a different provider.

**Cheaper still, and why not:** ImprovMX forwards mail from a custom domain to
an existing inbox for free, but the free plan **receives only — it cannot send**.
Sending from `hello@novenstudio.co.uk` needs their paid plan at around $9/month,
which is more than Zoho Mail Lite. A forwarding-only setup where replies come
from a Gmail address is worse than not doing it at all: the customer sees the
inconsistency in the reply.

**Do this alongside the Netlify DNS work in roadmap 1b** — both are DNS record
changes on the same domain, so it's one sitting rather than two.

### A2. Site analytics — Cloudflare Web Analytics

**Pick:** Cloudflare Web Analytics.

**Cost:** Free, with no page-view ceiling.

**Why:** It's cookieless, so it needs no cookie banner — which matters because a
banner is the one thing that would put a consent dialog in front of the crawlers
and readers the whole site is built to serve. It is genuinely free rather than
free-to-a-limit, and at our traffic the paid options solve nothing extra.

**The alternatives, and when they'd win:** Plausible starts around $9/month for
10,000 page views and has a better dashboard plus goal tracking. Fathom starts
around $15/month. Umami's cloud free tier is generous (around 1 million events a
month) and it's open source if self-hosting ever appeals. All three are better
products than Cloudflare's. None is better *enough* to justify £100+ a year
before there is any revenue. Revisit if we ever need to know which page an
enquiry came from.

**Note:** Netlify has its own analytics as a paid add-on. Don't buy it — same
job, real monthly cost.

**Also free, also worth doing, already in the roadmap at 1e:** Google Search
Console and Bing Webmaster Tools. Both free, both need the sitemap submitted.
Bing matters more than its market share suggests, because Copilot draws on it.

### A3. Password manager — Bitwarden

**Pick:** Bitwarden, free tier.

**Cost:** Free for a single user, unlimited passwords and devices.

**Why:** We are about to accumulate credentials for a bank, a domain registrar,
Netlify, Zoho, an insurer, HMRC and the ICO — and shortly after that, access to
client websites. Client website credentials are the ones that matter: we will be
holding other businesses' access, and "it was in a note on my phone" is not a
defensible answer if something goes wrong.

Set this up **before** the account-opening run in section B and C, not after,
so credentials land in it as they're created rather than being migrated later.

---

## B. Before we're visibly trading

### B1. Address for service — a virtual office

**Correction (29 July 2026):** the note previously here said Hoxton Mix runs
"~£30/year". That was wrong — checked directly against their own pricing,
Hoxton Mix's cheapest plan is **£180/year** (£15/mo, scanning only, no
forwarding), and their bare registered-office-only tier is **£249.99/year**.
There is no £30 Hoxton Mix product. Don't reuse that figure.

**The market splits into two different products — confirm which one you're
buying:**

1. **Director's / registered-office service address** — ~£22–39/yr (The
   PostBox Company £22/yr, 1st Formations' "London Service Address" £26/yr,
   Quality Company Formations' registered office £39/yr). Companies House use
   only. Several of these providers state plainly that mail from banks,
   suppliers or customers is **returned to sender**, not forwarded — and this
   product is a limited-company concept, so it doesn't legally satisfy a sole
   trader's trading-disclosure requirement at all.
2. **Business / trading address service** — ~£72–115/yr. Explicitly licensed
   for publishing on a website, invoices and stationery. This is the one we
   need.

**Within category 2, checked on price and on Trustpilot/reviews.co.uk
reliability, because a dropped delivery here means a missed legal document —
and, since 7 August, on billing cadence:**

**Billing cadence is a selection criterion, not a payment detail.** *Added
2026-08-07, on the owner's constraint: capital is tight now, so an annual
£115 up front is a harder purchase than £12 a month, even though the annual
one is cheaper over a year.* This split the table in a way that price alone
never showed — **the two best-reviewed providers are annual-only and therefore
unavailable**, and the question becomes which of the monthly providers is
trustworthy rather than which provider is cheapest.

| Provider | Cost | Billing | Reviews | Note |
|---|---|---|---|---|
| ~~V LOT (vlot.uk)~~ | ~~£9.99–£47.88/yr~~ | — | **Poor** | **Dead. Paid ~29 Jul, nothing delivered, refund requested 2026-08-07** |
| **UK Postbox** — Business Street Address, Poole | **£10/mo exc VAT = £12/mo inc VAT** (£144/yr) | **Monthly, cancel any time** | ~800 reviews, **score unresolved: 4.0 and 4.7 both reported** — verify | **The pick, 2026-08-07.** See B1b |
| Icon Offices — Silver | £38.87/quarter (£155.48/yr) | **Quarterly** | 4.0/5, ~1,150 reviews, **7% one-star** | Cheapest quarterly, weakest record. See B1a |
| Hoxton Mix | £21/mo + VAT ≈ £25.20 inc (~£302/yr) | Monthly | 4.6–4.7/5 | Well-reviewed and monthly, but twice UK Postbox |
| Seed Formations | £72/yr | Annual | Mixed (~3.7/5) — includes a complaint of legal documents not being forwarded | Explicitly sole-trader marketed |
| Rapid Formations | £96/yr | Annual | Established, less review data pulled | Business Address Service |
| **1st Formations** | £96 + VAT (~£115.20/yr) | **Annual only** | **4.8–4.9/5, ~23,000+ reviews** | Best reviewed. **Ruled out by cadence, not by quality** |
| **Quality Company Formations** | £96 + VAT (~£115.20/yr) | **Annual only** | **4.7–4.8/5, ~2,500 reviews** | Same |

**Decision, 7 August 2026: UK Postbox, Business Street Address, Poole, £12/month
inc VAT.** Full working in B1b below.

**How this decision moved twice in one day, since the log should show it
straight.** The morning position was *buy 1st Formations, ~£115/yr* — reached
after V LOT was written off and Icon Offices was researched and rejected for
costing £120.12 against 1st Formations' £115.20. That reasoning was sound and
is unchanged; it was answering the wrong question. **The owner then set the
real constraint — monthly or quarterly billing — and 1st Formations does not
offer it at any price.** So the £5/yr difference that decided the morning's
comparison turned out not to be the deciding variable at all.

**The lesson worth keeping:** we compared six providers on annual cost before
anyone established that an annual payment was affordable. Ask what shape the
money has to be in before pricing anything again.

**Every provider in this market charges per item on top of the headline, and
none of them leads with it.** 1st Formations adds **£0.50 per letter** scanned
and **Royal Mail rates plus a 15% handling fee** to forward; Quality Company
Formations charges **£1 per item** scanned; UK Postbox charges **£1.20 per page
scan** on pay-as-you-go, plus postage to forward. At this business's volume — a
handful of statutory letters a year — all of these are pennies, and none is a
reason to re-open the choice. Recorded so the first invoice is not a surprise,
and so the next comparison starts from the all-in number.

#### B1a. Icon Offices — why it was assessed and not taken (7 August 2026)

Checked directly against their own pricing page, their terms and conditions,
Companies House and Trustpilot, not against their marketing.

**What is genuinely good about them.** They are a real, established company —
Icon Offices Limited, company number **10343713**, incorporated 24 August 2016,
active — and they hold the registrations this product is supposed to have: a
Companies House **ACSP** (agent number AP000227), **HMRC AML supervision**
(XNML00000198642) and an ICO registration. Their virtual office terms clause 3
**explicitly permits** using the address as a business address on a company
website, on contracts and on invoices, which is the category-2 product above
and the thing a sole trader's disclosure duty needs. On the product definition,
they pass where V LOT never did.

**Why we are not buying it anyway — the headline price is not the price.**

| Tier | Annual inc VAT | Mail forwarding | Scan & email |
|---|---|---|---|
| Bronze | £45.76 | **No** | **No** |
| Silver | £120.12 | Yes | Yes |
| Gold | £200.20 | Yes | Yes |
| Platinum | £273.00 | Yes | Yes |

The advertised "£0.99 per week" is Bronze, and Bronze is **collect in person, by
appointment, during office hours**. Their terms say so twice: Bronze customers
"are not eligible for on-demand postage or scanning services at an additional
cost", and post over 100g must be collected in person. Their nine addresses are
in Essex, London, Glasgow, Edinburgh and Belfast. **From the Wirral, Bronze is
not a service.** The first tier that forwards post is Silver at £120.12/yr —
which is *more* than 1st Formations at £115.20, against a 4.0 Trustpilot score
with 7% one-star reviews versus 4.8–4.9 across 23,000. Paying more for less
reliability on the one item whose failure mode is a missed legal document is
the same mistake as V LOT, in the other direction.

**Four things in their terms worth knowing, whoever we eventually buy from,
because they are not unique to Icon Offices:**

1. **"Free" forwarding means no handling fee, not free delivery.** Icon's free
   forwarding is the cheapest postage, **no tracking, no insurance, no delivery
   guarantee**, and only up to 100g; over that you arrange your own courier.
   They then disclaim liability for post lost, damaged or never delivered
   (clauses 10, 21, 24). Every provider in this market disclaims this. It means
   the address is a place documents can be *served*, not a guarantee they arrive.
2. **Clause 6: they may change your allocated address or cancel the service at
   any time**, and take no responsibility for your costs. For an address that
   goes into JSON-LD and gets cached and copied by assistants, that is a real
   exposure and worth checking for in whichever contract we do sign.
3. **Clause 3 has an odd carve-out** — you "cannot include our address where it
   may not be legally appropriate such as court summons or subpoenas". Read
   narrowly that is about what *we* put on court paperwork; read broadly it
   rubs against the whole point of an address for service of documents.
   **If we ever do buy from a provider with that wording, ask them in writing
   first and keep the answer.**
4. **Trading names must be registered with the provider and approved.** Post
   arriving for a name they hold no record of "may be destroyed or returned to
   sender" (clause 27). Whoever we buy from, register **Wardith** with them
   explicitly, not just the owner's own name.

**What would make Icon Offices worth revisiting.** One thing only: they bill
**quarterly at £38.87** where 1st Formations is **annual-only at £115.20 up
front**. If capital is tighter on 26 August than expected, ~£39 buys a working
address now against £115. That is a cash-flow choice, not a saving — held
quarterly for a year it costs £155.48 — and it is the only argument for them.

*Postscript, same day: the owner did set that constraint, so this paragraph
became the live question within hours of being written. Icon Offices is still
not the answer — **UK Postbox bills monthly at £12 and is cheaper than Icon's
quarterly £38.87 pro-rata (£155.48/yr vs £144/yr)**, on a longer trading
history. Icon Offices stays the second-choice quarterly option and nothing
more.*

#### B1b. UK Postbox — the pick (7 August 2026)

**Product:** Business Street Address, **Lytchett House, Poole, Dorset, BH16**.
**£10/month exc VAT, £12/month inc VAT (£144/yr), billed monthly, cancel any
time.** Mail plan is a separate component and **can be £0** on pay-as-you-go.

**Why it wins on the constraint that actually binds.** It is the only provider
checked that is simultaneously monthly, credentialled, long-established and
under £15/month. Hoxton Mix is monthly and well-reviewed at twice the price;
Icon Offices is quarterly and costs more per year on a weaker record; the two
best-reviewed providers do not sell monthly at all.

**The credentials, checked the same way Icon Offices was** — this is the test
B1 should have applied to V LOT and didn't:

- **UK Postbox Ltd, company number 06723381**, trading since 2008 — eight years
  longer than Icon Offices.
- **HMRC anti-money-laundering supervision: MLR XLML00000192390.** This is the
  registration that makes a virtual address provider lawful to operate, and the
  thing to demand of anyone selling one.
- **ICO data protection registration ZA038907**, and VAT registered
  (GB 456 8521 65).

**It sells the category-2 product explicitly, to sole traders specifically.**
Their own page lists "**Business Trading Address** — to use on marketing
materials and stationery" as a supported use, and states the service is "suited
to all types of company structures, whether you're a sole trader, partnership,
limited company or PLC". They carry an FAQ for exactly our case — a sole trader
not registered at Companies House — telling you to sign up as a sole trader.
**No inference required; this is the disclosure-duty product, sold as such.**

**What it costs beyond the £12**, so the first invoice is not a surprise:
pay-as-you-go page scans are **£1.20 each**, or a mail plan can be added
monthly; physical forwarding is charged at courier/postage cost. At this
business's volume — a handful of statutory letters a year — the £12 is
substantially the whole cost.

**Four things to know before signing up:**

1. **No in-person collection, by policy.** They do not release post at the
   sorting facility; everything is scanned or forwarded. Irrelevant to us and
   arguably better, but it is the opposite of Icon Offices' cheap tier.
2. **Identity verification is required and has its own process.** Build the
   lead time in rather than discovering it on the day; have ID ready.
3. **A PO Box will not do.** Their Business **PO Box** is cheaper and is
   marketed at sole traders, but their own FAQ confirms a PO Box is not a valid
   registered office, and the same objection applies to an address for service
   of documents. **Buy the Business *Street* Address.**
4. **Poole, Dorset is not Merseyside** — see the note below, which applies to
   every credible provider, not just this one.

**On the annual comparison, stated plainly rather than buried:** £144/yr
against 1st Formations' £115.20 means **monthly costs about £29/yr more**. That
is the price of not paying £115 in one go, and it is a reasonable price. If
capital eases later, switching to an annual provider is a change of address —
which, once it is in the footer and the JSON-LD, is not free. **Prefer to make
this choice once.**

**The locality question this does not solve.** `ROADMAP.md` records that adding
a `PostalAddress` to the structured data was tried on 2026-08-06 and reverted,
partly because it would commit us to "Merseyside" before the address existed.
It still would not: **none of the credible providers is in the north-west**, and
the address that lands will say Dorset. That is a decision to take deliberately
when the address arrives — publish the real locality, or publish no locality —
and not a reason to pick a worse provider for geography.

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

**Original research (28 July 2026) pointed at Mettle or Starling** — both
free digital business accounts, aimed squarely at sole traders, with free
transfers and FSCS protection. That reasoning is kept below for the record.

**Decision actually made (30 July 2026): Revolut Pro.** Not the account
researched, and worth writing down why it still holds up rather than reading
as a shortcut:

- **It's the product Revolut itself builds for this exact situation.**
  Revolut Pro sits inside an existing Revolut personal account rather than
  being a separate application — it's free to open and hold, gets its own
  sort code, account number and transaction history, and is explicitly
  aimed at freelancers, sole traders and other solo professionals. Registered
  companies aren't eligible for it, which confirms it's the sole-trader
  product, not a business account in a trench coat. It covers invoices,
  payment links, QR codes and Tap to Pay, so bank transfer, the C2 pick
  below, is a native option rather than a workaround.
- **FSCS protection now applies.** Revolut became a bank in the UK in March
  2026, so balances are FSCS-protected up to £120,000 — the same protection
  Starling was chosen for over Tide. **One caveat carried forward:** for a
  sole trader, personal and Pro balances are treated as one legal entity for
  this purpose, so the £120,000 cap is shared across both, not doubled. At
  £250–£800 per transaction and no meaningful balance sitting in either
  account, this isn't a practical risk — just don't assume it's two full
  limits if that ever changes.
- **Already banking here saved real time.** Skipping a new application with
  a bank we don't already have a relationship with was a legitimate reason
  to prefer this over opening at Mettle or Starling from scratch, on top of
  Revolut Pro fitting the job on its own merits.

**Not yet confirmed — check before relying on it:** the Zoho Books bank-feed
integration Revolut publishes documentation for is written against **Revolut
Business**, not Revolut Pro specifically. Pro has its own account number, so
Open Banking aggregators should still be able to find it when connecting
Zoho Books, but this hasn't actually been tried yet. Confirm the bank feed
connects before assuming reconciliation will be automatic — if it doesn't,
transactions can still be entered manually at our volume.

**Superseded reasoning, kept for context — why Mettle or Starling were the
original pick:**

**Why Mettle:** free, aimed squarely at sole traders, no monthly fee, free
transfers and direct debits, and it includes basic invoicing and payment chasing.
Application is online and quick.

**Why Starling if not Mettle:** it is a fully licensed bank with FSCS protection
and the deepest Open Banking integrations, also at zero monthly fee with
unlimited free transactions. If you expect to want anything else from a bank
later — a card, a loan, a savings pot — Starling is the safer long-term home.

**One to avoid for us specifically: Tide's free tier charges 20p per bank
transfer and is e-money rather than FSCS-protected.** At £250 and £150 payments,
20p a transfer is noise — but the lack of FSCS protection is a real difference
for money that isn't ours to lose.

**Timing matters most here.** Digital providers can open an account in about a
day; a high street bank can take weeks. The roadmap correctly identifies this as
the long pole in 1c. It's also worth checking whether your existing personal
account's terms permit business use in the meantime — most banks' terms don't,
and a single £250 transfer for services rendered is business use. (Revolut Pro
sidesteps this question entirely, since it's a separate account from the
personal one, not a personal account being used for business.)

### C2. Getting paid — split by price, decided 30 July 2026

**This section previously said "invoice everything by bank transfer, revisit at
client five".** That was right about the Foundation and the monthly plans and
wrong about the audit. Corrected below; the original reasoning is kept at the
end because it still holds everywhere except the audit.

**Prices restated 2026-08-01** after the 2026-07-31 repricing. The decision below
was taken when the audit was £30 and the Foundation £350; it was re-checked
against £250 and £800 and does not change, but the numbers it argues from do.

**Pick, per product:**

| What | How it gets paid | Fee on that amount |
|---|---|---|
| £250 audit | Revolut Pro payment link, on the website, upfront | ~£2.70 personal card, ~£7.20 commercial |
| £800 Foundation | Invoice, contract sent alongside, on agreement | £0 (bank transfer) |
| £150–700/month | Unchanged — manual invoice, revisit at client five | £0 (bank transfer) |

**Why the audit is the exception.** The general argument against cards is that
fees are a real slice — and at £800 they are. On the audit the arithmetic
inverts, because the fee an invoice saves is smaller than the friction it adds.
An invoice loop for an audit means: they email, we scope it, we raise the
invoice, we wait, we check whether it's been paid, we chase if not, then we
start. That is several touches and a delay of days on a product that promises
the report within two working days of scope and payment being confirmed — days
the client experiences as our turnaround, not as their own bank's. Roughly
£2.70–£7.20 buys all of that away and takes the money before the work rather
than after it. The chase risk goes to zero, which is worth more than the fee.

**The repricing does not weaken this, and it is worth saying why.** At £30 the
fee was ~1.7–3.5% of the sale; at £250 it is ~1.1–2.9%, because the rate is a
percentage and the fixed 20p shrinks against a larger sale. The fee argument for
the audit therefore got *better*, not worse. The only thing that changed
materially is the Foundation, where £5–10 of card fee became £8–23 — which
reinforces keeping it on invoice.

**Fees, checked 30 July 2026 — confirm before relying on them.** Revolut Pro
charges nothing to create or send payment links and invoices, and takes a cut
only on successful payments: **1.0% + £0.20** on domestic personal Visa or
Mastercard and on Revolut Pay, 1.5% + £0.20 on domestic personal Amex, and
**2.8% + £0.20 on international and commercial cards**. On £250 that is £2.70 at
best and £7.20 at worst. Note the worst case is the likely one more often
than it looks — we sell to businesses, and a business paying on a company card
is a commercial card.

**Why Revolut Pro's link and not Stripe.** Stripe is 1.5% + £0.20 on domestic
UK cards, which beats Revolut's commercial-card rate and loses to its personal
rate. On £250 the gap either way is under £3.25. Against that, Revolut Pro is
already set up (C1), the money lands in the account we already bank in, and
there is no second provider to onboard or reconcile against. **Not worth
running two payment providers for £1.65 a sale.** Revisit if volume ever makes
the difference real — same "don't build for this yet" logic as the monthly
plans below.

**The details get collected on our own page, not on Revolut's.** Revolut's
payment links do support custom fields that show as a page before the payment
page, and the first version of this plan used them — no page to build, no
backend. **Changed on 30 July 2026**, because those fields surface against a
*successful payment*: anyone who fills them in and then abandons at the card
screen is invisible to us. Our own form submits before the handoff, so an
abandoned checkout still leaves a lead. We also get validation we control (a
required, checked website field), and we keep our own brand in front of the
customer until the last step instead of dropping them onto a bare third-party
form immediately before asking for £250.

So the flow is: **our order page collects and validates → hands off to a
Revolut Pro payment link for the money only.** The site stays static — the
form can go to Netlify Forms, whose free tier covers 100 submissions a month,
far more than we need. Revolut's own custom fields drop to belt-and-braces;
worth carrying the email address across so payments can be matched to
submissions, which is a manual, by-eye job at our volume and should stay one.

**Still verify Pro's link behaviour in the app before building against it** —
the payment-link documentation is written against Revolut Business, and Pro is
the retail-app product. This matters less now that the fields aren't load
bearing, but the link itself still has to exist.

**A cost note worth confirming:** payment processing fees may carry VAT, and as
a non-VAT-registered business we cannot reclaim it — so the real cost may be
20% above the headline. Immaterial at these amounts, but don't be surprised by
it on the statement.

**Why the Foundation stays on invoice.** At £800 a card fee is roughly £8–23,
which is real money, and none of the friction argument applies — by the time
someone buys a Foundation there is already a conversation running, so an
invoice costs nothing in momentum. Contract and invoice go out together on
agreement. **What starts the delivery clock is now settled:** the pricing page
was changed on 2026-07-31 to read *within two working days of your payment
clearing*, so the clock cannot be started by someone who signed and didn't pay.

**Still true, and unchanged:** the cancellation terms in roadmap 1a were
deliberately written to read the same whichever way payment collection goes, so
none of this reopens the site copy. The monthly plans are untouched by this
decision — manual invoicing, revisited at client five, for the reasons below.

**The honest limitation, and the trigger to revisit.** Manual invoicing and
chasing stops being viable somewhere around **client five** on monthly plans —
the roadmap already says so. The work isn't the invoice, it's the chasing: five
clients paying monthly is sixty payment events a year to notice, match and follow
up on. That's when this decision is worth reopening, and the shape of the answer
is:

- **GoCardless (or Direct Debit via Zoho Books' own integrations)** for the
  monthly plans. Direct Debit is dramatically cheaper than cards on recurring
  payments and has materially better retention, because there's no card to
  expire. The trade-off is setup time — it used to also need a bank account we
  didn't have, but C1 has now settled that, so setup time is the only thing
  left standing between us and this when the trigger comes.
- ~~Payment links for the one-off audit and Foundation~~ — **decided,
  30 July 2026**, and no longer waiting on a conversion signal. The audit takes
  a Revolut Pro payment link on the website; the Foundation stays on invoice.
  See the top of this section.

**Don't build for the monthly plans yet.** It's a real decision with a real
trigger, and the trigger hasn't happened.

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

### D1. Data protection fee — register with the ICO

**Done, 30 July 2026.** Registered directly with the ICO and paying by Direct
Debit, so **£47/year** rather than £52. Application number `C1995412`. Renews
annually — the diary reminder is the part that actually matters, since missing a
renewal carries a penalty of up to £4,000.

**One thing left open**, recorded in roadmap 1c: which address went on the
registration. The ICO publishes the controller's name and address on a public,
bulk-downloadable register, and its own advice to home-based sole traders is to
supply an alternative address. Worth fixing at the source if a home address went
on, rather than seeking removal later.

**Pick:** Register directly with the Information Commissioner's Office. There is
no third party involved and no reason to use one.

**Cost:** **£52 a year** at tier 1 (micro organisation — under 10 staff or under
£632,000 turnover), reduced to **£47 if you pay by Direct Debit**.

**Why it applies to us:** under the Data Protection (Charges and Information)
Regulations 2018, organisations — sole traders included — that process personal
information must pay the data protection fee unless exempt. Consultancy and
advisory work for clients is generally within scope. We will be holding client
contact details, business information, and correspondence.

**Before paying, run the ICO's own self-assessment tool** — it's free, takes a
few minutes, and gives a definitive answer for our specific circumstances rather
than a general one. There are exemptions, and it's worth knowing whether one
applies before spending £47. If the tool says no fee is due, the ICO asks to be
told rather than simply not hearing from you.

**Why not to leave it:** the ICO can issue a penalty of up to £4,000 on top of
the fee for failing to register or renew. £47 against that is not a close call.
It renews annually, so put a reminder in the calendar the day you pay.

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

### E1. The category exists, and it's expensive

There is now a mature market of platforms that track how AI assistants answer
questions about a given business, and repeatedly ask the assistants a set of
questions and report how often a brand appears. As at July 2026 the main names
and their advertised entry prices:

| Platform | Entry price | What that buys |
|---|---|---|
| Otterly.ai | from ~$25–29/month | ~15 questions tracked, across ChatGPT, Google AI Overviews, Perplexity, Copilot |
| Peec AI | from ~€89/month | ~25 questions on the annual starter plan; ~€199 for 100 |
| Profound | from ~$82.50/month billed annually | 50 questions; ~$332.50/month for 100 |
| Scrunch AI | from ~$250/month | ~125 questions, 4 platforms |
| Ahrefs / Semrush add-ons | from ~$828/month including the required base plan | Bundled into a larger toolset |

**The problem is the pricing model, not the price.** These are priced per brand
tracked. That is the right shape for a business monitoring *itself* and exactly
the wrong shape for us, because we would be tracking a different brand per
client.

**Run it against our own numbers.** The cheapest option is roughly £20–23 a month
for one brand and about fifteen questions:

- Against the **£250 one-off audit**: a non-starter. The audit is a one-off, so
  we'd be renting a monthly subscription to produce a single document — and the
  subscription tracks one brand, so the second client needs a second one.
- Against the **£150/month Maintain plan**: that's roughly 13–15% of the revenue
  gone to one tool, before any of our time. On a plan whose entire promise is
  monitoring, that is survivable but it caps the business.
- Against the **£700/month Lead plan**: comfortable, and arguably worth it.

**The 2026-07-31 repricing softened these numbers but changed nothing.** The
binding objection was never the level, it was the shape: these tools price *per
brand tracked*, so the cost scales with our client count exactly as fast as the
revenue does, and never amortises. Running the questions ourselves costs about
£1.20 an audit at full rate (E2), and that number does not move when we add a
client.

Agency plans exist and would amortise better across many clients, but they start
well above the entry prices above and none of them makes sense before there are
clients to amortise across.

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

**Pick:** **Zoho Bigin** free tier when a spreadsheet stops working. Not before.

**Cost:** Free for 1 user, 500 records, one pipeline. Paid tiers from about
$7–9 per user per month.

**Why Bigin and not Zoho CRM:** Zoho CRM's free tier allows 3 users but is built
for sales teams and carries a lot of machinery we'd never touch. Bigin is built
for one to twenty people and does pipeline and contact management without the
overhead. It's also about a third cheaper if we ever pay. And again — same Zoho
account as Books, so client records and invoices live in one place.

**Why not yet.** The roadmap says it plainly in 3d: "a spreadsheet is fine until
it isn't". At one to three clients a spreadsheet is genuinely better — faster to
change, no schema to fight, and it lets the real data model emerge from real work
rather than being guessed at in advance. That's the same principle the whole
roadmap runs on.

**The trigger to switch** is when you can't answer "who's due a visibility check
this week" by looking. That's usually around five to eight clients.

**What to record from client one, whatever the tool** — this is roadmap 3d's
list and it's right: business, contact, what they want to be found for, area
served, stage, plan, what we've done, and dated visibility checks. Getting the
fields right in a spreadsheet now makes the eventual import trivial.

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
