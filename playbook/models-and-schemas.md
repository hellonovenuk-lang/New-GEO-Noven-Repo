# Models, versions, and data schemas

*Reference for audit setup and client data storage.*

---

## Which model per provider

**Use each provider's current default consumer-facing tier, required by the audit methodology — never a cheaper model chosen to lower audit cost.** Representativeness is the point, not cost. Record the actual provider cost of every run where the provider reports it (`playbook/audit-process.md`, "What it costs us to run") rather than quoting a fixed figure — costs move with usage and provider pricing, and a stale number is worse than none.

**Record the exact model version string on every single run.** When a provider ships a new model, numbers move for reasons unrelated to the client. A month-on-month comparison across a model change is not a comparison, and the record must flag it rather than report progress or decline.

| Provider | Check via | Where to find current model |
|---|---|---|
| OpenAI (ChatGPT) | API docs at `platform.openai.com` | Models → select default |
| Google (Gemini) | API docs at `aistudio.google.com` | Choose model screen |
| Perplexity | API docs at `perplexity.ai/account/settings` | Sonar API → default model |

---

## Audit data schema

**One row per run.** Not per question, not per assistant — per run, or the rate cannot be reconstructed and raw answers are lost.

### `runs.csv` — API and hand runs

| Column | Type | Notes |
|---|---|---|
| `audit_id` | String | `slug-YYYY-MM-DD` |
| `client` | String | Business name |
| `run_at` | ISO 8601 | UTC timestamp |
| `assistant` | Enum | `chatgpt` / `gemini` / `perplexity` / `copilot` / `ai-overviews` |
| `surface` | Enum | `api` or `app` — never blank, this determines the band |
| `model_version` | String | Exact string the provider reports |
| `question_id` | String | `q01`–`q10` |
| `run_no` | Integer | 1–5 for API, 1–3 for hand |
| `outcome` | Enum | `not_named` / `named` / `named_detail` / `named_wrong` |
| `competitors` | String | Semicolon-separated, as written in answer |
| `errors` | String | What was said that is untrue, if anything |
| `sources_cited` | String | URLs cited, semicolon-separated |
| `answer_text` | Text | Full answer, verbatim |
| `notes` | String | Refusals, misread questions, outages, oddities |

### `questions.csv` — frozen question set

| Column | Type | Notes |
|---|---|---|
| `audit_id` | String | `slug-YYYY-MM-DD` |
| `question_id` | String | `q01`–`q10` |
| `category` | Enum | discovery / qualified-discovery / named-business / comparison / buying-intent |
| `question_text` | Text | The actual question as run |
| `frozen_from` | String | Client name, for monthly plans |

---

## Storage location

**Client audit data does not go in this repository.** The repo is written as though it were public, and recorded answers contain business contact details and personal data (sole traders' names and addresses are personal data under UK GDPR).

Structure per client:

```
clients/<slug>/audit-YYYY-MM-DD/
  runs.csv
  questions.csv
  checklist.md      (filled copy of audit-site-checklist.md)
  report.md         (filled copy of audit-report-template.md)
  report.pdf        (what the client receives)
```

**Retention recommendation:** keep audit records for the life of the relationship plus twelve months, then delete. Twelve months so a returning client has their baseline; beyond that is stale data held for no reason.

---

## Verbatim answer text is not optional

It is what lets you answer "why did you conclude that" six months later, it is where the report quotes come from, and re-running is not a substitute because the answer will have changed.

**The runner reads `questions.csv` and calls the three APIs, then writes `runs.csv`.** Non-negotiable properties: a hard cap on queries per invocation (so a loop bug costs pence, not pounds), resume capability (provider outage halfway through does not mean starting again), verbatim answer text, and client data written outside the repo.

Deciding each run's outcome, spotting wrong facts, reading the website — those are the judgment the client pays for. Everything the runner cannot do stays manual.
