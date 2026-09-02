---
name: 90qrun
description: >-
  Run the complete 90-question AI-visibility prospecting research stage for a
  trade x geography, end to end, from just an industry and a place name.
  Generates the question set, runs the smoke test, executes the full 90-query
  batch across OpenAI/Gemini/Perplexity via the existing trade_run.py,
  retries any failures once automatically, and validates completeness before
  reporting. Runs straight through with no mid-run approval prompts - only a
  genuinely serious problem (missing keys, a provider failing outright,
  grounding not firing) stops it early; anything smaller is retried and
  folded into the final report. Stops after producing a validated raw CSV -
  market census, mention counting and prospect qualification are a separate,
  later stage. Invoke as `/90qrun <industry> - <geography>` or
  `/90qrun <industry> | <geography>`, e.g. `/90qrun estate agents - Liverpool`.
---

# 90Q run

## GitHub Actions remote adapter

When `WARDITH_REMOTE=true`, the workflow has already used
`scripts/wardith-secrets.sh`'s allowlisted implementation to load the approved
provider values. `BWS_ACCESS_TOKEN` is deliberately absent by this stage. Do
not call PowerShell, the Claude session hook, or Bitwarden again. Use `python3`
directly for provider commands, use `$WARDITH_RUNS_DIR` instead of assuming
`~/wardith-runs`, and treat `$WARDITH_DATA_REPO` as the only repository that
may be committed and pushed. Never modify or commit the core checkout.


*Trade x geography, AI-visibility research stage. Ninety queries, one CSV,
one verdict. Reference implementation: `estate-agents-chester`, 2026-08.*

This skill covers **stage one only** — discovery-question data collection.
It does not build a market census, does not count mentions, does not touch
Companies House, and does not propose prospects. That is a separate skill,
built on top of this one's output.

## What "done" means before you start

Read `tools/trade-run/README.md` in full once — this skill drives that
script, it doesn't replace it. The six env vars
(`OPENAI_API_KEY`/`MODEL`, `GEMINI_API_KEY`/`MODEL`, `PERPLEXITY_API_KEY`/`MODEL`)
and the resume/retry behaviour described there are load-bearing for
everything below.

## Step 1 — Parse the invocation

Input is `<industry> - <geography>` or `<industry> | <geography>` (split on
` - ` or ` | ` specifically, not a bare hyphen, so a hyphenated place name
like `Stoke-on-Trent` still parses as one token).

Build a slug: lowercase, non-alphanumeric runs collapsed to a single hyphen,
e.g. `estate agents` + `Liverpool` -> `estate-agents-liverpool`. This slug is
used everywhere below (`--client`, filenames, `audit_id` prefix).

If either half is missing or empty, stop and ask for the missing piece —
this is the one input this skill genuinely cannot infer.

## Step 2 — Preflight (stop clearly, don't proceed, on any failure here)

1. Confirm `tools/trade-run/trade_run.py` exists in the current repo.
2. Confirm all six env vars are set and non-empty. If any are missing, stop
   and quote the exact fix from `tools/trade-run/README.md` ("Setting up the
   keys") — do not guess a model name or proceed with a partial set.

   **Check `$CLAUDE_CODE_REMOTE` first — it decides which shell and which
   keys file the rest of this skill uses.**

   - **Cloud session (`CLAUDE_CODE_REMOTE=true`):** there is no PowerShell in
     this VM. A repo-committed `SessionStart` hook already ran before this
     skill started and, if it succeeded, has written `~/.noven/env` (bash
     format) from the Bitwarden vault. **Load it by running
     `source ~/.noven/env` inside an actual Bash tool call.** If the file
     doesn't exist or the vars still come back empty after sourcing it, that
     hook failed or the Bitwarden bootstrap token isn't configured on this
     environment — stop and say so plainly rather than guessing; this is a
     preflight failure, not something to work around.
   - **Local session (Windows):** run provider commands through
     `scripts/wardith-secrets.ps1 run`. Check it first with
     `pwsh -File scripts/wardith-secrets.ps1 status`; it retrieves the exact
     approved secrets from Bitwarden for the child process and keeps no
     plaintext key file.
   - **Local session (macOS/Linux):** `source ~/.noven/env` inside a Bash
     tool call, same as the cloud case above.

   **Shell state does not carry over between separate tool invocations,
   either, in any of the three cases.** Sourcing the file in one call and
   running `trade_run.py` in a later, separate call means the script runs
   against an empty environment. Every command in Step 4 and Step 5 must
   re-source the file in the *same* call as the script invocation — see
   those steps.
3. **Sync `~/wardith-runs/` against the private `hellonovenuk-lang/wardith-crm-data`
   repo** before the prior-run cross-check below reads it — see
   `scripts/wardith-runs-sync.sh`'s header for the full mechanism. Cloud
   session: attach the repo with `add_repo` (`access: "push"`, needed at the
   end of Step 7) and run the clone command it returns, then
   `bash scripts/wardith-runs-sync.sh pull`. Local session: just
   `bash scripts/wardith-runs-sync.sh pull` (self-clones on first use).
   Entirely optional and never blocks — if the repo doesn't exist yet or
   `add_repo` fails, note it once and continue with whatever's already on
   disk, same posture as a missing `COMPANIES_HOUSE_API_KEY` elsewhere in
   this pipeline.
4. **Confirm the loaded models are the intended prospecting models, not
   stale or leftover values — before Step 4 spends anything.** Two named
   failure modes, both observed on a real run, plus a general check:
   - **`PERPLEXITY_MODEL` must be a bare model name (`sonar`), never a
     provider-prefixed one (`perplexity/sonar`).** If it has a `perplexity/`
     prefix, **stop and say so** before Step 4 — the prefixed form is a
     leftover from the old Agent API convention this script no longer
     calls — see the comment on `call_perplexity()` in `trade_run.py`
     (`openai/gpt-5.6-sol`-style names belong to that retired path, not the
     current `/v1/sonar` endpoint it actually uses). The smoke test would
     catch this too if missed here, but catching it now costs nothing
     instead of one wasted smoke attempt.
   - **`OPENAI_MODEL` should currently be `gpt-5.6-luna`** — the cheaper
     model designated for prospecting, deliberately different from whatever
     frontier/audit-default model `env.ps1` may otherwise hold for client
     audit work. Update this line if that designation ever changes; don't
     let it drift silently.
   - **Cross-check all three against the most recently modified prior run.**
     Find the newest `~/wardith-runs/*.csv` (excluding the file this run is
     about to create) and read its per-provider `model_version` values. If
     any of `OPENAI_MODEL`/`GEMINI_MODEL`/`PERPLEXITY_MODEL` differs from
     what that prior run actually recorded, **stop and print both values**
     before proceeding — this may be an intentional upgrade, but it must be
     a deliberate one, confirmed by the owner, not a stale env.ps1 default
     nobody re-checked. This is exactly the gap that let 19 of 90 queries
     run on a stale `OPENAI_MODEL` before anyone noticed, purely by chance.
5. Print one reminder line that provider spend caps
   (`playbook/records-and-data.md`, "Spend caps") should already be
   confirmed set on each provider dashboard. This is not something you can
   check programmatically — say it once, then move on. Do not block on it.
6. Check the current git branch. If it's the default branch, create and
   switch to a new branch for this run (e.g. `trade-run/<slug>`) before
   writing the question file in Step 3 — this repo's convention
   (`CLAUDE.md`, "Always work on a branch") applies to the question file
   even though the run output itself never enters the repo. Commit that one
   file to the new branch once it's written (short message, e.g. "Add
   question set for `<slug>` trade run") — it's generic, non-sensitive
   content, so committing it is in scope for a hands-off run. **Never push,
   open a PR, or merge** — that stays the user's explicit, separate call,
   same as any other branch in this repo.

None of this step should ask the user anything unless it fails.

## Step 3 — Generate the question set

Write `tools/trade-run/questions-<slug>.csv` with the exact columns
`audit_id,question_id,category,question_text,frozen_from` (leave
`frozen_from` blank — that column is only for a question set frozen from a
paying client's monthly plan, not a prospecting run).

**Exactly six questions.** Category values are the schema enum from
`playbook/models-and-schemas.md`'s `questions.csv` table:
`discovery`, `qualified-discovery`, `buying-intent`, `comparison` (a fifth
value, `named-business`, exists in the schema but has no place in a
trade run, which by definition asks about the trade generically, never by
business name). Any mix across those four categories that sums to six is
fine — the two existing reference sets split it differently
(`discovery` x2 / `qualified-discovery` x2 / `buying-intent` x1 /
`comparison` x1 for Chester estate agents; `discovery` x3 /
`qualified-discovery` x1 / `buying-intent` x1 / `comparison` x1 for Wirral
dentists) — there is no single required split, only the four categories and
the total of six.

Write fresh, trade-appropriate phrasing — do not reuse another trade's
wording with the nouns swapped. Two rules matter more than exact phrasing:

- **Every question names the geography explicitly**, because Gemini's
  grounding tool has no locale parameter at this API tier — a named place is
  what keeps its answers comparable with the other two providers.
- **Phrase each question the way a real customer looking for this trade in
  this place would actually ask it** — not corporate, not a keyword
  fragment. Read `tools/trade-run/questions-estate-agents-chester.csv` and
  `tools/trade-run/questions-wirral-dentists.csv` as the two worked examples
  of what this looks like for a services trade vs. a healthcare trade.

Set `audit_id` to `<slug>-<today's date, YYYY-MM-DD>`.

Show the six generated questions in your own output before moving on —
not as an approval gate, just so the record of what was asked is visible
without having to open the file.

## Step 4 — Smoke test (automatic, not a manual checkpoint)

Run inside a single tool call of whichever shell Step 2 identified — the
env-var sourcing and the script invocation are in the *same* call, per Step
2 item 2, never split across two.

Cloud session (Bash tool call):

```bash
source ~/.noven/env
python3 trade_run.py --questions questions-<slug>.csv --client <slug> \
    --location <geography> --out ~/wardith-runs/<slug>.csv --smoke
```

Local Windows session, from the repository root:

```powershell
pwsh -File scripts/wardith-secrets.ps1 run py tools/trade-run/trade_run.py `
    --questions tools/trade-run/questions-<slug>.csv --client <slug> `
    --location <geography> --out ~/wardith-runs/<slug>.csv --smoke
```

This produces three rows, one per provider, tagged `smoke — delete this
row` in `notes`. Check all three automatically against the five checks
`tools/trade-run/README.md` lists for a human to run by eye — do the ones
that are actually checkable in code, and treat the rest as a soft signal:

**Stop here — genuinely serious, spending the full ~$5 would be wasted:**
- Any provider's smoke row carries an `errors` value (that provider is
  unreachable or rejecting the call outright).
- Any provider's smoke row has an empty `sources_cited` (the search/grounding
  tool didn't fire — you would be measuring the model's memory, not what a
  customer is actually told, for the entire run).
- Any provider's smoke row has no `model_version` recorded despite no
  error (can't satisfy the "record the exact model version string on every
  run" rule in `playbook/models-and-schemas.md`).

If any of these fire, stop, report exactly which provider and which check
failed, and suggest the likely cause (auth, endpoint/API change, provider
outage) — do not proceed to the full run.

**Soft signal only — log it for the final report, do not stop for it:**
- The geography name doesn't appear anywhere in a smoke answer's text. This
  can be a genuine false positive (a model paraphrasing "the area" instead
  of repeating the place name), so it's a note, not a gate.

If smoke passes the blocking checks, delete **every** row tagged smoke from
the output CSV (filter out rows whose `notes` contains "smoke") — not
literally three. A provider that errors on its first attempt and succeeds
on a retry leaves both rows behind, since `trade_run.py` never overwrites a
failed row, only appends its replacement; count what's actually tagged, not
what's expected. Continue immediately once cleared — no prompt, no pause.

## Step 5 — Full run (automatic, this is the real spend)

Same rule as Step 4 — use the environment-specific loader in the same call:

Cloud session (Bash tool call):

```bash
source ~/.noven/env
python3 trade_run.py --questions questions-<slug>.csv --client <slug> \
    --location <geography> --out ~/wardith-runs/<slug>.csv --cap 90
```

Local Windows session, from the repository root:

```powershell
pwsh -File scripts/wardith-secrets.ps1 run py tools/trade-run/trade_run.py `
    --questions tools/trade-run/questions-<slug>.csv --client <slug> `
    --location <geography> --out ~/wardith-runs/<slug>.csv --cap 90
```

`--location` is the plain-English place name from the invocation (e.g.
`Liverpool`, not the slug) — it's what makes Perplexity's own search step
geography-aware; see the comment on `call_perplexity()` in `trade_run.py`
for why this exists and what it does and doesn't cover across the three
providers.

Six questions x three providers x five runs = 90 queries, roughly $5 across the
three providers combined (per `playbook/outreach-process.md`). This runs to
completion (or until it errors row-by-row and keeps going — the script logs
each error and continues, per its own design) with no approval checkpoint.
A single failed row here is expected operating behaviour, not a reason to
interrupt the user — that's what Step 6 is for.

## Step 6 — Validate, retry once if needed, validate again

Run the bundled validator:

```
python3 .claude/skills/90qrun/scripts/validate_run.py \
    --csv ~/wardith-runs/<slug>.csv --questions questions-<slug>.csv
```

It checks: total row count against the planned 90, per-provider and
per-question and per-run_no distribution, duplicate successful identities,
smoke-row leakage, model-version consistency per provider, and — the one
that matters most here — **whether every planned identity has a successful
row**, not just a physical row. An unretried errored row makes it exit 1
even though the row count looks right, because that's exactly the gap an
automatic retry closes for free.

**If it exits 1 because of errored rows only** (not a structural problem —
see below): re-run the *exact same Step 5 command* once. `trade_run.py`'s
own resume logic skips every row that already succeeded and retries only
the ones that errored, so this costs at most a few pennies, not another
$5. Then run the validator again.

**Retry exactly once.** Do not loop. If the second validation still exits 1,
stop and report the exact remaining gap (provider, question, run number,
error text) rather than retrying again or silently shipping a short dataset.

**If it exits 1 for a structural reason** (wrong provider/question/run_no
counts, duplicate successful identities, more than one `model_version` per
provider) — that's a bug in the run or the question file, not something a
retry fixes. Stop and report it plainly; don't attempt to patch the CSV by
hand.

## Step 7 — Write the run log and report

Write `~/wardith-runs/<slug>-run-log.md`: the six questions used, the
provider/model versions recorded, the validator's final output verbatim,
and the retry outcome if one happened. This is exactly the "raw trade-run
CSV and its provider/run statistics" input that
`tools/prospect-compiler/CAMPAIGN-HANDOFF.md` §2 expects to already have in
hand when the next stage (market census, mention counting, qualification)
starts — write it now, once, while everything is fresh, rather than
reconstructing it later.

**Where Step 2 synced against `wardith-crm-data`**: run
`bash scripts/wardith-runs-sync.sh push "90qrun <slug>"` now, so the raw CSV
and run log this run just produced are there for a `/qualify` run in a
*different* session or on the laptop to pick up — in a cloud session this
is what stops them being lost when the VM is reclaimed. Non-blocking, same
as everything else in this pipeline: note a push failure in the report
below, never treat it as a reason to change the verdict. Skip silently if
Step 2 never found or synced the repo.

Then report to the user — **this is the only checkpoint they see**:

- **Verdict**, stated plainly: `PASS` (90/90 clean first time) /
  `PASS WITH RETRY` (some rows failed, retry fixed them, final state is
  clean) / `INCOMPLETE` (still short after one retry — say exactly which
  rows and why).
- Row counts and the provider split.
- Model version strings actually recorded (not the env var names).
- Any soft (non-blocking) flags from Step 4 or Step 6.
- File paths: the question file (committed on its own local branch — name
  the branch, and say plainly that it hasn't been pushed or opened as a PR),
  the run CSV, the run log — the latter two under `~/wardith-runs/`, never
  inside the repo.
- Whether the run CSV/log were also synced to `wardith-crm-data`: pushed
  OK, or the repo wasn't set up — never affects the verdict above.
- One line stating plainly that this is stage one only, and prospect
  qualification is separate, later work.

Do not go further than this. Do not build a market census, do not count
mentions, do not touch Companies House, do not draft a campaign JSON, do
not run the Prospect Compiler. Those are a different skill's job.
