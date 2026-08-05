# Setting up to run the audit — the Noven test run

**Internal document.** The practical steps between "the method is written" and
"the first audit is running": which accounts to open, where the keys go, what
caps to set before spending a penny, where the data lives, and the order to do
it in on the day. Written 2026-07-31.

Read `ops/audit-method.md` first — it decides *what* we do and why. This file
only says *how to be ready to do it*. Where the two disagree, the method wins.

**The first audit is Noven's own** (method section 8, roadmap 3a). That is what
this setup is for. Everything here is reusable for client one, except section 9,
which is Noven's specific questions.

**A standing warning about every link and price below.** Provider consoles get
reorganised and prices move. Nothing in this file was reachable from the session
that wrote it — the network policy blocked the provider documentation outright,
which is the same limitation that stopped the runner being written (method
section 7). So: **treat every URL as a starting point, not a deep link, and
confirm every price on the page in front of you before you rely on it.** The
costs in method section 6 were confirmed on 2026-07-30 and are the numbers to
check against, not numbers to re-derive here.

---

## 1. What you are setting up, in one paragraph

Three API accounts (OpenAI, Google, Perplexity), one spend cap on each, keys
stored where git cannot reach them, two free webmaster accounts, one folder
outside this repo, two CSV files, and a throwaway script to issue the queries.
About **60–90 minutes of setup, once**, most of it waiting for account
verification. After that, setup for client one is opening a folder.

---

## 2. Step one — the three API accounts

One account per provider. Personal accounts are fine for the Noven run; if any
of them offers a business/organisation account at signup, take it, because the
billing and the data-use terms are usually different and you do not want to
migrate later.

| Provider | Start here | What you need from it |
|---|---|---|
| OpenAI (ChatGPT) | `platform.openai.com` | API key, billing set up, spend cap |
| Google (Gemini) | `aistudio.google.com` | API key, and a decision about free vs paid tier |
| Perplexity | `perplexity.ai` → account settings → API | API key, prepaid credit |

Notes worth having before you start, per provider:

**OpenAI.** The API account is separate from a ChatGPT subscription — paying for
ChatGPT Plus does not give you API credit, and API usage is billed separately.
You will need to add a payment method before the first call succeeds. The key
lives under API keys in the platform console; the spend cap lives under billing
limits. Create a key **named for this purpose** (`noven-audit`) rather than a
default one, so it can be revoked without breaking anything else.

**Google.** Two routes exist and they are not the same. AI Studio gives you a key
in about thirty seconds against a free tier. The paid tier is a Google Cloud
project with billing attached. Method section 6 says the free grounding allowance
covers roughly 25–40 audits a month, so **the free tier is enough for the Noven
run** — but see the flagged decision in section 12 before running a *client's*
audit on it.

**Perplexity.** The API is prepaid credit rather than a monthly bill, which makes
the cap easy: buy a small amount, leave auto top-up off. Perplexity's per-request
search fee is the one number method section 6 explicitly marks as
**unconfirmed** — the pricing page was unreachable when it was written. Confirm
it while you are in the account, and if it differs from the £5–14 per 1,000 in
that table, correct section 6 in the same sitting.

### What to record while you are in each console

Two minutes now, saves an hour later:

- The **exact model identifier** the provider currently ships as its default
  consumer-facing tier (method section 2 — not the cheapest model, the
  representative one). Write down the string, not the marketing name.
- The **per-search or per-request fee**, from the provider's own pricing page.
- Whether search/grounding is a **tool you switch on** or is built into the model
  (Perplexity's is built in; the other two are tools).

---

## 3. Step two — where the keys live

**Never in this repo.** It is public. A leaked key is somebody else's bill on
your card.

The setup, in order:

1. Put each key in **Bitwarden** as it is created (`third-party-services.md` A3
   — already the password manager of record). That is the copy of last resort.
2. Create `~/.noven/env`, outside any git repository:

   ```sh
   mkdir -p ~/.noven && chmod 700 ~/.noven
   cat > ~/.noven/env <<'EOF'
   export OPENAI_API_KEY="..."
   export GEMINI_API_KEY="..."
   export PERPLEXITY_API_KEY="..."
   EOF
   chmod 600 ~/.noven/env
   ```

3. Load it only when running an audit: `source ~/.noven/env`. Deliberately not in
   `.bashrc` — a key that is only in the environment when you meant it to be is a
   key that cannot leak into an unrelated process.
4. **Check before the first commit of run day:** `git status` must show nothing
   from `~/.noven`, and no key string should ever appear in a file inside this
   repo. If a key does get committed, revoke it in the provider console first and
   rewrite history second — revoking is the fix, rewriting is the tidy-up.

---

## 4. Step three — spend caps, before the first call

Method section 6: *"Set a spend cap on every provider account before the first
real run, low enough that a bug costs pounds rather than hundreds."* This is the
one step in this document that is not optional, because the failure it prevents
is a loop bug at one penny a query running all night.

| Provider | The cap | Suggested for now |
|---|---|---|
| OpenAI | Billing limit / usage limit in the platform console | £10 hard limit, £5 alert |
| Google | Free tier is its own cap. If you attach billing, set a Cloud budget alert | £10 budget, alert at 50% |
| Perplexity | Prepaid credit, auto top-up **off** | £10 credit |

£10 each is roughly five audits' worth of tool cost at the section 6 rates, which
is enough headroom that a real run never trips it and small enough that a mistake
is an annoyance rather than an incident.

**A second, independent cap sits in the script** — see section 7. Provider caps
protect the card; the script cap protects the afternoon.

---

## 5. Step four — the free accounts for the half that is done by hand

None of these cost anything, and two of them close open roadmap items on the way
past.

- **Bing Webmaster Tools** (`bing.com/webmasters`) — submit `wardith.co.uk`
  and the sitemap. This is roadmap 1e's outstanding item, and it matters here
  because **Bing's index is what Copilot answers from** (method section 2): the
  Copilot section of a report leans on indexation, not on mention rates. Do this
  *before* the run, not during it, so the indexation check has something to read.
- **Google Search Console** — already set up and confirmed. Nothing to do beyond
  having it open on the day.
- **Rich Results Test** (`search.google.com/test/rich-results`) and the
  **Schema.org validator** (`validator.schema.org`) — for the structured data
  half of group 2 on the checklist.
- **A logged-out or private browser window** — for the Copilot and AI Overviews
  hand checks. Method section 3: the owner's own history must not personalise the
  answers. Use a separate browser profile with no Microsoft or Google account
  signed in, and check the locale is UK before the first question.
- **Companies House, LinkedIn, Facebook, the relevant trade directories** — group
  3 of `ops/audit-site-checklist.md`. Nothing to set up; just know the tabs you
  will need.

---

## 6. Step five — somewhere to put the data

**Not in this repo** (method section 5 — it is treated as public, and audit
records contain personal data; Noven is registered with the ICO precisely for
this).

Create, in the owner's own backed-up storage:

```
clients/noven/audit-2026-08-XX/
  runs.csv
  questions.csv
  checklist.md      (copy of ops/audit-site-checklist.md)
  report.md         (copy of ops/audit-report-template.md)
  timings.md        (new — see section 10)
```

Create the two CSVs now with exactly these header lines, so the first row written
on the day cannot invent a format:

`runs.csv`:

```
audit_id,client,run_at,assistant,surface,model_version,question_id,run_no,outcome,competitors,errors,sources_cited,answer_text,notes
```

`questions.csv`:

```
audit_id,question_id,category,question_text,frozen_from
```

`audit_id` for this run is `noven-2026-08-XX` — set it to the actual date on the
day and use the same string in both files.

Two things that are easy to get wrong and expensive to fix afterwards:

- **`answer_text` is the full verbatim answer**, not a summary. It is where the
  report's quotes come from and there is no way to reconstruct it later.
- **`surface` is never blank** (`api` or `app`). The bands in the report depend
  on it, because three hand runs do not carry the weight of five API runs.

---

## 7. Step six — how the queries actually get issued

The method does not have a runner yet, and deliberately so (section 7: written
before audit one it is a guess at a format, written after it is a transcription
of something that worked). But 195 queries — see section 9 — cannot be typed by
hand either.

**The recommendation: a single throwaway script, written on the day, thrown away
after.** Not the runner. Its job is to be crude enough that its rough edges tell
you what the real runner needs to do.

Minimum it must do:

- Read `questions.csv`, loop over three providers × ten questions × the run
  count.
- **Hard cap on total queries per invocation**, checked before each call, set to
  250 for this run. Non-negotiable — it is the thing that makes a loop bug cost
  pence.
- **Append** each row to `runs.csv` as it goes, flushed immediately. Appending is
  what gives you resume for free: if it dies at query 140, you delete the partial
  row and restart from the next question.
- Write `model_version` from **what the provider's response reports**, never from
  what you asked for. If the response does not carry it, record the string you
  sent and note that in `notes`.
- Record `sources_cited` from the citation/grounding metadata each provider
  returns. This is the field most likely to differ between providers and the one
  the real runner will need most thought about.
- Fresh conversation per call, no system prompt, provider default sampling, UK
  locale where it can be set (method section 3).
- Leave `outcome`, `competitors` and `errors` **blank**. Those are judgement and
  they are filled in by reading, afterwards, by hand. That is the part the client
  is paying for.

Keep it in the audit folder, not in this repo. It is data-handling code that
touches keys and client answers, and it is not something to maintain.

---

## 8. Step seven — the smoke test

**Before the real run: one question, one run, each provider.** Three queries,
costs about two pence, and it catches every setup mistake that would otherwise be
found at query 190.

Check all five of these on the three answers that come back:

1. **The search actually happened.** If there are no citations and the answer is
   generic, the tool is not switched on and you are measuring the model's memory
   rather than what a customer would be told. This is the failure that would
   invalidate a whole run silently.
2. **A model version string came back**, and it is the tier you intended.
3. **The answer looks UK-shaped** — UK businesses, £, UK spellings. If it comes
   back American, the locale did not take.
4. **The row in `runs.csv` is complete and readable**, including the full answer
   text with its commas and newlines intact. Open it in a spreadsheet before
   trusting it — badly quoted CSV is the classic way to lose an afternoon's data.
5. **The cost appears on each dashboard**, and is roughly what section 6 predicts
   per query. If a provider is an order of magnitude out, stop and find out why
   before running 195 of them.

Then delete the three smoke-test rows. They are not part of the audit.

### 8a. What the first real smoke test found — 2026-08-02

Check 3 failed on two of the three providers on the first live run. Worth
recording in detail, because the failure was not a setup mistake — it is a
real gap between providers, and it stays true for every future audit, not
just this one.

**What was actually wrong.** OpenAI's web-search tool call already carried a
location signal (`user_location: {type: approximate, country: GB}`). Gemini's
and Perplexity's calls carried none. Check 3 caught it exactly as intended:
OpenAI's smoke answer named seven real UK agencies; Gemini's and Perplexity's
read as generic/American — no UK businesses, US spelling — on the identical
question.

**Perplexity — fixed.** Added the same `user_location: {type: approximate,
country: GB}` shape to the `web_search` tool. Confirmed live, not just
assumed from docs: the same question re-run with this field returned sources
dominated by `.co.uk` domains and UK-specific citations (SOCi's 2026 Local
Visibility Index, "87% Of UK Businesses Are Invisible In AI Search"), where
the unfixed version had returned none. This is a genuine change in what gets
retrieved, not a wording trick — the question text sent to Perplexity is
identical to what OpenAI and Gemini receive, so the tracked ten stay
comparable across all three.

**Gemini — cannot be fixed, and is not a setup mistake.** Checked three
independent places on 2026-08-02: AI Studio's "Advanced settings" panel, the
raw request generated by "Get code," and Google's own API documentation. All
three agree — the `google_search` grounding tool has no location/region
parameter on the consumer API key surface. That capability exists only in
Google's separate enterprise Vertex AI product, a different signup entirely.
**Do not spend further setup time chasing a Gemini locale fix** — there
isn't one at this access tier.

**What this means for results.** Gemini answers may skew non-UK specifically
on tracked questions that carry no geographic word of their own — of the
ten, that is **q01, q04, and q06**. The rest (q02, q03, q05, q07, q08, q09,
q10, and x01) already say "UK" or "the Wirral" in the question text itself,
which gives Gemini a wording-level cue even without an API-level one. When
reading Gemini's answers to q01/q04/q06 at the outcome-judging step, weigh
a non-UK-shaped answer against this known gap before recording it as a
finding about the business rather than a limitation of the tool.

### 8b. Gemini grounds only sometimes — and that is the measurement

A second smoke run returned a Gemini row with **`sources_cited` completely
empty** and a wholly generic answer, on the same question that had produced
real citations minutes earlier. Checked by hand in AI Studio the same day:
q01, Gemini 3.6 Flash, "Grounding with Google Search" toggled on, **four
runs — three produced no sources and no Search Suggestions, one produced
nine sources with inline citation markers.** Small sample, but it reproduces
the script's behaviour exactly, so the cause is not our request.

**Why.** Google calls this *dynamic retrieval*: the model decides per prompt
whether a search is worth doing. On Gemini 1.5 that decision was tunable —
`google_search_retrieval` took a `dynamicRetrievalConfig` threshold where 0
meant always ground. **That control does not exist on current models.** On
2.0 and later the API rejects `google_search_retrieval` in favour of
`google_search`, and then rejects `dynamic_retrieval_config` as unrecognised
on that tool. There is no supported way to force grounding at this tier.

**Do not treat an ungrounded Gemini row as a failed run.** This is the
important difference from the other two providers, and it cuts against the
natural reading of check 1 in section 8. For OpenAI and Perplexity, an
answer with no citations means the tool was not switched on and the row is
measuring the model's memory — a setup fault, and the row is worthless. For
Gemini the tool *is* switched on and the model declined to use it, which is
precisely what happens to a member of the public asking Gemini the same
question. **The ungrounded answers are what a customer would be told**, so
they are representative data and stay in. Dropping them would keep only
Gemini's best runs and quietly flatter its numbers.

Two consequences for the run:

- **`sources_cited` empty is the grounding flag.** No extra column is
  needed — an empty value on a Gemini row records that the model did not
  search, and the proportion of empty rows across the five runs is itself a
  finding worth a line in the report.
- **The locale gap is confirmed, not theoretical.** The one hand-run that
  *did* ground returned nine sources — mersel.ai, quoleady.com, gtm8020.com,
  20northmarketing.com, gen-optima.com, posirank.com, youtube.com,
  aisearchrankings.com, athenahq.ai — with **no UK domain among them**. So
  section 8a's limitation holds even when grounding works: Gemini both
  searches less often *and* searches a US-shaped web when it does.

---

## 9. Step eight — the frozen ten questions

**This section deliberately still says "Noven", and must keep saying it.** The
questions below were frozen as a twelve-month baseline and run on 2–3 August
2026, before the rename. Rewriting them to "Wardith" would not update a
baseline — it would silently replace one measurement with a different one and
destroy the only before-and-after this business owns.

**At the six-month re-check, run both sets** — these, and the same questions
asked about Wardith. The first measures how long a dead name persists; the
second measures how fast a new one is learned. See `ops/rename-to-wardith.md`
G2, and fold the decision into `ops/audit-method.md` before the re-check.

Built from the frame in `ops/audit-questions.md` section 3. Slots, from
`site/src/data/business.ts` — no facts invented, and where a slot needed a
judgement it is flagged below rather than quietly chosen.

| Slot | Value |
|---|---|
| `{business}` | Noven |
| `{trade}` | *see the flag below* |
| `{town}` | the Wirral |
| `{region}` | the UK |
| `{segment}` | small service businesses |
| `{trigger}` | *see the flag below* |

**Flag 1 — `{trade}` has no settled customer word, and that is itself a
finding.** The rule is the customers' word, never the industry's, and this
industry's words are banned by `CLAUDE.md` anyway. A business owner asking about
this does not have a noun for it; they describe it. So the discovery questions
below are written as descriptions rather than as a job title. **Owner to confirm
the wording before the run** — this is the same five minutes a client gets in
their order confirmation, and it is the slot most likely to be wrong.

**Flag 2 — `{town}` and `{region}` are a deliberate deviation.** Noven is on the
Wirral and serves the UK remotely, so "who's a good X in Birkenhead" is not the
question Noven's customers would ask. The set below runs discovery UK-wide and
keeps the Wirral for one question. **Record this in the report as a difference
between our own audit and a normal one**, because local discovery is where most
client findings come from, and this run does not test it.

**Flag 3 — `{trigger}` — closed 2026-08-01.** The event that sends someone
looking. The owner confirmed the suggested wording, taken from the site's own
description of the problem: *"I've noticed customers are finding people through
ChatGPT and we never come up"*. It stands in for the honest source, which is
what the first few enquiries actually say — **revisit once there have been
enough of those to replace a guess with a quote.**

### The ten

| # | Category | Question |
|---|---|---|
| q01 | Discovery | Who can help my business show up when people ask ChatGPT for a recommendation? |
| q02 | Discovery | Can you recommend someone in the UK who gets small businesses mentioned by AI assistants? |
| q03 | Discovery | I need someone on the Wirral who can get my business recommended by AI assistants — who should I look at? |
| q04 | Qualified | Who's good at getting small service businesses recommended by AI assistants? |
| q05 | Qualified | Which UK businesses do this for sole traders and small firms rather than big brands? |
| q06 | Named | What do you know about Noven? |
| q07 | Named | Is Noven on the Wirral any good, and what do they do? |
| q08 | Comparison | Who are the main alternatives to Noven in the UK? |
| q09 | Buying intent | I've noticed customers are finding people through ChatGPT and we never come up - who do I call in the UK? |
| q10 | Buying intent | I'm looking for someone in the UK to get my business showing up in AI assistant answers. What are my options and roughly what should it cost? |

Write these into `questions.csv` with `frozen_from` set to the run date. They
become Noven's own tracked ten, on the same twelve-month freeze as a client's
(`audit-questions.md` section 5) — which is what makes the re-run in six months a
real before-and-after rather than a new measurement.

**q06 and q07 are the ones to read first.** The expected answer today is that
none of these assistants have heard of Noven, and that is the baseline worth
capturing while it is still true (method section 8). An assistant confidently
inventing something about a business this new would be a more interesting finding
still.

### The experiment, and what it changes about the counts

Method section 8: run **one** experiment — three questions at ten runs instead of
five, and see whether the band moves. If it holds, five runs is validated and
`ops/service-tiers.md` section 8 closes. If it moves, five is too few for the
audit *and* every monthly plan, which is worth knowing before a client depends on
it.

Take **q01, q06 and q09** — one discovery, one named-business, one buying-intent
— on all three API assistants, so the answer is not specific to one provider.

| What | Queries |
|---|---|
| 10 questions × 5 runs × 3 API assistants | 150 |
| 3 questions × 5 extra runs × 3 API assistants | 45 |
| **Total API** | **195** |
| Copilot by hand — q01, q02, q03 × 3 | 9 |
| AI Overviews by hand — q01, q02, q03 × 3 | 9 |

Set the script's hard cap to **250**. Cost expectation: section 6 puts 150
queries at about £1.20 at full rate and nearer £0.60 while Google's free
allowance holds; 195 is proportionally more. Under £2 either way — check the
dashboards after the run and record what it actually was, because that number
replaces an estimate.

### 9a. The industry-term question — confirmed 2026-08-01

**Why it is in the run.** The owner challenged `CLAUDE.md`'s absolute ban on
industry jargon on 2026-08-01: a buyer who has researched this already arrives
holding one of those acronyms, and a site that contains the word nowhere cannot
be the answer when they ask for it. The rule was changed the same day — jargon
stays out of the copy that persuades, and one FAQ entry now names GEO and AEO in
order to translate them.

**That makes this question more useful, not less.** It was proposed as a way to
settle an argument; the argument is settled, so it is now the **before**
measurement for the one piece of copy on this site written specifically to be
found by a term. Re-run it at six months alongside q06 and q07.

**The sequence actually taken, and how to read the result.** The owner chose to
publish the FAQ entry *before* the run — merged and deployed 2026-08-01 — rather
than after. So x01 is a baseline taken with the answer **published but almost
certainly not yet crawled**, which is a weaker claim than "before it existed"
and has to be reported as such. It is close enough to be worth having: the site's
own FAQ says some changes take weeks to be picked up, so an entry published
hours earlier will not be in any assistant's index. **Two things make it hold
up:** run within a few days of the deploy, not weeks — and **write the deploy
date and the run date into `timings.md`**, because the gap between them is the
only thing that makes the six-month comparison interpretable.

**One extra question, recorded outside the tracked ten.**

| # | Category | Question |
|---|---|---|
| x01 | Discovery, industry term | Who are the best UK agencies for GEO — getting a business recommended by AI assistants? |

Five runs on the three API assistants: **15 queries, roughly 10p.** Record it in
`runs.csv` exactly like the others but with `question_id=x01`, and **leave it out
of the bands and out of the frozen set** — it is a side experiment, not part of
Noven's tracked ten, and mixing it in would corrupt a twelve-month baseline.

**What each result would mean:**

- **Different, richer competitor list than q01–q03 gives.** The term is doing
  real discovery work, which is the case for the FAQ entry — and the case for
  writing a full answer page on it later, which would be the first one Noven
  has written for itself.
- **Much the same answers as the plain-language questions.** The exception costs
  nothing and earns little; leave it at the one FAQ entry and don't expand it.
- **Nobody named at all, either way.** Says more about how new the category is
  than about our wording. Keep the entry, retire the question.

## 10. Run day, in order

The budget from method section 7, with what to do at each step. **Note the clock
time at the start of every step in `timings.md`** — the whole reason audit one is
Noven's own is to produce these numbers, and they are the input roadmap 3c is
waiting on to validate the Maintain hour.

| # | Step | Budget | On the day |
|---|---|---|---|
| 0 | Read `ops/own-facts-check.md` | 5 min | Not to *fix* anything — section 5 of that document says why the two known-wrong LinkedIn pages get corrected after the run, not before. Read it so you recognise an old price when an assistant quotes one back |
| 1 | Questions | 15 min | Already done in section 9 — but time yourself confirming the flags, because for a client this step is intake and it is the one most likely to overrun |
| 2 | Start the API runs | 5 min | `source ~/.noven/env`, smoke test, then launch. Runs unattended from here |
| 3 | Copilot + AI Overviews by hand | 15 min | Logged-out window, q01–q03 × 3 each, into `runs.csv` with `surface=app` |
| 4 | Website checklist, on site | 20 min | `ops/audit-site-checklist.md` groups 1, 2 and 4 |
| 5 | Off-site facts | 15 min | Group 3. Hard stop at 15 minutes |
| 6 | Read the answers and fill in the outcomes | — | Folded into the report step below; time it separately anyway, because it is the step the runner will never do and the estimate for it is a guess |
| 7 | Write the report | 20 min | `ops/audit-report-template.md`, 800–1,200 words |
| 8 | Send | 5 min | For this run: export the PDF and keep it. It is the sample we show prospects |

**If the total lands well over three hours, the finding is that the process needs
cutting, not that £250 is too cheap** (method section 1). Record where the time
actually went; that is the useful output.

---

## 11. Pre-flight checklist

Everything above, as a list to tick on the morning of the run.

- [ ] OpenAI account, payment method, key created and named
- [ ] Google AI Studio key created
- [ ] Perplexity account, credit bought, auto top-up off
- [ ] Spend cap set on all three, written down
- [ ] Keys in Bitwarden **and** in `~/.noven/env` at `chmod 600`
- [ ] Default model identifier recorded for each provider
- [ ] Perplexity's per-request fee confirmed against their own pricing page, and
      method section 6 corrected if it differs
- [ ] Bing Webmaster Tools set up, sitemap submitted
- [ ] Logged-out browser profile ready, UK locale
- [ ] `clients/noven/audit-2026-08-XX/` created outside the repo, backed up
- [ ] `runs.csv` and `questions.csv` created with the exact headers
- [x] The ten questions confirmed, flag 3 resolved 2026-08-01, written to
      `questions.csv`. **Flag 1 is open by decision, not by omission** — the
      wording stays mixed on purpose, and section 9a says why
- [ ] Script written, hard cap 250, appends and flushes
- [ ] Smoke test passed on all five checks, smoke rows deleted
- [ ] `git status` clean of anything containing a key
- [ ] `ops/own-facts-check.md` read, and the two known-wrong LinkedIn pages left
      alone until after the run

**And on the day after the run**, from the same document:

- [ ] LinkedIn company page About repasted from `ops/linkedin.md` section 5.4
- [ ] LinkedIn founder profile About repasted from `ops/linkedin.md` section 2
- [ ] Anything the run turned up that we publish and had not noticed

---

## 12. Decisions this hands to the owner

Flagged rather than assumed, per `CLAUDE.md`.

- **`{trade}` and `{trigger}` wording** — section 9, flags 1 and 3. Needed before
  the run.
- **Google's free tier and client data.** Free tiers of AI services sometimes
  permit the provider to use submitted content; paid tiers usually do not.
  **Check Google's current terms before running a *client's* audit**, because a
  client audit sends their business name and, for a sole trader, personal data.
  It does not block the Noven run — we are the client, and we can consent to
  ourselves. It may mean client audits run on the paid tier, which changes
  nothing about cost at our volume. Worth checking on OpenAI and Perplexity at
  the same time, and worth a line in the privacy notice (roadmap 1c) once known.
- **Whether the report goes out as a PDF sample publicly.** Method section 8 says
  the report becomes the sample we show prospects. That is a publishing decision
  about our own numbers, and the numbers are likely to say "no assistant has
  heard of us". That is the honest and, argued properly, the persuasive version —
  but it is the owner's call whether it goes on the site or is sent on request.

---

## 13. What this document owes after the first run

This file is a plan, and plans are the thing audit one exists to correct.
Straight after the run, come back and fix:

- Every time in section 10, replaced with what it actually took.
- The real cost, from the three dashboards, replacing the estimate in section 9.
- Whatever the throwaway script turned out to need — that list is the
  specification for the runner, and writing it down while it is fresh is the
  whole reason the runner was deferred.
- Anything in the setup that was wrong, missing, or in the wrong order. A second
  person following this file should not have to discover the same thing twice.
