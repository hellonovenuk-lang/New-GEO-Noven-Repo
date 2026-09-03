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
import getpass
import json
import os
import sys
import warnings
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
        raise SystemExit(f"Grant token exchange failed: HTTP {e.code}") from None
    if "refresh_token" not in data or "access_token" not in data:
        missing = [k for k in ("refresh_token", "access_token") if k not in data]
        raise SystemExit(f"Zoho did not return tokens - missing: {missing}")
    return data["refresh_token"], data["access_token"]


def lookup_account(api_domain, access_token):
    url = f"{api_domain}/api/accounts"
    req = urllib.request.Request(url, headers={"Authorization": f"Zoho-oauthtoken {access_token}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Account lookup failed: HTTP {e.code} {e.read().decode('utf-8', errors='replace')[:200]}")
    # Report which expected fields were missing; never interpolate the raw
    # response or account record. Same rule as exchange_grant_token above -
    # a Zoho account record carries tokens and other fields that have no
    # business being echoed to the terminal.
    accounts = data.get("data") if isinstance(data, dict) else None
    if not accounts or not isinstance(accounts, list):
        raise SystemExit(
            "Zoho returned no accounts for this token - check the Self Client "
            "was granted the ZohoMail.accounts.READ scope, then generate a new "
            "grant token and re-run this script."
        )
    account = accounts[0]
    if not isinstance(account, dict):
        raise SystemExit("Zoho's account record was not an object - cannot read accountId "
                         "or primaryEmailAddress from it.")
    missing = [k for k in ("accountId", "primaryEmailAddress") if not account.get(k)]
    if missing:
        raise SystemExit(f"Zoho's account record was missing field(s): {missing}")
    return str(account["accountId"]), account["primaryEmailAddress"]


def interactive_setup(region):
    """User-only terminal exchange; no arguments or files contain credentials."""
    if os.environ.get("GITHUB_ACTIONS") or os.environ.get("CI") or not sys.stdin.isatty() or not sys.stdout.isatty():
        raise SystemExit("Interactive setup requires a private local terminal, not CI or redirected output.")
    print("Do not record this terminal or share screenshots. Inputs are hidden.")
    with warnings.catch_warnings():
        warnings.simplefilter("error", getpass.GetPassWarning)
        try:
            client_id = getpass.getpass("New Zoho Client ID: ").strip()
            client_secret = getpass.getpass("New Zoho Client Secret: ").strip()
            print("Now generate the short-lived code in Zoho, then paste it below.")
            grant = getpass.getpass("Zoho generated code: ").strip()
        except getpass.GetPassWarning:
            raise SystemExit("Hidden input is unavailable. No credentials were read.") from None
    if not all((client_id, client_secret, grant)):
        raise SystemExit("All three inputs are required.")
    try:
        refresh, _ = exchange_grant_token(REGION_DOMAINS[region]["accounts"], client_id, client_secret, grant)
    except (urllib.error.URLError, ValueError, TypeError):
        raise SystemExit("Token exchange failed. No credentials have been displayed or saved.") from None
    input("Press Enter to display the refresh token privately for copying into Bitwarden: ")
    print(refresh)
    print("Copy only the token into Bitwarden's refresh_token field, save, then close this terminal. No file was written.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--interactive", action="store_true", help="Use hidden local prompts; display the refresh token privately without writing a file")
    ap.add_argument("--client-id")
    ap.add_argument("--client-secret")
    ap.add_argument("--grant-token")
    ap.add_argument("--region", choices=sorted(REGION_DOMAINS), required=True,
                     help="The domain in your API console URL: accounts.zoho.<region>")
    ap.add_argument("--out", default=DEFAULT_OUT_PATH)
    args = ap.parse_args()

    if args.interactive:
        if args.client_id or args.client_secret or args.grant_token:
            ap.error("Do not supply credential arguments with --interactive")
        return interactive_setup(args.region)
    if not all((args.client_id, args.client_secret, args.grant_token)):
        ap.error("Use --interactive for hidden credential entry")

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
    # A 0700 directory holding a 0600 file - playbook/records-and-data.md's
    # settled pattern for secrets on this machine (`mkdir -p ~/.noven &&
    # chmod 700`, then `chmod 600` the file). The mode is established when
    # the file is CREATED, not chmod'd on afterwards, so the refresh token
    # never sits in a default-permission file even momentarily. Every
    # permission call is best-effort: not all platforms honour POSIX modes.
    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        try:
            os.chmod(out_dir, 0o700)
        except OSError:
            pass
    fd = os.open(args.out, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        # O_CREAT's mode applies only to a file it actually creates, so tighten
        # an already-existing one too - by descriptor, before anything is
        # written through it.
        os.fchmod(fd, 0o600)
    except (AttributeError, OSError):
        pass  # no os.fchmod on Windows
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(creds, f, indent=2)

    masked = refresh_token[:6] + "..." + refresh_token[-4:] if len(refresh_token) > 10 else "***"
    print(f"Wrote {args.out}")
    print(f"  account_id:    {account_id}")
    print(f"  from_address:  {from_address}")
    print(f"  refresh_token: {masked}")
    print("Done. tools/zoho-draft-push/zoho_draft_push.py will use this file automatically.")


if __name__ == "__main__":
    main()
