# Audit — Noven (self-audit), 2 – 3 August 2026

**The first live run of the audit method, on ourselves.** Kept because it is the
**dated baseline**: the same ten questions, put to the same models by the same
script, can be re-run later and compared directly. That comparison is the whole
reason this folder exists — a one-off snapshot would not have been worth keeping.

`audit_id` — `noven-2026-08-02` · Questions frozen from 2026-08-02.

## What's here

| File | What it is |
|---|---|
| `report.md` | The client-facing report. Markdown master |
| `Noven-audit-report-2026-08-03.docx` | The same report as a Word document — the editable master per `CLAUDE.md`'s Documents rule. **Export the PDF from Word**, not from a converter |
| `checklist.md` | The filled internal working note. Never sent to a client |
| `questions.csv` | The eleven questions, frozen. `x01` has a blank `frozen_from` so it sits outside the frozen set by construction |
| `audit_query.py` | The script that made the API runs, exactly as it ran |
| `build-report.js` | Builds the `.docx` from `docx` (npm). `npm install docx`, then `node build-report.js` |
| `logo.png` | Build input for the above. Rasterised from `site/public/logo.svg`, not redrawn — regenerate with `python -c "import cairosvg; cairosvg.svg2png(url='../../../site/public/logo.svg', write_to='logo.png', output_width=1600)"` |

**On keeping `audit_query.py`.** `ops/audit-setup.md` §7 calls it a throwaway and
says to delete it after the audit. It is archived here anyway, unmodified, and
the two rules do not actually conflict: §7 means *do not maintain this as
software*, and that still stands — nothing should import it or build on it. But
a baseline you cannot re-run is not a baseline, and the exact script is what
makes the comparison honest. It is frozen with the audit, not living in the
codebase. Note it carries no keys: all six values come from the environment.

## What is missing, and it matters

**`runs-clean.csv` — the 210 rows of answer data — is not in this folder.** It
existed only as a file on the owner's machine during the run. Every figure in
`report.md` traces to it, and without it none of them can be re-checked.

`ops/audit-report-template.md` requires, before a report is sent, that *"every
figure in the report traces to a row in `runs.csv`"*. **That check was never
completed for this audit.** The numbers are as recorded during the session and
are believed correct; they are not verified against the data.

**For every future audit the data file goes in the audit folder first, before
the report is written.** It is the only thing that can defend a number in six
months, and it is the one part of the method this run got wrong.

## Scope: what was and wasn't checked

- **Done:** 210 API runs across ChatGPT, Gemini and Perplexity; 18 hand runs
  across Copilot and Google; on-site checklist groups 1, 2 and 4; the Bing and
  Google index checks.
- **Not done:** checklist group 3's off-site half — Google Business Profile,
  Bing Places, Companies House, directories, LinkedIn, review counts. The report
  discloses this. On most audits group 3 produces the largest number of fixable
  findings, so a client audit should not repeat this omission.
- **The 18 hand answers are not in the run data.** They were recorded in a
  markdown file, not as `runs.csv` rows with `surface=app`, so the report's "not
  named in any of the 18 answers" does not trace to a row either.

## The findings, in one line each

1. **The name belongs to somebody else, at least four times over** — Noven
   Pharmaceuticals (Miami), Noven Build (North West), `noven.studio` (an AI
   product), `noven.io`.
2. **Copilot has no record of the site at all** — `site:novenstudio.co.uk`
   returns nothing on Bing, which is what Copilot retrieves from. Left unfixed
   on purpose so the baseline records the real state.
3. **Nothing tells a machine where the business works** — the pages say "the
   Wirral"; the machine-readable data says only `GB`.

**Verdict: C — the Foundation would be wasted until something else is fixed.**

## Two faults this audit found in the method itself

Both are recorded here rather than silently patched, because the reasoning is
the useful part.

1. **Verdict C is written too narrowly.** `checklist.md` and
   `ops/audit-report-template.md` both describe C in terms of broken *sites* —
   "no website, a Facebook page standing in for one, a site that cannot accept
   structured data". Noven's site is the opposite of all of those and the
   verdict is still C, because the *identity* is the blocker. C should cover
   identity problems, not only site problems. **Not yet amended.**
2. **`ops/audit-setup.md` §6 is wrong about cost.** It estimates ~£1.20 per 150
   queries. OpenAI alone came to **$12.63** for roughly 75. The Gemini and
   Perplexity totals were not recorded, so §6 has been left alone rather than
   half-corrected. This matters commercially: `ops/service-tiers.md` prices
   Maintain at £95/month for ten questions at five runs a month, and that price
   was set against the wrong estimate. **Needs the two missing totals, then
   fixing.**
