# Standing rules for all work in this repo

These rules apply to every future change, in every session, unless the owner
explicitly overrides them.

## Language

- Client-facing language is plain and outcome-led. Say what the customer gets,
  in words a busy business owner would use.
- No search-industry jargon in the copy that persuades — headlines, navigation,
  body text, meta descriptions. **Noven never describes itself with an
  acronym.**
- **One deliberate exception, decided by the owner 2026-08-01.** A single FAQ
  entry or answer page may name the industry's terms — "GEO", "AEO", "SEO" and
  whatever replaces them — *in order to translate them into plain words*, and
  that page's own meta description may say so too. Naming a term to explain it
  is not jargon; leading with it is. The live
  example is the "Is this what people call GEO or AEO?" entry on the FAQ page.
  The reasoning: a buyer who has already researched this arrives holding one of
  those acronyms, and a site that contains the word nowhere cannot be the answer
  when they ask for it — which is the exact failure the audit is sold to find on
  other people's businesses. See `ops/session-log.md`, 2026-08-01.

## Design

- Credibility over design flair. The site must never look AI-generated.
  Specifically banned: all-caps eyebrow tags, symmetric three-column feature
  rows, glowing gradients, buzzwords, and repeated calls-to-action.
- Use the `frontend-design` skill for distinctive visual design guidance when
  reshaping UI or building new pages. It helps with aesthetic direction,
  typography, and intentional design choices.
- Use the `ui-ux-pro-max` skill when designing or reviewing any UI elements:
  pages, components, color schemes, typography, layout, accessibility, or
  animations. It provides design intelligence with 192 color palettes, 74 font
  pairings, 98 UX guidelines, and best practices across modern web stacks.

## Facts

- Never invent business facts, results, testimonials or statistics.
  Anything unknown is written as `[PLACEHOLDER]` and flagged to the owner.

## Brand

- Use the committed brand assets as-is. Never redraw, retype or recreate the
  logo.

## Technical

- Keep the site as crawlable static HTML:
  - AI crawlers explicitly allowed in `robots.txt`
  - an XML sitemap
  - JSON-LD structured data (Organization, Service, FAQPage)

## Git

- Always work on a branch. Never commit to `main`.
- Finish every piece of work on an unmerged branch for review.
