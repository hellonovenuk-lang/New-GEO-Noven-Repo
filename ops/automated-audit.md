# Automating the audit — findings

**Internal document.** Written 2026-07-30, in answer to the owner's question:
can we take a card payment on the site for the £30 audit and have the report
sent by email automatically, with no involvement from him?

**Status: findings, not a decision.** Nothing here is built. Section 9 lists
what the owner still has to decide. This closes nothing in the roadmap — it
sets up 3a and adds detail to 1c.

Produced by four separate reviews arguing against each other: one designing the
full build, one arguing against doing it at all, one designing the cheapest
route, one specifying what the report has to contain. Where they ended up
agreeing is worth more than any one of them, so that is section 1.

---

## 1. The short answer

**Most of it can be automated. The send cannot — and none of the four reviews
argued otherwise once they had read what the site promises.**

The pipeline splits cleanly:

| Can run without the owner | Must not |
|---|---|
| Taking the payment | Sending the report |
| Collecting what we need to know | Deciding a fact about the client is true |
| Asking the assistants, 240 times | Deciding who counts as a competitor |
| Checking the client's website | Telling someone they don't need us |
| Recording every answer | Telling someone their site is broken |
| Assembling the draft | Naming a rival |
| Applying the recommendation rules | |

That is not a hedge. The machine does the repetitive part, which is most of the
elapsed time and nearly all of the tedium. What is left for the owner is
**ten to fifteen minutes per audit**, against sixty to ninety minutes fully by
hand.

The reason the last step stays human is in `CLAUDE.md`: never invent business
facts. A machine writing about a real plumber will state their opening hours or
their accreditations confidently and wrongly, and there is no way to catch that
from inside the pipeline. The FAQ actively invites the client to check our work
— *"ask ChatGPT or Perplexity what the £30 audit includes, and compare"* — so
the first wrong report is disproved by the client in under a minute. The only
asset this business has yet is being the one that doesn't do that.

**The bigger win is not the send anyway.** Today the site promises a reply
within two working days, and then the report within one working day of that. A
paid intake form deletes the two-day wait entirely. Automating the final send
saves hours; automating the front of the process saves days. The owner's
instinct was right about the payment and half right about the email.

---

## 2. What the pipeline looks like

Intake first, payment last. Both the build review and the cheap-route review
started on opposite sides of this and converged on it:

1. **One form** collects business name, website, town, trade, service area,
   phone as listed, and up to three questions the client wants asked. Stripe
   allows only three custom fields on a payment link or checkout, so the
   details cannot ride along with the payment.
2. **Payment is the last step of that form.** This matters beyond tidiness: it
   makes "paid but never told us anything" structurally impossible, and it puts
   the consent wording in front of the buyer before the contract concludes
   rather than after.
3. **Payment confirmed** triggers the run.
4. **The machine works** — 12 questions, 5 runs each, 4 assistants, plus the
   site checks. Under half an hour of wall-clock.
5. **A finished draft** lands in front of the owner with everything filled in.
6. **The owner reads it, clears the three judgement calls, and sends** from the
   existing mailbox.

Step 6 is the whole of his involvement.

**Hand-sending from Zoho is an advantage worth keeping**, not a limitation.
The mailbox already has working SPF and DKIM (`ops/zoho-mail-setup.md`). An
automated sender means a new subdomain, its own DNS records and a reputation
warm-up on a domain that is weeks old — real work, undertaken solely to save
the last eight minutes.

---

## 3. What the report contains

Full specification in the appendix of this document's working notes; the
short version is what the audit can honestly measure.

**Signals that survive a small build:** how often each assistant names the
business, per question; who gets named instead; what the assistants believe
about the business and whether it matches what the owner told us; how often the
assistant declines to recommend anyone; whether AI crawlers are allowed in
(both what `robots.txt` says *and* what a live fetch with those user agents
actually gets, because they differ); whether the structured data is present and
valid; and whether the site serves real text or an empty shell that needs
JavaScript.

**Signals worth dropping from a first version:** consistency of the business's
details across directories, which is the most brittle and expensive thing to
build; whether a specific page answers a specific question, which needs
retrieval; ordering within an answer, which is usually undefined in prose; and
heading structure, which never leads a report anyway.

If the directory check is dropped, **the report must say so** rather than
implying it was checked and clean. The Foundation then scopes that part after
payment.

**Counts, never percentages.** `ops/third-party-services.md` E3 established
that a single run is noise. Five runs resolves to twenty-point steps, so a
percentage is false precision dressed as rigour — the exact thing we say
distinguishes us from tools selling confident single-run scores. Each question
scores **Present** (3+ of 5 runs), **Occasional** (1–2), or **Absent** (0), and
the report's two headline numbers are integers: how many of the ten questions
are strong, and how many of the four assistants name them at all.

**Question count: 10 customer questions plus 2 about the business itself, five
runs each, four assistants — 240 grounded calls, comfortably under £2.** Ten
matches Maintain exactly, so the audit is a true sample of what the monthly
plan delivers and cannot contradict the pricing page. The two brand questions
are counted separately, or the mention rate flatters itself.

---

## 4. The recommendation

Rules, applied in order, first match wins. No model picks the tier; the model
only writes prose around a decision the rules already made.

| # | Condition | Recommendation |
|---|---|---|
| 1 | 8+ of 10 questions strong, on 3+ assistants, no false beliefs, crawlers allowed, structured data valid | **You don't need us** |
| 2 | That visibility, but a blocking fault | **Foundation only** |
| 3 | Same competitors named in 5+ of 10 non-mentioning runs on their top three questions, and they are Present on 4+ questions | **Lead** |
| 4 | 4–7 questions strong, faults present | **Foundation, then Maintain** |
| 5 | 3 or fewer strong, technicals sound | **Foundation, then Grow** |
| 6 | 3 or fewer strong, faults present | **Foundation, then Maintain** |
| 7 | No site, or a site too broken to work on | **Say so, recommend nothing yet** |

Row 1 has to fire in real audits or the promise on three published pages is
decorative. The two reviews that proposed thresholds started far apart on it —
one at a bar so high it would almost never fire, one at a bar low enough to
call a business fine when three of four assistants have never heard of it — and
settled here. The bar is deliberately near the strict end: telling someone
they're fine when they aren't, to keep the promise looking alive, is a worse
dishonesty than the row rarely firing.

**Rows 1, 3 and 7 stay human permanently.** They are the ones with consequence
— we're either turning away money, naming a rival, or telling someone their
website is broken. Rows 2, 4, 5 and 6 can eventually release unattended. That
shrinks the human step from ten minutes on every audit to about three minutes
on roughly a third of them.

**[PLACEHOLDER: the numbers in rows 1, 3, 4 and 5 are policy guesses. Revalidate
after ten real audits.]** The row 2 and row 7 conditions are not guesses; they
are pass/fail facts about a website.

---

## 5. What it costs

| | Per audit |
|---|---|
| Assistant APIs | ~£2.00–2.50 |
| Stripe, UK card, 1.5% + 20p on £30 | £0.65 |
| **Net of £30** | **~£27** |

Google's free grounding allowance alone covers roughly 25–40 audits a month at
zero cost (`ops/third-party-services.md` E2), so early audits cost less than
this. Fixed monthly cost in the version recommended here is **£0** — no
automation subscription, no hosting beyond what exists.

**[PLACEHOLDER: confirm Stripe's current UK dispute fee — sources disagree
between £15 and £20.]** At either figure a single chargeback wipes out about
two clean sales, which is an argument for warm buyers before a public button,
not against cards.

**Build effort.** The full autonomous stack was costed at around 81 hours. The
subset that is genuinely not throwaway — the question library, the site-check
script, the record format, the recommendation rules as a function — is about
**12 hours**, and every hour of it saves time on manual audits too. Everything
payment- and infrastructure-shaped defers with no rework later.

Eighty-one hours against zero delivered audits is building the factory before
proving the product, and it is eighty-one hours not spent on Phase 2, where the
actual bottleneck is that nobody has been approached yet.

---

## 6. What has to be true before any card button

In order. The first four are already on the roadmap in 1c; this puts them in
sequence and prices them.

| # | Must be true | Cost | Lead time |
|---|---|---|---|
| 1 | ICO self-assessment run, fee paid if due | £47–52/yr | Same day |
| 2 | Privacy notice live, linked in the footer | Free | An evening |
| 3 | Business bank account open — Stripe pays out to it | Free | 1 day to 3 weeks |
| 4 | Service address confirmed receiving mail, footer updated | £10–115/yr | Ordered, not delivered |
| 5 | Terms page, and a receipt out of Zoho Books | Free | Half a day |
| 6 | One audit delivered by hand, start to finish, and timed | Free | One working day |
| 7 | Refund line and immediate-supply wording in the payment email | Free | Ten minutes |

**The ICO fee is the one that changed.** The reasoning in 1c — that the notice
can wait because the site collects nothing — is exactly what an intake form
invalidates. A form plus a spreadsheet holding a named person's details is an
automated filing system on day one, and the point of collection is where the
privacy notice legally has to be. Registration is £47 by Direct Debit against a
penalty of up to £4,000 for not having it. It is not a close call.

Items 1–7 clear a **payment link sent by email to someone we've spoken to**.

A **public "buy now" button on the site** needs three more things: ten audits
delivered by hand, rate limiting (anyone can pay £30 to profile a competitor,
and a script can trigger a hundred), and the copy fix in section 7.

---

## 7. Two sentences on the site that this contradicts

Both are published today and both are ours to change deliberately — but they
have to be changed *before* the thing they describe stops being true, not
after.

**`site/src/pages/faq.astro:79`** — *"the person who answers your email is the
person who does the work and writes your report."* If software drafts the
report, that sentence is false. Proposed replacement, which stays honest and
arguably sells better:

> The person who answers your email is the person who reads the answers and
> writes your report. Software asks the assistants the questions and records
> what they say, because that part is repetitive and machines are better at it.
> The judgement and the writing are his.

**`site/src/pages/contact.astro:17`** — *"No forms, no call-booking software,
no follow-up sequence."* A paid intake form living **only behind the payment**
does not break this, and the promise is about how you reach us. A form on the
contact page would break it. Keep the form where it is and this sentence
stands.

Also affected once self-serve exists: `faq.astro:26` and `contact.astro:38`
both promise a two-working-day reply *then* one working day for the report.
Self-serve makes the first half obsolete, which is a copy improvement, not a
problem.

---

## 8. What not to do

- **Don't hand-format reports** in a design tool. A template with named slots
  is the same work and becomes the machine's output later with no rewrite.
- **Don't put the API calls inside an automation subscription.** They can't be
  migrated out and they're metered. A script the owner owns runs anywhere.
- **Don't buy an automation tier yet.** The free tiers cover roughly a hundred
  audits; the owner's time breaks long before any of them do.
- **Don't build the checkout into the site yet.** The build is static today,
  and server code, secrets and a payment surface are all deferrable with no
  rework.
- **Don't let records live only inside a form tool.** From audit one, one sheet
  the owner controls, with the columns `ops/third-party-services.md` E3
  specifies — question, assistant, model and version, date, run number,
  mentioned, competitors named, raw answer text — plus minutes spent and the
  recommendation given. Retro-fitting a format across twenty inconsistent
  records is miserable, and minutes-spent is the number section 6 of
  `ops/service-tiers.md` says decides whether the business works.

---

## 9. Decisions for the owner

1. **Is the ten-to-fifteen-minute human check the end state, or a waypoint?**
   The cheap-route review argued it is the end state: at twenty audits a month
   it is four hours, and the thing that actually caps this business is Maintain
   delivery time, not audit send time. Full auto-send saves eight minutes an
   audit and adds the risk of a wrong report reaching a stranger unread.
2. **When does the public button go live?** Proposed trigger, rather than a
   number: five audits delivered inside one working day, the question library
   covering the target trade, the decision table surviving five real reports
   unchanged, and no refunds.
3. **Does the £30 credit against the Foundation if booked within 30 days?** It
   costs £30 of £350 and turns the audit into a decision. If yes, it lands on
   `pricing.astro`, `faq.astro` and `business.ts` together.
4. **Confirm the section 4 thresholds** after ten audits, not before.
5. **Approve the FAQ rewording in section 7** before any drafting is automated.

---

## 10. The dissent worth keeping

The review arguing against all of this made one point that none of the others
could answer, and it should be read before any of the above is built:

**`ops/service-tiers.md` section 6 says the Foundation is the year-one income
and converting audits into Foundations is what matters. The conversation that
follows the report is how that conversion happens.** Twenty automated audits
gross £600; one Foundation is £350. Optimising the £600 while removing the
mechanism that produces the £350 would be a bad trade, and it would also cost
the pattern recognition that makes Maintain deliverable in an hour a month.

The answer the others gave — that the *report itself* is the conversation, and
that a recommendation ending in one plain question is not a worse opening than
a scoping email — is plausible but untested. It stays untested until audit one
has been done by hand.

**So: build in the order in section 6. Audit one is item six on that list, and
nothing downstream of it should be written until it has been done once.**
