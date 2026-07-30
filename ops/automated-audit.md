# Automating the £30 audit

**Internal document.** Decides how much of the audit a machine does, what a human
must still look at, what it costs to build and to run, and what the report is
allowed to claim. Written 2026-07-30.

**Status: section 3 is decided. Sections 1 and 2 are new and thin.**

> **A note on this file's history, because it matters for reading it.** An earlier
> session produced findings on automating this audit and they were never
> committed — this path does not appear anywhere in the repository's history on
> any branch. So sections 1 and 2 below are written fresh and are deliberately
> short; they are not a recovery of anything. Section 3 is a full re-derivation,
> not a revision, done because the earlier version proposed a weekend-sized first
> build that dropped cross-source fact consistency and per-question page
> answerability. Those are two of the three site-side checks
> `site/src/pages/how-it-works.astro` promises out loud, so they were never
> available to drop.

---

## 1. What the audit has already promised

`how-it-works.astro` stage 01, second paragraph, is the binding text:

> "Then we look at why. We check what the AI crawlers can and can't read on your
> website, whether the basic facts about your business are consistent across the
> places these systems draw from, and whether anything on your site answers the
> questions being asked."

**Three site-side checks, all published, none droppable.** Everything in section 3
exists to deliver those three and nothing else. Where a design decision reduces
what we can claim, section 3 says so against this paragraph specifically.

The rest of the audit — asking the assistants the client's customer questions and
recording what comes back — is settled elsewhere and not re-opened here. See
`ops/third-party-services.md` section E2 for the cost model and E3 for the
non-determinism finding, and `ops/service-tiers.md` section 3 for the question
and run counts. The shape it fixes: **10 questions, 5 runs each, across four
assistants — 200 grounded calls per audit.**

## 2. Why automate it at all

Two reasons, and only the second one is about money.

`ROADMAP.md` 3a: *"Do the first one end to end and time it. £30 has to be
sustainable, so if it takes a day, the process is wrong, not the price."* That is
the test this whole document is written against.

And `ops/service-tiers.md` section 6: the ceiling on this business is delivery
time, not price. The audit is also the outreach tool — priced to be an easy yes,
converting into Foundations, which are the actual year-one income. **So the audit
does not have to be profitable on its own. It has to be fast enough not to eat
the month.** That distinction decides several arguments below.

---

## 3. How we detect the two findings that matter

Re-derived 2026-07-30 by five specialists working the problem separately —
crawler access, machine-readability, source conflict, false positives, and
reporting — then a debate round in which the false-positive work was put back in
front of each designer to concede, hold or resolve. The concessions changed the
design substantially and are recorded here, because the reasoning is the part
worth keeping.

The two findings, in the owner's words:

1. **Their information conflicts across sources** — different phone number,
   address, opening hours, business name or services in the places these systems
   draw from — and we flag it, with evidence.
2. **Their website can't be properly read by AI systems** — crawlers blocked,
   content only present after JavaScript runs, structured data absent or
   malformed — and we flag it, with evidence.

### 3.1 Five rules that bind every check

These came out of the debate as the things that stop the audit producing
confident nonsense. They are not negotiable per-check.

1. **Three outcomes, never two: pass, fail, and could-not-determine.** No check
   returns a boolean. A source we could not read is never reported as a source
   that disagrees with us. This is the single most important rule in the document.
2. **Every finding carries the URL, the verbatim quoted text, the date, and what
   it was compared against.** A finding missing any of the four is rejected at
   write time, not caught in review.
3. **Counts, never percentages.** Five runs resolves to twenty-point steps; a
   percentage is false precision. "You were named in 14 of 200 answers." This
   supersedes the "report as a rate" wording in `ops/third-party-services.md` E3
   and `ROADMAP.md` 3a — **both need correcting, and that is an open item in
   section 3.9.**
4. **Never assert a third party is wrong.** We report that two things disagree and
   which is which. We do not adjudicate whose data is stale unless we can prove
   it.
5. **Inputs are declared, and a check whose input failed emits
   could-not-determine automatically.** Enforced by a dependency graph in the
   fetch harness, not by per-check guards — ad-hoc guards are exactly how the
   worst bug in the first draft got missed (3.3).

### 3.2 Finding 2, part one — can these systems read the site at all

**The file that tells crawlers what they may read, parsed properly.** Full RFC
9309: group consolidation, the product-token match rather than the whole
user-agent string, longest-path precedence, Allow winning ties, `*` and `$`
wildcards, case-sensitive paths, the 500 KiB truncation limit. The trap that
produces most real findings is group specificity — a `GPTBot` group makes the `*`
group inapplicable to GPTBot *entirely*, so a site with `User-agent: * /
Disallow: /private` and a permissive `GPTBot` group does not protect `/private`
from GPTBot at all, and the reverse configuration silently blocks it completely.

The crawler roster is split by job, because conflating them produces a false
finding: the **training and ingest** crawlers, the **live retrieval** crawlers
(the group that actually decides what an assistant can say about this client
today), and the **classic search bots** that feed the assistants indirectly —
Bingbot matters here far more than Bing's market share implies, because it feeds
Copilot. Two tokens in the roster, `Google-Extended` and `Applebot-Extended`, have
no crawler behind them at all; they gate training use, not fetching, and the
report must never describe a `Disallow` there as a block.

**A live fetch with those user-agent strings, because the file is a claim and a
fetch is evidence.** Status codes, redirect chains, `noindex` in both the meta tag
and the `X-Robots-Tag` header (kept strictly separate from the file, because one
controls fetching and the other controls listing — same symptom to the client,
different fix), canonical disagreement, and soft blocks: an HTTP 200 carrying a
challenge interstitial, which is more dangerous than a 403 because every test the
owner runs in their own browser passes.

**Content only present after JavaScript runs.** Raw HTML against rendered DOM,
extracted with the identical normaliser on both sides or the diff means nothing.
Playwright and Chromium, two pages only — it is the slowest step in the audit by
two orders of magnitude. Metrics: main-content length ratio, headings absent from
raw, the specific business facts absent from raw, and framework fingerprints (an
empty `#root`, an `<astro-island>` with no slotted content) which turn a
measurement into a diagnosis with a named cause.

**Sitemap**, only as far as it bears on readability: present, parses, sampled URLs
return 200 without redirecting, and the sitemap's own URL is not itself
disallowed by the file — which is common and real.

### 3.3 What the debate changed about that, and it is a lot

**A fail-quiet bug, conceded as the worst defect in the first draft.** The status
table mapped "4xx other than 429 → treat as unavailable → allow all", which is
what RFC 9309 says a *crawler* does. Applied to a 403 served specifically to our
user agent, it made the tool report "no restrictions on AI crawlers" having parsed
nothing at all. A check that silently starts passing everything is worse than one
that crashes. The fix is not a missing case but a conflation: every result now
carries two fields — `inferred_crawler_behaviour`, which stays faithful to the
RFC, and `audit_confidence`, which records whether we actually observed the file
the crawler sees. A parked domain gets its own gate and makes the **entire audit**
could-not-determine, because nothing downstream of a parked domain means anything.

**The crawler-block finding is cut from v1 as a finding, and ships as an
observation.** This is the biggest reduction in the document and the designer of
the check argued for it. The problem is that we fetch with a spoofed user-agent
string from an IP in no vendor's published range, sending no bot-authentication
signature, and Cloudflare rolled crawler verification to free and pro plans with
default-on enforcement in June 2026. Our request and a real crawler's can differ
**in both directions** — we can be challenged *because* we are unverified while
the real crawler passes, or we can sail through as an unremarkable generic client
while the genuinely verified crawler is blocked by a rule keyed on the verified-bot
category rather than the string.

The first draft claimed a before-and-after browser control "narrows it to the user
agent". The false-positive work broke that on three counts, all conceded: request
headers were never required to match, so a rule keyed on missing client hints
produces the identical pattern with the user-agent string irrelevant; cookie jars
were not isolated, so a shared clearance cookie makes the second control pass for
the wrong reason; and cadence was not controlled, so across fifty-odd requests
whichever fetch trips a per-IP threshold gets challenged — and cadence throttling
often returns 200-with-interstitial, which the soft-block detector reads as
policy.

Controlling all three is roughly nine to thirteen hours of work whose calibration
is entirely unmeasured, to support a claim whose failure mode is telling a paying
client their site blocks GPTBot when it does not — the one finding where they can
get a contradicting answer from their own dashboard in a single click. **So v1
records what each user-agent string received, on what date, in the technical
appendix, and makes no attribution claim.** The report cannot say a crawler is
blocked by a CDN. It can still say a crawler is blocked by the file that tells it
what to read, which is provable from a file and is the far commoner case on UK
small-business sites. The honest ask goes in the report: send us your bot
analytics or host logs and we will tell you definitively.

**The JavaScript finding is reframed as a consumer split, and stripped of vendor
names.** "Your site can't be read" is not defensible. The false-positive work
proposed "Google runs JavaScript, so answers through Google still see it" — and
the designer went further than the attacker, refusing even that: the clause was
not verified this round, and asserting it from memory is what `CLAUDE.md` forbids.
So v1 says only what it measured, naming no vendor, and carries a per-vendor
`renders_javascript` field that stays `[PLACEHOLDER]` until each vendor's own
documentation is read and cited with an access date.

**The baseline cascade.** One 403 against our own honest user agent collapses
roughly thirty-five to forty result cells across all three checks — and worse,
flips two of them to *confident false positives*, because Playwright still renders
successfully, so the raw-versus-rendered diff compares an empty raw against a full
DOM and diagnoses a JavaScript-only site. Hence rule 5 in 3.1. On consent, the
designer split what the attacker had merged, and the distinction is right: **the
client's own robots file disallowing us is a consent-wording change** — robots.txt
is a request from a site's operator to automated clients, the client *is* the
operator, and they are giving us a specific written contrary instruction about
their own property, so we fetch at limited volume and report the disallow as a
finding in its own right. **A WAF 403 is not**, and no consent wording moves it:
that is an active control, not a courtesy norm, and written client instruction
does not authorise us to evade it. No IP rotation, no masquerade to get past it,
no challenge solving. We escalate and ask the client to allowlist us — which is
the honest reason a small number of audits will not complete same-day, and it
belongs at checkout rather than being discovered on delivery.

**One politeness contract, owned by the fetch harness.** A one-second delay is a
delay, not a rate limit, and WordPress security plugins throttle on per-minute
counts. So: one process-wide per-host token bucket, no component gets a raw HTTP
client, 1 request/second **and** a hard ceiling of 20 per rolling 60 seconds per
host. First 429 or cadence-shaped interstitial backs off globally; the second
aborts that host and prints the reduced page count in the report. Every component
declares its per-host budget up front and the harness refuses an audit that
exceeds the ceiling.

### 3.4 Finding 2, part two — the machine-readable summary, and answerability

**Structured data.** JSON-LD and Microdata both extracted — Microdata stays in
because the client base is Wix and older WordPress where it is still common, and
reporting "absent" when facts are present is the one error we cannot make. RDFa is
detection-only, flagged to the human as "present in a format we don't fully read",
never a false absent. Parse defects are each their own finding with a byte offset,
and HTML-escaped entities inside the script block get their own class because
`<script>` is raw text per the HTML spec, so that genuinely breaks.

**Validity and completeness are different findings with different verbs** — broken
versus thin — and the debate demolished most of the validity half.

Conceded: **range and domain checking comes out of fail-tier entirely.** The
argument that landed was not the list of patterns where a home-built checker
disagrees with Google's (Text-or-class unions, bare-host `sameAs`, `dayOfWeek:
"Monday"`, `latitude` as a string, `@type` arrays, `priceRange` on `Organization`)
but the **oracle argument**: the design ruled out the hosted validators as a
dependency and then proposed a hand-curated override list, which means nothing in
the design could ever adjudicate an override. Range violations become advisory.
Fail-tier becomes a fixed list of about twelve unambiguous patterns — empty
string, `null`, "N/A", template placeholders left in, malformed URL scheme,
invalid ISO time, a phone number under nine digits.

Also conceded: **a freetext `address` string is demoted from a defect to an
opportunity.** The first draft wrote "legal per schema.org's range" and then made
it a Tier-1 finding, which is a recommendation dressed as a defect on a page
Google passes clean. It splits by recoverability instead — a string a regex can
pull a valid UK postcode out of is a pure opportunity; "opposite the church,
Heswall" stays low-tier but is headline-eligible, because a machine genuinely
cannot place that business.

The vocabulary loader survives, at half the hours and for different jobs: a
**three-way type lookup** (known / unknown-in-our-pinned-release /
could-not-determine, never "this type is not real"), which also kills the
"schema.org ships a release and we start failing new types" failure mode; reading
`domainIncludes` positively to know what to look *for*; and subclass walking so
Plumber and Dentist inherit LocalBusiness completeness properly.

Two nodes both claiming to be this business with different phone numbers is one of
the strongest findings available and costs nothing to detect — but it fires on
accreditation bodies, suppliers, review embeds, head office plus branch, and a
sole trader's `Person` alongside their `Organization`. It now fires only on
same-name, both-business-typed, mutually-unreferenced nodes with different
geographic subscriber numbers and no differing postcode.

**Answerability — does any page answer each of the ten questions we asked.**
Sitemap plus a politeness-capped crawl. A BM25 shortlist per question over
weighted fields (headings ×3, title ×2, body ×1), then **one LLM judgement per
question against its shortlist — ten calls, fixed, regardless of site size.**

The judge is constructed so that flattery is structurally impossible rather than
discouraged. It is asked **backwards**: *quote the single passage that answers
this question, or return null* — so the default output is nothing and a verdict
without a quote cannot exist. **Every quote is then verified in code** as a
verbatim substring of the named page, which kills paraphrase-as-evidence and
hallucinated quotes outright. Position and heading structure are computed by us,
not by the model, so the model cannot upgrade its own verdict. And the named
failure mode is written into the prompt: a page being on the same topic is not an
answer, and if the passage would be equally true of any competitor, return null.

The debate reshaped this too. **The position windows are ungraded.** The first
draft failed an answer sitting behind a legitimate one-paragraph intro, and
downgraded the W3C-recommended disclosure pattern that real visitors use happily —
imposing a house style and calling it a defect. Resolved into two axes:
**answerability is graded** (a passage exists, it is self-contained, it is in the
visible text) and **prominence is printed as facts and never grades anything** —
"the answer starts about 90 words after the heading 'Our Services'", whether that
heading is real markup, whether it was collapsed at first paint. Each line maps to
a named Foundation fix. Note honestly: "near the top, under a heading" was the
brief's phrasing, not the published promise. Stage 01 says only "whether anything
on your site answers the questions being asked", so this concession does not touch
what the site claims. It does soften the brief, and that is said out loud rather
than quietly.

Conceded as a straight bug: an empty shortlist went directly to "not answered" at
zero cost. **An empty shortlist is a statement about our retrieval, not about the
site.** It now triggers a recall-biased fallback and then could-not-determine. The
same reasoning fixed image headings — a Wix hero whose heading is a picture leaves
the ×3 field empty, so the page never shortlists and we assert "not answered"
about a page that answers it. And the synonym problem is solved by *not* curating
a list that rots: widen the shortlist to eight, drop the score floor, let the
judge discriminate. Trades a maintenance burden for about ten pence of tokens.
PDFs are deferred honestly: we detect a linked price list and downgrade the
question to could-not-determine naming the PDF, rather than pretending we read it.

### 3.5 Finding 1 — conflicting facts across sources

**Sources are discovered from citations we have already paid for.** All 200
grounded calls return citations. Capture them, resolve them (Gemini's are
redirect URLs and must be resolved at capture time, not report time), reduce to
registrable domain **via the public suffix list** — naive splitting turns
`plumber.co.uk` into `co.uk` and merges every UK business into one bucket — and
count. "Cited in 12 of 200 runs." Then fetch only the domains that actually
influence answers about this business.

**Assessed honestly against a fixed directory list, the answer is both.** Citation
discovery is necessary and not sufficient: it is structurally biased toward
sources that are already working, so a directory holding a five-year-old phone
number that is never cited is never seen; the citation set is partly an artefact
of our own question wording; and the cold-start case is worst precisely for the
client most likely to buy a £30 audit. So a small seed list runs alongside it,
and the highest-yield item on it costs one onboarding question — *which listings
and directories are you on?*

**Companies House** is free, is used for **name and status only**, and its
registered-office address is explicitly excluded from adjudication: a virtual
office is entirely legitimate and this business uses one itself
(`ops/third-party-services.md` B1). A sole trader has no record at all, which is
`not applicable` and never a conflict.

**Google Places is deliberately not used as an evidence source.** Its terms
restrict caching to 30 days with a place-ID exemption and require attribution;
our evidence rule requires storing quoted text and a date indefinitely in a client
report. Those are in direct tension and the exact clause text could not be read —
Google's own pages returned 403. `[PLACEHOLDER: confirm the current Maps Platform
Service Specific Terms directly, and the Place Details pricing, before revisiting.]`
Instead the client's Google listing is read **with the client on the onboarding
call** — they are the licensor of their own data, the quote is theirs to give, and
watching their own stale listing on a call sells the Foundation better than a
paragraph ever will.

### 3.6 What the debate changed about that — including the biggest hole found

**The verbatim guard proves presence, not attribution, and this was missed
entirely.** The rule that every extracted value must be quotable verbatim from the
fetched page is a good rule and it stops hallucination. It does nothing to
establish that the string is *about this business*. A phone number in a footer
advert, a "similar businesses nearby" module, a review quoting an old address, a
directory's own call-tracking number, a category page listing twenty plumbers
where the client is row nine — all pass the guard and all produce a quoted, dated,
**severity-one** conflict.

Conceded, and the designer made it worse before making it better: the source
selection rule *preferentially* surfaces exactly those category pages, because
those are what get cited for "who's a good plumber in Birkenhead". **The mechanism
that finds sources is the mechanism that feeds the false positive.**

The attacker proposed resolving a subject node, with a fallback to "the smallest
DOM container holding both a name match and the value". The designer rejected the
fallback as assertable — on a flat list of sibling divs it will happily pair row
nine's name with row ten's number, and on a table there may be no container
holding both — and resolved it harder: **assert a value only when a structured node
whose name matches carries it as its own property, or the page contains exactly one
candidate of that field type in total and the declared name appears within 400
characters of it.** Everything else is could-not-determine. Most listing pages then
yield nothing, which is correct rather than degraded. It also kills the
call-tracking case free, because a proxy number appears identically beside twenty
different names and fails the single-candidate test.

**The reference can invert, and that is the most embarrassing report we could
send.** Comparing everything against what the client told us at onboarding is
right — using their website as the reference would make their website's own errors
structurally invisible, which is the finding the owner most wants. But the
reference is one unverified verbal claim from someone with every incentive to
describe their business as they wish it were. If they are stale or aspirational,
every conflict points the wrong way and we tell fifteen directories they are wrong
about a business whose data is fine.

Resolved better than either opening position. The attacker wanted consensus
inversion at three or more agreeing sources; the designer pointed out that three
directories syndicating from one feed are one source and there will never be a
syndication map. So inversion fires when three or more distinct domains disagree
with the client **and at least one of them is a source the client controls** —
their own site, their Facebook page, their Companies House record. A
client-controlled source siding with the directories is real evidence the
declaration is stale. Three unrelated directories agreeing is just as likely one
stale feed replicated, and resolves to could-not-determine in *either* direction.

**Six legitimate-difference cases were missed and all six are conceded.** The
worst is service-area businesses: `ops/service-tiers.md` names the sole-trader
trades as the market, and a mobile trade is exactly the client for whom the
postcode anchor is meaningless — the first draft would have generated address
conflicts against every source for an entire customer segment. Also: an address
the client abandoned deliberately and the directory refuses to remove; a
mid-flight rebrand or a franchise under a national brand; a dormant company in a
sole trader's name, which fired the "dissolved company still trading" finding
falsely; call-tracking numbers, which are correct data deliberately published; and
seasonal hours.

The onboarding model that fixes them is deliberately tiny, because onboarding is
currently two minutes. **Two new questions** — *is this one place customers come
to, several places, or do you go to them?* (one tap; service-area switches address
adjudication off entirely) and *any other name you've traded under, or are moving
to?* (usually no). **One derived** — we query Companies House ourselves and ask
*is this you? yes / no / I'm a sole trader*, which kills the dormant-company false
positive without anyone needing to know their company number. Suppressions are not
an onboarding field at all: they are a byproduct of the first audit's own review
("that's my old address, they won't remove it"), and they matter for Maintain
rather than for the one-off.

**Hours narrowed, services dropped.** The attacker wanted both cut from
adjudication. Services conceded fully — trade vocabulary drift ("boiler servicing"
versus "gas appliance maintenance") produces more legitimate differences than
findings. Hours held, but narrowed to one class, and the distinction is a good
one: `openingHours` is a *recurring schedule*, not a calendar, so a bank holiday
is not in it. Seasonal and bank-holiday noise all moves opening and closing
*times*. A source publishing "Sunday 10–16" for a business that has never opened
on a Sunday is a genuine conflict that none of the false-positive scenarios
explains. **So v1 adjudicates day-level open/closed only, and prints the times
side by side without judging them** — which is arguably more useful to a client
than a verdict.

**Cold start gets materially worse, and the check inverts in shape rather than
failing.** Entity-scoping strips out multi-entity pages, and an invisible
business's citations are *disproportionately* multi-entity pages — when a business
has no properties of its own, the only reason it is ever cited is that it appears
in someone's list. So for an invisible sole trader the output is a **coverage map,
not a conflict table**: their own site against their declaration, Companies House
if incorporated, their Google listing read on the call, and the absence itself as
a counted, dated finding. *"Across the 200 times we asked, 47 different websites
were used to answer. Yours was used twice. We looked for you on six named places
on 30 July 2026 and found no entry on four of them."* That is true, evidenced,
and more useful to that client than any conflict table — and it is a legitimate
reading of the published promise, because **you cannot be inconsistent where you
are absent.**

### 3.7 The report

Five sections, and the ordering is a decision rather than a default. **The
assistant results lead**; the site-side findings follow as the explanation. Lead
with "your machine-readable summary is thin" and it reads as a sales pitch; lead
with "you were named in 14 of 200 answers, and here is what's in the way" and the
identical finding reads as a diagnosis. `how-it-works.astro` already sequences it
this way — *"Then we look at why."*

The three site-side checks are merged into **one severity-ordered section, not
grouped by which check produced them.** A business owner does not care that one
finding came from a file and another from a directory. Severity is ranked by what
it costs the business, not by technical seriousness — which puts a wrong phone
number above a blocked crawler, and that is deliberate.

Technical vocabulary is quarantined into a final block addressed to whoever looks
after the website. That quarantine is what makes plain English possible in the
body; without somewhere for the precise names to live, they leak into sentences a
plumber is trying to read in five minutes. The standing phrasings: robots.txt is
*"the file on your site that tells these systems what they may read"*; structured
data is *"the machine-readable summary of your business details"*; rendering is
*"content that only appears once your site's code has run"*.

Every finding carries the same four-line evidence block, so the eye learns to skip
or read it at will:

> **We checked:** https://example.co.uk/contact — 30 July 2026
> **We found:** "0151 555 0199"
> **Compared against:** the number you gave us, 0151 555 0123

Every conflict sentence drops any implied direction: *"These two don't match —
whichever is out of date, one of them needs changing."* Never "your listing is
wrong", never "[source] is wrong". And where consensus has inverted, the same
evidence produces the opposite recommendation: *"Five places agree on a phone
number that isn't the one you gave us. That pattern usually means the older number
is the one that's spread, not that five directories are wrong together."*

**The good-news path is a first-class layout, not a fallback.** The site promises
*"If you're already in good shape, the report says so and we don't try to sell you
the next stage"* — so passes are stated as plainly as failures, and there is
written wording for "you don't need us", for the awkward middle (a few small
things, not £350 worth), and for both mismatch cases: assistants naming the client
happily while the site is poor, and a good site with almost no visibility. That
last is the most commercially awkward report this business can produce and is
therefore the one most worth writing before anyone is looking at a bank balance.

**The prose comes from fixed templates with slot-filling, not an LLM pass.** An
LLM writing the findings has the numbers and quotes in context and will
occasionally interpolate — "a number of directories", "most of these systems" —
and every one of those is an invented fact in a document carrying our name and a
fee. A template can only say what it has slots for, and it makes the same finding
read identically across twenty audits, which is what `ops/service-tiers.md`
section 6 means by systematising from client one. **`[PLACEHOLDER]` is a
send-blocker**, not a marker: no report leaves with one in it, which is how the
no-invented-facts rule becomes mechanical rather than aspirational.

### 3.8 What it costs

**Build hours.** Solo developer with an AI coding assistant, Node/TypeScript.
These are the post-debate numbers; every component grew.

| Component | First draft | After debate |
|---|---|---|
| Crawler access — file parsing, fetch matrix, JavaScript diff, sitemap, shared fetch harness and politeness contract | 42–70 | **71–115** |
| Machine-readable summary (structured data) | 33–49 | **40–57** |
| Answerability (the ten questions against the site) | 30–44 | **43–62** |
| Source conflict — discovery, extraction, adjudication | 21–34 | **33–51** |
| Reporting layer — templates, evidence blocks, severity sort, output | — | **28–43** |
| **Total** | | **215–328** |

Deferring the crawler-block attribution controls (3.3) takes roughly 9–13 hours
out of v1, so **v1 is about 206–315 hours.** That is five to eight weeks of
full-time work. The weekend estimate in the earlier version was not merely
optimistic; it was wrong by more than an order of magnitude, and dropping the two
promised checks is what made it look achievable.

**Running cost per audit.**

| | Cost |
|---|---|
| Citation capture across the 200 grounded calls | £0 — already paid for by the visibility check |
| ~52 crawler-access requests, page fetches, redirect resolution | sub-penny |
| Two Playwright renders | ~0.5p `[PLACEHOLDER: confirm the host's per-second vCPU rate]` |
| Companies House, OpenStreetMap, public-suffix and vocabulary lookups | £0 |
| Answerability judge — 10 calls, Sonnet 5 via the Batch API | ~45p (Haiku ~15p) |
| Fact extraction — ~15 pages, Haiku via Batch | 3–6p |
| Report generation | <1p |
| **Site-side total** | **~50p** |

Against the sub-£2 budget in `ops/third-party-services.md` E2, and with Google's
free grounding allowance covering 25–40 audits a month, a complete audit lands
comfortably inside £1 in the common case. **Money is not the constraint. It never
was.**

**What stays manual — 65 to 90 minutes per audit.** This is the number that
decides whether the process works.

| | Minutes |
|---|---|
| Crawler access — render screenshots, the could-not-determine sweep, malformed-file read, baseline-blocked triage | 17–25 |
| Structured data and answerability — every "not answered" opened and checked, cross-check conflicts read | 22–32 |
| Source conflict — attribution check on every severity 1–4 conflict, legitimate-difference triage | 14–20 |
| Report — read it once as the client, confirm the recommendation matches the findings, covering email | 10–15 |

Three things make that survivable. It is the **same** hour every time, so it
systematises. It clears the bar `ROADMAP.md` 3a actually set — an hour is not a
day. And there is a **tail cap**: manual time scales with conflict count, so above
six conflicts at severity 1–4 the audit is escalated rather than triaged
item-by-item, and the report names the six costing most and lists the rest.
Without that cap one messy client eats the margin on fifty audits.

**But be clear about what this means commercially.** At £30 for an hour-plus of
human time, the audit does not pay for itself and is not supposed to. Section 2
already says why: it is the outreach tool, and the Foundation is the income.
Anyone reading this later and tempted to "fix" the audit's margin should raise the
Foundation conversion rate, not the audit price.

**Maintenance, and the category that matters.** A check that crashes is a good
day. The dangerous failures are silent: a challenge-markup change stops the
soft-block detector matching and 200-with-interstitial starts reading as a pass; a
renamed user-agent token means we send a stale string, get a clean 200, and report
"allowed" having tested nothing; a change to Gemini's grounding shape empties the
citation array and the check reports fewer conflicts, camouflaged as cold start.

Two structural answers, budgeted nowhere in the first draft. **A canary suite**
asserted every run — URLs known to challenge, known-good fixtures, one known
multi-entity page — which converts most quiet failures into loud ones. And
**zero-result assertions**: a robots file over 200 bytes that parses to zero rules
is an error, not a result; a provider returning zero citations across all fifty of
its runs is an error, not a result. Roughly 6–10 hours to build, **3–5 hours a
month ongoing.**

One correction worth recording, because the two were nearly conflated: a canary
against a challenging URL **cannot detect a stale user-agent string**, because a
URL that challenges everything challenges the old string exactly as it challenges
the new one. Only pinning each string with its source URL and diffing the vendor's
published page on a schedule catches that. A second canary — running the full
matrix against our own site, where we control the file and can plant a
`Disallow: /canary-gptbot` inside a single crawler's group — tests parser, group
specificity and roster end to end, and catches a token typo for free. It is also
exactly the self-test `ROADMAP.md` 1e wants anyway.

### 3.9 What ships in what order, and what is still open

Sequenced so that each phase produces findings we could put in a real report,
rather than infrastructure that produces nothing until the end.

1. **The spine** — fetch harness, politeness contract, input-validity dependency
   graph, evidence record, report skeleton. Nothing ships without this and every
   component depends on it.
2. **Finding 2** — the file parsing (highest-confidence check in the audit and it
   fails safe once the 4xx bug is fixed), the JavaScript diff with vendor-free
   wording, the sitemap checks, and the structured-data half. The fetch matrix
   ships here as an appendix of facts.
3. **Finding 1** — citation capture, entity-scoped extraction, adjudication, and
   the cold-start coverage-map variant.
4. **Answerability** — the ten questions against the site, with every "not
   answered" human-reviewed until the calibration set clears the judge.
5. **Deferred to v2** — the crawler-block attribution claim and its controls, PDF
   extraction, and range checking if it is ever worth revisiting.

**Open, and each one blocks something:**

- **Counts versus rates in two existing documents.** `ops/third-party-services.md`
  E3 and `ROADMAP.md` 3a both say "report a rate" and quote 20%–80%. Rule 3 above
  supersedes that. Both need correcting so a future session doesn't build to the
  wrong instruction.
- **Google Places terms** — `[PLACEHOLDER]`, section 3.5. Resolving it would
  recover the highest-impact source in the set.
- **Per-vendor JavaScript rendering** — `[PLACEHOLDER]`, section 3.3. Until each
  vendor's own documentation is read and cited, the report names no vendor.
- **Checkout terms**, covering both the user-agent technique and the client's
  written instruction to fetch their own site regardless of their robots file.
  `[PLACEHOLDER: have the wording reviewed before the first paid audit.]`
- **Evidence retention** — we are storing copies of client site bodies.
  `[PLACEHOLDER: confirm the retention period and the UK GDPR lawful basis.]` This
  touches the ICO registration in `ROADMAP.md` 1c.
- **The judge calibration set** — 20 hand-labelled pages, a hard gate before an
  unreviewed "not answered" ever ships.
- **Every threshold in this document is asserted, not measured.** The page caps,
  the citation-count floor, the 400-character attribution window. `ROADMAP.md` 3a
  says do the first one end to end and time it. That still stands, and it is worth
  more than any number above.
