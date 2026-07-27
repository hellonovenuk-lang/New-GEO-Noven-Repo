import { chromium } from 'playwright';
import { mkdirSync, rmSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const here = dirname(fileURLToPath(import.meta.url));
const frames = join(here, 'frames');
rmSync(frames, { recursive: true, force: true });
mkdirSync(frames, { recursive: true });

const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args: ['--force-device-scale-factor=2', '--font-render-hinting=none'],
});
const page = await browser.newPage({
  viewport: { width: 540, height: 540 },
  deviceScaleFactor: 2,
});
await page.goto('file://' + join(here, 'frame.html'));
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(200);

let n = 0;
const shot = () =>
  page.screenshot({
    path: join(frames, `f_${String(n++).padStart(4, '0')}.png`),
    animations: 'disabled',
  });

const lens = await page.evaluate(() => ({
  a: window.A_LEN,
  b: window.B_LEN,
  c: window.C_LEN,
  tail: window.TAIL_LEN,
}));

for (let i = 0; i < lens.a; i++) {
  await page.evaluate((i) => window.setFrameA(i), i);
  await shot();
}
for (let m = 0; m < lens.b; m++) {
  await page.evaluate((m) => window.setFrameB(m), m);
  await shot();
}
for (let k = 0; k < lens.c; k++) {
  await page.evaluate((k) => window.setFrameC(k), k);
  await shot();
}
// Hold the finished state so the loop has a beat of rest before it restarts.
await page.evaluate((k) => window.setFrameC(k), lens.c - 1);
for (let t = 0; t < lens.tail; t++) await shot();

console.log('total frames:', n, lens);
await browser.close();
