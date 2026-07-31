# Session log

**What this is:** the full record of what changed each session, what we learned,
and why each decision went the way it did. Newest at the top.

**It lives here rather than in `ROADMAP.md` so that the roadmap stays short
enough to read at the start of every session.** `ROADMAP.md` says what is true
now and what is left; this file says how we got there. Add an entry at the end
of each session, and keep the reasoning — the point of this file is that a
decision never has to be re-argued from scratch.

---

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
  in `ops/service-tiers.md` section 9. **Foundation now included with twelve
  months of Grow** — £750 free against £3,000 committed, which converts a one-off
  into a subscription without discounting the standalone price.

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
