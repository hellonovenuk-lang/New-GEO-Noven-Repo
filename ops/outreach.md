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

### The sweep is the filter, never the source — measured 2026-08-10

**This section used to read as though the 67 were the prospect list. They are
not, and the gap is now a number rather than a worry.** Of the twelve practices
that survived every test and made the first batch, **two appear anywhere in the
67.** The rest are registered under a company name that looks nothing like the
practice, or outside the peninsula entirely.

**What the 67 actually contains is dentists' personal service companies**, named
after people or after nothing — the flagged 17 was an undercount. As a list of
businesses to write to it is close to useless.

**So run it the other way round.** Build the candidate list from the trade run
and the directory census below, then use Companies House **by name** to answer
"is this a live company" for each one. That is what §2 asks for and it is all
the sweep was ever good for. **One caution: Companies House free-text search
matches any word in the query and returns thousands of rows**, so the check is
per-practice against the company's own registered name, not a keyword hunt.

**The sweep does keep one job.** It surfaces practices that appear in no
assistant answer at all — three of the first batch came from it and from nowhere
else — so it stays, as a source of *candidates to check*, not of prospects.

**Wirral postcodes: CH41–CH49, CH60–CH63.** CH64 is Neston, on the peninsula but
in Cheshire West, so it is a judgement call rather than an obvious yes. **Check
this list too** — a postcode district that turns out to be Chester puts the
"we're local" line in the email into an outright false claim.

**The registered office is not always the clinic.** Many use their accountant's
address. Match on trading address from the clinic's own website, and use
Companies House only to answer "is this a company".

**What we record per prospect** is in `ops/client-record.md` — the prospect
fields are already decided there. Do not invent a second schema.

**Size of the first batch: dental is answered, the other three are not.**
67 limited companies before triage (above), of which some meaningful fraction are
real patient-facing practices. `[PLACEHOLDER: the triaged figure, once the CSV
has been worked through.]` `[PLACEHOLDER: the same sweep for cosmetic,
physiotherapy and veterinary.]` **On the dental number alone, one trade does not
fill a twenty-a-week batch for long** — which is the §7 point about the list
being the binding constraint, arriving earlier than expected.

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

### How the tier was actually built — 2026-08-10, and this is the repeatable method

**Take the five directory pages the run's own `sources_cited` column shows the
assistants reading**, fetch each one, and list every practice on it. Add the NHS
practice list for the area and the Companies House sweep. That union is the
census. **Subtract every business the mention table names, then verify each
survivor by searching all ninety answer texts for its name** — absence from a
summary is not absence from the data, and two candidates failed exactly there,
turning out to be named once.

**It works, and it is cheap.** Nine practices at a verified zero across all
ninety answers, plus two named exactly once. Every one of them sits on a page
the assistants demonstrably read.

**Two things it caught that a name list alone would not have.** Two of the
zero-mention practices are **corporate chains trading under a local name** — one
Bupa, one Rodericks — which fail the good-first-client test and would have been
wasted letters. And one has **let its website domain lapse**, which is a fact
about why it is invisible and a delicate thing to raise.

**The census is a floor.** Two of the cited directories refuse automated access,
so more prospects exist than this method returns. That is the right direction to
be wrong in.

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

**Every "of thirty-nine" in this section is provisional.** A recount on
2026-08-10 over the same 90 rows, using the Companies House and directory names
as the candidate list, returned **fifty-four**. The two methods disagree, the
ratios above are built on the smaller one, and **no total goes in a letter until
they are reconciled** — §5 has taken the number out of both drafts. The
per-practice counts are unaffected: those are matched directly against the
answer text and were re-verified name by name.

**Rewrite the §5 draft around it.** The draft was written before the run and
makes the weaker "you are not mentioned" claim. **Done 2026-08-10** — see the
reordering note at the head of the drafts.

**Amended 2026-08-10 by the owner, and it cuts the Draft A pool by two thirds.**
The per-assistant gap is only worth a letter **when the missing assistant is
ChatGPT**. The finding as stated above treats the three as interchangeable, and
they are not: a practice told it is invisible on Perplexity will ask what that
costs them, and **we cannot answer** — the run measured what the assistants say,
not what they refer. Leading with a gap we cannot price is a bad opening for a
£250 sale.

**Worse, the ranking it produced was upside down.** Sorting by size of contrast
put a practice named twelve times out of fifteen by ChatGPT at the top of the
batch. That practice does not have a problem, and a well-written letter telling
them so buys a shrug and costs one of the twenty.

**So: absent from ChatGPT is a finding. Absent from Perplexity alone is not.**
Of eleven candidates ranked this way on 2026-08-10, three survived.

**And the deeper correction, which is the one that will drift back.** §4 above
rejects "you are not mentioned" because it is not *distinguishing* — if 90% of
the peninsula is unnamed, the fact cannot tell you who to write to. **True, and
it is an argument about targeting.** It was then used to reject the claim as an
*email*, which does not follow. A letter does not need its finding to be rare,
only true, checkable and worth acting on. **Two different tests, collapsed into
one.** The never-named are the first batch; the census method above is how they
are found.

**One risk comes with that, and it is delivery, not targeting.** For a
never-named practice the honest diagnosis is often "you are not on the pages the
assistants read", and the most evidenced fix is a free directory listing. If a
£250 report comes down to that, the price looks wrong — which the rule in §5
already answers: **that means the audit has to do more, not that the customer
was the wrong pick.**

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

**Reordered 2026-08-10, and the labels are now the job rather than a letter.**
The two drafts used to be presented A-then-B, which put the per-assistant letter
first and read as the default. It is not the default any more — §4's amendment
made the never-named the first batch. **"The absent letter" below was Draft B
and "the ChatGPT-gap letter" was Draft A**, so the references further down this
section still resolve.

**Three fixes applied at the same time, all of them consequences of the change
of target:**

- **The count of named practices comes out of both letters.** They said "thirty
  nine practices got named". A recount on 2026-08-10 from the same 90 rows,
  using the Companies House and directory names as the candidate list, returned
  **fifty-four**. Two methods, two answers, and **neither is safe to state in a
  cold email until they are reconciled.** What is not in doubt is the bit that
  matters — that a named practice was searched for across all ninety answer
  texts and is not there — so the letters now make that claim and drop the
  total. `[PLACEHOLDER: the reconciled count of practices named.]`
- **The source line has to say where we actually found them.** Both letters
  said "I found the practice through Companies House". That was true when the
  list was built from the SIC sweep. **It is now false for most of them** — the
  never-named are found on the NHS practice list and the directories, and
  Companies House is only used afterwards to check the company is live. Under
  UK GDPR this line is the Article 14 disclosure, so it has to be accurate
  rather than approximately right.
- **A practice named once needs one word changed**, not a different letter. See
  the note after the absent letter.

**The absent letter — for a practice named in none of the ninety answers.** This
is the first batch.

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
> I went through all ninety answers looking for [practice]. It isn't in any of
> them. Those are the exact words I used, if you want to try them yourself.
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
> I found [practice] on the NHS list of Wirral dentists and on [directory], and
> the rest from your own website. If you'd rather I didn't keep your details,
> tell me and I'll delete them.

**For a practice named once or twice, change one sentence and send the same
letter.** "It isn't in any of them" becomes "It came up once, in ninety
answers" — everything else holds, and it is a stronger opening than the absent
version because it is more obviously a real count rather than a failure to
look.

**The ChatGPT-gap letter — for a practice named by Perplexity or Gemini and
absent from ChatGPT.** Only when the missing assistant is ChatGPT, per §4. A gap
on Perplexity alone does not earn a letter.

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
> I found [practice] on [where], and the rest from your own website. If you'd
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

### Sending it — the mechanics

*Written 2026-08-10, when the owner asked what actually has to happen to start.
Everything above is what the email says; this is how it physically goes out.*

**From `hello@wardith.co.uk`, the Zoho mailbox, and nothing else.** Not the
Gmail account — that is an identity that owns logins, not a mailbox
(`ops/accounts.md`). Authentication is already good: SPF, DKIM and DMARC were
confirmed passing in a real delivered message during the rename
(`ops/rename-to-wardith.md`). **DMARC is still `p=none`**; raise it to
`p=quarantine` once a batch has gone out clean, not before.

**One recipient per email. Never a CC, never a BCC list.** Twenty clinic
addresses visible to each other is a personal data breach and the end of the
pitch in the same moment.

**Typed or pasted into an ordinary compose window, in plain text.** No
mail-merge tool, no tracking pixel, no read receipt, no shortened links, no HTML
signature or logo image. Each of those is a thing a person writing to one
business would not do, and each of them is a thing a spam filter scores. The
email's whole claim is that it came from someone down the road who ran the
questions himself.

**Spread twenty across the week — four or five a day, weekday mornings.** A
domain two months old that has sent almost nothing, suddenly sending twenty
near-identical messages inside an hour, is the shape of the rule rather than the
exception. The batch is weekly anyway (§7); there is no reason to send it in one
sitting.

**To a named person wherever the practice's own site gives one.** `info@` is the
fallback, not the default — the drafts open "Hello [name]" because a letter to
nobody reads as a circular.

**Paste the sent email into the record as it goes** (§6), not at the end of the
day. The record is what makes a second approach impossible and an opt-out
permanent, and it is worthless if it is reconstructed from memory.

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
