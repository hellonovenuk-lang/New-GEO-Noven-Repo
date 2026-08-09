# Session log

**What this is:** the full record of what changed each session, what we learned,
and why each decision went the way it did. Newest at the top.

**It lives here rather than in `ROADMAP.md` so that the roadmap stays short
enough to read at the start of every session.** `ROADMAP.md` says what is true
now and what is left; this file says how we got there. Add an entry at the end
of each session, and keep the reasoning — the point of this file is that a
decision never has to be re-argued from scratch.

**Trimmed 2026-08-08, on the owner's instruction: 3,539 lines to 1,430.** The
entries kept are the ones still carrying live reasoning — a decision in force, a
condition nobody has tested yet, or an argument a live document deletes and
points here for. The rest recorded work that is finished and whose outcome is
now a fact stated somewhere else: the rename, the site build, the LinkedIn and
Zoho setup, the two earlier repricings, and the repo-maintenance sessions whose
rules now live in `.claude/skills/repo-consistency/`. **They were deleted
outright rather than archived** — git holds every one of them, and that is now
the only route to them.

**The test for a future trim, and the reason this one was safe to make:** an
entry goes when its argument is settled *and* recorded elsewhere. It stays while
anything still points at it. Before deleting one, grep the repo for a dated
reference to it — three of the entries below survive only because a live
document had its argument stripped and sends the reader here.

---

### 2026-08-09 (outreach goes cold, and the target is decided)

- **The owner has no business network. Warm-first is closed, not deferred.**
  Three documents were built on it — `HANDOVER.md` step 6 ("take the sample audit
  to three warm contacts"), `ROADMAP.md` 2c, and §7 item 3 — and all three are
  now corrected. `ops/outreach.md` is the new playbook.
- **Two decisions taken by the owner the same day: private clinics, Wirral
  only.** Dental, cosmetic, physiotherapy, veterinary. The reasoning is in
  `ops/outreach.md` §1, and the order of the reasons matters: they are almost all
  limited companies *first*, because that is a legal requirement rather than a
  preference; their customers really do ask an assistant for a recommendation
  second; the area is small enough for one assistant run to cover the whole
  market third.
- **The legal position is the load-bearing part of this entry.** Under PECR,
  limited companies and LLPs are corporate subscribers and may be cold-emailed
  without prior consent. Sole traders and unincorporated partnerships are treated
  as individuals and may not. So **the target list is filtered on Companies House
  before anyone is contacted**, and that filter builds the list at the same time.
  *Not legal advice, and `ops/outreach.md` says so where it states the position.*
- **This contradicted something already written down, and the contradiction is
  the useful part.** `HANDOVER.md` said the target buyers are "mostly sole
  traders". Cold-only rules that segment out entirely, so the buyer moves up a
  notch — which happens to suit the £700 Lead tier better than a sole trader ever
  did. The old line is corrected rather than left to be discovered.
- **Cold moved two items onto the critical path that warm would have let us
  skip.** Every cold email must carry the address for service, and there must be
  somewhere permanent to keep a do-not-contact record. So
  `business.addressForService` (£12/month, UK Postbox, has a lead time) and
  `business.clientDataStorage` now block the **first email**, not the launch. The
  privacy notice already carries the right paragraph — its "If we contact you
  first" section was written on 2026-08-09 naming legitimate interest and
  permanent opt-out recording — but it does not publish until those two values
  exist. **Worth stating plainly because it is the real cost of the change of
  plan.**
- **The pre-work method changed, and the new one is better than what it
  replaced.** `ROADMAP.md` 2b said run a mini audit on each prospect before
  contacting them. Right for warm, unaffordable cold: the self-audit's recorded
  cost was $12.63 on OpenAI alone for ~75 queries, so roughly $0.17 a query.
  **Ask the discovery questions once per trade and area instead of once per
  business.** One run produces, for every clinic on the list at once, both
  whether they were named and — the part that sells — which competitors were
  named ahead of them. About $15 for a whole batch. `ops/competitor-analysis.md`
  had already established the mechanism on our own market.
- **The email is drafted in full** (`ops/outreach.md` §5) with the reasoning for
  each choice underneath it, so a later session does not edit it into a funnel:
  competitor names are the whole email, the price goes in the second paragraph,
  it links the published self-audit rather than attaching a PDF, and there is no
  chasing sequence. **No free audits and no introductory rate** — recorded there
  as a standing rule, because a free first audit is an introductory rate wearing
  a different hat, and section 9 of `ops/service-tiers.md` settled that on
  2026-07-31.
- **Cold calling is explicitly not covered.** The email position does not
  transfer to phone calls — TPS and CTPS are a separate piece of work. Written
  into `ops/outreach.md` §9 so nobody assumes it does.
- **Capacity answered the same day, and it reframes the business.** Three hours
  a day comfortably, and materially more for a paid audit, **because one £250
  audit offsets a whole day of the owner's other earnings.** Against the
  2h40–3h30 audit budget in `ops/audit-method.md` §7 that is roughly two and a
  half times his alternative hourly rate. **So delivery is not the constraint —
  finding buyers is**, which is the opposite of what the capacity question was
  asked to find out and is worth remembering the next time someone proposes
  building product instead of selling.
- **Batch size falls out of it: twenty a week**, with one stop rule — do not
  send batch two while batch one has more than four audits still owed. Six
  audits a week is the ceiling, four without stretching. **The binding
  constraint turns out to be the size of the list, not the diary**, and the
  answer to running out of prospects is to widen the area (Liverpool and Chester
  were the runners-up) rather than to send more per week.
- **The address for service is ordered and pending approval**, told to us by the
  owner: placed Friday 7 August, ID verification in flight, confirmed address
  expected Monday 10 August. Marked as pending in four places rather than one —
  `HANDOVER.md` step 2, `ROADMAP.md` 2b, `ops/third-party-services.md` B1b and
  `ops/outreach.md` §2 — because "ordered" and "confirmed" are the same word to a
  reader skimming for a blocker, and **it is confirmation in writing that
  unblocks the footer, the structured data, the terms, the privacy notice and
  every cold email.** Steps 5 to 9 of the B1c runbook are still owed after it
  lands.
- **The mention-counting method already existed and had been run once — it just
  had not been written down as a method.** `ops/competitor-analysis.md` Part 2
  counted 41 businesses across 165 opportunity rows and produced a ranked table
  with a per-assistant split. `ops/outreach.md` §4 now carries it as a repeatable
  procedure, with the detail that matters: **the `competitors` column was empty
  on the export, so the counting was done by matching names against
  `answer_text`** — and for outreach that is the better route anyway, because
  **the Companies House list is the candidate name list**. We are not discovering
  who exists, we are checking which of a known set got named.
- **The new half is the complement, and it is the actual targeting method.**
  Named businesses subtracted from the Companies House list is the prospect pool.
  **But "not named" will be the normal condition** — the self-audit's own Wirral
  question returned five businesses where the national one returned forty-one, so
  on a local trade question the great majority of a list is invisible and absence
  distinguishes nobody. So prospects are sorted by **how close they are to
  appearing**, using `sources_cited`, which the run already captures:
  - **Tier A, in the cited sources but not in the answers.** The best prospects,
    and the finding this business exists to produce: they have already done the
    obvious thing and it did not work. Anyone can tell a clinic to get listed;
    telling them they *are* listed on the page the assistant reads and it still
    names three competitors is a fact nobody else has.
  - **Tier B, named occasionally.** A measurable gap rather than an absence.
  - **Tier C, absent from everything.** Real, but their first fix is cheap enough
    that they may not need us for it.
  - **Named consistently: not a prospect.** Nothing to sell them, and the audit's
    own voice is "you don't need us".
- **The trade run is built: `ops/trade-run/`.** The owner asked whether we were
  ready to fire the API calls for "dentists in Wirral". Nearly — and the gap was
  smaller than expected, because **the self-audit's "throwaway" script was
  already reusable**. It takes `--questions`, `--out`, `--cap`, `--smoke`, has a
  hard query cap checked before the first call, and resumes after a provider
  failure. Three changes made: the client name and the run count became flags
  (they were hardcoded to `"noven"` and to the self-audit's five-vs-ten
  experiment), and the defaults suit a trade run. **The original in
  `ops/audits/noven-2026-08-02/` is frozen and was not touched** — it is part of
  that audit's record.
- **Its docstring said "delete this file after the audit — do not maintain it",
  and that instruction was wrong.** Worth recording rather than quietly ignoring:
  the script was written crude on purpose so its rough edges would specify the
  real runner, and the rough edges turned out to be two hardcoded constants. The
  deferral of the actual audit runner (`ROADMAP.md` 3a) is untouched — a trade
  run is prospecting, not a paid audit, and this does not guess at the runner's
  spec.
- **Six questions written for Wirral dentists**, three discovery, one qualified,
  one buying intent, one comparison, on the frame in `ops/audit-questions.md` §1.
  6 × 3 assistants × 5 runs = **90 queries in one command**.
- **Smoke-tested against its own guards, not against the APIs.** The cap check
  fires before the first call and exits having spent nothing; the missing-key
  guard exits cleanly; the header is written correctly. **No API call has been
  made.** Two things are open and both are recorded as `[PLACEHOLDER]` rather
  than assumed: **what is left on the three API balances after 2 August is
  written down nowhere**, and whether Python is installed on the owner's Windows
  machine. The run is about $15, which is a spend inside the freeze window and
  therefore the owner's call.
- **The run stops at raw answers on purpose.** `outcome` and `competitors` are
  written empty, because classifying them is the judgement the audit budgets 60
  to 110 minutes for. A second script to build the mention table is deliberately
  not written until we have seen what a real trade run's answers look like —
  the same reasoning that defers the runner, applied to the same trap.
- **`ops/trade-run/`, not `ops/outreach/`.** A folder and a file with the same
  name sitting beside each other is a trap for the next reader, and the repo
  already has `name-check/` and `site-check/` as the pattern for a tool folder.
- **The API balances are known for the first time since 2 August**, given by the
  owner: **OpenAI $16.00, Gemini £8.95, Perplexity $4.49.** Recorded in
  `ops/accounts.md`, which had been carrying "the totals were never recorded" as
  an open gap since 4 August.
- **The verdict is two yes and one short, and the reasoning is worth keeping
  because it will be reused for every trade run.** One run is **30 queries per
  provider**, not 90. **There is exactly one measured rate in this business** —
  OpenAI at $12.63 for ~75 queries on 2 August, about $0.17 a query — so all
  three were priced at it and the borrowing was declared rather than hidden.
  OpenAI has roughly three runs of headroom; Gemini is comfortable and grounded
  search is normally cheaper than this; **Perplexity is short by about fifty
  cents at the borrowed rate.** Sonar is genuinely cheaper than OpenAI web
  search, so it may well cover it, and "may well" is not a balance check.
- **The smoke test was already the required first step; it is now also the
  measurement.** Three queries, one per provider, then read the three dashboards
  and divide. About fifty cents to convert three borrowed estimates into three
  measured per-query rates — **a number this business has needed since 2 August
  and has never had**, and one that also feeds the open £150 Maintain question
  in `ops/plan-to-1-september.md`.
- **Running dry costs nothing, which is what makes it safe to just try.** The
  providers run OpenAI, then Gemini, then Perplexity, so an exhausted Perplexity
  balance fails last with sixty rows already flushed to disk, and re-running
  retries only the errored rows. The downside is a $5 top-up and one repeated
  command.
- **The balance is not the thing to check first.** `ops/audit-setup.md` §4 says
  to set £10 caps on all three and turn Perplexity's auto top-up off, and
  **neither has ever been confirmed**. With auto top-up on, "is there enough"
  stops mattering — running dry silently charges the card, which during a
  spending freeze is the exact event the freeze exists to prevent. Flagged in
  `ops/accounts.md` and in the trade-run README rather than only here.
- **The owner asked whether the £12/month address could be skipped entirely, and
  the honest answer separated two things the documents had tangled.** `B1` said
  the address was a legal disclosure requirement, which is true, and left the
  reader to infer that a *virtual* one was required, which is not. **The
  business-names duty asks for an address where documents can be effectively
  served, and a home address satisfies it completely.** The site could be fully
  compliant tomorrow for nothing. **The £144/year buys privacy, not compliance**,
  and `ops/third-party-services.md` B1 now says so.
- **Kept anyway, and the reason is specific to this business rather than
  general.** The address goes in the footer of every page, in the Organization
  structured data as a machine-readable `PostalAddress`, in the terms, in the
  privacy notice and in every cold email. **This site is built to be maximally
  readable by AI crawlers, and the business exists because those systems absorb
  and repeat what they find.** Publishing a home address into them is a worse
  trade here than almost anywhere else, and it is not reversible for the same
  reason the register's copies are not.
- **The asymmetry is the thing to remember.** A public register is passive
  listing; a crawled website and a few hundred cold emails are active
  distribution. **Being relaxed about the first does not imply being relaxed
  about the second**, and the same evidence does not cover both.
- **Two ICO calls, not one.** Tomorrow's is about the trading name. The second
  goes in once the service address exists, because asking them to change the
  record to an address that has not arrived is pointless and runbook step 8
  assumes it is in hand.
- **The ICO address panic is downgraded, and the owner was right to push on it.**
  `HANDOVER.md` §4 treated the 10 August publication of the registered address as
  close to an emergency. The owner's argument: home addresses are ordinary for
  sole traders, and his does not obviously read as one. **Checked rather than
  accepted — Companies House advanced search returns 281 active companies with a
  registered office in that Birkenhead square.** It reads as commercial to a
  human and to a scraper. The exposure is real and permanent, because
  bulk-downloadable data gets mirrored and amending the ICO's record does nothing
  about copies, but **it is low-impact and it is not the thing that should be
  stopping everything else.** §4 and the dates table are rewritten.
- **The call still happens tomorrow, for a better reason the owner half-spotted:
  the trading name on the record.** He is not sure whether it was filed as
  "Noven". If it was, that is not a privacy problem — **it is a published-fact
  problem.** `/privacy/` prints registration C1995412 and invites the reader to
  check it against the ICO's own register, precisely because a business selling
  verifiable facts should hand them over. **A reader who checks and finds a
  different name has found the exact fault this business is sold to detect in
  other people's businesses.** Suppression drops to third on the call, behind the
  name and the coming address change.
- **The ICO register could not be checked from a session — it returns HTTP 403 to
  automated fetches.** Recorded as unverified rather than assumed either way.
- **The owner's home locality is deliberately not written into this repo**, only
  the fact that the address is shared with hundreds of registered businesses.
  Same reasoning as the practice names: this repo is written as though public.
- **Client records live in Microsoft OneDrive. Decided by the owner 2026-08-09**,
  closing the last open item in `ops/client-record.md`. Office is already paid
  for, so no new supplier and no cost; the `.docx` audit masters live there
  natively rather than being moved by hand; and version history gives a restore
  that can actually be tested, which a new account could not have offered for
  weeks.
- **The decision named the provider and stopped there on purpose.**
  `clientDataStorage.where` is a `[PLACEHOLDER]`, because **the privacy notice
  states the country in published wording and it is not a fact to assert from
  general knowledge** — Microsoft's answer depends on the account and the
  tenant's configured residency. It is two minutes to check in the account. A
  first draft of this entry had a confident country in it and it was wrong to
  write; `CLAUDE.md`'s rule about inventing facts applies hardest to the
  sentences that are about to be published.
- **So the gate in `legal.ts` was tightened to match.** `privacyLive` previously
  read `clientDataStorage !== null`, which would have published a notice naming
  a supplier and saying `[PLACEHOLDER]` where the country goes. **It now checks
  the string as well as the object.** Site rebuilt: nine pages, `/privacy/`,
  `/terms/` and `/order/` all still correctly absent.
- **The emails' closing ask was wrong twice, and the owner caught both.** Both
  drafts ended by offering to send "the six questions I'd ask about [practice]".
  **Nobody wants six questions** — it is an artefact from our side of the desk,
  offered as though the recipient would value it. And **it named a thing that
  does not exist**: the audit is a ten-question frame (`ops/audit-questions.md`);
  six was the trade run's number. The line survived from a draft written before
  the run existed, which is how a stale detail gets carried into copy nobody
  re-reads from the recipient's side.
- **The replacement is the one thing they would actually want: the answers.** We
  hold ninety of them. A practice owner reading the verbatim text where three
  competitors get recommended and they do not is a stronger pull than any offer
  we could construct, it costs nothing to send, and **it stays inside the
  give-away rule because it is observation rather than diagnosis.** The source
  list is stripped before sending — the sources are the diagnostic clue and they
  belong in the paid report.
- **`ops/voice.md` added, from `github.com/blader/humanizer`, on the owner's
  instruction and explicitly as a general framework rather than a checklist.**
  It applies to everything a customer reads and to nothing in `ops/` —
  the operating documents are read by the assistant far more often than by a
  person, and their reasoning is worth more than their rhythm. `CLAUDE.md` gains
  a three-line pointer rather than the whole list.
- **The owner's diagnosis of the first two emails was sharper than the source
  material.** He said the subjects read as "an automated AI company you've
  probably had thousands of emails from" rather than a new small business from
  the Wirral. **The cause was structural rather than lexical: both emails opened
  with the finding.** That is how automated outreach is built, because a template
  has no self to introduce. A person says who they are first.
- **So the top of `voice.md` is one structural rule, above the word-level list:
  say who you are before you say what you found.** And its corollary for subject
  lines: **a subject that makes a claim reads as a campaign, a subject that names
  the thing reads as a person.** "[Practice] and ChatGPT" against "[Practice]
  doesn't come up on ChatGPT". **That single change did more than every
  word-level edit put together**, which is worth recording because the temptation
  with a list of 33 tells is to work the list.
- **Both drafts rewritten.** Introduction first, plainer register, the em dashes
  and the rule-of-three rhythms out, "It's £250 and that's the whole cost"
  instead of the three-clause marketing beat. **The give-away rule survived the
  rewrite** — "which one it is I'd have to look at properly" keeps the diagnosis
  inside the paid work without implying we know less than we do.
- **The owner caught a real gap in the outreach method and it is now a rule:
  the observation is free, the diagnosis is the product.** A first draft of
  Draft B told the prospect *why* they were missing — that the answers are built
  from directory pages they are not on. **That is the finding they would be
  paying £250 for, given away in a sentence**, and it was written that way out of
  a reflex to be maximally forthcoming rather than any reasoning.
- **Why this is not a dishonesty question, written down because it will be
  re-argued.** "You were named in none of ninety answers" is true and complete on
  its own terms. Declining to add "and I think I know the reason" withholds
  nothing the reader was promised and states nothing false. **The site's voice is
  *you don't need us for everything*, not *here is the work for nothing*.** What
  goes in the email is observation — what was asked, how often, who got named,
  whether they did. What stays in the report is diagnosis.
- **Two guardrails were attached, because the rule has a failure mode in each
  direction.** **Never imply we do not know** — "there are a handful of reasons"
  is honest, feigned puzzlement is not, and vagueness about our own knowledge is
  the line. And **the audit has to be worth £250 without that finding**: ten
  questions on their business, what the assistants believe about them and whether
  it is true, their own site. **If a report ever reduces to "get listed on a
  directory", the price is wrong rather than the customer.**
- **The same rule generalises to the market-level findings.** How the answers are
  built on the Wirral is known because ninety queries were paid for and analysed.
  It is an asset: it belongs in client reports, not in cold emails and not on the
  site.
- **The email draft is rewritten on the run, and it is now two drafts.** The
  single letter could not honestly address both problems the data found.
  **Draft A** for a practice named by one or two assistants and missing from the
  rest — eighteen of thirty-nine are in that position, and the letter leads with
  the count. **Draft B** for a practice named by none, whose problem is bigger
  and plainer: they are absent from the directory pages the answers are built
  from, which is the cheaper end to fix and partly free. **The instruction not to
  claim the assistants disagree in general is written in next to the drafts**,
  because that is the mistake a future session would make from memory of the
  smoke test.
- **The full run landed the same evening: 90 rows, zero errors, zero empty
  answers, sources on every row, all three model strings correct.** The balances
  covered it — Perplexity finished, so the fifty-cent shortfall predicted from
  OpenAI's borrowed rate did not appear. **Check 5, the actual per-query cost,
  is still owed from the dashboards.**
- **Two of the four smoke-test findings were wrong, and the owner's instruction
  to wait is what stopped them reaching an email.** Recorded at length in
  `ops/trade-run/README.md` rather than quietly amended, because the correction
  is the more useful record:
  - **"Not one practice was named by all three assistants."** False. 39
    practices were named and **21 of them by all three**, 12 by two, 6 by one.
    **Consensus is the normal case.** Three single runs were read as a market
    structure when they were sampling noise.
  - **"Tier A is populated"**, with a named example. That example is named 18
    times at 90 rows. The tier exists but had to be found a different way.
- **What actually holds, and it is still a good story.** A **top tier of four at
  36–43% of rows** — more concentrated than the national field, whose leader
  managed 28%. **But no incumbent above it:** the leader is missing from a clear
  majority of answers. And the finding that sells, once stated per practice
  rather than in general: **18 of the 39 named practices are missing entirely
  from at least one assistant**, including some in the top ten. Strong on
  ChatGPT and absent from Perplexity is common, and nobody knows it.
- **The email's central claim is rewritten on this.** "The assistants disagree"
  is checkable in five minutes and would not survive. *"You come up on
  Perplexity, you do not come up on ChatGPT at all, here are the three that do"*
  is true of eighteen practices, checkable, and known to none of them.
- **4,902 source URLs. 345 are Gemini's opaque redirects — 7% of the total and
  100% of Gemini's**, so Finding E's limitation is unchanged rather than eased.
- **ThreeBestRated is cited in 20 of 90 rows — third independent confirmation.**
  It lists three Wirral practices and **all three are named by the assistants.**
  Free to join. **It is now the single most evidenced action in the business.**
- **Reddit is cited in 30 of 90 rows, more than any single directory.** Mostly
  r/Liverpool and r/Wirral recommendation threads. `ROADMAP.md` 2f holds Reddit
  as an owner's decision rather than a default; **this is the evidence that
  decision was waiting for.**
- **How Tier A is actually found, which is a method the audit gains.** A cited
  URL is usually a directory *page* listing many practices, so absence from the
  URL list proves nothing. **Fetch the cited directory pages, read who is on
  them, cross-reference against the mention table.** Two fetches produced the
  tier immediately. That is a fourth question the audit can answer for a client
  at no cost: *which of the pages feeding the assistants are you on, and is it
  working?*
- **arXiv preprints appear in 30 of 90 rows, from one assistant, irrelevant to
  every question.** Retrieval noise, no effect on the counts. Recorded so nobody
  investigates it twice.
- **The Companies House sweep is done for dental, and it can be done from a
  session rather than by hand.** Advanced search takes a SIC code and a postcode
  district in a plain URL — no account, no API key, thirteen fetches for the
  whole Wirral. **67 active limited companies on SIC 86230.** Method and the
  per-district counts are in `ops/outreach.md` §3; **the names are not in the
  repo**, same rule as the run data, and the CSV went to the owner directly.
- **86230 is now confirmed by evidence rather than memory** — every district
  returned dental businesses. The other four SIC codes are still unchecked and
  the doc says so.
- **67 companies is not 67 prospects, and the gap is the work.** Three things
  have to come out, all visible in the raw data: **personal service companies**
  (a dentist invoicing through their own limited company from somebody else's
  chair — 17 rows flagged, no practice to make visible, not a prospect);
  **suppliers, labs, training providers and referral services**, which share the
  SIC code and are not patient-facing; and **shared registered offices — 22 of
  the 67**, four companies at one postcode in three separate cases. That last one
  is the accountant's-address trap the doc already warned about, now measured.
- **The list is a floor, not a census.** A practice trading on the Wirral but
  registered at an accountant's office in Liverpool does not appear at all.
- **The binding constraint arrived earlier than expected.** §7 predicted the list
  would run out before the diary did. On the dental number, **one trade does not
  sustain a twenty-a-week batch for long** — so the other three trades' sweeps
  are not optional extras, they are what keeps the batch fed.
- **The smoke test ran at 17:08 UTC and passed all five checks.** Three queries,
  q01, one per assistant. Search fired on all three; model strings came back as
  the intended tiers; every answer was UK-shaped; the CSV survived with its
  multi-line answer text intact. **Check 5, the cost, is the one still
  outstanding** — the per-query rates only exist once the three dashboards are
  read.
- **The geographic-word rule is confirmed live, and it was written down the day
  before it was tested.** `ops/audit-setup.md` §8a recorded on 2 August that
  Gemini's grounding tool has no locale parameter and cannot be fixed. q01 names
  the Wirral, and **Gemini returned seven Wirral practices by name and by town.**
  A place name in the question does what the missing parameter cannot, which
  means Gemini's answers are usable in a trade run rather than discounted. First
  evidence either way since the limitation was found.
- **The owner held the analysis at the smoke test, and was right to.** The setup
  checks are conclusive from three rows — a search either fired or it did not.
  **The market claims are not**, and they were written up in language that
  outran the sample: the national version of "no incumbent" rests on 165 rows and
  this rests on three. Both documents now carry the sample size in the first
  line of the section rather than in a footnote, and neither claim goes into an
  email or a client report before the full run.
- **A live gotcha found while re-reading the script for this: the smoke rows
  will be skipped rather than replaced.** `load_done` keys on assistant plus
  question plus run number and skips anything that succeeded — and the smoke rows
  *are* q01 run 1 on each assistant, with no error. A full run against the same
  file leaves three rows tagged "delete this row" standing in for real data, and
  the mention table would count them. **Delete them first.** In the README now,
  with the reason rather than as housekeeping.
- **The finding that changes the product pitch: the three assistants barely
  agree.** One question, one run each, **roughly a dozen distinct practices named
  across the three answers and not one named by all three.** Two appeared twice,
  everything else once. This is `ops/competitor-analysis.md` Finding A repeating
  on a completely unrelated market — **no incumbent, even locally, even in a
  field this small.**
- **So the email's central claim should change, and the §5 draft now says so.**
  "You are not mentioned" is the weak version. The strong version is *"you are
  the top recommendation on one of these and absent from the other two, and here
  is which"* — specific, checkable, and unknown to the prospect because nobody
  checks all three. The draft was written before there was evidence for the
  better claim; rewrite it when the full run lands.
- **ThreeBestRated was cited again, by two of three assistants, on a question
  with nothing to do with our own market.** It was already the one open door in
  Finding F. **Two independent questions, two assistants each — it stops being a
  curiosity and becomes a lever**, and it belongs in the audit deliverable as a
  concrete action rather than only in our own list.
- **The answers are built from directories and Reddit, not from practice
  websites.** CQC, NHS service search, Yell, WhatClinic, ThreeBestRated, a long
  tail of dentist-listing sites, and a striking volume of r/Liverpool and
  r/Wirral threads. Practice sites appeared, but as confirmation after a
  directory supplied the name. **Consistent with Finding B's listicle mechanism,
  and it puts Reddit back on the table** — which `ROADMAP.md` 2f still holds as
  an owner's decision, not a default.
- **Tier A was populated in three queries.** Several practices appear in the
  cited directories and in no assistant's answer — listed on the exact pages the
  assistants read, and still not recommended. The ladder's top tier is real
  rather than theoretical, found on one question rather than ninety.
- **No practice names are recorded anywhere in this repo, and that is the rule
  rather than an oversight.** A list of named local dental practices, in a repo
  written as though it were public, is the comparison the owner parked on
  defamation grounds. **The rule applies to our own working notes, not only to
  published pages.** The findings above are all shape, not names.
- **`.claude/settings.json` added, and it is deliberately two lines long.** The
  owner asked how to stop the permission prompts. Scanning the session's actual
  tool calls, **almost everything that recurs is already auto-allowed and never
  prompted at all** — `sed`, `head`, `grep`, `tail`, `ls`, `wc`, and every
  read-only `git` subcommand. Exactly one recurring command was both prompting
  and safe to pre-approve: **the consistency checker**, run 15 times in one
  session because `CLAUDE.md` tells every session to run it. It is verified
  read-only — opens one config file, no writes, no subprocess, no network.
- **`.claude/settings.local.json` is now gitignored, and the distinction is
  worth keeping.** `.claude/settings.json` is the shared allowlist, committed and
  reviewable in a pull request like any other decision. The `.local.json` beside
  it is whatever "don't ask again" recorded in one terminal on one machine, and
  it should never arrive in a pull request dressed as a decision.
- **One correction worth recording, because it will be assumed again.** Running
  the allowlist skill does not make Claude Code *learn* from chat history. It is
  a one-off scan that writes static rules to a file. What persists across
  sessions is the file — nothing watches the conversation and adapts.
- **What was deliberately left out, because the reason matters more than the
  list.** `git add`, `git commit` and `git push` prompt seven times each in a
  session and none of them is on the allowlist: they change the repository, and
  `push` publishes. **A wildcard on `python3` was also refused** — it is
  arbitrary code execution wearing a script's clothes, and in this repo it would
  cover `trade_run.py`, which spends real money on API calls. The rule that
  produced both: pre-approve a *named* read-only script, never an interpreter.
- **The owner's local Claude Code terminal had neither git nor the keys, and
  that is one cause rather than two.** Claude Code on Windows runs its shell
  through Git Bash, which arrives with Git for Windows — with git missing, the
  shell is not the one any of these instructions assume, so variables set in a
  PowerShell window are invisible to it. Written into
  `ops/trade-run/README.md` as "Setting up the machine", with the three
  one-line checks that tell you which of git, Python and the keys file is
  actually absent.
- **The keys most likely already exist.** `ops/name-check/README.md` loads the
  same three keys from `$HOME\.noven\env.ps1`, so if the name check was ever run
  on that machine the file is there and needs dot-sourcing, not recreating.
  **That file keeps the old name deliberately** — it is private to one machine,
  nothing published reads it, and renaming it silently breaks the name-check
  runbook. Same reasoning as `hello.noven.uk@gmail.com` in
  `ops/rename-to-wardith.md` F10.
- **The script's own error message was wrong on Windows** — it said
  `source ~/.noven/env`, which is not how that machine loads it. It now names
  the PowerShell form and points at the README. A setup instruction that is
  wrong on the only machine it runs on is worse than no instruction.
- **Python from `python.org`, not the Microsoft Store**, and tick "Add
  python.exe to PATH". The Store build sandboxes file access in ways that break
  a script writing outside the user profile, which is exactly what `--out` does.
- **A design rule fell out of the smoke-test history, and it is worth more than
  the run it was found for.** `ops/audit-setup.md` §8a records that Gemini's
  grounding tool has no location parameter at this access tier, cannot be fixed,
  and skews non-UK **specifically on questions carrying no geographic word of
  their own**. Every question in the dentist set names the Wirral, Birkenhead or
  Wallasey — which is what a real customer would type anyway. **Written into
  `ops/trade-run/README.md` as a rule for every future trade question set**,
  because it is the kind of property that survives one file and gets lost on the
  first copy-paste.
- **Source analysis is two assistants, not three**, wherever the ladder is used.
  Gemini's cited URLs are all opaque `vertexaisearch` redirects (Finding E), so
  every conclusion about *why* a business is named rests on ChatGPT and
  Perplexity. This is the third document now carrying that limit, and the
  method-doc fix it implies is still open in `ROADMAP.md` 2f.
- **The ladder is never published.** A ranked table of named local clinics is the
  public comparison the owner parked on defamation and comparative-advertising
  grounds. Written into `ops/outreach.md` §4 next to the ladder itself rather than
  left in `competitor-analysis.md`, because that is where someone will be looking
  at a ranked table and thinking it would make a good page. **Naming a prospect's
  competitors privately to that prospect is a different act from publishing a
  league table**, and only the first is in scope.
- **Two things the arithmetic exposed rather than settled**, both recorded in
  `ops/outreach.md` §7 so they are met at the point they matter:
  - **No audit has ever been timed.** 2h40–3h30 is a budget, and the
    classification step inside it — 60 to 110 minutes — has no prior estimate at
    all. Every capacity number above is arithmetic on an estimate until the
    Wardith run is timed.
  - **Four audits a week is when the runner stops being deferrable.** Deferring
    it was right and stays right — written before the first audit it is a guess
    at a specification — but the only thing that fires the queries today is a
    script marked throwaway, and the deferral's release condition is the first
    real audit, which is what the outreach exists to produce.

---

### 2026-08-09 (the terms of service and the privacy notice — written, and switched off)

- **Both documents are finished, and neither is a draft.** `/terms/` and
  `/privacy/` are written in the site's own voice, not assembled from a
  template, and they publish when two facts exist.
- **The mechanism changed, and it is the more important half of this entry.**
  `business.addressForService` is now a real value in `business.ts`, typed as a
  `PostalAddress`. Setting it does five things from one edit: fills the footer
  line, adds `address` to the Organization JSON-LD, publishes `/terms/`,
  publishes `/privacy/`, and — with the Revolut link — opens the order page.
  This closes the note left in `schema.ts` on 2026-08-06 the way that note asked
  for: the visible address and the machine-readable one are now built from one
  value and cannot drift.
- **`/privacy/` needs one more fact than `/terms/` does:** where client records
  live. The notice names who holds the data, and that decision is still open in
  `ops/client-record.md`. So the storage question now blocks a page rather than
  just being untidy — which is the honest position, and gives it a deadline.
- **This replaced the `import.meta.glob` file-existence check** added earlier the
  same day. Once the two pages exist as files, "does the file exist" stops being
  the interesting question and "will it build" starts being it. `order.ts` is
  shorter for it and now imports `termsLive` / `privacyLive` from `legal.ts`.
- **Retention is decided rather than recommended:** enquiries twelve months,
  client records the relationship plus twelve, do-not-contact permanently.
  **Invoices were never ours to decide** — tax law requires at least five years
  after the relevant 31 January deadline, and the notice says so instead of
  implying we could delete them on request. Three documents had been carrying
  this as a recommendation; it is now published wording.
- **Two disclosures no generated privacy notice would ever contain**, and they
  are why this was written by hand:
  - **An audit works by asking other companies' assistants about the client.**
    Their business name and website are typed into OpenAI, Google, Perplexity
    and Microsoft systems. For a sole trader trading under their own name that
    is personal data, and it is said plainly.
  - **This site loads its fonts from Google**, which gives Google every reader's
    IP address before they have clicked anything. Disclosed. **The better answer
    is to self-host the two typefaces** — about an hour, removes the third-party
    request, marginally faster page. Recorded in `third-party-services.md` D2.
    Until then the notice tells the truth about it.
- **The terms were checked line by line against the pricing page, the FAQ and
  how-it-works**, because D3 warns that a template would contradict all three at
  once: no minimum term, no guaranteed outcomes, we don't build websites, no
  part-month refunds. Liability is capped at fees paid over the preceding twelve
  months, with the statutory carve-outs that cannot be limited.
- **The ICO's generator is still worth running**, not as the source of the
  notice but as the regulator's own checklist to read beside it. D2 amended to
  say so rather than deleted.
- **Not done:** nobody with a legal qualification has read either document. That
  is the owner's call, and it is cheap insurance on the two pages a dispute
  would be argued from.

### 2026-08-09 (the order page and the Revolut hand-off — built, and switched off)

- **What was asked:** get the Revolut payment link onto the website, do
  everything possible in code, and come back with a short list of what only the
  owner can do.
- **Everything in code is done. Nothing is public.** `/order/` (the six-field
  form) and `/order/pay/` (the Revolut button) exist behind a switch in
  `site/src/data/order.ts`. Verified both ways: with the switch off the build
  produces the same nine pages as before and the sitemap is unchanged; with it
  on, eleven pages, `/order/` in the sitemap, `/order/pay/` `noindex` and
  excluded.
- **Why a switch rather than an unmerged branch.** The blockers are the terms,
  the privacy notice and the address for service, and none of them is a coding
  job. A branch left open would have made the code the thing that was waiting;
  the switch makes the documents the thing that is waiting, which is true. It
  also means this can merge and sit on `main` doing nothing until it is wanted.
- **Two of the four conditions check themselves.** `termsPublished` and
  `privacyPublished` are not booleans somebody has to remember to flip — they
  are true when `/terms/` and `/privacy/` exist in `src/pages`. A payment form
  that links to a 404 is the worst possible broken link, and this makes that
  state unreachable rather than merely unlikely. The payment link and the
  address line are set by hand; the address one cannot be derived, because it is
  a fact about the rendered footer rather than a file.
- **The form is a Netlify form, which is a data-protection fact, not a technical
  one.** Submissions sit in Netlify's dashboard before they reach the inbox, so
  Netlify is a processor and the privacy notice has to say so. Recorded in
  `ops/accounts.md` and `ops/third-party-services.md` C2 as well, because
  whoever writes that notice will not be reading this file.
- **Spam defence is a honeypot field and nothing else.** The alternative Netlify
  offers is reCAPTCHA, which would put Google's JavaScript on a site whose whole
  argument is that it ships none.
- **The footer's "order the audit" ask is suppressed on both order pages.**
  A button back to the order form, shown to someone halfway through paying, is a
  repeated call-to-action of exactly the kind the design rules ban.
- **`repo-consistency` was reporting 142 errors, all of them false.** Its
  skip-list tested `startswith("node_modules/")`, and this repo's dependencies
  are at `site/node_modules` — so the moment a session runs `npm install`, the
  checker starts reading Vite's licence files and the stale prices in
  `site/dist`. Now matched on any path segment. Back to 0 errors. **This was
  invisible until now only because no previous session had installed the site's
  dependencies and then run the checker.**
- **Not done, and deliberately:** the terms of service and the privacy notice
  themselves. They are the blocker, they are a day's desk work, and drafting
  them uninvited would have buried a payment-page diff under two legal
  documents. Offered to the owner as the next piece of work.

### 2026-08-09 (the humanisation and voice pass — the final copy edit before launch)

- **The brief:** the structural and visual passes were settled and out of scope.
  This one asked a single question of the existing copy — what still reads as
  machine-written? — with an explicit standard of restraint: a sentence that
  already sounds natural, precise and like Wardith gets left alone.
- **No Humanizer skill exists in this environment or on the account.** The brief
  named one as the diagnostic framework. It was searched for and is not
  installed. The brief's own section 3 enumerates the pattern list in full, so
  that list was used instead. **If a future session is told to "use the
  Humanizer skill", it will not find one — do not spend the budget looking.**
- **The finding was one dominant tell, and it was measurable.** Em dashes ran at
  12.8 per 1,000 words across the site. Edited human prose runs about 2–5. The
  specific construction was `— and` (20 instances site-wide) and `— so` (6): a
  clause tacked on after a pause, which is the "claim — qualification —
  conclusion" rhythm. The site is now at 8.3 per 1,000, and the pages still
  above that are the ones that should be — the reproduced self-audit report,
  which is a record and was not touched, and the pasteable prompts on
  `/ask-your-ai/`, which are an instrument rather than prose.
- **Em dashes were assessed individually, not banned.** The ones carrying a real
  beat were kept, deliberately: "228 recorded answers — and we failed", "No —
  and nobody honestly can", "The rest aren't ranked lower — they're not in the
  answer."
- **How it works was over-corrected and then partly put back.** Cutting every
  flagged dash took it to 1.2 per 1,000, which made it read noticeably drier
  than the pages either side of it. One was restored. **Uniform absence is its
  own tell** — the target was natural frequency, never zero.
- **Three consecutive `X, not Y` list headings on `/ask-your-ai/` were the
  clearest house pattern after the dashes.** "A range instead of a roll of the
  dice" / "A stranger's view rather than your own" / "The reason, not just the
  result". The strongest was kept and the other two flattened to plain noun
  phrases. The technique survives; the pattern doesn't.
- **Two manufactured slogans went.** Pricing's "staying visible is maintenance,
  not magic" (alliterative, advert-shaped) became "ongoing work". The About
  statement's "One person, one focus, and a written record of everything
  promised" was a forced rule of three whose middle beat meant nothing.
- **Deliberate duplicates were broken up.** "Every stage has to earn the next
  one" appeared verbatim on the homepage and as the how-it-works statement; the
  homepage copy was cut so the statement keeps it. "A sales call with a document
  attached" appeared on both the homepage and pricing; pricing keeps it, where
  it answers the "why does it cost £250" question.
- **What was protected, and checked afterwards:** every price, the two-working-day
  turnaround, the no-minimum-term structure, the published self-audit numbers
  (228 / 168 / 30), the scope language, and all of the transparency copy — the
  audit that concludes you don't need us, the refusal to guarantee, the absent
  case studies, the failed self-audit, the promise to publish future audits
  whatever they say.
- **Structured data was diffed before and after and is byte-identical**, with one
  intended exception: a single FAQ answer, because the visible copy and the
  `FAQPage` JSON-LD are built from the same array and are supposed to move
  together. Titles and meta descriptions are unchanged.
- **The specificity rule held.** "Google Business Profile, Bing Places, Companies
  House…" appears near-verbatim on three pages and reads as templated, but the
  detail is the value and each instance sits in a different context. Flagged to
  the owner rather than thinned.

---

### 2026-08-09 (the visual communication pass — three diagrams, and the rejections)

- **The brief:** the structural and copy review was already done and the site's
  hierarchy, positioning, pricing and CTAs were treated as settled. This pass
  asked one question only — where does a picture explain something faster than
  the prose already does? — with an explicit expectation of three to five
  additions across the whole site, and fewer if fewer are justified.
- **Three built, and one presentation change.** Homepage: a figure showing the
  same ten businesses on a results page and in an assistant's answer, seven of
  them emptying out. How it works: a stage ladder whose branches are the exits,
  so "every stage has to earn the next one" is visible before the reader has
  read nine hundred words rather than after. Self-audit: the "who gets
  recommended instead" table redrawn as bars, with Noven's own row at zero
  underneath the ten. Pricing: the JSON block folded into a `<details>`.
- **What was rejected, and why — these are settled, don't re-open them
  without a reason.**
  - *A journey diagram on Ask your AI.* The brief raised it. The page's whole
    argument is already in its section headings, one screen apart, and the
    hero says "Don't take our word for it" in six words. A four-box flow would
    have restated headings the reader can already see, which is decoration.
  - *A figures strip on Ask your AI* (228 answers / 0 in 168 / 30 of 30). Every
    number real, but the self-audit page one click away now carries the visual
    treatment of the same evidence. Twice is once too many.
  - *Redrawing the seven-question "never (0 of N)" table on the self-audit.* The
    twenty-one identical cells **are** the finding, and the run counts (0 of 10
    against 0 of 5) are real information a mark would lose. Left alone.
  - *Anything on About or FAQ.* About is short and personal; a Q&A is already
    the most scannable form there is, and its markup feeds the FAQPage schema.
- **The homepage record panel stays open and animated.** It was reviewed under
  the same question and kept: on that page the code *is* the subject of the
  section. The pricing block is different — there the sentence is the argument
  and the code is the proof, so it now sits one click behind it. Both pages'
  actual JSON-LD is untouched either way; folding a visible block changes
  nothing a machine reads.
- **Net page height across the four changed pages is +220px on about 25,000** —
  the diagrams cost roughly what the folded JSON block and the shortened prose
  gave back. **The site is not shorter, and it was not supposed to be.** What
  changed is the order in which it can be understood: the shape first, the
  argument after. Anyone measuring this pass by word count is measuring the
  wrong thing.
- **One accuracy decision worth keeping.** The self-audit chart adds a row that
  is not in the delivered report — Noven at zero. That is an edit to a page
  whose entire premise is that it reproduces the document unchanged, so it is
  declared in the note under the chart, in the same way the two redactions are.
  The zero itself is the report's own headline finding, stated twice above the
  chart. A chart of who got recommended that omits the business commissioning
  it is a chart with the point taken out.
- **What the homepage figure deliberately does not claim.** No counts in the
  labels, no percentages, no measured ratio — ten marks are "the businesses
  that could answer", not a finding. The motion (the seven emptying) is timed
  to start after the block has finished fading in, so the intermediate state
  where the assistant lane looks like the results page is never what a reader
  is left looking at.
- **The 01/02/03 markers are gone from how-it-works, on the owner's second
  instruction the same day — and this had been said before and not written
  down, which is why it came back.** It is recorded here and in a comment on
  `.stages` in `global.css` so a third session cannot reintroduce it. The
  reasoning: the order is real and the `<ol>` still carries it, but a numbered
  run of three reads as one three-step process the reader is partway through,
  and that page's entire argument is that it is allowed to end at any of them.
  A numbered marker is also the single most common tell of a generated layout
  — the `frontend-design` skill names it explicitly — and it is only earned
  where the sequence itself is the information. Here the *exits* are the
  information. **Do not put them back.**
- **The diagram marks were redrawn after a contrast check.** The first version
  used `--paper-3` and `--rule`, which measure 1.1:1 and 1.3:1 against paper —
  a diagram you have to be told is there. They are now three intensities of the
  brand navy: 30% fill for a business on the results page, full navy for one
  named in an answer, and that same 30% reduced to an outline for one the
  answer left out. Solid-dark, solid-light, outline — fill and weight, so the
  encoding never rests on hue. **It reaches about 2:1, not the 3:1 WCAG 1.4.11
  asks of a meaningful graphic, and that is a judged trade rather than an
  oversight:** the marks are `aria-hidden` and every word of what they show is
  in the caption beside them at 6.75:1, and the tone that clears 3:1 on this
  paper turns a quiet figure into a wireframe that fights the page. If the
  graphic ever becomes the only carrier of something, this has to move.
- **The site's own look sits near one of the current generated-design defaults**
  — hairline rules, small radii, a serif display on warm off-white. Worth
  knowing rather than acting on: the brand direction is fixed in `CLAUDE.md`
  and wins, and what separates it in practice is the navy and brass rather than
  the usual cream and terracotta, the three-voice serif/sans/mono system, and
  the fact that the signature element is the business's own structured data
  rather than an illustration. Raised so nobody re-derives the worry.
- **Next:** nothing outstanding from this pass. The second self-audit, when it
  lands, will produce genuinely comparable data for the first time — that is
  the moment to ask whether a before/after visual is earned. It is not earned
  on one data point.

### 2026-08-09 (the copy and conversion review, applied across all six selling pages)

**The owner supplied a page-by-page review of the live site and asked for
surgical changes, not a rewrite.** Its two organising principles — *diagnosis
before intervention, evidence before recommendation*, and *we do not ask for
trust where verification is possible* — were treated as internal copy standards
rather than headlines, which is how the review framed them. Priorities 1 and 2
were implemented in full. Priority 3 is explicitly gated on outreach evidence
and was left alone.

**The homepage was restructured, and it is the only structural change.** The
hero was a two-column grid with the JSON-LD record panel beside the headline.
That put the strongest proof for a reader who *already believes there is a
problem* in front of the reader who doesn't, which is the wrong way round for
cold traffic. The hero is now the same single-column `hero--rules` every other
page uses; the record moved to its own section below the proof section. The
`.hero-grid` rule in `global.css` had no remaining user and was deleted (a
comment marks where it was and why). A `.record-panel` rule replaces it — the
panel now sits in the body column of a split, under the paragraph introducing
it, and needed the top margin a paragraph would have had.

**Two new homepage sections, both arguing the same thing from different ends.**
"What if there's nothing wrong?" sits third, directly after the problem
statement, because a cold reader decides within two screens whether this is an
audit or a sales funnel. "Where's the proof?" was reordered to lead with the
self-audit rather than the website — the self-audit is the stronger proof and
was buried third in its own section. The hero's secondary call to action is now
`/ask-your-ai/` rather than `/how-it-works/`: outreach traffic is not ready to
spend £250, and "check us yourself" is a route that costs them nothing.

**The absolute technical claims were tightened everywhere they appeared, and
this is the change most worth not undoing.** The pattern was the same in six
places: *everything these systems demonstrably rely on*, *gets you visible*,
*the format these systems are built to consume*, *this is what an assistant
reads*, *re-crawl and re-rank*. Each now says what is observable and influenced
rather than what is guaranteed or known. The site sells an audit that separates
observation from assumption; copy that overclaims is the one thing that makes
that unsellable. Nothing was softened into vagueness — "we work on the inputs we
can observe and influence" is a narrower claim than the one it replaced, not a
woollier one.

**Foundation was rewritten outcome-first on `how-it-works.astro`.** Four bullets
that opened with a technical task now open with what changes for the client and
name the mechanism second. Same four pieces of work, same fixed scope.

**Ongoing was simplified on `how-it-works.astro` and given buyer-fit lines on
`pricing.astro`.** How It Works now describes the operating model and points at
pricing for the plan detail, rather than explaining three plans twice. Each plan
opens with who it is best for. **Lead stopped promising to make you the first
name mentioned** — in the page copy and in its `schemaDescription`, which is
published and cached, so the overclaim was in the machine-readable version too.

**The self-audit page got an executive summary and nothing else.** The report
below it is untouched and should stay untouched: it is evidence, and an edited
piece of evidence is not one. The summary exists because the report earns its
conclusion over several thousand words and a busy owner needs the finding in
twenty seconds. Every number in it is lifted from the report underneath. It also
carries the Audit → Foundation bridge, because this page is the cleanest
illustration the business has of a finding that did *not* belong in Foundation.

**The `ask-your-ai` sections were deliberately not reordered, and the reason is
recorded in the page's own header comment.** The review asked for the free
self-test to appear earlier. Its own recommended sequence is check-us → check
yourself → what the paid version adds, which is what the existing order already
does — moving the self-test above the report would have inverted it. A skip link
under the hero gives a reader the test in one click instead. The competitor
due-diligence commentary was compressed from four paragraphs to two: the
argument is stronger as a structural observation about a young field than as a
list of things other people do.

**Review §3F — the external corroborating sources — was first misread as an open
scope question, and it is not one.** This session's initial reading was that
nobody had decided whether the £250 audit checks directories, company records
and review ecosystems, and that writing it into the copy would be inventing
scope. **The owner challenged that and was right.** It has been decided since
the checklist was written: `ops/audit-site-checklist.md` **Group 3, "Are the
facts the same everywhere"** — fifteen minutes, hard stop — names nine sources
and requires the name, address and phone recorded *exactly as written* in each:
Google Business Profile, Bing Places, Companies House, the applicable
professional register, two trade directories, LinkedIn, Facebook, plus the
public Bing and Google index checks. The checklist calls it "in practice the
group that produces the most findings on the most audits".

**So §3F was always a copy fix, and it is now made.** The gap was that no
selling page named any of those sources — How It Works said "the places these
systems draw from", Pricing said nothing at all. All three of How It Works,
Pricing and the FAQ now list them and say what is recorded. The old-address
finding is called out by name, because the checklist flags it as the classic one
clients do not know about, and it is the most legible proof that this half of
the audit is real work rather than a line in a scope list.

**Why the confusion was available to make, which is the part worth keeping.**
Group 3 is specified in `audit-site-checklist.md`, and `audit-method.md` —
whose numbered sections cover the assistant-querying half only — pointed at it
twice, both times too thinly to register: four words in the companion-documents
list ("what we look at on their website and off it") and a 15-minute row in the
section 7 time budget. **A first draft of this entry said the method document
"never mentions Group 3", which is wrong and has been corrected here.** The
pointers existed; they were just skippable, which for a document a session reads
to establish what the £250 buys is the same failure with a smaller cause. Fixed
2026-08-09: the preamble of `audit-method.md` now says outright that the file
covers half the audit, names Group 3's nine sources, and says both files have to
be read. It also genuinely was not run on the
self-audit (`ops/audits/noven-2026-08-02/checklist.md`: "Group 3 not started"),
so the one published example of a finished report shows no off-site findings.
The report is honest about it — "We haven't checked your listings elsewhere" is
in its own limitations list — but that line was, until today, the only place on
the entire site where those sources were named, which is precisely the failure
§3F describes: telling a prospect these sources matter while appearing not to
check them.

**The two follow-ups this session left open were both closed the same day, on
the owner's instruction, and they closed differently.** The `audit-method.md`
pointer was a document fix and was simply made — tracking a one-paragraph edit
costs more than doing it. Review Priority 3 could not be: its four items are
gated on evidence that does not exist yet, and doing them now means inventing
the thing they are supposed to be built from. They are now **roadmap 2g**, each
carrying the specific gate that unlocks it, sitting in Phase 2 where the
evidence will arrive rather than in a log entry nobody re-reads. **The
distinction is worth reusing: a fix goes in the file, a wait goes in the
roadmap.**

**Found while placing 2g, and fixed:** roadmap 2d described "the `[PLACEHOLDER]`
block in the last section of `/ask-your-ai/`". That block was removed on
2026-08-06 — it was an instruction to the next session about to be crawled and
cached as site copy, and it now lives in a source comment. The task it described
is still open and still correct; only its landmark was gone.

**Checked:** `npm run build` clean, `repo-consistency` clean (zero errors
outside `node_modules`), homepage screenshotted at 1440 and 390 with JavaScript
off, which is how the reveal animations are bypassed — with JS on, every
`data-reveal` block is `opacity: 0` until scrolled to, and a full-page
screenshot captures a blank page. Worth knowing before the next session wastes a
screenshot on it.

---

### 2026-08-08 (the condensing pass, run on the files a session actually opens)

**The owner's reason: usage limits are arriving faster.** So the target was
reading cost, not correctness — the scanner was already at 0 errors before this
started and the whole pass added none.

**`ROADMAP.md`: 7,774 → 6,211 words, 20% off.** It is the one file whose header
tells every session to read it start to finish, so it is worth more per word cut
than anything else here. What went was the second telling, in every case: the
three method faults were written out in full in "Where we are today" *and* in 3a;
1e restated 1c-3's two search-console items; the seven closed rename items in
1c-3 carried a paragraph of history each where a closed item is supposed to carry
its decision and its live consequence. **Section 3e went entirely** — it recorded
the deletion of three stub files in July, which `ops/README.md` already carries.

**Nothing open was touched.** Every `[ ]` and `[D]` item, every date, reference
number, phone number and URL survives — the ICO deadline and helpline, `C1995412`,
the £120,000 FSCS cap, the decay baseline of 4, the DMARC test still owed, the
redirect regression test.

**One real fault found, and no checker could have found it.** The "Open questions
for the owner" section still led with **"Does Noven keep its name?"** — settled
on 4 August, in the same file that announces the rename in its own banner. It is
the same shape as the three contradictions found on 7 August: a paragraph correct
when written and never re-read after the thing it described changed. Replaced
with the brand decision from 2f, which is genuinely open.

**`ops/search-console-and-bing.md`: 3,031 → 1,038 words, 66% off** — the clearest
settled-versus-live case in the repo. It was a click-by-click runbook for two
consoles that were both finished on 6 and 7 August. **The setup steps are gone**;
what stays is what outlives the job: the four things that must not be undone
(keep the old property, never press CANCEL MOVE, leave the redirects, don't add
the old domain to Bing), the three checks still owed, the §1.5 live-URL test
because it is the only check in this repo that asks a system we do not control
what it actually sees, and the validator lesson that found the missing redirects.
Its own header now says it is closed as a runbook and live as standing rules.
**It had claimed the click steps were "kept as written, because it is the
procedure for the next domain"** — there is no next domain, and keeping a
procedure for a situation we have not met is the thing `ROADMAP.md` says in its
own header that we do not do.

**`ops/README.md` was not indexing four of its own files** —
`competitor-analysis.md`, `plan-to-1-september.md`, `rename-to-wardith.md` and
`search-console-and-bing.md`, one of which is the launch timetable. An index
missing a quarter of its folder is worse than no index, because it is trusted.
Two new sections added and all four given a status.

**One false positive written into the scanner rather than left to recur.**
`ops/README.md` describing "the full Noven → Wardith changeover" reads as a
current-fact use of the dead name; it is the title of a past event, and the file
it points at is the record of that event. In `reviewed_names` with the reason,
per the documented practice.

**Repo prose 92,600 → 88,551 words.** Scanner: 0 errors before, 0 after.

**What a merge publishes: nothing visible.** No file under `site/` changed.

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

### 2026-08-07 (owner confirms UK Postbox; purchase runbook written)

**Done:** the owner confirmed UK Postbox. The comparison is closed and the item
is now a purchase, so the work this session was turning a decision into
something that can be executed without re-reading six sections — **new section
`ops/third-party-services.md` B1c, the runbook**. A row for UK Postbox was
added to the `ops/accounts.md` register pre-filled and marked not-yet-bought,
and the status changed from "the pick" to "confirmed" across `ROADMAP.md`,
`HANDOVER.md` and `ops/plan-to-1-september.md`.

**Four operational facts found in their user agreement and verification pages
that were not known when the decision was made.** None of them changes the
decision; all four would have been unpleasant to discover at the checkout.

1. **The ID check leaves a soft footprint on the owner's personal credit
   file.** Their terms say it is an ID check only and affects neither the
   credit report nor the ability to borrow. It is recorded because it touches
   the owner personally and should not be a surprise. Verification is
   biometric, usually approved **within 24 hours**.
2. **Registering the trading name is its own verified step**, not a text field
   — UK Postbox publishes a separate "Add Business Names" verification guide
   alongside its per-legal-status guides, and there is a specific **"Sole
   Trader"** guide to download *before* signing up.
3. **An inactive account gets its mail returned to sender after a month, and
   purged and shredded at six.** On a £12 subscription paid by card, a failed
   payment is a plausible event — and its consequence is a silently broken
   legal disclosure on the site plus returned statutory post. That risk is now
   the "if missed" column of the `ops/accounts.md` row.
4. **Leaving is a project, not a cancel button.** Their terms require the
   address to be moved off ICO, HMRC and everywhere else *before* closing, or
   continued use stays chargeable. Icon Offices sets the same trap. **This is
   the strongest argument yet for choosing once**, and it sharpens the note in
   B1b about switching to an annual provider later if capital eases: that is a
   change of address across the footer, the JSON-LD, the ICO record and HMRC,
   not a swap of direct debits.

**One cost recorded as unknown rather than assumed, per `CLAUDE.md`.** Their
user agreement refers to "the standard setup fee", but **no setup fee appears
on the pricing page, the business address page or in the terms** — the only
mention is in a clause about re-creating a lapsed account. It may be £0 for new
signups. It is `[PLACEHOLDER]` in B1b and in the accounts row, with an
instruction to read the checkout total before confirming. **The B1 comparison
was run entirely on headline monthly rates, so if a setup fee exists it is a
gap in that comparison and not just a line on an invoice.**

**Why the runbook orders the downstream work rather than listing it.** Buying
the address is step one of nine, and the last three — footer, ICO address
change, structured-data locality — are the ones that actually close the
original risk. The ICO change is why this became urgent at all: registration
`C1995412` carries the owner's home address on a bulk-downloadable public
register. **Buying the address and stopping there fixes nothing**, which is the
failure mode a runbook is for.

**Still open and deliberately not resolved here:** the Trustpilot score
(reported as both 4.0 and 4.7; Trustpilot blocks automated fetching, so it is a
five-minute human check before paying), the setup fee, and the locality
question — whether the structured data eventually says Poole, Dorset or says
nothing.

**Next:** buy it, following B1c; fill in the `ops/accounts.md` row the same
day; then the footer and the ICO address change.

---
### 2026-08-07 (Competitor analysis Part 2 — the raw data, and what it overturned)

**Done:** `runs-clean.csv` supplied by the owner and mined against Part 1's desk
research. `ops/competitor-analysis.md` now carries both halves and one execution
plan; `ROADMAP.md` 2f rewritten from "start a new session here" to six execution
items. **The file was read in the scratchpad and not committed**
(`ops/audit-method.md` §5). Confirmed for the owner that it is the same data as
the Noven audit — `audit_id = noven-2026-08-02` on all 210 rows.

**The finding that changes the framing: there is no incumbent.** The audit
report's table — Tilio 36, nine more behind — reads as a pecking order to climb.
Counted against the right denominator (165 rows where a business could have been
recommended) Tilio is named in 28%, second place 23%, third 12%, and **62 of the
165 answers name nobody at all.** 41 businesses in total, against the report's
ten. That is not a market with leaders to displace; it is one that has not
formed. Everything else in the plan is cheaper in that light.

**Part 1's main recommendation had to be withdrawn, and this is the reason to
keep writing these documents down.** Part 1 called "get Wardith added to the
existing third-party listicles" the highest-leverage, lowest-risk option of all.
WebFetch was blocked that session, so it rested on search snippets. This session
WebFetch worked, so all of them were actually read — and **they are not
third-party.** Buried Agency's list of the best agencies is published by Buried
Agency, which ranks itself first. So does FirstMotion's, Sort The Clicks',
Okapi's, Tilio's, ClickSlice's, Rank4AI's. None has a submission form, an
editorial email, or stated criteria for applying. The recommendation was to ask
competitors for a favour, and the honest expected answer is no.

**The same evidence points somewhere better.** Every one of those publishers got
cited *by writing the list*. Answers citing a list name 3.3 businesses; answers
citing none name 1.2. Part 1 had already agreed a self-inclusive comparison page
was fair game and listed it third of three options. The data promotes it to
first. **It is emphatically not the parked "trust score" idea** — no invented
scores, no pass/fail criteria, real providers described accurately, Wardith's
authorship on the page, every claim verifiable before publication. That
distinction is the whole reason "Considered and not done" was written, and it
held up: it stopped the wrong version being re-proposed while leaving the
defensible one available.

**One genuinely open door, and it is small and free.** On the Wirral question
the field is five businesses, not forty-one — and Bold Online Marketing is named
in 15 of 15 runs, on all three assistants. Two of them cited
`threebestrated.co.uk/marketing-agencies-in-wirral` as a source. It is a real
directory, Bold is on it, and it says "List your business for Free!" That is the
cheapest concrete action in the whole piece of work.

**The rename is vindicated by data that didn't exist when it was decided.**
`ops/rename-to-wardith.md` argued the move mainly from there being no indexation
equity to lose, which is true but defensive. The raw answers are worse than that
argument assumed: asked "What do you know about Noven?", **0 of 30 runs
described this business** and all 30 described Noven Pharmaceuticals, the US
patch maker. Adding "on the Wirral" didn't fix it — ChatGPT 0 of 5, and
Perplexity confidently offered a North West *builder* and a Wirral *IT support
firm* instead, which is worse than silence. Asked for "the main alternatives to
Noven", ChatGPT answered about managed IT service providers. Only Gemini got it
right, 5 of 5, and that is a point about Google having indexed the site rather
than about the name. Nothing here reopens the decision; it closes the argument.

**A method problem found by accident, and it matters more than the analysis.**
All 479 of Gemini's cited URLs are `vertexaisearch.cloud.google.com` redirect
wrappers that resolve nowhere readable. **For one of the four assistants we sell
coverage of, `sources_cited` is structurally empty.** `ops/audit-method.md` §5
lists the column without saying so, and that document feeds client reports. A
report must never imply we can see what Gemini read. On the roadmap as a fix.

**Recorded as a limit, not smoothed over:** the supplied export is
pre-classification — `outcome` and `competitors` are blank on all 210 rows — so
the report's own mention counts could not be re-derived from it. Every count in
Part 2 comes from matching names against `answer_text` directly, which is why
the numbers don't tie to the report's table. Said plainly in the document rather
than reconciled away.

**Then, at the owner's request: the commercial reading, filed where each piece
belongs.** The execution plan in `ops/competitor-analysis.md` was reordered by
size of ticket rather than by ease, and two things came out of the data that the
analysis write-up had under-weighted.

**The biggest number in the dataset is a pricing number, not a visibility one.**
All three assistants quote a **median £1,500/month**, and they describe
£500–£1,500 as *freelancer and consultant* rates with agency work above. Lead is
£700. The consequence is specific and it is new: **a buyer who arrives through
an assistant has been anchored at £1,500 by the assistant itself**, and then
reaches a pricing page asking under half that. `ops/service-tiers.md` §1 argues
we are priced against local search agencies and against a quiet phone, not
against agency quotes — that argument is untouched and still right for the buyer
it describes. It is simply no longer the only comparison the buyer has seen.

**Filed in `ops/service-tiers.md` §8, not acted on.** That document owns pricing,
this one doesn't, and an assistant does not move a price. Both entries are
written to say what they do *not* settle as well as what they show — the audit
one explicitly is **not** a case for moving the £250, only for asking whether a
deeper second tier nearer the £750 the assistants quote is worth having.

**The play with the best return for the effort is the cheapest one here.**
Re-running q06–q08 under "Wardith" costs three questions. Under "Noven" it was
0 of 30. If it flips, it produces the one thing no competitor on any of the
sixty cited lists has and no amount of copywriting can manufacture: a dated,
measured before-and-after on our own business. `CLAUDE.md` forbids inventing
results, and **that prohibition is exactly what makes a real one valuable** — it
is the only honest answer a months-old business has to "why would I pay a
stranger £800."

**One gap in the market that the write-up had recorded as a statistic and not as
an opportunity:** 62 of the 165 opportunity rows name **no business at all** —
better than a third of the demand goes to vetting advice instead of a
recommendation, and nothing currently occupies that ground. A plain-words page
on telling a real practitioner from a rebranded one costs credibility nothing,
because it is already the voice of `/ask-your-ai/`.

**A brand decision was asked for and deliberately left unanswered.** The
comparison page is the exact situation `CLAUDE.md`'s single deliberate exception
was written for on 2026-08-01 — a buyer arriving holding the acronym, and a site
that contains the word nowhere being unable to be the answer. But that exception
was granted for **one** FAQ entry, by the owner, on the record. Whether it
stretches to a second page is not an assistant's call, and the page does not
start until the owner rules. Recorded in both the doc and `ROADMAP.md` as
blocking rather than assumed either way.

**What this merge publishes: nothing visible.** Four documents changed —
`ops/competitor-analysis.md`, `ops/service-tiers.md`, `ops/session-log.md`,
`ROADMAP.md`. No file under `site/`, no copy, no JSON-LD, no price. Netlify will
rebuild and serve a byte-identical site. Said out loud because `CLAUDE.md` asks
for it before every merge, and because "nothing visible" is the honest answer
often enough to be worth stating rather than skipping.

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

