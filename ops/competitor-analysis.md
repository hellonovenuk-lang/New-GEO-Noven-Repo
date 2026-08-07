# Competitor citation analysis — why they get named and we don't

**Internal document.** Written 2026-08-07, session one of two. Prompted by the
Aug 2026 self-audit's "who gets recommended instead" table
(`ops/audits/noven-2026-08-02/report.md`): across the automated runs, Tilio was
named 36 times, more than any other business, with nine more competitors named
repeatedly behind it. This document asks why, and what to actually do about it.

**Two parts, two sessions, by design.** Part 1 is desk research on what these
competitors visibly do — done, this session, using only public search. Part 2
needs `runs-clean.csv`, the raw verbatim answer data from the self-audit, which
lives on the owner's own machine and is not in this repo
(`ops/audit-method.md` §5 — the same rule applies here as to any audit data).
**Start Part 2 in a new session once that file is supplied** — see the
instructions at the end of this document, and `ROADMAP.md` 2f.

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

## Part 2 — instructions for the next session

**Trigger: the owner supplies `runs-clean.csv`** (the raw verbatim answer data
from the Aug 2026 self-audit — 210 rows, `answer_text` and `sources_cited` per
run). Read `ops/audit-method.md` §5 first if picking this up cold: this file
is treated the same as any audit data and **must not be committed to this
repo**. Work with it in place (or the scratchpad), don't add it to git.

1. **Test WebFetch first**, on a throwaway domain. This session's environment
   blocked it entirely; a new session's might not. Useful either way for
   verifying whatever `sources_cited` turns up.
2. **Mine every competitor mention, not just Tilio.** For every row where the
   `competitors` column names a business — all ten from the aggregate table,
   plus anything else that turns up in the raw data that didn't make the
   top-10 cut — pull the matching `answer_text` and `sources_cited`.
3. **Test Finding 1 against real data.** Do the listicles identified in Part 1
   (Tilio's own list, ClickSlice's lists, the other third-party sites) actually
   appear in `sources_cited`? That's the difference between "plausible from
   desk research" and "confirmed by what the assistants actually cited."
4. **Break it down by provider** (ChatGPT / Gemini / Perplexity) — which cite
   directories and listicles most, which cite competitors' own sites, since
   that decides which lever (get-listed-elsewhere vs. own service pages)
   matters more and where.
5. **Cross-reference Part 1 and Part 2 into one execution plan** — the actual
   deliverable this was all for. Concretely: which listicles to approach for
   inclusion first, whether a "digital PR / citation" line belongs in the
   product (Finding 4) at Foundation, Grow or Lead level, and what a safe
   self-inclusive comparison page should say, all prioritised by what the real
   citation data shows matters most rather than by what merely seemed
   plausible from desk research alone.
6. **No public "expose / trust-score / ranking" content** — that's parked, per
   the "Considered and not done" section above, unless the owner deliberately
   reopens it.
7. **Any individual-competitor observations should come from this pass's own
   data, on their own merits** — not carried over from anything outside this
   document.
