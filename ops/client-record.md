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

**As of 2026-08-10 this is the only thing `/privacy/` is waiting on.** The
address for service — the other half of that gate since it was written — went
live that day. So one field, `clientDataStorage.where`, now stands between the
site and a published privacy notice, and through it between the business and
both a live order page and a lawful first cold email.

**It was recorded here as "a two-minute look inside the account, not a
decision". That was wrong, and the research on 2026-08-10 is why.** The owner
opened a **consumer** Microsoft account, and a consumer account has no data
location to look up, no contract that would let us process client data through
it, and terms that bar the use outright. Section "The consumer account problem"
below has the sourced detail. **It is a decision after all, and it costs money.**

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
  Microsoft in general. `/privacy/` will not build while the placeholder is
  there — the gate in `site/src/data/legal.ts` checks the string, not just the
  object. **The answer depends on which kind of Microsoft account this is, and
  the next section is the whole of that problem.**
- **A backup that has actually been restored once.** Naming a provider is a
  decision; restoring a file is the proof, and the proof is the part that was
  always the point.

---

## The consumer account problem

*Researched 2026-08-10, after the owner said a "regular account" had been
opened. Every claim here is sourced; the sources are listed at the end of the
section. **The short version: a consumer Microsoft account cannot hold client
records, and no amount of checking settings will make it able to.***

**Three independent reasons, any one of which is enough.**

**1. There is no country to look up, because Microsoft does not commit to one.**
Microsoft's privacy statement (last updated July 2026) says personal data "may
be stored and processed in your region, in the United States, and in any other
jurisdiction where Microsoft or its affiliates, subsidiaries, or service
providers operate facilities." Data residency in Microsoft 365 is a **tenant**
feature: the Data Location card, the Product Terms commitments, Advanced Data
Residency and Multi-Geo all attach to a commercial tenant with a *Default
Geography*. A consumer account has none of them and no admin centre to look in.
Microsoft's own support answer on where OneDrive Personal data sits is that they
"do not specify publicly the exact locations for OneDrive Personal data" and
that a personal user should contact support to ask. **So the two minutes this
file promised do not exist**, and even a support answer would be a statement
about today rather than a commitment we could publish.

**2. There is no Article 28 contract.** Under UK GDPR, whenever a controller
uses a processor there must be a written contract binding the processor, with
the eight specific terms in Article 28(3) — documented instructions,
confidentiality, security, sub-processors, assistance with data-subject rights
and breaches, deletion or return at the end, and audit. The ICO is explicit that
this applies to cloud storage providers and applies before any processing
begins. Microsoft provides those terms through the **Products and Services Data
Protection Addendum**, which attaches to Microsoft **Commercial Licensing**. A
consumer subscription is not commercial licensing and does not carry it. **We
would be a controller handing client personal data to a company with no
processor contract at all** — which is exactly the kind of finding this business
charges to detect in other people's setups.

**3. Microsoft's own terms forbid it.** Microsoft Services Agreement §13.h.i:
Microsoft 365 Family, Microsoft 365 Personal and Microsoft 365 Basic are "for
your personal, non-commercial use, unless you have commercial use rights under a
separate agreement with Microsoft." Storing client records is commercial use.
So is writing a client's audit report in that copy of Word — which matters
because `CLAUDE.md` requires client deliverables in Office formats, so this
reaches further than the storage question.

**What the fix is: a Microsoft 365 Business subscription, with the tenant
created as United Kingdom.**

- **A commercial tenant whose *Default Geography* is the United Kingdom gets a
  Product Terms data residency commitment for SharePoint and OneDrive**, with
  data at rest in the UK — Microsoft's own data centre cities for the UK are
  Cardiff, Durham and London. That turns `clientDataStorage.where` from an
  unanswerable question into "the United Kingdom", published truthfully.
- **The country is chosen at tenant creation and cannot be changed afterwards.**
  This is the one irreversible step in the whole task. **Enter United Kingdom.**
- A Business subscription is Commercial Licensing, so the DPA applies and
  reason 2 is answered at the same time.
- The Data Location card then exists and shows it: **Admin → Settings → Org
  settings → Organization profile → Data location.** That is the two-minute
  check this file originally promised — it just needs the right account to exist
  first.

**The cost, and the honest version of it.** Microsoft's own UK pricing, read
2026-08-10: **Business Basic £5.40 per user/month excluding VAT** (annual,
paid yearly) — about £6.48 inc VAT, roughly £78 a year — which gives the tenant,
1 TB of OneDrive, business email and web-only Word and Excel. **Business
Standard is £18.10 per user/month excluding VAT**, about £21.72 inc VAT, and
adds the desktop apps.

**Which one is a judgement call for the owner, and the two are not equivalent:**

- **Business Basic** fixes the storage problem and the contract problem for
  about £78 a year. It does **not** fix reason 3 for the Office apps themselves,
  because it has no desktop Word — so client `.docx` masters would be written in
  web Word, or in a consumer copy of Word that the terms say is not for
  commercial use.
- **Business Standard** fixes all three and replaces the consumer subscription
  rather than sitting beside it, so the true cost is the difference between the
  two, not £261 on top. It is the clean answer and it is roughly £16 a month.

**A recommendation, since this file exists so decisions are not re-argued:
Business Standard, tenant country United Kingdom.** The £12/month address, the
£47 ICO fee and a £22/month Microsoft bill are the running cost of being a
business that holds other people's data lawfully, and the alternative on offer
is a setup that fails on three grounds at once. **But this is a real recurring
cost during a spending freeze, and it is the owner's call**, so the decision is
put here rather than taken.

**What must not happen in the meantime:** no client or prospect record goes into
the consumer account. That includes the outreach list — a list of named people
at named practices is personal data before anybody has replied.

**One thing deliberately not claimed here.** Whether a consumer account has ever
actually stored a given user's files outside the UK is unknown and unknowable
from outside. The argument above does not rest on it. The problem is the absence
of a commitment and of a contract, not evidence of a bad location.

**Sources**, all read 2026-08-10:
[Microsoft Privacy Statement](https://www.microsoft.com/en-gb/privacy/privacystatement) ·
[Microsoft Services Agreement](https://www.microsoft.com/en-gb/servicesagreement) ·
[Microsoft Q&A: where is OneDrive Personal data stored](https://learn.microsoft.com/en-us/answers/questions/5325400/where-(in-what-country)-is-the-data-stored-for-one) ·
[Microsoft 365 data residency overview and definitions](https://learn.microsoft.com/en-us/microsoft-365/enterprise/m365-dr-overview?view=o365-worldwide) ·
[Microsoft 365 Business plan comparison and UK pricing](https://www.microsoft.com/en-gb/microsoft-365/business/compare-all-microsoft-365-business-products) ·
[ICO: contracts between controllers and processors](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/contracts-and-liabilities-between-controllers-and-processors-multi/when-is-a-contract-needed-and-why-is-it-important/) ·
[Microsoft GDPR compliance and the DPA](https://learn.microsoft.com/en-us/legal/gdpr)

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
