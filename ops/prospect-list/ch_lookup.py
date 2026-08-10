"""Ask Companies House, one provider name at a time, whether it is a live company.

This is step 3 of the method in `ops/outreach.md` section 3, and it is the PECR
test: limited companies and LLPs may be cold-emailed, sole traders and
unincorporated partnerships may not. A provider name ending in "Ltd" is not
evidence — one Wirral provider whose name ended that way had no live company at
all.

    python3 ch_lookup.py locations.csv "Provider name" out.csv

Reads a CSV with a column of provider names, writes the same rows back with the
company number, registered office and incorporation date appended. Anything it
cannot match exactly is left blank and printed, because a near-match is not a
match when the question is a legal one.
"""

import csv
import html
import re
import sys
import time
import urllib.parse
import urllib.request

BASE = ("https://find-and-update.company-information.service.gov.uk"
        "/advanced-search/get-results")
BLOCK = re.compile(r'<tr class="govuk-table__row">(.*?)</tr>', re.S)
LINK = re.compile(r'href=/company/(?P<num>\w+) target="_blank">(?P<name>.*?)<span', re.S)
LI = re.compile(r'<li>(.*?)</li>', re.S)
SUFFIX = re.compile(r'\b(limited|ltd)\b\.?$', re.I)


def strip(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()


def norm(s):
    """Compare names ignoring punctuation and the Limited/Ltd spelling."""
    s = re.sub(r'\b(limited|ltd)\b\.?', 'ltd', s.lower())
    return re.sub(r'[^a-z0-9]', '', s)


def search(name):
    url = f"{BASE}?companyNameIncludes={urllib.parse.quote(name)}&status=active"
    req = urllib.request.Request(url, headers={"User-Agent": "wardith-prospect-list/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        page = r.read().decode("utf-8", "replace")

    hits = []
    for block in BLOCK.findall(page):
        m = LINK.search(block)
        if not m:
            continue
        items = [strip(x) for x in LI.findall(block) if strip(x)]
        inc = next((x for x in items if "Incorporated" in x), "")
        office = ""
        for x in items:
            if "Incorporated" in x or x.startswith("SIC codes") or "company" in x.lower():
                continue
            office = x
        hits.append({
            "number": m.group("num"),
            "name": strip(m.group("name")),
            "incorporated": inc.split("Incorporated on")[-1].strip(),
            "office": office,
        })
    return hits


def main():
    src, column, out = sys.argv[1:4]
    rows = list(csv.DictReader(open(src, encoding='utf-8')))
    cache, misses = {}, []

    for r in rows:
        provider = (r.get(column) or '').strip()
        r['company_number'] = r['registered_office'] = r['incorporated'] = ''
        if not provider:
            continue
        if provider not in cache:
            # Search without the suffix; Companies House matches substrings.
            query = SUFFIX.sub('', provider).strip()
            try:
                hits = search(query)
            except Exception as e:
                print(f'ERROR {provider}: {type(e).__name__}', file=sys.stderr)
                cache[provider] = None
                time.sleep(2)
                continue
            exact = [h for h in hits if norm(h['name']) == norm(provider)]
            cache[provider] = exact[0] if exact else None
            if not exact:
                misses.append((provider, [h['name'] for h in hits[:4]]))
            time.sleep(1)
        hit = cache[provider]
        if hit:
            r['company_number'] = hit['number']
            r['registered_office'] = hit['office']
            r['incorporated'] = hit['incorporated']

    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    live = sum(1 for r in rows if r['company_number'])
    print(f'{live} of {len(rows)} rows matched to a live company -> {out}', file=sys.stderr)
    if misses:
        print('\nNo exact match, so not contactable until checked by hand:', file=sys.stderr)
        for name, near in misses:
            print(f'  {name}  (nearest active: {"; ".join(near) or "nothing"})',
                  file=sys.stderr)


if __name__ == '__main__':
    main()
