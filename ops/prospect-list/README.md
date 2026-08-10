# Building a prospect list

**Three scripts and an order to run them in.** The method they implement, and the
argument for why it is this way round, is `ops/outreach.md` §3. This file is the
runbook.

**Written 2026-08-10, after the dental list was built with it.** The dental run
is the only one so far, so treat the numbers below as one worked example rather
than a norm.

---

## Why the regulator comes first

The obvious method is Companies House by SIC code and postcode, and it is wrong
as a first step. Run twice, it reproduces itself exactly and **still misses every
practice whose accountant is not local** — twelve of them on the Wirral, one in
five of the real market. A registered office is where the post goes, not where
the business trades, and the whole list is built on that field.

The regulator publishes the trading list. That is the one we want.

**The trade decides whether step 1 exists.** Dental, cosmetic and some
physiotherapy are CQC-registered. Veterinary has the RCVS instead, and its
register has not been checked. For a trade with no regulator, the Companies House
sweep is the only free route and the caveat above applies to the result.

---

## The files

| File | What it does |
|---|---|
| `cqc_filter.py` | Cuts one trade, in one set of postcode districts, out of the CQC national directory |
| `ch_lookup.py` | Asks Companies House whether each provider is a live company — the PECR test |
| `mention_table.py` | Counts who the assistants named, per assistant, and sorts the outreach list by it |
| `ch_sweep.py` | The old postcode sweep, kept as a cross-check rather than as the list |

**No output goes in this repository.** Every file these produce names real
businesses and often real people. `.gitignore` here is the second guard; the
first is writing `--out` somewhere else entirely.

---

## Running it

**1. Get the CQC national directory.** A free CSV, updated most weeks, about
18 MB. The URL carries its date:

```
https://www.cqc.org.uk/sites/default/files/2026-07/22_July_2026_CQC_directory.csv
```

Find the current one on `cqc.org.uk/about-us/transparency/using-cqc-data`. **That
page 403s automated fetches, so a person has to look**, but the CSV itself
downloads without trouble once the URL is in hand.

**2. Cut the trade and the area out of it.**

```
python3 cqc_filter.py cqc.csv Dentist \
    CH41,CH42,CH43,CH44,CH45,CH46,CH47,CH48,CH49,CH60,CH61,CH62,CH63 \
    ~/wardith-lists/wirral-dental.csv
```

The service name matches the CQC's own `Service types` column: `Dentist`,
`Doctors/GP practice`, and so on. Open the national file and read the column
before guessing at it.

**3. Check every provider against Companies House.**

```
python3 ch_lookup.py ~/wardith-lists/wirral-dental.csv "Provider name" \
    ~/wardith-lists/wirral-dental-checked.csv
```

**Read what it prints.** Anything it could not match exactly is listed, and an
unmatched provider is not contactable until a person has looked. It is deliberate
that a near-match is not treated as a match: the question is a legal one.

**4. Triage by hand.** The script cannot do this and should not pretend to.

**5. Sort what is left by who the assistants named.** Needs the trade run
(`ops/trade-run/`), which is the only step here that costs money.

```
python3 mention_table.py ~/wardith-runs/wirral-dentists.csv \
    ~/wardith-lists/wirral-dental.csv \
    ~/wardith-lists/wirral-dental-sorted.xlsx \
    ~/wardith-lists/outreach-names.txt
```

The fourth argument is optional and is the triaged list from step 4, one practice
name per line as the CQC spells it. Give it one and the workbook opens on a sheet
holding only those, which is the sheet to send from; the whole market stays on the
sheet behind it, which is the one to study. **Score the whole market either way** —
the businesses ranked ahead of a prospect are usually ones we cannot or should not
sell to, and they are the content of the email.

**Read what it prints, again.** A practice whose name never matched any answer is
listed rather than scored zero. Left alone, that practice goes out as a Draft B
saying it was named in none of ninety answers, which would be a false statement in
a cold email about somebody else's business — the one mistake this business cannot
make.

---

## What the triage actually removes

In order, because the order matters — each cut is cheaper than the one after it:

- **Duplicate registrations of one location.** A practice that changed hands
  appears twice, once under each provider. Keep the current one.
- **Groups.** National and regional chains, and the NHS trust. A practice manager
  reporting to a group board is a long sale, per `ops/outreach.md` §3.
  **Check the trading name as well as the provider** — one Wirral practice is
  registered to an ordinary-looking company and trades under a group's brand.
- **Providers who are not a company.** "Dr So-and-so", "Such-and-such
  Partnership". §2 closes these and it is not a judgement call. **On the Wirral
  this was 21 practices, about a third of the market.**
- **Anything outside the area.** CH64 is Neston, on the peninsula and in Cheshire
  West. A quoted question that says "the Wirral" does not apply to it.
- **Businesses that are not the product.** A referral service has no patients to
  be found by. A hygiene-only studio does not answer to the dentist questions.
- **The practices the assistants already name.** The last cut and the one that
  needs the trade run. `ops/outreach.md` §4 has the ladder; the top rung is not a
  prospect and emailing them anyway is the fastest way to look like everyone else
  in their inbox.

**Then find the website and the contact address**, from the practice's own site.
The CQC website column is patchy — 27 of 73 on the Wirral — so a blank means
unknown, not absent. **Never infer an address from a domain name.** A wrong
business fact in a cold email is the one mistake this business cannot survive.

---

## What it produced, once

The Wirral dental run, 10 August 2026, from 73 CQC locations in range:

| Cut | Left |
|---|---|
| Duplicate registrations merged | 69 |
| Groups and the NHS trust out | 55 |
| Providers who are not a company out | 34 |
| Neston out | 31 |
| Referral service, hygiene-only, and one with no live company out | 28 |
| **Lawfully approachable** | **28** |
| Ready to send, with a website and an address in hand | 9 |

**28 approachable practices against a batch of twenty a week is a fortnight of
sending.** One trade in one area does not feed the plan for long, and that is the
finding this exercise produced that nobody was looking for.
