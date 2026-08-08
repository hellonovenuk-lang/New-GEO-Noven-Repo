---
name: repo-consistency
description: >-
  Sweep this repo for facts that contradict each other, references that point at
  nothing, self-describing prose that has gone stale, and duplicated or bloated
  writing that costs tokens to read — then fix what is unambiguous and put the
  rest to the owner. Use this whenever the owner asks to check, audit, tidy,
  clean up, reconcile or "go over" the repo or its documents; whenever they say
  files contradict each other, a price or name is wrong somewhere, the docs are
  too long, or sessions are burning too much context; and — without being asked
  — straight after any rename, repricing, or decision that changes a fact stated
  in more than one file, because that is the moment drift is created.
---

# Repo consistency

## Why this exists

This business sells the claim that a company's facts are consistent everywhere a
machine can read them. The audit's third promise is exactly that, run on other
people's businesses. A repo that contradicts itself is therefore not untidy — it
is the product failing on the vendor.

The second reason is cost. This repo holds tens of thousands of words of prose —
run the `bloat` check for the current figure rather than trusting a number
written here, which is how the last one went stale by more than double.
Every session that reads the wrong half of it pays for the privilege, and a
duplicated paragraph is paid for twice. Cutting what nobody needs to read is
work with a return.

## The shape of the job

The mechanical sweep is done by a script, so it costs nothing and misses
nothing. Judgement is yours. Do not read files at random hoping to spot drift —
run the scan first and let it tell you where to look.

```
python3 .claude/skills/repo-consistency/scripts/check.py
python3 .claude/skills/repo-consistency/scripts/check.py --only facts,names
python3 .claude/skills/repo-consistency/scripts/check.py --json
```

Findings come in three grades, and the grade tells you how far to trust it:

- `[!] error` — a comparison came out wrong. The evidence line is printed;
  glance at it, then fix it.
- `[?] verify` — the script resolved something and cannot judge it. Read the
  line and decide.
- `[ ] note` — context, not a fault. Where the reading cost is, which files
  carry no status, which mentions look historical.

`references/checks.md` explains what each check looks for and the specific ways
each one is wrong. Read it when a finding surprises you.

## Work on a branch, always

`CLAUDE.md` requires it, and this job in particular touches many files at once.
Branch first, make the changes, then show the diff. Merging is normal and
expected — ask for it, say what it publishes, and do not treat agreement as
standing permission for the next run.

Say plainly what a merge would put live. Most consistency fixes publish nothing
a visitor sees, and saying so is worth a sentence. A price or a fact that
reaches the JSON-LD is different and deserves calling out before it lands.

## What to fix without asking

Fix it when the correct value is not a matter of opinion:

- a price in prose that disagrees with `site/src/data/business.ts`
- a superseded name, domain or address used as a current fact
- a line count, file count or "N files" claim that no longer matches
- a reference to a file that does not exist, where the intended file is obvious
- a section pointer that resolves to the wrong heading
- the same sentence appearing in three files, where one can point at another

Bring back rather than decide:

- whether two documents should merge, split, or one be deleted
- anything where fixing the inconsistency means choosing which fact is true —
  if `business.ts` and a doc disagree about something that is not a price, the
  doc might be the one that is right
- deleting a document, ever
- anything touching a `[PLACEHOLDER]`, which marks a fact nobody knows yet and
  which must never be filled in by inference

## Never edit the record

Some files exist to say what happened: `ops/session-log.md`, the delivered
audits under `ops/audits/`, `ops/rename-to-wardith.md`. Old prices and the old
name are *correct* there. The script skips them; you should too. Editing them
does not fix an inconsistency, it destroys the reason a decision was made — and
that reasoning is the thing that stops a future session re-litigating a
settled question.

The same instinct applies inside live documents. A paragraph explaining why a
value is null, why a price moved, or why an approach was rejected is load-bearing
even when it is long. Condense it if it is flabby; do not delete the argument.

## Cutting the wording

The owner wants prose condensed, not merely deduplicated. The discipline is to
cut words while keeping every load-bearing fact. `references/editing.md` has the
method and worked examples from this repo — read it before rewriting any
passage.

The short version. A passage must keep:

- the decision, and the date it was made
- the constraint that would otherwise be re-litigated ("this stayed null because
  a stale `sameAs` is a false statement, not a broken link")
- any falsifiable condition still outstanding ("nobody has confirmed mail from
  this address passes DMARC")
- who decided it, where that matters

It can lose: restated context, the same point made twice with different
examples, hedging, throat-clearing before the actual claim, and narration of
what the reader is about to read.

Two cuts do most of the work, and both are counter-intuitive enough to state
here rather than leaving to the reference:

- **A comparison closes when the choice is made, not when the money moves.** An
  unticked box means the errand is open; it says nothing about the argument.
  Once a provider is picked, the case against the ones that lost goes — the
  runbook and the traps stay.
- **Narrative colour goes, however good it is.** A sentence about what a
  decision cost, who has to carry it, or how ironic it is changes nobody's next
  action. The test: if deleting it could let someone do the wrong thing later,
  it is a constraint and it stays. If it only makes them feel less, it goes.

Report the saving in words, not as a vague claim of tightening.

## Structural changes

Reach for these when the scan shows the same thing in several places:

- **One fact, one home.** Where a fact is restated across files, pick the file
  that owns it and make the others point there. `business.ts` already works this
  way and says so in its header — extend the pattern rather than inventing one.
- **Index what is long.** A document over ~400 lines that people enter halfway
  needs a contents list at the top. `ops/README.md` does this for the folder;
  long files need it for themselves.
- **Status in the header.** `ops/README.md` defines Live / Decided-unvalidated /
  Closed / Stub and asks each file to carry one. Files missing it are listed by
  the `status` check — adding it is cheap and stops the most dangerous misread,
  where a decision written down is taken for a thing that works.
- **Split by when it is used, not by topic.** That is already the organising
  idea of the ops folder; keep new structure consistent with it.

Do not reorganise for its own sake. Every move breaks references elsewhere —
re-run the scan afterwards and fix what you broke.

## Finish the job

1. Re-run the full scan. The count of errors should have gone down, and you
   should be able to say why any remaining one is staying.
2. If site files changed, build: `cd site && npm run build`.
3. Show the diff, grouped by what kind of problem each change fixes.
4. Add an entry to `ops/session-log.md` — newest first — recording what was
   changed and why. This job is exactly the kind whose reasoning gets lost.

## Reporting back

Lead with what changed, not with how hard it was.

```
Fixed (N):
  <class of problem> — <files> — <what was wrong, one line>

Brought back for you (N):
  <the choice, and what each option costs>

Not touched:
  <historical files, and anything deliberately left>

Words: <before> → <after>
```

Keep the list of unfixed items honest and short. If a finding is a false
positive from the scanner, say so and fix the scanner's config in
`scripts/config.json` rather than silently ignoring it — an unfixed false
positive gets rediscovered and re-investigated every single run.
