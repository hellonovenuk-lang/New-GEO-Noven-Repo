---
name: context-watch
description: >-
  Search the open web for recent, genuine news and research that supports why
  AI-search visibility matters right now, and draft each qualifying find as a
  local review file (headline, publisher, date, a short quoted excerpt, and a
  Wardith-voice relevance note) for the owner to read and approve. Writes
  nothing into this repository and never touches the live site — output is
  local drafts under `content/context-watch/`, outside git, for the owner to
  review. Use this whenever the owner asks to run a context/news scan, check
  for new supporting articles, or invokes `/context-watch`. Does not publish,
  does not create or edit anything under `site/`, and does not decide what
  goes live — that is a separate, later, explicit step once the owner has
  approved specific finds.
---

# /context-watch

Invoked as `/context-watch`, on demand, whenever the owner wants a run — there
is no schedule. Finds recent articles and research that back up why AI-search
visibility matters, and drafts them for review. It never publishes anything
and never touches `site/`.

**This is stage one of a two-stage process.** This skill finds and drafts.
Promoting an approved draft into the site (`site/src/content/context/`,
committed, eventually rendered on the "Why this matters" page) is a separate,
explicit, later action the owner asks for by name — not something this skill
does, and not something that happens automatically because a draft exists.

## Stage 0 — Scope and approval, once

State this once at the start, then run straight through without pausing for
approval again — the pattern `/90qrun`, `/qualify` and `/outreach` already
use:

- **Read-only web research** — `WebSearch` and `WebFetch` only, against the
  topic list below. No Claude in Chrome, no computer-use, no browser
  automation of any kind — this skill never needs a live browser connection.
- **Writes**, confined to a new local folder, `content/context-watch/`, at
  the repository root. This folder is gitignored — nothing this skill writes
  is ever committed, pushed, or reaches the live site by itself.
- **No writes anywhere under `site/`, and no git commit or push.** Promotion
  is a distinct, later, human-directed action outside this skill.

## Stage 1 — Topic list

Search against these, adjusting phrasing per query rather than searching the
list verbatim:

- AI search visibility / being recommended by AI assistants
- Generative engine optimization (GEO)
- ChatGPT, Gemini, Copilot or Perplexity as a search/recommendation surface
- AI Overviews and zero-click search
- AI shopping / AI agents making purchase or booking decisions
- How LLMs choose which businesses to name or recommend
- Research or surveys on consumer trust in AI-generated answers

Keep the list current — if the owner mentions a new angle worth tracking,
add it here rather than treating it as a one-off search.

## Stage 2 — Find and qualify candidates

For each candidate a search turns up, check before drafting anything:

- **Real publisher or researcher.** A named outlet, research body, or
  primary source (Pew, Gartner, McKinsey, a platform's own blog, established
  trade press) — not an anonymous content-farm page or an SEO listicle.
- **Genuinely recent.** Published within roughly the last 90 days. Older
  pieces only qualify if they're a primary research report still being
  actively cited, not routine news.
- **Says something substantive.** A real finding, data point, or argument —
  not a marketing post repackaging someone else's news with no new content.
- **Not a duplicate.** Check the URL against every file already in
  `content/context-watch/` and, if `site/src/content/context/` exists,
  against every entry already promoted there. Skip anything already present
  either way.

**If nothing on a given run clears this bar, say so and draft nothing.**
There is no quota to fill — a run that finds zero qualifying articles is a
normal, successful run.

## Stage 3 — Draft each qualifying find

For each one, write `content/context-watch/<slug>.md` (slug from the
headline, kebab-case), frontmatter:

```yaml
title: "..."           # the source's own headline
url: "..."
publisher: "..."       # the actual outlet or research body
date: "YYYY-MM-DD"      # the source's publish date
excerpt: "..."          # one sentence, verbatim, quoted, under ~25 words
foundDate: "YYYY-MM-DD" # today
note: "..."             # see below
```

**`excerpt`** is a short, direct quotation from the source — never a
paraphrase presented as a quote. It exists to give the owner (and, later, a
site visitor) a real flavour of the piece before clicking through, not to
reproduce it at length.

**`note`** is one or two sentences, in `playbook/voice.md`, on why this
specific piece matters for a Wardith client — grounded strictly in what the
excerpt and source actually say. Never a generic "AI is changing search"
line reused across entries; never a claim the source doesn't support. Write
it against `playbook/voice.md` the first time, not as a cleanup pass after —
say who found what before making the claim, avoid the rule-of-three and
em-dash tells, keep it a sentence a person would actually say.

## Stage 4 — Report

One message, not just the files:

- How many candidates were considered and how many cleared Stage 2.
- For each draft: headline, publisher, date, the excerpt, the note, and the
  file path.
- **An offer, not an action:** "Tell me which notes to extend and I'll
  lengthen just those, still checked against `voice.md`." Only extend a note
  when the owner names it — don't pre-emptively lengthen every one.
- A one-line reminder: **nothing here has been added to the site.** Promotion
  is a separate step the owner asks for by name, per draft.

## What this skill does not do

- **Does not write anything under `site/`.** The Astro content collection
  and the "Why this matters" page don't exist yet and this skill does not
  create them — that happens at first promotion, once there's real approved
  content behind it, as its own explicit piece of work.
- **Does not commit or push.** `content/context-watch/` is gitignored; this
  skill's writes never enter git history.
- **Does not decide what's good enough to publish.** It qualifies candidates
  against Stage 2's bar for drafting, not against a publishing bar — every
  draft still needs the owner's explicit approval before it goes anywhere
  near the live site.
- **Does not use a browser.** `WebSearch`/`WebFetch` only — never Claude in
  Chrome, never computer-use, so a run never stalls on a browser-connection
  prompt.
