# Search Console, Bing, and Copilot feed

*Keeping the domain indexed so assistants can find it.*

---

## Status as of 2026-08-10

| Task | Status | Date |
|---|---|---|
| Google Search Console | Domain property verified; sitemap submitted; indexing requested on all pages; Change of Address accepted | 2026-08-06 |
| Bing Webmaster Tools | Site submitted; indexing requested on all indexable pages | 2026-08-07 |
| Live URL test (Google) | Homepage tested, passed, verified byte-identical code panels | 2026-08-07 |

**Both search consoles are done.** That closed the retrieval side for Copilot, which answers from Bing's index.

---

## Standing rules — do not undo these

- **Keep the old `novenstudio.co.uk` property forever.** Deletion destroys half of the G2 before/after measurement. It costs nothing to keep.
- **Do not press CANCEL MOVE.** Change of Address was accepted 2026-08-06 and runs ~180 days. Google treats it as a signal for that window.
- **Leave the redirects alone.** `wardith.co.uk`, `wardith.com`, and `wardith.uk` all redirect to the live domain. Do not re-submit the old sitemap.
- **Do not add `novenstudio.co.uk` to Bing.** It only 301s away now; submitting asks Bing to index a redirect.
- **Do not re-run the self-audit questions straight after migration.** The baseline measurement depends on stable ground, not movement.

---

## Still owed

- [ ] **Sitemap in Bing.** Open **Sitemaps** in Bing and either see `sitemap-index.xml` listed or submit it. Thirty seconds.
- [ ] **New pages to both consoles.** `/terms/` and `/privacy/` added 2026-08-10. Request indexing in Google Search Console; submit URLs in Bing. The sitemap picks them up on its own but submissions are stronger signals. Four operations, five minutes.
- [ ] **`site:wardith.co.uk` weekly on Google and Bing.** Returns the pages; measurement that indexing worked. Target: all pages. Judge as "all of them" not a fixed number, because `/order/` will move it.
- [ ] **`site:novenstudio.co.uk` at one month and six months.** Baseline: returned 4 on 2026-08-06. Measures how long indexed pages survive a 301 plus Change of Address.

---

## Why Copilot matters

Copilot answers are grounded in Bing's index. **If your site is not in Bing's index, Copilot cannot cite it.** This is a harder, more useful finding than any mention rate — indexation is fixable; model behaviour is not.

The audit's Copilot section leans on the Bing index check (`site:{domain}` search, a public check, not Wardith's own Webmaster Tools account) and treats hand-run mentions as illustration.

---

## Sign in as

`hello.noven.uk@gmail.com` owns both Search Console and Bing Webmaster properties. It is the same identity as GitHub and Netlify. It carries the dead name and stays — it is an identity, not a brand surface.

**If a screen shows a value that differs from what's written here, trust the screen.** These consoles change their wording and menus more often than documentation gets read.
