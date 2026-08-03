# Website checklist — Noven self-audit

**Internal working note. Never sent to the client.** Filled 2026-08-03 against
`ops/audit-report-template.md`'s pre-send rule: the verdict here must match the
verdict in the report.

**Source of truth for this pass:** the repo at `origin/main`. `site/` on the
working branch is byte-identical to `origin/main` (`git diff --stat origin/main
-- site/` is empty), and Netlify deploys `main`, so reading the source is
reading the deployment — for everything except what a server or CDN does in
front of it. Those items are marked **UNVERIFIED** below and need a live fetch.

**Time:** ~25 min on-site. Group 3 not started.

---

## Before you start

- **Business name, exactly as they write it:** Noven
- **Website:** https://novenstudio.co.uk
- **Town / area served:** the Wirral, UK — serving the United Kingdom
- **What they want to be found for:** getting service businesses recommended by
  AI assistants
- **Site platform:** Astro, static output, custom build, deployed on Netlify
  from GitHub. **Fully editable, no third party holds the keys.** Best possible
  answer to this question — nothing in the Foundation is blocked by access.

---

## Group 1 — Can the assistants get in at all

### 1.1 robots.txt

Present at `site/public/robots.txt`, 713 bytes, unchanged since 27 Jul 2026.

| Crawler | Whose | Result |
|---|---|---|
| `GPTBot` | OpenAI — training and retrieval | **allowed** (named) |
| `OAI-SearchBot` | OpenAI — ChatGPT search index | **allowed** (named) |
| `ChatGPT-User` | OpenAI — live fetch when a user asks | **allowed** (named) |
| `ClaudeBot` | Anthropic | **allowed** (named) |
| `Claude-SearchBot` | Anthropic | **not mentioned** → allowed by catch-all. File names `Claude-User` instead |
| `PerplexityBot` | Perplexity | **allowed** (named) |
| `Perplexity-User` | Perplexity | **allowed** (named) |
| `Google-Extended` | Google — Gemini grounding control | **allowed** (named) |
| `Googlebot` | Google | **allowed** (named) |
| `Bingbot` | Microsoft — Copilot depends on this | **allowed** (named) |
| `Applebot-Extended` | Apple | **not mentioned** → allowed by catch-all |
| `*` (catch-all) | Everyone | **`Allow: /`** — no blanket disallow |

- **Blanket `Disallow: /`?** No. Clean.
- **Sitemap declared?** Yes — `https://novenstudio.co.uk/sitemap-index.xml`,
  which matches the `@astrojs/sitemap` integration's real output path and the
  `site:` value in `astro.config.mjs`. The two agree.
- **Does robots.txt exist?** Yes.

**Nothing to fix in group 1.1.** Two crawler names absent (`Claude-SearchBot`,
`Applebot-Extended`) are allowed by the catch-all anyway, so naming them is
tidiness, not a finding. Worth adding on the next edit; not worth a line in a
client report.

### 1.2 Is anything else blocking them

Direct fetch is still denied by this container's network policy (proxy returns
403 to CONNECT). **Resolved instead from the Netlify deploy record**, which
answers most of it more reliably than a single fetch would.

Live project: `kaleidoscopic-cuchufli-ff7b1a`, deploy `6a6e76ef…`, state
`ready`, published **2026-08-01 22:45:33Z**, branch `main`, framework `astro`.

- **Password protection / SSO login wall?** **No** — `requiresPassword: false`,
  `requiresSSOTeamLogin: false`.
- **Redirect rules?** **None** — "This deploy did not include any redirect
  rules."
- **Header rules?** **None.**
- **Functions or edge functions?** **None deployed.** Nothing can intercept a
  request and serve a challenge.
- **Cloudflare or similar in front?** Netlify serves the apex directly
  (`ssl_url: https://novenstudio.co.uk`). Nothing in the deploy suggests a CDN
  in front, but DNS-level interposition at Namecheap is not visible from here.
  **Residual, low risk.**
- **Country blocking / age gate?** None in the source or the deploy.

**Verdict on 1.2: effectively passed.** There is nothing in the hosting layer
that can turn a crawler away.

### 1.3 Can they read it once they're in

- **Is the visible text in the source?** **Yes.** Astro with no adapter and no
  `output: 'server'` → fully prerendered static HTML. No client-side rendering
  of body copy. This is the failure mode that kills app-style site builders and
  it is absent here.
- **HTTP 200 on key pages, no redirect chains:** deploy state `ready` with no
  redirect rules, so no chains exist by construction. Per-page 200s not
  individually fetched.
- **One canonical home, www or apex not both:** **PASS — verified.** Netlify's
  `primarySiteUrl` is `https://novenstudio.co.uk` — the apex, over HTTPS —
  which matches `astro.config.mjs` and the `Sitemap:` line in robots.txt
  exactly. The risk flagged in the config file's own comment has not
  materialised. All three agree.
- **HTTPS with a valid certificate:** **PASS** — `ssl_url` is the HTTPS apex and
  the deploy is live on it.
- **Sitemap loads and lists what matters:** the `@astrojs/sitemap` integration
  is in the config and the build completed `ready`, so it was generated.
  **The live 200 is the one item still genuinely unverified** — a five-second
  check in a browser.
- **Key pages within two clicks of home:** yes — six pages, all in the nav.
- **Anything important only in a PDF, image or video?** No. The `video/`
  directory holds decoration; every claim is in text.

---

## Group 2 — What is machine-readable

- **Any JSON-LD at all?** Yes, on every page.
- **Does it parse and validate?** Built by typed functions from one data file,
  serialised through `toSource()`, not hand-written — so malformed JSON is
  structurally unlikely. Live validation **UNVERIFIED**.
- **Types present:**
  - `Organization` — site-wide, injected by `Base.astro` on every page
  - `Person` — nested as `founder`, with `alumniOf`, `image`, `sameAs`
  - `ContactPoint` — nested
  - `HowTo` — how-it-works page
  - `Service` + five `Offer` objects — pricing page
  - `FAQPage` — faq page, 12 entries
  - **No `LocalBusiness`.**
- **Does the structured data carry the facts?**

  | Fact | In structured data? |
  |---|---|
  | Legal name | Partly — `Noven` only. The sole-trader note is visible copy, not schema |
  | Trading name | Yes (`name: 'Noven'`) |
  | Address | **No — absent entirely** |
  | Area served | Only `'GB'` |
  | Phone | No — the business has none by design |
  | Email | Yes |
  | Opening hours | No |
  | Services | Yes — `Service` with `serviceType` |
  | Prices | **Yes — all five, with currency** |

- **Does the visible site state a price?** **Yes** — £125, £750, £95, £250,
  £495, on a dedicated page, in text, and again in the `Offer` schema built from
  the same numbers. This is the checklist's "highest-value single fix we ever
  recommend" and it is already done. On a client audit this would be the
  headline strength.
- **Does the site say plainly where they work?** **Partly, and this is the
  finding.** "the Wirral, UK" is visible in the footer of every page, on the
  contact page and in the About bio. But **no named towns** (no Birkenhead,
  Heswall, Bebington, Wallasey), and — more importantly — **the machine-readable
  layer carries no location at all**. `areaServed: 'GB'` is the only geographic
  claim an assistant can read, and "GB" cannot answer "on the Wirral".
- **One `<h1>` per page saying what the page is?** Yes, all six. Three are
  phrased as the customer's own question ("What does Noven cost?", "How does
  Noven get you found?", "What is Noven?") — which is the right shape.
- **Titles that describe the page?** Yes; no "Home | Company Name".
- **Says what it does above the fold, in words, without an image?** Yes — the
  homepage `<h1>` is a full sentence stating the proposition.

**Structured data read against the visible page:** they agree everywhere they
overlap, because both are generated from `site/src/data/business.ts`. The
problem is not disagreement — it is **omission**. The visible page knows the
business is on the Wirral; the machine-readable data does not.

**This explains two of the audit's results directly.** q03 ("someone on the
Wirral") returned Noven zero times out of fifteen, and q07 ("Is Noven on the
Wirral any good") was only answered correctly by Gemini. There is no
machine-readable statement tying the name to the place for anything to match on.

---

## Group 3 — Are the facts the same everywhere

**Mostly not started** — Google Business Profile, Bing Places, Companies House
and the directories still need the owner. But one check ran, and it produced the
most serious finding in this document.

### 3.1 The site is not in Bing's index at all

**`site:novenstudio.co.uk` on Bing returns zero results.** Checked by the owner
2026-08-03.

**This is the most consequential finding in the audit, and it explains a result
the automated runs could only observe.** Copilot's retrieval is Bing. A business
absent from Bing's index cannot be recommended by Copilot no matter what its
website says, how good its structured data is, or how many crawlers robots.txt
invites. The hand-run answers recorded that Copilot never named Noven across
nine answers; this is *why*.

It also means group 1 was passing a test that was never being taken. `Bingbot`
is explicitly allowed in robots.txt, the site is crawlable, and none of that
matters until the domain is submitted.

**The fix is free and takes about fifteen minutes:** register the domain in Bing
Webmaster Tools and submit `sitemap-index.xml`. `ops/accounts.md` already lists
Bing Webmaster Tools as "Not done" under things needed but not in place, with
the note that "Copilot's real diagnostic is Bing indexation, so the audit is
weaker without it". That assessment was right and is now measured.

### 3.2 Google's index carries superseded prices

Google has the **current** business — title, description and About page all
describe AI-assistant visibility, indexed 5 days ago. The earlier claim in this
document that indexes were serving the previous web-design business was **wrong,
and is withdrawn**: it rested on a single US-only search tool holding a much
older snapshot, and Google — the index that actually feeds Gemini — is current.

What Google *does* carry is the pre-repricing price list:

| Plan | In Google's index | Actual (repriced 2026-07-31) |
|---|---|---|
| Audit | **£30** | £125 |
| Foundation | **£350** | £750 |
| Maintain | **£75** | £95 |
| Grow | **£125** | £250 |
| Lead | not shown | £495 |

**This is a wrong fact, not an absence**, which puts it in the report's "what
they believe about you" section rather than the findings list. An assistant
answering "roughly what should it cost" from Google's cached description quotes
**£30 for a £125 product** — and q10 is one of the ten questions.

**Already actioned.** The owner ran URL Inspection on 2026-08-03: *"URL is
available to Google"*, *"Page can be indexed"*, and the live render shows the
current headline. Re-indexing was requested. This should self-correct within
days to weeks, so it is recorded as found-and-fixed rather than outstanding.

### 3.3 The live site is verifiably current

Worth stating plainly, because it is what rules out a broken deployment as the
cause of anything above:

| Evidence | Value |
|---|---|
| Deployed commit | `68fb1fe` — "Merge branch 'claude/noven-audit-readiness-s3t3gb'" |
| Published | 2026-08-01 22:45:33Z |
| Branch | `main` |
| `site/` at `68fb1fe` vs current `origin/main` | **identical** — later commits touch only `CLAUDE.md` and `ops/session-log.md` |
| Google live test | "URL is available to Google", "Page can be indexed" |
| Sitemap | `sitemap-index.xml` returns valid XML pointing to `sitemap-0.xml` |

The site is healthy. Everything above is about what the indexes hold, not about
what the server serves.

### 3.4 The name collides with more businesses than the audit found

Two more, beyond the pharmaceutical company and the builder already in the
report:

| Name | What it is | Why it matters |
|---|---|---|
| `noven.studio` | "Noven — AI Creator Workflow OS" | **The closest collision yet.** An AI company whose domain is `novenstudio` split at the dot. Same word, same sector |
| `noven.io` | "Noven" | A fourth business on the name |
| `nover.studio` | "nover studio" | Not a collision — a confusable near-miss, one letter away |

**At least four businesses answer to "Noven", two of them in AI or tech.**

### 3.2 The name collides with more businesses than the audit found

The same search surfaced two more, beyond the pharmaceutical company and the
builder already in the report:

| Name | What it is | Why it matters |
|---|---|---|
| `noven.studio` | "Noven — AI Creator Workflow OS" | **The closest collision yet.** An AI company whose domain is `novenstudio` split at the dot. Same word, same sector |
| `noven.io` | "Noven" | A fourth business on the name |
| `nover.studio` | "nover studio" | Not a collision — a confusable near-miss, one letter away |

**At least four businesses answer to "Noven", two of them in AI or tech.** This
materially strengthens finding 1 and is new evidence for the renaming decision.

### Still needed from the owner

Google Business Profile, Bing Places, Companies House, professional register,
trade directories, LinkedIn, review counts, and the Bing index check. Fifteen
minutes, hard stop. **Deliberately deferred, not skipped — the report must say
so.**

Also already known from the audit and belonging here: **`novenstudio.co.uk` was
cited as a source zero times in 210 answers**, and the two "noven" domains that
*were* cited (`noven.com`, `noven.build`) belong to other businesses.

---

## Group 4 — Does anything on the site answer the question

| # | Question | Page that answers it | Verdict |
|---|---|---|---|
| q01 | Who can help my business show up when people ask ChatGPT for a recommendation? | `index.astro` — the `<h1>` is this question restated | **answered** |
| q02 | Recommend someone in the UK who gets small businesses mentioned by AI assistants | `index` / `about` — UK stated, but nothing framed as a UK-wide recommendation | **partly** |
| q03 | Someone on the Wirral who can get my business recommended | one FAQ sentence and a footer line | **nothing** |
| q04 | Who's good at getting small service businesses recommended? | `how-it-works`, `serviceName` says "for service businesses" | **answered** |
| q05 | UK businesses doing this for sole traders and small firms rather than big brands | `about.astro` — "almost no small firm has had this looked at… at prices a small firm can justify" | **partly** |
| q06 | What do you know about Noven? | `about.astro` — "What is Noven?" | **answered** |
| q07 | Is Noven on the Wirral any good, and what do they do? | `about` + FAQ "Why should I trust a company with no case studies?" | **partly** — the "any good" half has nothing behind it, honestly so |
| q08 | Who are the main alternatives to Noven in the UK? | — | **nothing** |
| q09 | Customers are finding people through ChatGPT and we never come up — who do I call? | `index` / `how-it-works` | **answered** |
| q10 | What are my options and roughly what should it cost? | `pricing.astro` — five real numbers | **answered** |

- **Questions with nothing at all behind them:** q03 (Wirral) and q08
  (alternatives). That is the gap list.
- **Plain text an assistant could quote, or a brochure?** Quotable throughout.
  Short declarative sentences, prices as numerals, no PDF-gated content.
- **A page stating what they do, who for, where, what it costs, what happens
  next?** Yes, spread across `index`, `about`, `pricing` and `contact` — but not
  in one place. The "where" is the weak link, per group 2.
- **Answer-page test (~400 words only this business could write):** `faq.astro`
  and `how-it-works.astro` both clear it comfortably. A Wirral page and an
  alternatives page would be the two additions, and both would clear it.

---

## The verdict

**Verdict: C — the Foundation would be wasted until something else is fixed.**

**And the checklist's own description of C does not cover this case, which is a
finding about the checklist.** C is written for broken *sites*: "no website; a
Facebook page standing in for one; a site that cannot accept structured data or
new pages at all." Noven's site is the opposite of all of those — it is static,
crawlable, editable by the owner alone, carries five schema types, publishes its
prices, and passes group 1 outright.

The blocker is not the site. **It is that the name resolves to two other
businesses**, so anything published under it accrues to a name the assistants
already believe belongs to a Miami pharmaceutical company and a North West
builder. Structured data is a machine-readable statement of identity; adding
more of it before the identity is settled is publishing the wrong thing more
loudly, into a layer where caches and third-party copies persist long after the
edit.

That is verdict C by consequence — the spend would not hold — reached by a route
the template doesn't anticipate. **`ops/audit-report-template.md` and
`checklist.md` should both widen C to include identity problems, not only site
problems.** Found by running the audit on ourselves, which is what the self-audit
was for.

This matches the report draft's "If something else has to happen first" branch.
Pre-send check satisfied on that point.

**The three things to fix first**, in order:

1. **Settle the name.** **At least four** businesses answer to "Noven" — a Miami
   pharmaceutical company, a North West builder, an AI workflow product at
   `noven.studio`, and `noven.io`. Until this resolves, every other fix accrues
   to the wrong entity. Not website work — a naming and identity decision.
2. **Get into Bing's index.** Zero results for `site:novenstudio.co.uk`. Copilot
   retrieves from Bing, so Copilot structurally cannot recommend the business —
   which is exactly what the nine hand-run Copilot answers showed. Free to fix,
   about fifteen minutes, and it is the only finding here with a same-day
   remedy.
3. **Put the location in the machine-readable layer.** `areaServed: 'GB'` is the
   only geographic fact a machine can read, while the visible page says Wirral.
   `LocalBusiness` with a real `areaServed`, plus a page that names the towns.
   Pure site work, worth doing under any name — the schema builds from a single
   data file, so it is a small change.

Two things deliberately *not* on this list:

- **Zero citations of `novenstudio.co.uk` across 210 answers** is a symptom, not
  a cause. The site was published days before the audit; it needs time and
  off-site presence, neither of which is a fix anyone can perform this week.
- **The superseded prices in Google's index** are a wrong fact, so they belong
  in the report's "what they believe about you" section, and they were actioned
  the same day they were found.

---

## Checks completed 2026-08-03

All four resolved.

| Check | Result |
|---|---|
| Sitemap returns 200 | **Pass** — valid XML, points to `sitemap-0.xml` |
| Netlify primary domain matches apex | **Pass** — `https://novenstudio.co.uk`, verified in Netlify |
| Anything blocking crawlers | **Pass** — no password, no SSO, no redirect or header rules, no functions or edge functions |
| Bing index | **FAIL — zero results.** See 3.1 |
| *(added)* Google index | Current business, superseded prices. See 3.2 |
| *(added)* Google live test | "URL is available to Google", "Page can be indexed". Re-indexing requested |

## Still outstanding

Group 3's off-site half, minus the two index checks now done: Google Business
Profile, Bing Places, Companies House, professional register, trade directories,
LinkedIn, and review counts. Fifteen minutes, hard stop. **Deliberately
deferred, not skipped — the report must say so.**

**Same-day action available:** register `novenstudio.co.uk` in Bing Webmaster
Tools and submit the sitemap. This is the only finding in the audit with a fix
that can be completed today, and `ops/accounts.md` already has Bing Webmaster
Tools on the "needed but not in place" list.
