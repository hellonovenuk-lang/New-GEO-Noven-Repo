# Agency attribution

Builds an agency contact list from a completed market census: for each
business, finds the web designer or SEO agency credited on its own site,
then researches each credited agency once for whether it's a plausible
buyer of the white-label product.

**Nothing here decides who to approach.** It finds and records public
evidence; the owner reads the output and decides. See
`playbook/agency-product.md` for the product this feeds.

## Why the qualifying fields are what they are (2026-08-23)

The original design treated this as a verification sell — proof that
schema/structured-data work moved the needle. That assumption doesn't hold:
agencies are paid on delivery and have no reason to want past work checked.

What an agency actually has is lumpy project revenue and a dormant client
list with no natural reason to re-contact it. The product is a
**re-engagement asset**: a branded report they can forward to a past
client, which surfaces who has a problem worth a new project. So:

- **PRIMARY `sells_retainer`** — a care plan, maintenance package, hosting
  retainer, or any recurring service. An agency already billing
  recurring revenue can add a line to it; a pure project shop is being
  asked to become a subscription business, a much bigger ask than the
  price implies.
- **PRIMARY `publishes_client_work`** — case studies, portfolio entries,
  client news. An agency that never writes about its clients is unlikely
  to forward a report about one.
- **SECONDARY `mentions_schema_or_aeo`** — advertises schema/structured
  data/GEO/AEO work. Kept, no longer a primary signal.
- **DISQUALIFYING `sells_ai_visibility`** — already sells an LLM-visibility
  or AI-visibility audit/monitoring product. This disqualifies them from
  the white-label pitch outright: a sample of their own client reads as an
  accusation that their own monitoring missed something. (This is the
  specific failure mode of the Max Web approach.)

## Input

- **`--census`** — a market census CSV, the same shape `/qualify` produces
  (`market-census-<slug>.csv`): needs a business-name column
  (`--business-column`, default `business`) and a website column
  (`--website-column`, default `website`). A business with no recorded
  website is skipped and listed in `skipped_no_website` — this script
  never guesses a URL.

## Output

**`agencies.csv`, written wherever `--out` points — never into this
repository.** `CLAUDE.md`'s "no client or prospect names in this
repository" rule is absolute and covers agency names too: they're personal/
business data about real companies, found through real client
relationships. The script refuses to run if `--out` resolves inside the
repo.

One row per distinct agency domain credited by at least one census
business:

| Column | Meaning |
|---|---|
| `rank` | See "Ranking" below |
| `agency_domain`, `agency_url` | |
| `agency_type` | `WEB_DESIGN` / `SEO` / `UNKNOWN`, from the agency's own homepage + portfolio text |
| `sells_retainer`, `publishes_client_work`, `mentions_schema_or_aeo`, `sells_ai_visibility` | The four qualifying fields above |
| `census_clients` | How many census businesses credit this agency — flag anything >1 prominently, it's the strongest signal in the file |
| `census_clients_confirmed` | Of those, how many the agency's own site (homepage or portfolio) also names — a portfolio mention distinguishes a *current* relationship from an old build credit a footer link alone can't |
| `census_clients_list`, `census_clients_confirmed_list` | Semicolon-separated, matching the `competitors` field convention elsewhere in this repo |
| `recent_maintenance_signal_count` | How many of this agency's credited clients show recent-maintenance signals (copyright year, sitemap `lastmod`) on their own site — a live relationship reads differently from a stale one even where the census evidence can't confirm current representation |
| `portfolio_url` | The page `publishes_client_work` and the confirmation check were read from, if found |
| `credit_method` | `phrase` (a "designed by"-style credit) and/or `keyword` (footer link whose text/domain merely reads as an agency — weaker, used only when no phrase credit exists for that business) |
| `evidence_notes` | The actual credit text found, truncated |
| `fetch_status` | `ok`, or the error if the agency's own site couldn't be fetched |

## Ranking

**Disqualified agencies (`sells_ai_visibility=true`) always sort last**,
regardless of every other field — they are never a candidate for this
pitch. Among the rest: `sells_retainer AND publishes_client_work` first,
then `census_clients` descending, tied by domain for determinism. This
surfaces the agencies most likely to actually send something, not the ones
with the most clients.

## How credit extraction works, and its real limits

Two tiers, tier 2 only used when tier 1 finds nothing for a business:

1. **Phrase-anchored** — a footer link immediately preceded by ("or whose
   own anchor text carries) a known credit phrase: "designed by", "built
   by", "web design by", and similar. High confidence.
2. **Keyword fallback** — any footer-region outbound link (excluding
   social/directory/utility domains) whose anchor text or domain reads as
   an agency ("web design", "digital studio", ...). Weaker, and it's why
   `credit_method` is recorded per agency.

**This will under-find, not over-find, real relationships.** A site with no
footer credit at all (agency didn't ask for one, or the client removed it)
produces nothing — there is no way to find an uncredited relationship from
the client side alone. `census_clients` is a floor, not a census of who
each agency actually serves.

**`agency_type`/`sells_retainer`/`mentions_schema_or_aeo`/
`sells_ai_visibility`** are keyword-heuristic reads of the agency's own
homepage and (if found) portfolio page text — not a confirmed fact. Spot
check before treating any single row as gospel, same discipline as every
other heuristic tool in this repo.

## Politeness

Every request goes through a robots.txt check first (`urllib.robotparser`,
one fetch per origin, cached for the run) and is skipped — not
substituted, not retried a different way — if disallowed for this tool's
user-agent. Requests are rate-limited (`--delay`, default 1.5s) and capped
per run (`--cap`, default 250). The tool identifies itself:

```
WardithAgencyAttributionBot/1.0 (+https://wardith.co.uk; research tool
building an agency contact list from public credit links; read-only, no
forms submitted; respects robots.txt)
```

Nothing is submitted to any site. No end client or agency is contacted by
this script — it only reads public pages, the same way any crawler would.

## Usage

```
python3 agency_attribution.py \
    --census ~/wardith-runs/<slug>/market-census-<slug>.csv \
    --out ~/wardith-runs/<slug>/agencies.csv
```

Optional `--report-json PATH` also writes the full structured report
(per-business fetch errors, every credit candidate found, everything the
CSV summarises) — useful for auditing a surprising row without re-running.

## Requirements

Python 3.9+, stdlib only. Nothing to `pip install`.
