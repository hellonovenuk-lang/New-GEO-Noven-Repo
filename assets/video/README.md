# The homepage answer animation

`site/public/video/noven-answer.mp4` (and the `.webm` twin) is rendered from
`frame.html` by `capture.mjs` — it is not generated footage. Every frame is the
site's own CSS, drawn by headless Chromium at 2x and encoded with ffmpeg, so the
navy, the warm white and IBM Plex are the same values `global.css` uses rather
than an approximation of them.

That matters for more than tidiness. The animation shows a question being typed
and read; if the lettering drifts or the palette shifts, the thing on screen
stops being a demonstration and becomes a picture of one.

## Re-rendering

    cd assets/video
    npm i ffmpeg-static
    node capture.mjs
    ./node_modules/ffmpeg-static/ffmpeg -y -framerate 30 -i frames/f_%04d.png \
      -vf "scale=1080:1080:flags=lanczos" -c:v libx264 -profile:v high \
      -pix_fmt yuv420p -crf 20 -movflags +faststart -an \
      ../../site/public/video/noven-answer.mp4

Chromium comes from `PLAYWRIGHT_BROWSERS_PATH`; the bundled Playwright ffmpeg
is VP8-only, which is why the encode uses `ffmpeg-static` instead.

The fonts in `fonts/` are the same latin subsets the site loads from Google
Fonts, vendored here so a render never depends on the network.

## Timing

202 frames at 30fps, about 6.7 seconds, four phases in `capture.mjs`: the
question types out, four businesses appear, they sort, the answer fills in.
The last phase holds so the loop has a beat of rest before it restarts.
