# Site check — the technical/crawlability audit, from a URL alone

**Does what `ops/audit-site-checklist.md` groups 1 and 2 ask for, using only
what a real crawler could see.**

The only time that checklist has been run — the Noven self-audit — quietly
used access that only exists for our own site: robots.txt read from the
source repo, redirect/password/CDN checks read from the Netlify dashboard,
JSON-LD "validity" reasoned from knowing the code that generates it. None of
that is available for a client's site. This script fetches the public URL the
way an outside crawler would, and reports what actually comes back.

## Use

Stdlib only — no `pip install`, no API key.

```
cd ops/site-check
python site_check.py --url https://client-site.example
```

Prints a plain-text summary. To keep the full detail, point `--out` at the
client's own folder outside the repo — the same place `runs.csv` and the
filled checklist live (`ops/audit-method.md` §5: client audit data does not go
in this repository):

```
python site_check.py --url https://client-site.example \
  --out ../../../clients/<slug>/audit-YYYY-MM-DD/site-check.json
```

`--cap` (default 8) hard-caps the number of HTTP requests in one run, so a
mistake costs a few requests, not a hammering. `--timeout` (default 15s)
covers slow client sites.

## What it checks

Straight from checklist groups 1 and 2:

- **robots.txt** — fetched live, parsed with Python's own `robotparser`
  (not a hand-rolled parser, because real-world robots.txt syntax is messier
  than ours) against every crawler name the checklist lists. Reports allowed
  vs blocked, named vs falling through to the catch-all, and any blanket
  `Disallow: /`.
- **Can they get in at all** — fetches the homepage with a non-browser user
  agent, follows and logs the redirect chain, flags an apex/www change,
  checks for password/login-wall signals (401/403, `WWW-Authenticate`), CDN
  signals, and challenge-page text ("checking your browser", "just a
  moment", captcha strings). This approximates what the hosting dashboard
  would show — the self-audit read that straight off Netlify, which a client
  audit can't do — and arguably tests the more honest thing anyway: what a
  crawler actually meets, not what a config claims.
- **Can they read it once they're in** — strips tags/scripts from the raw
  HTML and counts what's left. A very low word count on a page that clearly
  has visible content is the standard JS-shell failure mode. **Heuristic, not
  a verdict** — always worth a human glance before it goes in a report.
- **Sitemap** — fetched from the robots.txt declaration or common paths,
  parsed as XML, entry count or child-sitemap list.
- **Structured data** — every `<script type="application/ld+json">` block is
  parsed, `@type`s inventoried, and checked for the presence of the common
  facts (`address`, `telephone`, `areaServed`, `openingHours`, `email`,
  `priceRange`, `offers`, `sameAs`). This is a **structural** check: it says a
  key exists somewhere in the graph, not that the value is right or matches
  the visible page — that comparison is still a human job.
- **Title, H1, meta description** — extracted for a quick read.

## What this doesn't tell you

Every run's JSON output carries a `still_needs_manual_checking` block with
the same list, but it's worth having here too:

- **The Bing/Google `site:domain` index checks** (checklist §3.1/§3.2) are
  public searches, not a webmaster-tools lookup, and this script deliberately
  doesn't automate them — scraping search-results pages is fragile and
  likely against those providers' terms. Two minutes by hand in a browser.
- **Google's definitive "can this be indexed" answer** comes from Search
  Console's URL Inspection tool, which needs verified ownership of the
  client's domain. Not available unless the client grants it. Treat as an
  optional upgrade — the same two-stage access pattern the Foundation
  already uses — not something to expect on a baseline audit.
- **Checklist group 3's off-site half** — Google Business Profile, Bing
  Places, Companies House, professional registers, trade directories,
  LinkedIn, review counts — needs comparing sources this script has no
  access to. Stays manual.
- **Checklist group 4** — whether a page genuinely answers each of the
  client's ten questions — is a judgement about the writing, not a fetchable
  fact. Stays manual.
- **Whether the page states a real price or names real towns** needs a
  person reading the rendered page. A regex hunting for `£` in the wrong
  context is worse than useless here — it's exactly the kind of invented
  precision `CLAUDE.md` rules out.

## A note on running this from inside a locked-down sandbox

This tool needs a live outbound HTTP fetch. It was written and unit-tested
against local HTML strings only — the sandbox it was built in blocks direct
network fetches (the same limit the Noven self-audit hit, which is exactly
why the self-audit substituted source/dashboard access in the first place).
Run it for real from the owner's own machine, the same place `audit_query.py`
makes its API calls from, and sanity-check it against `wardith.co.uk` first —
the self-audit already recorded that site's robots.txt, JSON-LD types and
sitemap state by hand, so any mismatch is immediately diagnosable.
