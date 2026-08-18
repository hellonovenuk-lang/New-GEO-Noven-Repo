# The checks, and how each one is wrong

Read this when a finding surprises you. Every check here was built against real
drift found in this repo, and every known false positive is written down — if
you rediscover one and investigate it from scratch, that is wasted work the
document was meant to prevent.

Run one at a time with `--only <name>`.

| Check | Finds | Trust |
|---|---|---|
| `facts` | prices in prose that disagree with `business.ts` | high |
| `names` | superseded name, domain or address used as current | medium |
| `refs` | backticked file paths pointing at nothing | high |
| `sections` | cross-file "section N" pointers, resolved | needs reading |
| `counts` | "N lines", "N files" claims that no longer match | high |
| `dupes` | near-identical paragraphs across files | high |
| `status` | ops documents with no status in the header | high |
| `bloat` | where the reading cost actually is | context only |

---

## facts

Reads `site/src/data/business.ts` — the declared single source of truth — and
does two things with it.

**One: attribution.** Every `£` amount is compared against the canonical price
of the plan named nearest to it on the line. Three guards keep that honest, each
added after it produced a wrong finding on this repo:

- no other `£` figure may sit between the name and the amount, or a fee column
  three cells away gets charged to a plan;
- if the line already states that plan's correct price, the other number is
  something else — a bank fee, a competitor's rate, a running cost;
- pence amounts are ignored, because `£1.20 per 150 queries` is a cost, not a
  price, and matching it as `£1` is a confident lie.

**Two: ladders.** A line that claims to list plans or tiers and carries three or
more amounts is checked as a set — every amount in it should be a current plan
price. This exists because attribution alone cannot see
`### 3c. Monthly plans (£95 / £250 / £495)`: no plan is named beside the
numbers. Nor does "does it contain a current price?" catch it, since £250 *is*
current — it is the audit's — sitting inside a stale monthly ladder.

This is the check that matters most, because prices are rendered from
`business.ts` on the site but restated by hand in the operating documents, and
prose does not recompile. When this repo was first scanned, `ROADMAP.md` and
`HANDOVER.md` still carried the entire superseded ladder — £125 / £750 / £95 /
£250 / £495 — as current fact, four days after the repricing.

**Where it is wrong:** a line comparing an old price with a new one, quoting a
range, or weighing a price that does not exist yet is discussion rather than a
statement. Those are downgraded to `verify` and given no suggested fix, but the
downgrade is a keyword guess. Read the evidence line before changing a number —
the fix is printed as a suggestion, not an instruction.

The test reads the previous line as well as the current one, because prose
wraps: "The old ladder" sat one line above the numbers it introduced, and
judging the number line alone called a history lesson a fault.

Whole sections can be records too. A heading matching
`record_section_heading` in the config — "The repricing — 2026-08-05" — marks a
section that has to state yesterday's prices to explain today's, and its
contents are skipped down to the next heading of the same or higher level.

**Keep that pattern narrow.** An earlier version accepted any dated heading
containing "changed", which swallowed `ROADMAP.md`'s "What changed on
2026-08-06" — a section about the present — and with it a genuinely stale £95
underneath. A noisy finding costs a glance. A suppressed one costs the whole
point of the check, silently. When in doubt, report.

## names

Superseded terms from `config.json` — the old business name, its domain, its
email — found outside the files that record history.

Aggregated per file rather than per line: a half-finished rename is fixed one
file at a time, and 224 separate findings for one rename is noise, not a task
list.

**Where it is wrong:** the name of a *past event* is not drift. "The Noven
self-audit" is what that audit was called; renaming it in the documents makes
them describe an event that never happened under that name. Lines that read as
narration — ticked checklist items, past tense, "formerly", "archived" — are
separated out and reported as notes. The split is a keyword guess, so check
whether a mention describes today or describes 2026-08-02 before rewriting it.

**The same applies to prices, via `reviewed_facts`.** A repo about money is full
of amounts that are not plan prices — hourly rates, API costs, a competitor's
median, twenty clients' combined revenue — and the attribution rule binds them to
the nearest plan name, which is right often enough to be worth keeping and wrong
often enough to be re-triaged every run. Ten were judged on 2026-08-08. Keyed on
**file and amount, not line**, so a condensing pass moving the text does not
strand the entry.

**It can only ever downgrade a `verify`.** An error — a document stating a price
this business has stopped charging — cannot be silenced from the config, and the
code makes that structural rather than a convention. Tested both ways before it
was committed. If a fact is wrong, fix the fact.

**When you have judged a file, record it.** `reviewed_names` in the config holds
file/term pairs already found correct, each with its reason and the date. Those
drop to notes — still printed, reason attached, so the judgement stays visible
and can be reversed — instead of arriving as errors every run. Twenty-four pairs
were recorded on 2026-08-07 after a full triage.

This is the honest way to quieten this check. The alternative, tightening the
regex until the noise stops, was tried and rejected: the mentions are spread
across a long tail of phrasings with no pattern that separates "the Noven
self-audit" from a stale fact, and every tightening risks hiding real drift.
Delete an entry whenever a file's purpose changes.

## refs

Backticked paths that resolve to no file. Bare names are matched anywhere in the
repo, because docs cite `robots.txt` and mean `site/public/robots.txt`.

**Where it is wrong:** deliberate mentions of deleted files. `ops/README.md`
records that `org-chart.md` and `escalation-rules.md` were deleted and why —
that reference *should* dangle, and removing it removes the explanation. Lines
containing deletion language are downgraded to notes for this reason.

Three more classes are excluded, each for its own reason:

- **Build output.** `dist/index.html` is absent from a clean checkout by design.
- **Ticked checklist items and "Deleted" sections.** `- [x] ops/spine.md →
  ops/client-record.md` records the rename; the dangle is the record working.
- **Files that live outside this repo**, listed as `external_files` in the
  config. `ops/audit-method.md` §5 puts client audit data in the client's own
  folder, so the per-run `timings.md` is *supposed* to be missing here. That one
  was investigated from scratch before being recognised — which is exactly the
  cost this document exists to prevent.

## sections

Resolves pointers like ``see `service-tiers.md` section 9`` and prints the
heading actually found there.

Almost every result is `verify`, and that is correct: whether section 9 is still
the section that was meant is a question about sentences, not numbers. Sections
get inserted above one another and pointers silently change meaning without ever
breaking. `ops/README.md` pointing at "section 9, the 2026-07-31 repricing" is
literally true and stale as guidance, because section 11 is the repricing that
set today's prices.

An `error` here — the section does not exist at all — is unambiguous.

## counts

Two forms, both found in this repo:

- ``` `session-log.md` — 1,100 lines ``` when it is 2,726
- "Fourteen files besides this index" when there are 18

Prose that counts something is the quietest liar in a repo. It was true when
written, nobody re-reads it, and it decays on every commit. A 10% tolerance is
allowed on line counts because round numbers are usually approximations.

**Where it is restrained:** "N files" only fires when the sentence names the
directory it is counting, or sits in the first ten lines of a folder index.
"Six files agreeing with each other" counts an argument, not a folder, and
earlier versions of this check flagged those confidently and wrongly.

Consider replacing a brittle count with a phrasing that cannot go stale, rather
than correcting the number and leaving it to rot again.

## dupes

Paragraphs of 200+ characters that are 75%+ identical across files, by
four-word shingle overlap.

Duplication is where inconsistency is born: two copies of a fact are two chances
to update one and forget the other. It is also plain cost — every session that
reads both pays twice for one idea.

Near-duplicates rather than exact ones are the interesting case, because those
are copies that have already begun to diverge. Decide which file owns the
passage; make the others point at it.

**Where it is wrong:** a banner intentionally repeated at the top of `README`,
`HANDOVER` and `ROADMAP` so that no entry point misses it may be worth keeping
in triplicate. That is a judgement about who reads what, and only you can make
it. If you keep it, keep it *identical* — a divergent banner is the worst
outcome available.

**Record that judgement in `reviewed_dupes` rather than re-making it.** Same
principle as `reviewed_names`: file pair, plus the reason. The rename banner was
recorded on 2026-08-08 after being re-investigated on three consecutive runs.

The exemption is **conditional on the copies staying identical**, and that is
enforced rather than trusted. While they match, the finding drops to a note with
the reason attached. The moment they drift it is reported as an **error** — a
higher grade than an ordinary duplicate gets, because a banner saying different
things at three entry points is worse than one written once, and catching that
is the entire reason the pair is worth listing. An exemption that went quiet on
divergence would be hiding the one thing it was written to watch.

## status

`ops/README.md` defines a four-word vocabulary — **Live**, **Decided,
unvalidated**, **Closed**, **Stub** — and says it is worth adding to each file's
header. Most files never got one.

The distinction is the one most easily got wrong in this repo, and the most
expensive: a decision written down reads exactly like a thing that works. Eight
of the operating documents describe procedures that have never been performed.

## bloat

Not a fault. It exists so a condensing pass starts where the reading cost is
rather than wherever a file happened to be open.

Length is often earned. `ops/session-log.md` is the largest file here and is the
record, so it is not cut for being long — it is cut only on the settled-versus-live
rule in its own header, and never by this check. Look instead for long files that
are *read often*, and for sections inside them that restate what an earlier
section already said.

**One shape is worth scanning for by eye, because no check finds it.** A
checklist item whose first paragraph is an instruction and whose remaining
paragraphs are history: a closed comparison, the justification of a change
already shipped, a reflection on what a decision cost. The unticked box makes
the whole entry read as live. `ROADMAP.md` §1c carried 311 words this way and
needed 185. The method is in `editing.md`, worked example 2.

---

## Fixing the scanner

When a finding is a false positive, change `scripts/config.json` — add a
historical path, a superseded term, a plan alias — rather than ignoring it. An
unfixed false positive is rediscovered and re-investigated on every future run,
which costs more over time than the fix ever does.

If `business.ts` changes shape enough that the parser stops finding prices, the
report says so at the top instead of quietly finding nothing. Do not trust a
clean `facts` result that comes with that warning.
