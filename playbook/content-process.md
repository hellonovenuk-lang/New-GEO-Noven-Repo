# Content process

**Status: Live.**

Content starts with evidence Wardith already holds. It does not start with a
blank-page request for ideas.

## Inputs

Use one of two sources:

- a completed, schema-valid campaign JSON produced by `/qualify`; or
- one specific research source the owner has approved, normally a draft from
  `/context-watch`.

The content operator may re-open a cited source to verify it is still available
and accurately represented. It does not redo qualification or run a general
news search.

## Output

One invocation creates one review pack under
`~/wardith-runs/content/<slug>/`:

- `content-package.json` — the structured claims, evidence and publication
  decisions;
- `personal-linkedin.md` — the founder-profile version;
- `wardith-linkedin.md` — the company-page version;
- `source-ledger.md` — every public claim and the source supporting it;
- `linkedin-graphic.png` — a 1200×1200 branded graphic.

Everything remains a draft. The process does not post, schedule or contact
anyone.

## Editorial boundary

The personal version may include Kieran's interpretation and first-person
judgement. The Wardith version is written as the business and stays closer to
the finding. Both use `playbook/voice.md` and must make clear whether a statement
is a source finding, a Wardith campaign result or interpretation.

Every factual claim has at least one evidence ID in `content-package.json`.
External evidence needs its publisher, publication date and live source URL.
Campaign evidence needs the local campaign file and a precise locator such as a
field, question ID or run row. A placeholder, an unsupported number or an
untraceable paraphrase blocks the pack.

Campaign content may name businesses only as a positive recognition list under
the rule in `playbook/decisions.md`: no rank numbers, no negative comparison,
and nobody outside the named set identified or implied. Otherwise company names
stay out of public copy.

## Brand boundary

Every public graphic uses the committed Wardith assets, never a recreated or
retyped logo. Content Engine v1 uses:

- `assets/logo.png` for the supplied Wardith wordmark;
- brand navy `#170969` and warm white `#fffefa`;
- `assets/og/fonts/Newsreader-500.woff2` for display type;
- `assets/video/fonts/IBMPlexSans-400.woff2` for body type;
- `assets/video/fonts/IBMPlexMono-500.woff2` for source labels.

The renderer preserves the wordmark's proportions and fails before export if
the text does not fit its fixed mobile-feed layout.

The renderer's only Python dependency is Pillow, declared in
`tools/content-engine/requirements.txt`.

## Review gate

A pack is `READY_FOR_REVIEW`, never published. Before presenting it, confirm:

- the two posts say the same factual thing without being duplicate copy;
- every claim ID resolves to evidence in the ledger;
- the source wording has not been made stronger;
- any named-business use meets the positive-recognition rule;
- the graphic is 1200×1200, uses the committed wordmark and contains no clipped
  text;
- both posts pass a final read against `playbook/voice.md`.
