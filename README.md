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
| Fill in the site checklist during an audit | `playbook/audit-site-checklist.md` |
| Write the report | `playbook/audit-report-template.md` |
| Write a monthly record for a client | `playbook/monthly-record-template.md` |
| Know what we keep, where, and for how long | `playbook/records-and-data.md` |
| Check an account, a cost or a renewal date | `playbook/accounts-and-dates.md` |
| Write anything a customer will read | `playbook/voice.md` |
| Check whether something is already settled | `playbook/decisions.md` |
| Run the assistant queries | `tools/trade-run/` |

## The repository

```
playbook/   how the business is run. Start with business.md
tools/      the scripts: trade-run, site-check, name-check
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

Work on a branch, show it, merge when the owner agrees. **Merging publishes** —
Netlify deploys `main` — so say what a merge will put in front of the world
before doing it, including "nothing visible", which is often the honest answer.
