#!/bin/bash
# Cloud-session-only. Populates the exact local files trade_run.py and
# zoho_draft_push.py already read - ~/.noven/env and
# ~/.wardith/zoho-credentials.json - from Bitwarden Secrets Manager, so
# neither script needs to change. Never runs, and never needs to, on the
# owner's own machine: those files already exist there by hand, per
# tools/trade-run/README.md and tools/zoho-draft-push/README.md.
#
# Bootstrap: this environment's ONE configured secret is BWS_ACCESS_TOKEN,
# a Bitwarden Secrets Manager machine-account token. Everything else is
# fetched from the vault at session start, never stored in the environment
# config itself. Expected secret keys in that Bitwarden Secrets Manager
# project: OPENAI_API_KEY, OPENAI_MODEL, GEMINI_API_KEY, GEMINI_MODEL,
# PERPLEXITY_API_KEY, PERPLEXITY_MODEL, ZOHO_CREDENTIALS_JSON (the full
# contents of a zoho-credentials.json file, as one secret value), and
# optionally COMPANIES_HOUSE_API_KEY (tools/companies-house/ - /qualify
# Stage 5 falls back to manual WebFetch/WebSearch if this one is absent, so
# it's fetched best-effort and never blocks the bootstrap).
# BWS_PROJECT_ID is optional - set it to scope the lookup if the token can
# see more than one project.
set -uo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

if [ -z "${BWS_ACCESS_TOKEN:-}" ]; then
  echo "cloud-session-secrets: BWS_ACCESS_TOKEN not set on this environment - skipping. Any skill needing these keys will report exactly which ones are missing." >&2
  exit 0
fi

if ! command -v bws >/dev/null 2>&1; then
  # bitwarden.com/secrets/install (the officially documented one-liner) 404s
  # as of 2026-08 - confirmed dead, not a transient blip. crates.io is a
  # more durable install path anyway: it's unconditionally in this
  # environment's Trusted network allowlist (no add_repo/attachment needed,
  # unlike a GitHub-releases download would require), and cargo/rustc are
  # pre-installed on every Anthropic-hosted cloud session VM. CONFIRMED
  # WORKING (2026-08-27) but compiling from source takes ~4-5 minutes, every
  # single time this branch runs - SessionStart hooks are NOT cached like an
  # environment's Setup script is. Strongly add 'cargo install bws --locked'
  # to this environment's Setup script field (claude.ai/code -> environment
  # dialog) so it's compiled once and cached, and this slow branch never
  # runs at all on later sessions.
  echo "cloud-session-secrets: bws CLI not found - installing via 'cargo install bws' now. This takes ~4-5 minutes because it compiles from source - add 'cargo install bws --locked' to this environment's Setup script so this only ever happens once." >&2
  cargo install bws --locked --quiet >/dev/null 2>&1 || true
  export PATH="$HOME/.cargo/bin:$PATH"
fi

if ! command -v bws >/dev/null 2>&1; then
  echo "cloud-session-secrets: bws install failed (cargo missing, or 'cargo install bws' itself failed) - secrets not bootstrapped." >&2
  exit 0
fi

if [ -n "${BWS_PROJECT_ID:-}" ]; then
  SECRETS_JSON="$(bws secret list "$BWS_PROJECT_ID" --output json 2>/dev/null)" || SECRETS_JSON=""
else
  SECRETS_JSON="$(bws secret list --output json 2>/dev/null)" || SECRETS_JSON=""
fi

if [ -z "$SECRETS_JSON" ]; then
  echo "cloud-session-secrets: 'bws secret list' returned nothing - check BWS_ACCESS_TOKEN is valid and not expired." >&2
  exit 0
fi

get_secret() {
  echo "$SECRETS_JSON" | jq -r --arg k "$1" '[.[] | select(.key == $k)][0].value // empty'
}

mkdir -p "$HOME/.noven"
: > "$HOME/.noven/env"
for var in OPENAI_API_KEY OPENAI_MODEL GEMINI_API_KEY GEMINI_MODEL PERPLEXITY_API_KEY PERPLEXITY_MODEL; do
  val="$(get_secret "$var")"
  if [ -n "$val" ]; then
    echo "$var=$val" >> "$HOME/.noven/env"
  fi
done
chmod 600 "$HOME/.noven/env"

zoho_json="$(get_secret ZOHO_CREDENTIALS_JSON)"
if [ -n "$zoho_json" ]; then
  mkdir -p "$HOME/.wardith"
  chmod 700 "$HOME/.wardith"
  printf '%s' "$zoho_json" > "$HOME/.wardith/zoho-credentials.json"
  chmod 600 "$HOME/.wardith/zoho-credentials.json"
fi

echo "cloud-session-secrets: bootstrap complete from Bitwarden Secrets Manager." >&2
exit 0
