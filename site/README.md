# Noven — marketing website

Static marketing site for Noven, built with [Astro](https://astro.build). Noven helps
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

## Before launch — placeholders to fill in

Search the codebase for `[PLACEHOLDER` and replace every instance:

- **Domain** — `site` in `astro.config.mjs` and the `Sitemap:` line in `public/robots.txt`
- **Contact details** — email, phone and location on the Contact page
- **Founder bio** — name, bio and location on the About page
- **Company details** — registered name/number/address in the footer (`Base.astro`)
- **Commercial terms** — VAT status, cancellation notice period, audit turnaround time, Foundation delivery time
- **Case studies** — the marked slot on the Home page, once real client results exist

No facts, statistics, results or testimonials have been invented anywhere on the site;
anything unknown is marked with a placeholder.
