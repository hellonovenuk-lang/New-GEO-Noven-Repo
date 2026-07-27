# Noven roadmap

**What this file is:** the single running list of what's done and what's left.
Update it at the end of every working session — tick things off, add what we
learned, and write the next session's starting point at the bottom.

**How we're working:** we build the minimum needed to take a real client, then
let real client work tell us what to build next. We don't design processes for
situations we haven't met yet. Anything we don't know is written as
`[PLACEHOLDER]` rather than guessed.

The three phases overlap — outreach starts before the build is perfect, and
the first delivery will change both.

---

## Where we are today

The website is built and works. Seven static pages (home, how it works,
pricing, FAQ, about, contact, 404), fully readable by AI crawlers, with
machine-readable business facts and a sitemap. It builds clean and is ready to
deploy the moment we have a domain.

The site now carries real business facts throughout: contact email, the Wirral,
Kieran Smith trading as a sole trader, no VAT, one working day for the audit,
two working days to reply. The domain `novenstudio.co.uk` is confirmed and set.

Three things are still missing: the founder bio, a cancellation notice period,
and an address for service of documents.

**Biggest remaining blocker:** the site isn't deployed, so nobody can read it.
The domain currently serves the old website, so switching it over is the next
real step — and the thing that makes Noven exist publicly.

---

## Phase 1 — Build (get to a site that can take a real customer)

### 1a. Facts only the owner can supply

These are all marked `[PLACEHOLDER]` in the site. Nothing else in Phase 1
matters until these exist. Search the repo for `[PLACEHOLDER` to find them all.

- [x] **Contact email address** — `hello.noven.uk@gmail.com`, live on the
      contact page and in the site's machine-readable business facts
- [x] Phone number — we don't offer one. Email only, and the contact page and
      FAQ now say why rather than leaving it looking like an omission.
- [x] Reply time — within two working days
- [x] Location — the Wirral, working with clients across the UK, remotely
- [x] Founder name — Kieran Smith, sole trader trading as Noven
- [x] Business identity for the footer — sole trader, so no company number
- [x] VAT — not registered, so no VAT to add. Stated on the pricing page.
- [x] Audit turnaround — one working day from confirming scope and payment
- [x] Foundation delivery — we reply within two working days with a plan and a
      date; the work itself depends on client access and information
- [ ] **Founder bio** — still a placeholder on the About page. Two or three
      sentences on background and what led to Noven. This is the one a
      cautious buyer reads hardest, so it's worth doing properly.
- [ ] **Cancellation notice period** for monthly plans (appears in three
      places: pricing, FAQ, how it works)
- [ ] **Address for service of documents.** Trading under a business name as a
      sole trader carries a legal disclosure requirement to show your name and
      an address where documents can be served, including on the website. A
      home address is uncomfortable; the usual answers are a virtual office
      address or a PO box style service. Worth 20 minutes of checking before
      launch — it's the only outstanding item with a legal edge to it.

### 1b. Domain and hosting

- [x] Domain confirmed and owned — `novenstudio.co.uk`
- [x] Domain set in `site/astro.config.mjs` and `site/public/robots.txt`
- [ ] **Decide apex vs www.** Both files currently use the bare
      `novenstudio.co.uk`. Whichever one Netlify treats as primary, the two
      files must match it, or the canonical links and sitemap point at the
      redirecting version.
- [ ] **Point Netlify at this repo — note the old site is currently live on
      this domain.** Deploying replaces it. Worth loading the new site on a
      Netlify preview URL first and reading it end to end before switching.
- [ ] Confirm HTTPS works after the switch
- [ ] Decide whether to keep any URLs from the old site alive, and redirect
      them in `netlify.toml` if so — otherwise anything linking to the old
      site starts hitting a 404
- [ ] Consider a `hello@novenstudio.co.uk` address to replace the Gmail one

### 1c. Taking money

The site says payment is arranged "by reply". Decide the actual mechanism:

- [ ] Business bank account in place
- [ ] How the £30 audit gets paid — bank transfer, a payment link, or an invoice
- [ ] How the £350 Foundation gets paid
- [ ] How monthly plans get collected (this matters most — manual collection
      stops being viable somewhere around client five)
- [ ] A simple invoice or receipt we can send

### 1d. Legal basics

- [x] Sole trader vs limited company — sole trader to begin with
- [ ] Privacy notice page — we'll be handling client business data and email
- [ ] Terms of service, or a short plain-English version of what we promise
- [ ] Register as self-employed with HMRC if not already done
- [ ] Keep an eye on the VAT threshold as revenue grows — not a launch concern,
      but the pricing page states we aren't registered, so it has to stay true

### 1d-2. Brand assets — found during the demo deploy check

The committed logo (`assets/logo.svg`) is a 1920×1920 tile: a cream `#FAF7EF`
square with the wordmark "Noven." centred in indigo `#241F7C`. **It is not used
on the website at all** — it was never copied into `site/public/`, so it isn't
even deployed.

Instead the header, the footer and the favicon all set the word "Noven" in
Inter. That's retyping the logo, which the standing rules in `CLAUDE.md`
specifically forbid. The site palette also doesn't match the real brand: the
accent is `#1c4d99` against the brand's `#241F7C`, and the page tint is
`#f7f6f3` against the brand's `#FAF7EF`. Close but not equal, which reads worse
than either matching properly or being plainly different.

- [ ] **Get a wordmark-only logo file** — horizontal, transparent or cream
      background, trimmed to the lettering. The square tile can't go in a site
      header: at header height the lettering would be unreadable.
- [ ] **Get a monogram or icon version for the favicon** — the square tile
      renders as an illegible smudge at 16px, because the lettering is only
      about 15% of the tile's height.
- [ ] Copy the supplied assets into `site/public/` so they actually deploy
- [ ] Replace the retyped header and footer wordmark with the real asset
- [ ] Replace the retyped "N" favicon with the real asset
- [ ] Align the site palette to the brand indigo and cream

Until there are proper assets, nothing here should be guessed at — cropping the
tile to fake a wordmark is still altering the logo.

### 1e. Launch checks

- [x] Verified what the build actually publishes: 6 pages plus a 404, every
      canonical URL correct, all JSON-LD parses as valid, the sitemap lists the
      right 6 URLs, robots.txt ships. No technical faults found.
- [ ] Read every page top to bottom with fresh eyes, out loud
- [ ] Check the site on a phone
- [ ] Submit the sitemap to Google Search Console and Bing Webmaster Tools
- [ ] Ask ChatGPT, Claude, Copilot and Perplexity what Noven does — record the
      answers, dated. This is our own before-and-after, and our first proof.

**Phase 1 is done when:** a stranger can read the site, understand the offer,
email us, and pay us £30.

---

## Phase 2 — Outreach (how we get the first clients)

The honest position: we're new with no case studies, and the site says so. The
whole outreach strategy follows from that — we cannot win on proof yet, so we
win on being specific, being cheap to try, and being obviously not a scam.

The £30 audit *is* the outreach tool. It's priced to be an easy yes, not to
make money.

### 2a. Before contacting anyone

- [ ] Write down who we're actually targeting first — one trade, one area.
      "Accountants and solicitors across the UK" is too broad to write a good
      email to. Pick something like "independent accountants in [town]".
- [ ] Decide how many we can realistically deliver for at once
- [ ] Set a working definition of what a good first client looks like

### 2b. The first approach — do the work before asking

The approach that fits our position: run a mini version of the audit *before*
making contact, so the first email contains a real finding about their
business, not a pitch.

- [ ] Build a shortlist of [PLACEHOLDER: number] businesses
- [ ] For each: ask the assistants the question their customers would ask, and
      record whether the business is mentioned
- [ ] Write the outreach email — short, one specific finding, the £30 offer,
      no chasing sequence
- [ ] Send in small batches so we can change the email based on replies
- [ ] Keep a simple record of who we contacted, when, and what came back

### 2c. Warm routes (likely the first paying client)

- [ ] List existing contacts — anyone who runs a business or knows people who do
- [ ] Personal approach to each, offering the audit
- [ ] Ask satisfied clients for one introduction each — the only referral
      mechanism we need for now
- [ ] [PLACEHOLDER: local business groups, networking, trade bodies worth trying]

### 2d. Proof — the thing that unlocks everything else

Our biggest constraint is having nothing to show. Fixing that is the priority
of the first few engagements.

- [ ] Get written permission to publish results from the first clients
- [ ] Record before-and-after: what the assistants said before, what they say
      after, both dated
- [ ] Publish the first case study on the home page, replacing the placeholder
- [ ] Publish our own before-and-after — we're our own first test case

### 2e. Later, only if the above works

Don't start these until we have paying clients and proof:

- [ ] Writing that answers the questions our own customers ask
- [ ] LinkedIn or wherever our buyers actually are
- [ ] [PLACEHOLDER: decide after the first ten conversations]

**Phase 2 is working when:** we have a repeatable way of getting conversations,
and we know roughly how many approaches produce one paid audit.

---

## Phase 3 — Outcome (actually doing the work we've promised)

This phase is deliberately thin. We'll write the real process while doing the
first audit for a real client, not before.

### 3a. The audit (£30)

What we've promised on the site: what each assistant says when asked about
businesses like theirs; what they know and believe about this business and
whether it's accurate; what's blocking them, in plain English; and an honest
recommendation including "you don't need us".

- [ ] Write the list of questions we ask the assistants, and how we vary them
      by trade and area
- [ ] Decide which assistants we check, and record how we record answers
- [ ] Build the checklist of things we look at on their website
- [ ] Build the audit report template — short, plain English, no jargon
- [ ] Do the first one end to end and time it. £30 has to be sustainable, so
      if it takes a day, the process is wrong, not the price.
- [ ] Rewrite the process based on what the first one taught us

### 3b. The Foundation (£350)

What we've promised: crawler access, structured machine-readable business
facts, consistent facts across the web, and pages that answer customer
questions — all on the client's existing site. We don't build websites.

- [ ] Write the Foundation checklist, mapped to what the audit found
- [ ] Work out how we get access to a client's website safely, and what we do
      when we can't (their site is on a platform we can't edit)
- [ ] Decide what happens when the client's site is too broken for the
      Foundation to work — the audit is supposed to say so honestly
- [ ] Agree what we hand over at the end, and how we show what changed
- [ ] Do the first one, time it, then fix the process

### 3c. Monthly plans (£75 / £125 / £250)

- [ ] Define what actually happens each month at each level, concretely enough
      that a client would recognise the value
- [ ] Decide how we check and report visibility each month
- [ ] Write the monthly client update — short and readable
- [ ] Define the quarterly review promised on the Lead plan
- [ ] Work out how many clients one person can hold at each level

### 3d. Keeping track of clients

The `ops/spine.md` file is meant to hold this and is currently empty. Keep it
minimal — a spreadsheet is fine until it isn't.

- [ ] Record per client: business, contact, what they want to be found for,
      area served, stage, plan, what we've done, dated visibility checks
- [ ] Set up wherever the audits and reports live

### 3e. The internal docs we've stubbed out

All three files in `ops/` are TODO stubs. These are worth writing *after* the
first client, when we know what's actually true.

- [ ] `ops/org-chart.md` — the five company seats
- [ ] `ops/spine.md` — the shared client and prospect data model
- [ ] `ops/escalation-rules.md` — the three "never do this without me" rules

**Phase 3 is working when:** we can do an audit and a Foundation to a
consistent standard without reinventing them each time, and a client on a
monthly plan gets something real every month.

---

## Open questions for the owner

Written down rather than guessed at. Answer them as they become relevant.

- Which trade and which area do we go after first? Being in the Wirral gives us
  a credible local answer — "accountants in the Wirral" or similar — and a
  local first client is far easier to get than a cold national one.
- How much time per week is there for delivery? This caps everything.
- Is there any existing contact who could be client number one?

---

## Session log

Add a short entry at the end of each session — what changed, what we learned,
what's next. Newest at the top.

### 2026-07-27 (later — demo deploy)
- Netlify linked to the repo, publishing `main` to a demo URL.
- Checked the built output rather than trusting the build: canonicals, JSON-LD,
  sitemap and robots.txt are all correct. No technical faults.
- **Found:** the committed logo isn't on the site at all, and the header,
  footer and favicon retype the wordmark in Inter — against the standing brand
  rule. The palette also doesn't match the brand indigo and cream. Logged in
  section 1d-2. Needs proper assets from the owner before it can be fixed.
- Note: every page on the demo declares its canonical as `novenstudio.co.uk`,
  which currently serves the old site. That's correct for the final state and
  stops the demo being indexed as a duplicate — but don't be surprised by it.

### 2026-07-27
- Reviewed the whole repo and confirmed the site builds clean (7 pages + sitemap).
- Wrote this roadmap.
- Filled in almost all of Phase 1a from real owner facts: contact email, no
  phone (with the reason stated rather than the gap left showing), two working
  day reply, the Wirral, Kieran Smith as sole trader, not VAT registered, one
  working day audit turnaround, Foundation timing framed honestly around client
  access. Domain set to `novenstudio.co.uk` in the config and robots file.
- Added a "Who will I actually be dealing with?" FAQ. A one-person business is
  an advantage with this buyer if we say it plainly, and a worry if we hide it.
- Added the founder to the site's machine-readable business facts.
- **State:** the site reads as a real business now rather than a template.
  Three facts outstanding — founder bio, cancellation notice, address for
  service. Nothing else blocks deployment.
- **Next session:** deploy to Netlify on a preview URL, read it end to end,
  then switch the domain over from the old site.
- **Worth deciding soon:** a Gmail address works to launch, but an address on
  the Noven domain reads as more established to the businesses we're
  approaching — and we sell consistent, credible business information.
