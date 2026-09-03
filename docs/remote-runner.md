# Wardith remote runner

The `Wardith remote run` GitHub Actions workflow runs while the laptop is off.
It supports `preflight`, `smoke`, `90qrun`, `qualify`, and `outreach`.

## Start it from a phone

1. Open `hellonovenuk-lang/New-GEO-Noven-Repo` in the GitHub app or browser.
2. Open **Actions**, then **Wardith remote run**, then **Run workflow**.
3. Choose the operation. For `90qrun`, enter an industry and geography; for
   `qualify` or `outreach`, enter the existing run slug. Leave the target blank
   for `preflight` and `smoke`.
4. Type `SMOKE` for a provider smoke test, `RUN` to confirm a paid `90qrun`,
   or `DRAFT` to confirm `outreach`.
   Leave confirmation blank for `preflight` and `qualify`.

Start with `preflight`. It performs no paid provider calls and creates no Zoho
drafts.

## Small cloud smoke test

Choose **smoke**, leave **target** blank, and enter **SMOKE**. Approve the
`wardith-production` deployment if GitHub requests it. The test asks the first
sample Wirral dentists question once each to OpenAI, Gemini and Perplexity,
using the models already configured in Bitwarden.

It makes three provider queries, with at most two retries per query for HTTP
429/503 (15 then 45 seconds). The upper limit is nine HTTP attempts, not nine
questions; provider charges may apply. Authentication errors and ambiguous
network failures are not retried. It never runs a research agent, qualification,
outreach, CRM imports or Zoho operations.

Results are committed only to the private `wardith-crm-data` repository under
`smoke-tests/<GitHub run ID>-<attempt>/`: `results.csv` contains the answers and
sources, and `summary.json` contains provider pass/fail checks. Partial results
are retained on failure. No public artifact contains the answers. A green job
requires nonempty answers and sources from all three providers and a successful
private results push. This tests connectivity, not research quality.

For the phone-only acceptance check, turn the laptop off, trigger **preflight**
from the phone and verify its success. Then trigger **smoke** and verify both the
job result and its private results directory from the phone. Do not trigger
`90qrun` as part of this check.

## Safety boundaries

- GitHub holds a separate read-only Bitwarden machine token for this runner.
- Provider and Zoho credentials remain sourced from Bitwarden and are masked in
  workflow logs.
- The private data repository has its own deploy key; the core repository's job
  token cannot write to it.
- Runs are serialized so two remote operations cannot update the CRM database
  simultaneously.
- `outreach` creates or updates Zoho drafts only. It never sends email, replies,
  deletes mail, submits forms, or posts to LinkedIn.

## Required GitHub configuration

Create the `wardith-production` GitHub Environment and these repository Actions
secrets:

- `BWS_ACCESS_TOKEN`: token for Bitwarden machine account
  `wardith-github-actions`, with read-only access to project
  `6ab59b25-f5ae-4e3e-8518-b4b30131120f`.
- `WARDITH_DATA_DEPLOY_KEY`: private half of an Ed25519 deploy key whose public
  half is installed with write access on `hellonovenuk-lang/wardith-crm-data`.

Enable a required reviewer on `wardith-production` when GitHub offers that
control for the repository plan. The workflow's literal `SMOKE`, `RUN` and `DRAFT`
confirmations remain required either way.

## Rotation

To rotate Bitwarden access, create a replacement token on the same read-only
machine account, replace the GitHub secret, verify `preflight`, then revoke the
old token. To rotate data-repository access, create a replacement deploy key,
replace both halves, verify `preflight`, then remove the old public key.

Never paste a token or private key into chat, workflow inputs, command-line
arguments, issues, or repository files.
