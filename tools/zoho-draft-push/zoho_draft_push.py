#!/usr/bin/env python3
"""
Pushes /outreach's drafted emails into Zoho Mail as real drafts, ready for
the owner to review, edit, and send by hand.

INVARIANT, load-bearing: this file makes exactly three kinds of Zoho API
call, all to fixed paths - POST {accounts_domain}/oauth/v2/token (refresh
an access token), GET {api_domain}/api/accounts (setup_zoho_oauth.py only),
and POST/PUT {api_domain}/api/accounts/{account_id}/messages with
mode: "draft" (create or update one draft). The two domains those paths
hang off come from the credentials file, so load_credentials() checks both
against Zoho's five known regional hosts before any of them is used. No
other Zoho endpoint is referenced anywhere below - no reply, no delete, no
folder move. Those are separate Zoho API surfaces this code never calls -
NOT surfaces the granted scope is incapable of reaching. Delete and
folder-move do need scopes this token lacks, but Reply is documented under
this same ZohoMail.messages.CREATE scope, same as Send (below) - the scope
alone does not rule any of them out.

Sending is the sharpest case of this: the OAuth scope does not rule it out
at all. Zoho's "Send an Email" and "Save Draft or Template" APIs are the
SAME endpoint (POST .../messages), the same HTTP method, and the same scope
(ZohoMail.messages.CREATE is documented as valid for both). The ONLY thing
distinguishing a send from a draft-save is the request body's `mode` field.
So the safety boundary is not the scope and not endpoint separation - it is
this file's payload construction:

  build_message_payload() returns a closed dict of six literal keys
  (fromAddress, toAddress, subject, content, mailFormat, mode) with mode
  hardcoded to "draft" unconditionally. Entry data is only ever read out of
  named fields into named values; no entry dict is ever merged, spread, or
  update()d into the payload. So no business's outreach content can reach
  or override `mode`, whatever it contains.

test_zoho_draft_push.py's DraftModeInvariantTests enforces both halves of
that - mode == "draft" and the exact key set - on every payload this file
builds and on every body it would put on the wire. A future edit that adds
a send path must consciously violate this stated rule and delete those
tests, not just add a line.

Reads the outreach-prep-<slug>-<date>.json file /outreach's Stage 7 writes
(a JSON array, one object per business - see .claude/skills/outreach/
SKILL.md Stage 7 for the full field list) and writes zoho_draft_id/
zoho_push_status/zoho_push_action/zoho_pushed_at back into each entry that
was processed, so a re-run updates the existing Zoho draft instead of
creating a duplicate.

Usage:
  python3 zoho_draft_push.py --input outreach-prep.json --in-place
  python3 zoho_draft_push.py --input outreach-prep.json --in-place --dry-run
"""
import argparse
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

DEFAULT_CREDENTIALS_PATH = os.path.expanduser("~/.wardith/zoho-credentials.json")
REQUIRED_CREDENTIAL_FIELDS = [
    "client_id", "client_secret", "refresh_token", "account_id",
    "from_address", "api_domain", "accounts_domain",
]

# Zoho's five regional hosts. Both of these values come out of a file on disk
# and are interpolated straight into request URLs - the api_domain alongside
# the OAuth bearer token - so this file checks them itself rather than
# trusting whatever wrote the file. Deliberately duplicated from
# setup_zoho_oauth.py's REGION_DOMAINS rather than imported: these two
# scripts share no imports by design (each is standalone and stdlib-only),
# and this is the reading end's own check on input it did not produce. Keep
# the two lists in step if Zoho ever adds a region.
ZOHO_ACCOUNTS_DOMAINS = frozenset([
    "https://accounts.zoho.com", "https://accounts.zoho.eu",
    "https://accounts.zoho.in", "https://accounts.zoho.com.au",
    "https://accounts.zoho.jp",
])
ZOHO_API_DOMAINS = frozenset([
    "https://mail.zoho.com", "https://mail.zoho.eu", "https://mail.zoho.in",
    "https://mail.zoho.com.au", "https://mail.zoho.jp",
])


class ZohoAPIError(Exception):
    pass


# Every message built from a remote response goes through this. Those
# messages get printed to the terminal by main() and, via zoho_push_status,
# written into the outreach-prep JSON - so an oversized or hostile response
# body must never land there whole, and a body that echoes the request back
# must not copy a recipient address along with it. Same rule as the one
# already applied to setup_zoho_oauth.py's exchange_grant_token: say what was
# wrong, never repeat the response verbatim.
_EMAIL_SHAPED = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
DETAIL_LIMIT = 200


def _safe_detail(value, limit=DETAIL_LIMIT):
    """Truncate a remote-supplied string and redact address-shaped
    substrings from it. Not a general sanitiser - a bound and an obvious
    redaction, sized to keep an error legible without persisting a payload."""
    text = value if isinstance(value, str) else repr(value)
    text = _EMAIL_SHAPED.sub("[address redacted]", text)
    if len(text) > limit:
        text = text[:limit] + f"... [truncated, {len(text)} chars]"
    return text


def load_credentials(path=None):
    """Reads the Zoho credentials file setup_zoho_oauth.py writes. Never
    called with real credentials in a test - path always points at a
    fixture file or a nonexistent one."""
    path = path or os.environ.get("WARDITH_ZOHO_CREDENTIALS") or DEFAULT_CREDENTIALS_PATH
    if not os.path.exists(path):
        raise ZohoAPIError(
            f"credentials file not found at {path} - run "
            f"tools/zoho-draft-push/setup_zoho_oauth.py first "
            f"(see tools/zoho-draft-push/README.md)"
        )
    with open(path, "r", encoding="utf-8") as f:
        creds = json.load(f)
    missing = [field for field in REQUIRED_CREDENTIAL_FIELDS if field not in creds]
    if missing:
        raise ZohoAPIError(f"credentials file at {path} is missing field(s): {missing}")
    for field, allowed in (("api_domain", ZOHO_API_DOMAINS),
                           ("accounts_domain", ZOHO_ACCOUNTS_DOMAINS)):
        if creds[field] not in allowed:
            # Name the field, never the rejected value - it goes to the
            # terminal and this file's other fields are secrets.
            raise ZohoAPIError(
                f"credentials file at {path} has an unrecognised {field} - "
                f"expected one of {sorted(allowed)}. Re-run "
                f"tools/zoho-draft-push/setup_zoho_oauth.py to regenerate it."
            )
    return creds


def refresh_access_token(credentials):
    """Exchanges the stored long-lived refresh_token for a short-lived
    access_token. This is the ONLY call this file makes to the accounts
    (OAuth) domain - never a login, never a password."""
    url = f"{credentials['accounts_domain']}/oauth/v2/token"
    params = urllib.parse.urlencode({
        "refresh_token": credentials["refresh_token"],
        "client_id": credentials["client_id"],
        "client_secret": credentials["client_secret"],
        "grant_type": "refresh_token",
    }).encode("utf-8")
    req = urllib.request.Request(url, data=params, method="POST",
                                  headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp_data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = _safe_detail(e.read().decode("utf-8", errors="replace"))
        raise ZohoAPIError(f"token refresh failed: HTTP {e.code} {detail}")
    except urllib.error.URLError as e:
        raise ZohoAPIError(f"token refresh failed: {e.reason}")
    token = resp_data.get("access_token") if isinstance(resp_data, dict) else None
    if not token:
        # Name the missing field only. main() prints this straight to the
        # terminal, and the response body can carry other tokens.
        raise ZohoAPIError(
            "token refresh response was missing field(s): ['access_token'] - "
            "the refresh token may have been revoked; re-run "
            "tools/zoho-draft-push/setup_zoho_oauth.py"
        )
    return token


def _to_html(text):
    """Plain-text email body (paragraphs separated by a blank line) to
    simple HTML - tables/inline-styles-only-signature territory doesn't
    apply here, this is just the message text, not the signature."""
    paragraphs = [p.strip() for p in text.strip().split("\n\n") if p.strip()]
    return "".join(f"<p>{html.escape(p)}</p>" for p in paragraphs)


def build_message_payload(entry, from_address):
    """Maps one outreach-prep entry (as written by /outreach's Stage 7) to
    the JSON body for Zoho's create/update-draft call. Never includes a
    signature - that is Zoho's own "new mail" setting, per
    assets/brand/email-signature.html's own instructions.

    This dict literal is the tool's whole send/draft safety boundary (see
    the module docstring): a closed set of six keys, `mode` hardcoded to
    "draft", entry data read only into named values and never merged in.
    Do not add a key here that is derived from `entry`, and never set
    `mode` from anything but this literal."""
    return {
        "fromAddress": from_address,
        "toAddress": entry.get("contact_route", {}).get("email", ""),
        "subject": entry.get("email_subject", ""),
        "content": _to_html(entry.get("email_body", "")),
        "mailFormat": "html",
        "mode": "draft",
    }


def _is_valid_draft_id(value):
    """Zoho message ids are numeric strings. This one comes from Zoho's own
    earlier response, but it round trips through a JSON file on disk before
    being interpolated into a URL path - so check it there. Defence in depth,
    not the primary control."""
    return isinstance(value, str) and value.isdigit() and 1 <= len(value) <= 32


def _extract_draft_id(resp_data):
    if not isinstance(resp_data, dict):
        raise ZohoAPIError(f"unexpected Zoho response shape (not a dict): {_safe_detail(resp_data)}")
    data = resp_data.get("data")
    if isinstance(data, dict) and data.get("messageId"):
        return str(data["messageId"])
    if isinstance(data, list) and data:
        if isinstance(data[0], dict) and data[0].get("messageId"):
            return str(data[0]["messageId"])
    raise ZohoAPIError(
        f"unexpected Zoho response shape (no data.messageId): {_safe_detail(resp_data)}")


def push_entry(entry, from_address, api_domain, account_id, access_token, dry_run=False):
    """Creates or updates exactly one Zoho draft for one outreach-prep
    entry. Never raises - every failure mode (HTTP error, connection
    failure, a read that dies mid-response, unexpected response shape, and
    anything else) is caught and returned as a FAILED status, so one
    business's problem never stops the batch (see process_outreach_prep) and
    never costs the batch the draft ids it has already earned."""
    if entry.get("withheld"):
        return {"zoho_push_status": "SKIPPED (withheld)"}

    existing_id = entry.get("zoho_draft_id")
    action = "updated" if existing_id else "created"

    if dry_run:
        payload = build_message_payload(entry, from_address)
        dry_action = "update" if existing_id else "create"
        print(f"[dry-run] would {dry_action} draft for {entry.get('business', '?')!r}: "
              f"to={payload['toAddress']!r} subject={payload['subject']!r}")
        return {"zoho_push_status": f"DRY-RUN ({dry_action})", "zoho_push_action": dry_action}

    if existing_id and not _is_valid_draft_id(existing_id):
        return {"zoho_push_status": "FAILED: stored zoho_draft_id is not a valid Zoho "
                                    "message id (expected digits only) - delete it from this "
                                    "entry to push a new draft"}

    payload = build_message_payload(entry, from_address)
    url = f"{api_domain}/api/accounts/{account_id}/messages"
    if existing_id:
        # UNVERIFIED, pending the owner's first real setup run: Zoho's public
        # docs cover creating a draft at this path but do not clearly document
        # PUT .../messages/{messageId} for updating one. If the first re-run of
        # a campaign reports "FAILED: HTTP 404/405" for every already-pushed
        # business, this branch is the reason - the fix would be to delete the
        # old draft by hand and let the create path run, or to find whatever
        # update call Zoho does support. Flagged in README.md too.
        url = f"{url}/{existing_id}"
        method = "PUT"
    else:
        method = "POST"

    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), method=method,
        headers={"Authorization": f"Zoho-oauthtoken {access_token}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp_data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = _safe_detail(e.read().decode("utf-8", errors="replace"))
        if existing_id and e.code == 404:
            # The stored draft is gone - most likely the owner deleted or sent
            # it in Zoho. Clear the id rather than leaving this entry stuck
            # PUTting forever at a message that no longer exists; the next run
            # takes the create branch and makes a fresh draft.
            return {
                "zoho_draft_id": None,
                "zoho_push_status": "FAILED: HTTP 404 - the stored draft may have been deleted "
                                    "in Zoho; its id has been cleared, so the next run will "
                                    "create a new draft",
            }
        return {"zoho_push_status": f"FAILED: HTTP {e.code} {detail}"}
    except urllib.error.URLError as e:
        return {"zoho_push_status": f"FAILED: {e.reason}"}
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return {"zoho_push_status": f"FAILED: malformed response ({type(e).__name__})"}
    except Exception as e:  # noqa: BLE001 - deliberate, see below
        # A connection dropped *after* the response headers arrive raises out
        # of resp.read() as http.client.IncompleteRead, ConnectionResetError,
        # or a read-phase TimeoutError - none of which urllib wraps in
        # URLError. If one of those escaped this function, main() would die
        # before writing the JSON file at all, discarding every zoho_draft_id
        # already earned earlier in the same batch even though those drafts
        # exist in the real mailbox - and the next run would create duplicates.
        # This function's contract is that it never raises; this keeps it.
        return {"zoho_push_status": f"FAILED: {type(e).__name__}"}

    # Validate the response envelope on BOTH paths. On the update path we
    # already hold the id and don't need the one this yields - but an API can
    # answer HTTP 200 with an error body, and "OK, updated" must never be
    # recorded for a call that actually failed. A shape _extract_draft_id
    # rejects is a real failure here exactly as it is on the create path.
    try:
        returned_id = _extract_draft_id(resp_data)
    except ZohoAPIError as e:
        return {"zoho_push_status": f"FAILED: {e}"}
    draft_id = existing_id or returned_id

    return {
        "zoho_draft_id": draft_id,
        "zoho_push_status": "OK",
        "zoho_push_action": action,
        "zoho_pushed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def process_outreach_prep(entries, credentials, access_token, dry_run=False):
    """entries: the JSON array from an outreach-prep-<slug>-<date>.json
    file, loaded and passed in by main(). Mutates each entry in place with
    the zoho_* fields; returns the same information as a flat list for
    summarize()."""
    from_address = credentials["from_address"] if credentials else "(dry-run: no credentials loaded)"
    api_domain = credentials["api_domain"] if credentials else None
    account_id = credentials["account_id"] if credentials else None

    results = []
    for entry in entries:
        outcome = push_entry(entry, from_address, api_domain, account_id, access_token, dry_run=dry_run)
        entry.update(outcome)
        results.append({"business": entry.get("business", "?"), **outcome})
    return results


def summarize(results):
    counts = {"created": 0, "updated": 0, "failed": 0, "skipped": 0, "dry_run": 0}
    failures = []
    for r in results:
        status = r.get("zoho_push_status", "")
        action = r.get("zoho_push_action")
        if status == "OK" and action == "created":
            counts["created"] += 1
        elif status == "OK" and action == "updated":
            counts["updated"] += 1
        elif status.startswith("FAILED"):
            counts["failed"] += 1
            failures.append(f"  {r.get('business', '?')}: {status}")
        elif status.startswith("SKIPPED"):
            counts["skipped"] += 1
        elif status.startswith("DRY-RUN"):
            counts["dry_run"] += 1
    lines = [
        f"Zoho draft push: {counts['created']} created, {counts['updated']} updated, "
        f"{counts['failed']} failed, {counts['skipped']} skipped (withheld), "
        f"{counts['dry_run']} dry-run."
    ]
    lines.extend(failures)
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, help="outreach-prep-<slug>-<date>.json from /outreach's Stage 7")
    ap.add_argument("--output", help="Path to write the updated outreach-prep JSON")
    ap.add_argument("--in-place", action="store_true", help="Overwrite --input instead")
    ap.add_argument("--credentials", help="Path to Zoho credentials JSON (default: ~/.wardith/zoho-credentials.json or $WARDITH_ZOHO_CREDENTIALS)")
    ap.add_argument("--dry-run", action="store_true", help="Log what would be pushed without calling Zoho or requiring credentials")
    args = ap.parse_args()
    if not args.output and not args.in_place:
        print("Specify --output PATH or --in-place", file=sys.stderr)
        sys.exit(2)

    with open(args.input, "r", encoding="utf-8") as f:
        entries = json.load(f)

    credentials = None
    access_token = None
    if not args.dry_run:
        try:
            credentials = load_credentials(args.credentials)
            access_token = refresh_access_token(credentials)
        except ZohoAPIError as e:
            print(f"Zoho setup error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            credentials = load_credentials(args.credentials)
        except ZohoAPIError:
            credentials = None  # dry-run works even before setup_zoho_oauth.py has ever run

    results = process_outreach_prep(entries, credentials, access_token, dry_run=args.dry_run)

    out_path = args.input if args.in_place else args.output
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    print(summarize(results))


if __name__ == "__main__":
    main()
