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
compares every `£` amount in prose against the canonical price of whichever plan
is named nearest to it on the line.

This is the check that matters most, because prices are rendered from
`business.ts` on the site but restated by hand in the operating documents, and
prose does not recompile. When this repo was first scanned, `ROADMAP.md` and
`HANDOVER.md` still carried the entire superseded ladder — £125 / £750 / £95 /
£250 / £495 — as current fact, four days after the repricing.

**Where it is wrong:** a line comparing an old price with a new one, or quoting
a range, is discussion rather than a statement. Those are downgraded to
`verify` and given no suggested fix, but the downgrade is a keyword guess. Read
the evidence line before changing a number — the fix is printed as a
suggestion, not an instruction.

Amounts with pence (`£1.20 per 150 queries`) are ignored on purpose: they are
running costs, not prices, and matching them as `£1` produced a confident wrong
finding on this script's first run.

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

## refs

Backticked paths that resolve to no file. Bare names are matched anywhere in the
repo, because docs cite `robots.txt` and mean `site/public/robots.txt`.

**Where it is wrong:** deliberate mentions of deleted files. `ops/README.md`
records that `org-chart.md` and `escalation-rules.md` were deleted and why —
that reference *should* dangle, and removing it removes the explanation. Lines
containing deletion language are downgraded to notes for this reason.

A reference to a file that does not exist *yet* — `timings.md`, which an audit
run is supposed to create — is a real finding but not necessarily a fault. It
means the document assumes something the repo does not provide. Decide whether
the file should exist or the instruction should change.

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

Length is often earned — `ops/session-log.md` is a quarter of all prose here and
should not be cut, because it is the record. Look instead for long files that
are *read often*, and for sections inside them that restate what an earlier
section already said.

---

## Fixing the scanner

When a finding is a false positive, change `scripts/config.json` — add a
historical path, a superseded term, a plan alias — rather than ignoring it. An
unfixed false positive is rediscovered and re-investigated on every future run,
which costs more over time than the fix ever does.

If `business.ts` changes shape enough that the parser stops finding prices, the
report says so at the top instead of quietly finding nothing. Do not trust a
clean `facts` result that comes with that warning.
