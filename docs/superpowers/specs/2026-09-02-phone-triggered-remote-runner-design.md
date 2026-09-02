# Phone-triggered remote runner design

## Decision

Wardith will use GitHub Actions as its first provider-neutral remote execution
environment. The owner can start `90qrun`, `qualify`, or `outreach` from the
GitHub mobile app or mobile browser while the Windows laptop is off.

The Windows Bitwarden integration remains the local execution adapter. It is
not reused by the hosted runner.

## Entry point

One manually dispatched workflow presents three inputs:

- `operation`: `90qrun`, `qualify`, `outreach`, or `preflight`.
- `target`: the public target description for a new run, or the existing run
  slug for later stages.
- `confirmation`: `RUN` for a paid `90qrun`, `DRAFT` for `outreach`, and blank
  for `preflight` or `qualify`.

The workflow rejects missing or mismatched confirmation before retrieving
provider credentials. `outreach` may create or update Zoho drafts, but no code
path sends email, posts to LinkedIn, or submits a contact form.

## Execution

The job checks out the Wardith core repository with GitHub's job-scoped token.
It checks out `hellonovenuk-lang/wardith-crm-data` into a separate working
directory using a dedicated SSH deploy key that has write access only to that
repository.

A Linux secrets wrapper retrieves Wardith's approved secret allowlist from the
existing Bitwarden project for one child process. The hosted runner receives a
separate, read-only Bitwarden machine-account token stored as the encrypted
GitHub Actions secret `BWS_ACCESS_TOKEN`. It never reuses the Windows token.

The job invokes the repository's provider-neutral `.agents` skill for the
selected operation through a non-interactive agent runner. Run files are
written under `~/wardith-runs`, synchronized into the data-repository checkout,
committed, and pushed. The core repository is never modified by an operational
run.

## Secrets and credentials

GitHub Actions stores exactly two bootstrap credentials:

- `BWS_ACCESS_TOKEN`: read-only access to the Wardith Bitwarden project.
- `WARDITH_DATA_DEPLOY_KEY`: write-capable SSH deploy key for only the private
  data repository.

Provider and Zoho credentials remain in Bitwarden. Secret values are masked
before use, are never printed, and are removed with temporary files at job end.
The Bitwarden token is not passed to the child agent process.

The workflow uses a GitHub Environment named `wardith-production`. GitHub's
required-reviewer protection is enabled when the account plan supports it. The
literal confirmation input remains mandatory regardless of environment-plan
support.

## Stage behaviour

`preflight` performs no paid provider calls and makes no external drafts. It
checks repository access, Bitwarden access, the required secret names, runtime
dependencies, and write access to a temporary branch-free data-repository
round trip that leaves no commit.

`90qrun` executes the existing smoke test and paid 90-query workflow, validates
the CSV, then pushes the validated run data.

`qualify` reads a completed run and produces the existing qualification
artifacts. Entries requiring owner judgment remain `REVIEW`; the runner does
not silently promote them to outreach-ready.

`outreach` accepts only an existing campaign whose records already satisfy the
current `ready_to_email == "YES"` gate. It creates or updates Zoho drafts and
syncs the output and CRM database. Sending remains a later human action inside
Zoho Mail.

## Failure handling

The workflow fails before paid work if prerequisites are missing. Operational
outputs are pushed only after their existing validators pass. A failed data
push leaves the artifacts attached to the workflow run for recovery. Logs show
secret names and pass/fail states only, never values.

Concurrent jobs share the data repository, so a repository-level concurrency
group serializes Wardith operational runs. Push conflicts are retried once
after a pull; a second conflict stops without overwriting remote history.

## Verification

Automated tests cover input validation, secret allowlisting, token isolation,
temporary-file cleanup, operation-to-prompt mapping, outreach safeguards, and
data synchronization failure paths. The rollout sequence is:

1. Local unit tests with fake Bitwarden and agent executables.
2. GitHub Actions `preflight` from the laptop.
3. The same `preflight` started from the owner's phone.
4. A no-provider-call fixture run that writes and recovers a disposable data
   artifact.
5. The first paid `90qrun`, only after the owner supplies `RUN`.

## Out of scope

The first release does not add a public webhook, custom mobile application,
scheduled runs, automatic email sending, or conversational triggers from the
ChatGPT or Claude mobile apps. Those interfaces can later dispatch the same
workflow without changing its secret or execution model.
