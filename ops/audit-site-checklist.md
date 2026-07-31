# The website checklist

**Internal working document.** What we look at during an audit, in the order we
look at it. Copy this file into the client's audit folder and fill it in — the
filled copy is the working note the report is written from, and it is never sent
to the client.

Written 2026-07-30 as part of roadmap 3a. Companion to `ops/audit-method.md`.

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
      GoDaddy, custom, unknown): .............................................

**The platform matters more than it looks** and is worth thirty seconds. It
decides whether the Foundation is an afternoon or a negotiation with somebody
else's web person — and on a few platforms it decides whether the Foundation is
possible at all. See the verdicts at the end.

---

## Group 1 — Can the assistants get in at all

Everything else is irrelevant if this is wrong, so it goes first.

### 1.1 robots.txt

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
      live, a plugin's default, a "privacy" setting somebody ticked).
- [ ] Is a sitemap declared in robots.txt?
- [ ] Does robots.txt actually exist? A 404 is fine and means everything is
      allowed. Say so plainly in the report rather than listing it as a problem.

**Crawler names change.** Check the providers' published lists before treating a
missing name as significant.

### 1.2 Is anything else blocking them

- [ ] Fetch the homepage with a non-browser user agent. A challenge page, a 403,
      or a "checking your browser" interstitial means the crawlers are being
      turned away regardless of what robots.txt says.
- [ ] Is the site behind Cloudflare or similar? Cloudflare rolled out AI crawler
      verification with **default-on enforcement across free and pro plans**
      during 2026 — so a site can be blocking assistants its owner never
      intended to block, and the owner will have no idea. Worth checking
      explicitly; it is a finding in its own right and it is free to fix.
- [ ] Any country blocking, login wall, or age gate in front of ordinary pages?

### 1.3 Can they read it once they're in

- [ ] Fetch the homepage and a service page as plain HTML. **Is the visible text
      actually in the source?** If the page arrives as an empty shell that
      JavaScript fills in, some crawlers get nothing. This is the standard
      failure mode of app-style site builders and single-page sites.
- [ ] HTTP status: 200 on every key page, no redirect chains.
- [ ] One canonical home — www or apex, not both serving separately.
- [ ] HTTPS, with a valid certificate.
- [ ] Is there a sitemap, does it load, does it list the pages that matter?
- [ ] Are the key pages reachable from the homepage in two clicks or fewer?
- [ ] Anything important living only inside a PDF, an image, or a video.

---

## Group 2 — What is machine-readable

- [ ] Is there any JSON-LD structured data at all? (Most small sites: no.)
- [ ] If yes, does it parse, and does it validate?
- [ ] Which types are present: `Organization` / `LocalBusiness`, `Service`,
      `FAQPage`, `Person`, `Product`, `Review`?
- [ ] Does the structured data carry: legal name, trading name, address or area
      served, phone, email, opening hours, services, prices?
- [ ] Does the *visible* site state a **price** anywhere? Record this separately
      even when the answer is no, because it usually is, and because it is the
      highest-value single fix we ever recommend. An assistant asked "roughly
      what should it cost" can only quote a business that published a number.
- [ ] Does the site say plainly **where** they work — named towns, not "we cover
      the North West"?
- [ ] One `<h1>` per page, saying what the page is?
- [ ] Page titles that describe the page, not "Home | Company Name"?
- [ ] Does the site say what it does above the fold, in words, without needing an
      image?

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
- [ ] Is the business in **Bing's index** at all? (Site search on Bing, or Bing
      Webmaster Tools with permission.) If not, Copilot structurally cannot
      recommend them, and that outranks every other Copilot finding.

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
£750. `ops/service-tiers.md` section 3 already decided that access is asked for
in two stages — this is the first stage, and this is where it gets flagged.

**C. The Foundation would be wasted until something else is fixed.** No website;
a Facebook page standing in for one; a site that cannot accept structured data or
new pages at all; a site so broken that fixing what it says is beside the point.
**Say so plainly, recommend what to do instead, and do not sell the Foundation.**
The site promises this outcome in four places. It is also the case the refund
line in the terms exists for — if we took £125 and this is the answer, the report
still gets written and delivered, because it is the report they paid for and it
is the one that saves them money.

**Verdict:** ......................................................

**The three things to fix first**, in order, with the reason each one matters:

1. ..........................................................................
2. ..........................................................................
3. ..........................................................................

Three, not ten. A list of ten findings gets nothing done and reads like
groundwork for a bill.
