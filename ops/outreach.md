# Cold outreach — how the first clients are found

**Status: Decided, unvalidated.** Written 2026-08-09. Nobody has been contacted.
Every number in the "what actually happens" section is a guess until a batch has
been sent, and is marked as one.

**Internal document.** Read `ops/audit-method.md` and `ops/audit-questions.md`
before running the assistant queries this depends on. Read
`ops/competitor-analysis.md` for why the finding in the email works.

---

## 1. The decision this document exists to record

**The owner has no business network, so the first clients are cold.** Settled
2026-08-09. Everything written before that date assumed warm introductions
first — `HANDOVER.md` step 6, `ROADMAP.md` 2c — and that route is closed, not
deferred.

**Target, settled the same day: private clinics on the Wirral.** Dental,
cosmetic, physiotherapy, veterinary. One trade, one area, per `ROADMAP.md` 2a.

Why this trade, in the order the reasons matter:

- **Almost all of them are limited companies**, which is a legal requirement of
  cold email rather than a preference. Section 2.
- **Their customers genuinely ask an assistant to recommend one.** "Best dentist
  near me", "Invisalign Wirral", "emergency vet Wirral" are real questions a real
  person types. A trade whose customers arrive by referral has nothing for us to
  find.
- **They already buy marketing**, so the £250 audit is a familiar kind of spend
  rather than a new category of one.
- **The Wirral is small enough that one assistant run covers the whole market**,
  which is the entire economic basis of section 4.

---

## 2. The legal frame — read this before building any list

*Not legal advice. It is the position this business is operating on, and it
should be checked.*

**Cold email is lawful to companies and unlawful to people.** Under PECR, limited
companies and LLPs are *corporate subscribers* and may be sent unsolicited
marketing email without prior consent. Sole traders and unincorporated
partnerships are treated as individuals and need consent we do not have.

**That turns the target definition into a filter, not a preference:**

> **Nobody is contacted unless Companies House shows a live limited company or
> LLP at that trading name.** No company number, no email.

This is free to check and it builds the list at the same time — see section 3.

**Three things every outreach email must carry**, all of them consequences of
the above rather than good manners:

1. **Who we are.** Wardith, the trading name, and the address for service.
2. **Where we got their details**, in one line. Under UK GDPR, when you hold
   someone's details from a source other than them you have to tell them, in
   practice at first contact.
3. **A working opt-out**, honoured permanently. A reply saying "don't contact me
   again" is the mechanism; we do not need an unsubscribe system for batches this
   size, we need a record that cannot be lost. See section 6.

**Two published pages are now blockers on the first email, not on launch.**

- **`/privacy/`** already carries the paragraph this needs — the "If we contact
  you first" section names legitimate interest and permanent opt-out recording.
  **It publishes as of 2026-08-10.** The address for service landed and the
  storage question was settled the same day: records are held locally, on the
  owner's own encrypted machine, in the United Kingdom. `ops/client-record.md`,
  "Storing it locally", has why the Microsoft consumer account could not do it.
  **The one thing that must be true is full-disk encryption being on**, because
  the notice claims records are encrypted at rest.
- ~~**The address for service**~~ — **live 2026-08-10.** UK Postbox, Poole,
  £12/month. The line to put in an email is the **mailbox** address:
  `Lytchett House, 13 Freeland Park, Wareham Road, Poole, Dorset, BH16 6FA`.
  Not the courier address — `ops/accounts.md` has both and explains which is
  which.

**A warm route would have sidestepped both. Cold cannot — and as of 2026-08-10
both are paid.** The first cold email needed `business.addressForService` and
`business.clientDataStorage` set in `site/src/data/business.ts`. Both are set,
both pages publish, and **outreach is no longer blocked by anything in this
section.**

**What remains is not a blocker but a rule, and it applies from the first
email.** Replies come from named people at named practices, and the permanent
opt-out record names them too — **that is personal data, held from the moment
somebody answers**, which is the trap in thinking this is only about clients.
**The 67-row Companies House sweep in §3 is already the beginning of it.** So
the machine it all sits on needs encryption switched on, and it must not sit in
a folder Windows syncs to a consumer OneDrive account. Neither costs anything;
both are in `ops/client-record.md`.

---

## 3. Building the list

**The order below is wrong, and 2026-08-10 proved it. Start with the regulator,
then use Companies House to answer one question about each name it gives you.**
The Companies-House-first method described in the rest of this section was run
again and reproduced its 67 rows exactly, district for district — and then a
CQC-first sweep of the same peninsula found **twelve real, trading, limited-company
dental practices it had missed entirely.** Their companies are registered in
Cheltenham, Exeter, Northampton, Bolton, Richmond, Maghull, Liverpool, Cheadle,
Ellesmere Port and Portchester. Nothing about them is unusual; they simply use
an accountant who is not on the Wirral. §3 predicted this failure in one
sentence — "the list is a floor, not a census" — and then built the list on the
floor anyway.

**The method that replaces it, for any regulated trade:**

1. **Take the census from the regulator.** For dental that is the CQC directory,
   a free national CSV of every registered location — name, address, postcode,
   phone, sometimes a website, and the registered provider. Filter to the
   postcode districts. It is the *trading* list, which is the thing we actually
   want, and no accountant's address can hide a clinic from it.
2. **Read the provider column, because it is the PECR test in disguise.** CQC
   records who is registered to run each location. "Something Limited" is a
   company and may be cold-emailed. "Dr So-and-so" or "Such-and-such Partnership"
   is a sole trader or an unincorporated partnership and may not be. **On the
   Wirral that single column removed 21 practices from the pool** — about a third
   of the market, closed by §2 rather than by judgement.
3. **Then use Companies House, by name, to confirm the provider is live.** One
   search per provider. This is where the "is this a company" question belongs,
   and it is a much smaller job than sweeping thirteen districts. One Wirral
   provider whose name ends in "Ltd" turned out to have **no live company at
   all**, which no amount of reading the name would have caught.
4. **Keep the postcode sweep only as a cross-check.** It still finds the
   personal service companies and the shared offices described below, and those
   are worth seeing. It is not the list.

**The trades that are not regulated do not get step 1**, and for those the
Companies House sweep is still the only free route. Check whether a regulator
publishes a directory before assuming it.

**It is built — `ops/prospect-list/`.** Three scripts, the runbook, and what the
triage removes and in what order. Run it before the trade run, not after: the
trade run's mention table is the last cut, and there is no point paying for
ninety queries about a market you have not counted.

**One correction to the shared-office finding below, because acting on it as
written would delete real prospects.** A registered office hosting several
companies on the list is not automatically an accountant. It splits two ways,
and only one of them is the trap:

- **An accountant or a serviced office.** The registered office is not a clinic
  and the trading address has to come from the practice's own website. This is
  the case §3 warned about and it is real — one Wirral accountant's address
  carried four of the 67.
- **A clinic where the associates also register.** The practice company and two
  or three dentists' personal service companies all sit at the practice's own
  address, because that is where they work. **The address is a clinic, and
  exactly one of those companies is the prospect.** Two of the four-company
  addresses on the Wirral are this, not an accountant.

**Source: Companies House, free, and the filter and the list are the same
operation.** Search by SIC code, then by registered-office postcode.

| Trade | SIC code | Confirm before trusting |
|---|---|---|
| Dental practices | 86230 | Yes |
| General medical practice | 86210 | Yes |
| Specialist medical practice | 86220 | Yes |
| Other human health activities — physio, chiropractic, podiatry | 86900 | Yes |
| Veterinary | 75000 | Yes |

**86230 is confirmed by evidence rather than memory as of 2026-08-09** — the
sweep below returned dental businesses in every one of the thirteen districts.
**The other four codes are still from memory and must be checked** against
Companies House's own list before they are used. A wrong code produces a list
that looks right and is not, which is exactly the failure this business is sold
to find in other people's data.

### The sweep, and what it returned — 2026-08-09

**Companies House advanced search does this in one URL per district**, no account
and no API key:

```
https://find-and-update.company-information.service.gov.uk/advanced-search/get-results
  ?sicCodes=86230&registeredOfficeAddress=CH41&status=active
```

Change the postcode district, repeat. Thirteen fetches covers the Wirral.

**Result: 67 active limited companies** on SIC 86230 with a Wirral registered
office. By district: CH41 4, CH42 2, CH43 4, CH44 2, CH45 4, CH46 6, CH47 2,
CH48 4, CH49 9, CH60 4, CH61 8, CH62 12, CH63 6.

**67 companies is not 67 prospects, and the gap is the whole job.** The list is
handed to the owner as a CSV with a `triage` column and is **not committed** —
see §6. Three things have to be stripped out before it is a prospect list, and
they are visible in the raw data:

- **Personal service companies.** A dentist who works at somebody else's practice
  and invoices through their own limited company is on this list and is not a
  prospect — there is no practice to make visible. **17 rows are flagged as
  likely, mostly on the name being a person's.**
- **Suppliers, labs, training providers and referral services.** Also SIC 86230,
  also not patient-facing, also not prospects.
- **Shared registered offices.** **22 of the 67 sit at an address shared with at
  least one other company on the list** — four at one postcode in three separate
  cases. That is an accountant's office, not a clinic, and it is the trap §3
  already warned about. **Match the trading address from the practice's own
  website, and use Companies House only to answer "is this a company".**

**The sweep also under-counts in one direction that matters.** A practice trading
on the Wirral but registered at an accountant's office in Liverpool does not
appear here at all. The list is a floor, not a census.

**Wirral postcodes: CH41–CH49, CH60–CH63.** CH64 is Neston, on the peninsula but
in Cheshire West, so it is a judgement call rather than an obvious yes. **Check
this list too** — a postcode district that turns out to be Chester puts the
"we're local" line in the email into an outright false claim.

**The registered office is not always the clinic.** Many use their accountant's
address. Match on trading address from the clinic's own website, and use
Companies House only to answer "is this a company".

**What we record per prospect** is in `ops/client-record.md` — the prospect
fields are already decided there. Do not invent a second schema.

### The triaged figure — 2026-08-10

**The dental list is built and it is smaller than anyone expected.** From 73 CQC
dental locations in CH41–CH49, CH60–CH63 and CH64:

| Cut | Left |
|---|---|
| All CQC dental locations in the postcode range | 73 |
| Minus duplicate registrations of the same site | 69 |
| Minus national and regional groups, and the NHS trust | 55 |
| Minus providers who are a person or an unincorporated partnership — §2 closes these | 34 |
| Minus Neston, which is Cheshire West rather than the Wirral | 31 |
| Minus a referral service, a hygiene-only studio, and one provider with no live company | 28 |
| **Approachable, and the company confirmed live on Companies House** | **28** |
| Of those, with a website and a contact address already in hand | **9** |

**Nine is most of a first batch and it is the whole of what is ready.** Five more
have a live company and a working website and need one look in a browser for an
address. The rest need a website found, or have none.

**Two things follow, and the second one is uncomfortable.** The list is the
binding constraint exactly as §7 predicted, and it binds harder than the
arithmetic there assumed: **twenty emails a week does not survive contact with a
single trade in a single area.** Dental on the Wirral is roughly a fortnight of
sending, not a quarter of it. Either the area widens, the trades widen, or the
batch size comes down — and that is a decision, not a detail.

`[PLACEHOLDER: the same census for cosmetic, physiotherapy and veterinary. The
CQC route covers cosmetic and some physiotherapy; veterinary has its own
regulator, the RCVS, and its register needs checking before it is relied on.]`

**Do not contact the practices the assistants already name.** The list is built
and it includes them; the visibility ladder's bottom rung says they are not
prospects, and §3's definition of a good first client says the same. On the
Wirral this is a live case rather than a hypothetical: **two of the three
practices on the directory cited in 20 of 90 answers share one owner**, and both
are named. That owner gets nothing from us and should not be emailed.

### What makes a good first client

Written now so it is not rationalised backwards after the first reply.

- **A limited company**, per section 2. Not negotiable.
- **Owner-run, or with a named person who can say yes.** A practice manager
  reporting to a group board is a long sale we cannot afford yet.
- **Has a website we can actually assess.** No site at all is a different
  product and a much harder conversation.
- **Not already visible.** If the assistants already name them first for their
  own trade, we have nothing to sell them and should say so rather than pitch.
- **On the Wirral**, so the first case study says something specific.

---

## 4. The pre-work — one run per trade, not one per business

**`ROADMAP.md` 2b says to run a mini audit on each prospect before contacting
them. That is right for warm and unaffordable for cold.** The self-audit's
recorded cost was **$12.63 on OpenAI alone for roughly 75 queries**
(`ops/audits/noven-2026-08-02/README.md`), so roughly $0.17 a query. A hundred
prospects at three questions each is real money during a spending freeze.

**The fix is better than the thing it replaces.** Ask the discovery questions
once for the *trade and area*, not once per business:

> "Who is the best dentist on the Wirral?"
> "I need an emergency dentist in Birkenhead, who should I call?"
> "Which Wirral dental practices do Invisalign?"

**One run answers the question for every clinic in the area at once.** For each
prospect it produces two facts, and the second one is the one that sells:

- whether they were named, and
- **which of their competitors was named instead of them, by name.**

`ops/competitor-analysis.md` established the mechanism on our own market: a third
of answers name nobody at all, and listicles carry most of the names. Being able
to tell a clinic owner which three practices come up ahead of them, with the
question that produced it, is a far sharper opening than "you are not mentioned".

**Cost of a batch run:** six questions, three assistants, five runs each is 90
queries, on the order of **$15 for the whole batch** rather than per prospect.
Derived from the one recorded figure above, so treat it as an order of magnitude.

**Use the frozen question rules in `ops/audit-questions.md`.** A trade run is not
a client audit and does not go in `ops/audits/`, but the wording rules are the
same, and a question that works here becomes part of the library that file
describes as the compounding asset.

### It is built — `ops/trade-run/`

**Written 2026-08-09, smoke-tested against its own guards, never run for real.**
The self-audit's throwaway query script turned out to be reusable, so it is
copied to `ops/trade-run/trade_run.py` with three changes — the client name and
the run count are flags, and the defaults suit a trade run. The dentist question
set is beside it. Six questions, three assistants, five runs: **90 queries, one
command.** The runbook is `ops/trade-run/README.md`.

**Three things have to be true before it fires, and two of them are open:**

- **API keys**, per `ops/audit-setup.md` §2. Already recorded.
- **Funded balances — two are, one may not be.** As at 2026-08-09: OpenAI
  $16.00, Gemini £8.95, Perplexity $4.49, against 30 queries each at the only
  rate we have ever measured (~$0.17, from OpenAI on 2 August). **Perplexity is
  short by about fifty cents on that borrowed rate**, and it runs last, so the
  worst case is sixty rows banked and a five-dollar top-up. The arithmetic, and
  the auto-top-up check that matters more than the balance, are in
  `ops/trade-run/README.md`.
- **Python 3.9+ on the machine it runs from.** Stdlib only, nothing to install.
  `[PLACEHOLDER: whether Python is installed on the owner's Windows machine.]`

**It stops at the raw answers, deliberately.** The `outcome` and `competitors`
columns are written empty, because assigning them is the human judgement the
audit budgets 60 to 110 minutes for. The mention table below is built from the
answer text by hand — or by a second script written once we have seen what a real
trade run's answers look like, which is the same reasoning that defers the audit
runner.

### The mention table — who is named, and how often

**We already have this method and it has been run once.**
`ops/competitor-analysis.md` Part 2 did exactly this on our own market: 210 rows
from the self-audit, split into 45 identity rows and **165 opportunity rows**,
then every business name counted across them. It produced a ranked table with a
per-assistant split — Tilio 46 rows of 165, Rank4AI 38, third place 12% — and the
finding that mattered, which was that **no business held even a third of the
answers**.

**How the counting actually worked, because it is not what the method doc
assumes.** `audit_query.py` writes a `competitors` column, but on the export used
for Part 2 that column was empty on all 210 rows, so the counting was done by
**matching business names against `answer_text` directly**. That turned out to be
the more useful route and it is the one to repeat here, for a reason specific to
outreach: **the Companies House list from §3 is the candidate name list.** We are
not discovering who exists, we are checking which of a known set got named.

**The table to produce per trade run:**

| Column | Where it comes from |
|---|---|
| Business | The Companies House list, plus any name the answers raise that is not on it |
| Rows named | Count of opportunity rows whose `answer_text` contains the name |
| % of opportunity rows | The share-of-voice number |
| Split by assistant | ChatGPT / Gemini / Perplexity, counted separately |
| Sources cited alongside | From `sources_cited` — **ChatGPT and Perplexity only** |

**That last restriction is not optional.** Every one of Gemini's cited URLs is an
opaque `vertexaisearch` redirect, so no source analysis is possible for it
(`ops/competitor-analysis.md` Finding E). Any conclusion about *why* a business
is named rests on two assistants, not three.

**Expect a much shallower field than the national one.** The self-audit's own
Wirral question returned **five businesses, not forty-one**, and one of them was
named in every single run across all three assistants (Finding F). A local trade
question is a small field with a clear owner, which is the shape this whole
outreach depends on.

### The visibility ladder — how the unnamed become the target list

**The mention table answers "who is named". The prospect list is its
complement**, and that subtraction is the targeting method:

> **Companies House list, minus the businesses the mention table names, is the
> pool. Everyone left is invisible on the question their own customers ask.**

**But "not named" will be the normal condition, not a distinguishing one.** If
the Wirral holds sixty dental practices and the answers name six, then 90% of the
list is unnamed and "you are not mentioned" is true of almost everyone. **The
useful sort is not named-versus-not. It is how close each one is to appearing**,
and the run gives us that for free because it captures the sources the answers
were built from:

| Tier | What is true of them | Why they are ranked here |
|---|---|---|
| **A. In the sources, not in the answers** | Listed on a directory or listicle the assistants actually cited, and still not named | **The best prospects.** They have already done the obvious thing and it did not work, which is precisely what we sell. The email writes itself: you are on the page ChatGPT reads, and it still names three others |
| **B. Named occasionally** | Appears in one or two runs out of fifteen | Second best. A measurable gap rather than an absence — "you come up about one time in five, these two come up every time" |
| **C. Absent from everything** | Not named, and not in any cited source | Real prospects, and the fix starts somewhere concrete: get listed. Ranked below A because the first step is cheap enough that they may not need us for it |
| **Not a prospect** | Named consistently, at the top | Nothing to sell them. Do not email them. §3's definition of a good first client already says this, and the audit's own voice is "you don't need us" |

**Tier A is the finding this business exists to produce.** Anyone can tell a
clinic to get listed on a directory. Telling them they are already listed, that
the assistant reads that exact page, and that it still recommends three
competitors, is a fact nobody else in their inbox has.

**Tier A is populated, and that was checked rather than assumed.** The
2026-08-09 smoke test — three queries, one question — already surfaced several
Wirral practices listed in the cited directories and named by no assistant.
`ops/trade-run/README.md` has the detail.

### What the email should actually claim — settled by the full run, 2026-08-09

**The general claim is dead and the specific one is strong.** The smoke test
suggested the three assistants barely agree; at 90 rows **21 of the 39 named
practices are named by all three.** Consensus is normal. Do not build an email on
"the assistants disagree" — a prospect can check it in five minutes and it will
not hold.

**What does hold, stated per practice:**

- **Of the 39 practices named, 18 are missing entirely from at least one
  assistant**, including some in the top ten overall. Being strong on ChatGPT and
  absent from Perplexity is common, and no practice knows it.
- **There is a top tier of four at 36–43% of rows, and no incumbent above it.**
  The leader is missing from a clear majority of answers.
- **The practices nobody names are absent from the cited sources too.** They are
  not being passed over, they are not present. **This one stays inside the
  business** — it is a diagnosis, and §5's rule on what the email gives away
  keeps diagnoses in the paid report.

**So "you are not mentioned" is the weaker version of the finding we can
actually make.** The stronger one is specific and checkable:

> You come up when people ask Perplexity for a dentist on the Wirral. You do not
> come up on ChatGPT at all, on any of the five ways I asked. Here are the three
> that do.

**That is checkable in five minutes, true of eighteen practices out of
thirty-nine, and known to none of them.** It is also the version that survives a
sceptical reader, which the general claim would not have.

**Rewrite the §5 draft around it.** The draft was written before the run and
makes the weaker "you are not mentioned" claim.

**And for the practices nobody names at all**, the honest line is different
again, because their problem is bigger: they are absent from the directories the
answers are built from, not passed over by them. That is a plainer sell and a
faster first win.

**Two rules that keep this honest:**

- **The named businesses are for studying, not targeting.** Why the top few get
  named is the content of the audit deliverable — `ops/competitor-analysis.md`
  Finding B established that listicles are the mechanism. It is not a reason to
  approach them.
- **Never publish the ladder, or any part of it.** A ranked table of named local
  clinics is exactly the public comparison the owner parked on defamation and
  comparative-advertising grounds. Read "Considered and not done" in
  `ops/competitor-analysis.md` before proposing it again. **Naming a prospect's
  competitors privately, in an email to that prospect, is a different act from
  publishing a league table**, and only the first one is in scope.

**Never send the trade run to a prospect as if it were their audit.** It is one
finding, and the paid audit is ten questions on their own business. Blurring that
is how the £250 stops being worth paying.

---

## 5. The email

**One finding, one offer, no sequence.** No chasing email, no "just bumping this
up your inbox", no three-touch cadence. If the finding is not interesting enough
to answer once, sending it again does not improve it.

**Send in batches of ten to twenty**, so the wording can change based on what
comes back. `ROADMAP.md` 2b already required this and it survives the change to
cold.

**Two drafts, because the run showed two different problems** and one letter
cannot address both honestly. Which one a practice gets is decided by the
mention table.

**Rewritten twice on 2026-08-09.** First against `ops/voice.md`, which fixed the
structure: they had opened with the finding, which is how automated outreach is
built, and the subjects made a claim, which is how a campaign is written. Then
again, because the owner read them back and found **two competing invitations** —
a link to our own audit and a separate offer to send the answers, with nothing
telling the reader which one to act on. **Both now go one place: the audit.**

**Draft A — for a practice named by one or two assistants and missing from the
rest.** Eighteen of the thirty-nine named practices are in this position.

> Subject: [Practice] and ChatGPT
>
> Hello [name],
>
> I'm [owner]. I run a small business on the Wirral that checks what the AI
> assistants say when somebody asks them to recommend a local business.
>
> Last week I asked ChatGPT, Google's Gemini and Perplexity for a dentist on the
> Wirral. Six different ways of asking, five times each.
>
> Here is what ChatGPT gave back to three of them:
>
> "Who is the best dentist on the Wirral?" — [A], four times out of five.
>
> "Which dental practices on the Wirral do Invisalign?" — [B], [C], [D] and [E].
> All of them five times out of five.
>
> "What are the highest rated private dentists on the Wirral?" — [B], [F] and
> [E], again all five.
>
> [Practice] wasn't named once, on any of the six. It does come up on Gemini and
> on Perplexity, so this is specific to ChatGPT. Those are the exact words I
> used, if you want to try them yourself.
>
> One thing worth saying, because it's the first thing I'd want to test. I didn't
> ask about [practice] by name. If you type the name in, all three will probably
> tell you plenty, and accurately. I asked the way somebody looks for a dentist
> when they don't have one yet and don't know who you are. That's the question
> that brings in new patients, and it's a different question.
>
> What I sell is the reason behind it. Ten questions on [practice] across all
> three assistants, where their answers are actually coming from, and a written
> report on what's making them pick somebody else. It's £250, that's the entire
> cost, and the report is yours to act on with me or without me.
>
> If you want to see what one looks like first, I ran the same thing on my own
> business and published all of it, including what came back badly:
> wardith.co.uk/ask-your-ai/self-audit/
>
> Worth a look at [practice]?
>
> [Owner name]
> Wardith, Lytchett House, 13 Freeland Park, Wareham Road, Poole, Dorset, BH16 6FA
> hello@wardith.co.uk
>
> I found the practice through Companies House and your own website. If you'd
> rather I didn't keep your details, tell me and I'll delete them.

**Draft B — for a practice named by none of them.**

> Subject: [Practice] and AI search
>
> Hello [name],
>
> I'm [owner]. I run a small business on the Wirral that checks what the AI
> assistants say when somebody asks them to recommend a local business.
>
> Last week I asked ChatGPT, Google's Gemini and Perplexity for a dentist on the
> Wirral. Six different ways of asking, five times each, so ninety answers.
>
> Three of the questions, and what came back:
>
> "Who is the best dentist on the Wirral?" — [A] in thirteen of the fifteen
> answers, [B] in nine.
>
> "Which dental practices on the Wirral do Invisalign?" — [C] and [D] in all
> fifteen, [E] in fourteen.
>
> "What are the highest rated private dentists on the Wirral?" — [E] in all
> fifteen, [B] in thirteen.
>
> Thirty-nine practices got named somewhere across the ninety answers.
> [Practice] wasn't one of them. Those are the exact words I used, if you want to
> try them yourself.
>
> One thing worth saying, because it's the first thing I'd want to test. I didn't
> ask about [practice] by name. If you type the name in, all three will probably
> tell you plenty, and accurately. I asked the way somebody looks for a dentist
> when they don't have one yet and don't know who you are. That's the question
> that brings in new patients, and it's a different question.
>
> A practice can be missing for a few different reasons and they aren't equally
> hard to fix. What I sell is finding out which one applies to you. Ten questions
> on [practice] across all three assistants, where their answers are actually
> coming from, and a written report on what to change. It's £250, that's the
> entire cost, and the report is yours to act on with me or without me.
>
> If you want to see what one looks like first, I ran the same thing on my own
> business and published all of it, including what came back badly:
> wardith.co.uk/ask-your-ai/self-audit/
>
> Worth a look?
>
> [Owner name]
> Wardith, Lytchett House, 13 Freeland Park, Wareham Road, Poole, Dorset, BH16 6FA
> hello@wardith.co.uk
>
> I found the practice through Companies House and your own website. If you'd
> rather I didn't keep your details, tell me and I'll delete them.

### What the email gives away, and what it does not

*Rule set by the owner, 2026-08-09, correcting a first draft of Draft B that
handed over the diagnosis for nothing.*

**The observation is free. The diagnosis is the product.**

- **Free, in the email:** what was asked, how many times, who got named, and
  whether they did. All of it observation, all of it checkable, none of it
  requiring us.
- **Not free:** *why* a particular practice is missing, which pages the answers
  are actually built from, which of those they are on, and what to change. That
  is the £250, and a first draft of Draft B gave the headline finding away in a
  sentence.

**This is not a dishonesty question and it is worth being clear why.** "You were
named in none of ninety answers" is true and complete on its own terms. Declining
to add "and I think I know the reason" withholds nothing the reader was promised
and states nothing false. The site's voice is *you don't need us for everything*,
not *here is the work for nothing*.

**Two guardrails, and they are the price of doing it this way:**

- **Never imply we do not know.** "There are a handful of reasons" is honest.
  "I have no idea why" would not be, and neither would a hint that the answer is
  more mysterious than it is. Vagueness about our own knowledge is the line.
- **The audit has to be worth the £250 on its own.** The directory question is
  one finding, and the report cannot be that finding restated at length. It runs
  ten questions on *their* business, checks what the assistants believe about
  them and whether it is true, and reads their own site. **If a report ever comes
  down to "get listed on a directory", the price is wrong, not the customer.**

**The same rule applies to the market-level findings generally.** How the answers
are constructed on the Wirral is a thing we now know because we paid for ninety
queries and did the analysis. It is an asset. It goes in client reports, not in
cold emails and not on the site.

**What the drafts are doing, so they are not edited into a pitch by accident:**

- **The number is the email.** "[N] times on one, zero on another" is checkable
  in five minutes, which is exactly why it works. **Do not soften it into "you
  may not be appearing".**
- **Never say "you don't show up" without saying what was asked. This is the
  one that would have cost replies.** Caught by the owner 2026-08-09. Every
  question in the trade run is a **discovery** question — somebody looking for a
  dentist who does not know the practice exists. **None of them asks about a
  practice by name.** A sceptical owner's first move is to type their own name
  into ChatGPT, get a full and accurate answer, and conclude we are wrong.
  `ops/audit-questions.md` already separates discovery from named-business
  questions as different categories, and `ops/competitor-analysis.md` splits
  identity rows from opportunity rows for the same reason. **The email collapsed
  a distinction the method already draws.**
- **The fix makes the distinction the argument.** Both drafts now say plainly
  that we did not ask by name, that the assistants will probably answer well if
  you do, and that the question we asked is the one that brings in patients who
  have never heard of you. **It converts the objection into the strongest
  paragraph in the email** — it invites the check, and the check then proves our
  point instead of refuting it.
- **One destination, and it is the audit.** Two earlier versions failed here.
  The first offered "the six questions I'd ask about [practice]" — nobody wants
  six questions, it is an artefact from our side of the desk, and it named a
  thing that does not exist, because **the audit is a ten-question frame**
  (`ops/audit-questions.md`) and six was the trade run's number. The second
  offered to send the verbatim answers, which is a good thing to have but sat
  directly after a link to our own audit, leaving two invitations and no
  instruction. **A cold email gets one action.**
- **The self-audit link is proof, not a second destination.** It is framed as
  "if you want to see what one looks like first", subordinate to the ask. Do not
  let it drift back into being an alternative to replying.
- **Show the questions and the names. Do not tell them to go and check.**
  Changed on the owner's instruction, 2026-08-09. An earlier version made the
  count the finding and invited the reader to verify it, which asks a busy person
  to do our work. **Quoting three questions verbatim with who came back, and how
  many times out of five, is the same fact delivered instead of promised.** The
  falsifiability survives as one short clause at the end — "those are the exact
  words I used, if you want to try them yourself" — which is stronger than the
  paragraph it replaced, because they can now copy the question straight out of
  the email.
- **Only quote questions the practice is geographically eligible for.** The six
  are not interchangeable: two name a specific town. Citing the Birkenhead
  question at a practice in Upton hands them a fair objection and wastes the
  email. **q01, q04 and q06 are Wirral-wide and safe for anyone on the
  peninsula.**
- **Quoting the questions gives away a little of the question library**, which
  `ops/audit-questions.md` calls the thing that compounds. Judged worth it: three
  generic discovery questions for one trade are not the asset, the library across
  trades and areas is, and a client is shown the full ten before their audit runs
  anyway.
- **The verbatim answers are still worth sending — as the reply, not as the
  ask.** Somebody who answers is a warm lead, and a copy-paste of the paragraph
  naming their competitors is the strongest possible second touch. **Strip the
  source list first:** the sources are the diagnostic clue and they belong in the
  paid report.
- **Never claim the assistants disagree in general.** They mostly agree — 21 of
  39 practices are named by all three. A prospect who checks that claim finds it
  false and stops reading. The gap is per practice.
- **It gives the price in the third paragraph.** A cold email that hides the
  price reads as the start of a funnel, which is what the homepage was rewritten
  to avoid.
- **It links the self-audit rather than attaching a PDF.** An attachment from a
  stranger is a security prompt; the published page is checkable.
- **No jargon.** The email never names the industry acronym.

**Never offered, and this is a standing rule rather than a style note:** no free
audits, no introductory rate, no "first five clients" discount, no bundling the
audit with a monthly plan. Settled 2026-07-31, `ops/service-tiers.md` section 9.
A free audit is an introductory rate wearing a different hat.


---

## 6. The record, and the do-not-contact list

**Everything goes in the client record** (`ops/client-record.md`): who was
contacted, when, what the finding was, what came back. Nothing goes in this
repository — it is public in principle and a clinic owner's name and email are
personal data.

**The do-not-contact record is the one that must survive everything.** A reply
asking not to be contacted is recorded permanently, because the only way to
honour it is to still have it when the list is rebuilt in six months. `/privacy/`
already commits us to this in writing.

**This is the second reason `business.clientDataStorage` blocks the first send.**
There is currently nowhere to put the record, and an outreach batch with no
record of who was contacted is worse than no batch.

---

## 7. What actually happens — the numbers, and what we do not know

**Nobody has sent one of these.** Everything here is a hypothesis with a place to
write the real number next to it.

| What | Guess | Real |
|---|---|---|
| Clinics on the Wirral, per trade | Unknown | `[PLACEHOLDER]` |
| Reply rate | Low single figures | `[PLACEHOLDER]` |
| Replies per paid audit | Unknown | `[PLACEHOLDER]` |
| Approaches per paid audit | **The number the whole plan rests on** | `[PLACEHOLDER]` |

### Capacity, and the batch size that comes out of it

**Answered by the owner 2026-08-09: three hours a day comfortably, and more than
that for a paid audit**, because one £250 audit offsets a whole day of his other
earnings.

That second half is the more useful number, and it is worth stating on its own:
**an audit is budgeted at 2h40–3h30** (`ops/audit-method.md` §7), so at £250 it
pays roughly two and a half times what an hour of the owner's alternative work
does. **Delivery is not where the money is lost. Selling is.**

The arithmetic, so a later session does not redo it:

| | |
|---|---|
| Hours available | ~21/week at three a day, and flexible upward for paid work |
| Running the business | ~2.5/week (`HANDOVER.md` §8: daily inbox, weekly batch, monthly reconciliation) |
| Left for delivery | ~18/week, so **six audits a week**, or four without touching the flex |

**So the batch size is twenty, sent weekly**, and the binding constraint is not
what it was assumed to be:

- **Twenty is safe on delivery.** An implausibly good cold outcome — one in four
  replying *and buying* — is five audits, comfortably inside a week.
- **Twenty is barely enough to learn from.** Two or three conversations and
  possibly no sale is the realistic first batch. That is not failure, it is the
  sample size.
- **The real cap is the list, not the diary.** If the Wirral turns out to hold
  forty clinics across the four trades, we run out of prospects before we run out
  of hours. **The answer to that is to widen the area — Liverpool and Chester
  were the runners-up when the Wirral was chosen — not to send more per week.**

**The one stop rule:** do not send batch two while batch one has more than four
audits still owed. Everything else is judgement.

**Two things this exposes rather than settles.**

- **Nobody has timed an audit.** 2h40–3h30 is a budget, and the classification
  step inside it (60–110 minutes) has no prior estimate behind it at all —
  `ops/audit-method.md` §7 says so and asks for it to be timed separately.
  **Everything above is arithmetic on an estimate.** Time the Wardith run
  (`HANDOVER.md` step 4) before the batch size is treated as a fact.
- **Four audits a week is when the runner stops being deferrable.** The only
  thing that fires the API queries today is
  `ops/audits/noven-2026-08-02/audit_query.py`, which is marked throwaway and
  says to delete it. Deferring the real runner was deliberate and correct
  (`ROADMAP.md` 3a, `ops/audit-method.md` §7: written before audit one it is a
  guess at a spec) — but its release condition is the first real audit, and the
  first real audit is what this document is for.

**Weekly, per `HANDOVER.md` section 8:** send the next batch, record what came
back. Thirty minutes.

---

## 8. What replies unlock

Four copy changes are deliberately parked waiting on real outreach evidence
(`ROADMAP.md` 2g). They are listed here as well because this is the document that
produces their evidence:

- **Real objections become FAQ entries.** Only ones that were actually raised.
- **Which businesses reply and buy** decides whether the homepage's list of who
  this is for — accountants, solicitors, private clinics, consultancies,
  agencies — is right. It is currently a hypothesis, and this batch tests one
  fifth of it.
- **The first client's written permission** unlocks the case study that replaces
  the "we have no case studies" messaging everywhere it appears.
- **Standing constraint:** no new services or pages for completeness until 100
  prospects have been approached.

---

## 9. Considered and not done

- **Warm introductions first.** Closed 2026-08-09: the owner does not have the
  network. Not a deferral.
- **Buying a list.** Illegal in practice for anything but corporate subscribers,
  and worthless for a batch of twenty on one peninsula. Companies House is free
  and better.
- **LinkedIn outreach as the opening move.** `ROADMAP.md` 2e keeps it for later,
  and it stays there. Connection requests to strangers are a slower version of
  this email with less room for the finding.
- **A multi-step chasing sequence.** Rejected above, on the grounds that it is
  the thing that makes a cold email feel like spam rather than a message from a
  person down the road.
- **Cold calling.** Not ruled out, but PECR's rules on unsolicited calls and the
  TPS/CTPS registers are a separate piece of work, and nothing in this document
  covers it. Do not start it on the assumption that the email position applies.
