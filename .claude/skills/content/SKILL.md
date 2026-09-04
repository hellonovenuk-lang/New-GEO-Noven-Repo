---
name: content
description: >-
  Turn one approved Wardith evidence source — a completed qualified campaign or
  a specific approved research item — into a ready-for-review LinkedIn content
  pack with distinct founder and company-page posts, a claim-level source
  ledger, and a finished graphic using Wardith's committed brand assets. Use
  when the owner invokes /content or asks to turn Wardith findings or approved
  research into LinkedIn content. Never posts, schedules, reruns qualification,
  or performs a general news scan.
---

# /content

Invoke as `/content <campaign folder or approved source file>`.

Read `playbook/content-process.md` and `playbook/voice.md` before drafting. The
content process is the source of truth for inputs, public-evidence rules, output
files and the review gate. Do not duplicate those rules here.

## Stage 0 — scope once

State that the run will read the named source and its directly cited evidence,
write only under `~/wardith-runs/content/<slug>/`, and create drafts plus a
graphic for review. It will not contact anyone, post, schedule, change a
campaign, write under `site/`, commit or push.

If no source was supplied, ask for one. Do not turn a missing input into a broad
content-ideas exercise.

## Stage 1 — gate the source

For a campaign, require a completed campaign JSON that validates under
`tools/prospect-compiler/schema.json`. Read it as evidence; never alter its
qualification, ranking, readiness or source records.

For research, require one source already approved by the owner, normally a
`/context-watch` draft. Open the underlying URL and verify the headline,
publisher, date and the passage supporting the proposed claim. If the source is
unavailable or does not support the claim, stop.

## Stage 2 — choose one argument

Select the strongest single publishable finding. Keep source fact, Wardith
finding and Wardith interpretation distinct. Do not combine unrelated numbers
to make the post feel fuller.

Campaign content defaults to anonymised market patterns. A named recognition
list is allowed only when it passes the positive-only publication rule in
`playbook/decisions.md`; record every published name in `publication`.

## Stage 3 — write the package

Create `~/wardith-runs/content/<slug>/content-package.json` matching
`tools/content-engine/content-package.schema.json`.

The founder post uses Kieran's first-person perspective where it adds something
real. The Wardith-page post speaks as the business and stays closer to the
evidence. They must not be duplicate copy. Both are complete, ready to copy and
paste, and include a source link where the evidence is public.

The graphic carries one headline, one supporting detail and a restrained source
line. Use `market-finding` for campaign evidence and `research-finding` for
external research. Do not create a new logo, palette, type treatment or graphic
outside the renderer.

## Stage 4 — validate and render

Run:

```bash
python3 tools/content-engine/build_pack.py \
  --input ~/wardith-runs/content/<slug>/content-package.json
```

An error is a blocked pack, not something to work around. Correct the source
package and rerun. Inspect the finished PNG at its actual size and at a reduced
mobile-feed size; confirm the wordmark, headline, detail and source remain
legible and nothing is clipped.

If Python reports that Pillow is missing, install the renderer's declared
dependency from `tools/content-engine/requirements.txt`, then rerun the same
command.

## Stage 5 — report for review

Show the complete founder post and Wardith-page post, the graphic, its source
line, the evidence used and all output paths. State any judgement or caveat the
owner should consider.

End with the exact reminder: **Nothing has been posted or scheduled.**
