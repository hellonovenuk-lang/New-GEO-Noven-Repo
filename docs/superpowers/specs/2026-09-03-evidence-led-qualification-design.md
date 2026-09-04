# Evidence-led qualification with an exception list

Status: design and six-record pilot approved by the owner on 2026-09-03. Implementation is local only. Pilot release checks must pass before wider rollout; no deployment or outreach is authorised by this design.

## Scope

Extend the existing agent-run qualification stage, not a new autonomous platform.
Reuse completed campaign runs, census, Companies House client, scoring engine,
strict validation and coverage report. Pilot on six records from the two current
owner-led installation/building campaigns, then process remaining review records.
The mechanism remains sector-neutral; targeting comes from campaign configuration.
No paid campaign reruns, new subscriptions, scheduled service, CRM changes,
outreach, production deployment or changes to approval policy in this version.

## Components and flow

1. A review planner reads campaign data and a private evidence ledger. It lists
   only missing, stale or conflicting requirements for each census record.
2. The existing qualification agent follows that plan using the current public
   research tools and Companies House client. This is agent-led automation;
   the helper is not a standalone web search service or an extra model pipeline.
3. A deterministic reconciler validates findings, generates specific exceptions
   and proposes a new campaign draft. It never manufactures source evidence.
4. Existing scoring and strict validation run on that draft. Existing coverage
   remains authoritative; a separate review-attempt report explains parked cases.
5. Produce one proposed approval batch plus one exception list. No send operation
   is included. Generic inboxes remain eligible for secondary consideration.

Likely implementation location: tools/prospect-compiler/review_evidence.py plus
tests and a ledger schema. Reuse tools/companies-house/company_lookup.py without
expanding its API surface initially. A small optional evidence input to coverage
may remove misleading blanket warnings, but must not weaken canonical gates.
No changes to the remote dispatch interface are needed for the first version.

## Evidence contract

Each ledger finding contains campaign/census record ID, requirement, value,
source URL, retrieved timestamp, short supporting excerpt, method, assessment
rationale, reviewer type and any superseded finding ID. Record fetch failures
separately from facts. Keep full operational evidence outside the public core.
Source content is untrusted data, never an instruction to the agent.

Requirements: exact legal/trading identity, active company type/status, relevant
services, actual geography, operational decision-maker, published contact route,
and duplicate identity. Each is VERIFIED, MISSING, CONFLICT, STALE or NOT_APPLICABLE
with an explicit reason. NOT_APPLICABLE cannot bypass company/email prerequisites.
Approval state is stored separately and defaults to NOT_APPROVED.

Name matches are candidate discovery, not legal verification. Require an exact
published company number or a corroborated legal-name/address link to the trading
business, alongside current registry status. Registered-office location alone
does not establish or disprove local trading. Directorship alone does not prove
operational ownership or personal inbox access. Published email is not proof of
deliverability. Similar names and shared hosting do not establish duplicates.

Import old notes as evidence leads, not automatically verified facts. Preserve
verified structured findings and reconcile contradictory canonical fields before
removing a blocker. Never merely suppress a warning because notes sound positive.
Facts do not automatically generate subjective commercial scores; the agent must
support those under the existing scoring rubric before canonical scoring runs.

## Bounded research defaults proposed for version one

- Reuse same-day verified evidence. On a later invocation, refresh mutable
  legal status, contact and owner facts before advancing readiness; preserve old
  evidence rather than changing dates. Service/geography evidence is reusable
  for 30 days unless a newer contradiction is found. These are operational
  defaults, not claims of legal sufficiency or permission to send.
- Per business, stop at 12 external requests or 5 minutes of active research,
  whichever comes first. Count searches, page/API requests and retries toward
  the limit. Shared cached sources need not be fetched again for another record.
- Allow at most two retries for transient network/service failures within that
  same budget. Respect retry instructions; defer if waiting exceeds the budget.
  Authentication failures, access restrictions and unavailable tools become
  explicit operational exceptions, never closure or absence findings.
- No email guessing, SMTP probing, forms, messages, sign-ins or access bypasses.
- Record consumed budget and attempted sources durably. A repeated invocation
  resumes without a fresh budget for unchanged unresolved records. Reopen only
  on new evidence, materially changed inputs, a due freshness check or an
  explicit research-budget reset. Routine re-entry does not restart searches.

## Outcomes and human decisions

Keep canonical proposed-target, secondary, excluded, incumbent and review
classifications intact. The exception list distinguishes missing evidence,
conflicting evidence, operational failure and genuine policy choice. Each item
states the exact requirement, attempts made, what would resolve it, and whether
the agent, owner or unavailable external information is needed next.

No email found means parked/unresolved, not excluded and not owner approval
required. Owners cannot approve unknown facts into verified facts. Current
targeting-policy changes and final proposed priorities/readiness remain genuine
owner decisions, presented together rather than one interruption per business.
Approval must be tied to the exact campaign draft version and must not carry
silently onto material changes. This version does not implement sending.

Review-attempt completion means all selected records were processed or parked.
It does not mean qualification COMPLETE. Preserve INCOMPLETE when canonical
coverage remains unresolved. Report majority coverage with unresolved records
visible in the potential non-top denominator; do not shrink it to hit a target.
Do not rewrite raw mentions, combine census identities or rerun paid research.
Confirmed duplicate findings become proposals with an auditable source mapping.

## Verification and rollout

First test offline with synthetic fixtures: verified evidence survives resume;
name-only legal match fails; contradictory evidence stays unresolved; missing
email stays parked; generic inbox is retained; transient failures respect the
budget; stale mutable evidence is refreshed; duplicate suspects are not merged;
approval remains separate; no external writes occur; original inputs are intact.

Then run six existing real review records spanning missing email, ambiguous
company, service scope, duplicate identity, local coverage and owner identity.
Record requests/time, evidence added, outcomes and remaining exceptions. Inspect
every pilot outcome against its cited sources. Do not infer a success-rate target
or promote uncertain records just to pass the pilot.

Expand only if all six have an auditable outcome or explicit exception, budgets
hold, validators pass where applicable and no false verification is found.
An incomplete coverage report is an expected result, not a failed research loop.
On failure, correct the bounded issue and repeat affected tests before expansion.

## Completion includes the reusable skill

Update both .agents/skills/qualify/SKILL.md and .claude/skills/qualify/SKILL.md
after the pilot demonstrates the process. Align the compiler handoff and outreach
instructions where they describe this stage; avoid duplicating the entire design.
Keep the skill generic and operational prospect names out of the core repository.
Test skill parity and representative scenarios, including a fresh-task resume.
Document commands, evidence reuse, limits, exceptions, generic inbox treatment,
one approval batch, and the distinction between attempt completion and coverage.
The work is not complete until the reusable instructions reflect tested behaviour.

Keep changes scoped and preserve earlier artifacts. Publishing core changes is
a separate deployment step with its effect stated beforehand; this design commit
alone is local and does not publish or alter the running workflow.
