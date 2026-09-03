# The trade run

Asks the three assistants (ChatGPT, Gemini, Perplexity) one sector-and-area
question set, five times each, and logs every answer with the sources it
cited. That produces the mention counts a market run is built from —
`playbook/outreach-process.md`.

**What it is not.** Not a client audit — a trade run asks about a sector and
an area, nobody has paid for it, and it produces a market census rather than
a report. And not "the runner" the audit process defers to for per-client
work; that's a separate, undecided piece of work.

## The files

| File | What it is |
|---|---|
| `trade_run.py` | The runner. Reads a questions CSV, calls the three provider APIs, writes a runs CSV |
| `questions-wirral-dentists.csv` | Example question file for one trade and area |
| `.gitignore` | Stops a run's output being committed — the second guard, not the first |

**To run a different sector × market, copy the CSV and change the words.**
Keep six questions across the same categories (see "Question-file
expectations" below) — a set of six discovery questions counts one thing six
times.

## Requirements

- **Python 3.9 or later, stdlib only.** Nothing to `pip install`.
- **Six environment variables**, loaded before running:
  `OPENAI_API_KEY`, `OPENAI_MODEL`, `GEMINI_API_KEY`, `GEMINI_MODEL`,
  `PERPLEXITY_API_KEY`, `PERPLEXITY_MODEL`. Current model strings:
  `playbook/models-and-schemas.md`. **Never guess a model name** — check the
  provider's own console.
- **Funded, capped balances on all three providers.** Check dashboards before
  a full run; a smoke test (below) tells you the real per-query cost.

## Setting up the keys

Bitwarden Secrets Manager is the source of truth. On Windows, configure its
read-only machine account once and run commands through the repository wrapper:

```powershell
pwsh -File scripts/wardith-secrets.ps1 setup <bitwarden-project-id>
pwsh -File scripts/wardith-secrets.ps1 run py tools/trade-run/trade_run.py ...
```

The wrapper decrypts only the Bitwarden machine token with Windows DPAPI,
fetches an explicit allowlist, injects the provider values into the child
process, and removes temporary Zoho credentials when that process exits.
Secrets are never committed or stored as permanent plaintext files.

Cloud sessions continue to use `scripts/cloud-session-secrets.sh`; local
macOS/Linux sessions use `source ~/.noven/env` until they gain an equivalent
native wrapper.

**Three rules, no exceptions:** the file lives outside every repo; it's loaded
deliberately, never from a profile script; no key string ever appears in a
file inside this repo or is pasted into a chat or cloud session. Bitwarden
Secrets Manager remains the canonical copy (`playbook/accounts-and-dates.md`).

## Question-file expectations

A CSV with columns `audit_id, question_id, category, question_text,
frozen_from`. Six questions per sector, covering discovery, qualified
discovery, buying intent and comparison — see
`questions-wirral-dentists.csv` for the shape.

**Every question must name the area** (town or region). It's what a real
customer would type anyway, and Gemini's grounding tool has no locale
parameter at this API tier — a named place in the question is what keeps its
answers comparable with the other two.

## Smoke test — always run this first

One query per provider, on the first question:

```
python3 trade_run.py --questions questions-{trade}-{area}.csv \
    --client {trade}-{area} --location {area} \
    --out ~/wardith-runs/{trade}-{area}.csv --smoke
```

**`--location` is the plain-English place name** (e.g. `Chester`, not
`chester-cheshire`) — it's passed to Perplexity's `user_location.city` to
narrow its own search step, the same job the area name in each question
text already does for a human reader. Keep it consistent with the place
name used in the questions file.

**Check the three smoke rows before trusting a full run:**

1. **Citations are present and specific.** A generic answer with no citations
   means the search tool didn't fire — you'd be measuring the model's memory,
   not what a customer is actually told.
2. **Model version strings match** what the provider's console currently
   reports. A silently substituted or retired model fails this check, not
   loudly.
3. **Answers are UK-shaped** — no US spellings, no non-UK businesses. If they
   aren't, the area name in the question isn't doing its job.
4. **The CSV survives intact** — multi-line answer text isn't truncated or
   corrupted.
5. **No errors, no empty answers**, on any row.

**Delete the smoke rows before the full run.** The script skips any row
already succeeded (keyed on assistant + question + run number), so leftover
smoke rows would silently stand in for real data in the full run's counts.

## Full run

```
python3 trade_run.py --questions questions-{trade}-{area}.csv \
    --client {trade}-{area} --location {area} \
    --out ~/wardith-runs/{trade}-{area}.csv --cap 90
```

Six questions × three assistants × five runs = 90 queries. In PowerShell it's
the same command with `py` instead of `python3` and a backtick line
continuation instead of a backslash.

## Output

**`--out` must point outside this repository.** Answer text names real
businesses and sometimes real people, and this repo is written as though
public — the `.gitignore` here is a backstop for the day somebody forgets,
not the rule itself.

**Query cap.** `--cap` (default 100) is a hard ceiling checked before the
first call — if the planned query count exceeds it, the script exits having
spent nothing.

**Bounded retries.** Each provider query retries HTTP 429/503 at most twice,
after 15 and 45 seconds. The cap counts planned queries, not HTTP attempts:
`--smoke --cap 3` makes three queries and at most nine attempts. Authentication
errors, other HTTP errors, timeouts and malformed responses are not retried.
Retries can add provider costs. No model is substituted.

**Safe diagnostics.** Error logs and CSV error cells contain only locally
constructed status/type information, never request URLs, headers or raw
provider error bodies. Gemini's key is sent in a header, not its URL.

**Smoke exit status.** A smoke test exits unsuccessfully if any provider
errors, returns an empty answer, or returns no sources. Other provider results
are retained. The cloud entry point is `scripts/provider_smoke.py`; it requires
a new output directory so test rows never become campaign data.

**Resume and errors.** Every row is flushed to disk as it lands. A re-run
skips rows that already succeeded and retries only rows that errored, so a
rate limit or outage partway through costs nothing but the re-run.

**What it will not give you.** The `outcome` and `competitors` columns are
written empty and stay empty — classifying who was named is human judgement,
not something the script does. `playbook/models-and-schemas.md` has the full
`runs.csv` schema and the classification bands.
