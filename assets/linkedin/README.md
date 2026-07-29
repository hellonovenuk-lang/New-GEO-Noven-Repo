# The two images the LinkedIn page needs

LinkedIn does not accept SVG, and every brand asset in `../brand/` is one. So
the company page needs PNGs, and these are them:

| File | Size | Goes in |
|---|---|---|
| `logo-400.png` | 400×400, transparent | The company page logo |
| `cover-1128x191.png` | 1128×191 | The company page cover image |

Both are build products. The sources are `logo.html` and `cover.html` beside
them, rendered by headless Chromium — the same approach as the link-preview
card in `../og/` and the homepage animation in `../video/`.

## What's in them, and what isn't

**Nothing is drawn here.** The standing rule is that the brand assets are used
as they were supplied, never redrawn or retyped, so:

- **The logo** is `../brand/Social Avatar.svg` placed as-is. All `logo.html`
  does is scale it and crop the frame to the bounds of the disc, so the mark
  meets all four edges. That way a circular mask fills completely and a square
  one reads as the disc it is. The corners are left transparent rather than
  filled white, so LinkedIn's own mask can sit wherever it likes.
- **The cover** is brand navy `#170969`, warm white `#fffefa`, the committed
  wordmark (`site/public/logo-dark.svg`, referenced as-is like the og card
  does) and one sentence, set in the same Newsreader 500 the site sets its
  display type in. The font is the copy already vendored at `../og/fonts/` for
  the og card, so neither render touches the network.

The sentence is **"We make your business easy for AI assistants to find,
understand and recommend."** — the site's own summary of the service, from the
homepage, verbatim bar the pronoun. It is the answer to what Noven sells, and
because it *is* the site's sentence it can't drift from it.

**It isn't the homepage headline**, which is what the og card carries. LinkedIn
prints the page's tagline immediately under the cover, and that tagline already
ends *"…ask an AI who to use"*. The headline ends the same way, so the two
would have stacked the same phrase twice, one above the other. Checked in a
mock-up of the page header, not guessed at.

## Why the wordmark is here and not in the logo slot

The full wordmark belongs on the cover, and the disc keeps the logo slot. That
isn't a taste call — the three candidates were rendered at 48px, which is the
size LinkedIn shows a company logo at in the feed:

- **The disc** stays legible. "N." is two glyphs and it holds up small.
- **The wordmark on navy** goes cramped — six letters across 48px.
- **The wordmark on warm white** nearly disappears, because LinkedIn's feed
  background is white too and the tile stops reading as a tile.

The cover is 1128×191, which is the shape a horizontal wordmark was drawn for,
so it goes there instead — right-aligned, signing off after the sentence.

**Why right-aligned.** The logo badge overlaps the *bottom-left* of the cover
on a company page, so the right edge is the one part of the strip that can
never be covered, whatever LinkedIn does to the crop on a phone. The left 248px
is kept clear for the badge for the same reason.

## Re-rendering

    npm i playwright          # or any Chromium of similar vintage
    node render.mjs

Run from anywhere; `render.mjs` resolves paths relative to itself and writes
both PNGs beside it. It reads the page's laid-out size first and throws rather
than writing if anything overflows the frame — a cover that renders a
half-sentence is the kind of thing that ships unnoticed, so it fails loudly
instead.

In this build environment Chromium is at
`/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, which is what the script
points at, and Playwright is installed globally rather than in the repo.

## If the wording on the site changes

The cover quotes the homepage's summary of the service. If that sentence is
reworded, reword it here and re-render, or the two stop agreeing — which is the
exact fault the audit is paid to find on other people's businesses.
