# The client record

**Internal document.** What we keep about each client and prospect, and where it
lives. Renamed from `spine.md` on 2026-07-31 — "the spine" was a word used in
three places and defined in none, and a stranger could not guess what the file
was for from its name.

**Status: the fields are decided, the retention is decided, and the storage
provider was decided on 2026-08-09 — but two steps remain before `/privacy/` can
publish.** Nothing is being kept yet, because there is no client. This exists so
that the first one doesn't start a spreadsheet from scratch, in the wrong place.

**The storage decision blocks something visible.** `/privacy/` has to name who
holds client records and where. Naming the provider was half of it; **the
country and the tested restore are the other half**, and both are below.

---

## The hard constraint, first

**None of this lives in this repository.** It is public, and a record about a
sole trader — their name, their business address, their contact details — is
personal data under UK GDPR. That is what the ICO registration was taken out for
(`ROADMAP.md` 1c), and putting it here would undo it in one commit.

**Decided by the owner 2026-08-09: Microsoft OneDrive.** Office is already paid
for, so it adds no supplier and no cost; the `.docx` audit masters live there
natively instead of being moved by hand; and version history gives a restore that
can actually be tested, which a brand-new account could not have offered for
weeks. `business.clientDataStorage` is set.

**Two things are still owed before this counts as done, and they are not
paperwork:**

- **The country Microsoft holds the data in.** `business.clientDataStorage.where`
  is deliberately a `[PLACEHOLDER]`, because the privacy notice states it in
  published wording and the answer depends on the account rather than on
  Microsoft in general. **Two minutes in the account settings.** `/privacy/` will
  not build while the placeholder is there — the gate in `site/src/data/legal.ts`
  checks the string, not just the object.
- **A backup that has actually been restored once.** Naming a provider is a
  decision; restoring a file is the proof, and the proof is the part that was
  always the point.

**The trigger to move to something else** (Zoho Bigin's free tier is the
researched option) is when you can't answer *"who's due a check this week"* by
looking at it. In practice that is five to eight clients.

---

## What we keep per client

One row each. Add columns when a real need appears, not in advance.

| Field | Why it's here |
|---|---|
| Business name | — |
| Contact name and email | The only channel; there is no phone |
| Website | The thing being audited and fixed |
| What they want to be found for | Fills the question slots; in their words, not ours |
| Area served | Fills the question slots |
| What a new customer is worth | Optional, from the intake. Lets the record say what being missing costs |
| Stage | Enquiry / audit paid / audit sent / Foundation / monthly / lapsed |
| Plan and price | Which tier, what they actually pay |
| Start date | Anniversary, and the twelve-month question freeze |
| Questions frozen until | The freeze date from `ops/audit-questions.md` |
| Work done, dated | What we actually did, so a client asking "what have I paid for" gets an answer |
| Visibility checks, dated | The month-by-month history the monthly record compares against |
| Access held | Which logins we hold for them, so they can be handed back or revoked |
| Retention date | When their records get deleted — see below |

**"Access held" earns its place** even though it looks like admin. At twenty
clients this is a list of live logins to twenty small business websites, several
holding customer enquiry data. Knowing what we hold is the first requirement of
being able to give it back, and the second of not being the reason a client gets
breached.

## What we keep per prospect

Much less, deliberately.

| Field | Why |
|---|---|
| Business, contact, source | — |
| Date contacted, and what was said | So nobody gets approached twice |
| What came back | The only way to learn what the approach is worth |
| Do not contact again | Honour it permanently |

**A prospect list is personal data the day it is written**, when the prospects
are sole traders — which they mostly are. Two things follow that the roadmap has
not carried until now: it falls under the ICO registration and the privacy
notice, and unsolicited marketing email to sole traders and unincorporated
partnerships is governed by PECR in a way that email to companies is not.
Confirm that position before building a cold list. It is not a reason to avoid
outreach; warm introductions sidestep it entirely.

---

## Retention

**Decided 2026-08-09: life of the relationship plus twelve months, then
delete.** The recommendation was taken as it stood, and it is now published
wording in `/privacy/` rather than a suggestion in three documents. Alongside it:
enquiries that go nowhere are kept twelve months, and do-not-contact requests are
kept permanently, because deleting one defeats its purpose.

**One part of this was never ours to decide.** Invoices and payment records have
to be kept for as long as tax law requires — at least five years after the
31 January submission deadline for the relevant tax year — so they outlive the
retention date in the row above. The notice says so plainly rather than promising
a deletion we could not perform.

Whatever is chosen, the retention date goes in the row above, so deletion is a
thing you can do by looking rather than by remembering.

---

## Where audits and reports go

Decided in shape (`ops/audit-method.md` section 5): **one folder per client per
audit**, holding the filled site checklist, `runs.csv`, `questions.csv`, the
report, and the timings. What is left is choosing the storage — same decision as
above, and best made once for both.
