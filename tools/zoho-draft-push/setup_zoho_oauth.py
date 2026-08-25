#!/usr/bin/env python3
"""
One-time setup: exchanges a Zoho "Self Client" grant token for a
long-lived refresh token, looks up the account id and primary email
address, and writes everything zoho_draft_push.py needs to
~/.wardith/zoho-credentials.json (or --out).

Run this once, after registering a Self Client at api-console.zoho.com
with scopes ZohoMail.messages.CREATE and ZohoMail.accounts.READ, and
generating a grant token there. See README.md in this folder for the
full walkthrough - the client id, client secret, and grant token below
all come from that console, never from this script or from Claude.

Usage:
  python3 setup_zoho_oauth.py --client-id ID --client-secret SECRET \
      --grant-token TOKEN --region eu
"""
import argparse
import json
import os
import urllib.error
import urllib.parse
import urllib.request

REGION_DOMAINS = {
    "com": {"accounts": "https://accounts.zoho.com", "api": "https://mail.zoho.com"},
    "eu": {"accounts": "https://accounts.zoho.eu", "api": "https://mail.zoho.eu"},
    "in": {"accounts": "https://accounts.zoho.in", "api": "https://mail.zoho.in"},
    "au": {"accounts": "https://accounts.zoho.com.au", "api": "https://mail.zoho.com.au"},
    "jp": {"accounts": "https://accounts.zoho.jp", "api": "https://mail.zoho.jp"},
}

DEFAULT_OUT_PATH = os.path.expanduser("~/.wardith/zoho-credentials.json")


def exchange_grant_token(accounts_domain, client_id, client_secret, grant_token):
    url = f"{accounts_domain}/oauth/v2/token"
    params = urllib.parse.urlencode({
        "code": grant_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
    }).encode("utf-8")
    req = urllib.request.Request(url, data=params, method="POST",
                                  headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Grant token exchange failed: HTTP {e.code} {e.read().decode('utf-8', errors='replace')[:200]}")
    if "refresh_token" not in data or "access_token" not in data:
        raise SystemExit(f"Zoho did not return tokens - response: {data}")
    return data["refresh_token"], data["access_token"]


def lookup_account(api_domain, access_token):
    url = f"{api_domain}/api/accounts"
    req = urllib.request.Request(url, headers={"Authorization": f"Zoho-oauthtoken {access_token}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Account lookup failed: HTTP {e.code} {e.read().decode('utf-8', errors='replace')[:200]}")
    accounts = data.get("data", [])
    if not accounts:
        raise SystemExit(f"Zoho returned no accounts for this token - response: {data}")
    account = accounts[0]
    account_id = account.get("accountId")
    from_address = account.get("primaryEmailAddress")
    if not account_id or not from_address:
        raise SystemExit(f"Could not find accountId/primaryEmailAddress in Zoho's response: {account}")
    return str(account_id), from_address


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--client-id", required=True)
    ap.add_argument("--client-secret", required=True)
    ap.add_argument("--grant-token", required=True)
    ap.add_argument("--region", choices=sorted(REGION_DOMAINS), required=True,
                     help="The domain in your API console URL: accounts.zoho.<region>")
    ap.add_argument("--out", default=DEFAULT_OUT_PATH)
    args = ap.parse_args()

    domains = REGION_DOMAINS[args.region]
    print(f"Exchanging grant token via {domains['accounts']} ...")
    refresh_token, access_token = exchange_grant_token(
        domains["accounts"], args.client_id, args.client_secret, args.grant_token)
    print("Got a refresh token. Looking up your account id and address ...")
    account_id, from_address = lookup_account(domains["api"], access_token)

    creds = {
        "client_id": args.client_id,
        "client_secret": args.client_secret,
        "refresh_token": refresh_token,
        "account_id": account_id,
        "from_address": from_address,
        "api_domain": domains["api"],
        "accounts_domain": domains["accounts"],
    }
    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(creds, f, indent=2)
    try:
        os.chmod(args.out, 0o600)
    except OSError:
        pass  # best-effort; not all platforms support POSIX permissions

    masked = refresh_token[:6] + "..." + refresh_token[-4:] if len(refresh_token) > 10 else "***"
    print(f"Wrote {args.out}")
    print(f"  account_id:    {account_id}")
    print(f"  from_address:  {from_address}")
    print(f"  refresh_token: {masked}")
    print("Done. tools/zoho-draft-push/zoho_draft_push.py will use this file automatically.")


if __name__ == "__main__":
    main()
