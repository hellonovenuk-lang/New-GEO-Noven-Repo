# Wardith — marketing website

Static marketing site for Wardith, built with [Astro](https://astro.build). Wardith helps
service businesses get found when their customers ask AI assistants (ChatGPT, Google,
Copilot, Perplexity) to recommend someone for what they do.

The site is itself a demonstration of the service: fully static crawlable HTML, no
client-side JavaScript, explicit AI-crawler permissions, an XML sitemap, and JSON-LD
structured data (Organization, Service, FAQPage).

## Commands

```sh
npm install     # install dependencies
npm run dev     # local dev server at localhost:4321
npm run build   # static build to ./dist (also generates the sitemap)
npm run preview # preview the built site
```

## Structure

- `src/layouts/Base.astro` — shared layout: head tags, Organization JSON-LD, header, footer
- `src/pages/` — one `.astro` file per page (Home, How it works, Pricing, FAQ, About, Contact, 404)
- `src/styles/global.css` — the entire stylesheet; one typeface (Inter), near-black ink, one deep-blue accent
- `public/robots.txt` — explicitly allows AI crawlers (GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended, Bingbot)
- The sitemap is generated at build time by `@astrojs/sitemap` at `/sitemap-index.xml`

## Placeholders still rendering on the live site

Two, both deliberate, both visible to visitors and to the AI crawlers `robots.txt`
invites in. Everything else on the original pre-launch list is done.

- **Address for service of documents** — `src/layouts/Base.astro`, footer, therefore
  on **every page**. Blocked on the service address landing; see `ROADMAP.md` 1c.
  This one is a legal disclosure that is already owed, not a cosmetic gap, and the
  placeholder text currently published names an internal file.
- **Case studies** — `src/pages/index.astro`, home page. Blocked on the first client.

Two other `[PLACEHOLDER` strings appear in `src/pages/about.astro`, in branches that
can no longer be reached now that `founderLinkedIn` and `founderPhoto` are set, and
one in `src/pages/faq.astro` is the detector function itself. Grepping for the string
finds all five; only the two above reach a page.

No facts, statistics, results or testimonials have been invented anywhere on the site;
anything unknown is marked with a placeholder.
