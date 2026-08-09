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

## Setting up the machine — Windows

*Written 2026-08-09, when the owner's Claude Code terminal reported that it had
neither git nor the API keys.*

**Those two symptoms usually have one cause.** Claude Code on Windows runs its
shell through **Git Bash**, which arrives with Git for Windows. With Git missing,
`git` fails *and* the shell you get is not the one the instructions assume — so
environment variables set in a PowerShell window are invisible to it.

### First, find out what is actually missing

Run these three, and read the failures rather than guessing:

```powershell
git --version
py --version
Test-Path "$HOME\.noven\env.ps1"
```

- **`git` fails** → install **Git for Windows** from `git-scm.com`, take the
  defaults, then **close and reopen the terminal**. `PATH` is only read at
  startup, so a terminal open during the install will keep saying git is missing
  and it is not lying, it is stale.
- **`py` fails** → install Python from **`python.org`**, and tick **"Add
  python.exe to PATH"** on the first screen of the installer. **Not the Microsoft
  Store build** — it sandboxes file access in ways that break scripts writing
  outside the user profile. This closes the open question in "Running it" above.
- **`Test-Path` returns `False`** → the keys file does not exist on this machine;
  see below.

### The keys are probably already there

**`$HOME\.noven\env.ps1` is the existing convention** — `ops/name-check/README.md`
loads the same three keys from it, so if the name check was ever run on this
machine, the file exists and holds the keys. Load it into the current terminal
with a dot and a space:

```powershell
. "$HOME\.noven\env.ps1"
```

**The path keeps the old name on purpose.** It is a private file on one machine,
nothing published reads it, and renaming it silently breaks
`ops/name-check/README.md`. Same reasoning as `hello.noven.uk@gmail.com` in
`ops/rename-to-wardith.md` F10: an identity that carries the old name is left
alone.

### If the file does not exist, create it once

```powershell
mkdir "$HOME\.noven" -Force
notepad "$HOME\.noven\env.ps1"
```

Paste this, with the real values, and save:

```powershell
$env:OPENAI_API_KEY     = "sk-..."
$env:GEMINI_API_KEY     = "..."
$env:PERPLEXITY_API_KEY = "pplx-..."
$env:OPENAI_MODEL       = "gpt-5.5"
$env:GEMINI_MODEL       = "gemini-3.6-flash"
$env:PERPLEXITY_MODEL   = "sonar"
```

The three model strings are what the 2 August run actually used
(`ops/competitor-analysis.md` Part 2). **Confirm each is still current in its own
console** — a retired identifier fails loudly, which is fine, but a silently
substituted one is not.

**The keys also go in Bitwarden**, per `ops/audit-setup.md` §2 step 1. The file
is the working copy; the vault is the copy of last resort.

**Three rules about this file, all from `ops/audit-setup.md` §2:**

- **It lives outside every git repository.** `$HOME\.noven\` is not inside the
  repo and must stay that way.
- **It is loaded deliberately, never from a profile script.** A key that is only
  in the environment when you meant it to be cannot leak into an unrelated
  process.
- **No key string ever appears in a file inside this repo**, and none is ever
  pasted into a cloud session — including a Claude Code session running on the
  web, which is a different machine from this one.

### Then

```powershell
git fetch origin
git checkout claude/initial-client-outreach-uvo1ow
cd ops\trade-run
mkdir "$HOME\wardith-runs" -Force
. "$HOME\.noven\env.ps1"
```

and run the smoke test below.

---

## Running it

**Three things have to be true first, and two of them are not.**

1. **API keys in the environment**, per `ops/audit-setup.md` §2, and on Windows
   see "Setting up the machine" below — the keys most likely already exist at
   `$HOME\.noven\env.ps1` from the name-check run. **Do not guess a model name.**
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
