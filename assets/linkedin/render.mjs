// Renders the two images LinkedIn needs from the HTML sources beside this
// file. Headless Chromium with an explicit viewport, the same way the
// homepage animation is captured in ../video/ — `--window-size` is not
// reliable at these sizes and silently clips the page.
//
//   NODE_PATH=/opt/node22/lib/node_modules node assets/linkedin/render.mjs
//
// Run from anywhere; paths are resolved relative to this file.

import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const here = dirname(fileURLToPath(import.meta.url));

const jobs = [
  { html: 'logo.html', out: 'logo-400.png', width: 400, height: 400, alpha: true },
  { html: 'cover.html', out: 'cover-1128x191.png', width: 1128, height: 191, alpha: false },
];

const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args: ['--font-render-hinting=none'],
});

for (const job of jobs) {
  const page = await browser.newPage({
    viewport: { width: job.width, height: job.height },
    deviceScaleFactor: 1,
  });
  await page.goto('file://' + join(here, job.html));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(200);

  // Fail loudly rather than shipping a clipped image: nothing may extend
  // past the frame, because the frame is the size LinkedIn accepts.
  const overflow = await page.evaluate(() => ({
    w: document.documentElement.scrollWidth,
    h: document.documentElement.scrollHeight,
  }));
  if (overflow.w > job.width || overflow.h > job.height) {
    throw new Error(
      `${job.html} lays out ${overflow.w}x${overflow.h}, larger than the ` +
        `${job.width}x${job.height} frame — it would be cropped.`
    );
  }

  await page.screenshot({
    path: join(here, job.out),
    omitBackground: job.alpha,
    clip: { x: 0, y: 0, width: job.width, height: job.height },
  });
  console.log(`${job.out}  ${job.width}x${job.height}`);
  await page.close();
}

await browser.close();
