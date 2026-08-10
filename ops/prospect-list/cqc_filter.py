"""Pull one trade's CQC-registered locations, in one set of postcode districts,
out of the CQC's national directory.

This is step 1 of the method in `ops/outreach.md` section 3 — the regulator is
the census, and it is the trading list rather than the registered-office list.

    python3 cqc_filter.py cqc.csv Dentist CH41,CH42,CH43 out.csv

The national file is a free download from CQC and the URL carries its date:
https://www.cqc.org.uk/sites/default/files/YYYY-MM/DD_Month_YYYY_CQC_directory.csv
Find the current one on cqc.org.uk/about-us/transparency/using-cqc-data — the
site 403s automated fetches, so the link needs a person, but the CSV itself
downloads fine once you have the URL.

The output names real businesses. It goes outside this repository, per
`ops/audit-method.md` section 5.
"""

import csv
import re
import sys

PC = re.compile(r'\s*([A-Z]{1,2}\d{1,2}[A-Z]?)\s*\d[A-Z]{2}\s*$')

KEEP = ['Name', 'Address', 'Postcode', 'Phone number',
        "Service's website (if available)", 'Provider name',
        'Local authority', 'Region', 'Location URL',
        'CQC Location ID (for office use only)',
        'CQC Provider ID (for office use only)']


def district(postcode):
    m = PC.match((postcode or '').upper())
    return m.group(1) if m else ''


def main():
    src, service, districts, out = sys.argv[1:5]
    wanted = {d.strip().upper() for d in districts.split(',')}

    rows = []
    with open(src, encoding='utf-8-sig', errors='replace') as f:
        header = None
        for row in csv.reader(f):
            # The file opens with a few title lines before the real header.
            if row and row[0] == 'Name':
                header = row
                continue
            if not header or len(row) < len(header):
                continue
            d = dict(zip(header, row))
            if service.lower() not in (d.get('Service types') or '').lower():
                continue
            if district(d.get('Postcode')) in wanted:
                rows.append(d)

    rows.sort(key=lambda d: (district(d['Postcode']), d['Name']))
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=KEEP, extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)

    counts = {}
    for d in rows:
        counts[district(d['Postcode'])] = counts.get(district(d['Postcode']), 0) + 1
    sited = sum(1 for d in rows
                if (d.get("Service's website (if available)") or '').strip())
    print(f'{len(rows)} {service} locations -> {out}', file=sys.stderr)
    print('  by district: ' + ', '.join(f'{k} {v}' for k, v in sorted(counts.items())),
          file=sys.stderr)
    print(f'  with a website on the CQC record: {sited}', file=sys.stderr)
    print('  the website field is patchy; treat a blank as unknown, not as absent.',
          file=sys.stderr)


if __name__ == '__main__':
    main()
