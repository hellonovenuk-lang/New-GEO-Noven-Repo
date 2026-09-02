# Wardith remote runner

The `Wardith remote run` GitHub Actions workflow runs while the laptop is off.
It supports `preflight`, `90qrun`, `qualify`, and `outreach`.

## Start it from a phone

1. Open `hellonovenuk-lang/New-GEO-Noven-Repo` in the GitHub app or browser.
2. Open **Actions**, then **Wardith remote run**, then **Run workflow**.
3. Choose the operation. For `90qrun`, enter an industry and geography; for
   `qualify` or `outreach`, enter the existing run slug. Leave the target blank
   for `preflight`.
4. Type `RUN` to confirm a paid `90qrun`, or `DRAFT` to confirm `outreach`.
   Leave confirmation blank for `preflight` and `qualify`.

Start with `preflight`. It performs no paid provider calls and creates no Zoho
drafts.

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
control for the repository plan. The workflow's literal `RUN` and `DRAFT`
confirmations remain required either way.

## Rotation

To rotate Bitwarden access, create a replacement token on the same read-only
machine account, replace the GitHub secret, verify `preflight`, then revoke the
old token. To rotate data-repository access, create a replacement deploy key,
replace both halves, verify `preflight`, then remove the old public key.

Never paste a token or private key into chat, workflow inputs, command-line
arguments, issues, or repository files.
