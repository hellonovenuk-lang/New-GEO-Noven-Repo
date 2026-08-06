# Search Console and Bing — getting `wardith.co.uk` indexed

**Internal document.** Written 2026-08-06. Steps to follow inside Google Search
Console, Bing Webmaster Tools and the GoDaddy DNS panel — all of which only the
owner can sign into.

**Why this is the job now.** The site is live and correct as Wardith, and the
company page corroborates the name. Neither of those puts the domain in an
index, and **an assistant asked about a URL it cannot retrieve falls back to
whatever it can** — which is still the old name. Two of the self-audit's three
findings are downstream of indexation, and finding 2 is entirely this:
`site:novenstudio.co.uk` returned nothing on Bing, **and Copilot answers from
Bing**.

**Everything here is free.** `ops/plan-to-1-september.md` has the business under
a spending freeze until 26 August and nothing below breaches it. If a screen
asks for payment, something is wrong — stop and say so.

**One principle throughout, borrowed from `ops/zoho-mail-setup.md`: if a screen
shows you a value that differs from one written here, trust the screen.** These
consoles change their wording and their menus more often than this file gets
read.

---

## Before you start: which account

**Sign in as `hello.noven.uk@gmail.com`.** It already owns the
`novenstudio.co.uk` property, and **Change of Address needs you to be an owner
of both the old and the new property** — using a different account means the
tool will not offer the pairing at all.

Yes, that address carries the dead name. It stays: `ops/rename-to-wardith.md`
F10 settled it. It is an *identity*, not a brand surface, and it owns the GitHub
login and Netlify's notifications as well as this. Nobody sees it.

---

## Part 1 — Google Search Console

### 1.1 Add `wardith.co.uk` as a new property

**The new domain is a new property.** There is no rename: a Search Console
property is bound to the host it was verified for.

Search Console → the property dropdown, top left → **Add property**.

You are offered two types. **Take `Domain`, not `URL prefix`:**

| | Domain property | URL prefix |
|---|---|---|
| Verified by | One DNS TXT record | File, meta tag, Analytics, or DNS |
| Covers | `wardith.co.uk`, `www.`, `http://`, `https://` — all of it | Only the exact prefix you typed |

You already control DNS for this domain at GoDaddy, and the apex/`www` split is
exactly the thing a Domain property removes. Enter `wardith.co.uk` — **no
`https://` and no `www`**, just the bare domain.

### 1.2 Verify it — and on GoDaddy this is one click

**Done 2026-08-06, and it never needed the hand-typed record below.** Search
Console offered to verify automatically, took the owner straight to GoDaddy to
approve it, and wrote the TXT itself. **Take that route whenever it is offered.**
It is what the `_domainconnect` CNAME in the zone is for, and it removes the
error class that actually happens on this account — a transposed character,
caught once already on `wardith.uk`'s apex A record.

The manual steps are kept below for the two domains that may still need them,
and for whenever the automatic flow is not offered.

Google shows a string starting `google-site-verification=`. Copy it.

GoDaddy → **My Products** → `wardith.co.uk` → **DNS** → **Add New Record**:

| Type | Name | Value | TTL |
|---|---|---|---|
| TXT | `@` | `google-site-verification=…` | 1 hour |

**`Name` is relative — type `@`, not the domain.** Typing `wardith.co.uk`
produces `wardith.co.uk.wardith.co.uk`, which resolves to nothing and looks
like a Google fault. This is the same trap D0.2 already caught once on this
account.

**Do not touch the existing TXT records.** There is an SPF record and a Zoho
verification record in that zone. Multiple TXT records on `@` are fine and
normal — *adding* one is safe. What is never safe is a second `v=spf1`.

Press **Verify**. If it fails, wait out the TTL and press it again rather than
adding a second record.

### 1.3 Submit the sitemap

New property → **Sitemaps** → enter:

    sitemap-index.xml

That is the file Astro generates and the one `site/public/robots.txt` already
points at. It indexes `sitemap-0.xml`, which lists the eight real pages — `/404/`
is correctly excluded.

**Do not submit `sitemap-0.xml` as well.** Submitting the index is enough, and
two entries pointing at overlapping sets is noise in the one report you will be
reading to judge whether any of this worked.

### 1.4 Change of Address — check whether it is worth doing at all

**Rewritten 2026-08-06, after the owner pushed back on it, and he was right.**
This section originally said Change of Address "tells Google the two domains are
one business" and treated it as a required step. That framing came from the
standard site-move advice and **it does not fit this business.**

**Change of Address exists to carry accumulated ranking signal across a move.
There is none to carry.** This document's own Phase-B argument in
`ops/rename-to-wardith.md` already settled it: not one of 210 automated answers
cited `novenstudio.co.uk`, the domain was never advertised anywhere but LinkedIn,
and it had a single page view before the switch. Nothing is being transferred.

**The residual reason is the reverse of the one first written down: retiring old
entries, not moving authority.** If Google holds indexed pages describing a
business called Noven, each is a live source for the exact answer the rename was
meant to stop — so replacing them faster has some value. But that depends on
those pages existing, **and nobody has ever checked whether they do.**

**What is actually known, and the gap in it:**

| | Recorded | Means |
|---|---|---|
| Bing | `site:novenstudio.co.uk` returns **zero** | Never indexed. Confirmed in the self-audit |
| Google | "sitemap submitted and confirmed, six pages" | **The sitemap was processed and six URLs read from it.** Not six pages indexed — a softer fact than the sentence reads |

**So run the 15-second check before the tool: `site:novenstudio.co.uk` on
Google.**

- **Zero results** — skip this section. There is nothing to consolidate and the
  tool would achieve nothing. Go to Bing.
- **Results come back** — run it, as below. Those pages are where the Noven
  answer still lives.

**RUN 2026-08-06: four results.** So Google did index the old domain, unlike
Bing, and Change of Address is worth doing. Four pages describing a business
called Noven sit in the index and each is a live source for the exact answer the
rename was meant to stop.

**Four is now the decay baseline.** Re-run `site:novenstudio.co.uk` at the
six-month check and record what is left. That number — how long indexed pages
survive a 301 plus Change of Address — is the one measurement out of this whole
migration that transfers to a client, because it measures something we caused.
See G2 in `ops/rename-to-wardith.md` for why the two *name* question sets are
worth much less than they were first written up as.

Go to the **`novenstudio.co.uk`** property → **Settings** → **Change of
address** → select `wardith.co.uk` as the destination → **Validate & Update**.

**It checks the redirects itself.** Netlify 301s every non-primary domain to the
primary, page for page, and `wardith.co.uk` is primary — so this should pass
without anything being written. If it reports the redirects are missing, stop:
that means the domain flip has regressed, and that is a bigger problem than
indexation.

**If `wardith.co.uk` is not in the dropdown, it is a property-type mismatch**,
and it has a two-minute fix rather than being a dead end. The old property is
most likely a **URL-prefix** property and the new one is a **Domain** property.
Add `https://wardith.co.uk/` as a *second*, URL-prefix property — **both types
can be held for the same site at once and they do not conflict** — verify it off
the DNS record already in the zone, then reopen Change of address and it will be
listed.

**If it still refuses after that, do not fight it.** The 301s carry most of the
signal on their own; Change of Address accelerates them and makes the intent
explicit, but it is not the load-bearing part. Note what it said and move on.

**After it is accepted:**

- **Leave the redirects alone.** Google treats the move as a signal lasting
  roughly 180 days. `ops/accounts.md` already commits to keeping
  `novenstudio.co.uk` registered for at least three years, which is stronger and
  is the binding number.
- **Do not submit the old sitemap again**, and do not delete the old property.
- **Do not expect the four indexed pages to go this week.** Weeks, not days.
  Re-run `site:novenstudio.co.uk` at one month and at six months; **4** is the
  baseline, measured 2026-08-06.
- The old property's numbers falling while the new one's rise is the tool
  working, not something breaking.

**Keep the old property forever. The owner asked directly on 2026-08-06 whether
it could be deleted: no — and this holds even if the check above says to skip
Change of Address entirely.** The two questions were conflated when this was
first written and they are independent:

1. It is the only view of what is still being served from the dead name.
2. It holds the before/after that G2 in the rename document wants at the
   six-month check — *how long a dead name persists* against *how fast a new one
   is learned*. That measurement is the single most useful piece of evidence
   this business could own, and one deletion destroys the first half of it.
3. And if the check does say to run Change of Address, the tool lives inside the
   old property — deleting it takes the tool with it.

It costs nothing to keep and there is no benefit to removing it.

### 1.5 Test the live URL first — this is the check nothing else can do

**Before requesting indexing, use URL Inspection → `https://wardith.co.uk/` →
Test live URL → View tested page → HTML.** That is a live fetch showing exactly
what Googlebot receives. Search the HTML for two strings:

- `PLACEHOLDER` — must be **zero hits**
- `company/wardith` — must appear once, in the JSON-LD

**Why this matters more than it looks.** Every check in this repo runs against
the built output in `dist` or against the Netlify API. **The session's network
policy blocks `wardith.co.uk`**, so no assistant working here has ever seen what
a crawler actually gets from the live host — that is the one link in the chain
this repo cannot verify itself, and it is stated as such in
`ops/own-facts-check.md` row 1. URL Inspection closes it, from the crawler's own
side, for free.

It will say "URL is not on Google". That is expected on a domain days old and is
not a fault.

### 1.6 Ask for the important pages directly

**URL Inspection** (top search bar) → paste a URL → **Request indexing**.

Do these five, and not the whole site:

    https://wardith.co.uk/
    https://wardith.co.uk/ask-your-ai/
    https://wardith.co.uk/ask-your-ai/self-audit/
    https://wardith.co.uk/pricing/
    https://wardith.co.uk/about/

The two `/ask-your-ai/` pages are first among equals: they are the richest
crawlable text on the site for the questions we want to be found for.

There is a daily quota and queue-jumping the whole sitemap does not help. The
sitemap covers the rest.

---

## Part 2 — Bing Webmaster Tools

**Nothing is being migrated here, because there is nothing to migrate.** The
self-audit found Bing had never indexed `novenstudio.co.uk` at all — so there is
no Change of Address to do, no old property to preserve, and no equity to lose.
This is a clean first submission.

**Do not add `novenstudio.co.uk` to Bing.** It would ask Bing to index a domain
that only 301s away, which is work for nothing.

### 2.1 Sign in and import

`bing.com/webmasters` → sign in. It accepts a Google sign-in — **use
`hello.noven.uk@gmail.com`**, the same identity as everything else.

On first sign-in Bing offers **Import from Google Search Console**. Take it.
It carries the verification and the submitted sitemap across, which skips 2.2
and 2.3 entirely.

**Do Part 1 first, then import.** Importing before the Google property exists
imports nothing, and it is not obvious from the screen that that is what
happened.

### 2.2 If the import does not work — verify manually

**Add a site** → `https://wardith.co.uk` → choose **DNS (CNAME or TXT)** and add
what it gives you at GoDaddy, exactly as in 1.2. The same `@` rule applies.

The HTML-file option also works and is arguably cleaner here: drop the file into
`site/public/`, commit, and it deploys to the root. **Prefer DNS anyway** — a
verification file in `public/` is a permanent piece of somebody else's
housekeeping in the repo, and it will outlive the reason it was added.

### 2.3 Submit the sitemap

**Sitemaps** → **Submit sitemap** → the full URL:

    https://wardith.co.uk/sitemap-index.xml

Bing wants the absolute URL here; Google wanted the path. That difference is
real and catches people.

### 2.4 Submit the URLs directly — this is Bing's advantage

**URL Submission** → submit all eight:

    https://wardith.co.uk/
    https://wardith.co.uk/about/
    https://wardith.co.uk/ask-your-ai/
    https://wardith.co.uk/ask-your-ai/self-audit/
    https://wardith.co.uk/contact/
    https://wardith.co.uk/faq/
    https://wardith.co.uk/how-it-works/
    https://wardith.co.uk/pricing/

Bing's daily allowance is in the thousands, not Google's handful, so unlike 1.5
there is no reason to be selective. **For a brand-new domain this is the single
fastest route into an index anywhere**, and it feeds the one that Copilot reads.

---

## What to expect, honestly

**Days to weeks, not hours**, and a new domain with no inbound links is the slow
case. Nothing here can be hurried by doing it twice.

**Do not re-run the self-audit questions the day after.** `ops/audit-method.md`
and the G2 note both depend on the baseline being a real measurement rather than
one taken while the ground was moving. Let it settle.

**The measurement that tells you it worked** is `site:wardith.co.uk` in each of
Google and Bing returning the eight pages. That is a fifteen-second check and it
is worth doing weekly rather than watching the Search Console graphs, which will
be empty and discouraging for a while for reasons that are not faults.

---

## Record it when it is done

- `ops/accounts.md` — the Bing row currently reads "Not done", and the Search
  Console row does not mention which property. Both need the new state and a
  date.
- `ops/own-facts-check.md` — rows 7 and 8 are the Search Console and Bing
  surfaces.
- `ops/audit-setup.md` §5 — the pre-run checklist.
- `ROADMAP.md` — F4 and F5 in the rename list, and 1e's outstanding Bing item.
