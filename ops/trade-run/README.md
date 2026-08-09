# The trade run

**Status: built and smoke-tested against its own guards, never run for real.**
No API call has been made from this folder — the balances and the questions are
checked below before that changes.

**What it does.** Asks the three assistants one trade-and-area question set,
five times each, and logs every answer with the sources it cited. That produces
the mention table and the visibility ladder in `ops/outreach.md` §4, which is
what the cold outreach email is built from.

**What it is not.** Not a client audit — a trade run asks about a trade and an
area, nobody has paid for it, and it produces a prospect list rather than a
report. And not "the runner" that `ops/audit-method.md` §7 defers; that decision
is untouched.

---

## The files

| File | What it is |
|---|---|
| `trade_run.py` | A copy of `ops/audits/noven-2026-08-02/audit_query.py`, which was written as a throwaway for the self-audit and turned out to be reusable. Three changes: the client name is a flag, the run count is a flag, and the defaults suit a trade run. **The original is frozen as part of that audit's record — change this one, never that one** |
| `questions-wirral-dentists.csv` | Six questions: three discovery, one qualified discovery, one buying intent, one comparison. Built on the frame in `ops/audit-questions.md` §1 |
| `.gitignore` | Stops a run being committed. The second guard, not the first |

**To do another trade, copy the CSV and change the words.** Dental, cosmetic,
physiotherapy and veterinary are the four in scope (`ops/outreach.md` §1). Keep
the six categories — a set of six discovery questions counts one thing six times.

---

## Running it

**Three things have to be true first, and two of them are not.**

1. **API keys in the environment**, per `ops/audit-setup.md` §2. `~/.noven/env`
   holds the keys; the three model variables are set from what that section
   recorded. **Do not guess a model name.**
2. **Funded balances on all three.** `[PLACEHOLDER: the balance on each of the
   three accounts after the 2 August self-audit is not recorded anywhere]`. The
   self-audit cost **$12.63 on OpenAI alone for roughly 75 queries**, so this
   run — 90 queries — is on the order of $15 across the three. **That is a spend
   inside the freeze window and it is the owner's call**
   (`ops/plan-to-1-september.md`).
3. **Python 3.9 or later.** Stdlib only, nothing to install.
   `[PLACEHOLDER: whether Python is installed on the owner's Windows machine]`.

**Smoke test first. Always.** Three queries, one per provider, on q01:

```
python3 trade_run.py --questions questions-wirral-dentists.csv \
    --client wirral-dentists --out ~/wardith-runs/wirral-dentists.csv --smoke
```

Then check the five things in `ops/audit-setup.md` §8 on those three rows —
the one that matters most here is **"does the answer look UK-shaped"**, because
Gemini's grounding tool has no documented UK-locale parameter and a US answer to
"best dentist on the Wirral" is a wasted run. Delete the smoke rows before the
real run; they are tagged in the `notes` column.

**Then the real run — 6 questions × 3 assistants × 5 runs = 90 queries:**

```
python3 trade_run.py --questions questions-wirral-dentists.csv \
    --client wirral-dentists --out ~/wardith-runs/wirral-dentists.csv --cap 90
```

**In PowerShell** it is the same command with `py` instead of `python3` and a
backtick where the backslash is.

**`--out` goes outside this repository.** Answer text names real businesses and
sometimes real people, and this repo is written as though it were public
(`ops/audit-method.md` §5). The `.gitignore` here is a backstop for the day
somebody forgets, not the rule.

---

## What it will and will not give you

**It will give you** one CSV row per answer, with the answer text verbatim, the
model version, and every source URL the assistant cited — except Gemini's, whose
URLs are all opaque `vertexaisearch` redirects and cannot be resolved
(`ops/competitor-analysis.md` Finding E). Source analysis is ChatGPT and
Perplexity only, and every conclusion drawn from it has to say so.

**It will not give you the mention table.** The `outcome` and `competitors`
columns are written empty and stay empty — that classification is human
judgement and it is the step the self-audit budgeted at 60 to 110 minutes
(`ops/audit-method.md` §7). For a trade run the counting is easier than it was
for the audit, because **the Companies House list is the candidate name list**:
you are checking which of a known set of practices got named, not discovering
who exists. `ops/outreach.md` §4 has the method.

**Two safety properties worth knowing before you trust it with a card.**

- **A hard cap on queries per invocation**, checked before the first call. Pass
  `--cap 90`; if the plan exceeds it the script exits having spent nothing.
- **It resumes.** Every row is flushed to disk as it lands, and a re-run skips
  what already succeeded and retries only what errored. A provider rate-limiting
  halfway through costs nothing but the re-run.
