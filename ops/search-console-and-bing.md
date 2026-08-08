# Search Console and Bing — `wardith.co.uk`

**Status: Closed as a runbook, live as a set of standing rules.** Written
2026-08-06 as step-by-step instructions; **Google was completed 2026-08-06 and
Bing 2026-08-07**, so the click-by-click setup is gone — git holds it if a second
domain ever needs it. What is below is what outlives the job: the things that
must not be undone, the checks still owed, and the measurements this migration
set up.

**Sign in as `hello.noven.uk@gmail.com`.** It owns both properties and is the
same identity as GitHub and Netlify. It carries the dead name and stays — it is
an identity, not a brand surface.

**One principle throughout: if a screen shows a value that differs from one
written here, trust the screen.** These consoles change their wording and menus
more often than this file gets read.

---

## What was done

| | State | Date |
|---|---|---|
| Google Search Console | Domain property verified; sitemap submitted; indexing requested on all eight pages; Change of Address accepted and running | 2026-08-06 |
| Live-URL test (§1.5 below) | Run on the homepage and **passed** | 2026-08-07 |
| Bing Webmaster Tools | Site submitted; indexing requested on all eight indexable pages | 2026-08-07 |

**Both search consoles are done.** That closed the retrieval side for Copilot,
which answers out of Bing's index and was the one assistant of four with no
direct route to the site.

---

## Do not undo these

- **Keep the old `novenstudio.co.uk` property forever.** The owner asked
  directly on 2026-08-06 whether it could be deleted. No, for three independent
  reasons: it is the only view of what is still served from the dead name; it
  holds half of the G2 before/after measurement in `ops/rename-to-wardith.md` —
  *how long a dead name persists* against *how fast a new one is learned* — and
  one deletion destroys the first half of it; and the Change of Address tool
  lives inside it. It costs nothing to keep.
- **Do not press CANCEL MOVE.** It sits next to the move status on that screen.
  Change of Address was accepted 2026-08-06 and runs to roughly February 2027;
  Google treats it as a signal for about 180 days.
- **Leave the redirects alone**, and do not submit the old sitemap again.
  `ops/accounts.md` commits to keeping `novenstudio.co.uk` registered for at
  least three years, which is the binding number.
- **Do not add `novenstudio.co.uk` to Bing.** It only 301s away now; submitting
  it asks Bing to index a redirect.
- **Do not re-run the self-audit questions straight after any of this.**
  `ops/audit-method.md` and the G2 note both depend on the baseline being a real
  measurement rather than one taken while the ground was moving.

---

## Still owed

- [ ] **Confirm the sitemap is listed in Bing.** URL Submission does not require
      a sitemap, so having submitted the URLs is not evidence the sitemap went
      in — and if the Search Console import carried it across, it did so
      silently. Open **Sitemaps** in Bing once and either see
      `sitemap-index.xml` listed or submit it. Thirty seconds.
      `ops/own-facts-check.md` row 8.
- [ ] **`site:wardith.co.uk` on each of Google and Bing, weekly.** Returning the
      eight pages is the measurement that says this worked, and **self-audit
      finding 2 does not close until it does.** Submission is not indexation.
      The Search Console graphs will be empty and discouraging for a while for
      reasons that are not faults.
- [ ] **Re-run `site:novenstudio.co.uk` at one month and at six months.**
      **It returned 4 on 2026-08-06 — that is the decay baseline.** How long
      indexed pages survive a 301 plus Change of Address is the one measurement
      out of this whole migration that transfers to a client, because it
      measures something we caused.

---

## §1.5 — the live-URL test, kept because it is the only check of its kind

**URL Inspection → the URL → Test live URL → View tested page → HTML.** That is
a live fetch showing exactly what Googlebot receives. Search the HTML for:

- `PLACEHOLDER` — must be **zero hits**
- `company/wardith` — **twice on the homepage, once everywhere else.** This line
  said "once" until 2026-08-07 and was wrong about the one page it tells you to
  test: the homepage carries it in the head JSON-LD *and* in the visible code
  block, and those being byte-for-byte identical is the site's central claim,
  enforced by `site/src/lib/json-code.ts`. **One hit on the homepage would be a
  real fault, and the check as written would have called it a pass.**

**Why this matters more than it looks.** Every other check in this repo runs
against `dist` or the Netlify API, and the session network policy blocks
`wardith.co.uk` — so this is the one link in the chain the repo cannot verify
itself (`ops/own-facts-check.md` row 1). URL Inspection closes it from the
crawler's own side, for free. **The pricing page is the one page carrying prices
that still has not been seen live.**

**Expect the homepage's visible code block to be empty in this view, and do not
treat it as a fault.** URL Inspection shows *rendered* HTML, and the block types
itself in at ~620 chars/sec from an emptied start, so the snapshot lands inside
that window. The head JSON-LD is unaffected, the raw HTML carries the full block,
most AI crawlers do not execute JavaScript at all, and every fact in the block is
also in `<head>` on the same page. **Nothing is lost from any index. Do not "fix"
this by changing the animation** — the panel exists to be watched being written,
and trading that for a rendering crawler's two-second snapshot is a bad exchange.
Understood and accepted, not outstanding.

---

## The instinct that earned its keep

**If a validator fails, read what it says — do not work around it and do not
skip the tool.** Change of Address failed its first attempt on 2026-08-06, and
that failure is what uncovered the missing redirects: `novenstudio.co.uk`,
`wardith.com` and `wardith.uk` had all been *serving* the full site at their own
addresses for nine days, with no redirect at all, while four documents assumed
otherwise. Google's validator was the only thing in this toolchain that fetches
the old domain and reports what it actually got. Seven explicit rules now live in
`netlify.toml`. Full account in `ops/rename-to-wardith.md` D3.
