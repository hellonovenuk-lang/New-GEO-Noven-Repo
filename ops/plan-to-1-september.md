# The run to 1 September

**Internal document.** Written 2026-08-04, the day the owner set two hard
constraints on this business. Everything else in `ops/` describes what to do.
This one describes **when, and with what money.**

---

## The two constraints

Both stated by the owner on 2026-08-04, and neither is negotiable by an
assistant:

1. **No further money can be spent on this business until 26 August 2026** (a
   Wednesday). Twenty-two days from the day this was written.
2. **The business must be fully operational, able to accept clients, with
   outreach active, by 1 September 2026** (a Tuesday). Six days after the
   money unfreezes.

**These two constraints do not conflict, and that is the finding.** Almost
everything left to do costs nothing. The rename — the largest remaining piece
of work — is free from end to end: DNS changes are free, Netlify is on the
free tier, a Zoho alias is free, LinkedIn is free, redirects are free, and the
repo work is free. It can all be finished inside the freeze.

What the freeze does is compress the *paid* items into a six-day window. That
window is the risk, and it is small enough to plan precisely.

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

**3. Nothing else.** Guard the six days. Anything not on this list waits.

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
and the paid list is short.

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
| **Wed 26 Aug** | Money unfreezes. API balances first, address for service second |
| **Tue 1 Sept** | Operational. Outreach active |
