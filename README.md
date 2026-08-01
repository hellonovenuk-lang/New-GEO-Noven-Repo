<p align="center">
  <img src="assets/logo.svg" alt="Noven logo" width="400">
</p>

# Noven

Noven helps businesses get found by AI assistants.

More and more customers don't search the web any more — they ask ChatGPT,
Google's AI, Microsoft Copilot or Perplexity to recommend someone. If those
assistants don't know a business exists, it doesn't get mentioned, and it
quietly loses work to competitors who do show up.

Noven fixes that. We make sure a business is visible, accurate and
recommendable when AI assistants answer questions like *"who's a good
[plumber / accountant / clinic] near me?"* — so the customers who ask AI
get pointed at our clients.

## What's in this repo

The site is live at [novenstudio.co.uk](https://novenstudio.co.uk). No customer
has paid yet.

| Path | What it is |
|---|---|
| `HANDOVER.md` | **New here? Start with this.** The whole business on one page: what's sold, what exists, what doesn't, what has to happen next, and what has to happen every week |
| `site/` | The Noven marketing website (Astro, fully static) |
| `ops/` | Internal operating docs — fourteen files, indexed in `ops/README.md` |
| `ROADMAP.md` | What's true now and what's left — read at the start of every session |
| `CLAUDE.md` | Standing rules for all future work in this repo |

To work on the website:

```sh
cd site
npm install
npm run dev     # local dev server
npm run build   # static build to site/dist/
```
