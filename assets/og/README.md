# The link-preview image

`site/public/og.png` is the 1200×630 card that LinkedIn, WhatsApp and the rest
show when a link to the site is shared. The platforms don't reliably accept
SVG, which is why a PNG ships at all.

It is rendered from `og.html` by headless Chromium — the same approach as the
homepage animation in `../video/`. The composition is nothing but the site's
own materials: brand navy `#170969`, warm white `#fffefa`, the committed
wordmark (`site/public/logo-dark.svg`, referenced as-is, never redrawn), and
the homepage headline set in Newsreader 500 the way `global.css` sets it. If
the headline on the homepage changes, change it in `og.html` too and re-render.

The font in `fonts/` is the same latin subset the site loads from Google
Fonts, vendored here so a render never depends on the network.

## Re-rendering

    /opt/pw-browsers/chromium --headless=new --no-sandbox --disable-gpu \
      --force-device-scale-factor=1 --window-size=1200,630 --hide-scrollbars \
      --font-render-hinting=none --virtual-time-budget=3000 \
      --screenshot=site/public/og.png assets/og/og.html

(Run from the repo root. The Chromium path is where Playwright's browsers live
in the build environment; any Chromium of similar vintage produces the same
output.)

Every page declares this one image — the card identifies the business rather
than the individual page, and one honest card beats seven near-identical ones.
The tags live in `site/src/layouts/Base.astro`.
