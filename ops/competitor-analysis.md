# Competitor citation analysis — why they get named and we don't

**Internal document.** Written 2026-08-07, session one of two. Prompted by the
Aug 2026 self-audit's "who gets recommended instead" table
(`ops/audits/noven-2026-08-02/report.md`): across the automated runs, Tilio was
named 36 times, more than any other business, with nine more competitors named
repeatedly behind it. This document asks why, and what to actually do about it.

**Two parts, two sessions, by design.** Part 1 is desk research on what these
competitors visibly do — done 2026-08-07, using only public search. Part 2 is
the same question asked of `runs-clean.csv`, the raw verbatim answer data from
the self-audit — **done 2026-08-07, later the same day, and written up below.**
That file lives on the owner's own machine and is not in this repo
(`ops/audit-method.md` §5 — the same rule applies here as to any audit data).
It was supplied for the Part 2 session, read in place, and **not committed.**

**Read Part 2 before acting on Part 1.** The data agrees with most of Part 1
but overturns its single biggest recommendation. Where the two disagree,
Part 2 wins — it is what the assistants actually did, not what desk research
suggested they might be doing.

---

## Part 1 — desk research findings (2026-08-07)

**Method and its limit.** WebSearch only. WebFetch returned `EGRESS_BLOCKED` for
every domain tried this session, including a bare sanity check against
`example.com`, both from the original web session and again after switching to
the desktop app — confirmed as a session/environment network policy, not
something fixable mid-session. **Everything below is sourced from search
snippets, not primary-source page reads.** Treat findings marked "confirmed" as
resting on multiple independent snippets; treat anything marked "open" as
needing an actual page visit before it's relied on for anything beyond "worth
checking further." Test WebFetch again at the start of the next session —
policy may differ in a fresh environment.

### Finding 1 — self-published and third-party "best of" listicles are the dominant visible pattern

Confirmed. Several of the named competitors publish their own ranked list of
providers in this category, including themselves:

- Tilio: "The 14 Best GEO Agencies in the UK (2026)" on `tilio.co.uk`.
- ClickSlice: "6 Best AI Answer Engine Optimisation Agencies in the UK (2026)"
  and a separate ecommerce-specific version.
- Rank4AI: a "GEO vs AEO Agencies UK 2026" research/rankings page.

On top of that, at least eight independent third-party listicle sites turned up
across searches (eseospace, FirstMotion, Climb SEO, Charle, Minuttia, Digital
Agency Leaders, SuperHub, Thrive, Digital Elevator, SEOprofy) — all ranking and
re-ranking overlapping sets of the same names. This is exactly the kind of
content an AI assistant pulls from when asked "who's the best X": structured,
comparative, freshly dated, repeatedly crawled. **Wardith appears on none of
them.** This is a more direct explanation for the mention gap than anything
about any individual competitor's honesty.

### Finding 2 — every named competitor has a dedicated service-specific page

Confirmed, ten for ten. `/generative-engine-optimisation`, `/aeo-agency`,
`/aeo/` — a standalone page for the specific service, not GEO folded into a
general marketing page. Matches what the Aug 2 self-audit already flagged as
Wardith's own structural gap at the time (site published days before the audit
ran).

### Finding 3 — published pricing is normal in this category, and Wardith's is genuinely competitive

Confirmed. Tilio publishes £499/month; SuperHub publishes £299–£899/month;
general market figures for fuller-service AI-visibility work run
£2,000–£5,000/month. Wardith's £150–£800 range undercuts this significantly.
The Aug 2 self-audit already established that publishing prices at all is rare
and valuable — this confirms it's a real differentiator *within* this specific
category too, not just against local-search agencies generally.

### Finding 4 — "digital PR" / citation strategy shows up as a distinct, separate service line

Confirmed at least once directly (Dynamically sells it apart from on-site
work): the being-talked-about-elsewhere half of GEO — placement on other
people's pages, directories, listicles — sold as its own line item, not bundled
into a website audit. **Wardith's current product (Audit / Foundation /
Maintain / Grow / Lead) doesn't touch this half at all.** Worth weighing
against Finding 1: if citation volume tracks appearing on other people's lists,
a service that only fixes a client's own site may be treating half the problem.

### Finding 5 — company age doesn't appear to be the driver

Tilio was founded mid-2025 — barely older than Wardith — and still topped the
mention count. Points toward content and citation strategy as the operative
variable, not years in business. Useful because it means the gap is closeable
quickly, not a tenure problem.

---

## Considered and not done — read this before proposing it again

Across this session, several ways of turning the above into published content
were proposed and worked through in detail, then explicitly parked by the
owner. Recorded here so a future session doesn't re-propose the same thing
without the reasoning that closed it:

1. **A numeric "trust score" ranking named competitors.** Dropped: a score
   reads as a factual claim, not opinion, which weakens rather than helps a
   defamation defence; UK comparative-advertising rules (Business Protection
   from Misleading Marketing Regulations 2008, the ASA's CAP Code) require
   objective, verifiable, non-denigrating comparisons with evidence held
   *before* publication; and it directly contradicts `ops/audit-method.md`'s
   own ban on an invented visibility score in Wardith's client reports — same
   reasoning, just pointed outward instead of at a client.
2. **A checklist-based pass/fail ranking of named competitors, framed as
   "industry standards."** Same risk category as (1). Also practically
   blocked: publishing "X fails this criterion" needs documentary evidence
   held in advance, and WebFetch was unavailable all session, so nothing could
   be verified past search-snippet level — see the method note at the top of
   Part 1.
3. **A "we are the most trustworthy" claim, published through something styled
   to look like an independent or third-party outlet.** Dropped specifically
   for the packaging, not the underlying claim: undisclosed self-promotion
   dressed as independent content is a Consumer Protection from Unfair Trading
   Regulations 2008 / CAP Code problem regardless of whether the claim is
   true. A transparently self-published version of the same claim was not
   ruled out, but "most trustworthy" as an unqualified superlative was flagged
   as weaker and less defensible than a specific, falsifiable claim — and out
   of step with how the rest of the site talks about itself (no invented
   score, "no honest way to dress that up" on `/ask-your-ai/`).

**Net decision: none of this gets published.** The findings above are for
internal strategy only — see Part 2. If a public comparison piece naming
competitors is ever revisited, it needs primary-source-verified evidence held
before publication, transparent Wardith authorship, and realistically a
solicitor's sign-off given the explicitly competitive intent behind the
original idea. None of that is in place, and this document doesn't create it.

**What's still fair game, and was agreed as such:** a self-inclusive "best of"
style page listing real providers with Wardith positioned on facts it can back
up; a standalone, transparently-Wardith "here's what to check, here's how we
measure up" page; and — probably the highest-leverage, lowest-risk option of
all — approaching the existing third-party listicles to get Wardith *listed*
on them, since that's the mechanism Finding 1 shows is actually working.

---

## Part 2 — what the raw answer data actually shows (2026-08-07)

**Source.** `runs-clean.csv` from the Aug 2026 self-audit: 210 rows, one per
run, three assistants (ChatGPT `gpt-5.5`, Gemini `gemini-3.6-flash`, Perplexity
`sonar`), all via API, eleven questions. Read in place from the owner's upload,
analysed in the session scratchpad, **not committed** — `ops/audit-method.md`
§5. Same file as the Noven audit; the owner asked us to confirm that and it is
confirmed by `audit_id = noven-2026-08-02` on all 210 rows.

**WebFetch works this session.** Part 1's whole method note was written around
`EGRESS_BLOCKED`; it was a per-session policy, as suspected. Every page named
below was fetched and read, not inferred from a search snippet. Findings here
are accordingly stronger than Part 1's.

**Two limits to hold on to.** First, **the supplied file is the
pre-classification export** — `outcome` and `competitors` are empty on all 210
rows, so the report's mention counts were produced somewhere else and could not
be re-derived from this file. Everything below counts businesses by matching
names against `answer_text` directly, which is why the numbers do not tie to
the report's table (see Finding A). Second, **Gemini's sources are unreadable**
(Finding E) — every source-based conclusion here rests on ChatGPT and
Perplexity only.

**How the counting works.** 210 rows split into 45 "identity" rows — q06 and
q07, which ask about Noven by name — and **165 "opportunity" rows**, the
discovery, comparison and buying-intent questions where a business could be
recommended and Wardith could in principle have been the answer. Percentages
below are of those 165 unless said otherwise.

### Finding A — the market is far more fragmented than the report's top ten suggested

**41 distinct businesses** are named across the opportunity rows, 39 of them in
more than one run. The report's table showed ten. The tail is not noise: it is
half the field.

More important is what the leader's share looks like once the denominator is
right. **Tilio is named in 46 of 165 opportunity rows — 28%.** Rank4AI, 23%.
Third place is 12%. And **62 of the 165 rows name none of the 41** — they
answer with categories, advice and "here's how to vet one" instead of names.

| Business | Rows named | % of 165 | ChatGPT | Gemini | Perplexity |
|---|---:|---:|---:|---:|---:|
| Tilio | 46 | 28% | 19 | 16 | 11 |
| Rank4AI | 38 | 23% | 13 | 8 | 17 |
| Passion Digital | 19 | 12% | 3 | 13 | 3 |
| AEO Agency | 16 | 10% | 6 | 2 | 8 |
| Bold Online Marketing | 15 | 9% | 5 | 5 | 5 |
| ClickSlice | 15 | 9% | 1 | 3 | 11 |
| Dynamically | 13 | 8% | 3 | 5 | 5 |
| Exposure Ninja | 13 | 8% | 1 | 9 | 3 |
| Blue Array | 12 | 7% | 2 | 7 | 3 |
| GEO Intelligence | 10 | 6% | 10 | 0 | 0 |

**Why this matters more than it sounds.** The report's framing — Tilio named 36
times, a leader board behind it — reads as an established pecking order to
climb. The data says something different: **there is no incumbent.** No business
is named in even a third of the answers, most of the field appears in under
10%, and more than a third of answers name nobody at all. That is not a market
with leaders to displace. It is an unformed one, and the cost of entering it is
correspondingly low. Part 1's Finding 5 guessed at this from Tilio's founding
date; the distribution is the better evidence for it.

**Also worth noting: nine of the top ten are new information.** Passion Digital,
Bold Online Marketing and Blue Array are all top-ten by this count and appear
nowhere in the report's table, while Otter Labs, GEOQ and Consilium Design drop
to 5% or below. Part 1's desk research was aimed at the report's ten. It was
aimed at roughly the right sort of business, but not consistently the right ones.

### Finding B — Part 1's Finding 1 is confirmed, and it is the mechanism

Listicles are not merely present in the citations. They are what the answers are
made of.

- **60 distinct domains** were cited publishing a "best/top GEO agency"-shaped
  page. Part 1 identified about eleven from search snippets.
- Rows citing at least one such page name **3.3 businesses on average**. Rows
  citing none name **1.2**. (ChatGPT and Perplexity only; Gemini excluded per
  Finding E.)
- Most-cited individual pages: Buried Agency's `top-geo-agencies-uk` (9 rows,
  both assistants), Polaris's `best-geo-services-uk` (7), Sort The Clicks (6),
  FirstMotion (6), ClickSlice's agency list (6), Okapi & Co (5), Passion
  Digital (5), Tenet (5), Tilio's own `top-geo-agencies-uk` (5), Level Up Leads
  (5), Genie Crawl's top-50 (5).

The correlation is not proof of causation — an assistant that has decided to
name businesses will naturally go looking for lists. But the direction is
consistent across both readable assistants, and the named businesses are
overwhelmingly drawn from the lists cited in the same answer. Part 1 called this
"plausible"; it is now the best-evidenced thing in either half of this document.

### Finding C — but there is nothing to apply to, and this overturns Part 1's main recommendation

Part 1 closed by calling it "probably the highest-leverage, lowest-risk option
of all" to approach the third-party listicles and get Wardith listed. **Part 2
fetched them. That option is mostly not available.**

Every high-citation list was read in full. Publisher, and whether a business can
ask to be included:

| Page | Published by | Route in |
|---|---|---|
| `buriedagency.com/post/top-geo-agencies-uk` | Buried Agency — lists itself #1 | None. No form, no email, no criteria for applying |
| `firstmotion.com/insights/best-geo-agencies-uk` | FirstMotion — lists itself | None. States "No agency paid to appear" |
| `sorttheclicks.com/.../best-uk-geo-agencies-2026` | Sort The Clicks — lists itself | None. General contact only |
| `okapiandco.co.uk/blog/best-geo-agencies-uk-2026` | Okapi & Co — lists itself #1 | None |
| `geniecrawl.com/top-50-...-rankings` | Genie Crawl | None stated; criteria mention Google reviews |
| `tilio.co.uk/blog/top-geo-agencies-uk` | Tilio — lists itself | None |
| `clickslice.co.uk/...` (four separate lists) | ClickSlice — lists itself | None |
| `rank4ai.co.uk/research/rankings/...` | Rank4AI — lists itself | None |

**There are no independent directories here.** With one exception noted in
Finding F, every one of these is an agency writing a ranked list of its
competitors and placing itself on it. They are not publications with editorial
inboxes. Asking Buried Agency to add Wardith to Buried Agency's list of the best
agencies is asking a competitor for a favour, and the honest expected answer is
no.

**What the same evidence says instead: publishing the list is the mechanism.**
Every publisher above got itself cited by writing one. That is the actual
observed route into these answers, it costs nothing but the writing, and
**Part 1 already recorded it as agreed fair game** — "a self-inclusive 'best of'
style page listing real providers with Wardith positioned on facts it can back
up." Part 1 listed that third of three options. The data promotes it to first.

Note carefully what this is and is not. It is not the parked "trust score" or
the pass/fail ranking — see "Considered and not done", which stands unchanged
and is not reopened here. The difference is that those scored competitors
against invented criteria; this describes real providers accurately, includes
Wardith with an honest statement of what it does and costs, and is transparently
published by Wardith. That is what all sixty of these publishers are doing.

### Finding D — an unexpected second route: Reddit

Reddit was the single most-cited domain in ChatGPT's answers — 860 citations
across 42 rows. Most is background, but a specific subset is not:

| Thread | Citations |
|---|---:|
| r/DigitalMarketing — "every seo agency now lists ai search optimization" | 29 |
| r/Superframeworks — "10 best ai seo geo/aeo agencies for 2026" | 26 |
| r/SearchTides — "10 best geo agencies for brands that want to win" | 21 |
| r/b2bmarketing — "the 7 leading ai seo agencies for modern search" | 18 |
| r/b2bmarketing — "the 10 best visibility companies and agencies" | 15 |
| r/SEO_LLM — "the best geo agency roundups and the agencies ai [cite]" | 12 |
| r/GEO_optimization — "what are the top generative engine optimization…" | 11 |
| r/LLMTraffic — "which geo marketing agencies are actually worth…" | 11 |

These are the same self-published listicles in a second venue, several posted to
subreddits that look agency-run. **This is a genuinely open door** in a way the
listicles are not: anyone can answer a public question thread. It also carries
real risk — undisclosed self-promotion is against most of these subreddits'
rules and against the spirit of the CPUT/CAP reasoning in "Considered and not
done". If it is used at all, it is used with Wardith's identity stated openly.
**Flagged as an option, not recommended without the owner deciding on it.**

### Finding E — the three assistants are three different problems

Source mix across the opportunity rows:

| | ChatGPT | Gemini | Perplexity |
|---|---:|---:|---:|
| URLs cited | 4,417 | 479 | 821 |
| Readable at all | yes | **no — 100% opaque** | yes |
| Listicles (third-party + on competitor sites) | 9% | — | **21%** |
| Competitor's own site, non-listicle | 11% | — | 7% |
| AI-platform / Google documentation | 16% | — | 2% |
| Forum / social | 15% | — | 7% |
| Wrong-Noven / off-topic noise | **15%** | — | 1% |

Three separate conclusions:

1. **Gemini's citations cannot be audited.** All 479 URLs are
   `vertexaisearch.cloud.google.com/grounding-api-redirect/…` wrappers that
   resolve nowhere readable. We can see what Gemini said, never what it read.
   **This is a method finding, not just an analysis one** — `ops/audit-method.md`
   §5 lists `sources_cited` as a column without noting that for one of the four
   assistants we sell, it is structurally empty. A client report must not imply
   we can see Gemini's sources. Recorded in `ROADMAP.md` as a method fix.
2. **Perplexity is the listicle machine.** More than a fifth of everything it
   cites is a ranked agency list, and it cites competitor-published lists
   (10.6%) nearly as often as third-party ones (10.7%). If the self-published
   list in Finding C gets written, Perplexity is where it lands first.
3. **ChatGPT is doing something else entirely** — it cites five times as many
   URLs as the other two combined, leans on OpenAI's and Google's own
   documentation (16%) and Reddit, and **15% of everything it cites is about the
   wrong Noven.** See Finding G.

### Finding F — the Wirral question is a different, much shallower field

q03 ("someone on the Wirral") does not return the national field at all. It
returns five local businesses, and one of them owns it outright:

| Business | Rows | of 15 |
|---|---:|---|
| Bold Online Marketing | 15 | **every single run, all three assistants** |
| Dynamically | 9 | |
| Storeton Digital | 5 | |
| Max Web Solutions | 5 | |
| Graham SEO | 4 | |

**And here is the one open door in the whole dataset.** Two assistants cited
`threebestrated.co.uk/marketing-agencies-in-wirral` on this question, and
Perplexity cited a `clutch.co` profile for Storeton Digital. ThreeBestRated was
fetched: it is a real directory, it lists Lead Pronto, Hyena Design and **Bold
Online Marketing**, and its own wording is **"List your business for Free!"**

That is a free, open, already-cited listing on the exact question where Wardith
is local and the field is five businesses deep rather than forty-one. It is the
cheapest concrete action in this document.

### Finding G — the name collision was total, and the rename is vindicated

`ops/rename-to-wardith.md` records the Noven → Wardith decision as settled on
2026-08-04, argued mainly from there being no indexation equity to lose. **The
raw data provides the stronger argument that was not available at the time.**

q06, "What do you know about Noven?", 30 runs:

- **0 of 30** described the Wirral business. Not one, on any assistant.
- **30 of 30** described a different Noven. All three led with **Noven
  Pharmaceuticals**, the US transdermal-patch maker owned by Hisamitsu — which
  is also why `medicines.org.uk`, `nhs.uk`, r/Menopause and r/transgenderUK turn
  up in the citations.
- Also returned: Noven Build Limited (construction), noven.io, heynoven.com,
  Noven NV, The Noven Foundation, and Novem.

q07 added the Wirral qualifier — "Is Noven on the Wirral any good?" — which
should have been decisive:

- **ChatGPT: 0 of 5.** **Perplexity: 0 of 5**, and worse than silence — it
  confidently offered *Noven Build*, a North West builder, and *Novem*, a Wirral
  IT support firm, as the likely intended business. A plausible, local, wrong
  answer is the most damaging possible outcome.
- **Gemini: 5 of 5 correct**, describing the business accurately, founder
  included. Consistent with Google having indexed the site.

q08, "main alternatives to Noven?" — the comparison question, the one that
should be most commercially valuable — **ChatGPT answered about managed IT
service providers**, listing Air IT, Littlefish and Zenzero, because it had
resolved Noven to Novem. Perplexity 0 of 5. The question was wasted.

**Nothing here reopens the rename; it closes the argument for it.** The name did
not merely fail to be found — it actively routed buying-intent questions to a
pharmaceutical company, a builder and an IT firm. The one assistant that got it
right was the one whose index had actually read the site, which is a point about
indexation, not about the name. **Re-run q06–q08 against "Wardith" once the site
has been indexed under the new name** — it is a clean before/after on the single
clearest finding in the audit, and it costs three questions.

### Finding H — pricing: Part 1's Finding 3 confirmed, with one correction

Across q05 and q10, where the assistants were asked what this should cost, the
**median figure quoted is £1,500/month** and it is the same median on all three.
The full quoted range runs £299/month to £25,000. GEO Intelligence's published
£299/£699/£1,499 tiers and Tilio's £499 are both quoted back by name — Part 1's
Finding 3 confirmed from the assistants' own mouths, and confirmation that
publishing prices gets them repeated.

**The correction.** Part 1 said Wardith's £150–£800 "undercuts this
significantly", framed as an advantage. The data adds context that complicates
it: the assistants describe the £500–£1,500 band specifically as **freelancer
and consultant** rates, with agency work above it. £150–£800 does not read as a
cheap agency in this framing — it reads as a freelancer, which is accurate but
is a different market position than "better value than Tilio". Worth deciding
deliberately rather than by default. **Not a recommendation to raise prices** —
`ops/service-tiers.md` owns that, and this is one input.

One number does land well: the assistants put an initial AI-visibility audit at
**"often £250–£750"**. The £250 audit sits exactly at the bottom of the band the
assistants themselves quote — credible, and the cheapest honest entry point.

### Finding I — Part 1's Findings 2 and 4, retested

- **Finding 2 (dedicated service pages): supported.** Where a business is named,
  its own site is cited alongside — tilio.co.uk in 41 rows, rank4ai.co.uk in 37,
  clickslice in 15. The pattern holds; being named and having your own page read
  go together. Wardith's site was cited **zero times in 210 runs**, as the report
  already said.
- **Finding 4 (digital PR as a separate line): not supported by this data, and
  not refuted either.** Nothing in the citations distinguishes an agency selling
  citation-building as a line item from one that does not. It was a desk-research
  observation about how competitors package services, and this dataset is the
  wrong instrument for it. **Treat it as still open.** The product question it
  raises is answered on other grounds below.

---

## The execution plan — Part 1 and Part 2 crossed

Ordered by what the data supports, cheapest first. Nothing here is published
without the owner's agreement, and none of it reopens "Considered and not done".

1. **List on ThreeBestRated (Wirral).** Free, open, already cited by two
   assistants on the Wirral question, and the one competitor named in 15 of 15
   runs is already on it. Finding F. Do this first — it is the only
   already-open door in the dataset.
2. **Write and publish Wardith's own honest comparison page.** The
   best-evidenced action here (Findings B and C): it is how all sixty cited
   publishers got cited, Perplexity consumes them at 21% of everything it cites,
   and Part 1 already agreed the self-inclusive form is fair game. Constraints,
   all from "Considered and not done": real providers described accurately, no
   invented scores or pass/fail criteria, Wardith's authorship stated on the
   page, every factual claim about another business verifiable from their own
   site and held before publication. **Draft it, then get the owner's sign-off
   before it goes near `main`** — publishing is deploying, per `CLAUDE.md`.
3. **Re-run q06–q08 under "Wardith" once indexed.** Finding G. Three questions,
   a clean before/after on the rename, and it directly measures whether the
   1 September work is landing.
4. **Fix the audit method's Gemini gap.** Finding E1. `ops/audit-method.md` §5
   must say that Gemini returns opaque redirect URLs and that no source analysis
   is possible for it. This is a promise-accuracy problem in a document that
   feeds client reports, not a nicety.
5. **Leave the product alone for now.** Part 1's Finding 4 asked whether a
   digital-PR/citation line belongs in Foundation, Grow or Lead. Finding I says
   this dataset cannot answer that, and item 2 above is the same lever at zero
   cost and zero product risk. Revisit after the comparison page has been live
   long enough to measure. **Do not add a service line on the strength of
   desk research alone.**
6. **Reddit: owner's decision, not a default action.** Finding D. Open door,
   real citation weight, and real disclosure risk. Not started without an
   explicit yes.

**Both parts of this piece of work are now closed.** What remains is execution,
tracked in `ROADMAP.md` 2f. If it is picked up cold: read "Considered and not
done" before proposing anything public that names a competitor, and read
Finding C before proposing that we ask to be added to someone's list.
