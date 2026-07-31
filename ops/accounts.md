# Accounts, dependencies and renewals

**Internal document.** Every outside thing this business depends on, what it
costs, when it renews, and what breaks if it lapses. Written 2026-07-31.

**No credentials go in this file, ever.** It is committed to a public
repository. This is the map, not the keys. Passwords and 2FA recovery codes
belong in the vault (see the bottom of this file), and the vault is the thing
that has to exist for any of this to be recoverable by anyone but the owner.

**`[PLACEHOLDER]` means the repo does not record it and nobody has looked it
up.** Those are not gaps in this document — they are gaps in the business, and
the domain row is the one that matters most.

---

## The register

| Dependency | What it's for | Cost | Renews | What breaks if it lapses |
|---|---|---|---|---|
| **`novenstudio.co.uk`** | Everything: the site, all canonicals, the sitemap, MX for mail, the `url` in the structured data, both LinkedIn links | [PLACEHOLDER] | **[PLACEHOLDER — registrar not recorded, expiry not recorded, auto-renew status not recorded]** | Total outage. Site dark, all mail dead, structured data broken, Search Console property invalid. `.co.uk` recovery after expiry is time-boxed and can fail outright |
| **Namecheap** | DNS: Netlify records, Zoho MX, SPF, DKIM, DMARC, two verification TXTs | [PLACEHOLDER] | [PLACEHOLDER] | Site and mail, together |
| **Netlify** | Hosting, build, TLS. Deploys `main` | Free tier | rolling | Site offline. No documented alternative host, no rollback runbook |
| **GitHub `hellonovenuk-lang`** | This repo — the source of truth and the deploy trigger | Free tier | n/a | Deploys stop; the only copy of every operating decision is at risk |
| **GitHub `hellonovenuk-lang/Noven`** | Second repo, holds brand and image originals | Free tier | n/a | Asset originals. Recorded in one line of the session log and nowhere else until now |
| **Zoho Mail Lite** | `hello@novenstudio.co.uk` — the only inbound channel on a site with no phone and no form | £14.40/yr inc VAT | ~29 Jul 2027 *(inferred from purchase date, not recorded)* | No enquiry reaches the business |
| **Zoho Books** | Invoicing and revenue records | [PLACEHOLDER] | [PLACEHOLDER] | Invoicing, and the Foundation/monthly billing route |
| **Gmail `hello.noven.uk@gmail.com`** | **An identity, not a mailbox.** Owns the GitHub login, the Search Console property and Netlify's notifications. Forwards to Zoho | Free | Forwarding reviewed ~Jul 2027 | See "the concentrated account" below |
| **Revolut Pro** | Business bank account; the audit payment link; Foundation and monthly transfers | Free to hold. Card fees 1.0% + £0.20 personal, 2.8% + £0.20 commercial | n/a | No way to be paid. FSCS cover is capped at £120,000 **shared** with the personal balance, not doubled |
| **ICO registration `C1995412`** | Legal requirement to process personal data | £47/yr, Direct Debit | ~30 Jul 2027 *(inferred from "renews annually")* | Penalty of up to **£4,000** against a £47 fee |
| **Google Search Console** | Sitemap, indexation, removals | Free | n/a | The only indexation diagnostic |
| **LinkedIn** | Founder profile and company page, both published in the structured data as `sameAs` | Free | n/a | Published `sameAs` points at a dead URL, breaking the site's own consistency claim |

### Ordered, decided or needed but not yet in place

| Dependency | Status |
|---|---|
| **Address for service** | V LOT paid ~29 Jul 2026, nothing delivered. Order reference, amount and payment method **all unrecorded** — which is what a chargeback would need. Fallback decided (1st Formations / Quality Company Formations, ~£115/yr) and not yet ordered |
| **Professional indemnity insurance** | Not bought. Should precede the first Foundation, which is where a live client site gets changed. Absent from `ROADMAP.md` entirely; researched in `ops/third-party-services.md` |
| **API accounts** — OpenAI, Google AI Studio, Perplexity | Not opened. Needed before any audit can run. Spend cap on each **before** the first call; keys never in this repo. `ops/audit-setup.md` |
| **Bing Webmaster Tools** | Not done. Copilot's real diagnostic is Bing indexation, so the audit is weaker without it |
| **Password vault** | Recommended as step one of nine and there is no evidence it exists. See below |
| **Client data storage** | Undecided. `ops/client-record.md` |

---

## The two structural risks

**The concentrated account.** `hello.noven.uk@gmail.com` is a free consumer
account that owns the GitHub login, the Search Console property and Netlify's
notifications. Losing it costs the deploy pipeline, the source of truth and the
indexation tooling in a single event, and appeals on free Google accounts are
slow. It was correctly reclassified in the session log on 29 July from "an
address" to "an identity" — and nothing was hardened afterwards. It needs
app-based 2FA, printed recovery codes and a recovery address that isn't itself.

**Zoho's account recovery currently points at the mailbox it protects.** A
lockout would be unrecoverable. The fix is five minutes — add the personal
iCloud address as an alternate under Zoho Accounts → My Profile → Email
Addresses — and it has been owed since 29 July.

---

## The dates, in one place

Every dated obligation in this business currently lives in a markdown tick box
inside a git repository. Three documents say "put the reminder in the calendar"
and nothing records that any reminder was ever set. **This table is not a
reminder. Put these in an actual calendar.**

| When | What | If missed |
|---|---|---|
| **~10 Aug 2026** | ICO publishes the registered address on a bulk-downloadable public register | The owner's home address published permanently. Copies survive any later amendment |
| ~29 Jul 2027 | Zoho Mail Lite renewal | The only contact channel dies |
| ~30 Jul 2027 | ICO annual renewal | Up to £4,000 |
| [PLACEHOLDER] | Domain renewal | Total outage |
| By 5 Oct 2027 | HMRC Self Assessment registration, if trading began in 2026/27 | Failure-to-notify penalties |
| Event-driven | VAT threshold crossed | Every page says "not VAT registered, so the prices shown are the prices you pay" — published, crawled and cached |
| Annually, once bought | Insurance renewal | Uninsured while touching client sites |

**Two notes on how to check these.** The ICO fee is collected by Direct Debit,
so it renews itself — the real failure mode is a *silent DD failure* after a bank
or card change, which a calendar reminder does not catch. The check is "did it
collect", not "did a reminder fire". And most of these cluster in late July,
which is useful: one renewals week in the last week of July covers nearly the
whole year.

---

## The vault, and why it is the whole answer to bus factor

A successor holding only this repo could rebuild the site, run an audit to the
documented method, and re-derive why every decision was made. They could not
deploy, change DNS, read or send mail, take a payment, or amend the ICO record —
which needs a security number that exists only in the owner's inbox. **They
could keep the product alive and not the business, for a single day.**

Three things fix that, and together they are an afternoon:

1. **A vault that exists** (Bitwarden was the decision) holding every account
   above, with 2FA recovery codes.
2. **An emergency-access grantee on it.** Bitwarden supports this natively and it
   is the entire answer to bus factor for a sole trader.
3. **A named human** who knows the business exists and holds that access.

Keep this file as the index to the vault: the vault says how to get in, this file
says what is in there and what it costs.
