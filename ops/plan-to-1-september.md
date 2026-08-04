# The run to 1 September

**Internal document.** Written 2026-08-04, the day the owner set two hard
constraints on this business. Everything else in `ops/` describes what to do.
This one describes **when, and with what money.**

---

## The two constraints

Both stated by the owner on 2026-08-04 and refined the same day, and neither
is negotiable by an assistant:

1. **No further money goes into this business before 26 August 2026 unless
   revenue pays for it.** A Wednesday, twenty-two days out. Revenue is the
   only exception, and it is a real one — see the section below.
2. **From 26 August there is capacity for the modest spend needed to get
   fully live.** Not a blank cheque; the list is short and costed below.
3. **1 September 2026 is the hard launch** (a Tuesday): fully operational,
   able to accept clients, outreach active.

**These two constraints do not conflict, and that is the finding.** Almost
everything left to do costs nothing. The rename — the largest remaining piece
of work — is free from end to end: DNS changes are free, Netlify is on the
free tier, a Zoho alias is free, LinkedIn is free, redirects are free, and the
repo work is free. It can all be finished inside the freeze.

What the freeze does is compress the *paid* items into a six-day window. That
window is the risk, and it is small enough to plan precisely.

---

## The revenue exception, and what it actually changes

**"No spend without revenue" is not the same constraint as "no spend".** It
means the business is allowed to pay for the things it sells, out of what it
sold them for — which is how a service business is supposed to work, and it
takes the biggest risk in this plan off the table.

**The £125 audit funds its own delivery several times over.** The worst
recorded tool cost is OpenAI at $12.63 for ~75 queries; even at three
providers and a fuller question set, an audit's API cost is a fraction of its
price. So a client who pays on 15 August pays for the API credit that delivers
their own report. That is cost of sale, not a breach of the freeze.

**The rule, so this doesn't get argued each time:**

1. **Revenue first funds delivering what was sold.** API credit to run the
   audit that was just bought. No approval needed — it is the cost of the
   thing.
2. **Then it sits.** Anything not required to deliver a sale already made —
   the address for service, insurance, tooling, a domain extension — waits
   for the 26th, even if there is money in the account. Otherwise "no spend
   without revenue" quietly becomes "no spend without an excuse".
3. **Not all of a payment is spendable.** Income received now is taxable
   later, and `ops/accounts.md` already carries the HMRC registration
   deadline. Set a share of every payment aside before treating the rest as
   working capital. What share is the owner's call, and it is not a decision
   an assistant should make.

### The consequence: selling before 26 August is now the plan, not a bonus

1 September is the **hard launch** — the date everything is finished and
outreach runs properly. **It is not the earliest a client can be taken.**
Under the revenue exception, one sale in the freeze window pays for its own
delivery, proves the whole pipeline end to end on a real customer, and
de-risks the six-day window at the end. That is worth more than a tidy launch.

**Two things have to be true before an early sale can be accepted**, and both
are free:

- **The site is renamed and live.** The rename costs nothing and can be
  finished well before the 26th — see `ops/rename-to-wardith.md`.
- **The payment route works.** Revolut Pro is free to hold and the audit
  payment link already exists. Test it with a real transaction before it is
  sent to anybody.

**And one thing is genuinely awkward.** The address for service is still
`[PLACEHOLDER]` in the footer of all seven pages, and it is a legal
disclosure requirement for trading under a name that is not the owner's own.
Taking money before that is resolved is the owner's call to make knowingly,
not something to discover afterwards. **Chasing V LOT is free and is the only
route that closes it before the 26th** — which moves it from an admin chore to
the thing standing between here and an early sale.

---

## A freeze on decisions is not a freeze on payments

Money leaves a business without anybody deciding anything. **Check these
before assuming nothing will be charged before the 26th:**

| What | Why it might charge in the window | Status |
|---|---|---|
| **Canva Pro** | The Wardith assets were exported as SVG on 2026-08-04, and SVG export is a Pro feature — so the subscription is live. Monthly or annual, billing date unrecorded | `[PLACEHOLDER: Canva plan, price and renewal date]` — **look this up** |
| **GoDaddy auto-renew** | Should not charge until ~Aug 2027, but GoDaddy attaches paid add-ons at checkout that renew on their own cycle | Check the three domains' add-ons, not just the renewal date |
| **`novenstudio.co.uk`** | Registrar, expiry and auto-renew status are all unrecorded — see below | **The one that could actually hurt** |
| **API credit auto top-up** | `ops/audit-setup.md` §4 says to leave auto top-up off. Whether it was actually left off during the 2 August run is not recorded | Confirm it is off, on all three |
| **ICO** | £47 Direct Debit, ~30 July, already collected | Fine |
| **Zoho Mail Lite** | £14.40/yr, ~29 July, already collected | Fine |

**Being unable to spend makes an unattended subscription worse, not better.**
A card declining is not a saving; on a domain or a mailbox it is an outage.

---

## The single biggest risk in the freeze window

**Nobody knows when `novenstudio.co.uk` expires, or who it is with.**

It is `[PLACEHOLDER]` in `ops/accounts.md`, and under a spending freeze it
stops being an admin gap and becomes a real exposure:

- If it expires between now and the 26th and auto-renew is off, **the site
  goes dark, all mail dies, and there is no budget to fix it.**
- If it expires in that window and auto-renew is on, a card is charged during
  a freeze — which is survivable, but should not be a surprise.

**This is a free, five-minute lookup and it is the first job on the list.** Log
into the registrar (Namecheap holds the DNS, so start there) and write the
date into `ops/accounts.md`. Do it today.

---

## Phase 1 — 4 to 26 August. Everything here costs £0

Ordered by what blocks what.

### The rename, start to finish

The whole of `ops/rename-to-wardith.md`, which is free. Phases C, D0, D and F
all land inside this window. The one paid item in that document is nothing:
the domains are already bought.

### The free admin that has been outstanding for weeks

None of this costs anything and all of it is on the critical path to being a
business somebody can safely pay:

- **The ICO call, Monday 10 August** (`HANDOVER.md` §4, registration
  **C1995412**). This has a deadline and no undo — the home address publishes
  to a bulk-downloadable register. **The freeze is not a reason to delay it;
  the fee is already paid.** Ask about the trading name on the same call.
- **Chase V LOT.** Money was paid ~29 July and nothing was delivered. Chasing
  is free, and it is the only route to an address for service that does *not*
  need £115 on the 26th. **Give it a deadline: if V LOT has not delivered by
  24 August, the fallback gets bought on the 26th.** Also find the order
  reference, amount and payment method — a chargeback needs all three, and
  none of them is written down.
- **The password vault** (Bitwarden, free tier) and an emergency-access
  grantee. `ops/accounts.md` calls this the whole answer to bus factor.
- **Zoho's recovery address** — five minutes, owed since 29 July, currently
  points at the mailbox it protects.
- **Bing Webmaster Tools** — free, and Copilot answers from Bing. More urgent
  after a domain move, not less.
- **Google Search Console** for the new domain, and the Change of Address
  tool once the redirects are live.
- **2FA and printed recovery codes on `hello.noven.uk@gmail.com`**, which owns
  the GitHub login, the Search Console property and Netlify's notifications.

### The work that makes 1 September possible

Outreach on 1 September needs things that do not exist yet and cost nothing to
make:

- **The audit deliverable, as a reusable template.** One exists as a one-off
  for the self-audit (`ops/audits/noven-2026-08-02/`). Per `CLAUDE.md`, client
  documents are `.docx` exported to PDF. Building the template now means the
  first paying client does not wait on it.
- **Who is being contacted, and what is said.** No target list and no outreach
  copy exists anywhere in this repo. This is the actual gap between "the site
  is live" and "the business is operational", and it is free to close.
- **What happens when somebody says yes.** Payment link, what is sent, in what
  order. `ops/client-record.md` records that client data storage is still
  undecided — and that is a decision, not a purchase.

---

## Phase 2 — 26 August to 1 September. Six days, in priority order

**1. The API accounts, and what they actually cost.**

The three accounts were opened and used for the self-audit on 2 August, so
this is a top-up rather than a setup. **But the cost estimate the pricing was
built on is wrong, and it is wrong in the expensive direction:**
`ops/audits/noven-2026-08-02/README.md` records **OpenAI alone at $12.63 for
roughly 75 queries**, against `ops/audit-setup.md` §6's estimate of about
£1.20 per 150. The Gemini and Perplexity totals were never recorded.

That matters here for one blunt reason: **every audit delivered costs real
money on the day it is delivered.** A client who buys on 27 August cannot be
served on an empty balance. Get the three real totals off the dashboards,
work out the true per-audit cost, and fund accordingly — with the caps from
`ops/audit-setup.md` §4 (£10 each was the plan; the real numbers may move it).

It also puts a question against the £95 Maintain price, which was set against
the wrong estimate. **Not a decision for this window** — do not reprice while
launching — but it needs answering before the first monthly client renews.

**2. The address for service, if V LOT has not delivered.**

~£115/yr inc VAT (1st Formations / Quality Company Formations). This is a
legal disclosure requirement for trading under a name that is not the owner's
own, and the rename does not change that — "Wardith" is a trading name exactly
as "Noven" was. It is the `[PLACEHOLDER]` in the footer of all seven pages.

**Trading on 1 September with that placeholder still on the site is publishing
a visible legal gap on a site whose entire pitch is that its own facts are
correct.** Buy it, or chase V LOT hard enough that it lands.

**3. The pre-launch audit — run it on Wardith, before 1 September.**

Owner's call, 2026-08-04, and it is a good one. The self-audit's verdict was
that the **identity** was the blocker rather than the site: "Noven" belonged to
at least four other businesses, so the answers went to them. A name with no
occupant removes that specific failure, and the fixes went in alongside it. So
whether the assistants can name Wardith by launch is a genuinely open question
— **and the only honest way to answer it is to ask them.**

- **It costs API money**, which is why it sits here rather than in Phase 1.
  Budget it with the balances in item 1.
- **It is a new dated run, not the frozen baseline.** Archive it as its own
  folder alongside `ops/audits/noven-2026-08-02/`. Do not overwrite that one
  and do not renumber its questions.
- **It doubles as the first half of the G2 measurement** in
  `ops/rename-to-wardith.md` — how fast a new name is learned, timed from the
  day the site went live under it. Nobody else has that number.
- **It decides what the site is allowed to say about its own visibility.**
  If Wardith comes back named, the strongest line on the homepage writes
  itself and it is checkable: *ask ChatGPT about Wardith and see.* If it does
  not, the site says nothing about it and stands on the proof it already has.
  Either way the copy follows the evidence.

**4. Nothing else.** Guard the six days. Anything not on this list waits.

### The free lever that decides how the pre-launch audit goes

**Indexation, not training.** An assistant can name a business two ways: from
what the model memorised, which moves on the timescale of model releases, or
from a live lookup at answer time, which moves on the timescale of a crawler.
The second is the one that can plausibly happen in four weeks, and it depends
on the site being in the indexes those assistants search.

That makes two free jobs the highest-leverage things in Phase 1:

- **Bing Webmaster Tools.** Still not done, already a finding, and Copilot
  answers from Bing. The self-audit found Copilot had no record of the site at
  all *because Bing never indexed it* — that is the single clearest cause of a
  blank answer, and it is free to fix.
- **Google Search Console** on the new domain, sitemap submitted, plus the
  Change of Address tool once the redirects are live.

Do both the week the site goes live, not the week of the audit. A crawler
needs time, and the audit measures whatever has happened by then.

---

## What is deliberately not being bought before 1 September

**Professional indemnity insurance** (~£8–25/month, `ops/third-party-services.md`
B2). The reasoning is sequencing, not thrift: it needs to be in force before
the first **Foundation**, which is where a live client site gets changed. An
**Audit** is a written report — nothing is touched, and the exposure is
different in kind.

So: sell audits from 1 September, and **buy the insurance before the first
Foundation is accepted, not before the first audit is.** If a Foundation is
sold in the first week, the insurance is bought that week. Do not let this
drift into "after the first one went fine".

---

## The honest read on 1 September

**Achievable.** The rename is free and fits comfortably in twenty-two days,
the paid list is short, and the revenue exception means a single early sale
removes most of what is left of the risk.

**The plan is no longer "wait, then launch".** It is: finish the free work,
try to sell one audit inside the freeze window, and let 1 September be the
date everything is finished properly rather than the date anything is first
attempted. A launch is a much smaller event when the pipeline has already run
once on a real customer.

**Three things could break it, in order of likelihood:**

1. **The outreach work never gets written**, because the rename is concrete
   and satisfying and writing a target list is neither. The site being live is
   not the same as the business being operational, and only one of those is on
   the 1 September promise.
2. **V LOT stays silent and the address for service is bought on the 26th** —
   which is fine, unless the provider takes longer than six days to issue it.
   **Check the fallback provider's turnaround before the 26th**, so the date
   is known rather than hoped for.
3. **`novenstudio.co.uk` expires in the freeze window.** Low probability,
   total impact, and currently unknown. See above.

---

## The dates

Add these to the same calendar the domain reminders went into on 2026-08-04.
`ops/accounts.md` is the full register; these are only the ones inside this
plan.

| When | What |
|---|---|
| **Today, 4 Aug** | Look up `novenstudio.co.uk` expiry and registrar. Confirm GoDaddy auto-renew. Find the Canva billing date |
| **Mon 10 Aug** | ICO call — address and trading name. Deadline, no undo |
| **Mon 24 Aug** | V LOT decision point: delivered, or the fallback gets bought |
| **Wed 26 Aug** | Spending capacity returns. API balances first, address for service second |
| **Tue 1 Sept** | **Hard launch.** Operational, outreach active |

**No date for the first sale, on purpose.** Under the revenue exception it can
happen any time the site is live and the payment route is tested, and the
earlier it does the less the six-day window at the end has to carry.
