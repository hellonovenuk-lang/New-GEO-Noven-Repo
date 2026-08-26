#!/usr/bin/env python3
"""
Structured, read-only access to Companies House's public data API, standing
in for the manual WebFetch/WebSearch browsing `/qualify` Stage 5 has always
used to verify a business is a real, active Ltd company or LLP.

INVARIANT, load-bearing: this file makes exactly two kinds of Companies
House API call, both GET, both read-only - GET {API_BASE}/search/companies
(name search) and GET {API_BASE}/company/{company_number} (a single
company's profile). No other endpoint is referenced anywhere below, and
nothing here can create, update, or delete anything at Companies House -
there is no such capability in this API for a public API key to begin with.

This tool does not replace the judgement `/qualify` Stage 5 already applies
- a defensible, active Ltd/LLP match, never a guess. A name search can
return several plausible candidates (a chain, a similarly-named firm, a
dissolved-then-reincorporated entity); picking the right one, or deciding
none is defensible and the business stays REVIEW, is still a human/agent
call made from the structured data this returns. What this replaces is the
manual page-scraping, not the verification step itself.

Auth: Companies House uses HTTP Basic Auth with the API key as the
username and an empty password - not OAuth, not a bearer token. Get a free
key at https://developer.company-information.service.gov.uk/ (see
README.md for the one-time setup) and set COMPANIES_HOUSE_API_KEY.

Usage:
  python3 company_lookup.py --name "Acme Ltd"
  python3 company_lookup.py --number 12345678
  python3 company_lookup.py --name "Acme Ltd" --json
"""
import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://api.company-information.service.gov.uk"
DEFAULT_ITEMS_PER_PAGE = 20


class CompaniesHouseError(Exception):
    pass


# Same discipline as tools/zoho-draft-push/zoho_draft_push.py's _safe_detail:
# a remote-supplied error body must never be echoed back whole - it gets
# printed to the terminal and could be arbitrarily large or malformed.
DETAIL_LIMIT = 200


def _safe_detail(value, limit=DETAIL_LIMIT):
    text = value if isinstance(value, str) else repr(value)
    if len(text) > limit:
        text = text[:limit] + f"... [truncated, {len(text)} chars]"
    return text


def resolve_api_key(explicit=None):
    """--api-key wins if given; otherwise COMPANIES_HOUSE_API_KEY, per
    playbook/records-and-data.md's ~/.noven/env convention for every other
    provider key. Raises rather than making a call with no key, since an
    unauthenticated request to this API returns a 401 that would otherwise
    look like a generic network failure."""
    key = explicit or os.environ.get("COMPANIES_HOUSE_API_KEY")
    if not key:
        raise CompaniesHouseError(
            "no Companies House API key found - pass --api-key or set "
            "COMPANIES_HOUSE_API_KEY (see tools/companies-house/README.md "
            "for how to get a free key)"
        )
    return key


def _auth_header(api_key):
    token = base64.b64encode(f"{api_key}:".encode("ascii")).decode("ascii")
    return f"Basic {token}"


def _get(path, api_key, params=None):
    """One GET against the Companies House API. Never raises anything but
    CompaniesHouseError."""
    url = f"{API_BASE}{path}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, method="GET",
                                  headers={"Authorization": _auth_header(api_key)})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = _safe_detail(e.read().decode("utf-8", errors="replace"))
        if e.code == 401:
            raise CompaniesHouseError(
                "Companies House rejected the API key (HTTP 401) - check "
                "COMPANIES_HOUSE_API_KEY is set to a valid key from "
                "https://developer.company-information.service.gov.uk/"
            )
        if e.code == 404:
            raise CompaniesHouseError(f"not found (HTTP 404): {path}")
        raise CompaniesHouseError(f"Companies House request failed: HTTP {e.code} {detail}")
    except urllib.error.URLError as e:
        raise CompaniesHouseError(f"Companies House request failed: {e.reason}")
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise CompaniesHouseError(f"malformed Companies House response ({type(e).__name__})")


def search_companies(name, api_key, items_per_page=DEFAULT_ITEMS_PER_PAGE):
    """Returns a list of candidate matches for a company name search, each
    a dict with at least title/company_number/company_status/company_type/
    address_snippet/date_of_creation - never more than one page (this tool
    is for picking a defensible match among a handful of candidates, not
    for building a market census; Stage 2's census comes from elsewhere,
    per playbook/outreach-process.md step 3)."""
    if not name or not name.strip():
        raise CompaniesHouseError("search_companies requires a non-empty name")
    data = _get("/search/companies", api_key,
                {"q": name.strip(), "items_per_page": items_per_page})
    items = data.get("items") if isinstance(data, dict) else None
    if not isinstance(items, list):
        raise CompaniesHouseError(f"unexpected search response shape: {_safe_detail(data)}")
    return items


_COMPANY_NUMBER_RE = re.compile(r"^[A-Za-z0-9]{1,10}$")


def get_company_profile(company_number, api_key):
    """Returns the full profile dict for a single company number - company
    status, type, name, registered office address, incorporation date."""
    company_number = (company_number or "").strip()
    if not _COMPANY_NUMBER_RE.match(company_number):
        raise CompaniesHouseError(f"not a valid Companies House number: {company_number!r}")
    data = _get(f"/company/{company_number}", api_key)
    if not isinstance(data, dict) or "company_number" not in data:
        raise CompaniesHouseError(f"unexpected profile response shape: {_safe_detail(data)}")
    return data


def _format_address(address_dict):
    if not isinstance(address_dict, dict):
        return ""
    parts = [address_dict.get(k) for k in
             ("premises", "address_line_1", "address_line_2", "locality",
              "region", "postal_code", "country")]
    return ", ".join(p for p in parts if p)


def _print_search_results(items):
    if not items:
        print("No candidates found.")
        return
    for item in items:
        print(f"{item.get('title', '?')}  |  {item.get('company_number', '?')}  |  "
              f"status={item.get('company_status', '?')}  |  "
              f"type={item.get('company_type', '?')}  |  "
              f"{item.get('address_snippet', '')}")


def _print_profile(profile):
    print(f"{profile.get('company_name', '?')}  |  {profile.get('company_number', '?')}")
    print(f"  status: {profile.get('company_status', '?')}")
    print(f"  type: {profile.get('type', '?')}")
    print(f"  incorporated: {profile.get('date_of_creation', '?')}")
    address = _format_address(profile.get("registered_office_address"))
    if address:
        print(f"  registered office: {address}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--name", help="Search for candidate companies by name")
    group.add_argument("--number", help="Look up a single company's profile by company number")
    ap.add_argument("--api-key", help="Companies House API key (default: $COMPANIES_HOUSE_API_KEY)")
    ap.add_argument("--items-per-page", type=int, default=DEFAULT_ITEMS_PER_PAGE)
    ap.add_argument("--json", action="store_true", help="Print raw JSON instead of a formatted summary")
    args = ap.parse_args(argv)

    try:
        api_key = resolve_api_key(args.api_key)
        if args.name:
            result = search_companies(args.name, api_key, items_per_page=args.items_per_page)
        else:
            result = get_company_profile(args.number, api_key)
    except CompaniesHouseError as e:
        print(f"Companies House error: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.name:
        _print_search_results(result)
    else:
        _print_profile(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
