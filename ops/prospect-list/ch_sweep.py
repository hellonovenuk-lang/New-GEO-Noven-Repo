"""Companies House advanced-search sweep, one district at a time.

Repeats the 2026-08-09 sweep recorded in ops/outreach.md section 3, but keeps
the parsed rows so they can be triaged. Output never goes in the repo.
"""

import csv
import html
import re
import sys
import time
import urllib.request

BASE = ("https://find-and-update.company-information.service.gov.uk"
        "/advanced-search/get-results")

ROW = re.compile(
    r'href=/company/(?P<num>\w+) target="_blank">(?P<name>.*?)<span',
    re.S)
BLOCK = re.compile(r'<tr class="govuk-table__row">(.*?)</tr>', re.S)
LI = re.compile(r'<li>(.*?)</li>', re.S)


def strip(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()


def fetch(sic, district, page=1):
    url = f"{BASE}?sicCodes={sic}&registeredOfficeAddress={district}&status=active"
    if page > 1:
        url += f"&page={page}"
    req = urllib.request.Request(url, headers={"User-Agent": "wardith-prospect-sweep/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def parse(page_html, district):
    out = []
    for block in BLOCK.findall(page_html):
        m = ROW.search(block)
        if not m:
            continue
        items = [strip(x) for x in LI.findall(block)]
        items = [x for x in items if x]
        kind = items[0] if items else ""
        inc = next((x for x in items if "Incorporated" in x), "")
        sic = next((x for x in items if x.startswith("SIC codes")), "")
        addr = ""
        for x in items:
            if x in (kind, inc, sic):
                continue
            addr = x
        date = inc.split("Incorporated on")[-1].strip() if inc else ""
        out.append({
            "district": district,
            "company_number": m.group("num"),
            "name": strip(m.group("name")),
            "type": kind,
            "incorporated": date,
            "registered_office": addr,
            "sic": sic.replace("SIC codes - ", ""),
        })
    return out


def total(page_html):
    m = re.search(r'([\d,]+)\s*results?', re.sub(r'<[^>]+>', ' ', page_html))
    return int(m.group(1).replace(",", "")) if m else 0


def main():
    sic = sys.argv[1]
    districts = sys.argv[2].split(",")
    out_path = sys.argv[3]
    rows = []
    for d in districts:
        page, seen = 1, 0
        while True:
            h = fetch(sic, d, page)
            n = total(h)
            got = parse(h, d)
            rows.extend(got)
            seen += len(got)
            print(f"{d}: page {page}, {len(got)} rows (of {n})", file=sys.stderr)
            if seen >= n or not got:
                break
            page += 1
            time.sleep(1)
        time.sleep(1)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} rows -> {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
