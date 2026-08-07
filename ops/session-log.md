# Session log

**What this is:** the full record of what changed each session, what we learned,
and why each decision went the way it did. Newest at the top.

**It lives here rather than in `ROADMAP.md` so that the roadmap stays short
enough to read at the start of every session.** `ROADMAP.md` says what is true
now and what is left; this file says how we got there. Add an entry at the end
of each session, and keep the reasoning — the point of this file is that a
decision never has to be re-argued from scratch.

---

### 2026-08-07 (V LOT written off; Icon Offices assessed and not taken)

**Done:** the owner requested a refund from V LOT, closing the 29 July decision
for good. Icon Offices (`iconoffices.co.uk`) was researched as the cheap
replacement and **rejected on the numbers**. The pick reverts to the fallback
that was already identified on 29 July — 1st Formations or Quality Company
Formations, ~£115/yr inc VAT — and it is now a purchase for the 26th with
nothing left to decide. Written into `ops/third-party-services.md` (new section
B1a), `ROADMAP.md`, `HANDOVER.md`, `ops/accounts.md` and
`ops/plan-to-1-september.md`.

**Icon Offices is not a V LOT.** That is worth saying plainly, because the easy
conclusion after being burned is that everything cheap is a scam, and it would
be the wrong lesson. Icon Offices Limited is company **10343713**, incorporated
24 August 2016 and active; it holds a Companies House **ACSP** registration
(AP000227), **HMRC AML supervision** (XNML00000198642) and an ICO registration.
Its terms, clause 3, explicitly permit publishing the address on a company
website, contracts and invoices — which is the category-2 product B1 says we
need, and the thing several cheaper providers quietly do not sell. It failed on
price, not on legitimacy.

**The reason it fails on price is the reason the whole cheap end of this market
looks cheap.** The advertised tier is £0.99/week — £45.76/yr — and it does not
forward post. Their own terms say Bronze customers "are not eligible for
on-demand postage or scanning services at an additional cost", and anything
over 100g must be collected in person, by appointment, at an address in Essex,
London, Glasgow, Edinburgh or Belfast. **From the Wirral that is not a service,
it is a storage locker.** The first tier that forwards is Silver at £120.12/yr
— *more* than 1st Formations at £115.20 — and Icon Offices sits at 4.0 on
Trustpilot with 7% one-star against 1st Formations' 4.8–4.9 across ~23,000
reviews. Paying more for worse reliability on the one purchase whose failure
mode is a missed legal document is the V LOT mistake made backwards.

**The general lesson, recorded because it will recur:** in this market the
headline price is the price of a mailbox you cannot reach, and the real price
of a usable business address is ~£115–120 whoever you buy it from. B1 has been
wrong about this twice now — first the "£30/yr Hoxton Mix" figure corrected on
29 July, then V LOT — and both errors were the same error: pricing the tier,
not the service. **When a supplier's cheapest plan is a tenth of the market
rate, find the feature that has been removed before assuming a bargain.**

**Four contract terms recorded in B1a for whoever we actually buy from**, since
none of them is unique to Icon Offices: "free" forwarding means no handling fee,
not tracked or insured delivery; providers reserve the right to change or
cancel your allocated address at will, which matters for an address that goes
into JSON-LD and gets cached; Icon's clause 3 carve-out about court summonses
sits oddly against an address whose purpose is service of documents, and is
worth asking about in writing if similar wording appears in the contract we
sign; and the trading name must be registered with the provider or post to it
may be returned or destroyed — so **Wardith** gets registered explicitly, not
just the owner's own name.

**What the write-off actually costs the plan.** The V LOT payment is gone
unless the refund lands, and the amount is still unrecorded — the order
reference, amount and payment method were never written down, and a chargeback
needs all three. More importantly it removes the last free route to closing the
address: `ops/plan-to-1-september.md` was built around "chasing V LOT is free
and is the only route that closes this before the 26th", and that sentence is
now false. The address is a firm ~£115 on 26 August, six days before launch,
with a postal lead time and KYC inside that window. **Check 1st Formations'
turnaround and ID requirements before the 26th** rather than discovering them
on the day.

**Next:** buy it on the 26th; before then, find the V LOT payment details off
the card statement while it is still recent.

**Superseded within the hour — see the entry below.** The owner set a
monthly-billing constraint straight after reading this, and 1st Formations does
not offer one. The V LOT and Icon Offices findings above still stand; the
conclusion does not.

---

### 2026-08-07 (the address, decided properly: UK Postbox, £12/month)

**Done:** the owner said the annual payment is not affordable right now and
asked for monthly or quarterly. **1st Formations and Quality Company Formations
— the two best-reviewed providers, and the conclusion reached one entry above —
are annual-only, so both were ruled out by cadence rather than quality.** The
pick is **UK Postbox's Business Street Address, Poole, Dorset: £10/month exc
VAT, £12/month inc VAT, billed monthly, cancel any time.** Written up as
`ops/third-party-services.md` B1b and propagated through `ROADMAP.md`,
`HANDOVER.md`, `ops/accounts.md` and `ops/plan-to-1-september.md`.

**The mistake in the earlier entry is worth naming, because it was a process
mistake and not a research one.** Six providers were compared on annual cost
before anybody had established that an annual payment was possible. The whole
morning's comparison turned on £120.12 against £115.20 — a £5 gap — and the
variable that actually decided the purchase was never in the table. **Ask what
shape the money has to be in before pricing anything.** B1 now carries billing
cadence as a selection criterion rather than a payment detail.

**Why UK Postbox rather than the other monthly options.** It is the only
provider checked that is monthly, credentialled, long-established *and* under
£15/month. Hoxton Mix is monthly and well-reviewed at £21/mo + VAT — roughly
£302/yr, twice the price. Icon Offices bills quarterly at £38.87, which is
£155.48/yr, so it is dearer than UK Postbox *and* carries the weaker record
that got it rejected in the first place; it stays second choice and nothing
more.

**Checked the same way Icon Offices was, which is the test V LOT never got.**
UK Postbox Ltd is **company 06723381**, trading since 2008; **HMRC AML
supervision MLR XLML00000192390**; ICO registration ZA038907; VAT registered.
Their own page sells a "**Business Trading Address** — to use on marketing
materials and stationery", states the service suits "a sole trader,
partnership, limited company or PLC", and carries an FAQ for exactly our case:
a sole trader not registered at Companies House. **That is the category-2
product sold as such, with no inference needed** — which is more than can be
said for most of this market.

**One number recorded as unresolved rather than rounded in our favour.**
Trustpilot returns 403 to direct fetching, and search results report UK
Postbox's score as both **4.0 and 4.7** across ~800 reviews. Those are
materially different claims and we could not settle which is current. It is in
the B1 table as unresolved, and it is a five-minute check on the day. **Given
this file's history with supplier reviews — V LOT's were poor and were
correctly flagged, and we bought anyway — do the check before paying, not
after.**

**Three traps written into B1b for the day of purchase:** buy the Business
**Street** Address, not their cheaper Business PO Box, because a PO Box is not
valid for this and their own FAQ says so; identity verification is a real step
with its own lead time; and pay-as-you-go page scans are £1.20 each on top of
the £12, which at our volume is pennies but should not be a surprise.

**What this does to the plan, which is the biggest practical change.**
`ops/plan-to-1-september.md` was built around a ~£115 lump sum that could not
be paid before the freeze lifted on 26 August, leaving six days to launch for a
purchase with a postal lead time. **£12 is a different kind of decision.**
Whether it fits inside the freeze is the owner's call and is deliberately not
assumed either way in the plan — but the option exists now, and it is the only
route that gets the disclosure onto the site before an early sale rather than
after one.

**Left unsolved, and flagged rather than quietly dropped:** the address is in
Poole, Dorset. **None of the credible providers is in the north-west**, so the
locality question `ROADMAP.md` raised on 2026-08-06 — whether to put a
`PostalAddress` in the structured data, and whether it says Merseyside — is not
answered by this purchase and is not a reason to pick a worse provider for
geography. Decide it deliberately when the address arrives: publish the real
locality, or publish none.

**Next:** buy it (date is the owner's call); check the Trustpilot score first;
and find the V LOT payment details off the card statement while it is recent.

---

### 2026-08-07 (Bing — the fourth assistant gets a route in)

**Done:** Bing Webmaster Tools set up for `wardith.co.uk`, indexing requested on
all eight indexable pages. `ops/search-console-and-bing.md` part 2, written
2026-08-06 and executed today. `novenstudio.co.uk` deliberately not added — it
only 301s away now, so submitting it would be asking Bing to index a redirect.

**Why this one mattered more than its fifteen minutes suggest.** The audit sells
coverage of four assistants. Three of them — ChatGPT, Google, Perplexity — reach
a site through routes nobody can submit to directly. **Copilot is the exception:
it answers out of Bing's index, and Bing takes submissions.** So of the four
assistants we charge to be found in, exactly one had a door, and until today
nobody had knocked on it. Self-audit finding 2 was that Copilot held no record of
this business at all, under either name. That is now acted on.

**Both search consoles are done.** Google closed 2026-08-06, Bing today. It is
the first point since the rename at which the indexation side of our own house
is in the state we would require of a client at the end of a Foundation.

**Submission is not indexation, and the log should not blur them.** Nothing here
proves a single page is *in* Bing's index. The proof is `site:wardith.co.uk`
returning eight pages, and it is days to weeks away on a domain four days old
with no inbound links. Both `ROADMAP.md` entries were written to say "acted on"
rather than "closed" for exactly this reason — the same distinction the audit
draws for clients, applied to us.

**One thing recorded as unknown rather than assumed: the sitemap.** The owner
reported requesting indexing on all pages, which is §2.4. It does not follow that
§2.3 happened — **URL Submission does not require a sitemap**, so doing the one
is not evidence of the other, and if the §2.1 import from Search Console carried
it across it did so with nothing on screen to say so. Written into
`own-facts-check.md` row 8 and the part 2 header as a thirty-second check rather
than assumed either way. **This is the habit the 2026-08-06 session cost a
morning to learn:** four claims in this repo turned out to be inferences that had
hardened into statements of fact, one of them ("no redirect rules need writing")
sitting two lines above an instruction to verify it that nobody ran. An
unconfirmed thing is cheap to write down as unconfirmed and expensive to
discover later.

**Also clarified today, on the owner's question — why Google got a
recommendation of five URLs and Bing gets all eight.** Google's request-indexing
quota is in the low tens per day and shared across the property, so §1.6
recommended spending it on the five pages that most need a manual nudge and
leaving the rest to the sitemap. Bing's URL Submission allowance is in the
thousands, so the scarcity that shaped the Google advice does not exist there.
In the event the owner did all eight on both, which was right on both counts:
eight is well inside Google's quota, nothing was competing for it, and a
request-indexing call is a stronger signal than a sitemap entry — the sitemap
says a page exists, the request says look now.

**Nine routes build, eight are submitted.** The ninth is `404.astro`, correctly
excluded from the sitemap and correctly never submitted. Worth writing down
because "nine pages" and "eight pages" both appear across the operating
documents and both are right about different things.

**And then §1.5 was run, and passed.** The owner ran Google's URL Inspection on
the homepage and supplied the returned HTML. Zero `PLACEHOLDER`, the
`company/wardith` `sameAs` correctly formed, `hello@wardith.co.uk` in both the
Organization and the `contactPoint`, the canonical right, and **no occurrence of
"Noven" anywhere on the page.**

**This is the first time anything in this repo has been checked against what a
crawler actually receives.** The network policy blocks `wardith.co.uk`, so every
verification any session has ever done ran against `dist` or the Netlify API —
both of which prove the *build* is right and neither of which proves the live
host serves it. `own-facts-check.md` row 1 has named that gap since it was
written. It is closed for the homepage; the pricing page is the one page
carrying prices that still has not been seen live.

**The check caught its own instructions being wrong.** §1.5 said
`company/wardith` "must appear once, in the JSON-LD". On the homepage it should
appear **twice** — head JSON-LD and visible code block — because those two being
byte-for-byte identical is the site's central claim, enforced by
`site/src/lib/json-code.ts`. So the check as written would have passed a
homepage that had silently lost half of the thing the page is about. Corrected.
Fifth wrong claim found in two days, and the same shape as the other four: a
sentence written from what was expected rather than from what was looked at.

**Bing sitemap confirmed in, and the first `site:wardith.co.uk` on Bing returns
nothing.** That is the expected reading one day after submission on a domain
four days old with no inbound links, and it is the zero this measurement starts
from. **Self-audit finding 2 closes when it returns eight, and not before** —
worth holding to, because the temptation with a submitted-and-waiting job is to
tick it and move on. Weekly check.

**The email signature was replaced rather than re-exported, and the reason is
the interesting part.** `Email Signature.svg` said `hello@wardith.com` above
`wardith.co.uk` — two domains, one business, on the highest-frequency surface
there is. Roadmap item 5 said "re-export on one domain". That was the wrong fix
twice over:

1. **Email cannot render SVG.** Outlook, Gmail's web client and most corporate
   gateways drop it. A corrected SVG would have been a correct signature nobody
   could see, and the fault would have looked closed.
2. **Its text is outlined paths, not type** — so correcting two words meant a
   Canva round trip. **That friction is what produced the fault.** An asset
   whose facts can only be changed by re-exporting is an asset whose facts go
   stale, and the address for service still has to go in on 26 August, which
   would have been a second round trip.

So the format was the root cause and the wording was the symptom. Replaced with
`assets/brand/email-signature.html`: table-based, inline styles, every fact live
text, wordmark as a PNG rasterised from the committed `logo.svg` with no path
data altered. The SVG stays in `assets/brand/` as the supplied original, and
`ops/rename-to-wardith.md` B7's closed fault stays closed — no service
description went back in.

**Two details worth not losing.** The font stack is the Palatino Linotype /
Segoe UI pair `CLAUDE.md` already chose for documents, because Newsreader and
IBM Plex are webfonts that do not exist in email — so this matches the site on
the machines that will actually open it. And `site/public/signature-wordmark.png`
**must not be deleted as an orphan**: it is the image every signature already
sitting in somebody else's inbox points at.

**Flagged, not invented:** a sole trader whose trading name is not their own
surname has to disclose the owner's name and an address for service on business
correspondence. The name is in the signature; the address is parked until
26 August, and the row is in the file commented out rather than filled with a
guess.

**One thing observed and deliberately not fixed.** In the rendered HTML the
visible code block is empty — every token span present, no text. That is the
typing animation, which blanks the text nodes and types them back at ~620
chars/sec, and URL Inspection shows *rendered* HTML, so the snapshot landed
inside that window. Bounded honestly: the head JSON-LD is unaffected, the raw
HTML carries the full block, most AI crawlers do not execute JavaScript at all,
every fact in the panel is also in `<head>` on the same page, and the page's own
"view source and compare" instruction points at raw HTML where both copies are
present. **Nothing is lost from any index.** Changing the animation to satisfy a
two-second snapshot would cost the panel the argument it exists to make, which
is a bad exchange. Written into §1.5 as understood-and-accepted so the next
session does not rediscover it as a bug.

---

### 2026-08-06 (later — why the assistants still say Noven, and a fact we got wrong about ourselves)

**The owner's question:** assistants asked to review `wardith.co.uk/` still come
back describing Noven. What is left to do.

**First finding: it is not the site.** Checked against the built output. All
nine canonicals are `wardith.co.uk`, every `<title>` ends "— Wardith", the
Organization JSON-LD is `name: Wardith` / `url: https://wardith.co.uk/`,
`robots.txt` names the AI crawlers and points at the right sitemap, the sitemap
lists eight `wardith.co.uk` URLs, and Netlify confirms `wardith.co.uk` is the
primary domain with a ready deploy. The `json-code.ts` invariant still holds.
**The rename landed. The site is not the reason.**

**The reason is that the name is two days old and nothing outside this site says
it.** `businessLinkedIn` is null, so the Organization publishes no `sameAs` at
all — wardith.co.uk asserts its own identity on its own authority and nothing
corroborates it. Meanwhile `novenstudio.co.uk` is still in the search indexes
under the old title and description, and a 301 does not rewrite an index entry.
An assistant asked about a URL it cannot retrieve falls back to the name it
*can* corroborate, which is still Noven. That is the same diagnosis the self-
audit reached about the old name, arriving from the other direction: **identity
is corroboration across surfaces, and there is currently one surface.**

**Second finding, and this one is a fault of ours.** `ROADMAP.md` claimed
`hello@wardith.co.uk` was "live on Zoho Mail … tested both directions" and that
Phase 1b was closed on it. It is not live. It has never been created. The same
false claim was in `HANDOVER.md`, `ops/accounts.md` (which had the licence the
wrong way round), `ops/third-party-services.md`, `ops/README.md`,
`ops/own-facts-check.md` — and in the block of `ops/linkedin.md` copy written to
be pasted into a public About section, which would have published a bouncing
address as the only contact route on a business with no phone and no form.

**How it happened is the useful part.** C10 of `ops/rename-to-wardith.md` swept
the old domain to the new one across the operating documents. That was right for
every sentence describing the *site* and wrong for every sentence describing the
*mailbox*, because the mailbox did not move. One find-and-replace turned a true
statement about an address that works into a false statement about an address
that does not exist, in six files at once.

**And the register that exists to catch exactly this missed it, because it was
swept too.** `ops/own-facts-check.md` is the list of every surface publishing our
facts; its Email row was rewritten by the same pass. Six documents agreeing with
each other is not evidence when one edit changed all six. Two rules written into
that file: after a bulk rename, the mailbox rows get read by hand, and the Email
row is checked against `business.ts` and a real test message rather than against
the other documents.

**`business.ts` was right the whole time**, and its comment says why — a working
address on the dead domain beats a bouncing one on the live domain. The code was
never wrong; only the documents describing it were. Nothing about what the site
publishes changed today.

**Finding 3 was closed and then reopened the same hour, and the owner was right
to stop it.** A `PostalAddress` of locality "Wirral", region "Merseyside" was
added to the Organization on all nine pages, on the reasoning that the pages
already said "the Wirral" in prose and `ops/own-facts-check.md` already carried
"Wirral, UK — city level, never a street" as a standing fact, so nothing new was
being published.

**The owner's objection was that the address for service is not confirmed** —
V LOT replied after eight days and did not inspire confidence, and the fallback
providers are not on the Wirral. That is right on its own: committing the
structured data to Merseyside before knowing where the address lands risks
publishing a fact that has to be retracted.

**Checking it turned up a worse version of the same objection.**
`site/src/layouts/Base.astro` carries a visible
`[PLACEHOLDER: address for service of documents]` in the footer of **every
page**. So the change had each page telling a human reader it has no address
while telling a machine, in the head of that same page, that it has one. **That
is precisely the drift the homepage claims is impossible** — the site shows its
own JSON-LD and says the visible facts and the machine-readable facts are built
from one file and cannot disagree. Building the exception into the one fact
still outstanding, on the page that makes the claim, would have been the
cheapest possible way to lose the argument the whole site rests on.

**And `PostalAddress` was the wrong instrument regardless.** "Kieran works from
the Wirral" is true today. "Post reaches this business at Wirral, Merseyside" is
not — there is no street line and no address for service. The type answers the
exact question the footer says is unanswered.

**Reverted in full.** `site/src` now differs from before the change only in
comments; the built output is unchanged, and the homepage's visible block is
still byte-for-byte its head JSON-LD. A note is left in `schema.ts` where the
block would go, so the next person to spot finding 3 does not re-add it.

**Finding 3 is now blocked on the address for service rather than free**, and
`ROADMAP.md` has been corrected — it listed the fix as "free and not blocking
anything". It closes *with* the address rather than before it: whatever lands is
a real postal address, is not the founder's home, and is a legal disclosure that
has to be published anyway, so it fills the footer placeholder and the
structured data from a single fact. If it is not in Merseyside, nothing has to
be taken back.

**The general lesson, and it is the second time today.** Both faults this
session came from writing down something we wanted to be true — a mailbox that
did not exist, a location we had not confirmed — rather than something checked.
The site's whole pitch is that it does not do that.

**Last thing, and it is the one that actually moves the problem the owner
asked about: the company page is renamed and `businessLinkedIn` is set.**
`https://www.linkedin.com/company/wardith/`, supplied by the owner. The
Organization now publishes one `sameAs` on all nine pages, and it renders in
the homepage record panel as well as the head, so the visible and
machine-readable versions still agree byte for byte.

**Holding it at `null` through the rename was the right call and is worth
keeping as a pattern.** Renaming a LinkedIn page changes its slug, so any value
set before the rename would have been a published claim that this business and a
dead URL are the same thing — not a broken link, a false statement, on a site
whose entire pitch is that its own facts are correct. `schema.ts` omits the key
rather than emitting an empty array, so waiting cost exactly nothing. **A
missing `sameAs` is invisible; a wrong one is a lie.**

**Why this matters more than anything else outstanding.** The diagnosis for why
assistants still answer "Noven" was that the name had exactly one surface
asserting it — wardith.co.uk, on its own authority, corroborated by nothing.
This is the second surface, and it is the one a stranger checks. It does not
work overnight and it does not replace getting the new domain indexed, but it is
the first thing that makes the name checkable rather than merely claimed.

**One thing is not verified and is recorded as row 13 of
`ops/own-facts-check.md`: nobody has confirmed the page loads without a login.**
This session's network policy blocks LinkedIn as well as `wardith.co.uk`, so it
could not be checked from here. A `sameAs` pointing at a page a crawler is shown
a login wall for corroborates nothing — it is the same fault as the
`linkedin.com/me` rule already written in ROADMAP 1a, arriving through a
different door. Two minutes in a private window settles it.

**Both LinkedIn checks came back clean the same evening.** The page loads in a
private window, so the `sameAs` points at something a crawler can actually read
— row 13 resolved. And the owner rewrote both About sections: no Noven, and the
prices match the site. **Rows 3 and 4 of the register are closed**, which were
described in that file as "the whole of the actionable problem" and had been
open since 1 August. F2 and F3 of the rename are done with them.

**Next: `ops/search-console-and-bing.md`, written this session.** Both consoles
start to finish. Three things in it are worth knowing without opening it:

- **A Search Console property is bound to the host it was verified for, so the
  rename did not carry it.** `wardith.co.uk` has no property at all. This had
  gone unnoticed because `ops/audit-setup.md` §5 said "already set up and
  confirmed, nothing to do" — true of the old domain, false since 4 August, and
  the pre-run checklist for the next audit. Corrected, along with the same claim
  in `ROADMAP.md`'s "where we are today" and `ops/accounts.md`.

  **This is the third wrong claim found today, and they are not all the same
  fault — the first draft of this entry said they were, and the owner caught
  it.** There are two shapes, and they need different checks:

  - **A sentence that was true when written and was made false by the rename,
    then never re-read.** The mailbox and this one. The suspect set is
    everything marked done *before 4 August*, because 4 August is when the
    ground moved under it. Both of these were also mechanically swept by C10,
    which is what disguised them: the sweep updated the words and could not
    know the underlying fact had not moved with them.
  - **A claim published without being checked at all.** The location block,
    which was written today and was never true. No re-read of old documents
    would have found it, because it was not old.

  **Conflating the two would send the next sweep looking only backwards**, and
  the second fault is the one that recurs — it is available every session.
- **Sign in as `hello.noven.uk@gmail.com`.** Change of Address only offers the
  pairing to an owner of *both* properties, and that account owns the old one.
  It carries the dead name and stays — F10 settled that it is an identity, not a
  brand surface.
- **Bing is now the more urgent of the two**, which inverts how it has been
  filed since July. There is nothing to migrate — Bing never indexed the old
  domain, so this is a clean first submission rather than a move — and its URL
  Submission tool takes all eight pages at once where Google's request-indexing
  is rationed. For a domain this new that is the fastest route into any index,
  and it feeds the one Copilot reads.

**Last change of the session, and the owner's call: all three visible
`[PLACEHOLDER]` blocks are off the site.** Made on the eve of submitting the
domain to Search Console and Bing, which is the argument for the timing — the
placeholders had been live since launch and survivable while nothing indexed the
domain. Submission is the moment that stops being true: they go from text on a
page nobody visits to two search indexes and whatever the assistants cache.

**The footer one was the serious one.** On all nine pages it published the
literal token `[PLACEHOLDER`, the name of an internal repo file (`ROADMAP.md`),
and a written statement that a legal disclosure requirement had not been met.
The owner's reasoning: it is compliance-relevant, not customer-relevant, and
handing a crawler a red flag to repeat to a prospect is a strange thing for
*this* business to do. Agreed, and the direction is safe — the removal publishes
less, not more.

**What it costs, said plainly: the reminder is now weaker than what it
replaced.** `ROADMAP.md` used to instruct the opposite — "don't remove the
footer placeholder until post through the address is confirmed working" — and
that instruction is now overridden and marked as overridden. A loud flag on nine
pages is impossible to forget; a source comment in `Base.astro` and a paragraph
in the roadmap are not. **The commitment that replaces the tick: the address is
published before the first customer is onboarded**, not before launch. Nothing
on the site takes a payment yet, which is what makes this defensible rather than
merely convenient. `ops/accounts.md`'s 24 August row has had its consequence
rewritten to match — the risk is no longer "the gap is visible on launch day",
it is "the gap is invisible".

**The other two were replaced with copy rather than deleted**, which is what the
owner asked for and is the better answer in both cases:

- **Homepage, "Where's the proof?"** — the case-studies placeholder is gone and
  the section now ends by pointing at `/ask-your-ai/`: we ran the audit on
  ourselves before selling one, failed it, published it in full, and changed the
  name because of what it found. That is proof of method for a business with no
  clients, and it was already sitting on the site unlinked from the one section
  whose entire subject is the absence of proof.
- **`/ask-your-ai/`, "What happened next"** — that block was never customer copy
  at all. It was an instruction to the next session, addressed to nobody who
  reads the site, and it was about to be crawled as if it were prose. Moved into
  a source comment; the paragraphs it sat above already stood on their own. Added
  in its place, at the owner's request, the standing commitment: **the audit is
  re-run on ourselves at intervals and every one is published on that page,
  dated, whatever it says.** That generalises what was already promised about the
  second run, and it is the strongest thing on the site — no competitor with real
  clients is publishing their own bad results.

**Verified after the change: zero `[PLACEHOLDER]` anywhere in the built output,
and no internal reference of any kind** — no `ROADMAP`, no `ops/`, no `.astro`,
no `business.ts`. The homepage's visible code block is still byte-for-byte its
head JSON-LD.

**Also added to the register as row 14, because it kept coming up and was
tracked nowhere:** two Netlify projects were public with no password —
`noven-2-0-preview` (a full Noven-branded copy of the business, raised as D0.1a
on 2026-08-04 and still open) and `aesthetic-unicorn-619923`, which appeared in
no operating document at all. Live crawlable copies under the dead name are
directly against the thing being worked on this session.

**Both deleted by the owner the same evening, and confirmed against the API:
one project remains on the team.** Row 14 closed, D0.1a closed. **The
generalisable bit is how the second one was found — by listing the team, not by
reading the register.** D0.1a existed because somebody happened to look; the
third project had no entry to find. A surface nobody documented is a surface
nobody checks, so the sweep now lists the host rather than working from its own
rows. The same argument applies anywhere creating a public thing is one click.

---

**Merged and deployed, and this is the publishing moment the session was
building to.** `main` at `d35557a`, Netlify deploy `ready` in production,
`commit_ref` confirmed against the API, 12-second build, secret scan clean over
28 files.

**What went live:** the `sameAs`, and no page saying `[PLACEHOLDER` any more.
Everything else in the merge was records.

**The full verification was run against the merged result before the push, not
against the branch** — nine pages, every canonical on `wardith.co.uk`, the
`sameAs` present on all nine Organization blocks, the five prices unchanged at
250 / 800 / 150 / 400 / 700, zero placeholders, no internal path in any visible
text, `robots.txt` and sitemap on the new domain, and the homepage's visible
code block still byte-for-byte its head JSON-LD. That last one is the site's
central claim and a merge is exactly when it would break unnoticed.

**Order of operations mattered and is worth keeping.** The Netlify copies were
deleted, then the merge deployed, and only then is the domain submitted for
indexing. Reversing any two of those hands a crawler either a Noven-branded
duplicate or a pre-merge page with the placeholders still on it — and the first
crawl of a new domain is the one that sets the initial index entry.

**Next session picks up at `ops/search-console-and-bing.md`**, which is written
and unstarted. Nothing in the repo blocks it.

---

### 2026-08-06 (close — the Google side is finished)

**Sitemap submitted, indexing requested on all eight pages, and both LinkedIn
About sections confirmed showing `hello@wardith.co.uk`.** That closes the Google
half of `ops/search-console-and-bing.md` and the last thread left hanging by the
mailbox move — the About copy had been rewritten a few hours before the new
address existed, so it was worth re-reading rather than assuming.

**All three of the audit's own promises now hold for this business.** The facts
are readable by machines, they are consistent across every surface we control,
and the surfaces agree with each other: the site, the structured data, the
company page and the founder profile all carry one name, one set of prices and
one contact address. That is the check `ops/own-facts-check.md` exists to run,
and it is the first time it has passed end to end.

**What is left is not on the Google side.** Bing has never indexed this business
under either name, and Copilot answers from Bing — `ops/search-console-and-bing.md`
part 2, written and unstarted. It is the highest-leverage free job in the file.

### 2026-08-06 (later still — the mailbox lands, and the last Noven leaves the structured data)

**`hello@wardith.co.uk` exists and receives.** The owner created it in Zoho and
confirmed mail arrives. The zone was then read independently rather than taken
on trust: MX to `mx.zoho.eu` / `mx2` / `mx3`, **exactly one `v=spf1`**, a DKIM
key at `zmail._domainkey`, and DMARC `p=none` — whose `rua` now points at a
mailbox that exists, closing a loose end flagged earlier the same evening when
that address was still fictional.

**So `business.ts` flipped, and with it the last machine-readable Noven on the
site.** The email was 25 of the 43 occurrences counted a few hours before —
present in the Organization and ContactPoint JSON-LD of all nine pages, and
visible on the homepage inside the very panel captioned *"What an AI assistant
reads on this page"*. The site was pointing at a box and telling assistants to
read it, and the box contained the old domain.

**Seven of nine pages now contain no reference to the old name in any form.**
What remains is confined to the two `/ask-your-ai/` pages and is deliberate: the
name-change explanation, and the reproduced 3 August report, which carries the
finding *"not one of the 210 automated answers cited novenstudio.co.uk"* and the
report's own signature block. **Both stay.** The standing decision is that
nothing in that report is altered to flatter the present, and neither is
misleading — the old address still receives and must for twelve months.

**Holding the old address on the site for two days was right and is worth
keeping as a pattern.** A working address on a dead domain beats a bouncing one
on a live domain, because an enquiry lost to a bounce is lost silently. The
condition written into the code — *flip when the alias exists and a test message
has arrived* — was met before anything changed. That is the same shape as
`businessLinkedIn` being held at `null` through the rename, and both were right
for the same reason: **a wrong published fact is worse than a missing one.**

**Still owed, and it is invisible from the site:** nobody has sent *from* the new
address and confirmed `SPF: PASS`, `DKIM: PASS`, `DMARC: PASS` in a real
message's headers. DNS records existing is not the same as authentication
passing, and a new domain that fails gets filtered silently — which in launch
week is indistinguishable from nobody replying. D0.4 step 5.

**Records closed with it:** ROADMAP 1c-3, rename E1 and E2, and the Search
Console rows in `ROADMAP.md` and `ops/accounts.md`, which still said
`wardith.co.uk` had no property hours after it got one. **That is the same stale
class as everything else found today, caught this time within the hour** —
because the sweep was done against what had just been verified rather than
against what the documents already said.

---

### 2026-08-06 (last — the redirects never existed, and Google's rejected form found it)

**Change of Address failed validation, and the failure was worth more than the
tool.** "301-redirect from homepage — Redirected outside the destination site."
The instruction had been to stop and report if that check failed, and stopping
was right.

**The site was being served at four addresses with no redirect anywhere.**
`novenstudio.co.uk` rendered the Wardith homepage *with `novenstudio.co.uk`
still in the address bar*. Google's expanded panel said "Redirect wasn't found"
against `https://novenstudio.co.uk/`, `/pricing/` and `/about/`. All four apex
domains resolve to Netlify's `75.2.60.5`, and `netlify.toml` contained no
redirect rules at all.

**The assumption that caused it is written down in D3 of
`ops/rename-to-wardith.md`: "No redirect rules need writing — Netlify 301s every
non-primary domain to the primary."** It does not, or not on this site.
Everything downstream was built on that sentence: D0.1 called the alias
behaviour "a live proof that DNS and TLS are correct", D3 called flipping the
primary "the whole of it", and the roadmap recorded the switch as done.

**Two lines below that assumption, the same item says: *verify the direction
actually flipped, on the day, with a real request to a real inner page.* That
was the correct instruction and it was never carried out.** Writing a check down
is not doing it. Nine days passed.

**And the evidence was in every deploy.** Netlify's own summary has been
reporting **"No redirect rules processed"** on every build since the flip,
including the one read out in full earlier today while confirming the merge.
It was read as boilerplate.

**Why it mattered more than a failed tool.** The old domain was serving *current*
content, which keeps it alive in the index rather than retiring it — and it
means a crawler or an assistant reaching `novenstudio.co.uk` found Wardith's own
pages sitting there under the old name. **That is not a stale mention of a dead
name; it is a live statement that the two are one site**, published at the
strongest level available, while the owner was in this same session asking why
assistants keep saying Noven. It is a plausible contributor to exactly that.

Canonicals pointing at `wardith.co.uk` on every page are what stopped it being
worse. **A canonical is a hint and a 301 is not.**

**Fixed with seven explicit rules in `netlify.toml`** — version controlled and
diffable, rather than a dashboard setting with no history. Every one carries
`force = true`, which is load-bearing: without it a redirect only fires when no
file matches the path, and every path here has a file, so the rules would be
silently ignored for precisely the pages that matter. `:splat` keeps it page for
page, which D3 committed to. Validated before deploy: seven rules, and **no rule
matches `wardith.co.uk` itself**, so no loop.

**Also caught by the same check: `wardith.com` and `wardith.uk` were serving the
site too.** A1 says they are owned and redirecting and never published as an
address. The first half was not true either.

**Deployed and confirmed the same evening.** Merge `a54e17e`, Netlify deploy
`6a751b6b`, production, ready, 13 seconds. **The deploy summary now reads
"7 redirect rules processed — All redirect rules deployed without errors."**
That is the same line that had been reading *"No redirect rules processed"* on
every build since the flip, which makes it the cheapest possible regression test
for this fault: **if that line ever says "No redirect rules processed" again,
the redirects are gone.** Read it on every deploy that touches `netlify.toml`.

**The general lesson, and it is the fourth of this shape today.** A confident
sentence written before the change, never re-tested after it. The other three
were the mailbox, the Search Console property, and the six-page sitemap claim.
**This one is the worst, because the document that contained the wrong
assumption also contained the check that would have caught it.**

**And the deeper one, which is about this repo rather than about Netlify.**
Every fault today was found by something *outside* the repo refusing to agree
with it — Google's validator, a browser address bar, the owner's own memory of
what he had set up. Nothing inside the repo caught any of them, because the repo
was the thing making the claims. **A document cannot verify itself, and a
build passing proves the build passed.** The checks that earned their keep today
all had one property: they asked a system we do not control what it actually
sees.

### 2026-08-06 (the self-audit is published — `/ask-your-ai/`)

**The owner's idea, and it is a good one:** put our own audit on the site with a
prompt telling the reader to hand it to their own AI assistant and ask what it
makes of the quality, credibility and price. He had already done this privately
and found assistants complimentary about the work. Two jobs in one — promotion,
and preparing a client for what the audit actually reads like.

**Two pages, not one.** `/ask-your-ai/` carries the argument;
`/ask-your-ai/self-audit/` reproduces the 3 August report in full.

**The report is published as HTML, and the PDF is secondary. This was the main
technical decision.** The obvious build was a PDF download. It is the wrong one
for this business: the standing rule is that the site stays crawlable static
HTML, and this is now the richest page on the site for the exact questions we
want to be found for — ten real questions, four assistants named, verbatim
answers, a competitor distribution, a method. Putting that behind a format
these systems read least well would be a strange thing for *this* business to
do. The report page is 2,469 words of crawlable text with `Report` JSON-LD
naming the Organization as author, publisher and subject.

**Three things in the delivered report fought with publishing it, and each was
resolved by declaring it rather than by editing quietly.**

- **It names eleven real competitors, with counts.** The owner's instruction was
  not to name them: most are genuine businesses doing real work, and none asked
  to appear in our marketing. The names are out and the counts stay, because the
  *distribution* is the finding — one business took roughly a fifth of every
  recommendation going — and it survives the names coming out.
- **It quotes four prices, all superseded five days later.** Resolved twice —
  see the correction below, which is the more important half of this entry.
- **It is branded Noven.** Kept, and made the hook. The audit is why the rename
  happened, so the page leads with the failure and explains the name in the
  second section. A silently rebranded report would be less credible, not more.

**Nothing in the report body was altered to flatter the present.** Where the
document is out of date it is left out of date and marked. A record quietly
corrected is not a record.

**Corrected the same session, and the owner caught it: the prices had to come
out, not be annotated.** The first build kept the report's four figures — £30,
£350, £125, £750 — and set a note beside them saying what the prices are now.
The reasoning was rhetorical: the paragraph those figures sit in is *about*
Google serving a stale price for this business, so leaving them in and owning it
read as the most honest paragraph on the page. **The owner asked whether that
many recent price changes would confuse the assistants, and the systems answer
beats the rhetorical one.** Six price figures for one business on one page, four
of them wrong, is a retrieval hazard: a chunk containing *"a £30 audit and a
£350 setup, against the £125 and £750 you charge"* reads as current pricing to
anything that grabs it without the surrounding dates. **This business exists to
find that exact fault on other people's sites.** Building it deliberately into
our own, for a turn of phrase, was the wrong trade.

**So the figures are subtracted rather than revised, and the finding survives
intact** — *"prices from an earlier version of the site, less than a quarter of
what you actually charge"* says everything the numbers said. The report body now
carries **zero price figures**; the only £ on either page is the site-wide
footer ask, built from `business.ts`. A rule is written into the top of
`self-audit.astro`: **do not add a price to that page, not even a correct one**,
because a correct price there is a second copy that can go stale on its own, and
the whole argument for the removal is that the page is not where a price should
be read. It links `/pricing/` instead.

**A real defect found while checking this.** The review prompt on `/ask-your-ai/`
had `£250` typed into it as a literal string, twice — the first hardcoded price
on this site since `business.ts` was made the single source. It would have gone
stale silently at the next repricing, inside a block written to be copied and
pasted elsewhere. Now interpolated from `plan('audit')` like everything else.
**Worth remembering that prompt text is copy like any other** and needs the same
rule; it is easy to miss because it looks like data.

**The .docx master got the identical treatment.** If the PDF and the web page
disagreed about our own prices, that would be the precise inconsistency this
business sells fixing. `build-publication-copy.py` is committed beside the audit
so the publication copy can be rebuilt from the untouched original rather than
reconstructed by hand; it fails loudly if the text it expects has moved.

**The competitor section became the best part of the page, after the owner
reframed it.** The first draft was a complaint about businesses publishing
"best provider" pages awarding themselves the title. The owner's version is
better: most named competitors are genuine and unnamed out of fairness, some
are not — fake accreditations, claims that outrun the operating period — and
rather than characterise anyone, the page hands the reader a due-diligence
prompt to check *any* provider. **Including us.** The page then pre-empts its
own result: run it on Wardith and you will find a one-person business, a name
with no record behind it, no awards, no accreditations and no testimonials.
Saying that before the reader discovers it is the whole posture of the site.

**Nothing is asserted about any identifiable competitor.** The section describes
a practice, names nobody, claims nothing about anyone's motive, and does not
assert that those pages are why anyone outranks us. Sharpening it further needs
evidence that can be pointed at, and should be discussed before it is written.

**Standing rules held to, and checked rather than assumed:** no acronym anywhere
in the copy; no all-caps tags, no three-column feature rows, no repeated
calls-to-action — the page asks once, in the footer, and deliberately not in the
body, because a "book now" button halfway down a page arguing for taking nobody's
word for anything would undo it. Verified in the built output: **0 elements
hidden with JavaScript disabled** on both pages (2,122 and 2,469 words readable),
**0 WCAG AA contrast failures** on either, and no horizontal overflow at 390px or
1280px. The new `Prompt` component builds its clipboard string from the same
values it renders, so what a reader copies and what they read cannot drift — the
same rule the JSON-LD follows, applied to a numbered list, which loses its
numbering if copied out of the DOM.

**What is deliberately unfinished.** The "What happened next" section is a
`[PLACEHOLDER]` block holding space for the Wardith rerun between the 26 August
unfreeze and the 1 September launch. It is written to be publishable whichever
way the rerun goes, and the page says so in its own copy: *a business that
publishes only its good audit has told you what kind of business it is.*

**The PDF is an owner job and the master is ready.**
`Noven-audit-report-2026-08-03-for-publication.docx` is the redacted version
with the three notes inserted, sitting beside the untouched original. It has to
be exported from Word rather than converted — `CLAUDE.md`, and LibreOffice in
the session container could not load any document at all, including a plain text
file. No PDF is linked from the site, so there is no broken link waiting.

### 2026-08-05 (the second repricing — 250 / 800 / 150 / 400 / 700)

**Audit £125 → £250. Foundation £750 → £800. Maintain £95 → £150, Grow £250 →
£400, Lead £495 → £700.** Scope unchanged everywhere. Confirmed by the owner
before the copy was applied. Full reasoning in `ops/service-tiers.md` §11;
§9 is left untouched as the record of the 2026-07-31 repricing.

**What prompted it.** §9 set the old prices against *estimated* effort and
said so: *"these prices work only if delivery cost matches them, and delivery
cost is currently an estimate."* The self-audit then produced a real
deliverable — 228 answers, four assistants, repeated runs, a written
diagnosis — and against that £125 was low enough to misrepresent the product.
**Then Maintain became the problem rather than the audit:** the owner's read
was that a buyer paying £250 for an audit and the best part of £800 for a
Foundation would question a two-digit monthly fee, which is why the whole
ladder moved rather than just the top.

**A cost argument was made and then withdrawn, and that matters.** The alarm
came from the self-audit's OpenAI figure ($12.63 for ~75 queries against an
estimate of ~£1.20 per 150) and was extrapolated across all three providers.
The owner then supplied the missing totals — **Gemini 86p for 70 queries,
Perplexity $0.51 for ~70** — and the extrapolation was wrong: OpenAI is
10–20× the other two and was driving the whole figure. **Maintain's real tool
cost is about £7.50 a month, 5% of the new price. There was no cost crisis.**
Recorded in §11 explicitly, because a future session reading only the first
half of that exchange would reach the opposite conclusion.

**So this is priced on the value of the work, not on costs** — and if it had
been cost-driven the right fix would have been cheaper queries, not higher
prices.

**Round numbers, decided by the owner.** A 245 / 795 / 150 / 385 / 675 ladder
was on the table and left Maintain as the only number not ending in 5. Both
fixes were coherent; the owner took the round one, and it is the better fit —
**charm pricing is a mild sales tactic, and this business has already refused
founding rates, bundles and referral discounts** on the grounds that they sit
badly on a brand built on plain dealing.

**Applied across 14 files, and the historical/current distinction was the
whole job.** `business.ts` is the single source, so the pricing page, the
five `Offer` objects and the JSON-LD moved together from one edit — but the
`schemaDescription` strings restate prices in prose and had to move by hand,
and eight meta descriptions and two FAQ mentions hardcode them. **Nothing in
`session-log.md` or `service-tiers.md` §9 was touched:** "the audit went from
£30 to £125" is a statement about a date and rewriting it would falsify the
record. `audit-method.md` §1 was date-stamped rather than renumbered — its
reasoning was correct at £125 and only strengthens at £250.

**`third-party-services.md` needed arithmetic, not substitution.** Its card
fees are computed from the amounts: 1.0% + 20p on £125 is £1.45, but on £250
it is £2.70, and the commercial rate goes £3.70 → £7.20. Twenty-four figures
recomputed rather than swapped, including the monitoring-platform comparison
(£23/month is 13–15% of £150 Maintain, not the 20–25% it was of £95).

**Verified:** build clean at 7 pages, only the five new prices appear anywhere
in the output, the JSON-LD offers read 250/800/150/400/700, and **both
homepage code panels are still byte-identical to the JSON-LD in the head** —
the property the site's whole argument rests on.

**Not merged.** Publishing this changes a price in the structured data
assistants read, where caches and third-party copies persist long after an
edit — the reason `CLAUDE.md` asks for a sentence before a merge like this.
Google's index is *still* carrying the £30/£350 prices from two repricings
ago (`own-facts-check.md` 3.2), which is the live demonstration of how slowly
this settles.

### 2026-08-05 (the technical audit, made runnable on somebody else's site)

**The finding, from the owner's question: can we actually do the crawlability
and technical half of the audit from just a client's URL?** Reading the filled
self-audit checklist back, the honest answer was no — not as the method was
written. The Noven run leaned on four things a client audit will never have:

- **robots.txt read from the source repo** (`site/public/robots.txt`), not
  fetched live. The session's own network policy blocked outbound fetches, so
  source access silently substituted for the check.
- **Password walls, redirect rules, header rules, CDN presence and edge
  functions read off the Netlify dashboard** — our own hosting account.
- **JSON-LD "validity" reasoned from knowing the code that generates it**
  ("malformed JSON is structurally unlikely"), not from parsing live output.
- **Google's "can be indexed" answer from Search Console URL Inspection**,
  which needs verified ownership of the domain.

None of that was wrong for a self-audit — it is *more* reliable than a blind
fetch. The problem was that `audit-site-checklist.md` didn't mark any of it as
self-audit-only, so it read as a list anyone could run on a client. Left
alone, the first client audit discovers this at the worst possible moment.

**Built `ops/site-check/site_check.py`** — stdlib-only, no API keys, no
per-query cost, so unlike `audit_query.py` it is a reusable tool rather than a
per-audit throwaway. It sits beside `ops/name-check/` as the second tool in
that shape. It does groups 1 and 2 from the public URL alone: robots.txt
fetched and parsed with Python's own `robotparser` against every crawler name
the checklist lists, homepage fetch with a non-browser UA, redirect chain
logged, login-wall and challenge-page and CDN signals, JS-shell word-count
heuristic, sitemap fetch and XML parse, JSON-LD extraction with `@type`
inventory and common-field presence. Hard request cap (default 8), and no
default output path inside the repo — `--out` points at the client's own
folder, per `audit-method.md` §5.

**The dashboard checks are approximated from outside rather than dropped**,
and that is arguably the better test: what an unauthenticated crawler actually
meets, not what a config file claims. Recorded because the instinct would be
to treat the external version as a downgrade.

**What deliberately stays manual, and is now written down as such:** the
`site:` index searches (scraping results pages is fragile and against those
providers' terms), Search Console URL Inspection (client-granted access, an
optional upgrade), all of group 3's off-site half, group 4 entirely, and
"does the page state a price / name real towns" — a regex hunting for `£` out
of context is the invented precision `CLAUDE.md` rules out.

**Every group 1 and 2 item is now tagged** `[script]` / `[public]` /
`[client access]` / `[read]`, so the distinction can't rot back out.

**One wording bug fixed on the way.** `audit-method.md` §2 said the Copilot
section "leans on the Bing Webmaster Tools check". It doesn't — the check
actually performed was a public `site:` search. Wardith's Bing Webmaster Tools
and Search Console accounts are registered against `wardith.co.uk` and can see
nothing on a client's domain. As written it invited a future session to think
a client audit needs webmaster access it will never have. Both files now say
public search, with the upgrade path named separately.

**Then, from a second owner question: how do we find out what built their
site?** The checklist had a "site platform, if identifiable" field and a
strong note that it matters — "decides whether the Foundation is an afternoon
or a negotiation with somebody else's web person" — but no method for
identifying it and no mapping from platform to what we actually ask for. The
script was fetching the exact HTML that gives it away and throwing it out.

**Platform fingerprinting added** — WordPress, Wix, Squarespace, Shopify,
GoDaddy Website Builder, Webflow, Duda, Weebly, Drupal, Joomla and the static
site generators, from generator tags, asset CDNs and vendor headers. Hosting
(Netlify, Vercel, GitHub Pages, Cloudflare Pages) is reported separately
because it answers a different question: those mean a developer exists, so
access is a deploy path, not a login. Tested across eight shapes including
GoDaddy detected from `wsimg.com` alone with no generator tag, and a layered
WordPress+Shopify page correctly declining to pick one.

**The distinction that was worth writing down, and that the old single field
hid: the platform sets the technical ceiling; the relationship sets what's
actually available.** A WordPress site on an agency maintenance contract is
the most capable platform on the list and still a verdict B. Capability is
not access. The checklist now asks both, and carries a platform table mapping
each to who holds the keys, what to request, and the likely A/B/C verdict.

**GoDaddy Website Builder is flagged as the dangerous one** — limited
custom-code and head access, so part of the Foundation may be undeliverable.
Establish what its editor accepts *before* quoting, not after taking £795.

**Plan-tier limits are deliberately not pinned to named plans** (Wix,
Squarespace and Weebly all gate code injection behind paid tiers, and those
tiers get renamed). A wrong specific in an ops file gets quoted at a client
months later. The instruction is to check their actual plan on the day.

**Access guidance lives in the checklist only, not in the script** — one copy,
per `service-tiers.md` §4's warning that two copies in two files is the
mechanism by which documentation goes stale. The script names the platform and
points at the table.

**Third question, on the back of the platform work: if the developer has gone,
could we rebuild the site from a crawl?** Answered no, and the reasoning is now
in the checklist under "When the developer has gone" rather than left in a
conversation. Three separate grounds: a mirror captures output not source (no
server-side code, no database, and close to nothing at all on a JS-rendered
site — *the sites easiest to clone are the ones that needed it least*); under
UK law copyright sits with the author by default, so **paying a freelance
developer for a website does not transfer it without a written signed
assignment**, which small-business web jobs routinely lack; and a faithful copy
faithfully reproduces the exact problems the audit exists to find.

**Added the recovery order that comes first**, because verdict B was being
reached too early. Check **who owns the domain** — if it is in the developer's
name that outranks everything else in the audit — then **who is billed for
hosting**, since hosting access is the master key and hands over database,
theme and files together where developer access would not. Only then verdict B.

**And the commercial question behind it: should we sell rebuilds as a separate
revenue line? Settled by the owner: no — and no brokering them either.**
`service-tiers.md` §10.

**Not selling one** rests on one decisive argument: **it puts a price on
reaching verdict B or C.** It attaches the largest fee in the business to the
most pessimistic verdict the audit can reach, decided by the person who would
be paid for it — unprovable from outside even when delivered honestly every
time, in a business whose entire product is trustworthy diagnosis.

**Not brokering one is the owner's correction to this session's first
answer, and the better call.** A referral pathway was drafted — we specify
what the new site must do, a developer builds it, we sell the Foundation on
top — and scrapped the same day. Three reasons kept: it is **a solution to a
client we do not have** (this may not turn up until the tenth or thirtieth
client, and building the process now is guessing at its shape — the same
mistake the runner was deliberately deferred to avoid); **it walks straight
back into the conflict**, because having specified the site we would then sell
a Foundation the build had partly delivered, and every honest fix for that
needed a reduced scope, a reduced price and an awkward pre-referral
conversation; and **a referral is a stake** — fee or no fee, recommending the
builder makes us a party to the build, with no PI cover.

The owner's framing, which is the right one: **if their website is
inaccessible we simply tell them, and they decide what to do next.** The audit
still names what is wrong and what is missing — that does not depend on us
being the ones to fix it, and on a verdict B or C it *is* the entire value of
what they bought, so the report has to be specific enough for a stranger to
work from.

**Published as a credibility asset, per the owner's instruction.** New FAQ
entry, "What if my website cannot be updated?", carrying the line the pricing
page already made but the FAQ never did — the report is theirs to hand to
whoever does look after the site. Plus the independence claim, which is only
true *because* of the two decisions above: **"we do not build websites, we do
not recommend anyone who does, and we take nothing from anyone you choose. We
have no stake in who fixes it."**

**Build verified:** clean at 7 pages, FAQPage structured data parses, now 13
questions, and the new answer is in the machine-readable copy an assistant
reads as well as on the visible page — which is the coupling `faq.astro` is
designed around and the reason anything added there is a publishing decision.
**Not merged: this is on the branch, so nothing is live yet.**

**Not verified live.** The script is unit-tested against local HTML strings
(robots parsing with a named `Disallow` correctly overriding a catch-all
`Allow`, JSON-LD parse and field inventory, JS-shell detection firing on an
empty body and not on a real page) but this sandbox blocks outbound fetches —
the same limit that caused the original problem. **It needs one real run from
the owner's machine against `wardith.co.uk`**, where the self-audit already
recorded the ground truth by hand, and then against one arbitrary
small-business site, which is the real test of whether it survives messier
robots.txt and malformed JSON-LD than our own site produces.
### 2026-08-05 (the hero record, written out line by line)

**The owner asked for the animation to go and the code to come back — this
time interactive, appearing a line at a time as though it were being typed,
with the facts that matter picked out.** Done, and the film is off the site.

- The homepage hero now carries the structured-data record at every width, and
  the panel writes itself out at about 620 characters a second when it comes
  into view, with a caret sitting after the last character written. It follows
  its own caret down, and settles back at the first line when it finishes —
  the end of the record is the least useful thing to leave a reader looking
  at.
- **Five lines are marked: `name`, `email`, `description`, `founder.name` and
  `areaServed`.** Each carries a brass edge, a brass wash and a brass underline
  on its value, and each explains itself in one plain sentence under the panel
  when it lands, and again whenever the reader points at it, taps it or tabs to
  it. Colour is not doing the emphasis on its own — the rule, the underline and
  the sentence say the same thing three ways, which is what keeps it working
  for a reader who can't separate brass from ink.
- The marks are keyed by path (`founder.name`), not by line number, so adding a
  fact to `business.ts` can never quietly move them onto the wrong lines. That
  is why `toLines` now returns a path with each line.
- Controls: **Skip** while it writes, **Replay** after, and tapping the block
  itself skips. All three are added by script and hidden without it.
- **Nothing here is load-bearing.** With JavaScript blocked the panel is simply
  the complete block, as before. With reduced motion set, no typing, no caret,
  no flash — the block is there and the marks and their explanations still
  work. A small inline script hides the lines the instant the panel is parsed
  so it never flashes complete first, and it undoes itself after three seconds
  if the module never arrives.
- The record used to appear in "Where's the proof?" on wide screens and in the
  hero on narrow ones, so the page held exactly one copy. It now lives in the
  hero at every width, and the proof paragraph points up to it rather than down
  at a second copy.
- **Removed:** `site/public/video/` (543KB of it), the `.hero-film` markup and
  styles, and the film's play-on-scroll script. The render source stays in
  `assets/video/` and still works — `assets/video/README.md` now says at the
  top that the site doesn't use it. This closes the outstanding "mobile cut of
  the animation" question from 2026-07-28: there is nothing left to cut.
- **Checked in a real browser, not just built:** wide and phone widths, the
  written-out block matching the JSON-LD in the head character for character
  when it finishes, hover, tap and keyboard focus on a marked line, skip,
  replay, reduced motion, and the page with scripting off entirely.
- **Merged to `main` at the owner's instruction.** The branch was parked for
  about an hour first — the plan was to collect the other website changes in
  progress and merge everything once, to spend fewer Netlify builds — and then
  the owner reversed it: there are enough builds left before Friday's reset,
  and a long-lived branch collecting unrelated work complicates more than it
  saves. Merged as it stood.
- **What the merge published:** the homepage hero, and nothing else. No
  business fact, no price, no canonical, no `robots.txt` rule and no byte of
  the JSON-LD the assistants read was touched — checked against `origin/main`
  before merging, because a homepage change must not move a price or an email
  address by accident. The 543KB of video stopped being served.
- Worth keeping for next time: **a zip dragged onto Netlify's drop zone runs no
  build at all**, so previewing a branch that way costs nothing from the
  allowance. A pull request can trigger a deploy-preview build on every push,
  so a branch that is going to collect several rounds of work is cheaper left
  as a plain branch until it is ready.
- **One bug worth remembering.** The first version followed the caret using
  `offsetTop`, which measures down the whole page rather than down the panel.
  On a desktop, where the panel sits near the top of the document, it was a few
  lines out and looked like nothing worse than a loose scroll. On a phone,
  where the panel is most of a screen down, it scrolled the panel clean past
  its own caret and the block appeared **empty** for the whole animation. It
  now measures both boxes with `getBoundingClientRect`. Nothing above the fold
  on a desktop is proof that a thing works on a phone.

### 2026-08-04 (published — the site is Wardith)

**Merged to `main` at the owner's instruction.** What that published: a new
business name on every page, a new `url` on every canonical and in the
sitemap, a changed `Organization` identity in the JSON-LD the assistants read,
new artwork throughout, and the removal of the company-page `sameAs`. The
prices did not move — 125 / 750 / 95 / 250 / 495, verified in the built output
before the merge, because a rename must not shift a price by accident.

**One thing was deliberately left on the old domain: the email address.** The
site publishes `hello@novenstudio.co.uk`, not `hello@wardith.co.uk`, because
the Zoho work is not done and the new address does not exist. That value goes
into the structured data and the contact page on every page, and it is the only
inbound channel on a business with no phone and no contact form — **so
publishing it early would have made every enquiry bounce, silently.** A working
address on the old domain is a smaller fault than a broken one on the new
domain. One line to flip once a test message has arrived; it is item 2 in the
new roadmap section and the reasoning is written into `business.ts` beside the
value so nobody "tidies" it.

**The merge leaves one contradiction live overnight, and it is a thirty-second
fix.** Every canonical now says `wardith.co.uk`, but `novenstudio.co.uk` is
still Netlify's primary domain, so `wardith.co.uk` currently redirects *to* the
old address — a canonical pointing at a URL that redirects back. Setting
`wardith.co.uk` as primary reverses every redirect at once and completes the
switch. It is item 1 in the new roadmap section, ahead of everything else.
Flagged to the owner before the merge rather than discovered after.

**`ops/rename-to-wardith.md` Phases A–D0 are done bar the two owner jobs.** The
whole of the DNS and TLS work was verified the same day: three GoDaddy zones
read row by row against the written spec, one wrong digit caught on
`wardith.uk`, certificates reissued, and the alias redirect proven page-for-page
in the direction that costs nothing to get wrong.

**Roadmap 1c-3 is new and is where the next session starts.** Netlify primary,
then Zoho, then LinkedIn, then the four smaller surfaces. Written as
instructions rather than as a summary, because the next session begins cold.

### 2026-08-04 (the site copy, and an assumption the owner was right to reject)

**Cut from the homepage, at the owner's instruction:** a paragraph saying that
an assistant asked about Wardith today would not know who we are. It sat
directly under "Where's the proof?", which is the highest-stakes position on
the page, and the owner's objection was that a prospect reads it as *this does
not work.* That is correct and it is the owner's call to make.

**But the better objection was the one about evidence.** The paragraph asserted
an outcome nobody has measured. The self-audit's verdict was that the
**identity** was the blocker rather than the site — "Noven" belonged to at
least four other businesses, so the answers went to them. A name with no
occupant removes that specific failure, and the fixes went in with it. Whether
the assistants can name Wardith by launch is genuinely open, and writing a
paragraph that assumed the pessimistic answer was exactly the thing this
business tells clients not to do: state as fact something you have not checked.

**So the copy now follows the evidence, and the evidence arrives before
launch.** The owner is running a second audit on Wardith between the 26 August
unfreeze and the 1 September launch. If it comes back named, the strongest
line on the site writes itself and is checkable — *ask ChatGPT about Wardith
and see*. If it does not, the site says nothing about it and stands on the
proof it already has. Recorded in `ops/plan-to-1-september.md` Phase 2 as a
funded item, and as the first half of the G2 measurement: how fast a new name
is learned, timed from the day the site went live under it.

**The other two rewrites stand, and they were bug fixes rather than
judgements.** Three passages had invited the reader to ask an assistant what
Noven does and compare the answer. The self-audit proved that test returned
nothing — 210 answers, not one citing the site — so the invitation was failing
before the rename. Both now point at the check the site passes every time:
view the source and see that the visible answers and the machine-readable ones
are built from one file. **That is a stronger claim than the old one**, because
`json-code.ts` enforces it byte for byte.

**One thing written down that had not been said plainly before: indexation is
the lever, not training.** An assistant names a business either from what the
model memorised — which moves on the timescale of model releases — or from a
live lookup at answer time, which moves on the timescale of a crawler. Only
the second can plausibly happen in four weeks. That makes Bing Webmaster Tools
and Search Console the highest-leverage free jobs in the whole plan rather
than housekeeping: the self-audit found Copilot had no record of the site *because
Bing never indexed it*. Do them the week the site goes live, not the week of
the audit.

### 2026-08-04 (later still — the domain settled, and two hard constraints set)

**`wardith.co.uk` is the business.** Owner's decision, closing A1. `.com` and
`.uk` are owned and redirecting and are never published as a contact detail.
The decision was forced sooner than planned by the brand set itself: the
supplied `Email Signature.svg` reads `hello@wardith.com` above `wardith.co.uk`,
which made the choice by accident and made it two different ways in one asset.
That file must be re-exported before it is used anywhere. Nothing else in the
set carries a domain.

**Two constraints set by the owner, and they are the frame for everything now:
no further spending until 26 August, and fully operational with outreach active
by 1 September.** Written up as `ops/plan-to-1-september.md`. The finding is
that these do not conflict — **the entire rename is free.** DNS, Netlify,
a Zoho alias, LinkedIn, the redirects and the repo work all cost nothing, so
the twenty-two-day freeze is spare capacity rather than a blocker. What the
freeze does is compress the paid items into six days, and that list is short:
API balances, and the address for service if V LOT has still not delivered.

Three things the constraint surfaced that were not visible before:

- **A freeze on decisions is not a freeze on payments.** Canva Pro, GoDaddy
  add-ons and API auto-top-up can all charge without anybody deciding
  anything, and none of their billing dates is recorded.
- **`novenstudio.co.uk`'s unknown expiry stopped being an admin gap.** If it
  lapses inside the freeze, the site goes dark and all mail dies with no
  budget to fix it. It is now the first job on the list.
- **The audit's tool cost is roughly ten times the estimate the prices were
  set against.** `ops/audits/noven-2026-08-02/README.md` had already recorded
  OpenAI alone at **$12.63 for ~75 queries** against §6's ~£1.20 per 150, but
  it was filed as an accuracy problem. Under a spending freeze it is a
  delivery problem: every audit spends real money on the day it is delivered,
  so a client who buys on 27 August cannot be served on an empty balance. It
  also puts a question against the £95 Maintain price. **Not to be answered
  while launching** — but before the first monthly client renews.

**`ops/accounts.md` gained a row it should always have had: Canva.** It is the
editable master for every brand asset — the committed SVGs are outlined paths,
so nothing can be re-set as type anywhere else — and it was absent from the
dependency register entirely. If the Pro plan lapses the site is fine and the
brand becomes uneditable, which is a slow failure nobody would notice for
months. The API accounts row was stale in the other direction and was
corrected: all three were opened and used for the 2 August self-audit.

**Phase D0 written: the four owner jobs, step by step.** Netlify, GoDaddy DNS,
Zoho and LinkedIn — the only parts of the rename that live behind a login. Two
things fell out of writing them:

- **The 301 redirects need no rules.** Netlify 301s every non-primary domain
  to the primary, preserving the path, so promoting `wardith.co.uk` at merge
  time reverses the lot in one action — as long as the old domain stays
  attached. D3 shrank from a page of rules to one checkbox and one
  verification.
- **Attaching the new domains now, days before the merge, is free insurance.**
  TLS gets days to issue instead of minutes, and until the flip the new
  domains simply redirect to the old one, which is a live proof the DNS is
  right rather than a hope.

**`og.png` was never a Canva job, and saying so was wrong.** It is a build
product of `assets/og/og.html`, which *references* the committed wordmark — so
re-rendering picked up the Wardith artwork on its own. The same was true of
both LinkedIn PNGs. Three corrections came out of actually reading those
files:

- **`assets/linkedin/logo.html` was broken**, and had been since the Noven
  originals were deleted: it placed `Social Avatar.svg`, which the Wardith set
  does not include. It now sets the navy disc in CSS and places the supplied
  `Icon Mark.svg` on it — the same move `og.html` already makes when it puts
  the committed wordmark on a navy field. The artwork is still used as
  supplied; only the ground behind it is ours.
- **Two files hard-coded the Noven wordmark's aspect ratio** (`1193.92 :
  236.39`) to derive a height. Left alone they would have squashed the new
  artwork silently rather than failing. Both now carry the Wardith ratio and a
  note to re-derive it on any re-export.
- **The 48px legibility test was re-run rather than inherited.** The old
  README recorded that "N." holds up small; a W is a wider, busier letterform
  and the old test does not transfer. "W." reads on white and on a dark feed.

### 2026-08-04 (later — domains bought, and the rename scoped)

**Three domains held:** `wardith.co.uk`, `wardith.com` and `wardith.uk`, GoDaddy,
**one year only**. The GoDaddy checkout pushed Microsoft 365 email at £0.99/mo
and it was declined — `ops/third-party-services.md` A1 had already rejected
Microsoft 365 and Google Workspace, the £0.99 is a first-term teaser against a
£6.49 renewal (£77.88/yr versus Zoho Mail Lite's £14.40), and a mailbox should
not be created before it is decided which of the three domains the business
actually is. Nothing is lost by declining: mail can be added to a domain at any
time, and the domain was the only time-sensitive part of that page.

**The renewal reminders are in a real calendar, which is a first for this
business.** `ops/accounts.md` says in as many words that its own dates table
*"is not a reminder — put these in an actual calendar"*, and records that three
documents had said so and nothing had ever been set. Two events now exist: 6 Oct
2026 to extend to a long term and decide whether to consolidate the registrar
(the 60-day transfer lock lifts ~3 Oct), and 4 Jun 2027 as a backstop two months
before expiry. **The August expiry falls a week after the late-July renewals
week**, so the clustering that covers Zoho and the ICO does not cover this one —
which is exactly why it needed its own date rather than a line in the table.

**`ops/rename-to-wardith.md` written — the full checklist, seven phases.** Built
from an inventory of the repo rather than from memory, and two things it turned
up changed the plan:

- **The brand assets cannot be retyped.** The owner's intention was to reuse the
  Noven pack with different words, which is the right instinct and saves real
  money — but all six SVGs in `assets/brand/` are **outlined vector paths, zero
  `<text>` elements, no `font-family` anywhere**. Typing WARDITH into them
  produces default-font letters beside designer-drawn ones, which is the same
  fault as the Inter-retyped wordmark caught on 27 July arriving through a
  different door. The route through is the editable original in the second repo
  (`hellonovenuk-lang/Noven`) or identifying the typeface from the outlines.
  Also: seven letters where there were five, so the lockup gets ~40% wider and
  the hard-coded dimensions at `Base.astro:88` and `:164` must change or the
  logo renders squashed. And the favicon and social avatar are monograms — an N
  becoming a W is a redraw, not a rename.
- **The hero animation does not need re-rendering.** `assets/video/frame.html`
  uses generic captions and abstract blocks; no business name appears in it.
  Only the filename carries the old name. Two lines in `index.astro` and a file
  rename. Worth checking rather than assuming, because a re-render was the
  single most expensive thing the rename could have required.

**The argument the checklist is built around: switch once, not gradually.**
`CLAUDE.md` already warns that merging publishes into the JSON-LD the assistants
read and that caches persist. A rename moves the `name`, the `url` and both
`sameAs` links at once. Done as one event it is something the assistants can
learn; dribbled out over three weeks it publishes a business whose own facts
disagree with each other, which is the exact failure we sell finding.

**And the reassuring half, which is true and worth saying.** The self-audit found
that **not one of 210 automated answers cited `novenstudio.co.uk`**, and that
Bing had never indexed the site at all. The usual argument against moving domain
is the accumulated indexation and links it forfeits. **There is none to
forfeit.** This is the cheapest moment this change will ever be, and it gets more
expensive every week.

**One thing the rename partly breaks, recorded now so it is not discovered in
February.** The self-audit's frozen q06 and q07 ask what the assistants know
about *Noven*. Under a new name the honest answer is "nothing" for months, which
is not a comparison but a different question. The way to keep the baseline
valuable is to run both at the six-month re-check — the frozen Noven questions
measure how long a dead name persists, the same questions about Wardith measure
how fast a new one is learned. One extra batch of queries, and it is the best
evidence this business could own: its own claim, tested on the only business we
are allowed to experiment on.

### 2026-08-04 (the name is WARDITH)

**The owner's decision, and it closes finding 1 of the self-audit.** Noven does
not keep its name. The replacement is **WARDITH**, built from the owner's own
name — the back half of *Edward* and the back half of *Smith*. Locito and Tovan
were shortlisted first and both rejected the same day by `ops/name-check/`;
this is the third candidate and the one that survived.

**What was actually checked, so nobody has to guess later.** A web search for
`"Wardith"` returns no company, no product and no brand anywhere. The only hits
are two private individuals and some hobby art. That is a different category of
result from the three names before it: Noven had four businesses, Locito had
Localito Marketplace Ltd and the Lockito app, Tovan had Tovan.ai and two
registered companies. **Nobody is occupying the commercial slot.** On the same
day, `wardith.com`, `.co.uk`, `.uk` and `.studio` all had no delegated
nameservers — a strong signal all four are free, and not proof.

**What was not checked, and it is not a small list.** Companies House (their
search refused the automated request), and the trade mark register (not
attempted). Both are owner jobs. The name-check tool's README already says it
is none of those three things; that limit is now load-bearing rather than
theoretical, so it is repeated in `ROADMAP.md` 1c-2 where the open work sits.

**The tool was deliberately not run on WARDITH, on the owner's instruction, and
the reasoning is sound enough to record rather than log as a shortcut.** The
tool's job is to find an occupant. A free search found no occupant, so all
twelve queries would return the "I don't have information on that" that the
README already defines as the pass. Locito and Tovan earned the money because
each looked plausible *and* had a real product one keystroke away. Paying to
confirm an absence a search has already shown is not the same purchase. Written
into `names.txt` beside the name so the exception travels with it.

**One argument was raised against the name and settled by the owner — recorded
so it is not reopened.** The objection: *Wardith* is hard to transmit by voice,
a listener has to choose between Wardith, Wardyth, Wardeth and Wardif, and a
mistyped name fragments a business's own information — which is the exact
failure this business is sold to find in other people's. **The owner's answer,
which is right:** by the time anyone is saying the name aloud they have already
found us, so the spoken form is not the discovery path; and read-to-said runs
only one way, so there is no real ambiguity in the direction that matters. The
objection was about a risk in the abstract; the business is discovered by
typing and clicking. It does not survive contact with how the work actually
arrives.

**The one residual thing worth knowing.** While searching, an assistant's own
summariser quietly offered *Wardley* instead — the nearest neighbours being
Wardley, Wardite (a mineral) and Wardian. Not a collision, and not a reason to
reject anything, but it is the shape of drift to watch for on the first audit
run after the rename, alongside how long "Noven" persists.

**Domain first, and it is time-sensitive.** Nothing else in the rename is safe
to start before the domain is held. Everything the change touches is scoped in
`ROADMAP.md` 1c-2 — it is not a find-and-replace, because the domain lives in
the canonicals, the sitemap, `robots.txt`, the JSON-LD, Netlify, Zoho and both
LinkedIn pages, and the brand assets carry a wordmark that cannot be retyped.

**A gap in this file, noted rather than fixed.** The sessions of 2 – 4 August —
the self-audit run, the name-check tool, the Locito and Tovan rejections, the
Office-documents rule — are not written up here. The audit has its own folder
and `names.txt` carries the rejections, so nothing is lost, but the log skips
from 1 August to this entry. Worth backfilling before the record gets colder.

### 2026-08-01 (audit readiness, and getting our own facts straight first)

**The jargon ban was challenged, tested, and narrowed — owner's decision.**
`CLAUDE.md` said *never use "GEO", "SEO", or search-industry jargon anywhere on
the site*. The owner's challenge: a buyer who has already researched this
arrives holding one of those acronyms, so a site containing the word nowhere
cannot be the answer when they ask for it. **That is right, and it is the exact
failure the audit is sold to find on other people's businesses** — we tell
clients to publish pages answering the questions their customers actually ask,
then declined to do it for one particular question.

The rule now splits by job rather than banning outright. **Persuasion copy stays
plain** — headlines, navigation, body text — and Noven never describes itself
with an acronym; that half of the rule was doing real work and survives. **One
deliberate exception:** a single FAQ entry or answer page may name the terms in
order to translate them. Live at *"Is this what people call GEO or AEO?"* on the
FAQ page, which also says out loud why the acronyms appear nowhere else — a
plumber losing work to a competitor does not think of it as an optimisation
problem. That candour is what keeps the entry from reading like everyone else's
version of the same page.

Two things worth keeping from the argument. **The terms are unsettled** — GEO,
AEO, "AI SEO", no winner — which is an argument against building an identity on
one, but not against translating them. And **the absolute ban had already cost
us something concrete**: flag 1 in `audit-setup.md` §9 exists because banning
the industry's words left no noun at all for the trade, which made writing our
own audit questions harder than it should have been.

The industry-term question (§9a) stays in the run, with its job changed: it was
proposed to settle the argument, and now that the argument is settled it is the
**before** measurement for the FAQ entry we are about to publish.

**Merged to `main` on the owner's instruction.** `CLAUDE.md` says never commit
to `main` and finish every piece of work on an unmerged branch; this is the
seventh explicit override, and it is logged as a call rather than a new default
— the rule stands for the next session.

**What going to `main` publishes, this time: nothing visible.** Netlify deploys
`main`, but the only site file touched is a comment in `site/src/data/business.ts`.
The built pages and the JSON-LD are byte-identical to what is already live —
confirmed by building before the merge (7 pages, offers reading
125 / 750 / 95 / 250 / 495). Everything else in this change is `ops/` and the
root documents, which are not published anywhere. So unlike the 31 July merge,
this one opens no one-way door.

**And then the rule itself was amended, which is why the override count stops
here.** The owner's clarification: the intent was always *branch, review, agree,
merge* — not *never merge*. Eight logged overrides in one day was the rule
failing to describe the workflow rather than the workflow misbehaving. The
branch-first half was doing real work and is kept, along with a new requirement
that carries the reason the old rule existed: **say what a merge will publish
before doing it**, because Netlify deploys `main` and a published fact is closer
to a one-way door than a normal site's. Future merges the owner has agreed to
are business as usual and are not logged as overrides.

**A second merge to `main` the same day, also on the owner's instruction — and
this one does publish.** The narrowed jargon rule and the GEO/AEO FAQ entry went
live on 2026-08-01, on the owner's explicit call to have the FAQ updated before
the audit rather than after. It is the eighth override, and it changes what x01
measures: the recommendation was to run first and publish second, so that the
industry-term baseline was taken before the answer existed. Published first, the
baseline is *published but not yet crawled* — weaker, still usable, and now
written into `audit-setup.md` §9a with the two conditions that keep it honest
(run within days of the deploy, record both dates in `timings.md`). Recorded
here because a baseline whose conditions are forgotten becomes a claim we cannot
defend in six months, which is the one thing the method exists to prevent.

**What is still live and still wrong, unchanged by either merge:** the footer
`[PLACEHOLDER: address for service of documents]` on all seven pages, and both
LinkedIn About sections. The LinkedIn pages are wrong *on purpose* until the
self-audit has run — `ops/own-facts-check.md` section 5.

**The owner's question was whether we are ready to run the audit, prompted by
noticing that assistants still describe Noven's services at the old prices.**
The answer on readiness is no — none of `audit-setup.md`'s pre-flight exists yet,
and every item on it is an owner action (accounts, keys, caps). The stale-price
observation turned out to be the more useful half of the question.

- **Where the old prices are actually still published: LinkedIn, both pages.**
  The company page About and the founder profile About were pasted from
  `ops/linkedin.md` before the 31 July repricing, so they say £30 / £350 / from
  £75. They are named in our own structured data as `sameAs`, which means we
  have formally told the assistants that those pages describe this business.
  The copy in `ops/linkedin.md` is corrected; the paste is the owner's, and
  `ops/linkedin.md` is reopened until it is done.

- **Deliberately not fixed before the self-audit.** An assistant quoting a price
  we abandoned is a `named_wrong` outcome on our own baseline — the single most
  persuasive finding an audit can produce, per `audit-method.md` section 4, and
  it is free evidence about how long stale facts persist. Fixing LinkedIn the
  morning before the run destroys the measurement to gain six hours. So: run,
  then fix the same day, then re-run q06 and q07 alone at six months. Recorded
  in `ops/own-facts-check.md` section 5 and as step 0 on run day.

- **`ops/own-facts-check.md` written.** The register of every surface where our
  own facts appear, what each must say, and what it currently says. It is the
  audit's third promise applied to us, and its absence is why the repricing
  updated the site and nothing else.

- **The repo was carrying old prices in seven files.** `ops/README.md`,
  `HANDOVER.md`, `ROADMAP.md`, `ops/service-tiers.md`,
  `ops/third-party-services.md`, `ops/linkedin.md` and a comment in
  `business.ts` still stated £30 / £350 / £75 as current. Corrected. Dated
  historical statements — the session log, `service-tiers.md` section 9, the
  "at £30 this argument held" passages in `audit-method.md` — were left alone,
  because they are correct as history and rewriting them would destroy the
  record of why the prices moved.

- **`third-party-services.md` C2 needed rewriting, not renumbering.** Its
  argument for taking the audit on a card was built on £30 versus £350. At £125
  the conclusion holds and gets stronger — the fee is ~1.2–3.0% of the sale
  against ~1.7–3.5% at £30, because the fixed 20p shrinks against a larger sale
  — but the numbers it argues from all moved, and the Foundation's card fee went
  from £5–10 to £8–21, which reinforces keeping it on invoice. Also closed the
  file's "audit depth" open question, decided in `audit-method.md` a day later
  and never struck through.

- **Correction: this repo is private, not public.** Verified against the GitHub
  API. Five places asserted it was public, and several rules were justified by
  it. The rules are unchanged and the wording is now *written as though it were
  public* — visibility is one click and does not retroactively unpublish a
  committed key, and the reason client data stays out is UK GDPR rather than a
  repo setting. **The useful consequence: the repo was never part of the
  stale-information problem**, because nothing reads it. LinkedIn is the cause.

- **Two smaller drifts fixed on the way past.** `ROADMAP.md` 1a still promised
  the audit "in one working day" against the site's two, and the ops file count
  was wrong in both READMEs and in different directions.

### 2026-07-31d (merged to main on the owner's instruction — the new prices are live)

**`CLAUDE.md` says never commit to `main` and finish every piece of work on an
unmerged branch. The owner overrode it explicitly, as they have six times
before. Logged as an explicit call, not a new default** — the rule stands for the
next session.

**What going to `main` actually does:** Netlify deploys `main`, so this publishes
the repricing to `novenstudio.co.uk` and, more importantly, into the JSON-LD that
the assistants read. The site is deliberately built so those systems ingest the
business facts and repeat them confidently, which is the whole product — and it
means a published price is closer to a one-way door than a normal site's is.
Caches and third-party copies persist after an edit. The prices were confirmed
individually before the copy was applied, so this is intended, but it is the
reason the next price change costs more than this one did.

**Live as of this merge:** audit £125, Foundation £750 at a fixed four-part scope,
Maintain £95, Grow £250, Lead £495 monthly. Questions 10/15/25. Turnaround two
working days. "Order" not "Book". "Available to clients across the UK" rather
than the present-tense claim that we already have some.

**Still live and still wrong, unchanged by this merge:** the footer
`[PLACEHOLDER: address for service of documents — see ROADMAP.md]` on all seven
pages. It was already on `main` and is not made worse here, but it remains the
one published defect, and it is a legal disclosure rather than a cosmetic gap.

### 2026-07-31c (the repricing, and clearing the decisions the review turned up)

Everything below was recommended in 2026-07-31b, put to the owner, and confirmed
before it was applied. The prices were confirmed individually.

- **The finding that drove it: the ladder was inverted.** Price against
  estimated effort and every step up earned less per hour than the one below —
  audit ~£9–12, Foundation ~£17–35, Maintain ~£27–42, Grow ~£18–28, Lead
  ~£11–19. **The premium tier paid about the same as the loss leader.** Success
  at selling made the business worse. That is not a level problem, it is an axis
  problem: the tiers separated on question volume, which is pure cost to us and
  little the client can feel. A page is a permanent asset; a longer spreadsheet
  is not.

- **New prices.** Audit £30 → **£125**. Foundation £350 → **£750**, scope fixed.
  Maintain £75 → **£95**, Grow £125 → **£250**, Lead £250 → **£495**. Questions
  10/25/50 → **10/15/25**. Lead's fortnightly checking removed. Full reasoning
  in `ops/service-tiers.md` section 9.

- **A bundle went in and came straight back out, same day.** "Foundation free
  with twelve months of Grow" was applied to the pricing page and then removed
  when the owner questioned it. **Nothing commits anyone to twelve months** — the
  plans roll month to month with no minimum term, published in four places
  including the FAQPage structured data and the pricing page's meta description
  ("No lock-ins"). The offer as written let someone take the £750 Foundation, pay
  one £250 month, and cancel: £1,000 of work for £250, entirely within our own
  terms. The "£3,000 committed" figure was false. **The cancellation policy is
  the older and better-argued decision and it wins.** The generalisable lesson:
  any offer phrased "for N months" is incompatible with no-minimum-term, and the
  terms are not the thing to bend.

- **Then settled properly: we do not bundle services at all.** Alternatives were
  offered — crediting the Foundation back monthly, a half-price first three
  months — and the owner declined all of them. The question was not which bundle
  to run but whether to bundle, and the answer is no. Recorded in
  `ops/service-tiers.md` section 9 as a **standing decision**, with the full list
  of what it rules out (Foundation-with-a-plan, first-month-free, annual-payment
  discounts, founding rates, referral discounts, "N months for the price of M")
  so it does not get re-litigated one offer at a time by a future session hunting
  for conversion. Every product is bought and priced on its own; a client who
  buys more pays more.

  Three supporting reasons worth keeping, because they are stronger than "the
  owner said so": every bundle found so far ends in an asterisk on the
  cancellation terms, which are in the structured data, and a business selling
  machine-readable accuracy should not need a footnote on its pricing page; the
  repricing set each product against its own effort, so a combination discount
  would say the standalone price was soft; and the upgrade engine is already the
  monthly record, which does the job without anyone selling. Also practical —
  one person cannot service a promotion with a window and a clawback, and the
  client record has no column for it because it should not need one.

  **Not a bundle, and stays:** the tiers are cumulative — Grow contains Maintain,
  Lead contains Grow. That is one product at three sizes.

- **Why before the first client.** It is free now and expensive later. No client
  to upset, no invoice to amend — and the monthly plans have no minimum term by
  design, so a later rise on paying clients is a churn event with nothing holding
  them. Launch prices are the only prices that can be set for free. **No founding
  rate**: considered, declined by the owner, on the grounds that a discount game
  sits badly on a brand built on plain dealing.

- **Raising the Foundation without capping it would have made things worse.**
  `how-it-works.astro` promised "writing or restructuring key **pages**" —
  plural, unbounded — and no time budget for the Foundation exists anywhere in
  this repo. The scope is now four fixed pieces of work, the fourth being **two**
  answer pages, and the page says so. Work found outside the four is quoted, not
  absorbed. It is still the only product with no estimate of how long it takes.

- **The audit's economics argument had to be rewritten, not just renumbered.**
  `audit-method.md` section 1 argued the audit was a loss leader that shouldn't
  be judged as profitable work. True at £30. At £125 and an honest 2.5–3.5 hours
  it earns ~£36–50/hour, so the argument is retired rather than repeated out of
  habit — with a new consequence in its place: **at £30 a thin report was
  survivable because the price apologised for it; at £125 it isn't.**

- **Considered and deliberately not done: cutting the audit's run volume.** Five
  runs on the three discovery questions and three on the rest would have halved
  the classification time. It was the right answer at £30, when the time budget
  was binding. At £125 it isn't — the volume is what the client is paying for,
  and a second band scale for three-run questions would complicate the one part
  of the report that is currently unambiguous. Revisit only if the timed
  self-audit lands above three hours.

- **The time budget now includes the work.** The audit table totalled 95 minutes
  and budgeted the largest step at a dash — reading 168 answers and assigning
  each an outcome, a competitor list and any untrue statement, folded into a
  20-minute report step. It does not fold. It is 60–110 minutes on its own, and
  leaving it out is exactly what made £30 look like £20/hour when it was nearer
  £9–12. New total: **2h40 – 3h30**. The site's turnaround moved from one working
  day to two, because one was never deliverable — `audit-questions.md` requires
  the client to confirm the questions first, which means an email and a wait.

- **`ops/monthly-record-template.md` written.** The audit runs once per client;
  this runs every month, for every client, forever, and it had a price and no
  format. One page, four sections, bands not percentages, and one hard rule: **a
  provider's model change is flagged at the top**, or the first month an
  assistant changes behaviour reads to the client as their own decline.

- **`ops/accounts.md` written**, and it is the continuity answer. Every account,
  cost, renewal, and what breaks if it lapses — no credentials, because this repo
  is public. Real gaps are marked `[PLACEHOLDER]` rather than guessed, and the
  worst is the domain: **registrar, expiry and auto-renew status are recorded
  nowhere**, on the one dependency whose failure is total.

- **`ROADMAP.md` now distinguishes decided from done.** New `[D]` marker: `[x]`
  means true in the world, `[D]` means a document describing an intention. All of
  3a's method items and 3c's tier items became `[D]`. They had been `[x]`, which
  told a reader the business does things it has never done once.

- **Two stubs deleted, one filled.** `org-chart.md` (five company seats) and
  `escalation-rules.md` (three never-do-this-without-me rules) described a
  business with employees and someone to escalate to; this one has neither, and
  `CLAUDE.md` already does the escalation job. `spine.md` → **`client-record.md`**
  with the field list filled in — "the spine" was used in three places and
  defined in none.

- **Site copy no longer duplicated in `service-tiers.md` section 4.** It used to
  transcribe the live pricing copy in full, and the repricing proved the cost:
  every quoted block was wrong within an hour. The site is canonical; the section
  now says where the copy lives and what must stay true about it.

- **Two truth gaps closed while the copy was open.** Three pages said in the
  present tense that Noven *is* working with clients across the UK — there are no
  clients; now "available to". And four calls to action said "Book the audit"
  when nothing can be booked; now "Order". Both were flagged in 2026-07-31b and
  left for the owner; the owner asked for them.

- **Verified, not assumed:** build clean at 7 pages, all five prices correct in
  the JSON-LD offers, and no stale price, cadence or "Book the" string anywhere
  in `dist/`.

**Still the constraint, and worth writing where it will be re-read:** these
prices are set from *estimated* effort. Nothing in this business has been timed
because nothing has been done. If the self-audit shows Maintain takes three hours
rather than one, section 9 gets rewritten, not defended.

### 2026-07-31b (an outside read of the whole business, and the entry point it was missing)

- **The question asked:** could an external person read this repo and understand
  what is sold, what has been done, and what is left to launch and run? The
  answer was no, and the reason was not the quality of the thinking. Every fact
  an outsider needs is here. There was no path to any of it — no entry point, no
  index, no glossary, and no way to tell a decision from a delivery.

- **`HANDOVER.md` written**, at the repo root, for a reader with no context: the
  five products, what exists, what does not, the critical path, the dated
  obligations, the dependency register, the ongoing operating cadence, the
  decisions only the owner can make, and a glossary of the vocabulary this repo
  uses without defining. It is the file to keep current; if it and `ROADMAP.md`
  ever disagree, one of them is wrong and it matters which.

- **`ops/README.md` written** — an index of the thirteen ops files with a status
  against each. The reading order for the five audit documents (method →
  questions → checklist → report template → setup) existed only as a "read X
  first" line inside each file, so it was discoverable only by opening all five.

- **The distinction the repo was missing: decided is not done.** `[x]` currently
  means "we settled this" in some places and "this exists in the world" in
  others. The ICO registration and the bank account are done. The pay button and
  every ticked item in 3a and 3c are decisions about things that have never
  happened. `audit-method.md` gets this exactly right in its own header —
  *"decided on paper, unvalidated in practice"* — and the roadmap's ticks carry
  no such qualifier. Not changed here, because retagging the roadmap is the
  owner's call, but it is the single most misleading thing in the repo.

- **Stale statements corrected, all verified against the code or against the
  same file's own later sections before touching them:** `site/README.md`'s
  pre-launch placeholder list (four of six bullets were dead, and the "grep for
  `[PLACEHOLDER` and replace every instance" instruction returned five hits of
  which three are unreachable or the detector function itself — that instruction
  was deleted from the roadmap on 30 July as spent and never propagated here);
  `third-party-services.md` naming Gmail as the contact address after Zoho
  replaced it on 29 July; the same file's to-do list still calling the ICO fee
  "currently missing from the roadmap entirely" 300 lines after recording it as
  done; the same file listing Netlify Forms under "deliberately not
  recommending" while C2 picks Netlify Forms; and `ROADMAP.md` pointing at
  section 1a for the service address, which is in 1c — a section labelled
  closed, so the reader concludes the item is settled.

- **Two findings worth carrying, both verified in the built output:**

  **The footer placeholder is a published disclosure breach, not a pending
  task.** `[PLACEHOLDER: address for service of documents — see ROADMAP.md...]`
  renders in the footer of all seven pages of the live site, naming an internal
  file, on a site engineered so that AI assistants read the business facts and
  repeat them confidently. The roadmap treats it as a footer field awaiting a
  supplier. It is the breach itself, and it is being crawled.

  **Three pages state in the present tense that Noven is working with clients
  across the UK** — `Base.astro:170`, `contact.astro:48`, `about.astro:151` —
  and there are no clients. Not changed here: it is the owner's copy and the
  right wording is a commercial choice, not a correction. But it is the exact
  class of claim this business exists to remove from other people's sites.

- **The gap that matters, stated plainly.** Five documents specify an audit
  that has never been run once. Three monthly plans are published, priced and
  machine-readable with no runbook for delivering a single month of any of them.
  The £350 Foundation is on sale with no method and no time budget anywhere in
  the repo. None of that is a crisis while nobody has paid; all of it becomes
  one on the day someone does. **The correct next move is not more planning —
  it is to run one audit on Noven itself and find out what this costs in
  hours.** The self-audit is the only item that is both unblocked and
  asset-creating, and it produces the one number the business plan rests on: how
  long a month of Maintain actually takes.

### 2026-07-31 (the audit has a setup guide, so the Noven run can start cold)
- **`ops/audit-setup.md` written.** The method said what to do; nothing said what
  to have open, signed up for and capped before doing it. This is that: three API
  accounts, keys in `~/.noven/env` at `chmod 600` and never in this repo, a spend
  cap on each provider before the first call, the free accounts for the hand
  half, the audit folder outside the repo with the two CSV headers ready, a
  smoke test, and the run-day order with the clock.
- **Noven's own ten questions are drafted in it**, from the frame in
  `audit-questions.md`. **Three slots are flagged rather than filled:**
  `{trade}` has no settled customer word — a business owner describes this rather
  than naming it, so the discovery questions are written as descriptions and the
  owner confirms the wording; `{trigger}` is `[PLACEHOLDER]` until there are real
  enquiries to take it from; and `{town}`/`{region}` run UK-wide rather than
  local, which is a deliberate deviation that has to be stated in the report —
  **local discovery is where most client findings come from and this run does not
  test it.**
- **The experiment is specified: q01, q06 and q09 at ten runs on all three API
  assistants.** 150 + 45 = **195 API queries**, script cap 250, plus 18 by hand.
  Spread across three categories and all three providers so the answer isn't
  provider-specific.
- **The 150 queries get issued by a throwaway script, not the runner.** Method
  section 7 deferred the runner on purpose; a crude script whose rough edges get
  written down is the specification for the real one. Hard cap, append-and-flush
  so resume is free, `outcome`/`competitors`/`errors` left blank because those
  are judgement.
- **Bing Webmaster Tools moved to a prerequisite** rather than a loose 1e item.
  Copilot's real diagnostic is Bing indexation, so it has to be set up before the
  run, not during it.
- **Two things could not be verified from this session** and are marked as such
  in the file: the provider documentation was blocked by the network policy, same
  as when the method was written. So every URL is a starting point rather than a
  deep link, and Perplexity's per-request fee — already the one figure method
  section 6 marks unconfirmed — is on the pre-flight checklist to confirm and
  correct.
- **Flagged to the owner:** whether client audits can run on providers' free
  tiers at all, given free tiers often permit the provider to use submitted
  content and a client audit carries their business name and, for a sole trader,
  personal data. Doesn't block the Noven run — we can consent to ourselves — and
  it wants a line in the privacy notice (1c) once known.
- **Next:** unchanged — do the Noven self-audit.

### 2026-07-30 (the roadmap got too big to read, so the log moved out of it)
- **`ROADMAP.md` went from 19,500 words to 4,100.** It was being read in full at
  the start of every session, and more than half of it was history rather than
  anything that changes what to do next.
- **This file is that history, moved out whole.** Nothing was rewritten or
  deleted in the move — every entry below is exactly as it was written on the
  day. That was deliberate: condensing the log means choosing which of the
  owner's own reasoning to throw away, and that isn't a call to make in passing.
  It can be trimmed later if it ever needs to be.
- **The roadmap's closed items were condensed hard**, which is where the rest of
  the reduction came from. The rule applied: **a closed item states the decision
  and its live consequence, and nothing else.** The argument behind it lives here
  or in the relevant `ops/` doc, and the roadmap points at it. Almost all of that
  reasoning was already duplicated between the two places, so very little of it
  existed only in the roadmap.
- **Two open jobs surfaced that had been buried inside ticked items** and are now
  visible as their own checkboxes: opening the LinkedIn profile URL in a private
  window to confirm it's publicly visible, and the `pricing.astro` fix making
  "booking" mean payment received rather than signature.
- **"Where we are today" was rewritten to lead with what's blocking**, which is
  the ICO home-address publication and the missing service address, rather than
  with what's already built.
- **Checked rather than assumed:** every distinctive fact in the old file — the
  ICO application number, the fees helpline, the brand hex values, the FSCS cap,
  the HMRC dates, the V LOT fallback — is still present in one of the two files.
  The only text dropped outright was 1a's instruction to search the repo for
  `[PLACEHOLDER]`, which is spent: 1a is closed, and the two placeholders still
  live on the site (the footer address and the home page case studies) are each
  tracked by an open item.
- **Next:** unchanged — the Noven self-audit.

### 2026-07-30 (the audit has a method — and two of the four assistants can't be checked by API)
- **Roadmap 3a's decision half is done.** Four new files in `ops/`:
  `audit-method.md` (the decisions and why), `audit-questions.md` (the question
  set), `audit-site-checklist.md` (the working checklist) and
  `audit-report-template.md` (what the client gets). Nothing has been run against
  a real business, and every time figure in them is an estimate until one is.
- **The finding that shaped everything: Microsoft Copilot has no API.** The Bing
  Search APIs were retired on 11 August 2025, and the replacement Microsoft
  points at — Grounding with Bing Search inside Azure AI Foundry — is an Azure
  project rather than an endpoint, and would measure a model we assembled rather
  than Copilot. Google's AI Overviews have the same gap. **So the four assistants
  we promise split into two groups:** ChatGPT, Gemini and Perplexity by API at
  ten questions × five runs; Copilot and AI Overviews by hand at three questions
  × three runs, labelled plainly in the report. Dropping Copilot would have been
  the tidier engineering answer and the worse commercial one — it is the
  assistant most likely to be open on a client's staff's screens.
- **Copilot's better diagnostic isn't a mention rate at all.** It answers from
  Bing's index, so if the client isn't in Bing's index it structurally cannot
  recommend them — a harder finding than any rate, and a fixable one.
- **Bands, not percentages.** Five runs distinguishes "never" from "sometimes"
  from "usually" and nothing finer. Printing "60%" this month and "40%" next
  invites a client to read chance as a decline. Four outcomes are recorded per
  run rather than two, because **"named wrongly" is worse than absent** and is
  the finding an owner reacts to immediately — an assistant confidently giving
  customers the wrong opening hours lands in a way a mention rate never does.
- **The audit checklist and the Foundation checklist are the same list**, ordered
  as the Foundation's four promises. One diagnoses, the other fixes. Nothing has
  to be translated into a scope afterwards and the client can see the report and
  the quote line up — which is most of why they believe the second one. It also
  means roadmap 3b's checklist is now largely written.
- **The audit's ten questions become the client's tracked ten.** Their first
  monthly record is then directly comparable with the audit they already paid
  for, and intake is never repeated.
- **Cost is settled and it isn't the constraint.** With the two `[PLACEHOLDER]`
  fees now confirmed — OpenAI and Anthropic both $10 per 1,000 searches — a full
  audit costs about **£1.20 in API fees at full rate, nearer £0.60 while Google's
  free allowance covers it**. About 4% of the fee. **Time is the constraint:** the
  budget is 90 minutes, and at £30 that is roughly £20 an hour, so the audit is
  honestly recorded as the qualifier for the £350 Foundation rather than as
  profitable work in itself. If it ever exceeds two hours the process is wrong,
  not the price.
- **150 API queries cannot be typed by hand** — 75 minutes of typing before a
  word of the report is written. So a small runner is the one thing that has to
  be built, and it is deliberately scheduled *after* the first audit, so it
  transcribes a format that worked rather than guessing one.
- **The first audit should be Noven's own, and it shouldn't wait for a client.**
  It times the process, closes 1e's outstanding "ask the assistants about Noven",
  captures the dated baseline 2d wants while "they've never heard of us" is still
  true, and produces a sample report we can show prospects — including the part
  where we come out badly, which is the only version worth showing.
- **Two things flagged rather than done.** Client audit records must not live in
  this repo: it is public, and a sole trader's name and address is personal data,
  which is exactly what the ICO registration two entries below attaches to — so
  storage and a retention period are now open items under 3d. And the order page,
  which doesn't exist yet, should collect a fifth field: *"what do people usually
  ask when they first get in touch?"* It is the only input we can't derive
  ourselves, and it is cheap now and expensive after the page is built.
- **Next:** run the Noven self-audit and time it. That single exercise closes the
  rest of 3a, validates the five-run count for `ops/service-tiers.md` section 8,
  and produces the first real input to 3c's Maintain hour — the number that
  decides whether this business tops out at eight clients or twenty.

### 2026-07-30 (ICO registration done — and a public register we hadn't accounted for)
- **Registered with the ICO and set up the Direct Debit.** Tier 1 at £47/year
  rather than £52, application number `C1995412`. Confirmation of the
  instruction lands within three working days. **Renews annually — the calendar
  reminder is the real deliverable**, since a missed renewal carries a penalty
  of up to £4,000 against a £47 fee.
- **The self-assessment was run first rather than paying blind**, and two of its
  questions have answers worth keeping. "Are you using personal information?"
  is **Yes** — our buyers are mostly sole traders, and the ICO's own wording
  makes information about sole traders, partners and directors personal. The
  outreach shortlist in 2b is personal information the day it's written, not the
  day someone pays.
- **"Do you use information for legal or financial services?" is No, and the
  question is a trap for us specifically.** Its hint names "accountancy and
  auditing" and "consultancy" — which reads like a description of Noven and
  isn't. The list is anchored by the heading: *financial* auditing, *legal or
  financial* consultancy, alongside credit referencing and mortgage broking.
  **Our product is called an audit but is not an audit in the ICO's sense of
  that word.** No accounts examined, no financial data held, no regulated
  activity. Answering Yes would have filed a two-person-adjacent visibility
  service under regulated services. Worth remembering: the product name is a
  false friend on official forms, and this won't be the last one.
- **Found while checking, and it's the reason this entry exists: the ICO
  publishes the registered controller's name and address on a public register
  of fee payers, downloadable in bulk.** The ICO's own guidance to sole traders
  working from home is to give a PO box or alternative address instead. The
  roadmap had the home-address risk filed entirely under the website footer —
  1a argues it at length as a one-way door — and this is the same door on a
  second front we hadn't identified, walked through while the service address is
  still unresolved. **Owner confirmed the same evening: the home address is on
  the registration.** It publishes within seven working days of payment, so the
  outside date is around Monday 10 August. Written up as the first item in 1c
  with an ordered set of steps — the time-critical one being a phone call to the
  fees helpline to hold or suppress the address, which can happen before a
  replacement address exists. Unpublishing afterwards is much the harder path,
  and does nothing about third-party copies of a bulk-downloadable register.
- **This also promotes the service address from "annoying and pending" to
  blocking two separate things**, which changes how much the V LOT failure
  costs. The ~£70/year saved by picking V LOT over an established provider is
  now measured against a published home address and a phone call to a regulator.
  Take the £115/yr fallback.
- **The general lesson, since it will recur:** every registration we complete
  from here — HMRC, insurance, anything else with a register behind it — needs
  the question "does this get published, and where?" asked *before* the form is
  submitted, not after. The service address isn't just a footer field; it's the
  address we need in hand before the next official form gets filled in.
- **Also confirmed today:** the privacy notice can be drafted free from the
  ICO's own generator (`ico.org.uk/create-your-own-privacy-notice`), which has a
  **professional services** sector variant that fits us better than the general
  business one. It's still labelled beta, downloads as Word or ODT, and is
  explicitly not legal advice. The ICO does **not** do terms of service — that's
  contract law, not their remit, and D3's existing argument against buying a
  template stands.
- **Next:** the V LOT service address looks like it may have been a scam — owner
  is picking that up tomorrow. Of the three things blocking the audit's pay
  button, ICO registration is now done; the privacy notice and the terms are
  both draftable without the address, and only the address itself is externally
  blocked.

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
