# Working in this repo

## Read this way

**Locate first, then read the range.** Grep for the line, then read around it.
Reading a whole file to use one section is the most common way a session spends
its budget on nothing. `README.md` has a table telling you which file holds what.

**Never re-read a file to check an edit landed.** The edit fails loudly if it
didn't.

## Facts

**Never invent a business fact.** Results, testimonials, statistics, prices,
dates. Anything unknown is `[PLACEHOLDER]` and flagged to the owner. The product
is verifiable published facts.

**No client or prospect names in this repository.** It is written as though
public.

## Outreach

Three rules with legal consequences, not preferences:

- **No cold email without a confirmed live limited company or LLP.** PECR.
- **One recipient per email, never a BCC list.** Twenty addresses visible to
  each other is a data breach.
- **Record every send and every opt-out before the next email goes out.** An
  opt-out you cannot find is not honoured.

## Language and design

**Client-facing copy is plain and outcome-led** — what the customer gets, in
words a busy business owner would use. No industry acronym describing ourselves,
with the one FAQ exception noted in `playbook/decisions.md`.

**Anything a customer reads gets checked against `playbook/voice.md`.** It is a
framework, not a checklist: a sentence that breaks one of its rules and reads
better for it is the right sentence.

**Credibility over design flair. The site must never look AI-generated.** No
all-caps eyebrow tags, no symmetric three-column feature rows, no glowing
gradients, no repeated calls-to-action. **Use the brand assets as supplied and
never redraw the logo.**

**Documents a person opens go in Office formats** — client reports, quotes,
proposals. The client gets a PDF exported from the Word file. Repo files, code
and `robots.txt` stay as they are.

## Git

**Work directly on `main`.** Make scoped changes, test them, commit, and push
— no temporary branch needed. Commits are clear and atomic. Branch only for
genuinely experimental, high-risk, or major architectural work, or when the
owner explicitly asks for one.

**Preserve what's already there.** Uncommitted work stays uncommitted unless
it's yours to finish. Inspect unexpected changes before touching them.

**Some things still need the owner's go-ahead first:** force-pushing,
rewriting history, destructive resets, deleting substantial existing work,
major architectural changes, and production or infrastructure changes.

**Review, research, and audit tasks stay read-only** unless implementation is
explicitly requested.

**Pushing to `main` publishes.** Netlify deploys it. Say what a push will put
in front of the world first — including "nothing visible", which is often the
honest answer.

**Report on completion:** what changed, what checks or tests ran, and the
commit created.

## Writing in this repo

**State the decision, not the argument for it.** This repo reached 12,000 lines
by recording the reasoning behind every choice, and reading it cost more than it
returned. Settled decisions go in `playbook/decisions.md` as one line. If a
future decision genuinely depends on why, one sentence — not a section.

**Do not invent rules.** A constraint belongs here only if the owner decided it
or it has a consequence outside our own preferences. An assistant-generated rule
is a reason to delete, not to keep.
