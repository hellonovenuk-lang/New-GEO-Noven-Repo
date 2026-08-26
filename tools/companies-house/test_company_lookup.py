#!/usr/bin/env python3
"""
Tests for company_lookup.py. No real network calls and no real Companies
House API key anywhere in this file - every urllib.request.urlopen call is
mocked. Fictitious data only, same convention as
tools/zoho-draft-push/test_zoho_draft_push.py.

Run: python3 test_company_lookup.py -v
"""
import base64
import io
import json
import os
import unittest
import urllib.error
from unittest.mock import patch

import company_lookup as cl


class _FakeResponse:
    def __init__(self, payload):
        self._body = json.dumps(payload).encode("utf-8")

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def _http_error(code, body_dict):
    body = json.dumps(body_dict).encode("utf-8")
    return urllib.error.HTTPError(url="https://x", code=code, msg="error", hdrs=None, fp=io.BytesIO(body))


FAKE_KEY = "fake-test-key-not-real"

SEARCH_RESPONSE = {
    "items": [
        {
            "title": "ACME PLUMBING LTD",
            "company_number": "12345678",
            "company_status": "active",
            "company_type": "ltd",
            "address_snippet": "1 Fake Street, Chester, CH1 1AA",
            "date_of_creation": "2015-03-01",
        },
        {
            "title": "ACME PLUMBING (NORTH) LTD",
            "company_number": "87654321",
            "company_status": "dissolved",
            "company_type": "ltd",
            "address_snippet": "2 Fake Street, Wirral, CH2 2BB",
            "date_of_creation": "2010-01-01",
        },
    ],
    "items_per_page": 20,
    "total_results": 2,
}

PROFILE_RESPONSE = {
    "company_name": "ACME PLUMBING LTD",
    "company_number": "12345678",
    "company_status": "active",
    "type": "ltd",
    "date_of_creation": "2015-03-01",
    "registered_office_address": {
        "premises": "1",
        "address_line_1": "Fake Street",
        "locality": "Chester",
        "postal_code": "CH1 1AA",
        "country": "United Kingdom",
    },
}


class ResolveApiKeyTests(unittest.TestCase):
    def test_explicit_key_wins(self):
        with patch.dict(os.environ, {"COMPANIES_HOUSE_API_KEY": "env-key"}):
            self.assertEqual(cl.resolve_api_key("explicit-key"), "explicit-key")

    def test_falls_back_to_env(self):
        with patch.dict(os.environ, {"COMPANIES_HOUSE_API_KEY": "env-key"}):
            self.assertEqual(cl.resolve_api_key(None), "env-key")

    def test_raises_when_neither_set(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(cl.CompaniesHouseError):
                cl.resolve_api_key(None)


class AuthHeaderTests(unittest.TestCase):
    def test_basic_auth_with_empty_password(self):
        header = cl._auth_header("mykey")
        self.assertTrue(header.startswith("Basic "))
        decoded = base64.b64decode(header.split(" ", 1)[1]).decode("ascii")
        self.assertEqual(decoded, "mykey:")


class SearchCompaniesTests(unittest.TestCase):
    def test_requires_non_empty_name(self):
        with self.assertRaises(cl.CompaniesHouseError):
            cl.search_companies("", FAKE_KEY)
        with self.assertRaises(cl.CompaniesHouseError):
            cl.search_companies("   ", FAKE_KEY)

    @patch("urllib.request.urlopen")
    def test_returns_items(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse(SEARCH_RESPONSE)
        items = cl.search_companies("Acme Plumbing", FAKE_KEY)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["company_number"], "12345678")
        self.assertEqual(items[1]["company_status"], "dissolved")

    @patch("urllib.request.urlopen")
    def test_sends_basic_auth_header(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse(SEARCH_RESPONSE)
        cl.search_companies("Acme", FAKE_KEY)
        request = mock_urlopen.call_args[0][0]
        self.assertTrue(request.get_header("Authorization").startswith("Basic "))

    @patch("urllib.request.urlopen")
    def test_query_reaches_the_request_url(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse(SEARCH_RESPONSE)
        cl.search_companies("Acme Plumbing Ltd", FAKE_KEY)
        request = mock_urlopen.call_args[0][0]
        self.assertIn("search/companies", request.full_url)
        self.assertIn("q=Acme", request.full_url)

    @patch("urllib.request.urlopen")
    def test_unexpected_shape_raises(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({"not": "the expected shape"})
        with self.assertRaises(cl.CompaniesHouseError):
            cl.search_companies("Acme", FAKE_KEY)

    @patch("urllib.request.urlopen")
    def test_401_gives_a_clear_key_error(self, mock_urlopen):
        mock_urlopen.side_effect = _http_error(401, {"error": "Invalid Authorization"})
        with self.assertRaises(cl.CompaniesHouseError) as ctx:
            cl.search_companies("Acme", FAKE_KEY)
        self.assertIn("401", str(ctx.exception))
        self.assertIn("API key", str(ctx.exception))

    @patch("urllib.request.urlopen")
    def test_network_error_is_wrapped(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.URLError("no route to host")
        with self.assertRaises(cl.CompaniesHouseError):
            cl.search_companies("Acme", FAKE_KEY)


class GetCompanyProfileTests(unittest.TestCase):
    def test_rejects_malformed_company_number(self):
        with self.assertRaises(cl.CompaniesHouseError):
            cl.get_company_profile("not a number!!", FAKE_KEY)
        with self.assertRaises(cl.CompaniesHouseError):
            cl.get_company_profile("", FAKE_KEY)

    @patch("urllib.request.urlopen")
    def test_returns_profile(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse(PROFILE_RESPONSE)
        profile = cl.get_company_profile("12345678", FAKE_KEY)
        self.assertEqual(profile["company_status"], "active")
        self.assertEqual(profile["company_name"], "ACME PLUMBING LTD")

    @patch("urllib.request.urlopen")
    def test_404_reports_not_found(self, mock_urlopen):
        mock_urlopen.side_effect = _http_error(404, {"error": "not-found"})
        with self.assertRaises(cl.CompaniesHouseError) as ctx:
            cl.get_company_profile("00000000", FAKE_KEY)
        self.assertIn("404", str(ctx.exception))

    @patch("urllib.request.urlopen")
    def test_unexpected_shape_raises(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({"no": "company_number here"})
        with self.assertRaises(cl.CompaniesHouseError):
            cl.get_company_profile("12345678", FAKE_KEY)


class FormatAddressTests(unittest.TestCase):
    def test_joins_present_parts_only(self):
        address = cl._format_address({
            "premises": "1", "address_line_1": "Fake Street",
            "locality": "Chester", "postal_code": "CH1 1AA",
        })
        self.assertEqual(address, "1, Fake Street, Chester, CH1 1AA")

    def test_handles_missing_or_non_dict(self):
        self.assertEqual(cl._format_address(None), "")
        self.assertEqual(cl._format_address({}), "")


class MainCliTests(unittest.TestCase):
    @patch("urllib.request.urlopen")
    def test_name_search_json_output(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse(SEARCH_RESPONSE)
        with patch.dict(os.environ, {"COMPANIES_HOUSE_API_KEY": FAKE_KEY}):
            rc = cl.main(["--name", "Acme Plumbing", "--json"])
        self.assertEqual(rc, 0)

    @patch("urllib.request.urlopen")
    def test_number_lookup(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse(PROFILE_RESPONSE)
        with patch.dict(os.environ, {"COMPANIES_HOUSE_API_KEY": FAKE_KEY}):
            rc = cl.main(["--number", "12345678"])
        self.assertEqual(rc, 0)

    def test_missing_key_returns_nonzero(self):
        with patch.dict(os.environ, {}, clear=True):
            rc = cl.main(["--name", "Acme"])
        self.assertEqual(rc, 1)

    def test_name_and_number_are_mutually_exclusive(self):
        with self.assertRaises(SystemExit):
            cl.main(["--name", "Acme", "--number", "123"])


if __name__ == "__main__":
    unittest.main()
