# Accounts, dependencies and renewals

**Status: Live** — with real gaps marked `[PLACEHOLDER]`.

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
| **`wardith.co.uk`, `wardith.com`, `wardith.uk`** | The business's name from 2026-08-04. **`wardith.co.uk` is the live address** — decided 2026-08-04. The other two are owned and redirecting, and are never published as a contact detail | `[PLACEHOLDER: total paid not recorded]` | **~4 Aug 2027. GoDaddy, bought 2026-08-04, ONE YEAR ONLY.** `[PLACEHOLDER: auto-renew status not confirmed]`. Extend to 5+ years — in the calendar for 6 Oct 2026, backstop 4 Jun 2027 | Total outage, once the site moves. `.co.uk` recovery after expiry is time-boxed and can fail outright |
| **`novenstudio.co.uk`** | Everything, until the rename lands: the site, all canonicals, the sitemap, MX for mail, the `url` in the structured data, both LinkedIn links. **Afterwards it carries the redirects, which is not a smaller job** | [PLACEHOLDER] | **[PLACEHOLDER — registrar not recorded, expiry not recorded, auto-renew status not recorded]. This placeholder is now urgent:** the rename makes this domain the thing every old link and cached answer points at | Total outage today. After the rename: every redirect dies at once and the name becomes free for somebody else to buy — including the `noven.studio` product working in the same field. **Keep registered at least three years. Do not drop it** |
| **Namecheap** | DNS: Netlify records, Zoho MX, SPF, DKIM, DMARC, two verification TXTs | [PLACEHOLDER] | [PLACEHOLDER] | Site and mail, together |
| **Netlify** | Hosting, build, TLS. Deploys `main`. **Also the order form** once that is switched on — Netlify Forms holds submissions, which makes Netlify a processor of customer data and puts it in the privacy notice. Free tier covers 100 submissions a month | Free tier | rolling | Site offline, and every order lost in the same moment. No documented alternative host, no rollback runbook |
| **GitHub `hellonovenuk-lang`** | This repo — the source of truth and the deploy trigger | Free tier | n/a | Deploys stop; the only copy of every operating decision is at risk |
| **GitHub `hellonovenuk-lang/Noven`** | Second repo, holds brand and image originals | Free tier | n/a | Asset originals. Recorded in one line of the session log and nowhere else until now |
| **Zoho Mail Lite** | **`hello@wardith.co.uk` — created 2026-08-06, confirmed receiving, and now the address the site publishes.** The only inbound channel on a site with no phone and no form. `hello@novenstudio.co.uk` stays on the same licence as a free alias and **must keep receiving for at least twelve months**: it is in the ICO record, on both LinkedIn pages and in whatever is already cached. Never a second user — aliases are free, users are £1/month | £14.40/yr inc VAT | ~29 Jul 2027 *(inferred from purchase date, not recorded)* | No enquiry reaches the business |
| **Zoho Books** | Invoicing and revenue records | [PLACEHOLDER] | [PLACEHOLDER] | Invoicing, and the Foundation/monthly billing route |
| **Gmail `hello.noven.uk@gmail.com`** | **An identity, not a mailbox.** Owns the GitHub login, the Search Console property and Netlify's notifications. Forwards to Zoho | Free | Forwarding reviewed ~Jul 2027 | See "the concentrated account" below |
| **Canva** | **The editable master for every brand asset.** Established 2026-08-04: the SVGs in `assets/brand/` are outlined paths, so the Canva project is the only place the wordmark can be changed as type rather than redrawn. SVG export is a **Pro** feature, so the plan is paid | `[PLACEHOLDER: plan and price not recorded]` | `[PLACEHOLDER: billing date not recorded]` | **The brand becomes uneditable.** The committed SVGs still render, and the site is fine — but no asset can ever be revised, resized or re-set again without redrawing the letterforms, which `CLAUDE.md` bans. It also silently downgrades SVG export to PNG, which the repo's tooling assumes. **This was missing from the register entirely until the rename made it load-bearing** |
| **Revolut Pro** | Business bank account; the audit payment link; Foundation and monthly transfers | Free to hold. Card fees 1.0% + £0.20 personal, 2.8% + £0.20 commercial | n/a | No way to be paid. FSCS cover is capped at £120,000 **shared** with the personal balance, not doubled |
| **UK Postbox** *(ordered 2026-08-07, **live and published 2026-08-10**)* | **The address for service of documents**: the legal disclosure in the site footer, the `PostalAddress` in the Organization structured data, the ICO registered address, and the trading-name registration for "Wardith". Company 06723381, HMRC AML XLML00000192390. **Two addresses were issued and they are not interchangeable — see the note below this table** | **£12/month inc VAT** (£10 exc). PAYG page scans £1.20 each. `[PLACEHOLDER: setup fee, if any — read the first statement]` | Monthly, rolling. `[PLACEHOLDER: billing date]` | **A failed £12 card payment silently breaks a legal disclosure**, and now a published one rather than a pending one. Their terms hold mail for one month on an inactive account, then **return it to sender**; at six months the account is purged and post is shredded. And the address cannot simply be dropped — it must be migrated off ICO, HMRC and the site *first*, or continued use stays chargeable. `ops/third-party-services.md` B1b |
| **ICO registration `C1995412`** | Legal requirement to process personal data. **Address changed off the owner's home and the trading name changed to Wardith, both notified 2026-08-10** — the register now points at Lytchett House, not Birkenhead | £47/yr, Direct Debit | ~30 Jul 2027 *(inferred from "renews annually")* | Penalty of up to **£4,000** against a £47 fee |
| **Google Search Console** | Sitemap, indexation, removals. **Two properties: `wardith.co.uk` (Domain, verified 2026-08-06 via GoDaddy Domain Connect) and `novenstudio.co.uk`, with a Change of Address running between them to ~Feb 2027.** Keep the old one permanently — the move runs from it, and it holds the before/after the six-month re-check needs | Free | n/a | The only indexation diagnostic |
| **LinkedIn** | Founder profile and company page, both published in the structured data as `sameAs` | Free | n/a | Published `sameAs` points at a dead URL, breaking the site's own consistency claim |
| **Bing Webmaster Tools** | **Set up 2026-08-07.** `wardith.co.uk` submitted and indexing requested on all eight indexable pages. **This is the account that feeds Copilot**, which answers out of Bing's index — one of the four assistants the audit covers, and the only one whose retrieval source we can submit to directly. `novenstudio.co.uk` is deliberately **not** added: it only 301s away now | Free | n/a | Copilot loses its only direct route to this site. Bing never indexed the old domain either, so there is no fallback to decay back to — the site would simply be absent |

**The two addresses, and which one is which.** UK Postbox issued a mailbox
address and a courier address, and they carry different postcodes. Using the
wrong one does not fail loudly — it fails as a parcel that never arrives or a
letter that goes to a loading bay.

| | Address | What it is for |
|---|---|---|
| **Mailbox** | Kieran Smith / Wardith, Lytchett House, 13 Freeland Park, Wareham Road, Poole, Dorset, **BH16 6FA** | Letters and small packets. **This is the address for service of documents** and the only one that is published — site footer, structured data, ICO record, terms, and every official form |
| **Courier point** | Kieran Smith / Wardith, Unit 171036, Courier Point, 13 Freeland Park, Wareham Road, Poole, Dorset, **BH16 6FH**, UK | Parcels and courier deliveries only. A delivery instruction for carriers, not a legal address. **Give it to suppliers; never publish it** |

**Both name lines must read "Kieran Smith / Wardith", and the trading name is
registered with UK Postbox** — confirmed by the owner 2026-08-10. Post addressed
to a name the provider holds no record of is the standard way mail is returned in
this industry, and the trading name is the half most likely to be dropped by
whoever is filling in a form. It is registered; keep it that way if the plan or
the account ever changes.

### Ordered, decided or needed but not yet in place

| Dependency | Status |
|---|---|
| **V LOT refund** | The address for service itself is **done** — the row is in the register above from 2026-08-10. What is left of this item is the write-off: **V LOT took payment ~29 July, delivered nothing, refund requested 2026-08-07**, and its order reference, amount and payment method are **all still unrecorded**, which is exactly what a chargeback needs if the refund is refused. Chase it or write it off deliberately; do not let it lapse by silence |
| **Professional indemnity insurance** | Not bought. Should precede the first Foundation, which is where a live client site gets changed. Absent from `ROADMAP.md` entirely; researched in `ops/third-party-services.md` |
| **API accounts** — OpenAI, Google AI Studio, Perplexity | **This row was stale and is corrected 2026-08-04.** All three were opened and used for the self-audit on 2 August — 210 runs. What is *not* known is the true cost: `ops/audits/noven-2026-08-02/README.md` records **OpenAI alone at $12.63 for ~75 queries** against `ops/audit-setup.md` §6's estimate of ~£1.20 per 150, and the Gemini and Perplexity totals were never recorded. Every audit delivered spends real money on the day. Get the three real totals before the 26 August unfreeze — see `ops/plan-to-1-september.md`. **Balances as at 2026-08-09, from the owner: OpenAI $16.00, Gemini £8.95, Perplexity $4.49.** A 90-query trade run is 30 queries each; at the one measured rate that is ~$5 a provider, so **Perplexity is the one that may not finish** — arithmetic in `ops/trade-run/README.md`. **Two things still unconfirmed and both matter more than the balances: the £10 caps from `ops/audit-setup.md` §4, and whether Perplexity's auto top-up is off.** With auto top-up on, running dry charges the card during a spending freeze |
| **Password vault** | Recommended as step one of nine and there is no evidence it exists. See below |
| **Client data storage** | **Reopened and re-answered 2026-08-10.** Microsoft was decided on 2026-08-09, but the account opened is a **consumer** one, which cannot lawfully hold client records: no data-location commitment, no Article 28 processor contract, and Microsoft's own terms bar commercial use. **The answer is local, encrypted storage on the owner's own machine** — no processor, so no contract to need and no supplier's country to publish, at **£0/month against £261/yr** for the Microsoft 365 Business alternative. **Two conditions, neither optional:** full-disk encryption on and verified with the recovery key held off the disk, and an **encrypted external backup drive kept off-site** (~£30–60 once) that has been restored at least once. **Turn OneDrive folder backup off first** — Windows syncs Desktop and Documents to the consumer account by default, which would undo the whole decision silently. Sourced reasoning in `ops/client-record.md`, "Storing it locally". **Until both conditions are met, no client or prospect record exists anywhere — including the outreach list** |

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

**Two of them now are.** The Wardith domain rows below were put in the owner's
Google Calendar on 2026-08-04, with a popup a day ahead and an email a week
ahead. That is the first dated obligation in this business to exist anywhere
other than this table. **The rest are still only here.**

| When | What | If missed |
|---|---|---|
| ~~**~10 Aug 2026**~~ | ~~ICO publishes the registered address on a bulk-downloadable public register~~ — **acted on, 2026-08-10: the service address landed and the ICO was notified of both the address change and the trading name the same day.** Kept in the table because the deadline is the reason the whole address project was urgent | **Whether anything was already published before the amendment is not known and cannot be assumed away.** Bulk data that has been downloaded is not recalled by an amendment. The remaining check is one page: look up `C1995412` on the ICO's public register and confirm it shows Wardith at Lytchett House |
| ~~**24 Aug 2026**~~ | ~~V LOT decision point~~ — **resolved early, 2026-08-07: V LOT written off, refund requested, UK Postbox chosen at £12/month.** Nothing to decide on the 24th; the date is kept only so the record reads straight | **The consequence changed on 2026-08-06.** The footer placeholder was removed, so the site no longer shows the gap — it publishes no address at all, silently. Launch day now arrives with a legal disclosure missing and nothing on the page to say so. The commitment is that it lands before the first customer, not before launch |
| **26 Aug 2026** | Spending freeze lifts. API balances first, address for service second — **now £12/month, not ~£115, so the owner may want to start it earlier than this** | Six days to 1 September and nothing bought |
| **1 Sept 2026** | Operational, accepting clients, outreach active — the owner's deadline, set 2026-08-04 | — |
| **6 Oct 2026** *(in the calendar)* | Extend the three Wardith domains to 5+ years; decide whether to consolidate the registrar, now the 60-day transfer lock has lifted | Left on a one-year term, renewing at GoDaddy's higher rate, across two registrars |
| **4 Jun 2027** *(in the calendar)* | Backstop: Wardith domains expire in ~2 months | See below |
| ~29 Jul 2027 | Zoho Mail Lite renewal | The only contact channel dies |
| ~30 Jul 2027 | ICO annual renewal | Up to £4,000 |
| **~4 Aug 2027** | **Wardith domain expiry** — `wardith.co.uk`, `.com`, `.uk` | Total outage: site dark, all mail dead, structured data broken. Falls a week *after* the late-July renewals week, so it is not covered by it |
| [PLACEHOLDER] | `novenstudio.co.uk` renewal — date unknown, and it now carries every redirect | Total outage before the rename; every old link and cached answer dead after it |
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
