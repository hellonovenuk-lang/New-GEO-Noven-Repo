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
queries, about $5**, and it answers the question for every business in the area
at once. The runner is `tools/trade-run/`, the runbook is beside it. `/90qrun`
(`.claude/skills/90qrun/`) automates this whole step end to end, from just
the trade and place name.

```
python3 trade_run.py --questions questions-{trade}-{area}.csv \
    --client {trade}-{area} --location {area} \
    --out ~/wardith-runs/{trade}-{area}.csv --cap 90
```

**`--location` is the plain-English place name** (e.g. `Chester`, not the
slug) — it feeds Perplexity's own search step, the only one of the three
providers with a geography parameter at this API tier.

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
is).

**Being named as consistently as its direct competitors is not, by itself, a
reason to drop a business — being in the small cluster already dominating
that market's answers is (2026-08-24).** The Chester and Wirral
retrospective (2026-08-14) first showed that visibility alone was too narrow
a reason to drop a business: a business with a strong existing AI position
is a `DEFEND` opportunity, not a dead end. The 2026-08-24 refinement narrows
that back, deliberately: not every visible business, only the small
most-named cohort of a market (as few as one business, or as many as five)
now defaults to excluded from this round by default — a `DEFEND` business
outside that cohort is still pursued exactly like `GAP`/`GROWTH`. See step 4.

### 4. Classify the opportunity, then qualify

**Low AI visibility is not the only commercially interesting condition.** A
business with meaningful existing visibility can be a stronger prospect than
a zero-mention one. Every credible business's AI recommendation position
falls into one of three commercially distinct opportunity types — not a
single "prospect or not" test — plus a fourth non-opportunity bucket
(calibrated against the completed Chester and Wirral retrospective,
2026-08-14):

- **GAP** — credible and materially underrepresented relative to genuine
  direct competitors. Named by nobody is the clearest case and remains the
  strongest, but zero appearances are not required — low or inconsistent
  counts against competitors named far more often qualify too, provided the
  gap is real rather than simply explained by being new, tiny, specialist or
  outside the actual market.
- **GROWTH** — already has meaningful AI visibility, but sits materially
  below the genuine leaders, is inconsistent between models, is absent from
  one provider despite presence elsewhere, or shows up only for a narrow set
  of questions. **Never describe a GROWTH business as invisible — it isn't.**
  Do not reject a business merely because it already appears relatively
  often.
- **DEFEND** — already one of the market's AI visibility leaders, credible
  and commercially capable. The opportunity is to show what's supporting
  that position, monitor it, and flag if it starts to erode. **Do not
  manufacture a visibility problem for a business that doesn't have one.**
  **A business in the small cluster already dominating a market's answers
  (as few as one, as many as five — the "most-named cohort") defaults to
  excluded from this round of outreach (2026-08-24), reason `ALREADY
  STRONGLY VISIBLE`.** This is a proposal, not an automatic drop: `DEFEND`
  is still a real, valid opportunity type for that business (a
  monitoring/retention play worth pursuing on its own terms later), and the
  owner can override the disposition for a specific business. A `DEFEND`
  business outside the most-named cohort is not excluded by default.
- **NO OPPORTUNITY** — market or business fit is unclear, legal or trading
  status is unresolved, geography is ambiguous, the apparent gap is
  explained by being new/specialist/out-of-market, local decision-making is
  unrealistic, or the only available outreach angle would be misleading.
  **This is not `REVIEW`** — REVIEW is a state of disposition and priority
  (unresolved, with a recorded evidence reason), not a fourth opportunity type. A business
  can settle cleanly on NO OPPORTUNITY, or simply carry no opportunity type
  at all while its disposition stays REVIEW.

**Use relative market position, not a fixed count.** Where a business sits —
leader, upper-mid, mid, low, absent — is relative to that market's own
distribution (89 successful answers means something different from 900), not
a threshold applied the same everywhere. Do NOT define hard bands like
"0–5 = GAP, 6–30 = GROWTH, 31+ = DEFEND" — that is exactly the invented
precision the raw-counts rule below already forbids. Consider total
appearances, share relative to the leaders, provider split, question/intent
spread where useful, and consistency across OpenAI, Gemini and Perplexity —
strong on one provider and absent from another is a different commercial
story from evenly weak across all three. Use the raw observed counts and
judgement. No proprietary score, visibility percentage or invented precision.

**The outreach claim must match the opportunity type** (framing principles,
not fixed copy — write the actual sentence from the real evidence each time):

- GAP: *"You appear materially less often than businesses you directly
  compete with."*
- GROWTH: *"You already have meaningful AI visibility, but our research
  shows clear room to strengthen that position."*
- DEFEND: *"You currently hold one of the strongest AI recommendation
  positions in your local market. We can show you what is supporting it and
  monitor whether that changes."*

The existing letters below are written for GAP-type outreach (the never-named
and per-assistant-gap cases). GROWTH and DEFEND need different letters, not
yet drafted — write them from the framing principles above when that
outreach begins, not by stretching the GAP letters to fit.

**Opportunity type, commercial priority and send-readiness are three
separate questions — do not conflate them.** Opportunity type
(GAP/GROWTH/DEFEND/NO OPPORTUNITY) is *why* a business is worth approaching.
Commercial priority (A/B/C/REVIEW) is how much it's worth pursuing, weighing
evidence quality, market relevance, credibility, competitive position,
commercial value and decision-maker accessibility — visibility count alone
must not set it. A DEFEND business can be Priority A; a zero-visibility GAP
business can be Priority C. Send-readiness (`ready_to_email`) is whether
*this* email is ready today: verified contact, correct numbers, a truthful
angle.

**The Audit is the default entry product for all three opportunity types.**
GAP, GROWTH and DEFEND all start with the £250 Audit (`playbook/services.md`)
— the opportunity type changes *why* Wardith approaches a business, never
the first thing it sells. "Start with the audit. If there is genuinely
nothing to fix, we will tell you" holds for all three, DEFEND included.
What follows the audit — no action, Foundation, an ongoing monthly plan
(Maintain, Grow or Lead), or Foundation then a monthly plan — is decided
from what the audit actually finds, not predicted at qualification time.
Foundation does not have to come before a monthly plan: a DEFEND client with
little to structurally fix may go straight from Audit to ongoing monitoring.
If a prospect explicitly asks to start directly on ongoing work, Wardith may
agree to skip the Audit — the exception, not the default sales path.

**Before a prospect is outreach-ready, verify:**

1. it genuinely operates in the selected sector;
2. it genuinely competes in the selected geography;
3. it has a defensible active Ltd/LLP legal-entity match;
4. it has a meaningful competitive AI recommendation gap;
5. there is a suitable evidenced business contact route.

**Ambiguous prospects are REVIEW, not assumed valid.**

Route missing, conflicting, or resumed evidence through
`tools/prospect-compiler/REVIEW-EVIDENCE.md`: preserve a verified published
inbox, park an unverified route with its precise missing fact, and resume only
that gap. A missing email or external fact is not an individual owner decision.
Timing must be measured across requests, reading, and pauses, or recorded as
`conservative_elapsed`; `unknown` timing blocks additional requests. No pilot
or rollout passes from request counts alone.

**Batch of ten to twenty, weekly**, four or five a day rather than all at once.
One stop rule: do not send batch two while batch one has more than four audits
still owed.

### 5. Record it, then wait

Every send goes in the client record as it goes out — who, when, what the
finding was, what came back. **Nothing goes in this repository**; prospect names
are personal data. A reply asking not to be contacted is recorded permanently.

### 6. Follow up with restraint

The cold sequence has three emails and no automatic sending:

1. **Email 1** — one evidenced finding and the £250 Audit offer.
2. **Email 2** — useful additional context from the same recorded evidence,
   or a clarification of what the Audit covers. Default: five business days
   after the actual Email 1 send.
3. **Email 3** — a brief final invitation. Default: seven business days after
   the actual Email 2 send. Then record `EMAIL_3_SENT` and close the sequence.

Never invent a second finding. A reply pauses the cold sequence for human
handling. An opt-out or manual contact hold blocks it. Sales and client stages
survive incidental activity such as LinkedIn views.

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

### The GROWTH letter

Drafted 2026-08-15, the first time GROWTH outreach actually ran
(`/outreach`, against the Chester dentists campaign). Same shape, with the
middle replaced — used when a business already has real, checkable
visibility but sits materially behind the market leader, including on a
specific question where the leader scores and this business doesn't:

> {Business} came up in {n} of them, which is real and worth having.
> {Leader}, the {business type} named most often in this research, came up
> in {m}. And on one question specifically — "{q}" — {Business} wasn't
> named once, in fifteen answers. {Leader} was, {k} times.

...and the offer paragraph becomes "A gap like this can come from a few
different places and they aren't equally easy to close. What I sell is
finding out which one applies to you."

**Never claim the per-question absence is a gap unless the leader actually
scores on that question** — some question phrasings get no business named
by any assistant, and citing one of those as a competitive gap is a false
comparison, not a finding.

DEFEND still has no drafted letter — no DEFEND outreach has run yet. Write
one from the framing principle above when that day comes, the same way
this section was written from it.

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
