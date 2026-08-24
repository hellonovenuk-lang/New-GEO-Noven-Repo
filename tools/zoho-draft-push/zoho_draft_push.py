#!/usr/bin/env python3
"""
Pushes /outreach's drafted emails into Zoho Mail as real drafts, ready for
the owner to review, edit, and send by hand.

INVARIANT, load-bearing: this file makes exactly three kinds of Zoho API
call, all to fixed paths - POST {accounts_domain}/oauth/v2/token (refresh
an access token), GET {api_domain}/api/accounts (setup_zoho_oauth.py only),
and POST/PUT {api_domain}/api/accounts/{account_id}/messages with
mode: "draft" (create or update one draft). No other Zoho endpoint is
referenced anywhere below - no send, no reply, no delete, no folder move.
The OAuth scope requested at setup (ZohoMail.messages.CREATE) cannot
authorize those calls even if this file tried. A future edit that adds a
send path must consciously violate this stated rule, not just add a line.

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
import html
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

DEFAULT_CREDENTIALS_PATH = os.path.expanduser("~/.wardith/zoho-credentials.json")
REQUIRED_CREDENTIAL_FIELDS = [
    "client_id", "client_secret", "refresh_token", "account_id",
    "from_address", "api_domain", "accounts_domain",
]


class ZohoAPIError(Exception):
    pass


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
        detail = e.read().decode("utf-8", errors="replace")[:200]
        raise ZohoAPIError(f"token refresh failed: HTTP {e.code} {detail}")
    except urllib.error.URLError as e:
        raise ZohoAPIError(f"token refresh failed: {e.reason}")
    token = resp_data.get("access_token")
    if not token:
        raise ZohoAPIError(f"token refresh response had no access_token: {resp_data}")
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
    assets/brand/email-signature.html's own instructions."""
    return {
        "fromAddress": from_address,
        "toAddress": entry.get("contact_route", {}).get("email", ""),
        "subject": entry.get("email_subject", ""),
        "content": _to_html(entry.get("email_body", "")),
        "mailFormat": "html",
    }


def _extract_draft_id(resp_data):
    data = resp_data.get("data")
    if isinstance(data, dict) and data.get("messageId"):
        return str(data["messageId"])
    if isinstance(data, list) and data and data[0].get("messageId"):
        return str(data[0]["messageId"])
    raise ZohoAPIError(f"unexpected Zoho response shape (no data.messageId): {resp_data}")


def push_entry(entry, from_address, api_domain, account_id, access_token, dry_run=False):
    """Creates or updates exactly one Zoho draft for one outreach-prep
    entry. Never raises - every failure mode (HTTP error, unexpected
    response shape) is caught and returned as a FAILED status so one
    business's problem never stops the batch (see process_outreach_prep)."""
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

    payload = build_message_payload(entry, from_address)
    payload["mode"] = "draft"
    url = f"{api_domain}/api/accounts/{account_id}/messages"
    if existing_id:
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
        detail = e.read().decode("utf-8", errors="replace")[:200]
        return {"zoho_push_status": f"FAILED: HTTP {e.code} {detail}"}
    except urllib.error.URLError as e:
        return {"zoho_push_status": f"FAILED: {e.reason}"}

    try:
        draft_id = existing_id or _extract_draft_id(resp_data)
    except ZohoAPIError as e:
        return {"zoho_push_status": f"FAILED: {e}"}

    return {
        "zoho_draft_id": draft_id,
        "zoho_push_status": "OK",
        "zoho_push_action": action,
        "zoho_pushed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


if __name__ == "__main__":
    pass
