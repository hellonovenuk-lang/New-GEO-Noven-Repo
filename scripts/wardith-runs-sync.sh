#!/bin/bash
# Syncs ~/wardith-runs/ (trade-run CSVs, campaign folders, outreach prep,
# and the CRM's wardith.db) against a private GitHub repo,
# hellonovenuk-lang/wardith-crm-data, so this data survives between an
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
# call the add_repo tool for hellonovenuk-lang/wardith-crm-data
# (access: "push") and run the clone command that tool returns, cloning to
# ~/.wardith-runs-repo/. Once that clone exists, `pull`/`push` here work the
# same on cloud and local.
#
# Local sessions: if ~/.wardith-runs-repo/ doesn't exist yet, `pull`
# clones it directly - your own git credentials already work here, same as
# any other repo on this machine.
#
# Safety: wardith.db is the one file more than one place writes to (the CRM
# app locally, `ingest` from any session), so it is guarded in BOTH
# directions:
#
#   pull - refuses to overwrite a local wardith.db that has changed since the
#          last sync, rather than silently discarding hand-entered CRM
#          notes/activity that only exist locally. Run `push` first.
#   push - refuses to replace the repo's wardith.db with one holding FEWER
#          rows in any core table. A session that never pulled successfully
#          (a cloud run where the repo was never attached, say) starts from an
#          empty database; ingesting one campaign into that and pushing used
#          to overwrite every other campaign, activity, cadence row and
#          contact hold in the repo. That happened on 2026-09-05 and cost 7
#          campaigns, 10 activity records, 20 cadence settings and 2 holds.
#          Override with WARDITH_SYNC_ALLOW_SHRINK=1 only when the shrink is
#          genuinely intended.
#
# Everything else under ~/wardith-runs/ is per-run, per-slug output that's
# never edited by more than one place at once in practice, so it's synced as
# a plain overwrite.
set -uo pipefail

REPO_URL="https://github.com/hellonovenuk-lang/wardith-crm-data.git"
CLONE_DIR="$HOME/.wardith-runs-repo"
RUNS_DIR="$HOME/wardith-runs"
DB_REL="crm/wardith.db"
DB_MARKER="$RUNS_DIR/crm/.last-synced-db-hash"

hash_of() {
  [ -f "$1" ] && sha256sum "$1" 2>/dev/null | awk '{print $1}'
}

# Row counts for the CRM tables whose loss is not recoverable from a re-ingest.
# import_log is deliberately excluded: it churns and shrinking it is harmless.
db_counts() {
  python3 - "$1" <<'PY'
import sqlite3, sys
tables = ["campaigns", "prospects", "activities", "cadence_settings",
          "clients", "client_activities"]
try:
    con = sqlite3.connect("file:%s?mode=ro" % sys.argv[1], uri=True)
    have = {r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    for t in tables:
        n = con.execute("SELECT COUNT(*) FROM %s" % t).fetchone()[0] if t in have else 0
        print(t, n)
except Exception as exc:
    print("db_counts: %s" % exc, file=sys.stderr)
    sys.exit(1)
PY
}

cmd="${1:-}"

case "$cmd" in
  pull)
    if [ ! -d "$CLONE_DIR/.git" ]; then
      if [ "${CLAUDE_CODE_REMOTE:-}" = "true" ]; then
        echo "wardith-runs-sync: $CLONE_DIR not found. In a cloud session, call add_repo for hellonovenuk-lang/wardith-crm-data (access: push) and clone it there first - this script never attaches a repo itself." >&2
        exit 0
      fi
      echo "wardith-runs-sync: cloning $REPO_URL to $CLONE_DIR" >&2
      git clone "$REPO_URL" "$CLONE_DIR" || {
        echo "wardith-runs-sync: clone failed - continuing with no synced data. Create hellonovenuk-lang/wardith-crm-data if it doesn't exist yet." >&2
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

    # Never let a thinner database overwrite a fuller one - see the header.
    if [ -f "$RUNS_DIR/$DB_REL" ] && [ -f "$CLONE_DIR/$DB_REL" ]; then
      mine="$(db_counts "$RUNS_DIR/$DB_REL")" || {
        echo "wardith-runs-sync: cannot read $RUNS_DIR/$DB_REL - refusing to push a database this script cannot verify." >&2; exit 1; }
      theirs="$(db_counts "$CLONE_DIR/$DB_REL")" || {
        echo "wardith-runs-sync: cannot read the repo's $DB_REL - refusing to push over a database this script cannot verify." >&2; exit 1; }
      shrink=""
      while read -r table n; do
        m="$(printf '%s\n' "$theirs" | awk -v t="$table" '$1==t{print $2}')"
        [ -n "$m" ] || continue
        if [ "$n" -lt "$m" ]; then
          shrink="${shrink}  ${table}: ${m} in the repo, ${n} here"$'\n'
        fi
      done <<EOF
$mine
EOF
      if [ -n "$shrink" ]; then
        if [ "${WARDITH_SYNC_ALLOW_SHRINK:-}" = "1" ]; then
          echo "wardith-runs-sync: pushing a SMALLER database because WARDITH_SYNC_ALLOW_SHRINK=1:" >&2
          printf '%s' "$shrink" >&2
        else
          echo "wardith-runs-sync: REFUSING to push - the local database has fewer rows than the repo's:" >&2
          printf '%s' "$shrink" >&2
          echo "wardith-runs-sync: this is what silently destroys other campaigns' history. Run 'pull' first and re-ingest on top of the repo's database. If the shrink is genuinely intended, re-run with WARDITH_SYNC_ALLOW_SHRINK=1." >&2
          exit 1
        fi
      fi
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
