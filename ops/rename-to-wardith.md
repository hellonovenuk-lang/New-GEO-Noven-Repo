# Noven → Wardith: the full rename

**Internal document.** Written 2026-08-04, the day the name was decided and the
domains bought. This is the complete list of what has to change, in the order it
has to change, and what breaks if it is done in a different order.

**The decision itself is settled** — see `ops/session-log.md`, 2026-08-04, and
`ROADMAP.md` 1c-2. Nothing here reopens it. This document is only the doing.

**Three domains are held:** `wardith.co.uk`, `wardith.com`, `wardith.uk`, bought
at GoDaddy on 2026-08-04, **one year only**. Extending them is in the calendar
for 6 Oct 2026 with a backstop on 4 Jun 2027, and in `ops/accounts.md`.

---

## The one thing to understand before starting

**This is not a find-and-replace, and it is not reversible in the way a normal
site edit is.** `CLAUDE.md` says merging to `main` publishes into the JSON-LD the
assistants read, and that caches and third-party copies persist long after an
edit. A rename changes the `name`, the `url`, both `sameAs` links and the
`Organization` identity all at once. Done in one clean switch it is a single
event the assistants can learn. Done in dribs over three weeks it publishes a
business whose own facts disagree with each other — **which is the exact failure
we sell finding.**

So: do all the preparation on a branch, verify the build, and switch once.

## The good news, and it is real

**There is almost nothing to lose by moving domain.** The self-audit found that
not one of 210 automated answers cited `novenstudio.co.uk`, and that Copilot has
no record of the site at all because Bing never indexed it. The usual argument
against a domain move — years of accumulated indexation and links — **does not
apply to this business.** There is no equity to forfeit.

This is the cheapest moment this change will ever be. It gets more expensive
every week from here.

---

## Phase A — decisions and deadlines. Do these first, this week

- [ ] **A1. Decide which domain the business actually *is*.** Everything below
      depends on this one answer and nothing can start without it. The site
      canonical, the sitemap, the `url` in the structured data, the email
      address and both LinkedIn links must all be the same domain, or we
      publish the inconsistency we charge to find.
      **Recommendation: `wardith.co.uk`.** It follows what has already been
      done, and it reads local to the Wirral service businesses being sold to.
      Hold `.com` and `.uk` as defensive registrations pointed at it — owned,
      redirecting, never used as an address.
- [ ] **A2. The ICO call is on 10 August and the trading name is the same
      call.** `HANDOVER.md` section 4 already has this as the one item with a
      deadline and no undo — the home address publishes to a bulk-downloadable
      register within seven working days of the 30 July payment. Registration
      **C1995412**. While on the phone, ask what the registration records as the
      trading name and what changing it involves. One call, two problems.
      Do not let the rename delay this call; the address is the urgent half.
- [ ] **A3. Confirm auto-renew is ON for all three new domains, today.** It is
      the safety net behind both calendar reminders. `ops/accounts.md` rates a
      domain lapse as total outage.
- [ ] **A4. Find out when `novenstudio.co.uk` expires, and who it is with.**
      Currently `[PLACEHOLDER]` in `ops/accounts.md` and it has just become far
      more important: **that domain now has to outlive the rename by years**,
      because it carries the redirects. If it lapses, every redirect dies at
      once and the old name is free for somebody else to buy — including the
      `noven.studio` product working in the same field.
      **Keep it registered for at least three years. Do not drop it.**
- [ ] **A5. Decide where DNS lives.** `novenstudio.co.uk` is at Namecheap; the
      new three are at GoDaddy. Two registrars means two renewal dates, two
      logins and two places to forget. Not urgent, but decide it before writing
      records twice. The transfer lock on the new domains lifts ~3 Oct 2026.

---

## Phase B — brand assets. **Read B1 before you start drawing**

- [ ] **B1. The asset pack cannot be retyped, and this changes your plan.**
      Checked 2026-08-04: **every one of the six SVGs in `assets/brand/` is
      outlined vector paths. Zero `<text>` elements, no `font-family` anywhere.**

      | File | Paths | What that means |
      |---|---|---|
      | `Logo Primary.svg` | 6 | Letterforms are shapes, not text |
      | `Logo Dark.svg` | 6 | Same |
      | `Favicon.svg` | 2 | Likely a monogram — see B3 |
      | `Social Avatar.svg` | 5 | Same |
      | `Email Banner.svg` | 45 | Wordmark plus layout |
      | `Brand Pattern.svg` | 50 | May be name-free — check |

      "Same pack, different words" is the right instinct and it will save real
      money, but it cannot be done by editing these files. Opening them and
      typing WARDITH produces letters in whatever font your editor defaults to,
      sitting next to letters drawn by a designer. That is exactly the mismatch
      `CLAUDE.md` bans — it is the same fault as the Inter-retyped wordmark
      caught on 27 July, arriving through a different door.

- [ ] **B2. Get the editable original or identify the typeface.**
      `ops/accounts.md` records a second repo, **`hellonovenuk-lang/Noven`**,
      holding brand and image originals. Look there first — if the source file
      exists, this is a twenty-minute job. If not, identify the typeface from
      the outlines (WhatTheFont or similar on a clean render of `Logo
      Primary.svg`) and set WARDITH in the real font, then outline it. Either
      route keeps the letterforms honest. Guessing does not.
- [ ] **B3. The monogram is a redraw, not a rename.** `Favicon.svg` is two paths
      and `Social Avatar.svg` is five. If either contains an **N**, it has to
      become a **W** — a different letter, different width, different optical
      weight in a circle. Budget for this as drawing work. The favicon is the
      one asset already confirmed to work at 16px and 32px, light and dark
      chrome, so whatever replaces it has to clear the same bar.
- [ ] **B4. Seven letters where there were five. The lockup gets wider.**
      `site/src/layouts/Base.astro` hard-codes the wordmark's dimensions in two
      places — line 88 (`width="1066" height="236"`) and line 164
      (`width="1194" height="236"`). At the same cap height WARDITH is roughly
      40% wider. **Those numbers must be updated to the new artwork's real
      viewBox or the logo renders squashed**, and the header will need a look on
      a narrow phone where the extra width has nowhere to go.
- [ ] **B5. Rebuild `site/public/og.png` at 1200×630.** It is a raster and it
      carries the name. Nothing else will regenerate it.
- [ ] **B6. Keep the originals untouched.** New masters go into `assets/brand/`
      unmodified; trimmed web copies (viewBox only, no path data altered) go to
      `site/public/`, exactly as the Noven set was handled. The old Noven files
      stay in git history — do not delete the record.
- [ ] **B7. The email banner's wording has been outstanding since 27 July.**
      "AI Visibility Services" still needs rewording and it is being redrawn
      anyway. Fix it in the same pass rather than reproducing a known fault.

**Not affected, checked:** the hero animation. `assets/video/frame.html` uses
generic captions and abstract blocks — no business name appears in it. Only the
*filename* carries the old name (`noven-answer.mp4` / `.webm`), referenced at
`site/src/pages/index.astro:60-61`. Rename the files and the two lines. **No
re-render needed.**

---

## Phase C — the repo, on a branch, as one change

Do this whole phase before anything is published. `business.ts` first: it is the
single source of truth and most of the rest follows from it.

- [ ] **C1. `site/src/data/business.ts`** — seven lines. `name` (10),
      `legalNote` (11 — "Wardith is a trading name of Kieran Smith, a sole
      trader"), `email` (13), `description` (20), the comment at 48–52, and
      `businessLinkedIn` (57). **The LinkedIn slug will change — do not update
      line 57 until the LinkedIn page has actually been renamed and the new URL
      confirmed**, or the structured data publishes a `sameAs` pointing nowhere.
- [ ] **C2. `site/astro.config.mjs:8`** — `site:` drives every canonical and the
      whole sitemap. One line, largest blast radius in the repo.
- [ ] **C3. `site/public/robots.txt`** — line 1 comment, line 44 sitemap URL.
- [ ] **C4. `site/src/layouts/Base.astro`** — line 62 (meta description), lines
      88 and 164 (logo `alt` text and the dimensions from B4).
- [ ] **C5. The seven pages.** `index.astro` (12 references), `faq.astro` (9),
      `about.astro` (8), `pricing.astro` (6), `how-it-works.astro` (4),
      `contact.astro` (2), `404.astro` (2). Read each — these are body copy, not
      config, and some will need rewriting rather than substituting.
- [ ] **C6. The small ones.** `site/package.json:2` (`"name": "noven-site"`),
      `site/package-lock.json` (2, follows automatically on install),
      `site/README.md` (2), `site/src/styles/global.css:1` (a comment).
- [ ] **C7. Rename the video files and their two references** (see Phase B).
- [ ] **C8. Verify the `json-code.ts` invariant still holds.** `CLAUDE.md` flags
      this specifically: the homepage's visible code block must stay
      byte-for-byte identical to the JSON-LD in `<head>`. It is the site's
      central proof and the rename touches everything it renders. **Check it
      explicitly rather than assuming.**
- [ ] **C9. Build and read the output, not the source.** Seven pages plus
      sitemap. Confirm: every canonical is the new domain, the sitemap lists the
      new domain, the JSON-LD `name` and `url` are new, and the five offers are
      **unchanged** at 125 / 750 / 95 / 250 / 495. A rename must not move a
      price by accident.
- [ ] **C10. Update the ops documents.** `novenstudio.co.uk` appears in
      `HANDOVER.md`, `README.md`, `ROADMAP.md`, `ops/README.md`,
      `ops/accounts.md`, `ops/audit-setup.md`, `ops/linkedin.md`,
      `ops/own-facts-check.md`, `ops/third-party-services.md` and
      `ops/zoho-mail-setup.md`. **Leave the audit folder alone** —
      `ops/audits/noven-2026-08-02/` is a dated historical record and rewriting
      it would destroy the baseline. Same rule as the repricing: correct what
      claims to be current, never what is correctly dated history.

---

## Phase D — the switch. This is the publishing moment

- [ ] **D1. Netlify: add the new domain, set it primary, keep the old one
      attached.** Do not detach `novenstudio.co.uk` — it has to stay bound to
      serve the redirects.
- [ ] **D2. DNS at the new registrar** — A/CNAME for Netlify, then wait for TLS
      to issue on all three new domains before switching anything.
- [ ] **D3. 301 redirects, page for page.** `/pricing` → `/pricing`, not
      everything to the homepage. Seven pages plus the 404. Redirect
      `.com` and `.uk` to the primary domain too, so only one address ever
      resolves content.
- [ ] **D4. Say what the merge publishes, then merge.** Per `CLAUDE.md`: this
      one publishes a new business name, a new URL on every page, new JSON-LD
      identity and two new `sameAs` links. It is the largest one-way door this
      repo has opened. Everything in Phase C should be verified before it.

---

## Phase E — mail

- [ ] **E1. Add the new domain in Zoho** — `ops/zoho-mail-setup.md` is a
      step-by-step for exactly this job on the old domain. Reuse it; the
      Namecheap-specific quirks in it apply to whichever panel you end up in.
      **Stay on Zoho.** `ops/third-party-services.md` A1 already rejected
      Microsoft 365 and Google Workspace, and the rename does not change that
      argument.
- [ ] **E2. Create `hello@wardith.co.uk`** as the licensed user. Aliases are
      free; second users are not.
- [ ] **E3. Keep `hello@novenstudio.co.uk` receiving for at least 12 months.**
      It is the address published on both LinkedIn pages, in the ICO record and
      in whatever has already been cached. Mail to it must not bounce.
- [ ] **E4. The signature.** `ops/own-facts-check.md` row 10 records that nobody
      knows what the signature says or whether it quotes a price. Find out and
      fix it in the same pass.
- [ ] **E5. Fix Zoho's recovery address while you are in there.** Owed since
      29 July: recovery currently points at the mailbox it protects, so a
      lockout is unrecoverable. Five minutes.

---

## Phase F — every external surface

Worked from the register in `ops/own-facts-check.md` section 3. **After the
switch, that register needs re-running in full** — this is precisely the trigger
its section 6 describes.

- [ ] **F1. LinkedIn company page — name and URL slug.** Both. The slug is
      published in our own structured data as `sameAs`, so the old URL dies the
      moment it changes. **Do this inside the same window as the site switch**,
      and confirm the new URL before setting `business.ts` line 57 (C1).
- [ ] **F2. LinkedIn company page About** — still publishing the pre-31-July
      prices (£30 / £350 / from £75). Repaste from `ops/linkedin.md` §5.4 with
      the new name. Two jobs, one paste.
- [ ] **F3. LinkedIn founder profile About** — same, from `ops/linkedin.md` §2.
- [ ] **F4. Google Search Console.** The new domain is a **new property** — add
      and verify it, submit the new sitemap, then use the **Change of Address**
      tool, which requires the D3 redirects to already be live. Keep the old
      property; do not delete it.
- [ ] **F5. Bing Webmaster Tools.** Still not set up, and it was already a
      finding. A brand-new domain with no history makes it more urgent, not
      less — Copilot answers from Bing.
- [ ] **F6. Zoho Books** — trading name on invoices and any invoice template.
- [ ] **F7. Revolut Pro** — the trading name shown on the audit payment link and
      whatever a customer sees on their statement.
- [ ] **F8. The ICO record** (A2), once the address question is settled.
- [ ] **F9. This repo's own name** and `hellonovenuk-lang/Noven`. Cosmetic, but
      do it before it becomes archaeology.
- [ ] **F10. Leave `hello.noven.uk@gmail.com` alone.** It carries the old name
      and it should. It is an *identity*, not a brand surface — it owns the
      GitHub login, the Search Console property and Netlify's notifications, and
      renaming or replacing it risks all three at once for no outward gain.
      Note the deliberate mismatch in `ops/accounts.md` so nobody "tidies" it.

---

## Phase G — after

- [ ] **G1. Re-run `ops/own-facts-check.md` end to end** and record the date.
- [ ] **G2. Decide what happens to the self-audit baseline, because the rename
      partly breaks it.** `ops/audits/noven-2026-08-02/` froze questions q06 and
      q07 as *"what do the assistants know about Noven"*. Under a new name the
      honest answer will be "nothing" for months, and that is not a comparison —
      it is a different question.

      **The way to keep it valuable is to run both.** At the six-month re-check,
      ask the frozen Noven questions *and* the same questions about Wardith. The
      first measures **how long a dead name persists**; the second measures **how
      fast a new one is learned.** Nobody else has that measurement, it costs one
      extra batch of queries, and it is the single most useful piece of evidence
      this business could own — the product's own claim, tested on the only
      business we are allowed to experiment on. Fold the decision into
      `ops/audit-method.md` before the re-check, not after.
- [ ] **G3. Expect both names in the world at once, for months.** That is not a
      fault and it does not need fixing beyond the redirects. `own-facts-check.md`
      section 1 already explains why: correcting the sources we control is the
      only lever, and the lag afterwards is real.

---

## What is not known, and has to be looked up

- `[PLACEHOLDER: novenstudio.co.uk registrar, expiry date, auto-renew status]`
  — A4, and now load-bearing.
- `[PLACEHOLDER: whether the ICO record names a trading name at all, and what
  changing it costs]` — A2.
- `[PLACEHOLDER: whether the brand originals in hellonovenuk-lang/Noven include
  an editable wordmark, or only exported SVGs]` — B2, and it decides whether the
  logo is a twenty-minute job or a drawing job.
- `[PLACEHOLDER: what the Zoho email signature currently says]` — E4.
