<p align="center">
  <img src="assets/logo.svg" alt="Wardith logo" width="300">
</p>

# Wardith — the whole business on one page

> **Renamed 2026-08-04: this business was called Noven.** The name collided
> with at least four other businesses, which the self-audit found the hard way.
> The live address is `wardith.co.uk`; `wardith.com` and `wardith.uk` are owned
> and redirect to it. Where a document below still says Noven it is recording
> something dated — the 2 August self-audit and its frozen question set are the
> main ones, and they must keep the old name or the baseline is destroyed.
> `ops/rename-to-wardith.md` is the full changeover; `ops/plan-to-1-september.md`
> is the timetable.

**What this file is for:** someone who has never seen this business should be
able to read this and know what is sold, what exists, what does not, what must
happen next, and what has to happen every week forever. Everything here is
either a fact recorded elsewhere in this repo or is marked as an estimate.

**Status: 2026-08-08. The site is live. No customer has ever paid. Revenue to
date is £0.**

If you read nothing else, read [What has to happen next](#what-has-to-happen-next).

---

## 1. What Wardith sells

Businesses used to be found through search. Increasingly their customers ask an
AI assistant — ChatGPT, Google, Copilot, Perplexity — "who's a good plumber near
me?" and act on the answer. If the assistant has never heard of a business, that
business quietly loses the job. Wardith makes a business visible, accurate and
recommendable to those assistants.

| Product | Price | What the customer gets |
|---|---|---|
| **Audit** | £250 one-off | A written report on how the assistants answer questions about their business today, what they believe, what's blocking them, and an honest recommendation — including "you don't need us" |
| **Foundation** | £800 one-off | A fixed scope of setup work on the customer's **existing** website: crawler access, structured machine-readable facts, consistent facts across the web, and **two** permanent pages answering customer questions. Wardith does not build websites |
| **Maintain** | £150/month | 10 questions tracked monthly, facts kept current, a one-page written record. Reports gaps, does not close them |
| **Grow** | £400/month | Maintain across 15 questions, plus one new answer page a month |
| **Lead** | £700/month | 25 questions, two answer pages a month, plus a quarterly review of competitors named ahead of them |

**The commercial logic:** the audit is the smallest thing sold and the qualifier
for the Foundation. Foundations are year-one income. The monthly plans are what
make the business worth owning.

**Prices have been raised twice, both times before the first sale.** On
2026-07-31 the tiers stopped separating on question volume — pure cost to
Wardith, little extra value to the client, so every step up earned *less* per
hour than the one below — and started separating on permanent answer pages
(`ops/service-tiers.md` §9). **The prices in the table above were set on
2026-08-05 (§11)**, once the self-audit had shown what the work actually
produces; §9 had priced against estimated effort and said so.

The timing was deliberate both times: with no minimum term on any plan, a later
price rise on existing clients is a churn event, so launch prices are the only
ones that can be set for free. **They were set from estimated effort, not
measured effort** — see section 7.

**Who runs it:** Kieran Smith, sole trader, trading as Wardith, based in the
Wirral, working remotely across the UK. One person, no employees.

---

## 2. What exists today

**Live and working**

- **The website** — `wardith.co.uk`, nine static pages on Astro, deployed
  from `main` by Netlify, HTTPS confirmed. It is deliberately built as a
  demonstration of the product: no client-side JavaScript, AI crawlers
  explicitly allowed in `robots.txt`, an XML sitemap, and JSON-LD structured
  data. Visible facts and machine-readable facts both read from one file
  (`site/src/data/business.ts`) so they cannot drift apart.
- **Email** — `hello@wardith.co.uk` on Zoho Mail, created 2026-08-06 and
  confirmed receiving. It is what the site publishes. `hello@novenstudio.co.uk`
  stays alive as an alias on the same licence for at least twelve months, and
  the old Gmail forwards in too. **Not yet checked: that mail sent *from* the
  new address passes SPF, DKIM and DMARC at the far end** — DNS is in place,
  but present records are not the same as a passing check.
- **Search Console and Bing** — a verified Domain property for `wardith.co.uk`
  since 2026-08-06 with the Change of Address running, and Bing Webmaster Tools
  set up 2026-08-07 with all eight indexable pages submitted. Bing matters
  because Copilot answers out of its index. Submitted is not indexed: neither is
  closed until a `site:wardith.co.uk` search returns the pages.
  `ops/search-console-and-bing.md`.
- **Brand** — the supplied assets are in and used as-is.
- **LinkedIn** — founder profile and company page, both linked from the
  structured data.
- **Business bank account** — Revolut Pro.
- **ICO registration** — `C1995412`, £47/yr by Direct Debit, registered
  2026-07-30.

**Decided in writing, but never once performed**

This distinction matters more than any other in this repo, and the roadmap's
tick boxes currently blur it. The following are **documents describing
intentions**, not things that have happened:

- The audit method — five documents in `ops/`, unusually thorough, never run.
- The monthly plans — priced and published, never delivered to anyone. They now
  at least have a format: `ops/monthly-record-template.md`.
- The Foundation — £800, published, scope now fixed, but with no delivery method
  written and **no estimate of how long it takes.** It is the only product in the
  business with no time budget at all.
- The payment route — the website half is now built and switched off (see
  step 5 below), and no payment has ever been taken.

`ROADMAP.md` marks these `[D]` — decided on paper — rather than `[x]`. That
distinction is the most important thing in the file.

---

## 3. What does not exist

Ordered by what it stops.

| Missing | What it blocks |
|---|---|
| **Address for service of documents** | A legal disclosure already owed; the ICO record fix; the site footer; every future official form |
| **Terms of service** — written 2026-08-09, unpublished | Taking money under a contract; the refund position that prevents chargebacks. Waiting only on the address for service |
| **Privacy notice** — written 2026-08-09, unpublished | Lawfully holding any customer or prospect information — including an outreach list. Waiting on the address and on the row below |
| **A decision on where client data lives** | The privacy notice, and delivering the first audit lawfully. Constraint: **it cannot be this repo**, which is public. It now blocks a page rather than only a habit |
| **API accounts, keys and spend caps** | Running any audit at all |
| **A working payment route** | Revenue |
| **A Foundation method and time budget** | The £800 product, and knowing whether it makes money |
| **Professional indemnity insurance** | Nothing yet — but it should precede the first Foundation, since that means changing a client's live website |

---

## 4. What has to happen next

The order below is by dependency and by irreversibility, not by importance.

### Immediately — but not for the reason this section used to give

**1. Ring the ICO fees helpline: 0303 123 1113.**

The ICO publishes each registered organisation's name and address on a public
register that anyone can download in bulk, within seven working days of payment.
Registration was paid on Thursday 30 July with the **owner's home address** on
it. **Monday 10 August 2026** is when that publishes.

**Reassessed 2026-08-09, and the address is the least of it.** This section used
to treat the publication as close to an emergency. The owner challenged that and
the challenge holds up: **the address sits in a Birkenhead square with 281 active
companies registered at it** (Companies House advanced search, checked
2026-08-09). It does not read as residential to a human or to a scraper, and
using a home address is ordinary for a sole trader. **The exposure is real and
permanent — bulk-downloadable data gets mirrored and the ICO amending its own
record does nothing about copies — but it is low-impact, and it is not worth
treating as the thing that stops everything else.**

**Settled 2026-08-09: this is two calls, not one.** Tomorrow's call is about the
trading name. **A second call goes in once the service address lands**, to change
the registered address — there is no point asking them to change it to an address
that does not exist yet, and the runbook's step 8 assumes the address is in hand.

**The call is still worth making tomorrow, for two better reasons:**

- **The trading name on the record.** The owner is not certain whether the
  registration was filed as "Noven". If it was, that is not a privacy problem, it
  is a **published-fact problem**: `/privacy/` prints registration **C1995412**
  and invites the reader to check it against the ICO's own register, because a
  business selling verifiable facts should hand them over. A reader who checks
  and finds a different name than the site claims has found exactly the fault
  this business is sold to detect in other people's businesses. **Ask, and get it
  corrected if it is wrong.**
- **The address has to change anyway** once the service address lands — it is
  step 8 of the `ops/third-party-services.md` B1c runbook. Asking about the
  process on the same call costs nothing.

**Suppression is still worth asking for while on the phone**, but as the third
item rather than the first, and it is not a reason to delay anything if the
answer is no.

**Not verified from a session:** the ICO's register returns HTTP 403 to automated
fetches, so whether the record still carries the pre-rename trading name could
not be checked here. Ask on the call, or look it up in a browser.

### Then, roughly a day and a half of desk work

**2. The service address — ordered Friday 7 August 2026, pending approval.** UK
Postbox Business Street Address, Poole, £12/month inc VAT. Identity verification
is with the provider and the confirmed address is expected **Monday 10 August**.
The provider comparison is closed in `ops/third-party-services.md` B1a–B1b and
should not be reopened.

**This is the item most other things are waiting behind**, so it is worth being
precise about what "pending" means: **nothing that publishes the address moves
until it is confirmed in writing.** That is the footer, the Organization
structured data, the terms, the privacy notice and every cold email. The desk
work below does not wait on it.

**Follow the runbook at `ops/third-party-services.md` B1c rather than working it
out at the checkout.** The two traps it exists to prevent: **buy the Business
*Street* Address, not the cheaper Business PO Box**, which is invalid for this;
and **register the trading name "Wardith" as its own verified step**, because
post addressed to a name the provider holds no record of is typically returned
or destroyed. It also covers the ID check — which leaves a soft footprint on
the owner's personal credit file — and the order the footer, the ICO address
change and the structured-data locality decision have to happen in.

**3. Publish the terms of service and the privacy notice.** ~~Write~~ — **both
were written on 2026-08-09** and are in the repo at `site/src/pages/terms/` and
`site/src/pages/privacy/`. The retention period was decided inside that step
rather than twice: life of the relationship plus twelve months, with tax records
outliving it because the law says so.

Neither page publishes yet, and neither is waiting on more writing. They are
waiting on two facts, because both documents state them: **the address for
service** (step 2), and **where client records live** — the open decision in
`ops/client-record.md`, which needs one named provider with encryption at rest
and a backup that has been restored once. Set those two values in
`site/src/data/business.ts` and both pages go live, the footer fills in, and the
structured data gains a postal address, all from the same edit.

Read them before they publish. They are terms this business will be held to.

**4. Run one audit end to end, on Wardith itself, and time it.** This is the first
step that creates an asset instead of removing a risk. It needs no client and no
address, and it does five jobs at once: proves the deliverable exists, produces
the sample report that answers the "you have no case studies" objection, sets the
dated before-and-after baseline, and produces the one number the whole business
plan rests on — how long a month of Maintain actually takes. Start at
`ops/audit-setup.md`.

**4b. Done — both LinkedIn About sections were confirmed correct on
2026-08-08.** `ops/own-facts-check.md` is the register of everywhere our own
facts appear, and is worth ten minutes on its own.

**5. Make one payment possible end to end.** Create and test a Revolut Pro
payment link with a real small payment; decide invoice or receipt; choose where
client records live (`ops/client-record.md`). Two hours. **A pasted payment link
in an email takes the first payment — the order page is a scaling tool, not a
gate.**

The order page itself was built on 2026-08-09 and is **switched off**: `/order/`
and `/order/pay/` are in the repo but are not built into the site, so nothing
about them is public. Paste the link into `site/src/data/order.ts` and it is
still off — it also waits on the terms, the privacy notice and the address, the
three items in step 3 and above. That is deliberate. Nothing in step 5 depends
on it.

**6. Send the first cold batch. Rewritten 2026-08-09 — this used to say "take
the sample audit to three warm contacts", and there are no warm contacts.** The
owner has no business network, so the first clients are cold, and the whole
method is `ops/outreach.md`: private clinics on the Wirral, limited companies
only, one assistant run per trade rather than per business, ten to twenty emails
at a time.

**The thing to know before reading it:** cold email is lawful to companies and
unlawful to sole traders, so steps 2 and 3 above stop being tidiness. Every
email has to carry the address for service, and there has to be somewhere to
keep a permanent do-not-contact record. **A warm route would have let us start
without either.**

### Not on the critical path, despite appearances

The order page and pay button, the audit runner script, Bing Webmaster Tools,
HMRC registration (not due until October 2027), the email banner rewrite, and the
three stub documents in `ops/`. None of these stops the first payment.

---

## 5. Dates and renewals

**Every dated obligation in this business currently lives in a markdown tick box
inside a git repository. There is no calendar, no reminder, no tickler file.**
Three separate documents say "put the reminder in the calendar" and nothing
records that any reminder was ever set. Fixing that is twenty minutes and is the
highest return on time in this document.

| What | When | If missed |
|---|---|---|
| ICO home address publishes | **~10 August 2026** | Permanent, mirrored, and **low-impact** — the address sits among 281 registered companies and does not read as residential (reassessed 2026-08-09, §4). The live question on that record is whether it carries the old trading name |
| ICO annual renewal | ~30 July 2027 | Penalty of up to £4,000 against a £47 fee. Note the real risk is a **silent Direct Debit failure**, so the check is "did it collect", not "did a reminder fire" |
| Domain renewal | **[PLACEHOLDER: registrar, renewal date and auto-renew status are recorded nowhere in this repo]** | Total outage — site, email, structured data, every published link |
| Zoho Mail renewal | ~29 July 2027 (inferred from purchase date) | The only contact channel on the site dies |
| Gmail forwarding | Review ~July 2027 | Mail sent to the old address is stranded |
| HMRC Self Assessment | By 5 October 2027 if trading began in 2026/27 | Failure-to-notify penalties |
| VAT threshold | Event-driven | Every page says "not VAT registered, so the prices shown are the prices you pay". That claim is published, crawled and cached |

Most annual items cluster in late July. One "renewals week" in the last week of
July covers nearly the whole year.

---

## 6. What the business depends on

**The full register is `ops/accounts.md`** — every account, cost, renewal date,
and what breaks if it lapses. No credentials in it — the repo is private today,
and is deliberately written as though it were public. `ops/own-facts-check.md`
section 4 has the correction and why the rule does not relax.

The one row worth repeating here: **the domain's registrar, renewal date and
auto-renew status are recorded nowhere.** It is the dependency whose failure is
total — site, mail, structured data, every published link — and it is the only
one nobody has looked up.

**Two structural risks worth naming.**

*The Gmail account is an identity, not an address.* `hello.noven.uk@gmail.com`
owns the GitHub login, the Search Console property and Netlify's notifications.
It is a free consumer account. Losing it costs the deploy pipeline, the source of
truth and the indexation tooling in one event.

*The bus factor is zero, not one.* A successor holding only this repo could
rebuild the site, run an audit to the documented method, and re-derive why every
decision was made — the reasoning here is genuinely well kept. They could not
deploy, change DNS, read or send mail, take a payment, or amend the ICO record.
**They could keep the product alive and could not keep the business alive for a
day.** The fix is a credential vault with an emergency-access grantee, plus a
written account register. That is an afternoon.

---

## 7. Things the owner must decide

Nobody else can settle these, and several are currently blocking work.

1. ~~**Which trade and which area to go after first.**~~ **Answered 2026-08-09:
   private clinics on the Wirral.** `ops/outreach.md` §1 has the reasoning.
2. ~~**How much time per week there is for delivery.**~~ **Answered 2026-08-09:
   three hours a day comfortably, and more for a paid audit — one £250 audit
   offsets a whole day of the owner's other earnings.** That is six audits a
   week, four without stretching, so outreach goes out in batches of twenty.
   `ops/outreach.md` §7. **It also reframes the business:** at 2h40–3h30 an
   audit, delivery pays about two and a half times the owner's alternative hourly
   work, so the constraint is finding buyers, not serving them.
3. ~~**Whether any existing contact could be client number one.**~~ **Answered
   2026-08-09: there is no network. The first client is cold.**
4. **Cold outreach is a legal question, not just a marketing one — and it is now
   the live route rather than the fallback.** Under PECR, limited companies and
   LLPs may be emailed without prior consent; sole traders and unincorporated
   partnerships are treated as individuals and may not. **So the target list is
   filtered on Companies House before anyone is contacted**, and the sole-trader
   buyers this document elsewhere assumes are the market are out of scope for
   cold email. The position, and the two things it puts on the critical path,
   are in `ops/outreach.md` §2. *Not legal advice — check it.*
5. **Whether the new prices survive contact.** They were set from estimated
   effort, not measured effort. If the self-audit shows Maintain takes three
   hours rather than one, `ops/service-tiers.md` section 11 gets rewritten, not
   defended.

*Settled on 2026-07-31 and recorded here so they aren't reopened:* the Foundation
is a fixed scope at a fixed price, not a ceiling to quote against; Lead's
fortnightly checking is gone; and **services are never bundled** — every product
is bought and priced on its own, with no combined offers, no "free with", no
discount for taking two, and no introductory or founding rates. A client who buys
more pays more. `ops/service-tiers.md` section 9 has the reasoning and the full
list of what that rules out.

---

## 8. Ongoing operations

None of this is currently defined anywhere. It is the recommended cadence.

**Daily (10 minutes, working days)** — read and clear `hello@`. The site
promises a reply within two working days; that promise is only kept by a habit.

**Weekly (30–45 minutes)** — reconcile Revolut against Zoho Books; check who is
due a visibility check; send the next small outreach batch and record what came
back; confirm the site is up.

**Monthly (2–3 hours)** — deliver every monthly plan; check API spend against
the caps; reconcile the month and put tax money aside; sweep the renewals table
for anything falling due in the next 60 days.

**Quarterly (half a day)** — revenue against the VAT threshold; re-check
supplier prices; verify a backup by actually restoring something; the Lead
quarterly reviews once a Lead client exists.

**Annually (late July)** — ICO renewal collected; domain renewed; Zoho renewed;
insurance renewed; delete client records past their retention period.

---

## 9. How to read the rest of this repo

**Read in this order.** Stop when you know enough.

1. **This file.**
2. **`ROADMAP.md`** — start at "Where we are today", which is the current state
   and the critical path. The rest is a detailed task list; skim it.
3. **`CLAUDE.md`** — the standing rules for any change. Short, and binding.
4. **`ops/`** — the operating documents. See the index in `ops/README.md`.
5. **`ops/session-log.md`** — long, newest first, the full record of why
   every decision went the way it did. Do not read it front to back. Go to it
   when you want to know *why* something is the way it is, and do not re-argue
   a settled decision without reading its entry first.

### The vocabulary

Terms used throughout as though the reader already knows them:

- **The Foundation** — the £800 one-off setup on the client's *existing* site.
  Not a website build.
- **The four promises** — the Foundation's four deliverables: crawler access,
  structured machine-readable facts, consistent facts across the web, and pages
  that answer customer questions. They organise the audit checklist.
- **The three verbs** — Maintain holds, Grow closes gaps, Lead beats competitors.
  Three verbs and four promises are unrelated to each other; the numbers being
  close is a coincidence that has already caused confusion.
- **Answer page** — one question, one permanent page, one URL, built from facts
  only that business has. Not a blog post, not an FAQ entry.
- **Run / outcome / band** — the audit's units. One run is one question put to
  one assistant once. Each run gets one of four outcomes — and "named wrongly"
  is treated as worse than absent. Results are reported as a band with the raw
  count, **never as a percentage**, because five runs cannot tell 3 from 2.
- **The runner** — a script to call the assistant APIs. Deliberately not built
  until after the first audit has been done by hand.
- **The order page** — does not exist yet. Referenced in several places as
  though it does.
- **One-way door** — this repo's term for anything that, once published, cannot
  be recalled. The home address is the live example.
- **A flag** — a `[PLACEHOLDER]` block that renders *visibly on the live site*.
  Not the same as a placeholder in a document.

---

## 10. The honest summary

The thinking in this repo is well above the standard for a business this size.
The decisions are argued, recorded, and mostly right. The reasoning would survive
the owner being hit by a bus.

The gap is between deciding and doing. Five documents specify an audit that has
never been run once. Three monthly plans are published and priced, and now have a
record format, but none has been delivered to anyone. An £800 product is on sale
with a fixed scope, no method and no time budget behind it.

None of that is a crisis, because nobody has paid yet. All of it becomes a
crisis on the day someone does.

**The correct next move is not more planning. It is to run one audit on Wardith
itself, and find out what any of this actually costs in hours.**
