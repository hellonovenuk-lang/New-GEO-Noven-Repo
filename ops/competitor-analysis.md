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

### Finding 6 — the Tilio testimonial lead (open, not resolved)

Investigated at the user's prompt, using WebSearch plus two screenshots the
user supplied directly from Tilio's site and from two LinkedIn profiles.

- **Confirmed:** the testimonial is real content on `tilio.co.uk` — Daniel
  Dale-Tucker, "Founder at Areon."
- **Confirmed:** Jack (Tilio's co-founder) attended Falmouth University
  2015–2018 (Games Development); Daniel Dale-Tucker attended Falmouth
  University 2016–2019 (Business) — overlapping years, same institution. A
  real, checkable personal-network connection between reviewer and founder.
- **Open:** "Founder at Areon" does not appear in the visible sections of
  Daniel's own LinkedIn profile (the two screenshots supplied showed
  Education, Licences, Volunteering and part of Experience — not the top of
  the profile). A search-indexed snippet of the same LinkedIn profile shows
  his headline as "Account Manager @ VoiceFlex." Companies House was not
  checked — WebFetch was unavailable all session.
- **Verdict: not proof of anything, and not to be treated as such.** It's a
  documented, real gap between a marketing claim and what's independently
  checkable so far — genuinely stronger than "why would a web designer need
  this," which is where the question started, but still short of a documented
  case. Would need: the top of Daniel's LinkedIn profile, and a Companies
  House check for an "Areon" company with him listed as director.

### Finding 7 — MarGen / Digital Agency Leaders (the strongest lead found this session)

Confirmed to a much higher standard than Finding 6 — multiple independent
search results corroborate this without requiring inference:

- Leeroy Powell is publicly identified, by his own LinkedIn and by multiple
  other sources, as **both** "Founder & CEO of MarGen" (a Sheffield-based
  GEO/AEO agency) **and** "CEO & Group Founder" of **Digital Agency Leaders**
  (`digitalagencyleaders.net`), a directory-and-rankings publication, also
  Sheffield-based.
- Digital Agency Leaders' own "15 Best AI SEO Agencies in the UK (2026)"
  ranking placed MarGen at #1. MarGen republished this on its own site
  ("MarGen Ranked the UK's #1 AI SEO Agency for 2026"). Two of the top three
  spots in a ranking claiming UK-wide scope went to Sheffield firms.
- Leeroy Powell is also credited with a "Director of the Year 2022" award from
  "AI Publishing Solutions" — an accrediting body not yet verified as
  independent or as existing in any substantive form. Same pattern the site's
  own `/ask-your-ai/` due-diligence prompt already tells a reader to check for.
- **Open, and it's the one fact that decides what this actually is:** whether
  Digital Agency Leaders discloses the MarGen connection anywhere on the
  ranking page or its About page. Disclosed → an agency owner transparently
  also running a directory, unremarkable. Undisclosed → a real, structural
  conflict of interest in a ranking that reads as independent. **Needs an
  actual page visit** — WebFetch was unavailable this session; the owner was
  going to check directly.

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
   blocked it entirely; a new session's might not. If it works, go back and
   resolve the two open items from Part 1 — Daniel Dale-Tucker's actual
   LinkedIn headline and Companies House record, and whether Digital Agency
   Leaders discloses the MarGen connection — before relying on either finding
   further.
2. **Mine every competitor mention, not just Tilio.** For every row where the
   `competitors` column names a business — all ten from the aggregate table,
   plus anything else that turns up in the raw data that didn't make the
   top-10 cut — pull the matching `answer_text` and `sources_cited`.
3. **Test Finding 1 against real data.** Do the listicles identified in Part 1
   (Tilio's own list, ClickSlice's lists, the Digital Agency Leaders ranking,
   the other third-party sites) actually appear in `sources_cited`? That's the
   difference between "plausible from desk research" and "confirmed by what
   the assistants actually cited."
4. **Check specifically for `digitalagencyleaders.net` or `margen.net`** in
   `sources_cited` — direct evidence either way on Finding 7.
5. **Break it down by provider** (ChatGPT / Gemini / Perplexity) — which cite
   directories and listicles most, which cite competitors' own sites, since
   that decides which lever (get-listed-elsewhere vs. own service pages)
   matters more and where.
6. **Cross-reference Part 1 and Part 2 into one execution plan** — the actual
   deliverable this was all for. Concretely: which listicles to approach for
   inclusion first, whether a "digital PR / citation" line belongs in the
   product (Finding 4) at Foundation, Grow or Lead level, and what a safe
   self-inclusive comparison page should say, all prioritised by what the real
   citation data shows matters most rather than by what merely seemed
   plausible from desk research alone.
7. **No public "expose / trust-score / ranking" content** — that's parked, per
   the "Considered and not done" section above, unless the owner deliberately
   reopens it.
