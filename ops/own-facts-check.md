# Our own facts — everywhere they are published, and whether they agree

**Internal document.** The register of every place Noven's own business facts
appear, what each one must say, and what it currently says. Written 2026-08-01,
prompted by the owner noticing that assistants still describe Noven's services
at the old prices.

This is the audit's third promise — *your facts agree with each other everywhere
they appear* — applied to us. `ops/audit-site-checklist.md` group 3 is the client
version of the same check. Run this one on ourselves whenever a published fact
changes, and as step zero of run day.

---

## 1. The two problems, which need different answers

Worth separating before doing anything, because only one of them is fixable by
us and confusing them wastes an afternoon.

**Problem one: sources that are still publishing the old facts.** Every one is a
page somebody controls, and correcting it is an edit. That is section 3, and it
is the actionable half.

**Problem two: assistants that already read the old facts and repeat them from
memory.** Not directly fixable. An assistant updates when it re-reads a source,
and there is no button. Correcting problem one is the only lever there is, and
the lag afterwards is real — which is *why* the site says nothing about how fast
this works, and why `audit-method.md` section 4's second honesty note exists.

**This is not a setback. It is the product's own case, happening to us.**
An assistant confidently quoting a price we abandoned on 31 July is exactly the
`named_wrong` outcome that `audit-method.md` section 4 calls the most persuasive
finding an audit can produce. Capture it in the self-audit rather than tidying it
away first — see section 5.

---

## 2. What the facts currently are

The source of truth is `site/src/data/business.ts`. Nothing below is a second
copy to maintain; it is here so a check can be run without reading TypeScript.

**Corrected 2026-08-06, and the way it broke is worth keeping.** The Email row
read `hello@wardith.co.uk`, and so did `ROADMAP.md`, `HANDOVER.md`,
`ops/accounts.md`, `ops/third-party-services.md`, `ops/README.md` and the
LinkedIn copy in `ops/linkedin.md` — a block of text meant to be pasted into a
public About section. **None of it was true.** The C10 sweep in
`ops/rename-to-wardith.md` replaced the old domain with the new one across the
operating documents, which was right for every sentence describing *the site*
and wrong for every sentence describing *the mailbox* — because the mailbox did
not change. A true statement about an address that works was rewritten into a
false statement about an address that does not exist.

**This register is the thing that is supposed to catch that**, and it did not,
because it was swept too. Two rules out of it: a find-and-replace across the
operating documents needs the mailbox rows read by hand afterwards, and **the
Email row is checked against `business.ts` and against a real test message, not
against the other documents** — six files agreeing with each other is not
evidence when one edit changed all six.

| Fact | Value as at 2026-08-05 | Changed on |
|---|---|---|
| Audit | £250 one-off | 2026-08-05 (was £125; £30 before 2026-07-31) |
| Foundation | £800 one-off, fixed four-part scope | 2026-08-05 (was £750; £350 and unbounded before 2026-07-31) |
| Maintain | £150/month, 10 questions | 2026-08-05 (was £95; £75 before 2026-07-31) |
| Grow | £400/month, 15 questions | 2026-08-05 (was £250; £125 and 25 questions before 2026-07-31) |
| Lead | £700/month, 25 questions, monthly | 2026-08-05 (was £495; £250, 50 questions and fortnightly before 2026-07-31) |
| Turnaround | Report within two working days of scope and payment confirmed | 2026-07-31 (was one working day) |
| Cancellation | No minimum term, no notice period | unchanged |
| Bundling | Never. Every service is priced and bought on its own | 2026-07-31, standing decision |
| Assistants covered | ChatGPT, Google, Copilot, Perplexity | unchanged |
| Location | Wirral, UK — city level, never a street | unchanged |
| Email | hello@novenstudio.co.uk — the address the site publishes and the only one that receives. `hello@wardith.co.uk` **does not exist yet** | corrected 2026-08-06; see the note above |
| Legal status | Trading name of Kieran Smith, a sole trader. Not VAT registered | unchanged |

---

## 3. The register

**"Verified" below means verified from the session that wrote this.** The
network policy blocked all outbound HTTP — `novenstudio.co.uk` and LinkedIn both
returned 403 through the proxy — which is the same limitation recorded in
`audit-setup.md`. So the site and LinkedIn rows are reasoned from the repo, not
read off the live page, and both need the owner's eyes.

| # | Surface | Controlled by | Carries prices? | State | Action |
|---|---|---|---|---|---|
| 1 | The **nine** site pages | Repo → Netlify | Yes | **Verified 2026-08-06 against the built output of the live commit.** `main` is at `d35557a`, deployed to production and `ready` per the Netlify API, and the `dist` for that commit carries 250 / 800 / 150 / 400 / 700, every canonical on `wardith.co.uk`, no `[PLACEHOLDER]` anywhere, and the homepage's visible code block byte-for-byte identical to its head JSON-LD | Owner: eyeball the live pricing page once. The build is verified; that the browser sees the same bytes is the one link in the chain this repo cannot check itself |
| 2 | Site JSON-LD (Organization, Service, FAQPage) | Same file, same build | Yes — `offerSchema()` | **Correct.** The built `Offer` prices were read out of `dist` and are the five above | Covered by 1 |
| 3 | **LinkedIn company page — About** | Owner, in LinkedIn | Yes | **Fixed 2026-08-06.** Rewritten by the owner: no Noven, and the prices match the site | Re-check at the next sweep, not before |
| 4 | **LinkedIn founder profile — About** | Owner, in LinkedIn | Yes | **Fixed 2026-08-06**, same pass | Re-check at the next sweep |
| 5 | LinkedIn tagline and role description | Owner | No prices | Believed fine — no numbers in either | Check while in there |
| 6 | This repo | Owner + sessions | Yes, in the ops docs | Was carrying old prices in seven files until 2026-08-01; corrected | Done |
| 7 | Google Search Console | Owner | Indirect | **`wardith.co.uk` Domain property added and verified 2026-08-06**, via GoDaddy Domain Connect rather than a hand-typed TXT. Sitemap, live-URL test, indexing requests and Change of Address still to run. **The `novenstudio.co.uk` property is kept permanently** — Change of Address runs *from* it, and it holds half the six-month measurement | `ops/search-console-and-bing.md` part 1, from §1.3 |
| 8 | Bing Webmaster Tools | Owner | Indirect | **Not set up**, and now the more urgent of the two: a brand-new domain with no history, and Copilot answers from Bing's index | `ops/search-console-and-bing.md` part 2. Nothing to migrate — Bing never indexed the old domain either |
| 9 | ICO public register entry | ICO | No | Name and **home address**, publishing ~10 Aug 2026 | Separate and more urgent — `HANDOVER.md` section 4 |
| 10 | Email signature on `hello@` | Owner, in Zoho | `[PLACEHOLDER: not recorded anywhere in this repo — does it quote a price?]` | Unknown | Owner to check |
| 11 | Directory or listing entries | Owner | Unknown | `[PLACEHOLDER: no record of any having been created]` | Owner to confirm none exist |
| 12 | Old site content at `novenstudio.co.uk` | Replaced | Yes, a different business's | Replaced before launch; caches may persist. **Gap found 2026-08-06: nobody has ever run `site:novenstudio.co.uk` on Google.** Bing was checked in the self-audit and returns zero; the Google side was never measured. The "sitemap submitted and confirmed, six pages" line elsewhere in the repo is the sitemap being *processed*, not six pages being *indexed* — a softer fact than it reads | **Measured 2026-08-06: 4 results.** So Google did index the old domain, and Change of Address is worth running — four pages describing a business called Noven are a live source for the answer the rename was meant to stop. **4 is now the decay baseline**: re-run the query at the six-month check and record what is left |
| 13 | **The site's `sameAs` claim** — Organization JSON-LD on all nine pages says this business and `linkedin.com/company/wardith/` are the same thing | Repo → Netlify, but its *truth* depends on row 3 | No | **Correct, and checked 2026-08-06.** The slug is right, the URL carries no tracking or view-mode parameters, and the owner confirmed the page loads in a private window — so a crawler is not shown a login wall. The claim is true in both directions | Nothing. Re-check only if the page is renamed again |
| 14 | ~~Two stale Netlify projects~~ | Owner, in Netlify | — | **CLOSED 2026-08-06. Both deleted by the owner**, confirmed against the Netlify API: one project remains on the team, `kaleidoscopic-cuchufli-ff7b1a`, serving `wardith.co.uk`. `noven-2-0-preview` was a full Noven-branded copy of the business, public with no password, raised as D0.1a on 2026-08-04; `aesthetic-unicorn-619923` was in no operating document at all and was found by listing the team. Done **before** the domain was submitted for indexing, which was the point | Nothing. Keep the habit: list the team when sweeping this register, because a project nobody documented is a surface nobody checks |

**Rows 3 and 4 are the whole of the actionable problem.** Two paste operations,
about ten minutes, and they are the only surfaces we control that are currently
publishing a price the site contradicts. They also carry disproportionate weight
for their size: LinkedIn is heavily crawled, it is what a stranger checks after
an email, and both pages are named in our own structured data as `sameAs` — we
have formally told the assistants that those pages describe this business.

---

## 4. A correction: this repo is private, not public

**Verified 2026-08-01 against the GitHub API:** `visibility: private`. Five
places in this repo asserted the opposite, and several rules were justified by
it. All five now say what is true.

**Every rule that was justified by "it's public" stands unchanged**, and the
wording was corrected to *written as though it were public* rather than
relaxed. Three reasons, in order of weight:

1. **Visibility is one click, and the click is not reversible for anything
   already committed.** A repo that goes public exposes its whole history, not
   its current state. A key committed today and removed tomorrow is still in the
   history the day the switch is flipped.
2. **The reasons for keeping client data out are not about GitHub.** Audit
   records contain personal data under UK GDPR; the obligation is the ICO
   registration, not the repo setting, and it does not care who can read it.
3. **It costs nothing.** No decision in this repo would have gone differently
   under the true fact.

**One thing does change:** this repo is **not** a source the assistants read, so
it was never part of the stale-information problem the owner noticed. Correcting
it was housekeeping. Rows 3 and 4 above are the actual cause.

---

## 5. How this interacts with the self-audit

**Do not fix rows 3 and 4 before the self-audit run — do them straight after.**

The self-audit is a dated baseline (`audit-method.md` section 8). Its q06 and
q07 ask what the assistants know about Noven. If the answer today includes a
price we no longer charge, that is a real, dated, quotable finding about how
long stale facts persist and what they cost — measured on ourselves, at no risk
to anyone. Fixing LinkedIn the morning before the run destroys the measurement
and gains about six hours.

Then fix them the same day, and re-run q06 and q07 alone at the six-month
re-check. That gives us a before-and-after on one specific correction, which is
worth more as evidence than anything we could say in a sales page — and it is
the same claim the Foundation makes, tested on the only business we are allowed
to experiment on.

---

## 6. When to run this check

- **Whenever a published fact changes.** The repricing changed five prices, two
  question counts, a cadence and the turnaround, and updated one surface. That
  is the failure this document exists to prevent, and it is a ten-minute check,
  not a project.
- **Step zero of every audit run day**, before the questions go out.
- **At the quarterly review**, alongside the renewals sweep in
  `HANDOVER.md` section 8.

The rule that would have caught it is already written, in `ops/linkedin.md`:
*if a price changes, it changes in both places or neither.* It was written down
and not followed, which is the ordinary way this goes wrong. Hence a register
rather than a resolution.
