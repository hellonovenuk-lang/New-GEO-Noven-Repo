# LinkedIn — profile rewrite and the Noven page

**Internal document.** Written 2026-07-29. Everything in here is copy to paste
and steps to follow inside LinkedIn, which only the owner can sign into.

This closes roadmap item 1a — *"Amend the LinkedIn profile, and create the
Noven business page"*.

**Why it matters more than it looks.** Noven's whole argument is that a
business is recommended when its facts agree with each other everywhere they
appear. Two pages saying the same thing about the same person is the cheapest
possible version of that, done on ourselves. It is also the first thing anyone
does after getting an email from a stranger: they look you up.

Anything below in `[PLACEHOLDER]` is a fact I don't have. Don't guess it —
the questions are gathered in section 6.

---

## 0. Read this before you touch anything

**Do it in this order.** Each step depends on the one above it.

| # | Step | Why this order |
|---|---|---|
| 1 | Create the Noven company page (section 5) | The page must exist before the profile can link to it |
| 2 | Add Noven as your current role on the profile (section 3) | Typing "Noven" in the company field now finds the real page, attaches its logo, and makes the two pages point at each other |
| 3 | Replace the About section (section 2) | — |
| 4 | Fill the missing Maersk description and fix the older ones (sections 3–4) | — |
| 5 | Add the website to both, **but see the warning below** | — |
| 6 | Set `businessLinkedIn` in `site/src/data/business.ts` (section 5.6) | Needs the finished page URL |

### The one thing that would actively hurt us

**`novenstudio.co.uk` still serves the old website.** The Noven site is built
but not deployed — that's the biggest open item on the roadmap. If you put that
address on LinkedIn today, every person who follows it lands on something that
isn't Noven, and so does every AI crawler that reads the page. A wrong,
crawled, cached fact is precisely what the audit is paid to find on other
people's businesses.

So: **either deploy the site first, or leave every website field blank for
now.** Blank is recoverable; wrong is what we sell against. I've marked each
website field below as `[HOLD until the site is live]` so it's obvious which
ones are waiting on that.

Everything else in this document can be done today.

---

## 1. What's on the profile now, and what's wrong with it

From the three screenshots, as of 2026-07-29:

| Section | Current state | Action |
|---|---|---|
| About | Written entirely about **Port Brief** (`portbrief.co.uk`), a project the owner confirms is finished | Replace — section 2, then sweep 3.4 |
| Headline | Not visible in the screenshots — whatever it says, it predates Noven | Replace with the line in section 3.1 |
| Maersk, Global Customer Experience Consultant (Sep 2024 – Jun 2025) | **No description at all** | Write it — section 3.3 |
| Maersk, Senior Customer Experience Consultant (Sep 2023 – Aug 2024) | Has a description, reads fine | Light tidy — section 4.1 |
| Sealand, Senior Customer Service Agent (Oct 2018 – Feb 2024) | Description shows broken `?` characters where bullets should be | Fix — section 4.2 |
| Seago Line, Customer Service Advisor (Jan 2017 – Oct 2018) | Same broken `?` characters | Fix — section 4.2 |
| Current role | Nothing since Jun 2025 — a 13-month gap, and the profile doesn't say you run Noven | Add Noven — section 3.2 |
| Top skills | Reads "**Frieght** Management" — a typo, on the profile of someone selling accurate business information | Fix — section 4.3 |
| Followers | 295 | — |

**The Port Brief problem is worse than a stale paragraph.** The About section
tells people to subscribe at `portbrief.co.uk` and promises them an email every
Tuesday. If that project is finished, the profile is currently making a
standing promise nobody is keeping, to anyone who reads it. It should come down
whether or not the Noven copy is ready.

### The "ten years" discrepancy — settled, and the site is now fixed

The old About said **"I spent 10 years inside the shipping and logistics
industry."** The site's About page said **"nearly ten years in operations at
Maersk."** Neither survived checking.

**The owner confirms the real figure is eight years and nine months.** The
answer everywhere is **"eight years"**, and that is already applied:

| Where | Now reads |
|---|---|
| `site/src/pages/about.astro` | "Kieran spent eight years in operations at Maersk" |
| `ops/service-tiers.md` §7 | "Eight years of operations at Maersk" |
| This doc's About copy (section 2) | "For eight years I worked in shipping operations" |
| Headline option B (section 3.1) | "Eight years in global shipping operations" |

**Why "eight" and not "nearly nine", which is also true.** The dates visible on
the profile run Jan 2017 → Jun 2025, which reads as eight years and five months
to anyone doing the arithmetic. "Nearly nine" invites a check it doesn't quite
pass; "eight years" is true against both the owner's figure and the profile's
own dates. Round down when the reader can count.

**Minor loose end, no copy impact:** those visible dates give 8y5m, not 8y9m.
If the 8y9m figure is right, a start or end date on the profile is out by a few
months — worth a glance while you're in there, but it changes nothing above.

Eight years that survive checking is a stronger claim than ten that don't.

---

## 2. The About section — replacement copy

LinkedIn's limit is 2,600 characters. This is about 1,900, which is deliberate:
the first three lines are all most people see before "…see more", so the point
lands there.

It follows the same shape as the Port Brief version, which was well built — a
real conversation, the problem behind it, what you did about it. That shape is
kept. Only the subject changes.

> For eight years I worked in shipping operations — most of it at Maersk, and
> latterly running the global cargo process end to end for two of the UK's
> largest retailers.
>
> Strip that job back and it was mostly one thing: making sure the same
> information was true in every system that touched it. When a booking, a
> customs entry and a delivery note disagree, someone pays for it — usually in
> demurrage, always in trust.
>
> Now I run Noven, and it turns out to be the same problem wearing different
> clothes.
>
> Here's the shift that started it. When someone needs an accountant, a
> solicitor or a clinic, a growing number of them no longer scroll through a
> page of search results. They ask ChatGPT, Google, Copilot or Perplexity —
> "who's good near me?" — and they act on the answer they get back.
>
> Most small firms have no idea what those assistants say about them. A few are
> recommended. Most aren't mentioned at all. And the reason is usually dull and
> fixable: the systems can't read the website properly, the business's own facts
> contradict each other across the web, or nothing anyone has published actually
> answers the question the customer asked.
>
> Noven does that work, for businesses that were never going to spend £400 a
> month with an agency.
>
> £30 buys a written report on what the assistants say about you today and
> what's in the way. £350 sets it right. From £75 a month keeps it that way,
> with a written record of where you appeared and where you didn't. No minimum
> term and no notice period — tell me before the next payment date and there
> isn't one.
>
> What I won't do is guarantee an outcome. Nobody controls what an AI assistant
> says, including me. I work on the inputs these systems demonstrably rely on, I
> measure what happens, and I show you numbers you can check yourself.
>
> One person does the work. Email Noven and you're emailing me.
>
> Based on the Wirral, working with clients across the UK.
>
> `[HOLD until the site is live]` More at novenstudio.co.uk — or ask me here,
> DMs are open.

### Notes on why it's written this way

- **Every fact in it is already in `site/src/data/business.ts`** — the prices,
  the cancellation terms, the Wirral, one person doing the work. Nothing new is
  claimed. If a price changes, it changes in both places or neither.
- **No industry jargon, per the standing rules.** No three-letter acronyms, no
  "leverage", no "solutions". A busy business owner reads it and knows what
  they'd be buying.
- **The refusal to guarantee is a selling point, not a disclaimer.** It's the
  same position the site takes, and it's the sentence that separates us from
  everyone in this category promising rankings.
- **It doesn't mention Port Brief.** Confirmed finished by the owner, and no
  reference to it stays anywhere. See the sweep in section 3.4 — it is almost
  certainly in more than one place on the profile.

---

## 3. Profile changes, in order

### 3.1 Headline (220 characters) — use this one

The headline is the line directly under your name. It follows you everywhere on
LinkedIn — every comment, every search result, every connection request — so it
does more work than the About section most people never scroll to.

**Use this:**

> Founder of Noven — I help UK service businesses get found when their
> customers ask an AI who to use. Eight years in global shipping operations
> before this.

154 characters, inside the 220 limit.

**Why this one.** The shipping line is doing real work, not decoration. You are
a one-person business nobody has heard of, selling something most prospects
haven't bought before — the eight years is the reason a stranger reads the next
sentence instead of closing the tab. It also survives the check, now that the
number is right.

If you want it shorter, cut the second sentence, not the first. But the version
with it is stronger while Noven is unknown, which is the whole of the next year.

The site rules ban buzzwords and stacked keyword tags, and LinkedIn headlines
are where those breed — no `Founder | Consultant | Speaker |` chains, no
"passionate about". One sentence saying what you do for whom.

### 3.2 Add Noven as your current position

This is the change that actually closes the gap and makes the profile say you
run Noven. **Do it after the company page exists**, so LinkedIn attaches the
real page and its logo rather than creating a loose text entry.

| Field | Value |
|---|---|
| Title | Founder |
| Employment type | Self-employed |
| Company | Noven *(pick the page from the dropdown — don't free-type it)* |
| Start date | The month you started working on Noven — see below |
| Currently in this role | Yes |
| Location | Wirral, England, United Kingdom |
| Location type | Remote |

**"Pre-launch" isn't the same as "no start date."** You said there isn't a real
start date yet because Noven hasn't launched. But a business starts when you
start doing the work, not when the website goes live — every founder's start
date predates their launch, and nobody reads it as a launch announcement. So
use **the month you began working on Noven**: deciding to do it, buying
`novenstudio.co.uk`, starting to build. The repo's first commit is 25 July
2026, so July 2026 is the latest it could honestly be; if the domain or the
decision came earlier, use that month instead. You know which — I don't, and
it isn't mine to pick.

**One consequence worth seeing before you set it.** You left Maersk in June
2025. If Noven starts July 2026, the profile shows a thirteen-month gap. Three
things to say about that:

- **It matters much less than you'd think here.** A gap is a hiring signal. You
  aren't job hunting — you're being looked up by a prospect who wants to know
  if you're real and if you know anything. Nothing about a gap answers no to
  either.
- **Don't paper over it.** No stretched dates, no invented consultancy. The one
  asset this business has is that everything on it survives checking.
- **If Noven genuinely started earlier than July 2026, use that date** and most
  of the gap closes honestly on its own.

Description:

> Noven helps service businesses get found and recommended when their customers
> ask an AI assistant — ChatGPT, Google, Copilot or Perplexity — who to use.
>
> Most of what decides that is unglamorous and fixable: whether these systems
> can read your website at all, whether the facts about your business agree with
> each other everywhere they appear, and whether anything you've published
> answers the questions your customers are actually asking.
>
> I audit what the assistants currently say about a business, fix what's in the
> way, and then check it on a schedule and write down what changed. Plain
> reports, round-number prices, and no guarantees about things nobody controls.
>
> Working with accountants, solicitors, clinics, consultancies and agencies
> across the UK, remotely.

### 3.3 The missing one — Global Customer Experience Consultant

**A.P. Moller – Maersk · Sep 2024 – Jun 2025 · 10 mos**

This is the most senior thing on your profile and it's currently blank, which
means the strongest role you've held is invisible to a reader skimming, and to
any assistant reading the page. Written from what you gave me:

> Global operational lead for Marks & Spencer and Tesco, owning their worldwide
> cargo end to end.
>
> • Owning the whole process globally, start to finish — one point of
> accountability across every region the cargo moved through, instead of a
> handover at each border and nobody holding the middle.
>
> • Ensuring every export requirement was met at origin, working directly with
> Maersk colleagues in the origin countries and with the customers' own freight
> forwarders, so cargo left correct the first time rather than being fixed in
> transit.
>
> • Ensuring every import requirement was met at the other end, so containers
> cleared and ran into the customers' distribution centres without being held.
>
> • Owning the process an administrative team of around six worked to across
> both accounts. Where something needed changing or raising, I set out what the
> change was and made sure it was carried through, escalating missed steps to
> their line manager.
>
> • Reporting directly to the customers on a regular basis, so they heard about
> an exception from me before they found it themselves.

**A note on the team bullet, because the wording is deliberate.** You told me
you didn't line-manage them — around six admin staff sat under your purview,
you owned the process they worked to, and escalation for missed steps went to
their own manager. So the bullet says that, and doesn't say "managed a team of
six." It would be an easy word to reach for and it would be untrue, on a
profile whose whole argument is that you keep information accurate. Process
authority over a team you don't line-manage is a real and senior thing to have
had; it doesn't need upgrading to sound like one.

**The client names are confirmed** — the owner has cleared naming M&S and
Tesco, so the copy above stands as written. Keep them. They are the single most
persuasive detail in your entire work history: "two major retailers" is a
fraction as strong, and specific, checkable names are exactly the kind of fact
this business claims to care about.

**One thing left to decide: the format.** Your older entries open with "Key
responsibilities
include;" and then bullet. This one doesn't — it opens with what the job *was*,
then evidences it. That's the stronger read, and it's what I'd keep. If you'd
rather all four entries matched, the fix is to bring the older ones up to this
format rather than take this one down to theirs.

**Note the tense.** This role ended, so it's past tense throughout. Your Sep
2023 entry is written in the present tense ("Acting as…", "Managing…") for a
role that also ended — worth changing when you're in there. Same for both older
entries, which say "my role **is** to act as".

---

### 3.4 Remove Port Brief — everywhere, not just the About section

Confirmed finished. Replacing the About section deletes the most visible
mention, but LinkedIn scatters things, and a half-removed project is worse than
a fully present one: it leaves a live-looking promise with nobody behind it.

**Check all seven of these before you close the tab:**

1. **About** — handled by section 2's replacement copy.
2. **Headline** — replaced in 3.1. Check the old one didn't name it.
3. **Featured** — the most likely leftover. A pinned link or newsletter card
   sits there quietly and survives every other edit. Unpin it.
4. **Experience** — if Port Brief has its own entry, delete it. Since it's
   finished with nothing to show, an end-dated entry isn't worth the questions
   it invites.
5. **Contact info → Website** — if it points at `portbrief.co.uk`, clear it.
   This is the one that actively misroutes people.
6. **The LinkedIn newsletter, if you created one.** These don't disappear with
   the About text; they keep their own page and their own subscriber list, and
   subscribers keep expecting Tuesdays. If one exists, delete it properly
   rather than abandoning it.
7. **Recent posts and any pinned post** — a pin promoting a dead subscription
   is the same problem as the About paragraph.

**And outside LinkedIn:** if `portbrief.co.uk` still resolves, decide what it
does now. A live site for a finished project is a second thing contradicting
you, which is precisely the fault the audit is paid to find on other people's
businesses. Either redirect it to Noven once the site is deployed, or take it
down. Either is fine; leaving it running unattended isn't.

There is nothing about Port Brief anywhere in this repo or on the Noven site —
already checked.

---

## 4. Fixes to what's already there

### 4.1 Senior Customer Experience Consultant (Sep 2023 – Aug 2024)

The content is fine. Two mechanical fixes:

- **Line breaks are landing mid-sentence** — "clients who need further
  assistance with their ⏎ supply chain and to optimise their booking process".
  That's hard wrapping pasted in from a CV. Delete the stray breaks so each
  bullet is one paragraph and wraps naturally on a phone.
- **"Acting as a matter expert"** should be "subject matter expert".
- Past tense, as above.

### 4.2 Sealand and Seago Line — the broken bullet characters

Both descriptions render every bullet as **`?`** in a box. That's a character
LinkedIn can't display — almost certainly Wingdings or a Word symbol that came
across when the text was pasted from a CV. On a recruiter's phone it reads as
five question marks down the left margin of your longest role.

**Fix:** select each description, delete it entirely, and retype the bullets
using a plain bullet `•` typed directly into LinkedIn, or a simple hyphen `-`.
Don't paste from Word again — paste into a plain text editor first if you're
copying from anywhere.

While you're in the Sealand entry, "**value protection**" is Maersk's internal
name for cargo insurance. Outside Maersk nobody knows what it means. Consider
"cargo insurance" instead — same fix in spirit as everything else in this
document.

### 4.3 Top skills

**"Frieght Management"** is misspelled. It's the first skill listed, on the
profile of someone whose business is making sure a company's information is
accurate and consistent. Delete and re-add as "Freight Management".

### 4.4 Contact info

- **Website:** `[HOLD until the site is live]` — then add
  `https://novenstudio.co.uk` with the label "Company".
- The site's structured data already claims your profile and Noven are the same
  person, via `founderLinkedIn`. Once the website field points back at the site,
  that claim is confirmed from both ends, which is a materially stronger signal
  than one page asserting it alone.

### 4.5 Featured section

Once the site is live, pin the **How it works** page as a Featured link rather
than the homepage. Someone who's just read your About already knows what Noven
does; the useful next click is what actually happens and what it costs.

---

## 5. The Noven company page

### 5.1 Why bother

A company page is a second, independently checkable source an assistant can
find and quote when someone asks who Noven is. It also means that when a
prospect looks Noven up after your email — and they will — they find a page
rather than nothing.

**A near-empty page is still better than no page.** Don't wait for launch.

### 5.2 Creating it

On desktop: the **For Business** grid, top right → **Create a Company Page** →
**Company**. Then:

| Field | Value | Notes |
|---|---|---|
| Name | `Noven` | Exactly as on the site — not "Noven Studio", not "Noven UK" |
| LinkedIn public URL | `linkedin.com/company/noven` | Almost certainly taken. Fallbacks in preference order: `noven-uk`, `novenstudio`, `noven-studio`. **Whichever you get is permanent-ish and goes into the repo — write it down** |
| Website | `[HOLD until the site is live]` → `https://novenstudio.co.uk` | Leave blank until the domain serves the new site |
| Industry | **Marketing Services** | The closest honest fit LinkedIn offers. "Advertising Services" oversells it; "Business Consulting and Services" undersells it |
| Company size | 1 employee | True. Say it plainly — it's on the site too |
| Company type | Self-employed | Matches "trading name of Kieran Smith, a sole trader" |
| Tagline (120 chars) | `Get found when your customers ask an AI who to use.` | 51 characters. Shows under the name everywhere the page appears |

Then tick the verification box confirming you're authorised to create it.

### 5.3 Location — read this one carefully

LinkedIn will offer to add a location with a street address. **Set the city
only — Wirral (or Birkenhead), England, United Kingdom. Do not enter the home
address.**

This is the same decision the roadmap already made for the site footer, and for
the same reason: a company page is crawled, cached, repeated by assistants and
scraped by anything that harvests business listings. A home address published
there is a one-way door — the page can be edited later, the archives and caches
can't. When the service address in roadmap 1c exists, add it here then.

### 5.4 About / Overview (2,000 characters)

The opening sentence is **verbatim** from `business.description` in
`site/src/data/business.ts`. That's the point — the site, the structured data
and this page all say the identical thing, so nothing an assistant reads can
contradict anything else it reads.

> Noven helps service businesses get found and recommended when their customers
> ask AI assistants — ChatGPT, Google, Copilot and Perplexity — who to use.
>
> More and more people ask an assistant for a recommendation instead of
> scrolling through search results. If the assistant doesn't know a business
> exists, it doesn't get mentioned, and the work quietly goes to a competitor
> who does show up.
>
> What decides that is mostly unglamorous and fixable: whether these systems can
> read your website, whether the facts about your business agree with each other
> everywhere they appear, and whether anything you've published answers the
> questions your customers actually ask. Almost no small firm has ever had this
> looked at.
>
> Noven does that work, at prices a small firm can justify.
>
> • Audit — £30, one-off. A written report on what the assistants say about you
> today, and what's in the way.
>
> • Foundation — £350, one-off. The setup that makes your business readable to
> these systems.
>
> • From £75 a month. Your customers' questions put to the assistants on a
> schedule, with a written record of where you appeared and where you didn't.
> Business facts kept current and corrected when they drift. No minimum term and
> no notice period.
>
> We don't guarantee outcomes — nobody controls what an AI assistant says. We
> work on the inputs these systems demonstrably rely on, we measure what
> happens, and we don't show numbers that can't be checked.
>
> Noven is run by Kieran Smith from the Wirral, and works with clients across
> the United Kingdom, remotely. One person does the work — when you email Noven,
> you're emailing him, and the report you get back is one he wrote.
>
> Noven is a trading name of Kieran Smith, a sole trader.
> hello@novenstudio.co.uk

That's roughly 1,750 characters, leaving room.

### 5.5 Images — both need exporting first

**LinkedIn will not accept SVG**, and every brand asset in `assets/brand/` is
an SVG. Two exports needed:

| Asset | Source | Export to | Notes |
|---|---|---|---|
| Logo | `assets/brand/Social Avatar.svg` (2000×2000) | **PNG, 400×400** | Square, min 300×300, max 8MB. Displays as a circle — the source already accounts for that |
| Cover | `assets/brand/Email Banner.svg` | **PNG, 1128×191** | The email banner is a different aspect ratio, so it needs re-composing, not just resizing. `assets/brand/Brand Pattern.svg` cropped to the strip is the safer option |

Per the standing rules: **export the committed assets, don't redraw them.** If
the cover can't be made from what exists without redrawing, leave it blank —
LinkedIn's default is a plain colour block and looks like nothing at all, which
is fine. `[PLACEHOLDER: confirm which cover treatment you want]`

### 5.6 After the page exists — one repo change

Set the page URL in `site/src/data/business.ts`:

```ts
businessLinkedIn: 'https://www.linkedin.com/company/<your-slug>/' as string | null,
```

It's already wired to join the Organization's structured data as `sameAs`, so
setting the value is the only step — nothing else needs touching.

**Same two rules that applied to `founderLinkedIn`:**

1. **Strip any `?utm_…` tracking parameters.** LinkedIn's share links carry
   them. They describe how a link was shared, not the business, and they'd be
   published verbatim in the JSON-LD.
2. **Never a URL containing `loginToken`, `authToken`, `session` or similar.**
   This value goes on a public page, into a public repo, and into markup built
   for crawlers to ingest — the worst available place to put a credential.

Then do the two-minute check: **open the page URL in a private window.** If it
loads without a login prompt, it's publicly visible, which is the entire point
of publishing it. If it prompts, the page isn't public yet.

### 5.7 First posts, so it isn't a ghost town

Three is enough to make the page look alive. Suggestions, not copy — these
should sound like you:

1. **What Noven is and why it exists.** Roughly your About section, shorter.
2. **A real example.** Ask an assistant "who's a good [trade] in [town]?" and
   post what came back and what the named businesses had in common. Costs you
   ten minutes and it's the most convincing thing you could post.
3. **One thing any business can check itself.** A genuinely useful freebie
   builds more trust at this stage than a pitch does.

**Never invent a client, a result or a statistic**, including in a post. If a
post needs a number you don't have, it isn't ready.

---

## 6. Questions — all answered, 2026-07-29

Every one is applied above. Nothing here is waiting on you; the list is kept
so the reasoning behind the copy is on the record.

| Question | Answer | Where it landed |
|---|---|---|
| How long in shipping? | Eight years nine months | "Eight years" everywhere; site and `service-tiers.md` corrected — §1 |
| How many staff managed? | Around six, **not** line-managed | Bullet rewritten as process authority — §3.3 |
| When did Noven start? | Pre-launch, no launch date | Use the month work began, not launch — §3.2 |
| Can M&S and Tesco be named? | Yes | Names kept; unnamed variant dropped — §3.3 |
| Why did Maersk end? | Resigned | Nothing needed on the profile; the gap is addressed in §3.2 |
| Is Port Brief finished? | Yes — no reference anywhere | Seven-place removal sweep — §3.4 |
| Current headline? | — | Replacement written and chosen outright — §3.1 |

**One decision left, and it's a preference not a fact:** whether to reformat
the three older job descriptions to match the new one's style, or leave them.
Section 3.3 explains the trade-off. Nothing blocks you either way.

**One date question that isn't mine to answer.** The profile shows Sealand
running **Oct 2018 – Feb 2024** while the Maersk role starts **Sep 2023** — a
six-month overlap. If that was a real transition period, it's fine and needs no
change. If one of the dates is wrong, fix it: overlapping dates are exactly the
kind of small contradiction that makes a careful reader — or an assistant
summarising your history — hedge.

---

## 7. Consistency check — run this when everything's live

The single test that matters: **does every source say the same thing?** Open
the site and both LinkedIn pages side by side and confirm each row matches
exactly.

| Fact | Must read | Sources that must agree |
|---|---|---|
| Business name | Noven | Site, company page, your current role |
| What it does | The `business.description` sentence, word for word | Site JSON-LD, company page About, your About |
| Location | Wirral, UK — city level, never a street | Site, company page, your role location |
| Area served | United Kingdom | Site, company page About, your role description |
| Email | hello@novenstudio.co.uk | Site contact page, company page About |
| Legal status | Trading name of Kieran Smith, a sole trader | Site footer, company page About |
| Prices | £30 / £350 / £75 / £125 / £250 | Site pricing page, both About sections |
| Cancellation | No minimum term, no notice period | Site (three places), both About sections |
| Website | `https://novenstudio.co.uk` — **only once it serves the Noven site** | Company page, your contact info |
| Founder → business | Profile links to the page; page links to the site; site's `sameAs` links back to both | All three |

If a row disagrees, fix it in `site/src/data/business.ts` first and propagate
outward. That file is the single source of truth by design, and the homepage
says so out loud — so it has to stay true of us before we charge anyone to make
it true of them.
