# Accounts, dependencies and renewals

**Status: Live.** **Internal document.** Every outside thing this business depends on, what it
costs, when it renews, and what breaks if it lapses. This is the map, not the
keys — **no credentials go in this file, ever**; it is committed to a public
repository. Passwords and 2FA recovery codes belong in the vault (bottom of
this file).

**`[PLACEHOLDER]` means nobody has looked it up.** These are gaps in the
business, not just in this document.

---

## The register

| Dependency | Purpose | Cost | Renews | Next action / consequence |
|---|---|---|---|---|
| **`wardith.co.uk`** | The live, published address | `[PLACEHOLDER: total paid]` | **~4 Aug 2027**, GoDaddy, one year only. `[PLACEHOLDER: auto-renew status]` | **Extend to 5+ years — in the calendar for 6 Oct 2026, backstop 4 Jun 2027.** Miss it and `.co.uk` recovery after expiry can fail outright |
| **`wardith.com` / `wardith.uk`** | Owned, redirecting. Never published as a contact detail | `[PLACEHOLDER]` | Same domain project as above | Keep redirecting; no separate action |
| **`novenstudio.co.uk`** | Pre-rename domain. Still carries MX for mail and both LinkedIn links until the rename fully lands | `[PLACEHOLDER]` | `[PLACEHOLDER — registrar, expiry and auto-renew all unrecorded. Urgent]` | **Record registrar, expiry and auto-renew status. Keep registered at least three years — do not drop it**, or every redirect dies and the name becomes free for a competitor in the same field to buy |
| **Namecheap** | DNS: Netlify records, Zoho MX, SPF/DKIM/DMARC, verification TXTs | `[PLACEHOLDER]` | `[PLACEHOLDER]` | Site and mail both depend on this; record cost and renewal |
| **Netlify** | Hosting, build, TLS. Deploys `main`. Also the order form once switched on (Netlify Forms, free to 100 submissions/month) | Free tier | Rolling | No documented alternative host or rollback runbook if it goes down |
| **GitHub `hellonovenuk-lang`** | This repo — source of truth and deploy trigger | Free | n/a | Deploys stop if lost |
| **GitHub `hellonovenuk-lang/Noven`** | Second repo, holds brand and image originals | Free | n/a | Only record of this repo's existence is this row |
| **Zoho Mail Lite** | `hello@wardith.co.uk` (published inbound channel). `hello@novenstudio.co.uk` stays as a free alias — it's in the ICO record and both LinkedIn pages — **must keep receiving for at least 12 months.** Never add a second user (aliases are free, users are £1/month) | £14.40/yr inc VAT | ~29 Jul 2027 *(inferred from purchase date)* | No enquiry reaches the business if this lapses |
| **Zoho Books** | Invoicing and revenue records | `[PLACEHOLDER]` | `[PLACEHOLDER]` | Invoicing and the Foundation/monthly billing route depend on it |
| **Gmail `hello.noven.uk@gmail.com`** | An identity, not a mailbox — owns the GitHub login, Search Console property and Netlify notifications. Forwards to Zoho | Free | Forwarding reviewed ~Jul 2027 | See "the concentrated account" below |
| **Canva** | The only editable master for brand assets — SVGs in `assets/brand/` are outlined paths, so this is the only place the wordmark can be changed as type rather than redrawn. SVG export needs the Pro plan | `[PLACEHOLDER: plan and price]` | `[PLACEHOLDER: billing date]` | Lapsing makes the brand uneditable without redrawing (`CLAUDE.md` bans that), and silently downgrades export to PNG |
| **Revolut Pro** | Business account; audit payment link; Foundation and monthly transfers | Free to hold. Card fees 1.0%+£0.20 personal, 2.8%+£0.20 commercial | n/a | FSCS cover capped at £120,000, shared with the personal balance |
| **UK Postbox** | Address for service of documents: site footer, `PostalAddress` structured data, ICO registered address, "Wardith" trading-name registration. **Two addresses issued, not interchangeable — see below** | £12/month inc VAT (£10 exc). PAYG scans £1.20 each. `[PLACEHOLDER: setup fee]` | Monthly, rolling. `[PLACEHOLDER: billing date]` | A failed card payment silently breaks a published legal disclosure. Inactive accounts: mail returned after 1 month, purged at 6. Must migrate off ICO/HMRC/the site *before* dropping this |
| **ICO registration `C1995412`** | Legal requirement to process personal data. Registered at Lytchett House, trading name Wardith | £47/yr, Direct Debit | ~30 Jul 2027 *(inferred)* | Penalty up to **£4,000** against a £47 fee |
| **Google Search Console** | Sitemap, indexation, removals. Two properties: `wardith.co.uk` (Domain, verified) and `novenstudio.co.uk`, Change of Address running between them to ~Feb 2027 — **keep the old property**, it holds the before/after the six-month re-check needs | Free | n/a | Only indexation diagnostic available |
| **LinkedIn** | Founder profile and company page, both in structured data as `sameAs` | Free | n/a | A dead page here breaks the site's own published consistency claim |
| **Bing Webmaster Tools** | `wardith.co.uk` submitted, all pages indexing-requested. Feeds Copilot, which answers out of Bing's index. `novenstudio.co.uk` deliberately not added — it only 301s away now | Free | n/a | Copilot's only direct route to the site; no fallback if lost |

**The two UK Postbox addresses.** Different postcodes, different purposes —
using the wrong one fails silently (parcel never arrives, or a letter goes to
a loading bay).

| | Address | For |
|---|---|---|
| **Mailbox** | Kieran Smith / Wardith, Lytchett House, 13 Freeland Park, Wareham Road, Poole, Dorset, **BH16 6FA** | Letters and small packets. **The published address for service** — footer, structured data, ICO record, terms, official forms |
| **Courier point** | Kieran Smith / Wardith, Unit 171036, Courier Point, 13 Freeland Park, Wareham Road, Poole, Dorset, **BH16 6FH** | Parcels only. A carrier delivery instruction, not a legal address. Give to suppliers; never publish |

Both name lines must read "Kieran Smith / Wardith" — the trading name is
registered with UK Postbox and mail addressed to a name they hold no record of
is commonly returned.

### Ordered, decided or needed but not yet in place

| Dependency | Status | Next action |
|---|---|---|
| **V LOT refund** | V LOT took payment ~29 July, delivered nothing, refund requested 2026-08-07 | Order reference, amount and payment method are still unrecorded — get them (a chargeback needs them if the refund is refused), or write the loss off deliberately |
| **Professional indemnity insurance** | Not bought | Should precede the first Foundation — that's where a live client site gets changed |
| **API accounts** — OpenAI, Google AI Studio, Perplexity | In use for audits and trade runs. Balances at 2026-08-09: OpenAI $16.00, Gemini £8.95, Perplexity $4.49 | Record actual per-provider cost after every run rather than estimating. Confirm Perplexity's auto top-up is off and spending caps are set on all three |
| **Password vault** | Recommended, no evidence it exists | Set one up (Bitwarden was the decision) — see "the vault" below |
| **Client data storage** | **Decided 2026-08-10: local, encrypted storage on the owner's own machine.** No processor, so no contract needed and no supplier country to publish | Two conditions before any client or prospect record may exist anywhere, including the outreach list: full-disk encryption on and verified (recovery key held off the disk), and an encrypted external backup drive, kept off-site, restored at least once (~£30–60). Turn OneDrive folder backup off first — it syncs Desktop/Documents to the consumer Microsoft account by default |

---

## Two structural risks

**The concentrated account.** `hello.noven.uk@gmail.com` is a free consumer
account that owns the GitHub login, the Search Console property and Netlify's
notifications. Losing it costs the deploy pipeline, the source of truth and
the indexation tooling at once, and free-account appeals are slow. **Needs
app-based 2FA, printed recovery codes, and a recovery address that isn't
itself.**

**Zoho's account recovery currently points at the mailbox it protects** — a
lockout would be unrecoverable. Fix: add the personal iCloud address as an
alternate under Zoho Accounts → My Profile → Email Addresses.

---

## The dates, in one place

**Put these in an actual calendar, not just this table.** The Wardith domain
rows are already in the owner's Google Calendar (popup a day ahead, email a
week ahead) — the rest are not.

| When | What | If missed |
|---|---|---|
| **26 Aug 2026** | Spending freeze lifts — top up API balances | Outreach and audit runs stay blocked |
| **1 Sept 2026** | Operational, accepting clients, outreach active | Owner's deadline |
| **6 Oct 2026** *(in the calendar)* | Extend the three Wardith domains to 5+ years; decide whether to consolidate the registrar | Left on a one-year term at GoDaddy's renewal rate, across two registrars |
| **4 Jun 2027** *(in the calendar)* | Backstop: Wardith domains expire in ~2 months | See domain row above |
| ~29 Jul 2027 | Zoho Mail Lite renewal | The only contact channel dies |
| ~30 Jul 2027 | ICO annual renewal | Up to £4,000 |
| **~4 Aug 2027** | Wardith domain expiry (`.co.uk`, `.com`, `.uk`) | Total outage: site dark, mail dead, structured data broken |
| `[PLACEHOLDER]` | `novenstudio.co.uk` renewal — date unknown, and it now carries every redirect | Total outage before the rename; every old link and cached answer dead after it |
| By 5 Oct 2027 | HMRC Self Assessment registration, if trading began in 2026/27 | Failure-to-notify penalties |
| Event-driven | VAT threshold crossed | Every page says "not VAT registered" — published, crawled and cached, so crossing it is a copy change across the whole site |
| Annually, once bought | Insurance renewal | Uninsured while touching client sites |

**How to check these, not just when.** The ICO fee collects by Direct Debit —
the real failure mode is a silent DD failure after a bank or card change, so
check *that it collected*, not that a reminder fired. Most renewals cluster in
late July, so one check in the last week of July covers nearly the whole year.

---

## The vault, and why it is the whole answer to bus factor

A successor holding only this repo could rebuild the site and run an audit to
the documented method, but could not deploy, change DNS, read or send mail,
take a payment, or amend the ICO record.

Three things fix that:

1. **A vault that exists** (Bitwarden was the decision), holding every account
   above with 2FA recovery codes.
2. **An emergency-access grantee on it** — Bitwarden supports this natively.
3. **A named human** who knows the business exists and holds that access.

Keep this file as the index to the vault: the vault says how to get in, this
file says what is in there and what it costs.
