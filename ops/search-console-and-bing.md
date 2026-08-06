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

### 1.2 Verify it with a TXT record at GoDaddy

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

### 1.4 Change of Address, from the *old* property

This is the step that tells Google the two domains are one business rather than
two, and it is the reason the old property must not be deleted.

Go to the **`novenstudio.co.uk`** property → **Settings** → **Change of
address** → select `wardith.co.uk` as the destination → **Validate & Update**.

**It checks the redirects itself.** Netlify 301s every non-primary domain to the
primary, page for page, and `wardith.co.uk` is primary — so this should pass
without anything being written. If it reports the redirects are missing, stop:
that means the domain flip has regressed, and that is a bigger problem than
indexation.

**If the tool refuses the pairing, do not fight it.** The two properties may be
different types, and the constraint changes. The 301s carry most of the signal
on their own; Change of Address accelerates it and makes the intent explicit,
but it is not the load-bearing part. Note what it said and move on.

**Keep the old property forever.** It is the only way to see what is still being
served from the dead name, and deleting it destroys the before/after that G2 in
the rename document wants at the six-month check.

### 1.5 Ask for the important pages directly

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
