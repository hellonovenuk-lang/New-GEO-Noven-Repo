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

The founder bio and the cancellation terms are now written, and the founder's
photograph is committed and live on the About page. One supporting value is
still wired but unset — the LinkedIn URL, which needs a desktop session to
fetch correctly; the steps are in 1a. The address for service is deliberately
deferred until we're closer to revenue.

**Biggest remaining blocker:** the site isn't deployed, so nobody can read it.
The domain currently serves the old website, so switching it over is the next
real step — and the thing that makes Noven exist publicly.

**How the remaining work is sequenced.** Nothing on the site takes a payment,
so the site can go public before the money and legal plumbing exists. Section
1c holds everything that must be true before the first person *pays* us, which
is a later moment than launch — including the bank account and the service
address, both of which have lead times and shouldn't wait for the day a client
says yes.

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
- [x] **Founder bio** — written and live on the About page: nearly ten years in
      operations at a global shipping company, and finding this problem by
      chance while building websites. One supporting piece is still open:
  - [ ] **LinkedIn URL** — set `founderLinkedIn` in `src/data/business.ts`.
        One value, two uses: it links from the About page and joins the
        founder in the structured data as `sameAs`. Nearly ten years at one
        employer is the most checkable thing we have, and right now a cautious
        reader has no way to check it.

        **Getting the right URL (owner, on desktop).** LinkedIn → **Me** →
        **View Profile**, then read the address bar once it has finished
        redirecting. It should look like
        `https://www.linkedin.com/in/kieran-smith-8b41a2b0` — the `/in/` is
        the part that matters. Anything after a `?` is tracking and can be
        deleted. Then paste it into a private window: if the profile loads
        without a login prompt, it is both the correct URL and publicly
        visible, which is the whole point of publishing it.

        **Two forms that cannot work, both already tried:**
        `linkedin.com/me` and `linkedin.com/nhome` are *viewer-relative* —
        they resolve to whoever is logged in, so for a stranger or a crawler
        they resolve to a login wall, not to Kieran. The URL has to name the
        person.

        **Hard rule before this value is ever set:** if the URL contains a
        `loginToken`, `authToken`, `session`, or any similar credential
        parameter, it must not go in. `founderLinkedIn` is published twice on
        a public page — once as a visible link, once inside the JSON-LD — in
        a public repo, on a site built to be easy for crawlers to ingest.
        That is the worst available place to put a credential. A URL safe to
        publish contains no token and needs no login for a stranger to open.

        While in the LinkedIn settings, also add `novenstudio.co.uk` to the
        profile's website field. Confirmation that only points one way is
        much weaker than two pages agreeing about the same person, and this
        is the argument the rest of the site makes.
  - [x] **Founder photograph** — the owner's photograph is committed at
        `site/public/founder-portrait.webp` (880x1100) and set as
        `founderPhoto` in `src/data/business.ts`. It shows under "Who's behind
        it?" on the About page and joins the founder in the structured data as
        the Person's `image`.
- [x] **Former employer named** — Maersk, confirmed by the owner. It reads in
      the bio and appears as the founder's `alumniOf` in the structured data,
      both from `founderFormerEmployer` in `src/data/business.ts`. Plain text
      only: never the Maersk logo, never anything implying they endorse Noven.
- [x] **Cancellation terms** — decided and live in all three places (pricing,
      FAQ, how it works): monthly plans roll month to month, no minimum term,
      **no notice period**. Tell us before the next payment date and there
      isn't one; the month already paid for runs to the end, with no
      part-month refunds.
      - Chosen against the agency norm (3-month minimum plus 30 days' notice)
        because that norm belongs to £2,000–8,000/month retainers with staff
        allocated. At £75–250 a notice period costs more in friction and
        chasing than it can ever recover, and the Foundation being a separate
        one-off already covers the front-loaded-work risk.
      - There is no statutory cooling-off period to satisfy: the Consumer
        Contracts Regulations 2013 cover consumers, not businesses buying in
        the course of business, so these terms are purely ours to set.
      - It also survives the undecided payment mechanism in 1c — it reads the
        same whether collection ends up manual or automatic.
      - If clients ever do start taking a month and leaving, add a minimum term
        *then*. Not before we have met the problem.
- [ ] **Address for service of documents — deferred pre-revenue, by decision.**
      Trading under a business name as a sole trader carries a legal disclosure
      requirement to show your name and an address where documents can be
      served, including on the website. The requirement is an address where
      post reaches us — **not** necessarily a home address, so a virtual office
      or service-address provider satisfies it.
      **Do not use the home address here.** This site is built so AI crawlers
      can read the business facts and repeat them confidently — explicit
      crawler permissions, structured data on every page, a sitemap. That is
      the product, and it works against us on this one field: a home address in
      that footer gets crawled, cached, repeated by assistants and swept up by
      anything that scrapes structured markup. It is also a one-way door —
      the footer can be edited, the indexes and archives cannot.
      Scheduled in 1c. The footer placeholder stays visible until it's set.

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

### 1c. Between launch and the first payment

**The decision, made deliberately:** the site goes public before the money and
legal plumbing is finished. Nothing on the site takes a payment — every page
asks people to email — so publishing commits us to nothing we cannot honour.
Everything in this section has to be true before the first person actually
*pays* us, which is a different and later moment.

This is the one place the phase definitions don't line up: "Phase 1 is done
when a stranger can read the site, understand the offer, email us, and pay us
£30." The site can go live before that is true. This section is the rest of it.

**The trigger is an event, not a date.** "Before the first payment" could be a
fortnight away if outreach lands. Two items below cannot be started on the day
someone says yes, so they need starting first.

#### Has a lead time — start these before they're needed

- [ ] **Business bank account.** Anything from a day with a digital provider to
      several weeks with a high street bank, so it's the long pole. Worth
      checking whether the existing personal account's terms permit business
      use in the meantime — most banks' terms don't, and a £30 transfer is
      still business use.
- [ ] **Address for service of documents.** Deliberately deferred pre-revenue
      (see 1a). A virtual office or service-address provider satisfies the
      disclosure requirement without publishing a home address, and runs about
      £20–60/year. **This one should land before we are visibly trading**, not
      merely before the first payment — and see the note in 1a about why this
      site in particular is the wrong place for a home address.

#### Before money changes hands

- [ ] How the £30 audit gets paid — bank transfer, a payment link, or an invoice
- [ ] How the £350 Foundation gets paid
- [ ] How monthly plans get collected (this matters most — manual collection
      stops being viable somewhere around client five). Note the cancellation
      terms in 1a were written to read the same whichever way this goes, so
      this decision doesn't reopen the copy.
- [ ] A simple invoice or receipt we can send

#### Before we hold a client's information

- [ ] Privacy notice page — we'll be handling client business data and email.
      Due before the first client sends us anything, not before launch, since
      the site collects nothing on its own.
- [ ] Terms of service, or a short plain-English version of what we promise.
      Most of it is already written across the site — the cancellation terms,
      "we don't guarantee outcomes", "we don't build websites". This is mostly
      a job of collecting what we've already committed to in one place.

#### Has its own legal clock

- [ ] **Register as self-employed with HMRC.** The general rule is registration
      for Self Assessment by 5 October following the end of the tax year in
      which trading began — so trading started in 2026/27 means October 2027.
      There is also a £1,000 trading allowance below which registration may not
      be required at all, which may cover the first few months. Both worth
      confirming against current HMRC guidance rather than taking from here.

### 1d. Standing decisions, and things to keep true

- [x] Sole trader vs limited company — sole trader to begin with
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

**Decided:** the owner is supplying the real brand assets and the site palette
will be matched to them. Nothing here gets guessed at or derived.

**Confirmed brand colours:** deep navy `#170969`, warm white `#fffefa`.

**The committed logo is out of date.** `assets/logo.svg` and `assets/logo.png`
are the *old* mark — a neutral grotesque in `#241F7C` on `#FAF7EF`. The new
brand is a heavier geometric sans in the new colours. Different artwork, not a
recolour, so the old files must be replaced rather than tinted, and nothing can
be rebuilt from their vectors.

Six SVGs were supplied and are now in the repo. All are true vector paths —
no embedded raster, no live text, no font dependencies — so they stay sharp at
any size and work as static files.

**Originals live untouched in `assets/brand/`.** The web copies in
`site/public/` differ only in their `viewBox`, trimmed to the artwork's own
bounds. No path data was altered, so the letterforms are exactly as drawn.

Measured content, as a share of each original's frame:

| Asset | Filled | Outcome |
|---|---|---|
| Logo Primary | 71% × 16% | Trimmed → `site/public/logo.svg`, header and footer |
| Logo Dark | 80% × 16% | Trimmed → `site/public/logo-dark.svg`, held for future dark use |
| Social Avatar | 60% × 60% | Trimmed → `site/public/favicon.svg` |
| Favicon | 40% × 29% | **Not used** — too much padding, and navy on transparent vanishes in a dark browser tab |
| Email Banner | 51% × 40% | Not a website asset. See the language flag below. |
| Brand Pattern | 92% × 91% | Not used yet |

- [x] Wordmark in the header and footer, replacing the retyped Inter text
- [x] Favicon replaced with the circle mark — verified legible at 16px and
      32px against both light and dark browser chrome
- [x] `assets/logo.svg` and `assets/logo.png` replaced; they were the old mark
- [x] Palette moved to the brand: `--accent` `#170969`, `--paper` `#fffefa`
- [x] Logo added to the site's machine-readable business facts
- [x] Contrast checked — every text pair passes WCAG AA, most AAA
- [x] Checked on desktop and at phone width

**The brand is two colours and nothing else.** Every asset uses only `#170969`
and `#fffefa`; the lighter tones in the banner and pattern are those same two
at reduced opacity. The site palette now follows that, so the section tint and
rules are the only derived values.

**The supplied "Favicon" asset is the one thing I'd not use.** The circle
avatar does the job better at every size. Worth knowing if it's used elsewhere.

**Language flag on the email banner.** It reads "AI Visibility Services", which
is category jargon — the words a competitor uses, not the words a customer
uses. The standing rules ban search-industry jargon, and the whole site
deliberately avoids it: the homepage says "when your customers ask an AI who to
use, the answer should include you." The banner should say something in that
voice instead, or the first impression contradicts every page it links to.

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

### 2026-07-28 (latest — the founder photograph)
- **The founder's photograph is in.** The owner's file lives in the separate
  `hellonovenuk-lang/Noven` asset repo at
  `public/brand/website/founder-portrait.webp`; it is copied here byte-for-byte
  as `site/public/founder-portrait.webp` and set as `founderPhoto` in
  `src/data/business.ts`. 880×1100, 48 KB, already the 4:5 the About page
  assumed.
- Nothing else needed changing, which was the point of how it was built: one
  value in `business.ts` turned on the portrait under "Who's behind it?", the
  `image` on the founder's Person in the structured data, and the removal of
  the on-page placeholder flag — all three from that single edit. Verified in
  the built output rather than assumed.
- The `<img>` now carries the file's real intrinsic dimensions instead of the
  600×750 stand-in, plus `loading="lazy"` and `decoding="async"`. Same ratio
  either way, so no layout shift; it's just no longer a guess. Checked the
  rendered section at 1280px and 390px.
- **Worth remembering:** the brand and image assets live in a *second* repo
  (`hellonovenuk-lang/Noven`), not this one. Asset paths the owner gives are
  likely relative to that repo's root, not this site's.
- **Merged to `main` at the owner's request**, which knowingly overrides the
  standing "finish on an unmerged branch for review" rule in `CLAUDE.md`. The
  standing rule is unchanged for future work — this was one explicit call, not
  a new default. Netlify publishes `main`, so the photograph is now live on
  the demo URL while the domain still serves the old site.
- **The LinkedIn URL was attempted and deferred to a desktop session.** Two
  URLs were supplied and neither could be used: one was `/nhome` carrying a
  `loginToken`, the other was `/me`. Full detail and the exact steps are
  written into 1a so the next session doesn't re-derive them.
- **Owner action outstanding, unrelated to the repo:** the first URL contained
  a live LinkedIn sign-in token, so it should be treated as exposed —
  LinkedIn → Settings → Sign in & security → sign out of other sessions, and
  change the password. Nothing was ever written to a file or committed.
- **Next session:** the LinkedIn URL (steps in 1a), then Netlify — apex vs www,
  read the preview end to end, then switch the domain off the old site.

### 2026-07-28 (the link card, and the record's wide-screen home)
- The site now ships a link-preview image, closing the gap found during the
  redesign: `site/public/og.png`, 1200×630, declared on every page. Sharing a
  link to LinkedIn or WhatsApp now shows the brand instead of bare text.
- It's rendered from `assets/og/og.html` by headless Chromium — the same
  approach as the homepage animation, and the same materials: brand navy, warm
  white, the committed wordmark referenced as-is, and the homepage headline in
  Newsreader. **The headline is deliberately duplicated there** — if it changes
  on the homepage, change `og.html` and re-render (command in
  `assets/og/README.md`).
- The structured-data panel decision is made and done: on wide screens it lives
  in "Where's the proof?", directly under the paragraph that claims
  "structured information about the business" — the claim above, the evidence
  below — using the navy-ground code styling `global.css` already had waiting.
  Below 60rem it stays hidden, because the hero shows the record there. The
  page holds exactly one visible copy of the record at every width; the two
  breakpoints are paired, and both files say so in comments.
- Verified in the built output, not just the source: at 1440px the hero shows
  the film and the proof section shows the record; at 700px the hero shows the
  record and the proof section shows none.
- **The founder bio is written**, from the owner's own facts: nearly ten years
  in operations at a global shipping company, and coming across this problem by
  chance while building a few websites. The bridge between the two is real
  rather than decorative — shipping operations is largely about keeping
  information consistent across systems that don't agree, which is a fair
  description of this work too. It deliberately doesn't claim a marketing
  background, because there isn't one, and the page around it already trades on
  saying so.
- **Maersk is named.** Vagueness about the one checkable fact we have would
  have contradicted the argument the rest of the site makes. It also appears as
  the founder's `alumniOf` in the structured data — nested under `founder`, so
  it says one person used to work there and nothing more. Verified after the
  change that both homepage code blocks are still byte-identical to the JSON-LD
  in the head, which is the property the whole design rests on.
- Two supporting facts are wired but unset: `founderLinkedIn` and
  `founderPhoto` in `src/data/business.ts`. Both are null, and everything that
  consumes them is conditional — no empty `sameAs`, no broken image, and a
  loud flag on the page until each is supplied. Setting either one value
  updates both the page and the structured data.
- **Cancellation terms written** — see 1a. Stated once, the same way, in all
  three places.
- **Found while doing it:** the cancellation placeholder was being published
  into the FAQPage structured data, because the FAQ answers feed both the
  visible page and the JSON-LD from one array. So `[PLACEHOLDER: confirm
  cancellation notice period.]` was in the machine-readable answer an assistant
  reads. Fixed by the same edit. Worth remembering that **anything written into
  `faqs` in `faq.astro` is published to assistants**, not just to readers — the
  coupling is the point of the design, and it cuts both ways.
- **The roadmap is now sequenced around launch rather than around topic.** New
  section 1c, "Between launch and the first payment", replaces the old "Taking
  money" and "Legal basics" lists. The insight worth keeping: the site takes no
  payments and collects nothing, so publishing it commits us to nothing we
  cannot honour — but the bank account and the service address both have lead
  times, so "do it when someone says yes" is too late for those two.
- **Address for service deferred pre-revenue, by the owner's decision.** The
  reasoning is written into 1a so it isn't relitigated: the requirement is an
  address where post reaches us, not a home address, and this site is
  specifically the wrong place to publish a home one — everything that makes it
  good at being read by assistants makes that field harder to take back.
- **Still outstanding:** founder photo and LinkedIn URL (both wired, waiting on
  values), the mobile cut of the animation, and the email banner's wording.
- **Next session:** Netlify. Point it at the repo, decide apex vs www so the
  canonicals and sitemap match, read the preview end to end, then switch the
  domain from the old site.

### 2026-07-27 (premium redesign)
- Reshaped the whole site to feel like a top-end firm rather than a document.
  The design idea: this business sells the gap between what a person reads and
  what a machine reads, so the page speaks in two voices — Newsreader (serif)
  for everything meant for a human, IBM Plex Mono for everything meant for a
  machine, IBM Plex Sans between them.
- **The signature is the code block** — the homepage and pricing page show the
  page's own JSON-LD, syntax-coloured and line-numbered. It is not a
  representation of the structured data, it *is* the structured data: the
  layout and the visible block render the same object through the same
  serialiser, so on the homepage the block on screen is byte-for-byte the
  block in `<head>`. The head JSON-LD is pretty-printed rather than minified
  specifically so "view source and compare" survives someone actually doing
  it. That is the only proof a business with no case studies can honestly
  offer.
  - Built from `src/lib/json-code.ts`, whose output is verified to match
    `JSON.stringify(value, null, 2)` exactly. **If you change that file, check
    that property still holds** — the site's central claim rests on it.
  - The pricing block is labelled "abridged" because it shows the offers
    without the surrounding Service fields. Keep that label if the contents
    stay partial.
- New `site/src/data/business.ts` is now the single source of truth for every
  business fact and price. **Change a price there, not in a page** — the
  pricing copy, the Offer structured data and the record panel all read from
  it.
- Motion added and kept disciplined: hero words rise on load, sections reveal
  on scroll, reading progress on the header. All of it is gated behind a `.js`
  class that only JavaScript can add, so with JS off — or for a crawler that
  never runs it — nothing is hidden. Verified: 0 hidden elements across all 7
  pages with JavaScript disabled, and again under `prefers-reduced-motion`.
- Checked contrast on every rendered text node across all 7 pages: no failures
  against WCAG AA.
- Cut the repeated calls-to-action. The site now asks once per page, in the
  footer, plus one contextual ask in the homepage hero.
- **Still outstanding, unchanged:** founder bio, cancellation notice period,
  address for service. All three are marked on the pages with a loud
  `[PLACEHOLDER]` block so they cannot be mistaken for finished copy.
- **New gap found:** there is no Open Graph image, so links shared to
  LinkedIn or WhatsApp will preview as bare text. Needs a 1200×630 PNG built
  from the brand assets — SVG is not reliably supported by the platforms.

### 2026-07-27 (later still — brand assets)
- Brand assets supplied as SVG and packaged. Originals kept untouched in
  `assets/brand/`; web copies trimmed to the artwork and wired into the header,
  footer and favicon. Palette moved to the brand navy and warm white.
- The site no longer retypes the logo anywhere, so it's back inside the
  standing rules.
- Two things for the owner: the supplied "Favicon" asset isn't the right one to
  use anywhere small, and the email banner's "AI Visibility Services" line
  still needs rewording.
- **Next session:** merge to `main` so the demo picks it up, then the founder
  bio and the cancellation notice period.

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

### 2026-07-28
- Built a short animation for the hero showing a customer asking an assistant
  for a solicitor, the assistant reading four businesses, the three it can't
  make sense of falling back, and the complete one being named. 7.5s, 161KB,
  silent. Source and render script in `assets/video/`.
- It is rendered from the site's own CSS by headless Chromium, not generated.
  Two Higgsfield generations were tried first and not kept: they drifted
  off-palette, softened toward the end, and the second misspelled the query.
  What they did contribute is the design — the terracotta pulse and the
  filled-block-versus-empty-box contrast are theirs.
- The render asserts the typed question matches the expected string exactly
  and fails rather than emitting a video with a typo in it.
- Hero now shows the animation at 60rem and up, and the structured-data panel
  below that, where the animation's captions would fall under 8px. Only one is
  ever shown, and narrow layouts don't download the video at all.
- The panel gained a plain sentence above it explaining what it is. A caption
  sitting on a code panel gets skimmed; a line of body text before it doesn't.
- The film plays once when scrolled into view and holds its last frame. A loop
  beside body copy pulls the eye off the words.
- **Worth deciding:** on wide screens the structured-data panel is now absent
  from the page entirely. Its natural home looks like "Where's the proof?",
  which already claims "structured information about the business" without
  showing any — and `global.css` has styling for a panel on the navy ground
  that nothing currently uses. Not done; needs a decision.
- **Also outstanding:** a mobile-specific cut of the animation, if we want the
  argument to land on phones rather than only on desktop.
