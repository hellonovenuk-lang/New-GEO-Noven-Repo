# Noven roadmap

**What this file is:** what's true now and what's left. Read it at the start of
every session and update it at the end.

**Where the reasoning lives:** `ops/session-log.md` holds the full record of why
each decision went the way it did, newest first. Closed items here are one line
and a pointer; go to the log or the `ops/` doc when you need the argument.
Don't re-argue a settled decision from the summary.

**How we're working:** build the minimum needed to take a real client, then let
real client work tell us what to build next. We don't design processes for
situations we haven't met yet. Anything we don't know is written as
`[PLACEHOLDER]` rather than guessed. The three phases overlap.

---

## Where we are today

**The site is live** at `novenstudio.co.uk`, on HTTPS, deployed from `main` by
Netlify: seven static pages, readable by AI crawlers, with machine-readable
business facts and a sitemap submitted and confirmed in Search Console. Email is
`hello@novenstudio.co.uk` on Zoho. The brand assets are in and the palette
matches them. **Phase 1a and 1b are closed.**

**The audit's method is written** (roadmap 3a) across four `ops/` docs, but
nothing has been run against a real business yet.

**Two things are blocking, both about an address:**

1. **The ICO published, or is about to publish, the owner's home address** on a
   bulk-downloadable public register. Time-critical — see 1c.
2. **The service address hasn't landed.** V LOT took payment and may have
   delivered nothing. It blocks the ICO fix, the site footer, and the audit's
   pay button.

**Next piece of real work:** the Noven self-audit (3a). It needs no client and
closes items in 1e, 2d, 3a and 3c at once.

**The critical path, in dependency order:** ICO helpline call (deadline Mon 10
Aug) → service address ordered → footer address and ICO record fixed → terms and
privacy notice written → one payment possible end to end. **Running in parallel
and blocked by none of it: the Noven self-audit.** The order page is not on this
path — a payment link in an email takes the first £30. `HANDOVER.md` has the
long version, written for someone with no context.

---

## Phase 1 — Build (get to a site that can take a real customer)

**Done when:** a stranger can read the site, understand the offer, email us, and
pay us £30.

### 1a. Facts only the owner can supply — closed

All live on the site and in the structured data: `hello@novenstudio.co.uk` (the
old Gmail forwards, and will for months); no phone, email only, and the site
says why; reply within two working days; the Wirral, serving the UK remotely;
Kieran Smith, sole trader, no company number, not VAT registered; audit in one
working day, Foundation plan within two. Founder bio, photograph, LinkedIn
profile and Maersk as `alumniOf` are all in. The LinkedIn work is finished —
profile amended, company page live at `linkedin.com/company/novenstudio/`,
`businessLinkedIn` confirmed in the built JSON-LD — and `ops/linkedin.md` has no
open questions.

**Cancellation terms**, live on three pages: monthly plans roll month to month,
no minimum term, **no notice period**; the month already paid for runs out, no
part-month refunds. Chosen against the agency norm because a notice period costs
more in friction than it recovers at £75–250, and the Foundation being a
separate one-off already covers the front-loaded work. Add a minimum term only
if clients actually start taking a month and leaving.

**Two standing rules that came out of this and will recur:**

- A published LinkedIn URL must name the person (`/in/…`). `linkedin.com/me` and
  `/nhome` are viewer-relative and hit a login wall for a crawler. Strip `utm_*`
  parameters, and never publish a URL containing a `loginToken`, `authToken` or
  `session` — this repo is built for crawlers to ingest, which is the worst
  place to put a credential.
- Maersk is named in plain text only. Never their logo, never anything implying
  they endorse Noven.

- [ ] **Owner, two minutes:** open the LinkedIn profile URL in a private window.
      If it loads without a login prompt it's publicly visible, which is the
      point of publishing it. If it prompts, turn public visibility on.

### 1b. Domain and hosting — closed

`novenstudio.co.uk` owned and set in `astro.config.mjs` and `robots.txt`. Apex is
primary, `www` redirects to it. Netlify deploys `main`; HTTPS confirmed via
Netlify's API. Nothing to redirect — the domain only ever hosted the owner's own
projects. `hello@novenstudio.co.uk` is live on Zoho Mail (Mail Lite, DNS at
Namecheap, MX to `mx.zoho.eu`, SPF, DKIM, `p=none` DMARC), tested both
directions; setup and failure checks in `ops/zoho-mail-setup.md`.

### 1c. Between launch and the first payment

**Why launching early was safe:** nothing on the site took a payment, so
publishing committed us to nothing we couldn't honour. **The audit's pay button
ends that on purpose** — see "What the pay button changes" below.

**The trigger is an event, not a date.** Providers for everything here are
researched and picked in `ops/third-party-services.md`; confirm prices on the
provider's own site before committing.

#### Has a lead time — start these before they're needed

- [x] **Business bank account — Revolut Pro**, set up. Free, FSCS-protected since
      Revolut became a UK bank in March 2026, and already the owner's bank. One
      caveat: FSCS cover is shared across Pro and personal under one £120,000
      cap, not doubled. `ops/third-party-services.md` C1.
- [ ] **Address for service of documents — ordered, not delivered.** Trading
      under a business name as a sole trader carries a legal duty to show a name
      and an address where documents can be served, including on the website. A
      virtual office satisfies it. **V LOT chosen on cost (~£10–48/yr against
      ~£96–115), and its Trustpilot reviews are poor — reports of nothing being
      delivered after payment.** Don't tick this off or remove the footer
      placeholder until post through the address is confirmed working; fall back
      to 1st Formations or Quality Company Formations (~£115/yr inc VAT) if it
      doesn't land. **Never the home address:** this site is built so crawlers
      read the business facts and repeat them confidently, which works against
      us on exactly this field, and it is a one-way door — the footer can be
      edited, indexes and archives cannot.

#### Before money changes hands

- [x] **The £30 audit is paid on the website, upfront**, through our own order
      page that hands off to a Revolut Pro payment link for the money only. At
      £30 an invoice loop costs more in admin than the ~50p–£1.04 card fee saves.
      Revolut's own custom fields were rejected because **field values only
      surface against a successful payment**, so an abandoned checkout would
      leave us nothing; our form submits first. The four fields already exist on
      `contact.astro`. Matching payment to submission is manual and should stay
      manual. Full reasoning in `ops/session-log.md` (30 July) and
      `ops/third-party-services.md` C2.
      **Two copy jobs when the page is built:** draw the distinction between
      email (to ask) and the form (to buy), rather than deleting `contact.astro`'s
      "no forms" line, which is true and worth keeping; and update the promise —
      with scope and payment arriving together it becomes the report within one
      working day of ordering, down from up to three days.
      **Blocked** behind the terms, the privacy notice and the address.
- [x] **The £350 Foundation is invoiced**, with the contract sent alongside once
      both sides agree to start. At £350 the card fee is real money, there's
      already a conversation, and bank transfer is free.
      - [ ] Small copy fix on `pricing.astro`: "booking" must mean *payment
            received*, not signature, or a two-day clock can be started by
            someone who signed and didn't pay.
- [ ] How monthly plans get collected. Manual stops being viable around client
      five. The cancellation terms were written to read the same either way, so
      this doesn't reopen any copy.
- [ ] Which invoice or receipt we actually send — Revolut Pro issues both and
      Zoho Books is already paid for. Decide before the first payment, not live.

#### What the pay button changes

A pay button moves four deferred items into hard prerequisites. **None is
optional once it's live:** terms of service including the refund position; the
privacy notice; ICO registration (done); and the address for service — taking
payment on the site *is* visibly trading, so **the address is the real
dependency.**

**The refund position needs writing.** Requiring and validating the website
field kills the "paid with no website" case, but it validates shape, not
existence — typos, dead domains, parked domains and Facebook pages all pass.
Confirming a site resolves needs a serverless function and still wouldn't prove
the business is auditable, so it isn't worth building. What the refund line is
actually for: dead or typo'd URLs, a social profile where we needed a website, a
business outside our area, duplicate or accidental payments, someone changing
their mind before we start, and a business we look at and genuinely can't help.

It earns its place twice over: **a chargeback costs more than a refund we
control**, and **it sells** — a plain refund line does the same job as the FAQ's
"why trust a company with no case studies?" at the moment it matters most.

The Consumer Contracts Regulations' 14-day cancellation right covers consumers,
not business-to-business contracts, which is what we sell. A line in the terms,
not a refund regime — confirm when the terms are written.

`CLAUDE.md` bans repeated calls-to-action: the pay button goes in one deliberate
place, not on every page.

#### Before we hold a client's information

- [x] **Registered with the ICO**, 2026-07-30, Direct Debit, tier 1 at £47.
      Application number `C1995412`. **It renews annually — put the reminder in
      the calendar**, because a missed renewal carries a penalty of up to £4,000
      against a £47 fee. Two answers from the self-assessment worth keeping:
      **we do use personal information** (information about sole traders,
      partners and directors is personal information — the outreach shortlist in
      2b counts the day it's written); and **we are not a legal or financial
      service** — our product is called an audit but is not an audit in the ICO's
      sense, and answering yes would file us under regulated services we have no
      business being in.
- [ ] **URGENT — the home address is on the ICO registration and will publish.**
      The ICO publishes the registered controller's name and address on a public
      register anyone can download in bulk, **within seven working days of
      payment**. Registration went in Thursday 30 July, so treat **Monday 10
      August** as the deadline. This is the same one-way door as the footer, on a
      front the roadmap hadn't identified — once it's on a bulk-downloadable
      register it gets copied and mirrored, and amending the ICO's own entry does
      nothing about the copies. In this order:
      - [ ] **Ring the ICO fees helpline first thing: 0303 123 1113.** Ask them
            to hold or suppress publication of the address pending a change.
            This doesn't need a new address and buys time for the rest. The
            ICO's own guidance tells home-based sole traders to use an
            alternative address, so it's a request they'll have heard often.
      - [ ] **Get a service address that actually works** — see 1c above. This
            now blocks two things, not one.
      - [ ] **Update the ICO record** at
            `ico.org.uk/for-organisations/data-protection-fee/change/`. Needs the
            registration reference and security number from the confirmation —
            another reason to phone rather than wait.
      - [ ] **Check the public register** at
            `ico.org.uk/about-the-ico/what-we-do/register-of-fee-payers/` to
            confirm what actually published.
      **The standing lesson:** ask "does this get published, and where?" *before*
      submitting any official form. The service address is not a footer field —
      it's a prerequisite for the next registration we fill in.
- [ ] **Privacy notice page.** Due before the first client sends us anything.
      Use the ICO's own free generator (`ico.org.uk/create-your-own-privacy-notice`)
      — written by the regulator, built for sole traders, updated for the Data
      (Use and Access) Act 2025. It also needs the audit-record retention period
      from 3d.
- [ ] **Terms of service.** Mostly a job of collecting what the site already
      commits to — cancellation terms, no guaranteed outcomes, we don't build
      websites — plus the refund position above.

#### Has its own legal clock

- [ ] **Register as self-employed with HMRC.** Registration for Self Assessment
      is due by 5 October following the end of the tax year trading began, so
      trading in 2026/27 means October 2027. A £1,000 trading allowance may mean
      no registration is required at all early on. Confirm both against current
      HMRC guidance rather than taking them from here.

### 1d. Standing decisions

- [x] Sole trader to begin with, not a limited company.
- [ ] Watch the VAT threshold as revenue grows. The pricing page says we aren't
      registered, so it has to stay true.

### 1d-2. Brand assets — closed but for one flag

The committed logo was the *old* mark and has been replaced. Six supplied SVGs
are in `assets/brand/` untouched, with trimmed web copies in `site/public/`
(`viewBox` only, no path data altered). Wordmark now in the header and footer
instead of retyped Inter, favicon is the circle mark (legible at 16px and 32px,
light and dark chrome), logo in the structured data, contrast passes WCAG AA
throughout, checked on desktop and phone.

**Confirmed brand colours: deep navy `#170969`, warm white `#fffefa`.** The brand
is those two and nothing else — lighter tones are the same two at reduced
opacity, and the site palette follows. The supplied "Favicon" asset is the one
thing not to use; the circle avatar beats it at every size. The brand pattern is
unused so far.

- [ ] **The email banner reads "AI Visibility Services"** — category jargon, the
      words a competitor uses rather than a customer. `CLAUDE.md` bans it and
      every page of the site avoids it. Rewrite it in the site's own voice, or
      the first impression contradicts every page it links to.

### 1e. Launch checks

- [x] Build verified: 7 pages, correct canonicals, all JSON-LD parses, sitemap
      and robots.txt ship. Read on desktop and mobile, owner confirms both.
- [x] **Sitemap submitted and confirmed in Search Console** — Success, 6 pages.
      Five URLs from whatever occupied the domain before Noven (`/terms`,
      `/work`, `/approach`, `/privacy`, `/start`) were submitted for removal and
      live-tested as 404s, which is Google registering they're gone. Nothing
      further to do.
- [ ] Bing Webmaster Tools — not yet done. Matters more than its market share
      implies, because Bing's index is what Copilot answers from.
- [ ] Ask the assistants what they say about Noven, recorded and dated — our own
      before-and-after and our first proof. **This is now part of the Noven
      self-audit in 3a**; do it there rather than twice.

---

## Phase 2 — Outreach (how we get the first clients)

We're new with no case studies and the site says so, so we can't win on proof
yet. We win on being specific, being cheap to try, and being obviously not a
scam. **The £30 audit is the outreach tool**, priced to be an easy yes.

**Working when:** we have a repeatable way of getting conversations, and we know
roughly how many approaches produce one paid audit.

### 2a. Before contacting anyone

- [ ] One trade, one area. "Accountants and solicitors across the UK" is too
      broad to write a good email to.
- [ ] Decide how many we can realistically deliver for at once.
- [ ] Set a working definition of a good first client.

### 2b. The first approach — do the work before asking

Run a mini audit *before* making contact, so the first email carries a real
finding about their business rather than a pitch.

- [ ] Build a shortlist of [PLACEHOLDER: number] businesses.
- [ ] For each, ask the assistants their customers' question and record whether
      they're mentioned.
- [ ] Write the email — short, one specific finding, the £30 offer, no chasing
      sequence.
- [ ] Send in small batches so the email can change based on replies.
- [ ] Keep a record of who was contacted, when, and what came back.

### 2c. Warm routes (likely the first paying client)

- [ ] List existing contacts who run businesses or know people who do.
- [ ] Personal approach to each, offering the audit.
- [ ] Ask satisfied clients for one introduction each — the only referral
      mechanism we need for now.
- [ ] [PLACEHOLDER: local business groups, networking, trade bodies worth trying]

### 2d. Proof — the thing that unlocks everything else

- [ ] Written permission to publish results from the first clients.
- [ ] Record before-and-after, both dated.
- [ ] Publish the first case study on the home page, replacing the placeholder.
- [ ] Publish our own before-and-after — see the Noven self-audit in 3a.

### 2e. Later, only if the above works

Not until there are paying clients and proof.

- [ ] Writing that answers the questions our own customers ask.
- [ ] LinkedIn, or wherever our buyers actually are.
- [ ] [PLACEHOLDER: decide after the first ten conversations]

---

## Phase 3 — Outcome (actually doing the work we've promised)

**Working when:** we can do an audit and a Foundation to a consistent standard
without reinventing them each time, and a monthly client gets something real
every month.

### 3a. The audit (£30)

Promised on the site: what each assistant says about businesses like theirs;
what they know and believe about this business and whether it's accurate; what's
blocking them, in plain English; and an honest recommendation including "you
don't need us".

**The method is decided (2026-07-30) across four docs:** `ops/audit-method.md`
(decisions and reasoning), `ops/audit-questions.md` (the question set),
`ops/audit-site-checklist.md` (the working checklist), `ops/audit-report-template.md`
(what the client gets). **`ops/audit-setup.md` (2026-07-31) is the practical
half** — the accounts, keys, spend caps, folder and CSV headers to have in place
before the Noven run, Noven's own ten questions, and the run-day order. Start
there when the run happens. Headlines:

- [x] **The questions.** Ten doing five jobs — three discovery, two qualified,
      two named-business, one comparison, two buying-intent — built from six
      slots filled with the client's own words. Varying by trade changes the
      slots, not the frame. **The audit's ten become the client's tracked ten**
      on a monthly plan, frozen for twelve months once agreed.
- [x] **Which assistants, and how we record.** All four we promise, by two
      mechanisms: **Copilot has no API and Google's AI Overviews have none
      either** (Microsoft retired the Bing Search APIs in August 2025). ChatGPT,
      Gemini and Perplexity by API at 10 questions × 5 runs; Copilot and AI
      Overviews by hand at 3 × 3, labelled as such. Copilot's real diagnostic is
      Bing indexation. Recording is one CSV row per run with verbatim answers,
      exact model version and every competitor named. **Client data does not live
      in this repo** — it's public and the records contain personal data.
- [x] **Rates, not yes/no.** Five runs per question, reported as a **band with
      the raw count and never a percentage** — five runs can't tell 3 of 5 from
      2 of 5, so "60%" invites a client to read noise as a decline. Four outcomes
      per run, not two, because **"named wrongly" is worse than absent** and is
      what owners react to hardest.
- [x] **The website checklist**, ordered as the Foundation's four promises, so
      **diagnosis and fix are the same list**. 20 minutes on-site, 15 off, hard
      stop. Ends in one of three verdicts, including "the Foundation would be
      wasted until something else is fixed".
- [x] **The report template.** 800–1,200 words, three findings not ten, verbatim
      quotes, and **no score, index or grade** — every competitor prints one and
      ours would be an invented statistic.
- [ ] **Do the first one end to end and time it — on Noven itself.** Needs no
      client, and does four jobs at once: times the process, closes 1e's
      outstanding assistant check, creates the dated baseline 2d wants while
      "they've never heard of us" is still true, and **produces the sample audit
      we show prospects**. Run one experiment inside it: three questions at ten
      runs instead of five, to settle whether five is enough
      (`ops/service-tiers.md` section 8). If an audit takes a day, the process is
      wrong, not the price.
- [ ] **Build the runner.** 150 API queries can't be typed by hand — 75 minutes
      before a word of the report is written, which breaks the 90-minute budget
      on its own. Reads the questions, calls the three APIs, writes the CSV; hard
      query cap, resume, verbatim answers, client data outside this repo.
      **Deliberately after the first audit** — written first it's a guess at a
      format, written second it's a transcription of something that worked.
- [ ] Rewrite the process based on what the first one taught us.
- [ ] **Add a fifth field to the order page before it's built** — "what do people
      usually ask when they first get in touch?", optional, two lines. The only
      input we can't derive ourselves, and the difference between questions in
      the client's customers' words and questions in ours.

### 3b. The Foundation (£350)

Promised: crawler access, structured machine-readable facts, consistent facts
across the web, and pages that answer customer questions — all on the client's
existing site. We don't build websites.

- [ ] Write the Foundation checklist. **Largely written already** —
      `ops/audit-site-checklist.md` is the same list from the diagnosis side.
      What's owed is the *how* of doing the work, not the *what*.
- [ ] How we get access safely, and what we do when we can't. **Ask in two
      stages:** the Foundation asks for access *to do the setup*; a monthly plan
      is where we ask to keep it. A "no" to the second mustn't threaten the
      first. `ops/service-tiers.md` section 3.
- [ ] What happens when the site is too broken for the Foundation to help. **The
      audit's three verdicts already decide this** — what's left is what we do
      next, and what we refund.
- [ ] What we hand over at the end, and how we show what changed.
- [ ] Do the first one, time it, then fix the process.

### 3c. Monthly plans (£75 / £125 / £250)

**Decided and live — `ops/service-tiers.md` has the reasoning.** Three verbs, not
three intensities: Maintain holds your position, Grow closes the gaps, Lead beats
the competitors named ahead of you. Question counts double at each step
(10/25/50), which is checkable in a way "faster pace" never was. **The upgrade
engine is the monthly record itself** — it reports the gaps and doesn't close
them, so nobody has to sell anything.

- [x] What happens each month at each level — live on the pricing page, in
      how-it-works and in the structured data.
- [x] **We publish the answer pages**, client approves the words. Structured data
      doesn't survive copy-paste, so the client-publishes path costs more time
      and delivers a worse page.
- [x] **What an answer page is** — one question, one permanent page, one URL,
      built from facts only that business has. Not a blog post, not an FAQ entry.
      Every Foundation is practice for Grow.
- [ ] **Validate the numbers by doing it.** 10/25/50 at five runs each and the
      one-hour Maintain budget are estimates. **The Noven self-audit in 3a is the
      exercise that produces them.** The Maintain figure matters most: at an hour
      a month it scales past twenty clients, at three it caps the business
      around eight.
- [ ] **Write the publishing fallback into onboarding** — where we can't get
      publish rights, hand over a complete file with the structured data intact
      plus a one-page paste instruction, then verify it live. That verification
      is billable time inside the plan, not a favour.
- [ ] Decide how we check and report visibility each month.
- [ ] Write the monthly client update — short and readable.
- [ ] Define the quarterly review promised on Lead.
- [ ] Work out how many clients one person can hold at each level.

### 3d. Keeping track of clients

`ops/spine.md` is meant to hold this and is empty. A spreadsheet is fine until it
isn't — the trigger to move to something else (Zoho Bigin free tier) is when you
can't answer "who's due a check this week" by looking, usually five to eight
clients.

- [ ] Record per client: business, contact, what they want to be found for, area
      served, stage, plan, what we've done, dated visibility checks.
- [ ] Set up where audits and reports live. **Shape decided** in
      `ops/audit-method.md` section 5 — one folder per client per audit. What's
      left is choosing the storage, and the hard constraint is that **it is not
      this repo**, which is public and would hold personal data.
- [ ] **Decide a retention period and write it into the privacy notice** rather
      than deciding it twice. Recommendation: life of the relationship plus
      twelve months, then delete.

### 3e. The internal docs still stubbed out

Worth writing *after* the first client, when we know what's actually true.

- [ ] `ops/org-chart.md` — the five company seats
- [ ] `ops/spine.md` — the shared client and prospect data model
- [ ] `ops/escalation-rules.md` — the three "never do this without me" rules

---

## Open questions for the owner

- Which trade and which area do we go after first? Being in the Wirral gives us
  a credible local answer, and a local first client is far easier to get than a
  cold national one.
- How much time per week is there for delivery? This caps everything.
- Is there any existing contact who could be client number one?
