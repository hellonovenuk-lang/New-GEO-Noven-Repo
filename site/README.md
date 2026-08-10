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

One. Everything else on the original pre-launch list is done.

- **Case studies** — `src/pages/index.astro`, home page. Blocked on the first client.

**The address for service came off this list twice.** It was removed from the
rendered page on 2026-08-06 — a visible `[PLACEHOLDER]` in the footer of nine
pages was publishing the name of an internal file to every crawler — and the
real address replaced it on **2026-08-10**. This section was stale for four days
in between, which is worth knowing about a file that describes the live site: it
does not update itself.

**One value in `src/data/business.ts` is still unset and it is not a rendered
placeholder — it is a page that does not exist.** `clientDataStorage.where` gates
`/privacy/`, which is deliberately not built rather than built with a gap in it.
`src/data/legal.ts` explains the reasoning; the practical effect is that
`getStaticPaths()` returns nothing and the route is absent from the site and the
sitemap.

Two other `[PLACEHOLDER` strings appear in `src/pages/about.astro`, in branches that
can no longer be reached now that `founderLinkedIn` and `founderPhoto` are set, and
one in `src/pages/faq.astro` is the detector function itself. Grepping for the string
finds all five; only the two above reach a page.

No facts, statistics, results or testimonials have been invented anywhere on the site;
anything unknown is marked with a placeholder.
