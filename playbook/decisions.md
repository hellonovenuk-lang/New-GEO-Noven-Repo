# Decisions that are closed

*One line each. Here so nobody reopens a settled question, not to explain the
reasoning. If you need the argument, it is in `git log` or `archive/`.*

## Positioning and product

- **The audit is the outreach tool** — the smallest thing we sell and the
  qualifier for the Foundation.
- **The audit is the default entry product for every opportunity type** —
  GAP, GROWTH and DEFEND alike. The type changes why we approach a business,
  never the first thing sold. 2026-08-14.
- **No free audits, no introductory rate, no first-five discount, no bundling.**
  2026-07-31.
- **SUPERSEDED 2026-08-24 — agency channel scrapped, see 'Outreach'
  section.** **One narrow exception: the Agency Sample.** Wardith may produce a limited
  Agency Sample as a sales-development asset for a prospective SEO agency.
  It goes to the agency and never to the end client; it uses a publicly
  evidenced agency-client relationship; it is materially narrower than the
  paid £500 Benchmark and is never represented as it; it demonstrates the
  methodology and two or three useful findings; it excludes the complete
  opportunity map, the full implementation prioritisation and the recurring
  benchmark setup. **This sets no precedent for free Wardith audits** — the
  rule above is otherwise unchanged. 2026-08-19.
- **SUPERSEDED 2026-08-24 — agency channel scrapped, see 'Outreach'
  section.** **Agency pricing: £500 Benchmark, then £150/month per client.** Quarterly
  Deep Review and white-label output both included while the client is on
  the monthly service. Portfolio pricing exists for agencies placing several
  clients; the thresholds come from early agency conversations and real
  delivery economics, not from a table written in advance. 2026-08-19.
- **Tiers separate on permanent answer pages, not question volume.** 2026-07-31.
- **We do not build websites.** The Foundation works on the site they have.
- **No score out of ten, no visibility index, no percentage.** Bands with raw
  counts.
- **Prompted and unprompted visibility are never blended into one headline.**
  Unprompted (the question does not name the business) measures discovery and
  powers the headline and every peer comparison. Prompted (it does) measures
  representation and is reported separately. Definition:
  `models-and-schemas.md`. 2026-08-19.
- **Report "named wrongly" separately and loudly.** It is worse than absence.
- **Copilot and AI Overviews are checked by hand**, at a reduced sample, because
  neither has an API and the Azure route would measure something else.
- **Claude is not checked.**

## Outreach

- **Direct to SME owners, not white-label to agencies.** Local trades and
  professional services, sector × local market, the £250 Audit as the entry
  product. The agency white-label channel (`archive/agency-product.md`) was
  explored and dropped — it is a contested channel against funded
  competitors, and the repo's own writing is visibly better aimed at an
  owner than an agency director. Kept in the repo as history, not deleted.
  2026-08-24.
- **The first clients are cold.** The owner has no business network. 2026-08-09.
- **Never contact anyone without a live limited company or LLP.** PECR.
- **The never-named are the first batch**, not the per-assistant gaps.
  2026-08-10.
- **A per-assistant gap is only worth a letter when the assistant is ChatGPT.**
  2026-08-10. Still true for the GAP letter specifically; a Gemini- or
  Perplexity-only absence can now be a GROWTH angle instead. 2026-08-14.
- **SUPERSEDED 2026-08-24 — the most-named cohort within DEFEND now
  defaults to excluded again; see the most-named-cohort bullet below.**
  **High AI visibility is no longer an automatic outreach exclusion.**
  GAP / GROWTH / DEFEND / NO OPPORTUNITY replaces the old visibility-only
  filter — a strongly visible business is a DEFEND opportunity, not a dead
  end. REVIEW is not a fifth opportunity type; it stays a state of
  disposition and priority. 2026-08-14.
- **A market's most-named cohort — the small cluster already dominating its
  AI answers, as few as one business or as many as five — defaults to
  excluded from outreach; a DEFEND business outside that cohort does not.**
  `most_named_cohort` in `scoring_engine.py`: an absolute visibility floor
  (`visibility_score >= 3`), a relative-position band (`>= 0.7` of the
  group's own top rate, loosened from the old 0.85), and a rank-within-group
  cap (top 5 by visibility_rate within its own service_scope group) — no
  longer conditioned on having a comparable peer at all. `GAP` is
  unconditional at zero visibility now; `business_credibility` no longer
  gates it. Both are proposals (`disposition_recommendation`,
  `opportunity_type`) the owner can override. 2026-08-24.
- **SUPERSEDED 2026-08-24 — DEFEND's classification changed to
  `most_named_cohort` (see above); the ranking order itself (GAP > GROWTH >
  DEFEND) is unchanged.**
  **DEFEND is ranked last and marked experimental.** `overall_rank`/
  `outreach_rank` sort by opportunity_type first — GAP > GROWTH > DEFEND —
  with `final_score` only the tiebreak within a type: `final_score` measures
  evidence quality, which correlates with business size, which correlates
  negatively with willingness to buy, so scoring it first put a market's
  most-visible, least-motivated businesses ahead of a genuine gap. The
  opportunity type itself is not deleted — a market leader may buy
  monitoring once a monitoring product with delivery history exists — but no
  DEFEND outreach has actually run yet. 2026-08-23.
- **Opportunity type, commercial priority and send-readiness are three
  separate fields, never conflated.** Visibility count alone does not set
  priority. 2026-08-14.
- **Decision-maker accessibility (`DIRECT`/`IDENTIFIABLE`/`GATEKEPT`/
  `CORPORATE`/`REVIEW`) is tracked for every qualified prospect.** It
  informs commercial priority as one factor among several; it never
  automatically sets or overrides it. 2026-08-15.
- **Companies House is the filter, never the source of the list.** 2026-08-10.
- **One finding, one offer, no chasing sequence.**
- **2026-08-23 — Recognition lists of named businesses may be published:**
  positive-only, no rank numbers, nobody below the named set identified
  individually or by implication, removal on request. Ranked league tables
  remain out of scope. Telling a prospect privately about a competitor is a
  separate, different act and is unaffected either way.
- **This narrowed publish rule was retained after the agency channel was
  dropped**, not written for it — it was reasoned through and settled on its
  own merits for the direct-to-SME recognition list, so dropping that
  channel does not reopen it. 2026-08-24.
- **`/outreach` pushes every drafted email into Zoho Mail as a real draft
  (Stage 7.5, `tools/zoho-draft-push/`), never sends.** The OAuth token used
  is scoped to `ZohoMail.messages.CREATE` only — no send/reply/delete
  capability exists in the code path at all, not just by convention.
  Credentials live at `~/.wardith/zoho-credentials.json`, outside the repo,
  generated by the owner directly in Zoho's own API console. 2026-08-24.
- **Cold calling is not started.** Separate rules, no work done.
- **LinkedIn outreach is later, not now.**

## Name, brand and site

- **The business is Wardith**, `wardith.co.uk`, from 2026-08-04. `wardith.com`
  and `wardith.uk` are owned, redirecting, never published.
- **`novenstudio.co.uk` stays registered** — it carries every redirect and is in
  the ICO record and both LinkedIn pages.
- **`hello@novenstudio.co.uk` keeps receiving for at least twelve months.**
- **Brand assets are used as supplied.** The logo is never redrawn or retyped.
- **The site publishes the real locality** — the founder is on the Wirral, post
  goes to Poole, and both are stated rather than reconciled.
- **Wardith never describes itself with an industry acronym**, with one
  deliberate exception: a single FAQ entry that names the terms in order to
  translate them.

## Money and legal

- **Sole trader**, trading as Wardith. Not VAT registered, and the site says so.
- **Client records are held locally, encrypted, in the UK.** 2026-08-10.
- **Retention: relationship plus twelve months; do-not-contact kept
  permanently.** 2026-08-09.
- **Revolut Pro is the business account.** UK Postbox is the address for
  service, and only the mailbox address (BH16 6FA) is ever published.

## Working practice

- **Work directly on `main`.** Branches are for experimental, high-risk or
  major architectural work, or when explicitly requested — not the default.
  2026-08-16.
- **Pushing to `main` publishes** — Netlify deploys it. Say what a push will
  publish before doing it.
- **Never invent a business fact.** Unknowns are `[PLACEHOLDER]` and flagged.

## Site content

- **`/context-watch` drafts are never committed.** `content/context-watch/`
  is gitignored; promoting a draft into `site/src/content/context/` is a
  separate, explicit, later step, never automatic. 2026-08-16.
