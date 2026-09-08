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
reason to drop a business — being one of the market's two most-mentioned
incumbents is (2026-09-05).** The Chester and Wirral retrospective
(2026-08-14) first showed that visibility alone was too narrow a reason to
drop a business: a business with a strong existing AI position is a `DEFEND`
opportunity, not a dead end. The exclusion is now a fixed campaign-wide count
— the two most-mentioned businesses in the market, held out of the default
cold-outreach batch and retained in the market analysis. Every other `DEFEND`
business is pursued exactly like `GAP`/`GROWTH`. See step 4.

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
  **The two most-mentioned businesses in a market (the "most-named cohort")
  default to excluded from this round of outreach (2026-09-05), reason
  `ALREADY STRONGLY VISIBLE`.** They stay in the market analysis with every
  scored field intact — only the default disposition changes. This is a
  proposal, not an automatic drop: `DEFEND` is still a real, valid
  opportunity type for that business (a monitoring/retention play worth
  pursuing on its own terms later), and the owner can override the
  disposition for a specific business. A `DEFEND` business outside those two
  is not excluded by default, and keeps its `DEFEND` classification — the cap
  decides how many incumbents this round skips, never what a business is.
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
angle. A named decision-maker is not required for it (2026-09-05) — a
verified general business inbox is a valid route, and where no name is
confirmed the email addresses the business rather than an invented person.

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
2. **Email 2** — delivers what Email 1 offered: what the Audit checks.
   Carries no finding. Default: five business days after the actual Email 1
   send.
3. **Email 3** — a brief final invitation. Default: seven business days after
   the actual Email 2 send. Then record `EMAIL_3_SENT` and close the sequence.

The copy for all three is in `## The letters`.

Never invent a second finding. A reply pauses the cold sequence for human
handling. An opt-out or manual contact hold blocks it. Sales and client stages
survive incidental activity such as LinkedIn views.

---

## Sending

- From `hello@wardith.co.uk` (Zoho). Display name **Kieran Smith**, not Wardith
  — in a reception inbox a person's name reads as correspondence.
- **One recipient per email. Never a CC, never a BCC list.** Twenty addresses
  visible to each other is a data breach and the end of the pitch at once.
- **The signature is text only, no wordmark image (2026-09-06).** Images are
  blocked by default in Outlook desktop and many corporate gateways, so an
  image signature degrades for exactly the reception inboxes this is written
  for. Text renders identically everywhere and cannot break.
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

**Emails 2 and 3 are replies on the Email 1 thread (2026-09-06).** It reads as
correspondence rather than a campaign, and the Article 14 disclosure stays
visible in the thread below. In-thread, they carry the opt-out and the
signature; the source disclosure is not repeated. A standalone follow-up would
have to carry all three again.

## The letters

**Status: rewritten 2026-09-06**, to the short form the owner refined and
sent. The previous four letters ran to roughly 400 words and read as a report
rather than a note. They are in git history and superseded.

**Subject: the business's own name, plus routing.** `{Business} — for {named
person}`, or `— for the owner` on a generic inbox. **No claim in the subject
and no technology word** — "ChatGPT" is the most common word in the marketing
email they already delete.

**Only quote questions the business is geographically eligible for.** Citing a
question that names a town they are not in hands them a fair objection.

**Never state a total count of businesses named** until the counting method is
settled — two methods have given two answers. State what was verified.

### Email 1, in eight blocks

Every first email is these eight, in this order. Nothing else goes in. About
150 words; if a draft is materially longer, a block has grown a second idea.

1. **Greeting.** `Hi {name},` to a person, `Hello,` to an inbox.
2. **Who you are, one sentence.** "I'm Kieran Smith, based in Birkenhead. I
   check which local businesses ChatGPT, Gemini and Perplexity recommend."
   Who you are before what you found — `playbook/voice.md`'s structural rule,
   and the one that matters most.
3. **The finding, one paragraph.** What was checked, this business's own
   number, and the single sharpest contrast. One comparison, never a table of
   competitors. Quote a question only where the question itself is the
   finding.
4. **The offer, restating their finding.** "For £250, I'll find out why {the
   specific thing block 3 just said}, then give you a written report showing
   what, if anything, is worth changing. It's yours to act on with me or
   without me." The offer sentence carries their own result, which is what
   stops it reading as a template.
5. **Proof.** "Here's the same audit on my own business:
   wardith.co.uk/ask-your-ai/self-audit/"
6. **The ask.** "Would you like me to send over what I'd check for
   {Business}?" Ask for a reply, not a £250 decision. Email 2 then delivers
   exactly this.
7. **Source and opt-out, one line.** "Your email came from {where}; I checked
   the business details against Companies House and {source}. Reply if you
   would rather not hear from me again." {source} must be a publisher in this
   business's own evidence, never one borrowed from another business in the
   same campaign.
8. **The signature.** Text only, see `## Sending`.

### Quoting the numbers

**"{n} of {N} relevant answers", never "of ninety".** N is the answers to the
questions this business is actually eligible for, so the figure survives the
eligibility rule above. Both come from the campaign JSON:
`relevant_appearances` and `relevant_opportunities`.

**Quote whole numbers only.** `relevant_appearances` is relevance-weighted and
can be fractional. Where it is not whole, do not round it into a claim — sum
`question_appearances` across the questions counted relevant and quote that.

### The three shapes of block 3

Write the sentence from this business's own evidence every time. Never reuse
another business's wording with the nouns swapped.

**Absent.** "I went through all {N} relevant answers looking for {Business}.
It isn't in any of them."

This shape, and only this shape, adds one more paragraph, because the
objection is live here and nowhere else:

> I didn't ask about {Business} by name. If you type the name in, all three
> will probably tell you plenty, and accurately. I asked the way somebody
> looks for a {trade} when they don't have one yet. That's the question that
> brings in new customers, and it's a different question.

**One assistant, not the others.** "{Business} appeared in {n} of {N} relevant
answers, but every mention came from {assistant}. {The other two} didn't name
you."

**Behind the leader.** "{Business} came up in {n}. {Leader}, the one named most
often in this research, came up in {m}." Never claim a per-question absence is
a gap unless the leader actually scores on that question — some phrasings get
no business named by anyone, and citing one is a false comparison.

**DEFEND still has no letter.** No DEFEND outreach has run. Write one from the
framing principle in step 4 when that day comes.

**Writing to a gatekeeper:** open to reception, ask them to pass it on, say
what it is in one line, then cut the second greeting.

> You're probably getting a lot of AI emails at the moment. This one has an
> actual finding about {Business} in it rather than a pitch — could you pass
> it to {named person}?

### Email 2 — the delivery

Five business days after the actual Email 1 send, as a reply on the same
thread. It delivers what block 6 offered. **It contains no finding at all**,
which is what keeps "never invent a second finding" out of play rather than
merely satisfied.

> Hi {name},
>
> I said I'd send over what I'd check for {Business}. Here it is, whether or
> not you want the audit.
>
> Four things, in this order:
>
> - Whether the assistants can reach your site at all.
> - Whether what's on it is readable by a machine, not just by a person.
> - Whether your facts (name, address, phone, hours, services) match
>   everywhere they appear.
> - Whether anything on the site actually answers the question a customer
>   types.
>
> Then ten questions about {Business} specifically, across ChatGPT, Gemini and
> Perplexity, to find which of the four is costing you.
>
> That last part is the £250: the answers for your business, and what to
> change. The list above is yours regardless. If it is more useful as
> something you work through yourself, genuinely, help yourself.
>
> If you'd rather not hear from me again, tell me and I'll delete your
> details.
>
> Kieran

The four lines are Groups 1 to 4 of `playbook/audit-site-checklist.md` in
plain words. Keep them that way. The method is already published on the
self-audit page; the answers for their business are the product.

### Email 3 — the close

Seven business days after the actual Email 2 send, as a reply on the same
thread. About 45 words. Then record `EMAIL_3_SENT` and the sequence is over.

> Hi {name},
>
> Last one from me.
>
> {The same finding, in one sentence.}
>
> If it becomes worth a look later, the research is on file and I'm easy to
> find. Otherwise I'll leave you to it.
>
> Tell me if you'd rather I deleted your details.
>
> Kieran

No new claim, no manufactured deadline, no "just circling back". The finding
is the one Email 1 already used, shorter.

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
