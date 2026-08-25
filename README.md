# Wardith

Wardith makes a business visible, accurate and recommendable to AI assistants —
ChatGPT, Google, Copilot and Perplexity — when their customers ask one for a
recommendation.

Sole trader, one person. `wardith.co.uk`.

## Where to look

| I need to… | Go to |
|---|---|
| Understand what this business is and where it stands | `playbook/business.md` |
| Know what we sell and what it costs | `playbook/services.md` |
| **Find and email prospects** | `playbook/outreach-process.md` |
| **Deliver an audit** | `playbook/audit-process.md` |
| Set up models, API keys, and audit data schemas | `playbook/models-and-schemas.md` |
| Fill in the site checklist during an audit | `playbook/audit-site-checklist.md` |
| Write the report | `playbook/audit-report-template.md` |
| Know what we keep, where, and for how long | `playbook/records-and-data.md` |
| Check an account, a cost or a renewal date | `playbook/accounts-and-dates.md` |
| Update the website copy or publish an answer page | `playbook/site-code-locations.md` |
| Keep the site indexed in Google, Bing and Copilot | `playbook/search-indexing.md` |
| Write anything a customer will read | `playbook/voice.md` |
| Check whether something is already settled | `playbook/decisions.md` |
| Run the assistant queries | `tools/trade-run/` |
| Count AI mentions against a completed run | `tools/mention-count/` |
| **Qualify a completed run into a campaign** | `/qualify` — `.claude/skills/qualify/` |
| **Prepare outreach for a qualified campaign** | `/outreach` — `.claude/skills/outreach/` |
| Compile a market run into an outreach workbook | `tools/prospect-compiler/` |
| Push prepared outreach into Zoho Mail as drafts — never sends | `tools/zoho-draft-push/` |
| **Run the daily CRM** (every campaign and prospect, next actions, revenue) | `wardith-crm.xlsx`, built by `tools/tracker/` — data lives in `~/wardith-runs/tracker/`, never here |
| Scan for news/research supporting "Why this matters" | `/context-watch` — `.claude/skills/context-watch/` |

**No monthly-plan record template exists yet.** Maintain, Grow and Lead are
priced and published but never delivered — that format will be built from the
first actual recurring client, not designed further pre-revenue.

## The repository

```
playbook/   how the business is run. Start with business.md
tools/      the scripts: trade-run, mention-count, prospect-compiler,
            tracker, site-check, name-check, zoho-draft-push
site/       the website. Astro, deployed from main by Netlify
assets/     brand originals and the email signature
archive/    superseded documents, kept for one review cycle
```

## Two rules that override everything

**Never invent a business fact.** Results, testimonials, statistics, dates,
prices. Anything unknown is written `[PLACEHOLDER]` and flagged to the owner.
The product is verifiable published facts; the moment the repo contains an
invented one, nothing in it can be trusted.

**No client or prospect names in this repository.** It is written as though
public. Those records live on the owner's own encrypted machine —
`playbook/records-and-data.md`.

## Working here

Work directly on `main`; branches are for experimental, high-risk or major
architectural work, or when explicitly requested. **Pushing to `main`
publishes** — Netlify deploys it — so say what a push will put in front of the
world before doing it, including "nothing visible", which is often the honest
answer.
