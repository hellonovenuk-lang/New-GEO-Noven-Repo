# The client record

**Internal document.** What we keep about each client and prospect, and where it
lives. Renamed from `spine.md` on 2026-07-31 — "the spine" was a word used in
three places and defined in none, and a stranger could not guess what the file
was for from its name.

**Status: the fields are decided, the retention is decided, and the storage
question was reopened on 2026-08-10 and re-answered the same day.** Nothing is
being kept yet, because there is no client. This exists so that the first one
doesn't start a spreadsheet from scratch, in the wrong place.

**The storage decision blocks something visible.** `/privacy/` has to say who
holds client records and where.

**As of 2026-08-10 this is the only thing `/privacy/` is waiting on.** The
address for service — the other half of that gate since it was written — went
live that day. So one field, `clientDataStorage.where`, now stands between the
site and a published privacy notice, and through it between the business and
both a live order page and a lawful first cold email.

**It was recorded here as "a two-minute look inside the account, not a
decision". That was wrong, and the research on 2026-08-10 is why.** The owner
opened a **consumer** Microsoft account, and a consumer account has no data
location to look up, no contract that would let us process client data through
it, and terms that bar the use outright — "The consumer account problem" below
has the sourced detail.

**Then the owner asked whether the records could just live on their own hard
drive, and that is the answer.** It is lawful, it costs nothing, and it makes
the published sentence shorter and more credible. **"Storing it locally" below is
the recommended route and carries the two conditions it depends on** — full-disk
encryption, and a backup that has been restored once. Neither is optional and
both are cheap. **`clientDataStorage` stays unset until both are done**, because
setting it publishes a claim about how this business protects other people's
data.

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
weeks.

**That decision did not survive 2026-08-10 and the two sections below are why.**
The account opened was a consumer one, which fails on three counts; the answer
that replaced it is to hold the records locally on an encrypted machine. **The
2026-08-09 reasoning is kept above rather than deleted**, because two of its
three arguments were sound and still are — no new supplier, no new cost, and a
restore that can be tested — and the local route satisfies all three better than
a Microsoft Business subscription would. What was wrong was the assumption that
"we already have Microsoft" identified a product.

**Two things are still owed before any of this counts as done, and they are not
paperwork:**

- **Full-disk encryption, on and verified**, with the recovery key stored
  somewhere that is not the encrypted disk.
- **A backup that has actually been restored once.** Choosing where data lives
  is a decision; restoring a file is the proof, and the proof is the part that
  was always the point. On the local route this is an Article 32 requirement in
  its own right, not just good practice — see "Storing it locally".

**`business.clientDataStorage.where` stays a `[PLACEHOLDER]` until both are
true.** `/privacy/` will not build while it is there — the gate in
`site/src/data/legal.ts` checks the string, not just the object — and that is the
correct behaviour, because the notice makes a published claim about security.

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

**A recommendation was made here for Business Standard on a UK tenant. It was
superseded within the hour by the owner asking a better question — see "Storing
it locally" below, which is now the recommended answer.** The Microsoft Business
route remains valid and is kept above, because it is the right fallback if the
local route's two conditions cannot be met.

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

---

## Storing it locally — the recommended answer

*Added 2026-08-10, when the owner asked whether the records could simply live on
their own hard drive. **They can, it is lawful, it costs nothing, and it makes
the privacy notice shorter and stronger.** It also moves work rather than
removing it, and the two things it moves are conditions, not suggestions.*

**Why it dissolves the problem rather than dodging it.** All three failures of
the consumer Microsoft account came from involving a third party in storage:

- **No processor, so no Article 28 contract is needed.** The contract duty
  exists because someone else processes data on our behalf. Holding it
  ourselves means there is nobody to contract with. The obligation does not
  reappear in another form; it simply does not arise.
- **The country stops being Microsoft's answer to give.** `where` becomes **the
  United Kingdom** — a laptop in the Wirral is in the UK — and it is true,
  checkable, and cannot be changed without our knowing.
- **Microsoft's non-commercial clause does not reach a folder on a disk.**

**And it is a better sentence to publish.** "Your records are held by us, in the
United Kingdom, and are not passed to a cloud storage provider" is stronger than
naming a US-headquartered supplier, and it is one fewer recipient a reader has to
take on trust. **For a business whose product is verifiable published facts, the
simpler true claim is worth more than the more impressive one.**

**Two conditions, and they are the whole of the cost.**

**1. Full-disk encryption, on and verified.** Article 32 requires security
appropriate to the risk, and the ICO treats encryption as an appropriate
technical measure — with its published position being that where data is lost
and encryption was *not* used, it may consider regulatory action. On Windows
that means BitLocker or Device Encryption, actually switched on rather than
assumed. **Store the recovery key somewhere that is not the encrypted disk** —
the vault, or printed — because a recovery key kept only on the machine it
unlocks protects nothing.

The practical difference this makes: a stolen laptop with the records on it is a
personal data breach either way, but with strong encryption and an uncompromised
key, the data is unintelligible to whoever has it. **That is the ICO's own
example of a breach unlikely to result in a risk to individuals**, and Article 34
is explicit that appropriate protection such as encryption removes the duty to
tell the affected people. **Whether it also removes the duty to report to the ICO
within 72 hours is a judgement to be made and documented at the time, and this
file is not going to assert an answer to it** — see the note on sources below.
Unencrypted, there is no judgement to make: it is a reportable breach, of a list
of named people at named businesses, by a firm registered with the ICO for
exactly this.

**2. A backup that has been restored once — and it is a legal requirement, not
prudence.** Article 32 requires "the ability to restore the availability and
access to personal data in a timely manner in the event of a physical or
technical incident". One hard drive is one failure away from having no client
records at all, which is a breach of availability as much as losing them to an
attacker would be.

**The backup must not quietly undo condition 1 or the whole decision.** A cloud
backup puts us straight back into the processor question. The answer that keeps
the decision intact is **a second encrypted external drive, kept somewhere other
than beside the laptop** — a fire or a burglary that takes one should not take
both. Roughly £30–60 once, against £261 a year for Business Standard.

**This file already demanded a tested restore and that has not changed.** It was
always the part that mattered: naming a provider is a decision, restoring a file
is the proof.

**The sharp edge, and the most likely way this goes wrong.** Windows signed in
to a Microsoft account will, by default, back up Desktop, Documents and Pictures
to OneDrive. **"Stored locally" then silently becomes "stored in the consumer
OneDrive account we just ruled out", with nobody having decided anything.**
Before any client record exists: turn OneDrive folder backup off, confirm it is
off, and keep client folders out of any synced location. **Check this again after
any Windows feature update**, which is exactly the kind of setting that gets
re-offered and accepted by reflex.

**What this does *not* fix, stated plainly.** Writing a client's `.docx` in a
consumer Microsoft 365 copy of Word is still commercial use, which Services
Agreement §13.h.i bars. Local storage does not touch that. **But it decouples
the two questions**, which is the real gain: the Office licence becomes a
contract matter with Microsoft to be decided on its own merits — accept it, use
LibreOffice, or buy Business Standard for the apps alone — instead of a
regulator-facing problem forcing a £261/year purchase during a spending freeze.

**Nor does it empty the privacy notice of processors.** Netlify holds order-form
submissions, Zoho holds email, and running an audit types a client's business
name into four other companies' assistants. Those are all still recipients and
are all already disclosed. What goes away is a *storage* provider.

**The rule this creates — corrected 2026-08-10, an hour after it was written.**
The rule was "do not set `clientDataStorage` until encryption is on *and* a
restore has been tested". **The second half was wrong**, and the way to see it
is to read the page rather than reason about it: `/privacy/` claims "records are
encrypted at rest" and **says nothing whatever about backups**.

- **Encryption is a precondition of publishing**, because the page asserts it.
- **The tested restore is a precondition of taking on a client**, because that
  is when there is data whose availability Article 32 protects. It is not a
  precondition of publishing a page that does not mention it.

**That distinction is worth more than the hour it cost**, because the general
form recurs: *a page gates on what the page claims, not on everything that is
owed.* Bundling the two turned a same-day launch into a shopping trip, on a
business whose stated constraint is to launch as early as possible.

**Recommendation, revised from the one above: store it locally, encrypted, with
an encrypted off-site backup drive.** It is lawful, it is £0 a month against
£261 a year, and it publishes a plainer and more credible sentence. The
Microsoft 365 Business route stays on the table as the fallback if the
encryption or the backup cannot be done — but they are an afternoon and about
£40, not a subscription.

**Set 2026-08-10.** `clientDataStorage` now reads
`{ name: 'us, on our own encrypted computer', where: 'the United Kingdom' }`,
and `/privacy/` publishes. The notice renders "It is held by us, on our own
encrypted computer, in the United Kingdom." **The one thing that has to be true
before that merges is full-disk encryption being on**, which is the page's own
claim and nobody else's.

**And the honest scope of what it describes: today it describes nothing.**
There is no client and no client record. The sentence states where records
*will* be held, published before the first one exists — which is the right way
round, because a privacy notice that arrives after the data does is the failure
it exists to prevent.

**On sources for this section.** The Article 28, 32, 33 and 34 obligations
described here are the text of UK GDPR and are not in dispute. **The ICO's own
guidance pages could not be read from this session — `ico.org.uk` returns HTTP
403 to automated fetching**, the same wall that stops the register being checked
here. So the ICO's positions above are reported from search summaries of their
guidance rather than from the pages themselves, and the one point where those
summaries contradicted each other — whether an encrypted lost device must still
be reported to the ICO — is deliberately left open rather than resolved by
picking the more convenient reading. **Two pages to read in a browser before
relying on this:** the ICO's *Encryption and data storage* guidance, and
*Personal data breaches: a guide*. *Not legal advice.*

---

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
