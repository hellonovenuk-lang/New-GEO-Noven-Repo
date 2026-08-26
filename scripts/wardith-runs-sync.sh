#!/bin/bash
# Syncs ~/wardith-runs/ (trade-run CSVs, campaign folders, outreach prep,
# and the CRM's wardith.db) against a private GitHub repo,
# hellonovenuk-lang/wardith-runs-data, so this data survives between an
# ephemeral cloud VM being reclaimed AND between the laptop and the cloud -
# not just the CRM db, everything under ~/wardith-runs/. Never run inside
# this repository's own git history; ~/.wardith-runs-repo/ is a separate
# clone.
#
# Usage:
#   wardith-runs-sync.sh pull            # bring ~/wardith-runs/ up to date
#   wardith-runs-sync.sh push "<msg>"    # commit + push local changes back
#
# Cloud sessions: this script does NOT attach or clone the repo itself - it
# has no credentials of its own to do that. The calling skill must first
# call the add_repo tool for hellonovenuk-lang/wardith-runs-data
# (access: "push") and run the clone command that tool returns, cloning to
# ~/.wardith-runs-repo/. Once that clone exists, `pull`/`push` here work the
# same on cloud and local.
#
# Local sessions: if ~/.wardith-runs-repo/ doesn't exist yet, `pull`
# clones it directly - your own git credentials already work here, same as
# any other repo on this machine.
#
# Safety: wardith.db is the one file more than one place writes to (the CRM
# app locally, `ingest` from any session) - `pull` refuses to overwrite a
# local wardith.db that has changed since the last sync, rather than
# silently discarding hand-entered CRM notes/activity that only exist
# locally. Run `push` first in that case. Everything else under
# ~/wardith-runs/ is per-run, per-slug output that's never edited by more
# than one place at once in practice, so it's synced as a plain overwrite.
set -uo pipefail

REPO_URL="https://github.com/hellonovenuk-lang/wardith-runs-data.git"
CLONE_DIR="$HOME/.wardith-runs-repo"
RUNS_DIR="$HOME/wardith-runs"
DB_REL="crm/wardith.db"
DB_MARKER="$RUNS_DIR/crm/.last-synced-db-hash"

hash_of() {
  [ -f "$1" ] && sha256sum "$1" 2>/dev/null | awk '{print $1}'
}

cmd="${1:-}"

case "$cmd" in
  pull)
    if [ ! -d "$CLONE_DIR/.git" ]; then
      if [ "${CLAUDE_CODE_REMOTE:-}" = "true" ]; then
        echo "wardith-runs-sync: $CLONE_DIR not found. In a cloud session, call add_repo for hellonovenuk-lang/wardith-runs-data (access: push) and clone it there first - this script never attaches a repo itself." >&2
        exit 0
      fi
      echo "wardith-runs-sync: cloning $REPO_URL to $CLONE_DIR" >&2
      git clone "$REPO_URL" "$CLONE_DIR" || {
        echo "wardith-runs-sync: clone failed - continuing with no synced data. Create hellonovenuk-lang/wardith-runs-data if it doesn't exist yet." >&2
        exit 0
      }
    else
      git -C "$CLONE_DIR" pull --ff-only || echo "wardith-runs-sync: pull failed (network, or local unpushed commits in the clone) - continuing with what's already on disk." >&2
    fi

    mkdir -p "$RUNS_DIR/crm"

    # wardith.db: refuse to clobber local changes made since the last sync
    if [ -f "$CLONE_DIR/$DB_REL" ]; then
      local_hash="$(hash_of "$RUNS_DIR/$DB_REL")"
      marker_hash="$(cat "$DB_MARKER" 2>/dev/null || true)"
      if [ -z "$local_hash" ] || [ "$local_hash" = "$marker_hash" ]; then
        cp "$CLONE_DIR/$DB_REL" "$RUNS_DIR/$DB_REL"
        hash_of "$RUNS_DIR/$DB_REL" > "$DB_MARKER"
      else
        echo "wardith-runs-sync: local wardith.db has changed since the last sync (hand-entered notes/activity?) - NOT overwriting it. Run 'push' first, then 'pull' again." >&2
      fi
    fi

    # everything else: plain additive overwrite from the repo copy
    find "$CLONE_DIR" -mindepth 1 -not -path "$CLONE_DIR/.git*" -not -path "$CLONE_DIR/$DB_REL" -print0 2>/dev/null \
      | while IFS= read -r -d '' src; do
          rel="${src#"$CLONE_DIR"/}"
          dest="$RUNS_DIR/$rel"
          if [ -d "$src" ]; then
            mkdir -p "$dest"
          else
            mkdir -p "$(dirname "$dest")"
            cp "$src" "$dest"
          fi
        done
    echo "wardith-runs-sync: pull complete." >&2
    ;;

  push)
    msg="${2:-Sync wardith-runs data}"
    if [ ! -d "$CLONE_DIR/.git" ]; then
      echo "wardith-runs-sync: $CLONE_DIR not found - nothing to push to. Run 'pull' first (cloud: after add_repo)." >&2
      exit 0
    fi
    if [ ! -d "$RUNS_DIR" ]; then
      echo "wardith-runs-sync: $RUNS_DIR doesn't exist - nothing to push." >&2
      exit 0
    fi

    find "$RUNS_DIR" -mindepth 1 \
      -not -name '*.db-wal' -not -name '*.db-shm' -not -name '*.db-journal' \
      -not -name '.last-synced-db-hash' -not -name '.DS_Store' \
      -print0 2>/dev/null \
      | while IFS= read -r -d '' src; do
          rel="${src#"$RUNS_DIR"/}"
          dest="$CLONE_DIR/$rel"
          if [ -d "$src" ]; then
            mkdir -p "$dest"
          else
            mkdir -p "$(dirname "$dest")"
            cp "$src" "$dest"
          fi
        done

    if [ -f "$RUNS_DIR/$DB_REL" ]; then
      hash_of "$RUNS_DIR/$DB_REL" > "$DB_MARKER"
    fi

    git -C "$CLONE_DIR" add -A
    if git -C "$CLONE_DIR" diff --cached --quiet; then
      echo "wardith-runs-sync: nothing changed, nothing to push." >&2
      exit 0
    fi
    git -C "$CLONE_DIR" commit -m "$msg" >/dev/null
    git -C "$CLONE_DIR" push || echo "wardith-runs-sync: push failed (network, or a conflicting remote commit) - your data is safely committed locally in $CLONE_DIR, retry the push later." >&2
    echo "wardith-runs-sync: push complete." >&2
    ;;

  *)
    echo "usage: $0 {pull|push [commit message]}" >&2
    exit 1
    ;;
esac
