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
every session and update it at the end.

**Where the reasoning lives:** `ops/session-log.md` holds the full record of why
each decision went the way it did, newest first. Closed items here are one line
and a pointer; go to the log or the `ops/` doc when you need the argument.
Don't re-argue a settled decision from the summary.

**How we're working:** build the minimum needed to take a real client, then let
real client work tell us what to build next. We don't design processes for
situations we haven't met yet. Anything we don't know is written as
`[PLACEHOLDER]` rather than guessed. The three phases overlap.

**The three markers, and the difference between the first two matters more than
anything else in this file:**

- `[x]` — **done, and true in the world.** The bank account exists. The ICO has
  our money. The sitemap is submitted.
- `[D]` — **decided on paper, never yet performed.** A document describing an
  intention. The audit method is `[D]`. Every monthly plan is `[D]`. A reader
  scanning ticks and finding `[x]` against a decision concludes the business does
  something it has never done once, which is how this file misled people before
  the marker existed.
- `[ ]` — open.

`ops/audit-method.md` has always got this right in its own header —
*"decided on paper, unvalidated in practice"*. The markers carry that
distinction everywhere else.

---

## Where we are today

**The site is live** at `wardith.co.uk`, on HTTPS, deployed from `main` by
Netlify: nine static pages, readable by AI crawlers, with machine-readable
business facts and a sitemap. **Search Console has a verified Domain property
for `wardith.co.uk` as of 2026-08-06 and the Change of Address is running** —
the rename did not carry the old property over, because a property is bound to
the host it was verified for. **Bing is still not set up**, and it is now the
more urgent of the two: Copilot answers from it and it has never indexed this
business under either name. `ops/search-console-and-bing.md`. Email is
**`hello@wardith.co.uk` on Zoho** — created and confirmed receiving
2026-08-06, and published on the site the same day. The brand assets are in and the palette
matches them. **Phase 1a and 1b are closed.**

### What changed on 2026-08-06, and the one thing it should change about how you work

**The session started from "assistants asked to review `wardith.co.uk` still
answer Noven" and ended up finding four wrong claims in this repo.** Full
reasoning in `ops/session-log.md`; the short version, because it affects what
you can trust in these files:

| Claim | Reality |
|---|---|
| `hello@wardith.co.uk` "live on Zoho, tested both directions" — in six files | Had never been created. Now real, and the site publishes it |
| Search Console "already set up, nothing to do" | A property is bound to its host; the live domain had none |
| "Sitemap submitted and confirmed, six pages" | Six URLs *read from a sitemap*, not six pages indexed |
| **"No redirect rules need writing — Netlify 301s non-primary domains"** | **It did not. The whole site was being served at four addresses for nine days** |

**The redirect one is the one to understand.** `novenstudio.co.uk` was not
redirecting — it was serving the Wardith site at its own address. So a crawler
reaching the old domain found the new business sitting there under the old name:
not a stale mention, a live statement that the two are one site. Seven explicit
301 rules are now in `netlify.toml`, and Netlify's deploy summary is the
regression test — **if it ever says "No redirect rules processed" again, they
are gone.**

**Three of the four came from a sentence written before a change and never
re-tested after it, and the fourth from publishing something unchecked.** Those
need different habits: re-read anything marked done before 4 August, and verify
anything new against the world rather than against another document. **Every one
was caught by something outside this repo refusing to agree with it** — Google's
validator, a browser address bar, the owner's memory. Nothing inside caught any
of them, because the repo was what made the claims.

**Also closed that day:** the LinkedIn company page renamed and published as
`sameAs` (the first surface outside this site corroborating the name), both
About sections rewritten, two stale public Netlify copies deleted, all three
visible `[PLACEHOLDER]` blocks taken off the site, and Change of Address
accepted.

---

**The Noven self-audit has run** — 2–3 August 2026, archived at
`ops/audits/noven-2026-08-02/`. This is the biggest change since this file was
last written, and it reorders what's next more than any single item below it.

**The result: verdict C, and not for the reason the method expected.**
`checklist.md` and the report template both describe C as a broken-*site*
problem — no website, a Facebook page standing in, a site that can't take
structured data. Noven's site is the opposite of all three and still verdicts
C, because the blocker is **identity, not the site**:

1. **"Noven" belongs to somebody else, at least four times over** — a Miami
   pharmaceutical company, a North West builder, and (most damaging) an AI
   product trading as `noven.studio`, a name that is ours with the dot moved,
   working in the same field. Asked "what do you know about Noven" thirty times
   across three assistants, **every answer described the pharma company.**
   Asked the harder question naming the Wirral, ChatGPT still named the builder
   four times out of five. Not one of 210 automated answers cited
   `novenstudio.co.uk`.
2. **Copilot has no record of the site at all** — `site:novenstudio.co.uk`
   returns nothing on Bing, which is what Copilot retrieves from. Free to fix,
   ~15 minutes, days to weeks to take effect.
3. **Nothing tells a machine where the business works.** The pages say "the
   Wirral"; the structured data says only `GB`. Cost all 15 checks that asked
   for someone on the Wirral.

**The report's own recommendation: fix the name before anything else.** No
amount of website work — including the Foundation — stops an assistant
believing Noven is a pharmaceutical company, and every future improvement under
the current name accrues to a name at least three other businesses already
answer to. Findings 2 and 3 are ordinary, fast Foundation-shaped fixes. Finding
1 isn't, and it now sits ahead of everything else in this file — see 1c-2.

**Finding 1 is answered as of 2026-08-04: the name is WARDITH.** Built from the
owner's own name — the back half of *Edward*, the back half of *Smith*. It is
the third candidate. `ops/name-check/` ran on the first two and killed both:
Locito collided 12 times out of 12 with Localito Marketplace Ltd and the Lockito
app; Tovan collided 11 times out of 12 with Tovan.ai and two registered
companies. WARDITH has no occupant to collide with — no company, product or
brand of that name exists — so the tool was deliberately not run on it, which is
argued out in `ops/session-log.md`, 2026-08-04, rather than left looking like a
skipped step.

**The rename is done, as of 2026-08-06.** This paragraph used to say "almost
none of the rename is done — the domain is not bought, and everything from the
canonicals to both LinkedIn pages still says Noven". All of that was true when
written on 4 August and none of it is true now. Domains bought, site published,
LinkedIn renamed, mail moved, redirects written, Search Console migrated.

**Still not done from that paragraph: Companies House and the trade mark
register have never been checked.** That is the one piece of the name decision
that remains open, it is free, and it is listed below.

**Two method faults the audit surfaced, neither fixed yet:**

- **The cost estimate in `ops/audit-setup.md` §6 is wrong.** It budgets ~£1.20
  per 150 queries. OpenAI alone billed **$12.63** for ~75 queries; Gemini's and
  Perplexity's totals were never recorded. This bears directly on whether
  Maintain's £95/month is priced correctly.
- **The raw answer data was never archived.** `runs-clean.csv` — the 210 rows
  every figure in the report traces to — existed only on the owner's machine
  during the run and isn't in the audit folder. Nothing in the report has
  actually been checked against source data.
- **Off-site checklist group 3 was skipped** — Google Business Profile, Bing
  Places, Companies House, directories, review counts. Disclosed in the report
  rather than hidden; usually where the most fixable findings live. A paying
  client's audit shouldn't repeat the omission.

**Also done in the 2026-08-03 session:** report template Rule 10 — every report must now say
what a business is getting right, not only what's wrong — applied retroactively
to the archived Noven report; and a new `CLAUDE.md` rule that documents meant
for a person (client reports, quotes, invoices) are Office files with the PDF
exported from Word, which is why the archive holds both `report.md` and a
`.docx`.

**Unchanged since 1 August, and still gating a live pay button — two things
blocking, both about an address:**

1. **The ICO published, or is about to publish, the owner's home address** on a
   bulk-downloadable public register. Time-critical — deadline **Monday 10
   August 2026** — see 1c.
2. **The service address hasn't landed.** V LOT took payment and may have
   delivered nothing. It blocks the ICO fix, the site footer, and the audit's
   pay button.

Nothing in the last three days' work touched the ICO call, the service address,
the terms of service, the privacy notice or the payment link — see 1c below.

**`ops/session-log.md` has a gap of its own:** no entry exists for the audit
run, the archiving, or the name-check tool, breaking the file's own rule ("add
an entry at the end of each session") at the point the record matters most.

**The critical path now:** the name decision (`ops/name-check/`, no cost,
blocks identity, see 1c-2) → ICO helpline call (deadline Mon 10 Aug) → service
address ordered → terms and privacy notice written → one payment possible end
to end. **Free and not blocking anything, so do it whenever:** register with
Bing Webmaster Tools (closes finding 2).

**Finding 3 was on that list until 2026-08-06 and has been taken off it: it is
not free and it is not independent.** Adding a location to the structured data
was tried that day and reverted within the hour. The footer of every page
carries a visible `[PLACEHOLDER: address for service of documents]`, so a
`PostalAddress` in the head — even locality-only — has the page telling a reader
it has no address and a machine that it has one, which is the drift this site
says is impossible. It would also have committed us to "Merseyside" before the
address for service exists, and the fallback providers are not on the Wirral.

**Finding 3 is therefore blocked on the address for service**, and closes with
it rather than before it: whatever lands is a real postal address, is not the
founder's home, and has to be published by law anyway, so it fills the footer
placeholder and the structured data from one fact. Reasoning in
`ops/session-log.md`, 2026-08-06, and in the note left in `schema.ts` where the
block would go. The order page is still not on this path —
a payment link in an email takes the first payment. `HANDOVER.md` has the
longer version, written for someone with no context — **not yet updated to
match this section.**

---

## Phase 1 — Build (get to a site that can take a real customer)

**Done when:** a stranger can read the site, understand the offer, email us, and
pay us £125.

### 1a. Facts only the owner can supply — closed

All live on the site and in the structured data: `hello@wardith.co.uk` (created
2026-08-06; the old Gmail and `hello@novenstudio.co.uk` both keep receiving, and
will for months); no phone, email only, and the site
says why; reply within two working days; the Wirral, serving the UK remotely;
Kieran Smith, sole trader, no company number, not VAT registered; the audit
report within two working days of scope and payment being confirmed (moved from
one working day on 2026-07-31 — `ops/audit-method.md` section 7 says why), and a
Foundation plan within two working days of payment clearing. Founder bio,
photograph, LinkedIn profile and Maersk as `alumniOf` are all in. The LinkedIn
setup is done — profile amended, company page live. **`businessLinkedIn` was
deliberately `null` from 2026-08-04 and is set as of 2026-08-06** to
`https://www.linkedin.com/company/wardith/`, supplied by the owner once the
page was renamed. Holding it null through the rename was right: renaming the
page changed its slug, so a value set earlier would have been a false
machine-readable claim rather than a broken link. The Organization now
publishes one `sameAs` on all nine pages — **the first surface outside this
site that corroborates the name.** **But the copy on both LinkedIn About sections predates the 31 July
repricing and still publishes the old prices**, so `ops/linkedin.md` was
reopened on 2026-08-01 for a repaste — see `ops/own-facts-check.md`.

**Cancellation terms**, live on three pages: monthly plans roll month to month,
no minimum term, **no notice period**; the month already paid for runs out, no
part-month refunds. Chosen against the agency norm because a notice period costs
more in friction than it recovers at £95–495, and the Foundation being a
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

`wardith.co.uk` owned and set in `astro.config.mjs` and `robots.txt`. Apex is
primary, `www` redirects to it. Netlify deploys `main`; HTTPS confirmed via
Netlify's API. Nothing to redirect — the domain only ever hosted the owner's own
projects. **`hello@novenstudio.co.uk` is live on Zoho Mail** (Mail Lite, DNS at
Namecheap, MX to `mx.zoho.eu`, SPF, DKIM, `p=none` DMARC), tested both
directions; setup and failure checks in `ops/zoho-mail-setup.md`.
**`hello@wardith.co.uk` does not exist yet** — 1c-3. This line said it did until
2026-08-06; see the correction note at the top of `ops/own-facts-check.md` §2.

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
      delivered after payment.** Don't tick this off until post through the
      address is confirmed working; fall back to 1st Formations or Quality
      Company Formations (~£115/yr inc VAT) if it doesn't land.

      **The footer placeholder is gone as of 2026-08-06, by the owner's
      decision, and this instruction used to say the opposite.** It read "don't
      remove the footer placeholder until post through the address is confirmed
      working". Overridden on the eve of submitting the domain to Search Console
      and Bing: what stood in the footer of all nine pages published the literal
      token `[PLACEHOLDER`, named an internal repo file, and stated in writing
      that a legal disclosure requirement had not been met. Indexed and repeated
      by an assistant, that is a red flag handed to a prospect by the business's
      own site — and the whole product is finding that fault on other people's.

      **What replaces it is a commitment, not a tick: the address is published
      before the first customer is onboarded.** Nothing on the site takes a
      payment yet, which is what makes the removal defensible rather than
      convenient. **The reminder is now a source comment in `Base.astro` and
      this paragraph, and both are weaker than nine visible pages were.** That
      is the cost of the decision and it is the owner's to carry. **Never the home address:** this site is built so crawlers
      read the business facts and repeat them confidently, which works against
      us on exactly this field, and it is a one-way door — the footer can be
      edited, indexes and archives cannot.

#### Before money changes hands

- [D] **The £125 audit is paid on the website, upfront**, through our own order
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
      **Not on the critical path** — see "Where we are today" above. A payment
      link in an email takes the first payment, and this page is a scaling tool
      for roughly sale five onward. Still blocked behind the terms, the privacy notice and
      the address whenever it is built.
- [D] **The £750 Foundation is invoiced**, with the contract sent alongside once
      both sides agree to start. At £750 the card fee is real money, there's
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

### 1c-2. The name decision — settled 2026-08-04. The rename is not

The self-audit's finding 1 (see "Where we are today") made this a
prerequisite for further investment in the current identity, not a
someday-decision. The report's own words: **"the honest order is the name
first, then the rest."**

- [x] **Decide whether Noven keeps its name.** It does not. **The name is
      WARDITH** — the owner's call, 2026-08-04, after Locito and Tovan were
      shortlisted and both rejected by `ops/name-check/`. Reasoning in
      `ops/session-log.md`, 2026-08-04.
- [x] **Run candidates through `ops/name-check/` before anything else touches
      them.** Done for Locito and Tovan, both rejected. **Deliberately not run
      for WARDITH**, and the reason is written into `names.txt` beside the
      name: the tool finds occupants, a free search found no occupant, so the
      queries would only confirm what was already known. That exception is
      recorded rather than quietly taken.

- [x] **Buy the domain.** `wardith.co.uk`, `wardith.com` and `wardith.uk`, all
      three at GoDaddy on 2026-08-04, **one year only**. Extending them to a
      long term is in the owner's calendar for 6 Oct 2026, with a backstop on
      4 Jun 2027 — the first dated obligation in this business to exist outside
      a markdown table. Recorded in `ops/accounts.md`.

- [x] **Decide which of the three domains the business *is*.** `wardith.co.uk`,
      owner's call 2026-08-04. `.com` and `.uk` are owned and redirecting and
      are never published as a contact detail.
- [x] **Publish the site as Wardith.** Merged to `main` on 2026-08-04, so the
      live site, every canonical, the sitemap and the JSON-LD identity are all
      Wardith on `wardith.co.uk`. DNS, TLS and the page-for-page redirects are
      verified working on all three new domains.

---

### 1c-3. What is left of the rename — **start a new session here**

**The site is live as Wardith. These are the open items, in order.** The full
checklist with step-by-step instructions is `ops/rename-to-wardith.md`; the
timetable and the money constraints are `ops/plan-to-1-september.md`.

**Do these two first. Both are on the critical path and both are free.**

- [x] **1. DONE — `wardith.co.uk` is primary in Netlify, and the redirects it
      was assumed to bring were written by hand on 2026-08-06.** This item said
      flipping the primary "reverses every redirect at once and completes the
      switch". **It did not.** For nine days afterwards `novenstudio.co.uk`,
      `wardith.com` and `wardith.uk` all *served* the full site at their own
      addresses with no redirect at all. Seven explicit 301 rules now live in
      `netlify.toml`.

      **The instruction in this item's own last sentence — verify the direction
      actually flipped with a real request to a real inner page — was right and
      was never carried out.** Writing a check down is not doing it. Google's
      Change of Address validator eventually found it. `ops/rename-to-wardith.md`
      D3.
- [x] **2. DONE 2026-08-06. `hello@wardith.co.uk` exists and the site
      publishes it.** The owner created the alias and confirmed mail arrives in
      the Zoho inbox; the zone was then read independently — MX to `mx.zoho.eu`,
      exactly one `v=spf1`, a `zmail._domainkey` DKIM key, and DMARC `p=none`
      whose `rua` now points at a mailbox that exists rather than one that did
      not. `business.ts` flipped the same day.

      **Holding the old address on the site for two days after the rename was
      right** — a working address on the dead domain beats a bouncing one on the
      live domain, and it is the only inbound channel on a business with no
      phone and no form.

      **One half of the test is still owed and is invisible from the site:**
      nobody has sent *from* the new address and confirmed `SPF: PASS`,
      `DKIM: PASS`, `DMARC: PASS` in a received message's headers. Records
      existing is not the same as authentication passing, and a new domain that
      fails it gets filtered silently — which in launch week is
      indistinguishable from nobody replying. `ops/rename-to-wardith.md` D0.4
      step 5.

**Then these.**

- [x] **3. LinkedIn: the page is renamed and the slug is ours.**
      `https://www.linkedin.com/company/wardith/` — supplied 2026-08-06 and set
      in `business.ts`, so the Organization publishes a `sameAs` on all nine
      pages — **the first surface outside this site that corroborates the
      name.** Cover and logo PNGs in `assets/linkedin/` were rebuilt for Wardith
      and re-verified against their sources.

      **One thing left in the same job:** check the About sections do not still
      show `hello@novenstudio.co.uk`. They were rewritten before
      `hello@wardith.co.uk` existed.

      **Both closed 2026-08-06.** The owner rewrote both About sections — no
      Noven, prices matching the site — and confirmed in a private window that
      the company page loads without a login, which is the one thing a `sameAs`
      needs to be worth anything to a crawler.
- [x] **4. DONE 2026-08-06 — and there were two, not one.** `noven-2-0-preview`
      was a full Noven-branded copy of the business, public with no password.
      Listing the Netlify team turned up a second, `aesthetic-unicorn-619923`,
      which appeared in no operating document at all. Both deleted; one project
      remains, serving `wardith.co.uk`. **The lesson is how the second was
      found — by listing the host, not by reading the register.** A surface
      nobody documented is a surface nobody checks.
- [ ] **5. Re-export `Email Signature.svg` on one domain.** It reads
      `hello@wardith.com` above `wardith.co.uk`. Do not use it until fixed.
- [x] **6a. Google Search Console — done 2026-08-06.** `wardith.co.uk` verified
      as a Domain property through GoDaddy Domain Connect, and **Change of
      Address accepted and running to roughly February 2027.** The old property
      is kept permanently: the move runs from it, and it holds half the
      six-month measurement. `site:novenstudio.co.uk` returned **4** results,
      which is now the decay baseline — re-run it at one month and at six.
      Sitemap, live-URL test and indexing requests still to confirm.
- [ ] **6b. Bing Webmaster Tools — still not done, and now the single highest
      -leverage free job left.** Copilot answers from Bing and Bing has never
      indexed this business under either name, so there is nothing to migrate
      and no equity at risk — a clean first submission. Its URL Submission tool
      takes all eight pages at once where Google's request-indexing is rationed.
      **`ops/search-console-and-bing.md` part 2**, which is written and
      unstarted.
- [ ] **7. The rest of Phase F** — Zoho Books, Revolut Pro, the ICO record, and
      this repo's own name. `ops/rename-to-wardith.md`.
- [ ] **8. Re-run `ops/own-facts-check.md` end to end** and record the date.

**Still open from before the rename, and unchanged by it:**

- [ ] **Check Companies House and the trade mark register.** Still not done —
      `find-and-update.company-information.service.gov.uk` refused the
      automated request, and no trade mark search has been run. Neither is
      covered by the name-check tool, which its own README says plainly.
- [ ] **Settle the ICO trading name on the 10 August call**, which is already
      happening for the address. `HANDOVER.md` section 4. One call, two
      problems, and the address is the urgent half — do not let the rename
      delay it.
- [ ] **Find out when `novenstudio.co.uk` expires.** It was already a
      `[PLACEHOLDER]` in `ops/accounts.md`; the rename makes it load-bearing,
      because that domain now has to outlive the change by years to carry the
      redirects. If it lapses the redirects die and the name is free for
      someone else — including the `noven.studio` product in the same field.
- [ ] **The brand assets are a drawing job, not a text edit.** Checked
      2026-08-04: all six SVGs in `assets/brand/` are outlined vector paths
      with zero `<text>` elements, so the wordmark cannot be retyped and the
      monogram cannot be relettered. `ops/rename-to-wardith.md` Phase B.
- [ ] **Expect the old name to outlive the change.** `ops/own-facts-check.md`
      exists because facts persist after they are corrected, and the self-audit
      measured exactly that. Plan for a period where both names are in the
      world, and decide what `novenstudio.co.uk` does — redirect, not drop.

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
- [x] **Sitemap submitted and confirmed in Search Console — for the *old*
      domain, and "6 pages" means less than it reads.** It is the sitemap being
      processed and six URLs read from it, not six pages indexed. Corrected
      2026-08-06 after this line was used to conclude the indexation job was
      done; a Search Console property is bound to its host, so none of this
      carried to `wardith.co.uk`, which needed a new property. See 1c-6a.

      Five URLs from whatever occupied the domain before Noven (`/terms`,
      `/work`, `/approach`, `/privacy`, `/start`) were submitted for removal and
      live-tested as 404s. **`/approach` was still in Google's index on
      2026-08-06** — `site:novenstudio.co.uk` returns 4 results, which is now
      the decay baseline for the six-month re-check.
- [ ] **Bing Webmaster Tools — still not done, and now a named finding, not a
      guess.** The self-audit confirmed Copilot holds no record of the site at
      all (`site:novenstudio.co.uk` returns nothing on Bing). Free, ~15
      minutes, days to weeks to take effect.
- [x] **Ask the assistants what they say about Noven — done, via the self-audit
      (3a), 2–3 August 2026.** Not the result hoped for: not named once across
      210 automated answers, and every "what do you know about Noven" answer
      described a Miami pharmaceutical company. Full findings in "Where we are
      today" above.

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
      full, as HTML rather than as a PDF so that the assistants can actually
      read it. Names of the eleven competitors withheld, old prices left as
      written with a correction beside them, both declared on the page.
      Reasoning in `ops/session-log.md`, 2026-08-06.
- [ ] **The "after" half of that page is still empty, and it is the point of
      it.** The `[PLACEHOLDER]` block in the last section of `/ask-your-ai/`
      holds space for the Wardith rerun (2c/Phase 2 of
      `ops/plan-to-1-september.md`, between the 26 August unfreeze and the
      1 September launch). Publish it whichever way it goes — the page already
      commits to that in writing.
- [ ] **Export the client PDF of the self-audit from Word.** The redacted master
      is `ops/audits/noven-2026-08-02/Noven-audit-report-2026-08-03-for-publication.docx`,
      beside the untouched original. `CLAUDE.md` requires the export to come
      from Word rather than a converter. Nothing on the site links a PDF yet, so
      this is additive — add the download to `/ask-your-ai/` once the file
      exists.

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

### 3a. The audit (£125)

Promised on the site: what each assistant says about businesses like theirs;
what they know and believe about this business and whether it's accurate; what's
blocking them, in plain English; and an honest recommendation including "you
don't need us".

**The method was decided on paper 2026-07-30, across four docs:**
`ops/audit-method.md` (decisions and reasoning), `ops/audit-questions.md` (the
question set), `ops/audit-site-checklist.md` (the working checklist),
`ops/audit-report-template.md` (what the client gets). **It has now been run
once, on Noven itself, 2–3 August 2026** — archived at
`ops/audits/noven-2026-08-02/` (report, working checklist, the exact script
used, and the report as a Word document). Full result in "Where we are today"
above; what the run confirmed or changed about the method is below.

- [x] **The questions, the assistants, the rates and the checklist all held up
      in practice.** Ten questions (frozen in `questions.csv`), 210 API runs
      across ChatGPT/Gemini/Perplexity plus 18 hand runs across Copilot/Google,
      reported as bands with the raw count, never a percentage. No structural
      change needed to any of these. **The audit's ten become the client's
      tracked ten** on a monthly plan, frozen for twelve months once agreed.
- [x] **The report template mostly held, with one gap fixed live: Rule 10.**
      The first draft listed only faults; a report that does that can't tell a
      client "your site is fine" from "we didn't look." Every report now
      covers all four checklist groups and states what's already right, not
      only what's wrong. Length raised 1,000–1,600 → **1,200–1,800** words.
      Applied retroactively to the archived Noven report.
- [x] **Verdict C fires correctly but is documented too narrowly — not yet
      fixed.** `checklist.md` and `ops/audit-report-template.md` both describe
      C as a broken-*site* problem. Noven's site passes nearly everything and
      still verdicts C, because the blocker is identity. **Needs an edit to
      the C definition, not a new verdict.**
- [ ] **Fix the cost estimate.** `ops/audit-setup.md` §6 says ~£1.20 per 150
      queries. OpenAI alone cost $12.63 for ~75 queries on the real run;
      Gemini's and Perplexity's totals were never captured. Get those two
      figures, correct §6, then re-check whether Maintain's £95/month
      (`ops/service-tiers.md` section 9) still holds at the real cost.
- [ ] **Archive the run data on every future audit, before the report is
      written.** `runs-clean.csv` — the 210 rows every number in the Noven
      report traces to — was never saved into the audit folder; it lived only
      on the owner's machine during the run. Nothing in the archived report has
      actually been checked against source data. Make this step 1 of the
      report stage, not an afterthought.
- [ ] **Run the off-site half of checklist group 3 next time** — Google
      Business Profile, Bing Places, Companies House, directories, review
      counts. Skipped on the Noven run and disclosed in the report as a gap;
      the report itself says this is usually where the most fixable findings
      turn up. A paying client's audit shouldn't skip it.
- [ ] **Total time still isn't known.** The on-site checklist alone took ~25
      minutes (group 3 not started); nothing records how long the API run,
      classification and report-writing took end to end. This is the one
      number `ops/service-tiers.md` section 9's pricing rests on, and the
      self-audit was supposed to produce it. It still hasn't — see 3c.
- [ ] **Build the runner.** Still deliberately deferred — written now it would
      be a transcription of `audit_query.py`, the exact script archived with
      the Noven run, rather than a guess at a format. **Not on the critical
      path.**
- [ ] Rewrite the process based on what the first one taught us, once the
      items above are closed.
- [x] **The two extra intake questions are live on `contact.astro`** (2026-07-31),
      both optional: "what do people usually ask when they first get in touch?"
      — the only input we can't derive ourselves, and the difference between
      questions in the client's customers' words and ours — and "roughly what is
      a new customer worth to you?", which lets the report say what being missing
      costs rather than only that it happens. Carry both onto the order page when
      it's built.

### 3b. The Foundation (£750)

Promised: crawler access, structured machine-readable facts, consistent facts
across the web, and pages that answer customer questions — all on the client's
existing site. We don't build websites.

- [D] **The scope is now fixed, and published** (2026-07-31): crawler access,
      structured data, facts made consistent across the web, and **two** permanent
      answer pages. `how-it-works.astro` used to promise "key pages" — plural,
      unbounded — with no time budget for the Foundation anywhere in this repo,
      which is what made £350 an open-ended commitment. The audit picks which two
      pages. Work found outside the four is quoted, not absorbed.
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

### 3c. Monthly plans (£95 / £250 / £495)

**Published on the site — `ops/service-tiers.md` has the reasoning.** Three
verbs, not three intensities: Maintain holds your position, Grow closes the gaps,
Lead beats the competitors named ahead of you. **The upgrade engine is the
monthly record itself** — it reports the gaps and doesn't close them, so nobody
has to sell anything.

**Repriced 2026-07-31** (`ops/service-tiers.md` section 9). The tiers now
separate on **answer pages** — 0 / 1 / 2 a month — rather than on question
volume, which rises gently at 10 / 15 / 25 instead of doubling. The old ladder
paid less per hour at every step up, because question volume is pure cost to us
and a page is a permanent asset to the client. Lead's fortnightly cadence is
gone.

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
      doesn't read it as their own decline. This closes "decide how we check and
      report visibility each month" and "write the monthly client update", which
      were two descriptions of the same missing document.
- [ ] **Validate the numbers by doing it — partially done, and the key number
      is still missing.** The Noven self-audit (3a) ran the method once but
      didn't record total time end to end, and its one hard cost figure
      (OpenAI: $12.63 for ~75 queries) is roughly ten times the ~£1.20/150
      estimate this pricing was set from. The Maintain figure still isn't
      known: at an hour a month it scales past twenty clients, at three it
      caps the business around eight. Time the next run properly, or extract
      timing from the first real client audit.
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
      Formerly `ops/spine.md`, a three-line stub whose name gave a stranger no
      clue what it was for.
- [ ] **Choose the storage.** Still the blocker, and it now blocks two things:
      the client record and the audit folders. **Shape decided** in
      `ops/audit-method.md` section 5 — one folder per client per audit. The hard
      constraint is that **it is not this repo**, which is public and would hold
      personal data. One named provider, encryption at rest, and a backup that
      has been restored once.
- [ ] **Decide a retention period and write it into the privacy notice** rather
      than deciding it twice. Recommendation: life of the relationship plus
      twelve months, then delete.

### 3e. The internal docs

- [x] **Resolved 2026-07-31.** `ops/org-chart.md` (five company seats) and
      `ops/escalation-rules.md` (three "never do this without me" rules) are
      **deleted**, not deferred. Both described a business with employees and
      someone to escalate to; this one has neither, and `CLAUDE.md` already does
      the escalation job. An empty file is not a deferral — it reads as
      permanent debt on every future reader's list. Write either one if it ever
      becomes real.
- [x] `ops/spine.md` → `ops/client-record.md`, filled in — see 3d.

---

## Open questions for the owner

- **Does Noven keep its name?** The self-audit found "Noven" resolves to at
  least three other businesses an assistant already knows, one of them
  (`noven.studio`) in the same field. `ops/name-check/` is built and waiting to
  test candidates. This now blocks further investment in the current identity
  — see 1c-2.
- Which trade and which area do we go after first? Being in the Wirral gives us
  a credible local answer, and a local first client is far easier to get than a
  cold national one.
- How much time per week is there for delivery? This caps everything.
- Is there any existing contact who could be client number one?
