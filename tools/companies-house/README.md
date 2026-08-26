# companies-house

A structured, read-only client for the Companies House public data API,
standing in for the manual browsing `/qualify` Stage 5 has always used to
verify a business is a real, active Ltd company or LLP before it can reach
`outreach[]` (`playbook/outreach-process.md` step 3: "no verified active
Ltd company or LLP at that trading name, no email").

It does not remove the judgement call — a name search can return several
plausible candidates (a chain, a similarly-named firm, a dissolved-then-
reincorporated entity) and picking the right one, or deciding none is
defensible and the business stays `REVIEW`, is still made from the
structured data this returns. What it replaces is the manual page-scraping,
not the verification step.

## One-time setup

1. Register a free account and application at
   [developer.company-information.service.gov.uk](https://developer.company-information.service.gov.uk/).
2. Create a "Live" application (`REST API` access) and copy its API key.
3. Add it the same way every other provider key already goes in, per
   `playbook/records-and-data.md`:
   - Bitwarden, as the copy of last resort.
   - `~/.noven/env`, outside any git repository:
     ```sh
     cat >> ~/.noven/env <<'EOF'
     export COMPANIES_HOUSE_API_KEY="..."
     EOF
     chmod 600 ~/.noven/env
     ```
4. **Done.** `/qualify` Stage 5 will use it automatically from then on. If
   `COMPANIES_HOUSE_API_KEY` isn't set, Stage 5 falls back to the manual
   `WebFetch`/`WebSearch` method unchanged — this is never a blocker to
   running `/qualify`.

Unlike Zoho, this is a single static API key, not OAuth — no separate grant
step, no refresh token, no `~/.wardith/` credentials file.

## How to revoke access

Delete or deactivate the application at
[developer.company-information.service.gov.uk](https://developer.company-information.service.gov.uk/),
then remove the key from `~/.noven/env` and Bitwarden.

## What this tool will and won't do

- **Will:** search Companies House by company name (`GET
  /search/companies`) and fetch a single company's profile by number (`GET
  /company/{number}`) — company status, type, registered office address,
  incorporation date.
- **Won't:** write, create, update, or delete anything at Companies House —
  there is no such capability in this public API for a key to reach in the
  first place. Every call this tool makes is a `GET`.
- **Won't:** decide which candidate is the right match on its own. A name
  search commonly returns more than one plausible result; `/qualify` Stage
  5 still applies the same "defensible, active Ltd/LLP match, or `REVIEW`"
  rule it always has, just against structured JSON instead of a scraped
  page.

## Auth

HTTP Basic Auth, API key as the username, empty password — not OAuth, not
a bearer token. This is Companies House's own documented scheme, distinct
from every other provider key in this repo.

## Manual usage

```
python3 tools/companies-house/company_lookup.py --name "Acme Plumbing Ltd"
python3 tools/companies-house/company_lookup.py --number 12345678
python3 tools/companies-house/company_lookup.py --name "Acme Plumbing Ltd" --json
```

Reads the key from `COMPANIES_HOUSE_API_KEY` unless `--api-key` is given
explicitly.

## Running the tests

```
cd tools/companies-house
python3 test_company_lookup.py -v
```

No real network calls, no real Companies House API key required — every
`urllib.request.urlopen` call is mocked.
