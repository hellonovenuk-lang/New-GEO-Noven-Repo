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
2. **Funded balances on all three. Read the next section — one of them is
   short.**
3. **Python 3.9 or later.** Stdlib only, nothing to install.
   `[PLACEHOLDER: whether Python is installed on the owner's Windows machine]`.

---

## Will the balances cover it? Two yes, one short

**Balances as at 2026-08-09**, from the owner: **OpenAI $16.00, Gemini £8.95,
Perplexity $4.49.**

**One run is 30 queries per provider**, not 90 each — six questions, five runs.

**There is exactly one measured rate in this business** and it is OpenAI's:
**$12.63 for roughly 75 queries on the 2 August self-audit, so about $0.17 a
query** with web search enabled. The Gemini and Perplexity totals from that day
were never recorded, so the only honest thing to do is price all three at the
one rate we have and say plainly that two of the three figures are borrowed.

| Provider | Balance | 30 queries at $0.17 | Verdict |
|---|---|---|---|
| OpenAI | $16.00 | ~$5.05 | **Fine**, roughly three runs' worth of headroom. And this is the one rate that is real |
| Gemini | £8.95 | ~$5.05 equivalent | **Fine.** Grounded search is charged per request and is normally cheaper than this, so the real figure should be well under |
| Perplexity | $4.49 | ~$5.05 | **Short by about fifty cents** at the borrowed rate. Sonar is genuinely cheaper than OpenAI web search, so it may well cover it — but "may well" is not a balance check |

**So the answer is: probably yes, and Perplexity is the one that might not
finish.** Do not resolve that by guessing at Perplexity's price list.

### The smoke test is the measurement, and that is what it is for

Three queries, one per provider, costs pennies. **Then read all three dashboards
and divide.** That converts every number above from a borrowed estimate into
three measured per-query rates, which is a fact this business has needed since
2 August and has never had. It also feeds the £150 Maintain question that
`ops/plan-to-1-september.md` leaves open, and it costs about fifty cents to
answer.

Record the three rates in `ops/accounts.md` the same day.

### If Perplexity does run dry, nothing is lost

**The providers run in order: OpenAI, then Gemini, then Perplexity.** So an
exhausted Perplexity balance fails last, with sixty rows already written and
flushed to disk. Re-running the same command after a top-up **retries only the
failed rows** — a row carrying an error is not counted as done. The cost of
getting this wrong is a five-dollar top-up and one repeated command.

### One thing to confirm before firing, and it is not about having enough

**Check Perplexity's auto top-up is off.** `ops/audit-setup.md` §4 says to set
it off and it has never been confirmed. With auto top-up on, "is the balance
enough" stops mattering — running dry silently charges the card, which during a
spending freeze is the exact event the freeze exists to prevent. The same
section's £10 caps on all three have also never been confirmed as set.

**Smoke test first. Always.** Three queries, one per provider, on q01:

```
python3 trade_run.py --questions questions-wirral-dentists.csv \
    --client wirral-dentists --out ~/wardith-runs/wirral-dentists.csv --smoke
```

Then check the five things in `ops/audit-setup.md` §8 on those three rows. **The
first one is the one that silently invalidates a whole run:** if there are no
citations and the answer reads generic, the search tool did not fire and you are
measuring the model's memory rather than what a customer would be told.

Delete the smoke rows before the real run; they are tagged in the `notes` column.

### Why the UK-locale problem mostly does not apply to a trade run

`ops/audit-setup.md` §8a records that **Gemini's grounding tool has no
location parameter at this access tier and cannot be fixed** — it is not a setup
mistake, and the fix does not exist outside Google's enterprise product. The
practical consequence recorded there is that Gemini skews non-UK **specifically
on questions carrying no geographic word of their own.**

**Every question in `questions-wirral-dentists.csv` names a place** — Wirral,
Birkenhead or Wallasey. That is not luck and it should not be lost when the file
is copied for another trade:

> **Design rule for trade question sets: every question names the area.** It is
> what a real customer would type anyway, and it is the only thing that keeps
> Gemini's answers comparable with the other two.

Check 3 still gets checked. A question naming the Wirral that comes back with
American practices and US spellings is still a wasted run, and it is cheaper to
find that out on three queries than on ninety.

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
