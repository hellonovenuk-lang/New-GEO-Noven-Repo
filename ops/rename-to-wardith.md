# Noven → Wardith: the full rename

**Internal document.** Written 2026-08-04, the day the name was decided and the
domains bought. This is the complete list of what has to change, in the order it
has to change, and what breaks if it is done in a different order.

**The decision itself is settled** — see `ops/session-log.md`, 2026-08-04, and
`ROADMAP.md` 1c-2. Nothing here reopens it. This document is only the doing.

**Three domains are held:** `wardith.co.uk`, `wardith.com`, `wardith.uk`, bought
at GoDaddy on 2026-08-04, **one year only**. Extending them is in the calendar
for 6 Oct 2026 with a backstop on 4 Jun 2027, and in `ops/accounts.md`.

**The business is `wardith.co.uk`** — decided by the owner 2026-08-04, see A1.

**This work is under a spending freeze until 26 August**, and a deadline of
1 September to be operational. See `ops/plan-to-1-september.md`. Nothing in
this document costs anything: the domains are bought and every remaining step
is free. If a screen asks for payment, something is wrong — stop and say so.

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

- [x] **A1. DECIDED 2026-08-04: the business is `wardith.co.uk`.** Owner's
      call. Everything below now has its answer.

      **What that means, concretely.** `wardith.co.uk` is the only address that
      ever appears as *an address*: the site canonical, the sitemap, the `url`
      in the structured data, `hello@wardith.co.uk`, both LinkedIn links, the
      invoice footer, the email signature. `wardith.com` and `wardith.uk` are
      **owned and redirecting, and are never typed anywhere as a contact
      detail.** They exist so that nobody else has them and so a mistyped
      address still lands.

      Why it was the right call: it follows what has already been done, and it
      reads local to the Wirral service businesses being sold to.

      **Consequence: `Email Signature.svg` must be re-exported.** It reads
      `hello@wardith.com` above `wardith.co.uk` — two different domains for one
      business, in the asset that goes out on every message. It is the only
      asset in the set carrying a domain. **Do not use it until it is
      re-exported on `wardith.co.uk` for both lines.**
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

## Phase B — brand assets. **Mostly done: the set landed 2026-08-04**

**The Wardith set is in.** Six SVGs from the renamed Canva project, installed as
originals in `assets/brand/` and trimmed into `site/public/`. The wordmark is
**"Wardith."** — title case with a full stop, navy `#170969` on light and warm
white `#fffefa` on dark, both exactly on-brand. The monogram is **"W."**. Both
logos measure 1298×238 after trimming; `Base.astro` lines 88 and 164 are updated
from the old 1066/1194×236, and the wordmark renders correctly in the header on
warm white and the footer on navy.

| Canva file | Installed as | Web copy |
|---|---|---|
| `1.svg` (navy) | `assets/brand/Logo Primary.svg` | `site/public/logo.svg` |
| `Logo - Dark Mode.svg` | `assets/brand/Logo Dark.svg` | `site/public/logo-dark.svg` |
| `Favicon.svg` (navy W.) | `assets/brand/Favicon.svg` | `site/public/favicon.svg` |
| `Icon Mark.svg` (white W.) | `assets/brand/Icon Mark.svg` | not used on the site |
| `Email Signature.svg` | `assets/brand/Email Signature.svg` | not used on the site |
| `LinkedIn Banner.svg` | `assets/brand/LinkedIn Banner.svg` | not used on the site |

**Still outstanding after the drop:**

- [x] **`og.png` — done 2026-08-04, and it was never a Canva job.** Corrected
      the same day it was raised: `assets/og/og.html` composes the card from
      the site's own materials and *references* `site/public/logo-dark.svg`,
      which is already the Wardith wordmark. Re-rendering it picked the new
      artwork up automatically. The only edit needed was the `.wordmark`
      height, which is derived from the wordmark's own viewBox ratio and was
      still on Noven's `1193.92 : 236.39`. Left alone it would have squashed
      the new mark rather than failed — so **re-derive that number any time the
      wordmark is re-exported.**

      Same for the two LinkedIn PNGs, which are build products of
      `assets/linkedin/`. `cover.html` needed the same ratio fix.
      **`logo.html` was broken outright** — it placed `Social Avatar.svg`,
      which the new set does not include and which was deleted with the Noven
      originals. It now sets the navy disc in CSS and places the supplied
      `Icon Mark.svg` on it, exactly the way `og.html` already puts the
      committed wordmark on a navy field. Re-checked legible at 48px on white
      and on a dark feed, because a W is a busier letterform than an N and the
      old test does not transfer.
- [ ] **There is no Brand Pattern in the new set.** The Noven pack had one. It
      was never used on the site, so nothing breaks — but decide whether it is
      dropped deliberately or was missed in the export.
- [ ] **The favicon needs a proper answer for dark browser chrome — see B3.**

---

### The one thing in the new set that contradicts a decision not yet made

**`Email Signature.svg` says `hello@wardith.com` on one line and `wardith.co.uk`
on the next.** Two different domains, in one asset, for one business.

That is the A1 decision being made by accident, and made inconsistently. It is
also — precisely — the failure this business is sold to find in other people's
businesses: contact details that disagree with each other across surfaces. An
email signature is a high-frequency surface; it goes out on every message and
gets pasted into other people's address books.

**Settle A1 first, then re-export the signature on one domain.** The
recommendation there is unchanged: `wardith.co.uk` for both, with `.com` and
`.uk` owned and redirecting. Nothing else in the set carries a domain, so this
is the only asset affected.

---

## Phase B (original notes) — **B1 is now historical, kept for the reasoning**

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

- [ ] **B2. Resolved 2026-08-04: the editable original is the Canva project.**
      The owner made the Noven assets in Canva and is renaming inside the same
      project. **That is the answer B1 needed** — and it explains B1: Canva
      outlines text on SVG export, so the flat paths were never the master, the
      Canva design was. Retyping there sets real letterforms in the real
      typeface, which is what the standing rule is protecting. Nothing needs to
      be identified, reconstructed or guessed.

      **Export settings that matter**, because the repo's tooling assumes them:
      - **SVG, not PNG.** SVG export is a Canva Pro feature — if the account
        has lapsed to free it will silently offer PNG instead.
      - **Keep the page at 1500×1500**, the size the Noven set used. The
        artwork floats inside a square and gets cropped later by viewBox; the
        crop is computed, so the canvas size only has to stay consistent.
      - **Transparent background on**, or every file arrives with a white
        rectangle behind it.
      - **Export all six**, even the ones that look unchanged. The pattern and
        banner may carry the name in places that are easy to miss.
      - `og.png` is separate: **PNG at exactly 1200×630** (B5).
- [x] **B3. The monogram was redrawn — and it half-clears the old bar.** It is
      now a **"W."**, navy for light chrome (`Favicon.svg`) and warm white for
      dark (`Icon Mark.svg`). Two findings from testing it at real sizes:

      **It needed the square trim badly.** As exported, the mark occupies about
      64% of the width and 39% of the height of its 375×375 page, so scaling
      the raw file into a 16px tile rendered the letters at roughly 10×6px.
      `trim.mjs --square --pad 7` crops to the artwork and it is legible at
      16px. Do not skip that step for icon assets.

      **It does not survive dark browser chrome unaided, and the Noven mark
      did.** The old favicon was a *filled tile* — navy `#170969` and warm
      white `#fffefa` in one asset — so it carried its own background and read
      on any tab strip. The new one is navy on transparent, which on a dark
      tab strip is very nearly invisible. Verified by rendering, not assumed.

      **Shipped stopgap:** `site/public/favicon.svg` now carries a
      `prefers-color-scheme: dark` rule flipping the mark to warm white,
      applied by `trim.mjs --dark-fill`. Verified legible at 16px and 32px on
      both light and dark chrome. It touches no path data and the original in
      `assets/brand/` is untouched.

      **The designed answer is still owed, and it is a small Canva job:** a
      filled navy tile with the warm-white "W." on it, exactly as the Noven
      circle worked. A tile beats a bare letterform at 16px because it owns
      every pixel it is given, and it removes the need for the CSS rule
      entirely. Owner's call.
- [ ] **B4. Seven letters where there were five. The lockup gets wider.**
      `site/src/layouts/Base.astro` hard-codes the wordmark's dimensions in two
      places — line 88 (`width="1066" height="236"`) and line 164
      (`width="1194" height="236"`). At the same cap height WARDITH is roughly
      40% wider. **Those numbers must be updated to the new artwork's real
      viewBox or the logo renders squashed**, and the header will need a look on
      a narrow phone where the extra width has nowhere to go.
- [x] **B5. Done 2026-08-04 — and the premise was wrong.** "Nothing else will
      regenerate it" was written before anyone read `assets/og/README.md`.
      `og.png` is a build product of `og.html`, which references the committed
      wordmark; re-rendering was the whole job. See the corrected note above.
- [ ] **B6. Keep the originals untouched, and let the script do the trim.**
      New masters go into `assets/brand/` unmodified. The web copies in
      `site/public/` are the same files with the viewBox cropped to the
      artwork, and **`assets/brand/trim.mjs` now does that** rather than
      anyone measuring by hand:

      ```
      npm install playwright
      node assets/brand/trim.mjs "assets/brand/Logo Primary.svg" site/public/logo.svg
      node assets/brand/trim.mjs "assets/brand/Logo Dark.svg"    site/public/logo-dark.svg
      node assets/brand/trim.mjs "assets/brand/Social Avatar.svg" site/public/favicon.svg --square
      ```

      It measures with the browser's own `getBBox()`, refuses to write if
      anything other than the viewBox, width, height and metadata changed, and
      **prints the exact numbers B4 needs for `Base.astro`**. Verified against
      the committed Noven set before it was trusted.

      **Note the third line.** `favicon.svg` is cropped from **Social
      Avatar.svg**, not from `Favicon.svg` — the supplied favicon asset was
      judged unusable at small sizes on 27 July and the circle avatar replaced
      it. That swap is easy to undo by accident when a fresh set arrives.

      The old Noven files stay in git history — do not delete the record.
- [ ] **B6a. Decide whether the published logo keeps Canva's C2PA manifest.**
      Found 2026-08-04: `site/public/logo.svg` carries an embedded Canva
      content-credentials manifest of **16.9KB inside a 26.6KB file** — nearly
      two-thirds of the weight of an asset on every page, and no browser reads
      it. `logo-dark.svg` and `favicon.svg` have none, so it is per-export
      rather than a blanket stamp.

      It contains **no personal data** — checked; it is Canva's signing chain
      and nothing about the account. It does carry a signed claim of
      `softwareAgent: Canva AI` and IPTC source type
      `compositeWithTrainedAlgorithmicMedia`. Nothing about that is dishonest —
      accurate provenance is the entire point of C2PA — but it is
      machine-readable metadata on a business that sells what machines read
      about you, so it is the owner's call rather than a silent default.

      **`trim.mjs` strips it from the web copies by default and the originals
      in `assets/brand/` keep theirs untouched**, which preserves the
      provenance record exactly where the standing rule says originals live,
      without shipping a signing chain to every visitor. Pass
      `--keep-metadata` to override.
- [x] **B7. The email banner's "AI Visibility Services" wording is gone.**
      Outstanding since 27 July, and the new set replaces that asset with
      `Email Signature.svg`, which carries no service description at all — just
      the wordmark and two contact lines. The old fault is closed. It has been
      replaced by the domain conflict recorded above, which is a bigger one.

**Not affected, checked:** the hero animation. `assets/video/frame.html` uses
generic captions and abstract blocks — no business name appears in it. Only the
*filename* carries the old name (`noven-answer.mp4` / `.webm`), referenced at
`site/src/pages/index.astro:60-61`. Rename the files and the two lines. **No
re-render needed.**

---

## Phase C — the repo, on a branch, as one change

**DONE 2026-08-04.** C1–C10 are all complete on
`claude/wardith-name-feedback-4zbg52` and verified against the built output
rather than the source: every canonical and sitemap entry is `wardith.co.uk`,
no occurrence of the old name or domain survives anywhere in `dist/`, the five
prices are unchanged at 125 / 750 / 95 / 250 / 495, and the `json-code.ts`
invariant holds — both visible blocks on the homepage match the head JSON-LD
byte for byte, and the abridged offers block on the pricing page is a faithful
subset of the head's Service schema.

**Three things did not survive a mechanical rename, and are worth knowing:**

- **`businessLinkedIn` was `null`, not the old slug.** See D0.5. `schema.ts`
  omits the key rather than emitting an empty array, so this cost nothing while
  it lasted. **Set 2026-08-06 to `https://www.linkedin.com/company/wardith/`**
  once the page was renamed and the URL supplied — F1.
- **Three passages invited the reader to ask an assistant what Noven does and
  compare the answer.** That test returned nothing under the old name — the
  self-audit proved it — so the invitation was already failing before the
  rename. Two now point at the check the site passes every time: view the
  source and see that the visible answers and the machine-readable ones are
  built from one file. **That is a stronger claim than the old one**, because
  `json-code.ts` enforces it byte for byte.

  **The third was a paragraph saying an assistant asked about us today would
  not know who we are. The owner cut it on 2026-08-04, and was right to.**
  Two reasons, and the second is the one that matters:

  1. Under "Where's the proof?", a skimming prospect reads it as *this does
     not work*. It is the highest-stakes position on the page.
  2. **It assumed an outcome that has not been measured.** The self-audit's
     verdict was that the *identity* was the blocker, not the site — "Noven"
     belonged to four other businesses, so the answers went to them. A name
     with no occupant removes that specific failure. Whether the assistants
     name Wardith by launch is an open question, and **the pre-launch audit
     is how it gets answered** — not a paragraph written in advance.

  **Re-decide what the site says about its own visibility after that audit,
  not before.** If it comes back named, the invitation returns stronger than
  it ever was, with evidence: *ask ChatGPT about Wardith and see.* That is a
  live demonstration no competitor can fake.
- **`ops/audit-setup.md` §9 still says Noven and must keep saying it.** The
  frozen question set is a twelve-month baseline. Rewriting it would not update
  a measurement, it would replace one with a different one. Noted in the file
  itself so nobody tidies it later.

Do this whole phase before anything is published. `business.ts` first: it is the
single source of truth and most of the rest follows from it.

- [x] **C1. `site/src/data/business.ts`** — seven lines. `name` (10),
      `legalNote` (11 — "Wardith is a trading name of Kieran Smith, a sole
      trader"), `email` (13), `description` (20), the comment at 48–52, and
      `businessLinkedIn` (57). **The LinkedIn slug will change — do not update
      line 57 until the LinkedIn page has actually been renamed and the new URL
      confirmed**, or the structured data publishes a `sameAs` pointing nowhere.
- [x] **C2. `site/astro.config.mjs:8`** — `site:` drives every canonical and the
      whole sitemap. One line, largest blast radius in the repo.
- [x] **C3. `site/public/robots.txt`** — line 1 comment, line 44 sitemap URL.
- [x] **C4. `site/src/layouts/Base.astro`** — line 62 (meta description), lines
      88 and 164 (logo `alt` text and the dimensions from B4).
- [x] **C5. The seven pages.** `index.astro` (12 references), `faq.astro` (9),
      `about.astro` (8), `pricing.astro` (6), `how-it-works.astro` (4),
      `contact.astro` (2), `404.astro` (2). Read each — these are body copy, not
      config, and some will need rewriting rather than substituting.
- [x] **C6. The small ones.** `site/package.json:2` (`"name": "noven-site"`),
      `site/package-lock.json` (2, follows automatically on install),
      `site/README.md` (2), `site/src/styles/global.css:1` (a comment).
- [x] **C7. Rename the video files and their two references** (see Phase B).
- [x] **C8. Verify the `json-code.ts` invariant still holds.** `CLAUDE.md` flags
      this specifically: the homepage's visible code block must stay
      byte-for-byte identical to the JSON-LD in `<head>`. It is the site's
      central proof and the rename touches everything it renders. **Check it
      explicitly rather than assuming.**
- [x] **C9. Build and read the output, not the source.** Seven pages plus
      sitemap. Confirm: every canonical is the new domain, the sitemap lists the
      new domain, the JSON-LD `name` and `url` are new, and the five offers are
      **unchanged** at 125 / 750 / 95 / 250 / 495. A rename must not move a
      price by accident.
- [x] **C10. Update the ops documents.** `novenstudio.co.uk` appears in
      `HANDOVER.md`, `README.md`, `ROADMAP.md`, `ops/README.md`,
      `ops/accounts.md`, `ops/audit-setup.md`, `ops/linkedin.md`,
      `ops/own-facts-check.md`, `ops/third-party-services.md` and
      `ops/zoho-mail-setup.md`. **Leave the audit folder alone** —
      `ops/audits/noven-2026-08-02/` is a dated historical record and rewriting
      it would destroy the baseline. Same rule as the repricing: correct what
      claims to be current, never what is correctly dated history.

---

## Phase D0 — the four owner jobs that have to be done before the merge

Written 2026-08-04, once A1 was settled. **These are the only things in this
document that an assistant cannot do**, because they all live behind a login.
Everything else on the repo side is Phase C and is already in hand.

**All four are free.** `ops/plan-to-1-september.md` puts the business under a
spending freeze until 26 August, and none of this breaches it. **If any screen
in any of these steps asks for payment, stop and say so** — it means something
is different from what is written here, and the answer is to wait, not to pay.

**One principle throughout, borrowed from `ops/zoho-mail-setup.md`: if a screen
shows you a value that differs from one written here, trust the screen.** These
panels change, and the console knows things this document cannot — which data
centre an account is on, which IP a host is currently using.

---

### D0.1 — Netlify: attach `wardith.co.uk` while the site is still Noven

Do this **first**. It is what makes the DNS in D0.2 verifiable, and doing it
early means TLS has days to issue rather than minutes.

1. Netlify → the site → **Site configuration** → **Domain management**.
2. **Add a domain** → `wardith.co.uk`. Netlify will say it does not resolve
   yet. That is expected; carry on.
3. Repeat for `www.wardith.co.uk`, `wardith.com` and `wardith.uk`.
4. **Leave `novenstudio.co.uk` as the primary domain for now.** Do not detach
   it and do not promote Wardith yet.
5. The site's `*.netlify.app` hostname is **`kaleidoscopic-cuchufli-ff7b1a.netlify.app`**
   — read from Netlify on 2026-08-04, site ID `d109871f-6f2c-4d05-9fa8-d7c9454fa1bf`.
   That is the CNAME target D0.2 needs. **Use the bare hostname, not the
   `main--` branch variant**, which points at one branch's deploys rather than
   at whatever is live.

**What this does in the meantime, and why it is not a problem.** Netlify's
documented behaviour is to 301 every non-primary domain to the primary,
preserving the path. So until the merge, `wardith.co.uk/pricing/` will
redirect to `novenstudio.co.uk/pricing/`. That is harmless — nobody has the
new address yet — and it is a live proof that DNS and TLS are correct.

**And it is the whole of D3.** Flipping the primary domain at merge time
reverses every one of those redirects at once, page for page, without writing
a single rule. Verify the direction actually flips on the day rather than
assuming it.

### D0.2 — GoDaddy DNS: point all three domains at Netlify

**DONE 2026-08-04, and the check earned its keep.** All three zones were
screenshotted and read row by row against this spec. `wardith.uk` had its apex
A record as **`70.2.60.5`** instead of `75.2.60.5` — one digit, and the failure
mode is silence: the domain simply would not have served, TLS would never have
issued for it, and because it is a defensive redirect nobody visits, nothing
would have surfaced the fault until somebody typed the address. Corrected.

**Keep that loop for anything typed into a registrar by hand.** The owner does
the panel, the screenshots come back, the rows get read against the written
spec. No credential moves and the error class that actually happens — a
transposed digit, a doubled hostname, a stale parked record — gets caught the
same day.

Two other things the zones turned up:

- **GoDaddy pre-provisions a `_dmarc` record**, and it arrives as
  `p=quarantine` with `rua=` pointing at GoDaddy's own address. On a domain
  with no SPF and no DKIM yet, that means the first message ever sent from it
  fails DMARC and is quarantined — **and that failure looks exactly like
  nobody replying**, in launch week. `wardith.co.uk` and `wardith.com` are now
  `p=none` with reports coming to `hello@wardith.co.uk`. Raise back to
  `p=quarantine` only after a real message shows SPF, DKIM and DMARC all
  passing. **Edit that row, never add a second one** — two DMARC records is a
  hard failure exactly like two SPF records.
- **Leave `_domainconnect` alone.** It is a discovery record, routes nothing,
  and grants nobody access — a Domain Connect change still has to be approved
  while signed into GoDaddy. It is what makes an automatic Zoho setup
  available in D0.4, which is the step with six hand-typed records and a
  400-character DKIM key.

**Still owed on `.com` and `.uk`, once nothing else is under pressure:** both
will never send mail, so `v=DMARC1; p=reject;` with no `rua` is the right
setting — free anti-spoofing on two domains carrying the brand. Dropping the
`rua` also sidesteps the cross-domain reporting rule, which needs an
authorisation record at the receiving domain before most reporters will send
anything at all.

#### The original spec, kept for reference

For **each** of `wardith.co.uk`, `wardith.com` and `wardith.uk`.

GoDaddy → **My Products** → the domain → **DNS** → **Manage Zones** /
**Manage DNS**.

1. **Delete the parked records first.** A new GoDaddy domain ships with an `A`
   record on `@` pointing at GoDaddy's parking page and a `CNAME` on `www`
   pointing at `@`. Both have to go, or the domain keeps serving the parking
   page from a cached record long after the real ones are added.
2. Add these two:

   | Type | Name | Value | TTL |
   |---|---|---|---|
   | A | `@` | `75.2.60.5` | 1 hour |
   | CNAME | `www` | `kaleidoscopic-cuchufli-ff7b1a.netlify.app` | 1 hour |

   `75.2.60.5` is Netlify's load-balancer IP and is the value
   `novenstudio.co.uk` already uses at Namecheap. **Read it off Netlify's own
   screen rather than trusting this line** — it is the one number here that
   Netlify can change without telling anybody.

3. **GoDaddy's `Name` field is relative, the same trap Namecheap has.** Type
   `@` for the domain itself and `www` for the subdomain. Typing
   `www.wardith.co.uk` produces `www.wardith.co.uk.wardith.co.uk`, which
   resolves to nothing and looks like a Netlify fault.
4. **Leave the nameservers alone.** GoDaddy will offer to "connect your domain"
   through a wizard that moves DNS elsewhere. Two records is the whole job.

### D0.1a — Deal with the second Netlify project

**Found 2026-08-04 while checking D0.1: there are two Netlify projects on this
team, not one.** The live site is `kaleidoscopic-cuchufli-ff7b1a`, primary
domain `novenstudio.co.uk`, deploy `ready`. The other is **`noven-2-0-preview`**,
also deployed and `ready`, publicly reachable at
`noven-2-0-preview.netlify.app` with **no password and no SSO**.

It is not in `ops/own-facts-check.md`, which is the register of every surface
publishing this business's facts — so it is a live, indexable copy of the
business on the open web that nothing in this repo was tracking.

**After the rename it becomes a stale copy under the dead name**, which is
precisely the "your facts disagree across surfaces" fault the audit is sold to
find. Two acceptable answers, both a minute's work:

- **Delete the project** if it was a one-off preview. Cleanest.
- **Set a password on it** (Site configuration → Access control) if it is still
  wanted, so it stops being a public surface.

Do **not** just leave it. Add whichever was chosen to `ops/own-facts-check.md`
so the next sweep knows it exists.

**DONE 2026-08-06: deleted, and it was not alone.** Listing the Netlify team
turned up a *third* project, `aesthetic-unicorn-619923`, also public and in no
operating document anywhere. Both are now deleted; one project remains,
`kaleidoscopic-cuchufli-ff7b1a`, serving `wardith.co.uk`. Confirmed against the
API rather than taken on trust.

**The generalisable bit: this was found by listing the team, not by reading the
register.** D0.1a existed because somebody happened to look; the third project
had no entry to find. **A surface nobody documented is a surface nobody
checks** — so the sweep in `ops/own-facts-check.md` now lists the Netlify team
rather than working from its own rows. Same argument applies to any host where
creating something is a click.

Timing mattered: done before the domain was submitted to Search Console and
Bing, so no crawler was ever offered a Noven-branded duplicate with nothing
pointing home.

### D0.3 — Wait for TLS, and check it before anything else moves

**PASSED 2026-08-04.** `https://wardith.co.uk` serves with a valid certificate
and redirects page-for-page to the primary domain. DNS, the Netlify
attachment, TLS and the alias redirect are all confirmed working — which means
the merge-time flip has been proven in the direction that costs nothing.

**Two things worth keeping from how this was diagnosed.**

**The certificate had to be reissued, and that is a consequence of the order
in D0.1.** Attaching the domains *before* DNS existed is right — it gives TLS
days rather than minutes — but it means Netlify's certificate was issued when
only `novenstudio.co.uk` resolved, and Netlify uses one certificate covering
every attached hostname. It cannot add a name it could not validate at the
time. So **expect to press Renew certificate once DNS is live**, and do not
read the resulting warning as a DNS fault.

**Test on a phone, on mobile data, before debugging anything.** Chrome caches
certificate failures per host and keeps showing the interstitial well after
the cause is fixed. On 2026-08-04 the desktop browser was still refusing the
site after the renewal had already succeeded; the phone loaded it cleanly
first try. Different resolver, different network, no cached error — it
separates "the site is broken" from "this browser remembers it being broken"
in about ten seconds, and it costs nothing.

Netlify issues a Let's Encrypt certificate once the records resolve. Usually
minutes, occasionally hours.

**Do not merge until all four hostnames show a valid certificate in Netlify's
Domain management panel**, and `https://wardith.co.uk` loads in a browser
without a warning. Merging before that publishes a site whose every canonical
points at an address the browser refuses to open.

If it stalls, the cause is almost always the parked records from D0.2 step 1
still being cached. Wait out the TTL and press **Renew certificate**.

### D0.4 — Zoho: `hello@wardith.co.uk`, as an alias

`ops/zoho-mail-setup.md` is a step-by-step for this exact job on the old
domain. It still applies; only the DNS panel changes, from Namecheap to
GoDaddy. **Note the account is on the EU data centre, which is why every
hostname ends `.eu`.**

**Add it as an alias on the existing user, not as a second user.** Aliases are
free; users are £1/month each, and one Mail Lite licence is all this business
needs. That is also what keeps this step inside the spending freeze.

1. Zoho Mail Admin Console → **Domains** → **Add Domain** → `wardith.co.uk`.
2. Verify ownership with the TXT record Zoho gives you, added at GoDaddy
   exactly as in D0.2 (Name `@`, no quotation marks — GoDaddy adds them).
3. **Users** → the existing `hello@` user → **Mail Aliases** → add
   `hello` @ `wardith.co.uk`.
4. Add the mail records at GoDaddy. MX has its own **Priority** column — do
   not put the number in the value field:

   | Type | Name | Value | Priority |
   |---|---|---|---|
   | MX | `@` | `mx.zoho.eu` | 10 |
   | MX | `@` | `mx2.zoho.eu` | 20 |
   | MX | `@` | `mx3.zoho.eu` | 50 |
   | TXT | `@` | `v=spf1 include:zoho.eu ~all` | — |
   | TXT | `zmail._domainkey` | the value Zoho generates | — |
   | TXT | `_dmarc` | `v=DMARC1; p=none; rua=mailto:hello@wardith.co.uk` | — |

   **One `v=spf1` record and no more.** Two is a hard failure, not a weaker
   check — receiving servers stop checking entirely. If GoDaddy refuses the
   DKIM value it is over the 255-character limit; regenerate the key at
   1024-bit in Zoho rather than splitting it across rows.

5. **Test before the merge, both directions.** Send *to*
   `hello@wardith.co.uk` and confirm it arrives. Then reply *from* it to a
   Gmail address, open **Show original**, and confirm `SPF: PASS`,
   `DKIM: PASS`, `DMARC: PASS`. A new domain with broken authentication gets
   quietly filtered, and the failure looks exactly like nobody replying —
   which on a launch week is indistinguishable from the outreach not working.

6. **`hello@novenstudio.co.uk` keeps receiving.** It is on both LinkedIn
   pages, in the ICO record and in whatever has already been cached. It must
   not bounce for at least twelve months (E3).

7. **If Zoho asks for money at any point in this** — for a second domain, or
   because Mail Lite will not host two — stop. Do not pay during the freeze.
   Tell the owner; the fallback is to keep publishing the old address for a
   few more weeks, which is ugly but free.

### D0.5 — LinkedIn: the name, and the decision about the slug

The company page name and its public URL are two separate fields, and only one
of them is published in our own structured data.

1. LinkedIn → the company page → **Admin view** → **Edit page** → **Page
   info** → change the name to **Wardith**.
2. In the same panel, look for the **public URL** field and try to change the
   slug from `novenstudio` to `wardith`.
3. **Then tell me which of these two happened**, because it changes C1:
   - **The slug changed.** Send the new URL. `business.ts` line 57 gets it,
     and the `sameAs` stays.
   - **LinkedIn will not let you change it.** Also a real answer. We ship the
     merge with both `sameAs` links removed and add them back later.

**My recommendation is to ship without the `sameAs` links either way.** A
missing `sameAs` is invisible; a wrong one is a published claim that this
business and that URL are the same thing, made on a site whose whole pitch is
that its own facts are correct. Decoupling a LinkedIn admin job from a deploy
is worth more than the link is.

4. While in there, the About text on **both** the company page and the founder
   profile still publishes the pre-31-July prices — £30 / £350 / from £75.
   Repaste from `ops/linkedin.md` §5.4 and §2 with the new name. **Two faults,
   one paste.** The new cover and logo PNGs are in `assets/linkedin/`, already
   rebuilt for Wardith.

---

## Phase D — the switch. This is the publishing moment

- [ ] **D1. Netlify: add the new domain, set it primary, keep the old one
      attached.** Do not detach `novenstudio.co.uk` — it has to stay bound to
      serve the redirects.
- [ ] **D2. DNS at the new registrar** — A/CNAME for Netlify, then wait for TLS
      to issue on all three new domains before switching anything.
- [ ] **D3. 301 redirects, page for page — and D0.1 already does this.**
      `/pricing` → `/pricing`, not everything to the homepage. Seven pages plus
      the 404, and `.com` and `.uk` folded in too, so only one address ever
      resolves content.

      **No redirect rules need writing.** Netlify 301s every non-primary domain
      to the primary, preserving the path, so promoting `wardith.co.uk` to
      primary reverses all of it in one action — provided `novenstudio.co.uk`,
      `wardith.com` and `wardith.uk` all stay *attached* to the site. **Verify
      the direction actually flipped, on the day, with a real request to a real
      inner page.** This is the step where an assumption costs every old link
      the business has.
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

- [x] **F1. DONE 2026-08-06. Both.** The page is renamed and the slug is
      `wardith`: `https://www.linkedin.com/company/wardith/`. Set in
      `business.ts`, so the Organization now publishes it as `sameAs` on all
      nine pages. The old `novenstudio` URL is dead, which is why this value
      was held at `null` through the rename rather than shipped pointing
      nowhere — see D0.5, and the recommendation there was followed exactly.

      **Confirmed 2026-08-06: the page loads in a private window**, so a
      crawler is not shown a login wall and the `sameAs` is worth what it
      claims. That check is what separates a corroborating link from a
      decorative one — see `ops/own-facts-check.md` row 13.
- [x] **F2. DONE 2026-08-06.** The company page About is rewritten by the
      owner: no Noven, and the prices match the site.
- [x] **F3. DONE 2026-08-06**, same pass — the founder profile About too.
- [ ] **F4. Google Search Console.** The new domain is a **new property** — add
      and verify it, submit the new sitemap, then use the **Change of Address**
      tool, which requires the D3 redirects to already be live. Keep the old
      property; do not delete it. **Step by step in
      `ops/search-console-and-bing.md` part 1**, written 2026-08-06.
- [ ] **F5. Bing Webmaster Tools.** Still not set up, and it was already a
      finding. A brand-new domain with no history makes it more urgent, not
      less — Copilot answers from Bing. **Part 2 of the same document**, and
      note there is nothing to migrate: Bing never indexed the old domain
      either, so this is a clean first submission rather than a move.
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
