# Outreach process

*How we find and approach prospects. Five steps. The letters are at the bottom.*

**Status: first three sent 2026-08-10.** No replies yet, so every expectation
below is a guess.

---

## The five steps

### 1. Pick a sector and a genuine local competitive market

**Wardith operates UK-wide.** Prospecting is organised as **sector × genuine
local competitive market** — a geography chosen because it's where customers
actually buy, not because it matches an administrative boundary. Examples:
estate agents × Wirral, estate agents × Chester — examples, not rules. Each
run is scoped fresh to the trade and the area its customers actually use.

The trade needs customers who genuinely ask an assistant for a recommendation —
a trade that runs on referral has nothing for us to find.

### 2. Run the discovery questions once for the trade

Not once per business. Six questions × three assistants × five runs = **90
queries, about $15**, and it answers the question for every business in the area
at once. The runner is `tools/trade-run/`, the runbook is beside it.

```
python3 trade_run.py --questions questions-{trade}-{area}.csv \
    --client {trade}-{area} --out ~/wardith-runs/{trade}-{area}.csv --cap 90
```

**`--out` goes outside this repository.** Answer text names real businesses.

### 3. Build the market, then filter for outreach eligibility

**Build the real customer-facing competitive market from the strongest
appropriate sources for that vertical.** These may include:

- authoritative or regulated registers;
- major customer-facing portals/directories;
- official business websites;
- other credible sector sources.

The assistants' cited sources (the run's `sources_cited` column) may
contribute to the census but do not define the market. Fetch the strongest
sources for the trade, list every business that genuinely competes in the
chosen geography. That union is the market census.

**Companies House is a legal-entity and outreach filter — never the source of
the competitive market.** Wardith's operating policy: **only send unsolicited
email outreach to prospects verified as active Ltd companies or LLPs. Sole
traders and ordinary partnerships are excluded from this outreach process.**

> **No verified active Ltd company or LLP at that trading name, no email.**

Search by name at Companies House advanced search. **Do not build the market
census from a Companies House postcode or SIC-code sweep** — measured
2026-08-10, a SIC-code sweep of the Wirral returned 67 companies of which only
two were businesses worth writing to. The rest were dentists' personal service
companies. The sweep is a filter, never a source.

**Large or national chains may stay in the market benchmark** — they are real
competitors — **but normally drop out of local outreach** where there is no
realistic local purchasing decision-maker (check who the registered provider
is). Also drop anyone already named as consistently as its direct competitors —
there is nothing to sell them.

### 4. Find the gap, then qualify

**A strong Wardith prospect is a commercially credible business that is
materially underrepresented in AI recommendations relative to meaningful
direct competitors in its actual market.** Businesses named zero times remain
the highest-interest cases, but zero appearances are not required — a
credible, established business with several appearances can still be a
stronger prospect than a never-named one, if its direct competitors appear far
more often. Use the raw observed counts and judgement. No proprietary score,
visibility percentage or invented precision.

- **Named by nobody** → the absent letter. Still the strongest case.
- **Named occasionally, direct competitors named far more** → the same letter,
  one sentence changed to reflect the count.
- **Named, but absent from ChatGPT** → the ChatGPT-gap letter. Only when the
  missing assistant is ChatGPT; a gap on Perplexity alone is not worth a letter,
  because we cannot say what it costs them.
- **Named as often as its direct competitors** → not a prospect.

**Before a prospect is outreach-ready, verify:**

1. it genuinely operates in the selected sector;
2. it genuinely competes in the selected geography;
3. it has a defensible active Ltd/LLP legal-entity match;
4. it has a meaningful competitive AI recommendation gap;
5. there is a suitable evidenced business contact route.

**Ambiguous prospects are REVIEW, not assumed valid.**

**Batch of ten to twenty, weekly**, four or five a day rather than all at once.
One stop rule: do not send batch two while batch one has more than four audits
still owed.

### 5. Record it, then wait

Every send goes in the client record as it goes out — who, when, what the
finding was, what came back. **Nothing goes in this repository**; prospect names
are personal data. A reply asking not to be contacted is recorded permanently.

No chasing sequence. One finding, one offer. If it is not interesting enough to
answer once, sending it again does not improve it.

---

## Sending

- From `hello@wardith.co.uk` (Zoho). Display name **Kieran Smith**, not Wardith
  — in a reception inbox a person's name reads as correspondence.
- **One recipient per email. Never a CC, never a BCC list.** Twenty addresses
  visible to each other is a data breach and the end of the pitch at once.
- The normal Wardith signature goes on, image and all.
- No mail-merge, no tracking pixel, no read receipt.
- Weekday mornings beat evenings — reception triages first thing.
- To a named person wherever the site gives one.

## What every email must carry

Three things, all legal rather than stylistic:

1. **Who we are** — the trading name and the address for service (the signature
   carries both).
2. **Where we got their details**, in one line, accurately. This is the UK GDPR
   Article 14 disclosure. If they came off a directory, say the directory.
3. **A working opt-out**, honoured permanently.

## The letters

**Subject: the practice's own name, plus routing.** `{Business} — for {named
person}`, or `— for the practice owner` on a generic inbox. **No claim in the
subject and no technology word** — "ChatGPT" is the most common word in the
marketing email they already delete.

**Only quote questions the business is geographically eligible for.** Citing a
question that names a town they are not in hands them a fair objection.

**Never state a total count of businesses named** until the counting method is
settled — two methods have given two answers. State what was verified: that we
searched every answer for them and they are not there.

### The absent letter

> Hello,
>
> I'm Kieran Smith. I run a small business on the Wirral that checks what the AI
> assistants say when somebody asks them to recommend a local business.
>
> Last week I asked ChatGPT, Google's Gemini and Perplexity for a {trade} on
> {area}. Six different ways of asking, five times each, so ninety answers.
>
> Three of the questions, and what came back:
>
> "{q1}" — {A} in {n} of the fifteen answers, {B} in {n}.
>
> "{q2}" — {C} and {D} in all fifteen, {E} in fourteen.
>
> "{q3}" — {E} in all fifteen, {B} in thirteen.
>
> I went through all ninety answers looking for {business}. It isn't in any of
> them. Those are the exact words I used, if you want to try them yourself.
>
> One thing worth saying, because it's the first thing I'd want to test. I didn't
> ask about {business} by name. If you type the name in, all three will probably
> tell you plenty, and accurately. I asked the way somebody looks for a {trade}
> when they don't have one yet and don't know who you are. That's the question
> that brings in new customers, and it's a different question.
>
> A {business type} can be missing for a few different reasons and they aren't
> equally hard to fix. What I sell is finding out which one applies to you. Ten
> questions on {business} across all three assistants, where their answers are
> actually coming from, and a written report on what to change. It's £250,
> that's the entire cost, and the report is yours to act on with me or without
> me.
>
> If you want to see what one looks like first, I ran the same thing on my own
> business and published all of it, including what came back badly:
> wardith.co.uk/ask-your-ai/self-audit/
>
> Worth a look?
>
> Kieran Smith
> Birkenhead, Wirral
>
> I found {business} on {where}, and the rest from your own website. If you'd
> rather I didn't keep your details, tell me and I'll delete them.
>
> *[normal signature follows — it carries the postal address]*

**Named once or twice:** change "It isn't in any of them" to "It came up once,
in ninety answers."

**Writing to a gatekeeper:** open to reception, ask them to pass it on, and say
what it is in one line. Then cut the second greeting.

> Hello,
>
> You're probably getting a lot of AI emails at the moment. This one has an
> actual finding about {business} in it rather than a pitch — could you pass it
> to {named person}?

### The ChatGPT-gap letter

Same shape, with the middle replaced:

> Here is what ChatGPT gave back to three of them:
>
> "{q1}" — {A}, four times out of five.
>
> "{q2}" — {B}, {C}, {D} and {E}. All of them five times out of five.
>
> "{q3}" — {B}, {F} and {E}, again all five.
>
> {Business} wasn't named once, on any of the six. It does come up on Gemini and
> on Perplexity, so this is specific to ChatGPT.

...and the offer paragraph becomes "What I sell is the reason behind it."

---

## What the email gives away, and what it doesn't

**The observation is free. The diagnosis is the product.**

Free: what was asked, how many times, who got named, whether they did. All
checkable, none of it requiring us.

Not free: *why* they are missing, which pages the answers are built from, which
of those they are on, what to change. That is the £250.

**Never imply we don't know.** "There are a handful of reasons" is honest. A
hint that it is more mysterious than it is would not be.

## Never do

- Claim the assistants disagree in general. They mostly agree.
- Send the trade run to a prospect as if it were their audit. It is one finding;
  the audit is ten questions on their own business.
- Publish a ranked table of named local businesses. Naming a prospect's
  competitors privately, to that prospect, is a different act from publishing a
  league table. Only the first is in scope.
- Cold call. PECR's rules on calls and the TPS/CTPS registers are separate work
  and nothing here covers it.
