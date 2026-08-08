# Wardith roadmap

> **Renamed 2026-08-04: this business was called Noven.** The name collided
> with at least four other businesses, which the self-audit found the hard way.
> The live address is `wardith.co.uk`; `wardith.com` and `wardith.uk` are owned
> and redirect to it. Where a document below still says Noven it is recording
> something dated — the 2 August self-audit and its frozen question set are the
> main ones, and they must keep the old name or the baseline is destroyed.
> `ops/rename-to-wardith.md` is the full changeover; `ops/plan-to-1-september.md`
> is the timetable.

**What this file is:** what's true now and what's left. Read it at the start of
every session and update it at the end. **Where the reasoning lives:**
`ops/session-log.md`, newest first. Closed items here are one line and a
pointer — don't re-argue a settled decision from the summary.

**How we're working:** build the minimum needed to take a real client, then let
real client work tell us what to build next. We don't design processes for
situations we haven't met yet. Anything unknown is `[PLACEHOLDER]` rather than
guessed. The three phases overlap.

**The markers.** `[x]` — done, and true in the world. `[D]` — **decided on
paper, never yet performed**; a document describing an intention. `[ ]` — open.
The first two are the distinction that matters most in this file: a reader
scanning ticks and finding `[x]` against a decision concludes the business does
something it has never done once.

---

## Where we are today

**The site is live** at `wardith.co.uk`, on HTTPS, deployed from `main` by
Netlify: nine static pages, readable by AI crawlers, with machine-readable
business facts and a sitemap. Email is **`hello@wardith.co.uk` on Zoho**,
receiving since 2026-08-06. **Both search consoles are done** — Google
2026-08-06, Bing 2026-08-07 (1c-3, items 6a and 6b). Brand assets are in.
**Phases 1a and 1b are closed.**

### The habit this repo has to work by

**On 2026-08-06 four claims in these files turned out to be false** — a Zoho
mailbox "tested both directions" that had never been created; Search Console
"already set up" with no property on the live domain; a "sitemap confirmed, six
pages" that counted URLs read, not pages indexed; and "Netlify 301s non-primary
domains", which was wrong in the way that mattered most — `novenstudio.co.uk`
served the Wardith site at its own address for nine days, telling every crawler
the two were one site.

**The habit: re-read anything marked done before 4 August, and verify anything
new against the world rather than against another document.** All four were
caught by something outside this repo refusing to agree with it — Google's
validator, a browser address bar, the owner's memory. Nothing inside caught any
of them, because the repo was what made the claims. `ops/session-log.md`,
2026-08-06.

---

**The Noven self-audit — 2–3 August 2026, archived at
`ops/audits/noven-2026-08-02/`. Verdict C**, and not for the reason the method
expected: the site passed all three tests and the blocker was **identity**. Its
three findings still order this file.

1. **The name belonged to somebody else, at least four times over** — including
   an AI product trading as `noven.studio`. Not one of 210 automated answers
   cited the site. **Answered: the name is WARDITH and the rename is done as of
   2026-08-06.** Detail in 1c-2. **Still open, and free: Companies House and the
   trade mark register have never been checked.**
2. **Copilot had no record of the site at all**, because it retrieves from
   Bing's index. **Acted on 2026-08-07.** **Not closed until
   `site:wardith.co.uk` on Bing returns the eight pages.**
3. **Nothing tells a machine where the business works.** The pages say "the
   Wirral"; the structured data says only `GB`. Cost all 15 checks that asked
   for someone on the Wirral. **Blocked on the address for service and closes
   with it.** A locality-only `PostalAddress` was tried on 2026-08-06 and
   reverted within the hour — it would have committed us to "Merseyside" before
   the real address existed. Whatever lands is a real postal address, is not the
   founder's home, and has to be published by law anyway, so it fills the footer
   and the structured data from one fact. The note in `schema.ts` marks the spot.

**Three method faults the audit surfaced, none fixed — they are itemised in 3a.**

**Two things blocking a live pay button, both about an address:**

1. **The ICO published, or is about to publish, the owner's home address** on a
   bulk-downloadable public register. Deadline **Monday 10 August 2026** — 1c.
2. **The service address is decided but not bought.** UK Postbox Business Street
   Address, Poole, £12/month inc VAT, settled 2026-08-07. Runbook in
   `ops/third-party-services.md` B1c. It blocks the ICO fix, the footer, the pay
   button and finding 3.

**The critical path:** ICO helpline call (deadline Mon 10 Aug) → service address
ordered → terms and privacy notice written → one payment possible end to end.
The order page is not on it — a payment link in an email takes the first payment.

**`HANDOVER.md` has the longer version of all of this.**

---

## Phase 1 — Build (get to a site that can take a real customer)

**Done when:** a stranger can read the site, understand the offer, email us, and
pay us £250.

### 1a. Facts only the owner can supply — closed

All live on the site and in the structured data: `hello@wardith.co.uk`; no
phone, email only, and the site says why; reply within two working days; the
Wirral, serving the UK remotely; Kieran Smith, sole trader, no company number,
not VAT registered; the audit report within two working days of scope and payment
being confirmed (`ops/audit-method.md` section 7 says why it moved from one), and
a Foundation plan within two working days of payment clearing. Founder bio,
photograph, LinkedIn profile and Maersk as `alumniOf` are all in.
`businessLinkedIn` was held `null` through the rename on purpose and set
2026-08-06 — see 1c-3 item 3.

**Cancellation terms**, live on three pages: monthly plans roll month to month,
no minimum term, **no notice period**; the month already paid for runs out, no
part-month refunds. Chosen against the agency norm because a notice period costs
more in friction than it recovers at £150–700, and the Foundation being a
separate one-off already covers the front-loaded work. Add a minimum term only
if clients actually start taking a month and leaving.

**Two standing rules that will recur:**

- A published LinkedIn URL must name the person (`/in/…`). `linkedin.com/me` and
  `/nhome` are viewer-relative and hit a login wall for a crawler. Strip `utm_*`
  parameters, and never publish a URL containing a `loginToken`, `authToken` or
  `session` — this repo is built for crawlers to ingest, which is the worst
  place to put a credential.
- Maersk is named in plain text only. Never their logo, never anything implying
  they endorse Wardith.

- [ ] **Owner, two minutes:** open the LinkedIn profile URL in a private window.
      If it loads without a login prompt it's publicly visible, which is the
      point of publishing it. If it prompts, turn public visibility on.

### 1b. Domain and hosting — closed

`wardith.co.uk` owned and set in `astro.config.mjs` and `robots.txt`. Apex is
primary, `www` redirects to it. Netlify deploys `main`; HTTPS confirmed via
Netlify's API. Mail is **`hello@wardith.co.uk` on Zoho**;
`hello@novenstudio.co.uk` stays alive as an alias and must keep receiving for at
least twelve months.

### 1c. Between launch and the first payment

**Why launching early was safe:** nothing on the site took a payment, so
publishing committed us to nothing we couldn't honour. **The audit's pay button
ends that on purpose.**

**The trigger is an event, not a date.** Providers are researched and picked in
`ops/third-party-services.md`; confirm prices on the provider's own site before
committing.

#### Has a lead time — start these before they're needed

- [x] **Business bank account — Revolut Pro**, set up. Free, FSCS-protected since
      Revolut became a UK bank in March 2026. One caveat: FSCS cover is shared
      across Pro and personal under one £120,000 cap, not doubled.
      `ops/third-party-services.md` C1.
- [ ] **Address for service of documents — not bought. Buy UK Postbox's
      Business Street Address, Poole, £12/month inc VAT.** Trading under a
      business name as a sole trader carries a legal duty to show a name and an
      address where documents can be served, including on the website. A
      virtual office satisfies it. **Buy the *Street* address, not their
      cheaper Business PO Box — a PO Box is not a valid address for this.**
      Don't tick this off until post through the address is confirmed working.
      Runbook — both traps, the ID check, the order the downstream work happens
      in — is `ops/third-party-services.md` B1c. The provider comparison is
      closed in B1a–B1b, along with the V LOT refund still outstanding; don't
      reopen it.

      **The footer carries no address, and what stands in its place is a
      commitment: it is published before the first customer is onboarded.**
      Defensible only while nothing on the site takes a payment. The reminder
      is a comment in `Base.astro`.

      **Never the home address.** The footer can be edited; indexes and archives
      cannot, and this site is built so crawlers repeat its business facts
      confidently.

#### Before money changes hands

- [D] **The £250 audit is paid on the website, upfront**, through our own order
      page that hands off to a Revolut Pro payment link for the money only.
      Revolut's own custom fields were rejected because **field values only
      surface against a successful payment**, so an abandoned checkout would
      leave us nothing; our form submits first. The four fields already exist on
      `contact.astro`. Matching payment to submission is manual and should stay
      manual. Full reasoning in `ops/session-log.md` (30 July) and
      `ops/third-party-services.md` C2.
      **Two copy jobs when the page is built:** draw the distinction between
      email (to ask) and the form (to buy), rather than deleting `contact.astro`'s
      "no forms" line, which is true and worth keeping; and carry the two
      optional fields already added to `contact.astro` (what customers usually
      ask; what a new customer is worth) onto the form.
      **Not on the critical path.** A payment link in an email takes the first
      payment; this page is a scaling tool for roughly sale five onward. Still
      blocked behind the terms, the privacy notice and the address whenever it
      is built.
- [D] **The £800 Foundation is invoiced**, with the contract sent alongside once
      both sides agree to start. At £800 the card fee is real money, there's
      already a conversation, and bank transfer is free.
      - [x] Copy fix on `pricing.astro`: "booking" now reads *payment clearing*,
            so the two-day clock can't be started by someone who signed and
            didn't pay. Applied 2026-07-31.
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

**The refund position needs writing.** Requiring a website field kills the "paid
with no website" case, but it validates shape, not existence — typos, dead
domains, parked domains and Facebook pages all pass, and confirming a site
resolves needs a serverless function that still wouldn't prove the business is
auditable. So the refund line covers: dead or typo'd URLs, a social profile where
we needed a website, a business outside our area, duplicate or accidental
payments, someone changing their mind before we start, and a business we look at
and genuinely can't help. It earns its place twice over — **a chargeback costs
more than a refund we control**, and a plain refund line *sells*, the same job
the FAQ's "why trust a company with no case studies?" does.

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
      August** as the deadline. Once it is on a bulk-downloadable register it
      gets copied and mirrored, and amending the ICO's own entry does nothing
      about the copies. In this order:
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

### 1c-2. The name decision — settled 2026-08-04

- [x] **The name is WARDITH** — the owner's call, 2026-08-04, after
      `ops/name-check/` rejected Locito and Tovan. **Deliberately not run for
      WARDITH**, with the reason recorded beside the name in `names.txt`: the
      tool finds occupants, and a free search found none. Reasoning in
      `ops/session-log.md`, 2026-08-04.
- [x] **Domains bought and the site published as Wardith**, 2026-08-04.
      `wardith.co.uk` is the business; `.com` and `.uk` redirect and are never
      published as a contact detail. Every canonical, the sitemap and the JSON-LD
      identity are Wardith. **All three are one-year registrations** — extending
      them is in the owner's calendar for 6 Oct 2026, backstop 4 Jun 2027.
      `ops/accounts.md`.

### 1c-3. What is left of the rename

**The site is live as Wardith.** Full checklist with step-by-step instructions is
`ops/rename-to-wardith.md`; the timetable and money constraints are
`ops/plan-to-1-september.md`.

**Closed, with the consequences that outlive them:**

- [x] **1. Redirects written by hand, 2026-08-06.** Seven explicit 301 rules in
      `netlify.toml`. **Netlify's deploy summary is the regression test — if it
      ever says "No redirect rules processed" again, they are gone.** Read it on
      every deploy that touches `netlify.toml`. The item had assumed making
      `wardith.co.uk` primary reversed every redirect at once; it did not, and
      the check this item told you to run was never carried out — Google's
      validator found the fault instead. **Writing a check down is not doing it.**
- [x] **2. `hello@wardith.co.uk` exists and the site publishes it**, 2026-08-06.
      Zone read independently: MX to `mx.zoho.eu`, exactly one `v=spf1`, a
      `zmail._domainkey` DKIM key, DMARC `p=none` with a live `rua`.
      **One half of the test is still owed and is invisible from the site:**
      nobody has sent *from* the new address and confirmed `SPF: PASS`,
      `DKIM: PASS`, `DMARC: PASS` in a received message's headers. Records
      existing is not authentication passing, and a new domain that fails gets
      filtered silently — in launch week that is indistinguishable from nobody
      replying. `ops/rename-to-wardith.md` D0.4 step 5.
- [x] **3. LinkedIn renamed**, 2026-08-06.
      `https://www.linkedin.com/company/wardith/` is in `business.ts`, so the
      Organization publishes a `sameAs` on all nine pages — **the first surface
      outside this site that corroborates the name.** Both About sections
      rewritten; page confirmed loading without a login.
- [x] **4. Stale public Netlify copies deleted**, 2026-08-06 — and there were
      two, not one. **The lesson is how the second was found: by listing the
      host, not by reading the register.** A surface nobody documented is a
      surface nobody checks.
- [x] **5. Email signature — done 2026-08-07**, replaced rather than re-exported:
      `assets/brand/email-signature.html`, live text with the wordmark as a PNG,
      because email cannot render SVG and its text was outlined paths. **Owner:
      install it in Zoho for new mail and for replies.**
- [x] **6a. Google Search Console — done 2026-08-06.** Domain property verified,
      **Change of Address running to roughly February 2027**; the old property is
      kept permanently because the move runs from it. Sitemap submitted, indexing
      requested on all eight pages, live-URL test passed 2026-08-07.
      `site:novenstudio.co.uk` returned **4** results — **the decay baseline;
      re-run at one month and at six.**
- [x] **6b. Bing Webmaster Tools — done 2026-08-07.** All eight indexable pages
      submitted. **This closes the retrieval side for Copilot.**
      **One loose end, recorded as unknown rather than assumed:** nobody has
      confirmed the sitemap is listed under Bing's Sitemaps panel — URL
      Submission does not require it. Thirty seconds — `ops/own-facts-check.md`
      row 8.

**Submission is not indexation.** Neither console is closed until
`site:wardith.co.uk` returns the eight pages on each. Weekly check.

**Open:**

- [ ] **7. The rest of Phase F** — Zoho Books, Revolut Pro, the ICO record, and
      this repo's own name. `ops/rename-to-wardith.md`.
- [ ] **8. Re-run `ops/own-facts-check.md` end to end** and record the date.
- [ ] **Check Companies House and the trade mark register.** Still not done —
      `find-and-update.company-information.service.gov.uk` refused the
      automated request, and no trade mark search has been run. Neither is
      covered by the name-check tool, which its own README says plainly.
- [ ] **Settle the ICO trading name on the 10 August call**, which is already
      happening for the address. `HANDOVER.md` section 4. One call, two
      problems, and the address is the urgent half — do not let the rename
      delay it.
- [ ] **Find out when `novenstudio.co.uk` expires.** A `[PLACEHOLDER]` in
      `ops/accounts.md`; the rename makes it load-bearing, because that domain
      now has to outlive the change by years to carry the redirects. If it
      lapses the redirects die and the name is free for someone else —
      including the `noven.studio` product in the same field.
- [ ] **The brand assets are a drawing job, not a text edit.** Checked
      2026-08-04: all six SVGs in `assets/brand/` are outlined vector paths
      with zero `<text>` elements, so the wordmark cannot be retyped and the
      monogram cannot be relettered. `ops/rename-to-wardith.md` Phase B.
- [ ] **Expect the old name to outlive the change.** Plan for a period where
      both names are in the world; `novenstudio.co.uk` redirects, never drops.

### 1d. Standing decisions

- [x] Sole trader to begin with, not a limited company.
- [ ] Watch the VAT threshold as revenue grows. The pricing page says we aren't
      registered, so it has to stay true.

### 1d-2. Brand assets — closed but for one flag

Six supplied SVGs are in `assets/brand/` untouched, with trimmed web copies in
`site/public/` (`viewBox` only, no path data altered). Wordmark in the header and
footer, favicon is the circle mark, logo in the structured data, contrast passes
WCAG AA throughout. **Confirmed brand colours: deep navy `#170969`, warm white
`#fffefa`** — the brand is those two and nothing else, lighter tones being the
same two at reduced opacity. The supplied "Favicon" asset is the one thing not to
use; the circle avatar beats it at every size.

- [ ] **The email banner reads "AI Visibility Services"** — category jargon, the
      words a competitor uses rather than a customer. `CLAUDE.md` bans it and
      every page of the site avoids it. Rewrite it in the site's own voice, or
      the first impression contradicts every page it links to.

### 1e. Launch checks — closed

Build verified (7 pages, correct canonicals, JSON-LD parses, sitemap and
robots.txt ship), read on desktop and mobile. Both search consoles done — 1c-3
items 6a and 6b. Old-domain cleanup done: five URLs from whatever occupied the
domain before Noven (`/terms`, `/work`, `/approach`, `/privacy`, `/start`)
submitted for removal and live-tested as 404s. The assistants were asked what
they say about us, via the self-audit — findings in "Where we are today".

---

## Phase 2 — Outreach (how we get the first clients)

We're new with no case studies and the site says so, so we can't win on proof
yet. We win on being specific, being cheap to try, and being obviously not a
scam. **The audit is the outreach tool** — the smallest thing we sell, and the
only one that hands over a finished piece of work before any larger commitment.

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
- [ ] Write the email — short, one specific finding, the audit offer, no chasing
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
- [x] **Publish our own audit — done 2026-08-06.** `/ask-your-ai/` carries the
      argument and `/ask-your-ai/self-audit/` reproduces the 3 August report in
      full, as HTML rather than PDF so the assistants can read it. Competitor
      names withheld and prices removed, both declared on the page.
- [ ] **The "after" half of that page is still empty, and it is the point of
      it.** The `[PLACEHOLDER]` block in the last section of `/ask-your-ai/`
      holds space for the Wardith rerun (Phase 2 of
      `ops/plan-to-1-september.md`, between the 26 August unfreeze and the
      1 September launch). Publish it whichever way it goes — the page already
      commits to that in writing.
- [ ] **Export the client PDF of the self-audit from Word.** The redacted master
      is `ops/audits/noven-2026-08-02/Noven-audit-report-2026-08-03-for-publication.docx`,
      beside the untouched original. `CLAUDE.md` requires the export to come
      from Word rather than a converter. Nothing on the site links a PDF yet, so
      this is additive.

### 2e. Later, only if the above works

Not until there are paying clients and proof.

- [ ] Writing that answers the questions our own customers ask.
- [ ] LinkedIn, or wherever our buyers actually are.
- [ ] [PLACEHOLDER: decide after the first ten conversations]

### 2f. Competitor citation analysis — analysis closed, execution open

**`ops/competitor-analysis.md`**, both parts done 2026-08-07. Headline: **there
is no incumbent.** 41 businesses named, the leader in only 28% of the 165
opportunity rows, and more than a third of answers name nobody. Listicles are the
mechanism — answers citing one name 3.3 businesses, citing none 1.2. What is left
is the six-item execution plan at the end of the doc.

**Two things are settled against and must not be re-proposed:**

- **Any public ranking, "trust score", or named-competitor comparison** —
  parked by the owner on defamation and UK comparative-advertising exposure.
  Read the doc's "Considered and not done" section before raising it. Part 2
  does not reopen it.
- **"Approach the third-party listicles to get listed."** Part 2 fetched all of
  them: agency-published, self-inclusive, no submission route. There is nothing
  to apply to. Read Part 2's Finding C.

**The plays, biggest ticket first. Every one costs nothing and fits inside the
spending freeze.**

- [ ] **Two pricing decisions are now open, and they are the owner's.** The
      assistants quote a **median £1,500/month** — the same median on all three
      — and call £500–£1,500 *freelancer* rates with agency work above. Lead is
      £700. Separately, they put an initial audit at "often £250–£750"; ours is
      at the floor. Written up in `ops/service-tiers.md` §8 with the two things
      they do *not* settle. **Evidence only — an assistant does not move a price.**
- [ ] **Re-run q06–q08 under "Wardith" once indexed — the proof asset.** Under
      "Noven" 0 of 30 runs identified the business. If it flips, it is a dated,
      measured before/after on our own business — the only honest proof a
      months-old business can offer against the £800. Three questions, no cost.
- [ ] **Draft Wardith's own honest comparison page.** Best-evidenced action in
      either part. Needs owner sign-off before `main` — publishing is deploying.
      **Blocked on the brand decision below.**
- [ ] **Answer the question that gets no names.** 62 of 165 answers name no
      business at all. A plain-words page on how to tell a real practitioner
      from a rebranded one. Nothing occupies that ground, and it fits the "you
      don't need us" voice.
- [ ] **List on ThreeBestRated (Wirral) — free, and the only open door found.**
      Already cited by two assistants on the Wirral question. Takes minutes.
- [ ] **Fix `ops/audit-method.md` §5 on Gemini.** All 479 of Gemini's cited
      URLs are opaque `vertexaisearch` redirects — no source analysis is
      possible for it. The method doc lists `sources_cited` without saying so,
      and that feeds client reports. **Promise-accuracy, not housekeeping.**
- [ ] **Open brand decision, asked 2026-08-07, not yet answered.** The
      comparison page is where a buyer arrives holding the industry acronym —
      the case `CLAUDE.md`'s single deliberate exception was written for. That
      exception was granted for **one** FAQ entry, by the owner. Whether it
      stretches to a second page is not an assistant's call. The page does not
      start until this is answered.
- [ ] **Reddit roundup threads — owner's decision, not a default.** Real
      citation weight, real disclosure risk. Not started without an explicit yes.
- [ ] **No product change yet.** Whether a digital-PR/citation line belongs in
      a tier can't be answered from this data. Revisit after the comparison page
      has been live long enough to measure.

---

## Phase 3 — Outcome (actually doing the work we've promised)

**Working when:** we can do an audit and a Foundation to a consistent standard
without reinventing them each time, and a monthly client gets something real
every month.

### 3a. The audit (£250)

Promised on the site: what each assistant says about businesses like theirs;
what they know and believe about this business and whether it's accurate; what's
blocking them, in plain English; and an honest recommendation including "you
don't need us".

**The method was decided on paper 2026-07-30** across `ops/audit-method.md`,
`ops/audit-questions.md`, `ops/audit-site-checklist.md` and
`ops/audit-report-template.md`. **It has been run once, on Noven itself, 2–3
August 2026**, archived at `ops/audits/noven-2026-08-02/`.

- [x] **The questions, the assistants, the rates and the checklist all held up
      in practice.** Ten questions (frozen in `questions.csv`), 210 API runs
      across ChatGPT/Gemini/Perplexity plus 18 hand runs across Copilot/Google,
      reported as bands with the raw count, never a percentage. **The audit's ten
      become the client's tracked ten** on a monthly plan, frozen for twelve
      months once agreed.
- [x] **The report template held, with one gap fixed live: Rule 10.** A report
      listing only faults can't tell a client "your site is fine" from "we
      didn't look." Every report now covers all four checklist groups and states
      what's already right. Length raised to **1,200–1,800** words.
- [x] **Verdict C fires correctly but is documented too narrowly — not yet
      fixed.** `checklist.md` and `ops/audit-report-template.md` both describe
      C as a broken-*site* problem. Noven's site passes nearly everything and
      still verdicts C, because the blocker is identity. **Needs an edit to
      the C definition, not a new verdict.**

**The three method faults the self-audit surfaced, none fixed:**

- [ ] **Fix the cost estimate.** `ops/audit-setup.md` §6 says ~£1.20 per 150
      queries. OpenAI alone cost $12.63 for ~75 queries on the real run;
      Gemini's and Perplexity's totals were never captured. Get those two
      figures, correct §6, then re-check whether Maintain's £150/month
      (`ops/service-tiers.md` §11) still holds at the real cost.
- [ ] **Archive the run data on every future audit, before the report is
      written.** `runs-clean.csv` — the 210 rows every number in the Noven
      report traces to — lived only on the owner's machine during the run.
      **Nothing in the archived report has actually been checked against source
      data.** Make this step 1 of the report stage, not an afterthought.
- [ ] **Run the off-site half of checklist group 3 next time** — Google Business
      Profile, Bing Places, Companies House, directories, review counts. Skipped
      on the Noven run and disclosed as a gap; the report itself says this is
      usually where the most fixable findings turn up.

- [ ] **Total time still isn't known.** The on-site checklist alone took ~25
      minutes (group 3 not started); nothing records how long the API run,
      classification and report-writing took end to end. This is the one
      number `ops/service-tiers.md` §11's pricing rests on — see 3c.
- [ ] **Build the runner.** Still deliberately deferred — written now it would
      be a transcription of `audit_query.py`, the exact script archived with
      the Noven run, rather than a guess at a format. **Not on the critical
      path.**
- [ ] Rewrite the process based on what the first one taught us, once the
      items above are closed.
- [x] **The two extra intake questions are live on `contact.astro`** (2026-07-31),
      both optional: "what do people usually ask when they first get in touch?"
      and "roughly what is a new customer worth to you?" — the first is the only
      input we can't derive ourselves; the second lets the report say what being
      missing costs. Carry both onto the order page when it's built.

### 3b. The Foundation (£800)

Promised: crawler access, structured machine-readable facts, consistent facts
across the web, and pages that answer customer questions — all on the client's
existing site. We don't build websites.

- [D] **The scope is fixed and published** (2026-07-31): crawler access,
      structured data, facts made consistent across the web, and **two** permanent
      answer pages. The audit picks which two. Work found outside the four is
      quoted, not absorbed.
- [ ] Write the Foundation checklist. **Largely written already** —
      `ops/audit-site-checklist.md` is the same list from the diagnosis side.
      What's owed is the *how* of doing the work, not the *what*.
- [ ] **Put a time budget on it.** Still the only product in the business with
      no estimate of how long it takes, which is what makes its margin unknown.
      Time the first one.
- [ ] How we get access safely, and what we do when we can't. **Ask in two
      stages:** the Foundation asks for access *to do the setup*; a monthly plan
      is where we ask to keep it. A "no" to the second mustn't threaten the
      first. `ops/service-tiers.md` section 3.
- [ ] What happens when the site is too broken for the Foundation to help. **The
      audit's three verdicts already decide this** — what's left is what we do
      next, and what we refund.
- [ ] What we hand over at the end, and how we show what changed.
- [ ] Do the first one, time it, then fix the process.

### 3c. Monthly plans (£150 / £400 / £700)

**Published on the site — `ops/service-tiers.md` has the reasoning.** Three
verbs, not three intensities: Maintain holds your position, Grow closes the gaps,
Lead beats the competitors named ahead of you. **The upgrade engine is the
monthly record itself** — it reports the gaps and doesn't close them, so nobody
has to sell anything.

**The tiers separate on answer pages** — 0 / 1 / 2 a month — rather than on
question volume, which rises gently at 10 / 15 / 25. Question volume is pure cost
to us; a page is a permanent asset to the client. That structure was set
2026-07-31 (§9); **the prices above are §11's, set 2026-08-05.**

- [D] What happens each month at each level — live on the pricing page, in
      how-it-works and in the structured data. **Never yet delivered to anyone.**
- [D] **We publish the answer pages**, client approves the words. Structured data
      doesn't survive copy-paste, so the client-publishes path costs more time
      and delivers a worse page.
- [D] **What an answer page is** — one question, one permanent page, one URL,
      built from facts only that business has. Not a blog post, not an FAQ entry.
      Every Foundation is practice for Grow.
- [x] **The monthly record has a format** — `ops/monthly-record-template.md`
      (2026-07-31). One page, four sections, bands not percentages, and a hard
      rule that a provider's model change is flagged at the top so the client
      doesn't read it as their own decline.
- [ ] **Validate the numbers by doing it — the key number is still missing.**
      The Noven self-audit ran the method once but didn't record total time end
      to end, and its one hard cost figure (OpenAI: $12.63 for ~75 queries) is
      roughly ten times the estimate this pricing was set from. **At an hour a
      month Maintain scales past twenty clients; at three it caps the business
      around eight.** Time the next run properly, or extract timing from the
      first real client audit.
- [ ] **Write the publishing fallback into onboarding** — where we can't get
      publish rights, hand over a complete file with the structured data intact
      plus a one-page paste instruction, then verify it live. That verification
      is billable time inside the plan, not a favour.
- [ ] Define the quarterly review promised on Lead. Deliberately not written yet
      — no Lead client exists, and guessing at what they want to know is how the
      rest of this repo got ahead of itself.
- [ ] Work out how many clients one person can hold at each level.

### 3d. Keeping track of clients

`ops/client-record.md` holds this. A spreadsheet is fine until it isn't — the
trigger to move to something else (Zoho Bigin free tier) is when you can't answer
"who's due a check this week" by looking, usually five to eight clients.

- [x] **The fields are decided and written down** — `ops/client-record.md`
      (2026-07-31), for clients and, separately and more sparsely, for prospects.
- [ ] **Choose the storage.** Still the blocker, and it blocks two things: the
      client record and the audit folders. **Shape decided** in
      `ops/audit-method.md` section 5 — one folder per client per audit. The hard
      constraint is that **it is not this repo**, which holds no personal data
      and is written as if public. One named provider, encryption at rest, and a
      backup that has been restored once.
- [ ] **Decide a retention period and write it into the privacy notice** rather
      than deciding it twice. Recommendation: life of the relationship plus
      twelve months, then delete.

---

## Open questions for the owner

- Which trade and which area do we go after first? Being in the Wirral gives us
  a credible local answer, and a local first client is far easier to get than a
  cold national one.
- How much time per week is there for delivery? This caps everything.
- Is there any existing contact who could be client number one?
- **The brand decision in 2f**, asked 2026-08-07 and still open: does the
  single deliberate acronym exception stretch to a second page?
