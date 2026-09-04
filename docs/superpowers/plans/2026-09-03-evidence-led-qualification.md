# Evidence-led Qualification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Resume qualification using cited facts, bounded research and a separate exception list, without sending or weakening scoring.

**Architecture:** A private versioned evidence ledger feeds a deterministic planner/reconciler. The existing qualification agent gathers evidence; existing scoring and coverage remain authoritative. A six-record pilot precedes expansion and reusable-skill updates.

**Tech Stack:** Python standard library, existing JSON campaign/scoring tools, unittest, existing agent web tools.

**Spec:** docs/superpowers/specs/2026-09-03-evidence-led-qualification-design.md

## Global Constraints

- No paid campaign reruns, new subscriptions, scheduled service, CRM changes, outreach, production deployment or changes to approval policy in this version.
- Per business, stop at 12 external requests or 5 minutes of active research, whichever comes first.
- Allow at most two retries for transient network/service failures within that same budget.
- Preserve original campaigns, census and raw mentions. Write new output paths only.
- Verified generic inboxes remain usable; no guessed contacts or name-only company matches.
- Attempt completion is not qualification completion; approval defaults to NOT_APPROVED and binds to a draft digest.
- Keep prospect evidence outside the core repository. Test with synthetic businesses.

## Task 1: Evidence planner, budget ledger and draft reconciliation

**Files:** create tools/prospect-compiler/review_evidence.py, review-evidence.schema.json, test_review_evidence.py and REVIEW-EVIDENCE.md. Existing scoring and coverage modules remain unchanged initially.

**Interfaces:** public Python functions `new_ledger(campaign, businesses, now)`, `add_finding(ledger, business, finding, now)`, `record_attempt(ledger, business, attempt)`, `build_plan(ledger, now)`, `build_report(ledger, campaign, now)`, `reconcile(ledger, campaign, now)`; transformations return copies and never mutate arguments. `now` is an ISO timezone-aware timestamp. CLI `init`, `finding`, `attempt`, `plan`, `report`, `reconcile`, `park`, `reopen`, all using explicit input/output paths and refusing existing output paths. Agent can also use the Python API. Send concise interface examples to controller early.

- [ ] Write real behavior tests first. Tests must fail for missing production behavior before implementation. Start with:

```python
def test_notes_are_not_verified_evidence(self):
    campaign = {'run': {'campaign_slug': 'sample'}, 'market': [{'business': 'Example', 'notes': 'active company'}]}
    ledger = new_ledger(campaign, ['Example'], '2026-09-03T12:00:00+00:00')
    self.assertIn('legal_identity', build_plan(ledger, '2026-09-03T12:00:00+00:00')['records'][0]['pending'])
```

- [ ] Run `python -B -m unittest discover -s tools/prospect-compiler -p test_review_evidence.py -v` and capture RED evidence.
- [ ] Implement the ledger with campaign slug/hash, stable business identity, source timestamps/excerpts/URLs, rationale, reviewer and supersession IDs. Requirements: legal_identity, active_company, services, geography, decision_maker, contact_route, duplicate_identity. States VERIFIED/MISSING/CONFLICT/STALE/NOT_APPLICABLE. Values remain structured. Validate source URLs, aware timestamps, nonempty rationale/excerpt; verified legal identity needs published-number or corroborated legal-name/address basis and business/register sources, never name-only. Active status number must agree with verified legal number. Verified contact must be explicitly published, not inferred. Explicit negative service/local findings are not equivalent to missing evidence. NOT_APPLICABLE cannot bypass legal/status/contact checks. Preserve contradictions until explicitly superseded; stale evidence cannot advance readiness. Mutable company/status/contact/owner findings require same-day evidence; services/geography can be reused up to 30 days. A newer contradiction overrides fresh positives.
- [ ] Implement durable attempt accounting before external actions: reserve a request/time allowance, then record completion. Pending reservations block further actions until reconciled, count against limits after interruption, and cannot disappear on resume. Existing external calls made before ledger creation are historical evidence, not new billable attempts. Limit requests/time/retries including failures and search queries; nontransient/auth/access errors cannot be retried as transient. Cache reads consume no external requests. Record parking and require explicit new evidence/changed input/freshness/reset reason to reopen; report that owner approval is not needed just because an email is missing. Use append-only attempt/finding history and validate loaded state, not only API calls.
- [ ] Report requirement-specific reasons and next actor (agent/external-information/owner-policy). Report approval batch separately with original proposed priority/readiness, draft SHA256 and NOT_APPROVED. Preserve canonical `build_report` coverage unchanged; do not conflate sidecar completeness with canonical status. Suspected duplicates remain exceptions and are not merged. Unchanged resume makes no new requests. Completed positive evidence can remove a sidecar missing-fact warning but not a canonical readiness gate.
- [ ] Reconcile only fully validated exact company number/status and published contact fields into existing records in a new draft; append traceable source records in the existing schema shape. Do not auto-create scored outreach, set research_complete/business_verified or invent value scores/service_scope. Unsupported existing positive facts must be surfaced as conflicts, not silently overwritten. Emit remaining reconciliation/scoring requirements explicitly. Do not change run date to manufacture freshness. Reconcile refuses campaign fingerprint mismatch. Approval never transfers implicitly.
- [ ] Expand tests for legal ambiguity, email guessing, generic inbox, missing facts, contradictory/newer sources, stale refresh, retry and time/request caps, negative/NaN budget values, interrupted reservations, no-reset resume, duplicate suspicion, immutable originals, input tampering, approval digest and source provenance. Use literal expected outcomes and temporary-directory CLI tests including overwrite refusal.
- [ ] Run focused tests then all prospect compiler and Companies House tests. Self-review, scoped commit, report results with commands and RED/GREEN evidence.

## Task 2: Six-record pilot and bounded expansion

**Files:** private task work/qualification-v2/evidence-pilot/ artifacts only; no prospect names in core.

**Consumes:** Task 1 public API/CLI. **Produces:** versioned ledgers, six-record pilot report, new reconciled draft(s), evidence-based exception list and batch approval digest.

- [ ] Select six existing records covering email, identity, scope, duplicate, geography and owner. Inspect saved source snapshots, reuse only actually supported facts and their original retrieval dates.
- [ ] Initialize each campaign ledger from its existing draft. Import facts with source URLs and short verbatim excerpts; record uncertainties as MISSING/CONFLICT rather than promoting notes. Use `build_plan` before each research action and persist reservations before any new external requests.
- [ ] Use existing API client if configured securely, otherwise public-register website fallback. No new credentials, prompts for routine reads, paid model campaign or outreach. Reserve each query/page request, record result/time, park at the first bound or precise unresolved outcome.
- [ ] Run report and reconcile into fresh paths; run existing scoring/strict validation where drafts changed and coverage with --require-complete. Expected INCOMPLETE is preserved and explained.
- [ ] Review every pilot finding against source snapshots; verify all six have an auditable result, no guesses, counts within caps, originals unchanged and no sends. Exercise a fresh-process resume and demonstrate unchanged request counters.
- [ ] Expand to remaining review records only after pilot checks pass. Persist all outcomes or precise exceptions; no forced promotions to hit majority coverage.

## Task 3: Update and verify reusable procedure

**Files:** .agents/skills/qualify/SKILL.md, .claude/skills/qualify/SKILL.md; tools/prospect-compiler/CAMPAIGN-HANDOFF.md; playbook/outreach-process.md where needed.

**Consumes:** tested helper commands and actual pilot results. **Produces:** consistent generic procedure used in fresh tasks.

- [ ] Read skill-creator and writing-skills instructions and referenced testing guidance before changes. Establish baseline with a realistic synthetic resume scenario before edits.
- [ ] Add concise routing to REVIEW-EVIDENCE.md and integrate missing-only planning, durable limits, exceptions, generic inbox retention and batch approval at the relevant existing stages. Remove contradictory blanket owner-review phrasing, not existing factual/readiness gates. Both skill copies must agree; preserve remote credential and no-core-mutation boundaries.
- [ ] Validate skill frontmatter, compare both copies, and independently forward-test a synthetic resume with contradictory evidence and no published email; verify actual outputs, not just prose matching.
- [ ] Run full relevant regression suites, inspect the diff for prospect data, record pilot counts and limitations, perform independent code review and fix supported findings. Commit locally; no deployment in this version.

## Progress

- Baseline: 115 prospect-compiler tests pass before implementation.
- User approved the design, limits and six-record pilot on 2026-09-03.
- Task 1 implemented locally in 38c8663; independent review correction in 983b3ec. Final fresh regression run: 174 prospect-compiler and 21 Companies House tests pass. The 59 focused helper tests are included in the 174.
- Pilot research covered six records and 16 external requests. Evidence and exceptions preserved; no new outreach approvals or promotions. Original drafts unchanged and strict-valid; full-census qualification remains INCOMPLETE. Fresh-process resume made no requests and preserved all counters.
- Pilot release gate remains HOLD: historic completion times were estimates, not measured active time. The corrected helper keeps legacy timing unknown, blocks additional requests and reports attempt completion INCOMPLETE. Do not infer a real-pilot timing pass from synthetic tests. No expansion of the remaining review records and no silent budget reset.
- Both reusable skill copies and handoff/playbook guidance updated to route to the tested evidence helper, preserve generic inboxes, park missing facts without owner questions, and retain one separate final approval digest. Platform-specific adapters preserved; evidence-led no-CRM/no-push scope takes precedence.
- No push, production deployment, CRM mutation, paid campaign rerun or outreach performed.
- Independent forward test used persisted synthetic ledgers and a fresh process: request cap, generic inbox preservation, contradictory identity, unknown timing, conservative timestamp-interval rounding and unapproved/canonically incomplete state all behaved as required. This proves those control behaviours, not historic real-pilot timing.
- Optional skill quick validator unavailable (PyYAML absent); frontmatter unchanged from committed baseline and guide references/diff checked without adding a dependency.
