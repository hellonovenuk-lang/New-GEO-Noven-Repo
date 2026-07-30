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

The founder bio and the cancellation terms are now written, the founder's
photograph is committed and live on the About page, and the founder's LinkedIn
URL is now set — so the About page links to it and the structured data claims
the profile and the business are the same person. **Roadmap 1a is now fully
closed.** The Noven company page is live at
`https://www.linkedin.com/company/novenstudio/`, `businessLinkedIn` in
`src/data/business.ts` points at it and is confirmed in the built structured
data, and the profile's Noven role is confirmed linked to the real page rather
than the loose text it started as. The address for service is deliberately
deferred until we're closer to revenue.

**The site is live, on HTTPS, at `novenstudio.co.uk`.** Netlify is pointed at
`main` and deployed — the old website is no longer what that domain serves.
Noven now exists publicly. What's left before Phase 1 is fully closed: decide
on redirects for any old URLs, and the 1e launch checks (read it end to end,
check on a phone, submit the sitemap, ask the assistants what they say about
Noven).

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

- [x] **Contact email address** — `hello@novenstudio.co.uk`, live on the
      contact page and in the site's machine-readable business facts. The old
      `hello.noven.uk@gmail.com` stays open and forwards, since it is in
      caches and indexes and will be for months.
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
- [x] **Founder bio** — written and live on the About page: eight years in
      operations at a global shipping company, and finding this problem by
      chance while building websites. One supporting piece is still open:
  - [x] **LinkedIn URL** — supplied by the owner and set as `founderLinkedIn`
        in `src/data/business.ts`:
        `https://www.linkedin.com/in/kieran-smith-50b953143`. One value, two
        uses: it links from the About page and joins the founder in the
        structured data as `sameAs`. Eight years inside one group is the most
        checkable thing we have, and now a cautious reader can check it.

        The shared link arrived with `?utm_source=share_via&utm_content=…`
        tracking parameters on the end. Those are stripped — they describe how
        the link was shared, not the person, and they'd be published verbatim
        in the JSON-LD.

        **The rule this was checked against, kept for next time:** the URL must
        name the person (`/in/…`). `linkedin.com/me` and `linkedin.com/nhome`
        are viewer-relative — both were tried earlier and both resolve to a
        login wall for a stranger or a crawler. And if a URL ever contains a
        `loginToken`, `authToken`, `session` or similar, it must not go in:
        this value is published twice on a public page and again in a public
        repo built for crawlers to ingest, which is the worst available place
        to put a credential.

        **One check still worth doing (owner, two minutes):** open the URL in a
        private window. If the profile loads without a login prompt, it's
        publicly visible, which is the whole point of publishing it. If it
        prompts, the profile's public visibility needs turning on — the link
        is live on the About page either way.
  - [x] **Founder photograph** — the owner's photograph is committed at
        `site/public/founder-portrait.webp` (880x1100) and set as
        `founderPhoto` in `src/data/business.ts`. It shows under "Who's behind
        it?" on the About page and joins the founder in the structured data as
        the Person's `image`.
- [x] **Amend the LinkedIn profile, and create the Noven business page**
      (owner, on desktop — nobody else can sign in). `ops/linkedin.md` is the
      working version of this item; it has no open questions left, and 1a is
      now fully closed.
  - [x] **The personal profile** — done by the owner. Headline, About section,
        the missing Maersk role, the Port Brief removal and the website field,
        all as written in `ops/linkedin.md` §§1–4.
  - [x] **A Noven company page** — live at
        `https://www.linkedin.com/company/novenstudio/`. `novenstudio` was the
        only one of the preferred slugs still free. Logo and cover uploaded
        from `assets/linkedin/`, About copy in, `businessLinkedIn` set in
        `src/data/business.ts` and confirmed in the built JSON-LD's `sameAs`.
  - [x] **The profile's Noven role, re-linked to the real page** — the profile
        was written before the page existed, so it started as loose text that
        LinkedIn had nothing to attach. Confirmed by the owner: retyped and
        picked from the dropdown, now shows the Noven logo and opens the page.
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
- [ ] **Address for service of documents — ordered, pending delivery.**
      Trading under a business name as a sole trader carries a legal disclosure
      requirement to show your name and an address where documents can be
      served, including on the website. The requirement is an address where
      post reaches us — **not** necessarily a home address, so a virtual office
      or service-address provider satisfies it.
      **Provider chosen: V LOT** (vlot.uk), on cost — plans run roughly
      £10–48/yr against the ~£96–115/yr established providers (1st Formations,
      Quality Company Formations) quote for the equivalent product. Order
      placed; the address itself hasn't been provided yet.
      **Known risk, accepted for now:** V LOT's Trustpilot reviews are
      poor — reports of no address/service being provided after payment and
      unresponsive support. This field is exactly the one place a dropped
      delivery matters most (a missed legal document), so **don't tick this
      off, and don't remove the footer placeholder, until mail through this
      address has actually been confirmed working.** If it doesn't deliver
      within a few days, fall back to 1st Formations or Quality Company
      Formations (~£115/yr inc VAT) — see `ops/third-party-services.md` B1.
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
- [x] **Decide apex vs www.** Confirmed by the owner: `novenstudio.co.uk`
      (apex) is primary, already set up from previous projects, and
      `www.novenstudio.co.uk` redirects to it. That matches what
      `site/astro.config.mjs` and `site/public/robots.txt` already assume, so
      no file changes were needed — just the decision recorded.
- [x] **Point Netlify at this repo.** Done — Netlify deploys `main` to
      `novenstudio.co.uk` directly, and the site is live. The old website no
      longer serves from the domain.
- [x] **Confirm HTTPS works after the switch.** Checked via Netlify's own
      API rather than assumed: the project's primary URL is
      `https://novenstudio.co.uk` and the current deploy is `ready`.
- [x] **Decide whether to keep any URLs from the old site alive.** Not
      applicable — the owner confirms `novenstudio.co.uk` has only ever hosted
      his own projects, not a prior unrelated business with its own external
      links to preserve. Nothing to redirect.
- [x] **`hello@novenstudio.co.uk` is live and replaces the Gmail address.**
      Zoho Mail on Mail Lite, DNS at Namecheap: MX to `mx.zoho.eu`, plus SPF,
      DKIM (`zmail` selector) and a `p=none` DMARC. Tested both directions —
      Gmail to `hello@` arrives in Zoho, and the reply reaches Gmail's inbox
      rather than spam. The whole setup, including what to check when a send
      fails, is in `ops/zoho-mail-setup.md`.

### 1c. Between launch and the first payment

**The decision, made deliberately:** the site goes public before the money and
legal plumbing is finished. Nothing on the site takes a payment — every page
asks people to email — so publishing commits us to nothing we cannot honour.
Everything in this section has to be true before the first person actually
*pays* us, which is a different and later moment.

**That changes once the audit's pay button ships.** Still true as written today,
and it is why launching was safe — but the £30 audit is now decided as paid on
the site, which ends the "nothing takes a payment" position on purpose. What
that pulls forward is set out in "What taking payment on the site changes"
below. Read the two together; this paragraph is the record of why launch was
safe, not a description of where we're heading.

This is the one place the phase definitions don't line up: "Phase 1 is done
when a stranger can read the site, understand the offer, email us, and pay us
£30." The site can go live before that is true. This section is the rest of it.

**The trigger is an event, not a date.** "Before the first payment" could be a
fortnight away if outreach lands. Two items below cannot be started on the day
someone says yes, so they need starting first.

**Which provider to use for each of these is researched and decided in
`ops/third-party-services.md`** — bank, service address, domain email,
insurance, ICO registration, analytics, client tracking and the delivery
tooling, each with a pick, a cost and the reasoning. Prices there were checked
on 2026-07-28 and should be confirmed on the provider's own site before
committing.

#### Has a lead time — start these before they're needed

- [x] **Business bank account — Revolut Pro, set up.** Owner's decision:
      Revolut Pro rather than the Mettle/Starling pick researched earlier.
      Reasoning and caveats are in `ops/third-party-services.md` C1 — in
      short, it's the account Revolut itself builds for exactly this
      situation (sole trader, freelancer), it's free, it now carries FSCS
      protection since Revolut became a UK bank in March 2026, and going
      with the bank the owner already uses saved real setup time over
      opening somewhere new. One caveat carried forward, not a blocker at
      our balances: FSCS protection for a sole trader is shared across the
      Pro and personal balance under one £120,000 cap, not doubled.
- [ ] **Address for service of documents.** Deliberately deferred pre-revenue
      (see 1a). A virtual office or service-address provider satisfies the
      disclosure requirement without publishing a home address, and runs about
      £20–60/year. **This one should land before we are visibly trading**, not
      merely before the first payment — and see the note in 1a about why this
      site in particular is the wrong place for a home address.

#### Before money changes hands

- [x] **How the £30 audit gets paid — on the website, upfront.** Owner's
      decision, and the right one: at £30 an email-invoice-wait-pay loop costs
      more in admin than the card fee saves. Card fee is roughly 50p on a
      personal card, up to about £1.04 on a commercial one — worth paying to
      remove a round trip and take the money upfront. Full reasoning in
      `ops/third-party-services.md` C2.
      **The mechanism: our own order page, which hands off to a Revolut Pro
      payment link for the money only.** An earlier version of this plan used
      Revolut's own custom fields to collect the details, which needs no page
      built. Rejected, for four reasons — the first being the one that decided
      it:
      - **An abandoned checkout on Revolut's page leaves us nothing.** Field
        values surface against a *successful* payment, so someone who fills
        them in and bails at the card screen is invisible to us. Our own form
        submits first, so a bail still leaves a lead we can follow up. At this
        stage that is worth more than the saved step.
      - **Validation.** We can require the website field and validate it. We
        have no reason to think Revolut's fields do either.
      - **Credibility at the worst possible moment.** Handing a stranger to a
        bare third-party form immediately before asking for £30 spends trust
        exactly where it is most expensive. `CLAUDE.md` puts credibility above
        flair; this is that rule applied to a checkout.
      - **Room for the copy that has to be there** — what happens next, when
        the report lands, and the refund position. Revolut gives us field
        labels and nothing else.
      **The four fields are already written**, on `site/src/pages/contact.astro`:
      business name, website address, services they most want to be found for,
      and the area they serve. The order page collects those, not a new list.
      **Two copy consequences, both to handle when the page is built:**
      - `contact.astro` currently sells "**No forms**, no call-booking
        software, no follow-up sequence" as a virtue, and it is one — it says
        we are not a marketing funnel. Adding an order form is in tension with
        that line and the fix is not to quietly delete it. An order form is not
        lead capture: email stays the way to *ask us something*, and the form
        exists only to buy the thing. Worth writing that distinction out
        properly rather than hoping nobody notices.
      - **The promise gets better, and should be updated to say so.** Contact
        currently offers a reply "within two working days to confirm scope and
        payment", then the report "within one working day of that" — up to
        three days. With scope and payment arriving together, it becomes the
        report within one working day of ordering. That is a materially
        stronger promise and it is now an honest one.
      **Matching payment to submission is manual, and that's fine.** The form
      lands in one place and the payment in another, so they get matched by
      email, by eye. At a handful a month that is a minute's work. Don't build
      an integration for it.
      **This one is blocked — see "What taking payment on the site changes"
      below.** The page cannot go live before the terms, the privacy notice
      and the address for service do.
- [x] **How the £350 Foundation gets paid — invoice, with the contract sent at
      the same time, once both sides agree to start.** Also right, and for the
      opposite reason: at £350 the card fee is real money (roughly £5–10),
      there is already a conversation happening so friction isn't the problem,
      and bank transfer into the Revolut Pro account is free.
      **Decide what starts the clock.** The pricing page promises we come back
      "within two working days of you booking it". With a contract and an
      invoice going out together, "booking" is ambiguous. It should mean
      *payment received*, not signature — otherwise a two-day clock can be
      started by someone who has signed and not paid. Small copy fix on
      `site/src/pages/pricing.astro` when the terms are written.
- [ ] How monthly plans get collected (this matters most — manual collection
      stops being viable somewhere around client five). Note the cancellation
      terms in 1a were written to read the same whichever way this goes, so
      this decision doesn't reopen the copy. Unchanged by the two decisions
      above — the client-five trigger still stands.
- [ ] A simple invoice or receipt we can send. Partly answered: Revolut Pro
      issues both, and Zoho Books is already paid for. Confirm which one we
      actually send before the first payment rather than deciding it live.

#### What taking payment on the site changes

**This is a deliberate break from the launch logic above.** That logic was:
nothing on the site takes a payment, every page asks people to email, so
publishing commits us to nothing we cannot honour. A pay button ends that.
It is the right call for a £30 product, but it moves four deferred items into
hard prerequisites. **None of these is optional once the button is live:**

- **Terms of service, including the refund position.** Currently listed below
  with no deadline. Taking money upfront, before any work is done, makes this
  a prerequisite rather than a tidy-up. It also needs to say plainly what
  happens when we can't do the job — see the refund note below.
- **Privacy notice.** Currently scheduled for "before the first client sends
  us anything". A checkout form collects personal information at the moment of
  purchase, so it moves forward to the same deadline as the button.
- **ICO registration.** Same reasoning, same move forward.
- **Address for service.** Currently "before we are visibly trading". Taking
  payment on the site *is* visibly trading, unambiguously. **This is the real
  dependency:** the pay button is blocked behind the V LOT address landing, or
  the fallback provider if it doesn't — see 1a.

**The refund position needs writing, not assuming — and a required website
field narrows it without removing it.** The order page should require the
website address and validate it, which kills the "paid with no website at all"
case outright. That is worth doing. But it validates *shape, not existence*: a
typo, a dead domain, a parked domain or a Facebook page all pass a URL check.
Actually confirming a site resolves would need a serverless function, and even
a 200 response wouldn't prove the business is auditable — so it isn't worth
building.

What survives the validation, and is what the refund line is actually for:

- A valid-looking URL that is dead, parked, or a typo
- A social profile where we needed a website
- A business outside the area we serve
- A duplicate or accidental payment — paid twice, or on the wrong card
- Someone who changes their mind between paying and us starting
- A business we look at and genuinely can't do useful work for

**Two reasons the line earns its place regardless of how good the validation
gets:**

- **Chargebacks are worse than refunds.** With no stated position, an unhappy
  customer goes to their card issuer instead of to us. That costs a fee and
  counts against the merchant account. A refund we control is the cheaper end
  of the same event.
- **It sells.** The FAQ already answers "why should I trust a company with no
  case studies?" A plain refund line does that same job at the exact moment it
  matters most — a stranger deciding whether to send £30 to a business with no
  trading history. It's a conversion line, not just legal cover.

So: require the website, and still say plainly that if we can't do it, the
money comes back in full.

**Cancellation rights are probably not an issue, but say so in the terms.** The
Consumer Contracts Regulations 2013 give a 14-day cancellation right on
distance sales, but generally only to consumers — people acting wholly or
mainly outside their trade — and not to business-to-business contracts, which
is what we sell. Worth a line in the terms rather than a refund regime, and
worth confirming with the terms rather than taken from here.

**One design constraint.** `CLAUDE.md` bans repeated calls-to-action. The pay
button goes in one deliberate place, not on every page.

#### Before we hold a client's information

- [ ] **Register with the ICO and pay the data protection fee.** Sole traders
      that process personal information must pay it unless exempt, and
      consultancy work for clients is generally in scope. Tier 1 (micro
      organisation) is £52/year, or £47 by Direct Debit. Run the ICO's own free
      self-assessment tool first — there are exemptions and it gives a
      definitive answer for our circumstances. Failing to register or renew
      carries a penalty of up to £4,000 on top of the fee, so £47 is not a close
      call. Renews annually; diarise it the day it's paid.
- [ ] Privacy notice page — we'll be handling client business data and email.
      Due before the first client sends us anything, not before launch, since
      the site collects nothing on its own. Use the ICO's own free privacy
      notice generator (`ico.org.uk/create-your-own-privacy-notice`) — written
      by the regulator, built for sole traders, and updated in 2026 for the Data
      (Use and Access) Act 2025. Paid generators charge for something worse.
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
- [x] Read every page, and checked on both desktop and mobile — owner confirms
      both look good.
- [x] **Sitemap submitted to Google Search Console and confirmed working.**
      Not straightforward — the property still had a stale `sitemap.xml` and
      indexed pages (`/terms`, `/work`, `/approach`, `/privacy`, `/start`) left
      over from whatever occupied this domain before Noven. Checked the actual
      Netlify deploy directly to rule out anything wrong on our side: the
      production deploy is `ready`, built from the current `main`, no redirect
      rules, and its file list is exactly the current 7 pages — nothing stale
      being served. `sitemap-index.xml` itself was confirmed valid by opening
      it directly (a proper `sitemapindex` pointing at `sitemap-0.xml`), so the
      "Couldn't fetch" Search Console showed at first was just Google's own
      timing, not a real fault. Old `sitemap.xml` entry removed, correct one
      resubmitted, now shows **Success, 6 pages, read same day.**
  - **The five leftover pages from the old site are now being cleared.**
    Submitted all five (`/terms`, `/work`, `/approach`, `/privacy`, `/start`)
    to Search Console's **Removals** tool — fast, temporary hide, all showed
    "Processing request". Then ran **URL Inspection → Request Indexing** on
    the same five: each came back **"Indexing request rejected — indexing
    issues were detected during live testing"**, which is the correct
    outcome here rather than a fault — Google live-fetched each URL, found it
    now 404s, and confirmed there's nothing there to index. That's Google
    registering the pages are gone. Ran the same check on the homepage
    (`/`), which queued normally as a real page should — confirming the
    rejections above were specific to the dead URLs, not a wider problem.
    Nothing further to do here; it plays out over the next few days as
    Google's index catches up.
  - Bing Webmaster Tools — not yet done.
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
- [ ] **Ask every question several times and report a rate, not a yes or no.**
      Assistant answers are not deterministic: published testing found the same
      brand query run ten times produced mention rates anywhere from 20% to 80%.
      A single run is noise, and "you don't appear" from one run can be
      disproved by the client in thirty seconds. Say the run count in the
      report. Also worth saying plainly: answers via the APIs differ from the
      consumer apps, so what we see and what the client sees won't match
      exactly. Being honest about both is a real differentiator against tools
      selling confident single-run scores. Full reasoning and the cost model are
      in `ops/third-party-services.md` (section E).
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
      when we can't (their site is on a platform we can't edit). **Ask for it in
      two stages:** the Foundation asks for access *to do the setup*; taking a
      monthly plan is where we ask to keep it. A "no" to the second shouldn't
      threaten the first. See `ops/service-tiers.md` section 3.
- [ ] Decide what happens when the client's site is too broken for the
      Foundation to work — the audit is supposed to say so honestly
- [ ] Agree what we hand over at the end, and how we show what changed
- [ ] Do the first one, time it, then fix the process

### 3c. Monthly plans (£75 / £125 / £250)

**Decided and live — see `ops/service-tiers.md` for the full reasoning.** Three
verbs rather than three intensities: Maintain holds your position, Grow closes
the gaps, Lead beats the competitors being named ahead of you. Question counts
double at each step (10 / 25 / 50), which is checkable in a way "faster pace"
never was. The upgrade engine is the monthly record itself: it reports the gaps
and doesn't close them, so the client sees the same gap every month and nobody
has to sell anything.

- [x] **Define what actually happens each month at each level**, concretely
      enough that a client would recognise the value. Live on the pricing page,
      in how-it-works, and in the structured data.
- [ ] **Validate the numbers by doing it.** 10/25/50 questions at 5 runs each,
      and the one-hour Maintain budget, are estimates — nothing has been timed.
      Roadmap 3a already says to do the first one end to end and time it; these
      are the numbers that check confirms or changes. **The Maintain figure is
      the one that matters most:** at an hour a month it scales past twenty
      clients, at three hours it caps the business around eight.
- [x] **Decided who publishes the Grow and Lead answer pages: we do.** The
      client approves the words, we publish them. Structured data doesn't
      survive copy-paste, so the client-publishes path costs us more time and
      delivers a worse page. Reasoning and the arguments against are in
      `ops/service-tiers.md` section 3.
- [x] **Defined what an answer page is** — not a blog post, not an FAQ entry:
      one question, one permanent page, one URL, built from facts only that
      business has. It's the Foundation's fourth bullet continued monthly, which
      means every Foundation is practice for Grow. Guard rail against sprawl and
      the full definition are in `ops/service-tiers.md` section 3.
- [ ] **Write the publishing fallback into onboarding** — where we can't get
      publish rights, we hand over a complete file with the structured data
      intact plus a one-page paste instruction, then verify it live afterwards.
      That verification is billable time inside the plan, not a favour.
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

### 2026-07-30 (the audit gets its own order page — Revolut's fields aren't enough)
- **Owner pushed back on two things from the entry below, and was right on
  both.** Recorded here rather than quietly amended, because the first version
  was published in the same session.
- **"Why not require a valid website URL so we never take money from someone
  without one?"** Yes — do that, and the order page should. It kills the
  no-website case outright. But it validates *shape, not existence*: typos,
  dead domains, parked domains and Facebook pages all pass a URL check.
  Verifying a site resolves would need a serverless function, and even a 200
  wouldn't prove the business is auditable, so it isn't worth building.
  **The refund line survives, narrowed** — for dead or typo'd URLs, duplicate
  and accidental payments, people who change their mind before we start, and
  businesses we look at and can't help. Plus two reasons independent of
  validation: an unhappy customer with no stated position goes to their card
  issuer instead of us, and a chargeback costs more than a refund we control;
  and the line does real selling work, the same job the FAQ's "why trust a
  company with no case studies?" already does.
- **"Don't we need a contact-style page anyway?"** Yes, and it's the better
  mechanism — this replaces the Revolut-custom-fields plan from the entry
  below. **The deciding reason: Revolut's field values surface against a
  successful payment**, so anyone who fills them in and bails at the card
  screen is invisible to us. Our own form submits first, so an abandoned
  checkout still leaves a lead worth following up. On top of that we control
  validation, we control the copy at the moment of payment, and we don't hand
  a stranger to a bare third-party form right before asking for £30 — which
  `CLAUDE.md`'s credibility-over-flair rule argues against on its own.
- **Found while checking: the four fields are already written.** `contact.astro`
  asks for business name, website, services to be found for, and area served.
  The order page collects those rather than inventing a new list.
- **Two copy consequences, both flagged in 1c rather than fixed now.**
  `contact.astro` currently sells "no forms, no call-booking software, no
  follow-up sequence" as a virtue — which it is, so the fix is to draw the
  distinction properly (email to *ask*, the form only to *buy*) rather than
  delete the line. And the promise actually improves: scope and payment now
  arrive together, so "two working days to confirm, then one for the report"
  collapses to the report within one working day of ordering.
- **Next:** unchanged — the page is still blocked behind the terms, the privacy
  notice and the address for service. Building it is a real design job under
  the `frontend-design` and `ui-ux-pro-max` rules, not a form bolted onto a
  page.

### 2026-07-30 (how each product gets paid for — decided, and it splits by price)
- **Owner's proposal, and it's the right one:** the £30 audit gets paid on the
  website upfront, the £350 Foundation goes out as an invoice with the contract
  alongside once both sides agree to start. Checked it rather than just
  agreeing, and the reasoning holds in both directions.
- **The audit is the exception to "invoice everything", and £30 is exactly why.**
  The standing argument against cards is that fees are a real slice — true at
  £350, inverted at £30. An invoice loop for a £30 sale is several touches and
  a delay of days on a product that promises a report in one working day.
  About 50p buys all of that away and takes the money before the work instead
  of chasing it after. `ops/third-party-services.md` C2 rewritten around this;
  it previously said invoice everything, which was right about the Foundation
  and wrong about the audit.
- ~~**Revolut Pro's payment link does the details capture too**, which is what
  makes the one-step version work — its links carry custom fields that show as
  a page *before* the payment page. One link scopes the audit and takes the
  £30, no form to build, no backend, site stays static.~~ **Superseded later
  the same day — see the entry above.** Those field values only surface against
  a successful payment, so an abandoned checkout would leave us nothing. The
  details get collected on our own order page instead, and the payment link
  takes the money only.
- **Fees, checked today:** 1.0% + £0.20 on domestic personal cards, 2.8% +
  £0.20 on commercial and international ones. Since we sell to businesses, the
  commercial rate is the likely one more often than it first appears — about
  £1.04 on £30. Stripe would be 1.5% + £0.20, better on commercial cards and
  worse on personal, but the gap on £30 is under 40p and isn't worth running a
  second provider and a second reconciliation for.
- **The thing worth flagging loudest: a pay button ends the launch logic, on
  purpose.** Phase 1c rested on "nothing on the site takes a payment, so
  publishing commits us to nothing we cannot honour". Taking £30 on the site
  moves four deferred items into hard prerequisites — terms of service with a
  refund position, the privacy notice, ICO registration, and the address for
  service. **The address is the real blocker**, since taking payment is
  unambiguously "visibly trading", and that's still waiting on V LOT. So the
  button is behind the address, not ahead of it. Written up in 1c under "What
  taking payment on the site changes".
- **Two loose ends the decision creates**, both now recorded: we take £30 before
  knowing the job is doable, so the terms need a plain refund line rather than
  a vetting step (it's £30 — accept the rare refund, and saying so up front is
  what makes paying a stranger feel safe); and "booking" on the pricing page
  needs to mean payment received, not signature, now that a contract and an
  invoice go out together.
- **Checked and probably fine:** the Consumer Contracts Regulations' 14-day
  cancellation right applies to consumers, not business-to-business contracts,
  which is what we sell. A line in the terms, not a refund regime — and worth
  confirming when the terms get written rather than trusted from here.
- **Next:** the monthly plans are untouched and still deferred to client five.
  The audit button can't be built until the terms, privacy notice and address
  exist, so those are the unblocking work — and the address is the one with an
  external dependency, so it stays the long pole.

### 2026-07-30 (business bank account decided — Revolut Pro, not the researched pick)
- **Owner set up Revolut Pro** rather than Mettle or Starling, the pair
  `ops/third-party-services.md` had researched and recommended. Checked
  whether it still holds up rather than taking it on faith, since the
  standing rule is not to invent or wave through business facts.
- **It does.** Revolut Pro is Revolut's own product for exactly this
  situation — sole traders and freelancers, not registered companies, who
  want a separate business balance without a separate application. Free to
  hold, its own account number, and covers invoices, payment links and bank
  transfer natively. Revolut became a UK bank in March 2026, so it now
  carries FSCS protection up to £120,000, same as Starling — with one
  caveat: for a sole trader that cap is shared between the personal and Pro
  balance, not doubled. Not a real risk at our transaction sizes, just noted
  for the record.
- **Also a legitimate reason on its own, not just convenience:** already
  banking with Revolut meant skipping a fresh application elsewhere, and
  Revolut Pro fits the actual need closely enough that switching researched
  providers for it isn't a compromise.
- **Closes the "Business bank account" item in roadmap 1c** — was the long
  pole of that section, now done. `ops/third-party-services.md` C1 rewritten
  to record the decision and reasoning, with the Mettle/Starling research
  kept underneath for context rather than deleted.
- **Left open, not yet checked:** whether Zoho Books' bank-feed integration
  actually connects to a Pro sub-account — Revolut's own integration docs
  are written against Revolut Business, not Pro. Worth confirming next time
  reconciliation is set up; manual entry is the fallback at our volume if it
  doesn't.
- **Next:** the other lead-time item in 1c, the address for service, is
  already in progress via V LOT (see the 29 July entry). Nothing else in 1c
  has a hard dependency on the bank account being open, so the next natural
  step is picking how the £30 audit and £350 Foundation actually get paid
  (1c, "Before money changes hands") now that an account exists to receive
  the transfer.

### 2026-07-29 (Search Console sorted out — sitemap live, old site's shadow found)
- **Owner confirms the site reads well and checks out on both desktop and
  mobile.** Ticked off in 1e.
- **Google Search Console was still carrying the previous occupant of this
  domain.** The "Indexed pages" report listed `/terms`, `/work`, `/approach`,
  `/privacy`, `/start` — none of which exist on this site — and the
  Sitemaps report had a stale `sitemap.xml` (not the `sitemap-index.xml` this
  Astro build actually produces) still reading "Success" from before the
  switch.
- **Ruled out anything wrong on our end before touching Search Console.**
  Checked the live Netlify deploy directly: production, `ready`, built from
  current `main`, "No redirect rules processed", file list is exactly the
  current 7 pages. Then opened `sitemap-index.xml` directly in a browser and
  confirmed it's a valid `sitemapindex` pointing at `sitemap-0.xml`. So the
  "Couldn't fetch" Search Console showed right after first submitting it was
  just Google not having attempted the crawl yet, not a real fault.
- **Fixed:** removed the old `sitemap.xml` entry, resubmitted
  `sitemap-index.xml` alone. Now shows **Success, 6 pages, read the same
  day.**
- **Not fixed yet, and separate from the sitemap:** the five leftover indexed
  URLs above are still in Google's index and will 404 once recrawled.
  Removing a sitemap doesn't deindex anything by itself — that needs Search
  Console's **Removals** tool (fast, temporary) and **URL Inspection →
  Request Indexing** on each stale URL plus the homepage (permanent, and
  also nudges Google's separate favicon cache to refresh).
- **Next session:** run the Removals + Request Indexing pass on the five old
  URLs and the homepage, submit the sitemap to Bing Webmaster Tools too, then
  the one 1e item still open — ask ChatGPT, Claude, Copilot and Perplexity
  what Noven does, and record it dated as our own before-and-after.

### 2026-07-29 (address for service — ordered with V LOT, pending)
- **Researched UK virtual-address providers properly** rather than taking the
  existing `ops/third-party-services.md` note at face value — found and fixed
  a real error in it: Hoxton Mix is not "~£30/year", it's **£180–300/year**
  (£249.99/yr for the bare registered-office tier). That number should not be
  trusted again without checking the provider's own site.
- Found the market splits into two different products that are easy to
  confuse: a **director's/registered-office service address** (~£22–39/yr,
  Companies House use only, often returns other mail to sender, and doesn't
  even legally apply to a sole trader) versus a **business/trading address
  service** (~£72–115/yr, explicitly licensed for a website and stationery),
  which is the one this site actually needs.
- Full comparison with reviews is in `ops/third-party-services.md` B1. The
  honest floor for a reputable provider doing the right product is closer to
  **£115/yr inc VAT** (1st Formations or Quality Company Formations, both
  4.7–4.9 on Trustpilot), not the £30–60 previously assumed.
- **Owner's decision: went with V LOT anyway**, on cost (~£10–48/yr) —
  capital is tight right now and that's a real constraint, not a mistake.
  Flagged clearly first: V LOT's Trustpilot reviews are poor, including
  reports of no service after payment. **Order placed, address not yet
  provided.** Agreed to give it a few days and see what actually arrives
  before treating this as settled.
- **Next session (or when the address lands):** if it works, set the real
  address in the footer and close this item. If it doesn't turn up or mail
  isn't confirmed working within a few days, fall back to 1st Formations or
  Quality Company Formations and treat the V LOT cost as a small loss rather
  than waiting longer on it.

### 2026-07-29 (roadmap 1a closed — the profile role is confirmed linked)
- **The owner confirms the profile's Noven role now links to the real company
  page.** That was the last open step from the previous entry: the role was
  added before the page existed, so LinkedIn had nothing to attach it to and
  kept it as plain text. Retyping "Noven" and picking it from the dropdown
  fixed it — the role shows the Noven logo and the company name opens the
  page.
- **Roadmap 1a is done.** `ops/linkedin.md` is updated to say so rather than
  read as a list of open steps, and this file's checkboxes for the item are
  all ticked.
- **Merged to `main` at the owner's request**, overriding the standing "finish
  on an unmerged branch" rule in `CLAUDE.md`. Explicit call, not a new default.
- **Next session:** 1e's launch checks — read every page fresh, check on a
  phone, submit the sitemap to Search Console and Bing, and ask the assistants
  what they say about Noven.

### 2026-07-29 (the Noven company page is live)
- **`https://www.linkedin.com/company/novenstudio/` exists.** `novenstudio` was
  the only one of the preferred slugs (`noven`, `noven-uk`, `novenstudio`,
  `noven-studio`) still available. The owner created the page, uploaded the two
  images from `assets/linkedin/`, and pasted in the About copy from
  `ops/linkedin.md` §5.4.
- **`businessLinkedIn` is set** in `src/data/business.ts`, stripped of the
  `?viewAsMember=true` LinkedIn appends when previewing your own page — that's
  a view-mode flag, not the canonical address, and the same rule that already
  applied to `founderLinkedIn` (no tracking or session parameters on a value
  that goes into a public repo and public markup) applies here.
- **Confirmed in the built output, not just the source.** `npm run build` runs
  clean, seven pages, and the LinkedIn URL appears in every page's `sameAs` in
  `dist/`. Build artifacts weren't committed.
- **One step of 1a is still owner-only: re-linking the profile role.** The
  owner added Noven as a role on the personal profile before the company page
  existed, so LinkedIn had nothing to attach it to and kept it as plain text.
  Now the page exists, going back into that role and retyping "Noven" should
  offer the real page in the dropdown. `ops/linkedin.md` §0 has the two ways to
  confirm it actually linked (the role shows the Noven logo; clicking the
  company name opens the page) rather than just re-saved text.
- **Next session:** once the profile role is confirmed linked, 1a is fully
  closed and the next thing on the roadmap is 1e's launch checks — read every
  page fresh, check on a phone, submit the sitemap to Search Console and Bing,
  and ask the assistants what they say about Noven.

### 2026-07-29 (the company page is unblocked — images made, holds lifted)
- **The profile side of 1a is done**, per the owner. What's left of that item is
  the Noven company page, so `ops/linkedin.md` now opens by saying so and §5 is
  written as the job in front of you rather than one of two.
- **The `[HOLD until the site is live]` markers are gone from `ops/linkedin.md`.**
  They were written when `novenstudio.co.uk` still served the old website and
  putting that address on LinkedIn would have pointed every reader and every
  crawler at the wrong business. The site is live, so the address goes in
  wherever LinkedIn asks. The reasoning is kept in the document rather than
  deleted — it's the argument we sell, applied to ourselves.
- **New: `assets/linkedin/`** — the two images LinkedIn needs, as PNGs, because
  LinkedIn takes no SVG and every brand asset is one. That was the last real
  blocker on the page. `logo-400.png` is `Social Avatar.svg` placed as-is and
  cropped to the bounds of its own disc, so it fills a circular mask and reads
  as a disc in a square one. `cover-1128x191.png` is brand navy, warm white and
  one sentence in the site's Newsreader — same materials, same method and same
  house pattern as the og card in `assets/og/`. Nothing was redrawn.
- **The cover carries the site's own summary of the service** — "We make your
  business easy for AI assistants to find, understand and recommend", the
  homepage sentence verbatim bar the pronoun. Not the homepage headline: a
  mock-up of the page header showed LinkedIn prints the tagline directly
  beneath the cover, and the tagline and the headline both end "…ask an AI who
  to use", so stacked they said the same phrase twice an inch apart. A first
  attempt used the About page's "small enough that you always know who did the
  work" — true, but it answers *who are you* when a banner should answer *what
  do you offer*. The owner called that, and picked the summary sentence.
- **The full wordmark goes on the cover, and the disc keeps the logo slot.**
  Settled by rendering all three candidates at 48px, which is the size LinkedIn
  shows a company logo at in the feed: the disc holds up, the wordmark on navy
  goes cramped, and the wordmark on warm white nearly vanishes because
  LinkedIn's feed background is white too. The cover is 1128×191, which is the
  shape a horizontal wordmark was drawn for. It sits right-aligned — the badge
  overlaps the bottom-left, so the right edge is the only part of the strip
  that can never be covered.
- **Found while writing it up: the profile's Noven role is probably linked to
  nothing.** LinkedIn attaches a real company page to an experience entry only
  if the page exists when you type the name; otherwise it silently keeps the
  text and links nowhere, and it looks identical on your own screen. The
  profile was written before the page — so once the page is up, the Company
  field on that role has to be retyped and picked from the dropdown. The link
  between the two pages is the entire point of having both.
- **`render.mjs` refuses to write a clipped image.** The first attempt at both
  PNGs used `--window-size`, which quietly laid the page out taller than the
  frame and cropped the cover mid-sentence. The script now reads the laid-out
  size and throws instead — a half-sentence cover is exactly the kind of thing
  that ships unnoticed.
- **Couldn't verify the live site from this session:** `novenstudio.co.uk`
  isn't on this environment's outbound allow-list, so both `curl` and the fetch
  tool got a 403 from the egress proxy. Lifting the holds rests on the owner's
  confirmation and the last session's record of the deploy, and
  `ops/linkedin.md` says so where it matters rather than implying it was
  checked.
- **Still `null`: `businessLinkedIn`.** It can't be set until the page exists
  and has a URL. Paste the slug into the next session and it's a one-line
  change.
- **Next session:** either the company page slug once it exists, or 1e's launch
  checks — read every page fresh, check on a phone, submit the sitemap to
  Search Console and Bing, and ask the assistants what they say about Noven.

### 2026-07-29 (the domain address works, and the site uses it)
- **`hello@novenstudio.co.uk` sends and receives.** Gmail to `hello@` lands in
  Zoho; the reply lands in Gmail's inbox rather than spam, which for a domain
  Gmail has never seen before is the practical sign SPF and DKIM line up.
- **`site/src/data/business.ts` now carries it**, so the contact page and the
  JSON-LD on every page changed with one value. `ops/linkedin.md` updated in
  the two places it quoted the Gmail address as copy to paste.
- **The first send out of Zoho failed and the instinct was to blame the DNS.**
  It wasn't: sending doesn't touch MX, which only governs mail coming in. It
  was Zoho's hold on outbound from a mailbox created minutes earlier, and
  replying to a received message went straight out. That reasoning is now in
  `ops/zoho-mail-setup.md` so the next person doesn't start editing records
  that were already right.
- **The Gmail address stays open and forwarding.** It is on the live site's
  cached copies, in Search Console and in whatever assistants have already
  read — closing it would strand real mail.
- **Price correction: £14.40, not £12** — the £12 figure was ex-VAT.
  `ops/third-party-services.md` now says what actually left the account.
- **Loose end for the owner:** the Gmail address was removed from the Zoho
  *account* and `hello@` put in its place, so account recovery for the mailbox
  now goes to the mailbox. Add the iCloud address as an alternate.
- **Decided, so it doesn't get re-litigated:** Zoho is the inbox from now on,
  and Gmail is not a second one. The Gmail *account* stays regardless — it
  owns the Search Console property, the `hellonovenuk-lang` GitHub login and
  Netlify's notifications, so it is an identity rather than an address. Its
  mail forwards into Zoho. Mirroring Zoho back into Gmail so a tool can read
  it is deliberately not being built at zero enquiries; the trigger for
  revisiting is a handful a week, and the method then is Gmail fetching over
  POP with Send-mail-as through Zoho's SMTP, so `hello@` stays the sending
  identity.
- **Merged to `main` at the owner's request**, overriding the standing "finish
  on an unmerged branch" rule in `CLAUDE.md` for the fourth time. Explicit call
  each time, not a new default.
- **Next session:** 1e's launch checks — read every page fresh, check on a
  phone, submit the sitemap to Search Console and Bing, and ask the assistants
  what they say about Noven.

### 2026-07-29 (domain verified — the rest of the mail setup is written down)
- **Zoho has confirmed ownership of `novenstudio.co.uk`**, so the step the last
  session was waiting on is done.
- **New file: `ops/zoho-mail-setup.md`** — the remaining steps in order, with
  the exact records: create the `hello@` mailbox, add MX (`mx.zoho.eu`,
  `mx2`, `mx3`), SPF, DKIM and a `p=none` DMARC, prove SPF/DKIM/DMARC pass on
  a real message, forward the Gmail address rather than closing it, then set
  `email` in `site/src/data/business.ts`.
- **All hostnames are `.eu`, not `.com`** — the account is on the EU data
  centre, the same fact that ruled out the free plan.
- **Two things that fail quietly and so are called out in the file:** a
  leftover MX record from a previous setup keeps taking the mail, and a second
  `v=spf1` record makes SPF a permanent error rather than just a weaker check.
- **DNS is at Namecheap**, and the steps are now written against its actual
  screens: MX rows live in a separate MAIL SETTINGS section that only appears
  once the dropdown is set to Custom MX, hosts are relative (`@`, not the full
  address), and a 2048-bit DKIM key exceeds Namecheap's 255-character limit —
  regenerate at 1024-bit rather than splitting it across rows.
- **The site still shows the Gmail address deliberately.** `business.ts` gets
  changed once a test message actually arrives at `hello@`, not before.
- **Next session:** make that one-line change in `site/src/data/business.ts`
  when the owner confirms mail is flowing, and tick the item in 1b.

### 2026-07-29 (Zoho Mail setup paused on DNS propagation)
- **Progress on `hello@novenstudio.co.uk`:** domain added in Zoho's Admin
  Console, Mail Lite plan bought (see below for why not the free plan), and
  the domain-verification TXT record has been added to `novenstudio.co.uk`'s
  DNS. Stopped there deliberately — Zoho's own verification can take up to a
  day to propagate, so there's nothing left to do until it clears.
- **Next session:** once the TXT verifies — add the MX, SPF and DKIM records
  Zoho then shows, create the `hello@novenstudio.co.uk` mailbox under Users,
  then update `founderEmail`/contact email in `site/src/data/business.ts` and
  tick this off in 1a.

### 2026-07-29 (Zoho Mail's free plan turned out not to be reachable)
- **Correction found while actually setting up `hello@novenstudio.co.uk`:**
  Zoho no longer offers its Forever Free plan to new sign-ups on the EU, US
  or AU data centres. The owner's account landed on `zoho.eu` and the setup
  wizard only offered paid plans — no free option shown at all.
- **No real decision changed.** `ops/third-party-services.md` had already
  named Mail Lite (~£12/yr) as the fallback if free wasn't usable, so that's
  simply now the number to use rather than a new cost appearing from nowhere.
  It also brings IMAP/POP, which the free plan lacks — actually the better
  outcome for using it in a normal mail app. Pick "Mail Only → Mail Lite" in
  Zoho's plan screen, not "Workplace" (that tier bundles shared team drive
  storage nobody here needs).
- Updated `ops/third-party-services.md`'s cost figures and the pre-revenue
  total (£40–75 → £50–85/yr) to match.
- **Next session:** finish the Zoho Mail DNS setup (domain verification, MX,
  SPF, DKIM), create the `hello@novenstudio.co.uk` mailbox, then update
  `founderEmail`/contact email in `site/src/data/business.ts` and this
  roadmap once it's live.

### 2026-07-29 (the site is live)
- **Noven is public.** The owner pointed the Netlify deploy for
  `novenstudio.co.uk` at `main` and it deployed correctly — the old website no
  longer serves from the domain. This is the "biggest remaining blocker" line
  that's been at the top of this file since it was written; it's gone now.
- **HTTPS confirmed via Netlify's own API, not just eyeballed:** the project's
  `primarySiteUrl` reads `https://novenstudio.co.uk` and the current deploy
  state is `ready`. (This session's sandbox can't reach the public internet
  directly — outbound requests to arbitrary hosts are proxy-blocked — so the
  Netlify MCP connection was the way to check rather than curling the site.)
- **Found while checking:** the Netlify team also has three older/unused
  projects — `noven-2-0-preview`, `noven-preview`, `novenwirral` — all on
  `.netlify.app` addresses, not the custom domain.
- **No old URLs to redirect.** `novenstudio.co.uk` has only ever served the
  owner's own projects (confirmed by the owner), not a prior unrelated
  business with its own external links, so there's nothing for `netlify.toml`
  to redirect.
- **The three old Netlify projects can't be deleted from a session** — the
  connected Netlify MCP tools only support updating visitor access, forms,
  project name, and env vars, plus creating new projects; there's no
  delete-project operation. Deleting `noven-2-0-preview`, `noven-preview` and
  `novenwirral` is owner work in the Netlify dashboard (Site settings →
  General → Danger zone), keeping `kaleidoscopic-cuchufli-ff7b1a` (the one
  serving the live domain).
- **Next session:** consider a `hello@novenstudio.co.uk` address, then 1e's
  launch checks: read every page fresh, check on a phone, submit the sitemap
  to Search Console/Bing, and ask the assistants what they say about Noven —
  our own first before-and-after.

### 2026-07-29 (apex vs www decided)
- **Apex vs www is closed.** `novenstudio.co.uk` is the primary domain, already
  configured from previous projects, and `www.novenstudio.co.uk` redirects to
  it. No file changes needed — `site/astro.config.mjs` and
  `site/public/robots.txt` already assumed the apex.
- **Next session:** the rest of 1b — point Netlify at this repo (the old site
  is currently live on the domain), read the preview end to end, confirm
  HTTPS, decide on redirects for any old URLs, then switch the domain over.

### 2026-07-29 (the LinkedIn doc has no open questions left)
- **The remaining four owner questions are answered and applied.** M&S and
  Tesco can be named, so the unnamed variant is dropped. He resigned from
  Maersk, so nothing on the profile needs to account for the ending. Port Brief
  is finished. Headline chosen outright rather than offered as options.
- **Headline settled:** *"Founder of Noven — I help UK service businesses get
  found when their customers ask an AI who to use. Eight years in global
  shipping operations before this."* 154 characters. The shipping sentence
  stays while Noven is unknown — it's the reason a stranger reads the second
  line, and it now survives checking.
- **"Pre-launch" was treated as "no start date", and it isn't.** A business
  starts when the work starts, not when the site goes live. The doc says to use
  the month work on Noven began — July 2026 at the latest, since that's the
  repo's first commit, earlier if the domain or the decision came first. Not
  picked here; the owner knows which month and it isn't ours to assign.
- **The consequence was written down rather than glossed:** leaving Maersk in
  Jun 2025 and starting Noven in Jul 2026 shows a thirteen-month gap. Said
  plainly that it matters far less for a prospect checking you out than for a
  hiring manager, and that it doesn't get papered over with stretched dates.
- **Port Brief removal is a seven-place sweep, not one paragraph.** Replacing
  the About text leaves the Featured link, any Experience entry, the contact
  website field, a LinkedIn newsletter with its own subscriber list, and any
  pinned post. A half-removed project is worse than a present one — it leaves a
  live-looking promise nobody is behind. Also flagged: decide what
  `portbrief.co.uk` itself does now, since a live site for a finished project
  is a second source contradicting us.
- **Nothing about Port Brief exists in this repo or on the site** — checked.
- **Section 6 is now a closed record**, kept for the reasoning rather than as a
  to-do. One preference is left open: whether to reformat the three older job
  descriptions to match the new one.
- **Next session:** unchanged — Netlify. Apex vs www, read the preview end to
  end, then switch the domain off the old site. That unblocks every `[HOLD]`
  in the LinkedIn doc.

### 2026-07-29 (the bio says eight years, because it is eight years)
- **"Nearly ten years" is corrected to "eight years" everywhere it appeared.**
  The owner confirms the real figure is eight years nine months, all inside the
  Maersk group. Changed in `site/src/pages/about.astro`, `ops/service-tiers.md`
  §7, item 1a above, and the LinkedIn copy. Site rebuilds clean, seven pages.
- **"Eight" rather than "nearly nine", which is also true.** The dates on the
  LinkedIn profile read as eight years five months to anyone counting, so
  "nearly nine" invites a check it doesn't quite pass. Eight is true against
  both the owner's figure and the profile's own dates. Round down when the
  reader can count — this is the one claim on the site a stranger can verify in
  four seconds, and the business is unsellable if it doesn't hold.
- **Small unresolved arithmetic, no copy impact:** 8y9m and the profile's
  visible Jan 2017 – Jun 2025 don't quite agree. Noted for the owner to glance
  at while editing; nothing depends on it.
- **The "managing administrative staff" bullet was rewritten, not just
  numbered.** The owner doesn't line-manage them — around six admin staff sat
  under his purview, he owned the process they worked to, and escalation went
  to their own manager. "Managed a team of six" was the easy phrasing and would
  have been false, on a profile whose argument is that he keeps information
  accurate. It now describes process authority, which is what it was.
- **Two of the seven open questions are closed.** Remaining: Noven's start
  date, whether M&S and Tesco can be named, why the Maersk role ended, whether
  Port Brief is finished, and the current headline text.
- **Next session:** unchanged — Netlify. Apex vs www, read the preview end to
  end, then switch the domain off the old site.

### 2026-07-29 (the LinkedIn copy is written)
- **`ops/linkedin.md` written.** Everything needed to do roadmap 1a's LinkedIn
  half in one sitting: replacement About copy for the personal profile, the
  missing Maersk job description, fixes to the three existing ones, and
  field-by-field copy for the Noven company page. The owner still has to sign
  in and paste it — nothing there can be done from a session.
- **The current About section is entirely about Port Brief**, a project that
  isn't live. It tells readers to subscribe at `portbrief.co.uk` and promises
  them an email every Tuesday, so it is currently making a standing promise
  nobody is keeping. That comes down whether or not the new copy is ready.
- **The most senior role on the profile has no description at all** — Global
  Customer Experience Consultant, Sep 2024 – Jun 2025, global operational lead
  for M&S and Tesco. Written from the owner's account of it. Client names are
  used, with an unnamed variant beside it pending a check of the Maersk
  contract.
- **A real consistency problem, and it's ours.** The site's About page says
  "nearly ten years in operations at Maersk"; the profile's own dates run
  Jan 2017 – Jun 2025, which is eight years five months. Anyone can check it
  in four seconds, in the same place we claim it. Either earlier roles are
  missing from the profile and should be added, or `about.astro` says eight.
  Not changed here — the owner has to say which. It is question 1 in the doc.
- **Sequencing catch: no website field gets filled in yet.** `novenstudio.co.uk`
  still serves the old site, so publishing it on LinkedIn today points every
  reader and every crawler at something that isn't Noven. Each website field in
  the doc is marked `[HOLD until the site is live]`. Blank is recoverable;
  wrong and cached is what the audit is paid to find on other people.
- **Company page before profile edits**, not after — typing the company name
  into an Experience entry only attaches the real page (and its logo, and the
  return link) if the page already exists.
- **The company page's location must be city-level only.** Same one-way-door
  reasoning already applied to the site footer in 1a: a page built to be
  crawled and quoted is the worst place to publish a home address.
- **LinkedIn takes no SVG**, and every brand asset is one. The logo needs a
  400×400 PNG export of `Social Avatar.svg`; the cover needs a 1128×191 strip,
  which is a different aspect ratio from `Email Banner.svg` and so needs
  re-composing rather than resizing. Export, never redraw.
- **Seven questions are open for the owner**, gathered in section 6 of the doc
  — headcount managed, Noven's start date, whether the client names can be
  used, and the ten-years question above.
- **Next session:** unchanged — Netlify. Apex vs www, read the preview end to
  end, then switch the domain off the old site. That also unblocks every
  `[HOLD]` in the LinkedIn doc.

### 2026-07-29 (the LinkedIn URL is in)
- **`founderLinkedIn` is set**: `https://www.linkedin.com/in/kieran-smith-50b953143`,
  supplied by the owner. The About page now links to it in the bio, and the
  founder's Person in the structured data carries it as `sameAs`. The
  `[PLACEHOLDER]` that was showing on the About page is gone. That closes the
  last open piece of the founder bio, and means the ten-years-at-Maersk claim
  is now checkable by a reader who wants to check it.
- **The tracking parameters were stripped.** The shared link carried
  `?utm_source=share_via&utm_content=profile&utm_medium=member_ios`. Those
  describe how the link was shared, not the person, and this value gets
  published verbatim inside the JSON-LD. Checked for the thing that actually
  matters first: no `loginToken` or session parameter, and the URL names the
  person via `/in/` rather than being one of the viewer-relative forms
  (`/me`, `/nhome`) that were tried and rejected in earlier sessions.
- **One verification is left with the owner and can't be done from here:**
  open the URL in a private window and confirm the profile loads without a
  login prompt. LinkedIn blocks automated fetches, so a check from this session
  would tell us nothing either way. Noted in 1a.
- **New roadmap step in 1a: amend the profile, and create a Noven business
  page.** These were half-buried in a note about "while you're in the
  settings"; they're now their own item, because the second half is a real
  piece of work rather than a settings tweak. The profile should point back at
  `novenstudio.co.uk`, and a business page gives an assistant a second source
  about Noven that agrees with the site word for word.
- **`businessLinkedIn` is wired but null**, the same way `founderLinkedIn` and
  `founderPhoto` were before they existed. It joins the *Organization* as
  `sameAs` — the business claiming a page as its own, which is a different
  statement from the founder claiming a profile. When the page exists, setting
  that one value is the whole job.
- **Merged to `main` at the owner's request**, overriding the standing "finish
  on an unmerged branch" rule in `CLAUDE.md` for the third time. Explicit call
  each time, not a new default.
- **Next session:** Netlify — apex vs www, read the preview end to end, then
  switch the domain off the old site. Zoho Mail's DNS records are worth doing
  in that same sitting.

### 2026-07-28 (what an answer page is, and who publishes it)
- **"Answer page" was doing undefined work in the Grow and Lead descriptions.**
  Now defined: not a blog post (dated, buried by the next one, decays), not an
  FAQ entry (one line among twenty on a page that's strongly about nothing).
  **One question, one permanent page, one URL**, built from facts only that
  business has. Written up in `ops/service-tiers.md` section 3.
- **It isn't a new product — it's the Foundation's fourth bullet continued
  monthly.** That matters for the owner's confidence: every Foundation delivered
  is practice for Grow, and no new skill has to appear between them.
- **Decided: we publish the pages ourselves.** The client approves the words, we
  publish them. **Structured data does not survive copy-paste** — a visual
  editor strips the JSON-LD, the heading hierarchy and the internal links, so
  what lands is prose with the product removed. We'd have to verify it
  afterwards anyway, which makes the client-publishes path *more* of our time
  for a worse page, and it's the exact mechanism by which facts drift.
- **The arguments against are real and are recorded, not dismissed** — ongoing
  publish rights is a bigger ask than one-off Foundation access; twenty live
  admin logins is a security surface that pulls on the ICO obligations in 1c;
  blame attaches to whoever touched the site last; some platforms and some
  regulated clients simply won't allow it. Hence a named fallback and a
  two-stage access request rather than a flat rule.
- **No site copy changed, and that was checked rather than assumed.** The FAQ
  already says *"You will not need to write anything yourself unless you want
  to"* and asks for *"access to update your website (or a contact for whoever
  manages it)"* — both paths were already anticipated, so the decision needed no
  new promise. "We don't build websites" in how-it-works still holds: publishing
  a page on a site someone already has is not building them one.
- **A guard rail went in with it.** Two pages a month at Lead is twenty-four a
  year. If we can't write ~400 words that only that business could write, it's
  an FAQ line, not a page. Thin pages hurt.
- **Merged to `main` at the owner's request**, again overriding the standing
  "finish on an unmerged branch" rule in `CLAUDE.md`. Explicit call, not a new
  default.
- **Next session:** unchanged — the LinkedIn URL (steps in 1a), then Netlify:
  apex vs www, read the preview end to end, then switch the domain off the old
  site. Zoho Mail's DNS records are worth doing in that same sitting.

### 2026-07-28 (the monthly levels say what they actually are)
- **The three monthly plans now do three different jobs rather than three
  intensities of one job.** Maintain holds the position the Foundation built,
  Grow closes the gaps, Lead gets you named ahead of competitors rather than
  alongside them. Live on the pricing page, in how-it-works, and in the
  structured data. Full reasoning in `ops/service-tiers.md`.
- **Question counts are now stated: 10, 25, 50, asked five times each.** That is
  a promise a client can check, which "faster pace and broader coverage" never
  was. It also maps to our real costs in both API calls and time, so the price
  steps are defensible from the inside as well as the outside.
- **The upgrade path is the monthly record, and it required no new copy.**
  Maintain reports which questions you're missing from and doesn't close them.
  The client reads the same unclosed gap every month; some will be content to
  hold position and that's a fine outcome, some will ask us to fix it. Nobody
  has to sell anything, which is the only version of this that fits the site.
  Grow to Lead runs on a different and stronger trigger — a named competitor.
- **Market research changed the framing.** UK local search agencies start around
  £395+VAT/month and typically charge £500–1,500; agencies doing this work
  specifically quote $1,500–10,000. **We are roughly a fifth of the UK floor,
  and Lead is still cheaper than the cheapest agency's entry package.** That's a
  deliberate position serving businesses agencies have abandoned — but it means
  agency tier logic doesn't transfer. Our levels are separated by how much of
  the owner's time each consumes, not by hours of labour sold.
- **The number that decides the ceiling is Maintain's delivery time.** At about
  an hour a month it scales past twenty clients; at three hours it caps the
  business around eight with no growth without a price rise. So Maintain gets
  systematised from client one and nothing bespoke happens inside it. Anything
  genuinely bespoke is a reason to talk about Grow, not to do it for free.
- **Worth knowing for year one: the Foundation is the income, the monthlies are
  the tail.** One £350 Foundation is nearly five months of a Maintain client
  delivered in one go. Converting audits into Foundations matters more early
  than converting Maintain clients into Grow clients — a different activity from
  upselling, and a better use of effort.
- **The levels happen to sequence in the order the owner will get good at
  them:** Maintain is a checklist, Grow is writing, Lead needs judgement about
  why an assistant favours a competitor. Nobody buys Lead in month one. That's
  lucky, and a reason not to disturb the structure.
- **Verified rather than assumed:** build clean at 7 pages, all JSON-LD parses,
  and both homepage code panels are still byte-identical to the JSON-LD in the
  head — the property the whole homepage argument rests on. No placeholders and
  no banned jargon in the built output.
- **Found while doing it:** the `summary` field on every plan in `business.ts` is
  defined and documented as "used in the record panels" but **nothing reads it**.
  Left alone rather than churned — the values still fit the new framing — but it
  is either dead code to delete or a panel that was meant to exist and doesn't.
- **Merged to `main` at the owner's request**, knowingly overriding the standing
  "finish on an unmerged branch for review" rule in `CLAUDE.md`, as with the
  founder photograph. One explicit call, not a new default.
- **Next session:** unchanged — the LinkedIn URL (steps in 1a), then Netlify:
  apex vs www, read the preview end to end, then switch the domain off the old
  site. Zoho Mail's DNS records are worth doing in that same sitting.

### 2026-07-28 (third-party services researched)
- **New file: `ops/third-party-services.md`.** Every outside service the roadmap
  implies we need, researched and decided: a pick, a cost and the reasoning for
  each. Ordered by when we need it rather than by topic, matching how the
  roadmap is now sequenced. Prices were checked on 2026-07-28 and the file says
  so — they move, and it tells you to confirm before committing.
- **Total committed spend before the first client pays is about £40–75 for the
  year**, nearly all of it the service address. Everything with a real monthly
  cost is deferred until there's revenue to judge it against.
- **The picks, briefly:** Mettle or Starling for the bank (both free; avoid
  Tide's free tier — 20p per transfer and no FSCS protection). Hoxton Mix or
  similar for the service address at ~£30–60/yr. Zoho Mail for
  `hello@novenstudio.co.uk` — free, or $12/yr for IMAP — chosen because we
  already have Zoho Books, which makes it a tenth the cost of Google Workspace.
  Cloudflare Web Analytics, free and cookieless so no consent banner. Bitwarden.
  Zoho Bigin later, when a spreadsheet stops working.
- **Gap found: we were not registered with the ICO, and it wasn't in the
  roadmap at all.** Sole traders processing personal information owe the data
  protection fee unless exempt — £52/yr, or £47 by Direct Debit — and failing to
  register carries a penalty of up to £4,000. Now in 1c, with a note to run the
  ICO's free self-assessment first in case an exemption applies.
- **The privacy notice has a free answer:** the ICO publishes its own generator,
  built for sole traders and updated in 2026 for the Data (Use and Access) Act
  2025. Written by the regulator that enforces the rules, so it beats any paid
  template.
- **The big delivery decision: don't buy an AI-visibility monitoring platform.**
  They exist and they're mature, but they're priced per brand tracked, which is
  the wrong shape for an agency. The cheapest is about £20–23/month for one
  brand and ~15 questions — roughly 30% of a £75 Maintain plan, and a
  non-starter against a £30 one-off audit. Running the questions ourselves
  through the assistants' APIs lands **under £2 per audit**; Google's free
  grounding allowance alone covers 25–40 audits a month at zero cost. The
  strategic argument matters more than the cost: the audit *is* the product, and
  a question set we build compounds into an asset a subscription never becomes.
- **Methodology finding that changes what we can honestly sell.** Assistant
  answers are not deterministic — the same query run ten times has been found to
  produce mention rates from 20% to 80%. So every question must be asked several
  times and reported as a rate. A single-run "you don't appear" can be disproved
  by the client in half a minute, which is a refund conversation. Written into
  3a, because it shapes the product rather than just the tooling.
- **Cheap evidence found:** Cloudflare's free plan shows which AI crawlers hit a
  site, by category. That turns "we opened up crawler access" into a dated,
  checkable before-and-after — worth a lot to a business with no case studies.
  Caveat: Cloudflare's 2026 crawler verification is default-on, so some sites
  may now be blocking crawlers unintentionally. That's an audit finding in
  itself.
- **Three questions left for the owner**, written into the new file rather than
  guessed: whether any existing insurance policy already covers this and how to
  describe the Foundation to an insurer; whether we're willing to ask clients to
  move DNS to Cloudflare; and how many questions × how many runs makes one
  audit, since that sets both the tool cost and whether £30 is sustainable.
- **Next session:** unchanged — the LinkedIn URL (steps in 1a), then Netlify:
  apex vs www, read the preview end to end, then switch the domain off the old
  site. Zoho Mail's DNS records are worth doing in that same sitting.

### 2026-07-28 (the founder photograph)
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
