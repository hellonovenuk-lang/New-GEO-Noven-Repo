/**
 * Turn a Canva SVG export into the site's web copy.
 *
 * Canva exports every asset onto its full 1500x1500 page, so the artwork
 * floats inside a square of empty space. The web copies in site/public are
 * the same file with the viewBox cropped to the artwork's real bounding box —
 * "trimmed to the artwork, viewBox only, no path data altered", which is the
 * standing brand rule in CLAUDE.md: use the assets as-is, never redraw them.
 *
 * That crop used to be measured by hand. This does it with the browser's own
 * getBBox(), which is the same number the renderer uses, so it cannot drift.
 *
 * Verified 2026-08-04 against the committed Noven set, which is the only
 * check that means anything here: logo-dark.svg and favicon.svg come out
 * byte-for-byte identical, and logo.svg differs in one character — the hand
 * trim wrote "216.00" where this writes "216". Same number, same rendering.
 * Note favicon.svg is cropped from Social Avatar.svg, NOT from Favicon.svg:
 * the supplied favicon asset was judged unusable at small sizes on 27 July
 * and the circle avatar replaced it. Keep that swap when the new set lands.
 *
 * Needs playwright, which is not a dependency of the site — install it
 * wherever you run this, the same way assets/video/capture.mjs expects it:
 *
 *   npm install playwright
 *   node assets/brand/trim.mjs "assets/brand/Logo Primary.svg" site/public/logo.svg
 *
 * Prints the width and height to paste into src/layouts/Base.astro. Those
 * attributes are hard-coded there and WILL be wrong after a rename — WARDITH
 * is seven letters where NOVEN was five, so the wordmark is wider and the
 * old numbers squash it.
 *
 * Flags:
 *   --square         crop to a centred square instead of a tight box. What
 *                    the favicon and social avatar want; a tight crop on a
 *                    circular mark shaves the circle.
 *   --keep-metadata  keep Canva's embedded C2PA manifest. Off by default:
 *                    on the Noven set it was 16.9KB of a 26.6KB file, all of
 *                    it a signing chain no browser reads. The originals in
 *                    assets/brand/ keep theirs and are never touched.
 */

import { chromium } from 'playwright';
import { readFileSync, writeFileSync } from 'fs';

const args = process.argv.slice(2);
const square = args.includes('--square');
const keepMetadata = args.includes('--keep-metadata');
const [src, dest] = args.filter((a) => !a.startsWith('--'));

if (!src || !dest) {
  console.error('usage: node trim.mjs <source.svg> <dest.svg> [--square] [--keep-metadata]');
  process.exit(1);
}

const round = (n) => Math.round(n * 100) / 100;

const original = readFileSync(src, 'utf8');

const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
});
const page = await browser.newPage();
await page.setContent(`<body style="margin:0">${original}</body>`);
const box = await page.evaluate(() => {
  const { x, y, width, height } = document.querySelector('svg').getBBox();
  return { x, y, width, height };
});
await browser.close();

let { x, y, width, height } = box;

if (square) {
  const side = Math.max(width, height);
  x -= (side - width) / 2;
  y -= (side - height) / 2;
  width = side;
  height = side;
}

const viewBox = `${round(x)} ${round(y)} ${round(width)} ${round(height)}`;

let out = original;
if (!keepMetadata) {
  const before = out.length;
  out = out.replace(/<metadata>[\s\S]*?<\/metadata>/g, '');
  if (out.length < before) {
    console.log(`  stripped ${(before - out.length).toLocaleString()} bytes of metadata`);
  }
}

// Only these three attributes change. Path data is never touched — that is
// the whole point, and the reason this asserts rather than trusting itself.
out = out
  .replace(/viewBox="[^"]*"/, `viewBox="${viewBox}"`)
  .replace(/(<svg[^>]*?)\swidth="[^"]*"/, `$1 width="${Math.round(width)}"`)
  .replace(/(<svg[^>]*?)\sheight="[^"]*"/, `$1 height="${Math.round(height)}"`);

const strip = (s) =>
  s
    .replace(/<metadata>[\s\S]*?<\/metadata>/g, '')
    .replace(/viewBox="[^"]*"/, '')
    .replace(/(<svg[^>]*?)\swidth="[^"]*"/, '$1')
    .replace(/(<svg[^>]*?)\sheight="[^"]*"/, '$1');

if (strip(original) !== strip(out)) {
  console.error('ABORT: something other than viewBox/width/height/metadata changed.');
  process.exit(1);
}

writeFileSync(dest, out);

console.log(`  ${src}\n    -> ${dest}`);
console.log(`  viewBox="${viewBox}"`);
console.log(`  Base.astro needs:  width="${Math.round(width)}" height="${Math.round(height)}"`);
