# The website checklist

**Status: Decided, unvalidated** — written down, never yet performed.

**Internal working document.** What we look at during an audit, in the order we
look at it. Copy this file into the client's audit folder and fill it in — the
filled copy is the working note the report is written from, and it is never sent
to the client.

Written 2026-07-30 as part of roadmap 3a. Companion to `ops/audit-method.md`.

**Every item below is tagged with how it's actually obtained**, added
2026-08-05 after the Noven self-audit turned out to lean on access that only
exists for our own site (source repo, the Netlify dashboard, Search Console
ownership) — none of which a client audit has. `[script]` means
`ops/site-check/site_check.py` does it from the public URL alone; run that
first and use this checklist to read and extend its output, not to redo it by
hand. `[public]` needs no account, just a browser. `[client access]` needs the
client to grant something, same two-stage pattern as the Foundation. `[read]`
is judgement a person has to make.

**Budget: 20 minutes on the site, 15 minutes off it.** If a section is running
long, record what you found so far, move on, and say in the report that it
needs a closer look. An audit that overruns to be thorough is an audit that
loses money and delays the report we promised inside two working days.

---

## How this is organised, and why

**The four groups below are the Foundation's four promises, in order.** From
`how-it-works.astro`: crawler access, structured machine-readable facts,
consistent facts across the web, and pages that answer customer questions.

That is deliberate. **The audit checklist and the Foundation checklist are the
same list — one diagnoses, the other fixes.** A finding in group 2 is a
Foundation line item in group 2. Nothing found here needs translating into a
scope later, and the client can see the audit and the quote line up, which is
most of why they believe the second one.

It also means roadmap 3b's checklist is largely written by this file. What 3b
still owes is the *how* of doing the work and the access question, not the
*what*.

---

## Before you start

- [ ] Business name, exactly as they write it: ................................
- [ ] Website: ................................................................
- [ ] Town / area served: .....................................................
- [ ] What they want to be found for: .........................................
- [ ] Site platform, if identifiable (WordPress, Wix, Squarespace, Shopify,
      GoDaddy, custom, unknown): ............................................. `[script]`
- [ ] Who actually controls it — the owner, an agency, a franchise/trade-body
      template, or a web person who has since disappeared: ................... `[ask]`

**The platform matters more than it looks** and is worth thirty seconds. It
decides whether the Foundation is an afternoon or a negotiation with somebody
else's web person — and on a few platforms it decides whether the Foundation is
possible at all. See the verdicts at the end.

`ops/site-check/site_check.py` now names the platform from the homepage's own
markup — generator tag, asset CDN, vendor headers — so this field is filled
before the call rather than guessed during it.

### Platform, and what it means for the access ask

**Two different questions, and this checklist used to run them together.**
*The platform sets the technical ceiling — what is possible at all.* *The
relationship sets what is actually available — who will hand over the keys.*
A WordPress site on an agency maintenance contract is the most capable
platform on this list and still a verdict B, because capability is not
access. Ask both.

| Detected | Who usually holds the keys | What to ask for | Usual verdict |
|---|---|---|---|
| **WordPress** (self-hosted) | Owner, or their web person | Admin login; Editor plus a structured-data plugin is often enough | **A** — best case. Full control of head, schema and new pages |
| **Shopify** | Owner | A staff account with theme access | **A** — `theme.liquid` takes the schema, pages are native |
| **Wix** | Owner | Add us under their Roles & Permissions | **A**, *if* their plan allows custom code — **verify on their plan, don't assume** |
| **Squarespace** | Owner | Contributor invite | **A**, same plan caveat — code injection is a paid-tier feature |
| **Weebly / Duda** | Owner, sometimes a reseller | Contributor access | **A** with the same plan caveat; Duda is often resold by an agency, so check who invoices them |
| **Webflow** | Often a designer, not the owner | Publish rights on the project | **A or B** — capable platform, but the seat is frequently held by whoever built it |
| **GoDaddy Website Builder** | Owner | Login, and check what the editor will actually accept | **B, sometimes C.** The restrictive one: limited custom-code and head access. **Establish what can be injected before quoting a Foundation** — this is the platform most likely to make part of the work undeliverable |
| **Developer-built** (Astro/Hugo/Next/Gatsby on Netlify/Vercel/GitHub Pages) | A developer | A deploy path — repo access or a build hook. Not a CMS login; there isn't one | **A if the developer is still around, B if they've gone** — and if they've gone, work the recovery order below before settling on B |
| **Franchise / trade-body template** | The franchisor or trade body | Ask whether local changes survive a master redeploy | **B or C** — `ops/service-tiers.md` §3 already names these: a master redeploy silently wipes our page |
| **unknown** | — | Ask them who built it and who maintains it | Don't guess. "Unknown" from the script means *not detected*, not *bespoke* |

**The plan-tier caveats are deliberately not pinned to a named plan here.**
Vendors rename and re-gate their tiers, and a wrong specific in this file
would be quoted at a client months later. Check what *their* plan allows, on
the day, and record it in the row above.

### When the developer has gone

The common small-business case: the site was built years ago by somebody who
no longer answers. **Do not settle on verdict B until these have been tried,
in this order** — the first two are usually available and solve it outright.

1. **Who owns the domain?** WHOIS and the registrar. **If it is registered in
   the developer's name, that is a bigger emergency than the site** and it
   comes first — everything else is worthless if the domain lapses to
   somebody else. Say so plainly whatever else the audit finds.
2. **Who is billed for the hosting?** **Hosting access is the master key** —
   more useful than developer access, because on a WordPress or similar site
   it hands over the database, the theme and the files together. Most hosts
   have an account-recovery or ownership-dispute process a business can use
   when it is the party actually paying. Start there, not with the developer.
3. **Only then, verdict B**, with what specifically is blocked named in the
   report so the client can decide.

**Do not offer to reconstruct the site from a crawl.** It is a poor idea on
three separate grounds and the reasoning is worth keeping, because it looks
superficially reasonable:

- **You get output, not source.** A mirror captures rendered HTML, CSS and
  images. It cannot capture server-side code, the database or the CMS, so
  what comes back is a static fossil nobody can maintain. On a
  JavaScript-rendered site — the case the readability check flags — the
  mirror comes back close to empty, because it takes the same view the
  crawler gets. **The sites easiest to clone are the ones that needed it
  least.**
- **Copyright very likely is not the client's.** Under UK law the author owns
  copyright by default, and for a freelance developer — not an employee —
  **paying for a website does not transfer it without a written, signed
  assignment**, which small-business web jobs routinely lack. An implied
  licence to *use* the site is often found; it does not obviously extend to
  copying, modifying and redeploying it, which is exactly what a rebuild
  needs. Themes, plugins, stock photography and fonts carry their own
  licences, frequently tied to the purchaser's account, and those do not
  travel with a crawl either. The same applies to pulling it from an archive.
- **It preserves the problems.** A faithful copy faithfully reproduces the
  missing structured data, the unreadable location and the absent answer
  pages — the things the audit exists to find. There is no version of this
  where the clone is the fix.

If access genuinely cannot be recovered, **say so plainly in the report and
stop there.** Name what is wrong, what is missing, and what it would take —
that list does not depend on us being the ones to act on it, and on this
verdict it is the entire value of what they bought, so it has to be specific
enough for a stranger to work from.

**Do not recommend a developer, arrange one, or offer to manage the work.**
We have no stake in who fixes it, and that is the point rather than a
limitation — see `ops/service-tiers.md` §10. If they come back later with a
site we can work on, the Foundation is there at its published price.

---

## Group 1 — Can the assistants get in at all

Everything else is irrelevant if this is wrong, so it goes first.

### 1.1 robots.txt `[script]`

Fetch `{site}/robots.txt`. Record each of the following as **allowed**,
**blocked**, or **not mentioned** (which means allowed by default, and is the
usual answer):

| Crawler | Whose | Result |
|---|---|---|
| `GPTBot` | OpenAI — training and retrieval | |
| `OAI-SearchBot` | OpenAI — ChatGPT search index | |
| `ChatGPT-User` | OpenAI — live fetch when a user asks | |
| `ClaudeBot` / `Claude-SearchBot` | Anthropic | |
| `PerplexityBot` / `Perplexity-User` | Perplexity | |
| `Google-Extended` | Google — Gemini grounding control | |
| `Googlebot` | Google — the index everything else leans on | |
| `Bingbot` | Microsoft — **this is the one Copilot depends on** | |
| `Applebot-Extended` | Apple | |
| `*` (catch-all disallow) | Everyone | |

- [ ] Any blanket `Disallow: /` under `*`? — the single most damaging finding
      available, and it happens by accident constantly (a staging site pushed
      live, a plugin's default, a "privacy" setting somebody ticked). `[script]`
- [ ] Is a sitemap declared in robots.txt? `[script]`
- [ ] Does robots.txt actually exist? A 404 is fine and means everything is
      allowed. Say so plainly in the report rather than listing it as a problem.
      `[script]`

**Crawler names change.** Check the providers' published lists before treating a
missing name as significant.

### 1.2 Is anything else blocking them `[script, approximated externally]`

The self-audit read password walls, redirect rules and CDN presence straight
off the Netlify dashboard — that only exists because it was our own hosting
account. A client audit has no such dashboard, so these are approximated from
the outside instead: what a plain unauthenticated fetch actually meets, which
is arguably the more honest test anyway.

- [ ] Fetch the homepage with a non-browser user agent. A challenge page, a 403,
      or a "checking your browser" interstitial means the crawlers are being
      turned away regardless of what robots.txt says. `[script]`
- [ ] Is the site behind Cloudflare or similar? Cloudflare rolled out AI crawler
      verification with **default-on enforcement across free and pro plans**
      during 2026 — so a site can be blocking assistants its owner never
      intended to block, and the owner will have no idea. Worth checking
      explicitly; it is a finding in its own right and it is free to fix.
      `[script flags signals, read] `
- [ ] Any country blocking, login wall, or age gate in front of ordinary pages?
      `[script flags a login wall via 401/403; country-blocking and age gates
      need a manual look, since a single-location fetch can't see what a
      different country would get — read]`

### 1.3 Can they read it once they're in `[script]`

- [ ] Fetch the homepage and a service page as plain HTML. **Is the visible text
      actually in the source?** If the page arrives as an empty shell that
      JavaScript fills in, some crawlers get nothing. This is the standard
      failure mode of app-style site builders and single-page sites. `[script —
      heuristic word-count check; treat a low count as a prompt to look, not a
      verdict]`
- [ ] HTTP status: 200 on every key page, no redirect chains. `[script, on the
      homepage; other key pages need spot-checking by hand]`
- [ ] One canonical home — www or apex, not both serving separately. `[script]`
- [ ] HTTPS, with a valid certificate. `[script]`
- [ ] Is there a sitemap, does it load, does it list the pages that matter?
      `[script fetches and validates it; whether the listed pages are the ones
      that matter is a read]`
- [ ] Are the key pages reachable from the homepage in two clicks or fewer?
      `[read]`
- [ ] Anything important living only inside a PDF, an image, or a video.
      `[read]`

---

## Group 2 — What is machine-readable

- [ ] Is there any JSON-LD structured data at all? (Most small sites: no.)
      `[script]`
- [ ] If yes, does it parse, and does it validate? `[script parses each block
      and reports errors; full schema.org validation is still worth a pass
      through validator.schema.org by hand]`
- [ ] Which types are present: `Organization` / `LocalBusiness`, `Service`,
      `FAQPage`, `Person`, `Product`, `Review`? `[script]`
- [ ] Does the structured data carry: legal name, trading name, address or area
      served, phone, email, opening hours, services, prices? `[script checks
      whether the keys exist anywhere in the graph; whether the values are
      correct, and match the visible page, is a read]`
- [ ] Does the *visible* site state a **price** anywhere? Record this separately
      even when the answer is no, because it usually is, and because it is the
      highest-value single fix we ever recommend. An assistant asked "roughly
      what should it cost" can only quote a business that published a number.
      `[read — a regex guessing at currency symbols out of context is exactly
      the invented precision CLAUDE.md rules out]`
- [ ] Does the site say plainly **where** they work — named towns, not "we cover
      the North West"? `[read]`
- [ ] One `<h1>` per page, saying what the page is? `[script, on the homepage;
      other pages by hand]`
- [ ] Page titles that describe the page, not "Home | Company Name"? `[script,
      on the homepage; other pages by hand]`
- [ ] Does the site say what it does above the fold, in words, without needing an
      image? `[read]`

**Read the structured data against the visible page.** Structured data that
disagrees with the page it sits on is worse than none — it is a machine-readable
statement of something untrue, and it is exactly the mechanism that produces the
"named wrongly" outcomes in `ops/audit-method.md` section 4.

---

## Group 3 — Are the facts the same everywhere

The off-site half, and in practice the group that produces the most findings on
the most audits. **Fifteen minutes, hard stop.**

Record the business name, address and phone **exactly as written** in each place.
Not "matches" — the actual string. Mismatches are only obvious side by side.

| Source | Name | Address | Phone | Notes |
|---|---|---|---|---|
| Their website | | | | |
| Google Business Profile | | | | Exists? Claimed? Categories right? Hours? |
| Bing Places | | | | **Feeds Copilot** — commonly missing entirely |
| Companies House | | | | If a company: name, registered address, status, filing state |
| Professional register | | | | ICAEW/ACCA, SRA, CQC, GMC/HCPC, Gas Safe, FCA — whichever applies |
| Trade directory 1 | | | | |
| Trade directory 2 | | | | |
| LinkedIn | | | | |
| Facebook | | | | Often the most out-of-date, often the top result |

- [ ] Any **old address or old phone number** still live anywhere? The classic
      finding, and the one clients most often did not know about.
- [ ] Any **defunct or duplicate** listing of the same business?
- [ ] Does the trading name differ from the registered name, and is the
      relationship stated anywhere a machine could read it?
- [ ] Google reviews: how many, how recent? Assistants quote review volume, and a
      business with four reviews will lose to one with ninety regardless of what
      we do — worth saying honestly rather than implying we can fix it.
- [ ] Is the business in **Bing's index** at all? Default check: a public
      `site:{domain}` search on Bing — no account needed, two minutes.
      **Wardith's own Bing Webmaster Tools account (`ops/accounts.md`) is for
      `wardith.co.uk`, not the client's domain** — it cannot check a client's
      site unless the client separately adds us to their own Webmaster Tools
      property, which is an optional upgrade, not the default route. `[public,
      upgradeable to client access]`. If not indexed, Copilot structurally
      cannot recommend them, and that outranks every other Copilot finding.
- [ ] Is the business in **Google's index**, and what does Google's cached
      description say? Default check: a public `site:{domain}` search on
      Google — catches stale cached facts the same way it caught our own
      superseded prices. The definitive "can this page be indexed" answer
      needs Search Console's URL Inspection, which needs verified ownership
      of the client's domain — again an optional client-granted upgrade, not
      a baseline requirement. `[public, upgradeable to client access]`

---

## Group 4 — Does anything on the site answer the question

The bridge between the two halves of the audit, and the part that becomes the
Grow plan's backlog if they ever take one.

For each of the ten questions, is there a page on their site that genuinely
answers it?

| # | Question | Page that answers it | Verdict |
|---|---|---|---|
| q01 | | | answered / partly / nothing |
| q02 | | | |
| ... | | | |

- [ ] Which questions have **nothing at all** behind them? That list is the
      report's gap list, and later it is the Grow backlog.
- [ ] Where a page exists, does it answer in plain text an assistant could quote,
      or does the answer require reading a brochure?
- [ ] Is there a page that states, in words: what they do, who for, where, what
      it costs, and what happens next?

**Apply the answer-page test from `ops/service-tiers.md` section 3 as you go:**
if there is not around 400 words of genuinely specific content that only this
business could write, the gap is an FAQ line and not an answer page. Marking that
here saves an argument later about what a Grow month is buying.

---

## The verdict

Every audit ends with exactly one of three. This is roadmap 3b's honesty
requirement, and it has to be decided here, in the audit, not discovered halfway
through a Foundation.

**A. The Foundation will work.** Normal case. Their site is editable, readable,
and the findings are fixable.

**B. The Foundation will work, but it needs someone else's hands.** Their site is
managed by an agency, a franchise template, a trade-body package, or a web person
who holds the keys. The work is the same; the access is the obstacle. Say so in
the report, name what access is needed, and let them decide before they spend
£800. `ops/service-tiers.md` section 3 already decided that access is asked for
in two stages — this is the first stage, and this is where it gets flagged.

**C. The Foundation would be wasted until something else is fixed.** No website;
a Facebook page standing in for one; a site that cannot accept structured data or
new pages at all; a site so broken that fixing what it says is beside the point.
**Say so plainly, recommend what to do instead, and do not sell the Foundation.**
The site promises this outcome in four places. It is also the case the refund
line in the terms exists for — if we took £250 and this is the answer, the report
still gets written and delivered, because it is the report they paid for and it
is the one that saves them money.

**Verdict:** ......................................................

**The three things to fix first**, in order, with the reason each one matters:

1. ..........................................................................
2. ..........................................................................
3. ..........................................................................

Three, not ten. A list of ten findings gets nothing done and reads like
groundwork for a bill.
