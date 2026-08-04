<p align="center">
  <img src="assets/logo.svg" alt="Wardith logo" width="400">
</p>

# Wardith

> **Renamed 2026-08-04: this business was called Noven.** The name collided
> with at least four other businesses, which the self-audit found the hard way.
> The live address is `wardith.co.uk`; `wardith.com` and `wardith.uk` are owned
> and redirect to it. Where a document below still says Noven it is recording
> something dated — the 2 August self-audit and its frozen question set are the
> main ones, and they must keep the old name or the baseline is destroyed.
> `ops/rename-to-wardith.md` is the full changeover; `ops/plan-to-1-september.md`
> is the timetable.

Wardith helps businesses get found by AI assistants.

More and more customers don't search the web any more — they ask ChatGPT,
Google's AI, Microsoft Copilot or Perplexity to recommend someone. If those
assistants don't know a business exists, it doesn't get mentioned, and it
quietly loses work to competitors who do show up.

Wardith fixes that. We make sure a business is visible, accurate and
recommendable when AI assistants answer questions like *"who's a good
[plumber / accountant / clinic] near me?"* — so the customers who ask AI
get pointed at our clients.

## What's in this repo

The site is live at [wardith.co.uk](https://wardith.co.uk). No customer
has paid yet.

| Path | What it is |
|---|---|
| `HANDOVER.md` | **New here? Start with this.** The whole business on one page: what's sold, what exists, what doesn't, what has to happen next, and what has to happen every week |
| `site/` | The Wardith marketing website (Astro, fully static) |
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
