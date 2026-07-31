<p align="center">
  <img src="assets/logo.svg" alt="Noven logo" width="300">
</p>

# Noven — the whole business on one page

**What this file is for:** someone who has never seen this business should be
able to read this and know what is sold, what exists, what does not, what must
happen next, and what has to happen every week forever. Everything here is
either a fact recorded elsewhere in this repo or is marked as an estimate.

**Status: 2026-07-31. The site is live. No customer has ever paid. Revenue to
date is £0.**

If you read nothing else, read [What has to happen next](#what-has-to-happen-next).

---

## 1. What Noven sells

Businesses used to be found through search. Increasingly their customers ask an
AI assistant — ChatGPT, Google, Copilot, Perplexity — "who's a good plumber near
me?" and act on the answer. If the assistant has never heard of a business, that
business quietly loses the job. Noven makes a business visible, accurate and
recommendable to those assistants.

| Product | Price | What the customer gets |
|---|---|---|
| **Audit** | £125 one-off | A written report on how the assistants answer questions about their business today, what they believe, what's blocking them, and an honest recommendation — including "you don't need us" |
| **Foundation** | £750 one-off | A fixed scope of setup work on the customer's **existing** website: crawler access, structured machine-readable facts, consistent facts across the web, and **two** permanent pages answering customer questions. Noven does not build websites |
| **Maintain** | £95/month | 10 questions tracked monthly, facts kept current, a one-page written record. Reports gaps, does not close them |
| **Grow** | £250/month | Maintain across 15 questions, plus one new answer page a month |
| **Lead** | £495/month | 25 questions, two answer pages a month, plus a quarterly review of competitors named ahead of them |

**The commercial logic:** the audit is the smallest thing sold and the qualifier
for the Foundation. Foundations are year-one income. The monthly plans are what
make the business worth owning.

**Prices were raised on 2026-07-31, before the first sale.** The old ladder
(£30 / £350 / £75 / £125 / £250) separated the monthly tiers by question volume,
which is pure cost to Noven and little extra value to the client — so every step
up earned *less* per hour than the one below it. The tiers now separate on
permanent answer pages. Full reasoning in `ops/service-tiers.md` section 9. The
timing was deliberate: with no minimum term on any plan, a later price rise on
existing clients is a churn event, so launch prices are the only ones that can be
set for free.

**Who runs it:** Kieran Smith, sole trader, trading as Noven, based in the
Wirral, working remotely across the UK. One person, no employees.

---

## 2. What exists today

**Live and working**

- **The website** — `novenstudio.co.uk`, seven static pages on Astro, deployed
  from `main` by Netlify, HTTPS confirmed. It is deliberately built as a
  demonstration of the product: no client-side JavaScript, AI crawlers
  explicitly allowed in `robots.txt`, an XML sitemap, and JSON-LD structured
  data. Visible facts and machine-readable facts both read from one file
  (`site/src/data/business.ts`) so they cannot drift apart.
- **Email** — `hello@novenstudio.co.uk` on Zoho Mail, tested both directions.
  The old Gmail address forwards to it.
- **Search Console** — sitemap submitted and confirmed, six pages.
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
- The Foundation — £750, published, scope now fixed, but with no delivery method
  written and **no estimate of how long it takes.** It is the only product in the
  business with no time budget at all.
- The payment route — decided, not built, no payment ever taken.

`ROADMAP.md` marks these `[D]` — decided on paper — rather than `[x]`. That
distinction is the most important thing in the file.

---

## 3. What does not exist

Ordered by what it stops.

| Missing | What it blocks |
|---|---|
| **Address for service of documents** | A legal disclosure already owed; the ICO record fix; the site footer; every future official form |
| **Terms of service** | Taking money under a contract; the refund position that prevents chargebacks |
| **Privacy notice** | Lawfully holding any customer or prospect information — including an outreach list |
| **A decision on where client data lives** | The privacy notice, and delivering the first audit lawfully. Constraint: **it cannot be this repo**, which is public |
| **API accounts, keys and spend caps** | Running any audit at all |
| **A working payment route** | Revenue |
| **A Foundation method and time budget** | The £750 product, and knowing whether it makes money |
| **Professional indemnity insurance** | Nothing yet — but it should precede the first Foundation, since that means changing a client's live website |

---

## 4. What has to happen next

The order below is by dependency and by irreversibility, not by importance.

### Immediately — this one has a deadline and no undo

**1. Ring the ICO fees helpline: 0303 123 1113.**

The ICO publishes each registered organisation's name and address on a public
register that anyone can download in bulk, within seven working days of payment.
Registration was paid on Thursday 30 July with the **owner's home address** on
it. Treat **Monday 10 August 2026** as the deadline.

Ask them to hold or suppress publication pending a change of address. This costs
nothing, takes fifteen minutes, and needs no other item to exist first. Once the
address is on a bulk-downloadable register it gets mirrored and copied, and
amending the ICO's own record does nothing about the copies.

### Then, roughly a day and a half of desk work

**2. Order the fallback service address (~£115/yr, 1st Formations or Quality
Company Formations).** The cheaper supplier already chosen — V LOT — took payment
around 29 July and has delivered nothing; the session log's own conclusion on 30
July was to take the fallback. That decision has not been executed. Order it
first because it has a postal lead time, then do the desk work while it travels.

**3. Write the terms of service and the privacy notice, and publish both.**
Nothing external blocks these. Use the ICO's own free privacy notice generator.
Decide the client-data retention period inside this step rather than twice
(the standing recommendation is life of the relationship plus twelve months).

**4. Run one audit end to end, on Noven itself, and time it.** This is the first
step that creates an asset instead of removing a risk. It needs no client and no
address, and it does five jobs at once: proves the deliverable exists, produces
the sample report that answers the "you have no case studies" objection, sets the
dated before-and-after baseline, and produces the one number the whole business
plan rests on — how long a month of Maintain actually takes. Start at
`ops/audit-setup.md`.

**5. Make one payment possible end to end.** Create and test a Revolut Pro
payment link with a real small payment; decide invoice or receipt; choose where
client records live (`ops/client-record.md`). Two hours. **A pasted payment link
in an email takes the first payment — the order page is a scaling tool, not a
gate.**

**6. Take the sample audit to three warm contacts.** Warm rather than cold, for
the reason in section 7.

### Not on the critical path, despite appearances

The order page and pay button, the audit runner script, Bing Webmaster Tools,
HMRC registration (not due until October 2027), the email banner rewrite, and the
three stub documents in `ops/`. None of these stops the first £30.

---

## 5. Dates and renewals

**Every dated obligation in this business currently lives in a markdown tick box
inside a git repository. There is no calendar, no reminder, no tickler file.**
Three separate documents say "put the reminder in the calendar" and nothing
records that any reminder was ever set. Fixing that is twenty minutes and is the
highest return on time in this document.

| What | When | If missed |
|---|---|---|
| ICO home address publishes | **~10 August 2026** | Home address on a bulk-downloadable public register, permanently |
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
and what breaks if it lapses. No credentials in it; this repo is public.

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

1. **Which trade and which area to go after first.** Being in the Wirral gives a
   credible local answer.
2. **How much time per week there is for delivery.** This caps everything.
3. **Whether any existing contact could be client number one.**
4. **Cold outreach is a legal question, not just a marketing one.** Under PECR,
   sole traders and unincorporated partnerships are treated like individuals for
   marketing email, so unsolicited approaches to them generally need consent —
   and this repo's own ICO notes say the target buyers are mostly sole traders.
   Warm introductions sidestep this entirely. Confirm the position before
   building any cold list. *Not legal advice — check it.*
5. **Whether the new prices survive contact.** They were set from estimated
   effort, not measured effort. If the self-audit shows Maintain takes three
   hours rather than one, `ops/service-tiers.md` section 9 gets rewritten, not
   defended.

*Settled on 2026-07-31 and recorded here so they aren't reopened:* the Foundation
is a fixed scope at a fixed price, not a ceiling to quote against; Lead's
fortnightly checking is gone; there is no founding-rate discount.

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
2. **`ROADMAP.md`** — the section "Where we are today" is the best 20 lines in
   the repo. The rest is a detailed task list; skim it.
3. **`CLAUDE.md`** — the standing rules for any change. Short, and binding.
4. **`ops/`** — the operating documents. See the index in `ops/README.md`.
5. **`ops/session-log.md`** — 1,100 lines, newest first, the full record of why
   every decision went the way it did. Do not read it front to back. Go to it
   when you want to know *why* something is the way it is, and do not re-argue
   a settled decision without reading its entry first.

### The vocabulary

Terms used throughout as though the reader already knows them:

- **The Foundation** — the £350 one-off setup on the client's *existing* site.
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
record format, but none has been delivered to anyone. A £750 product is on sale
with a fixed scope, no method and no time budget behind it.

None of that is a crisis, because nobody has paid yet. All of it becomes a
crisis on the day someone does.

**The correct next move is not more planning. It is to run one audit on Noven
itself, and find out what any of this actually costs in hours.**
