#!/usr/bin/env python3
"""
Tests for setup_zoho_oauth.py. No real network calls, no real Zoho
credentials - every urllib.request.urlopen call is mocked.

Run: python3 test_setup_zoho_oauth.py -v
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import setup_zoho_oauth as sz


class _FakeResponse:
    def __init__(self, payload):
        self._body = json.dumps(payload).encode("utf-8")

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class ExchangeGrantTokenTests(unittest.TestCase):
    @patch("urllib.request.urlopen")
    def test_returns_refresh_and_access_token(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({"refresh_token": "1000.rt", "access_token": "1000.at"})
        refresh_token, access_token = sz.exchange_grant_token(
            "https://accounts.zoho.eu", "client-id", "client-secret", "grant-token")
        self.assertEqual(refresh_token, "1000.rt")
        self.assertEqual(access_token, "1000.at")

    @patch("urllib.request.urlopen")
    def test_missing_tokens_in_response_raises(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({"error": "invalid_code"})
        with self.assertRaises(SystemExit):
            sz.exchange_grant_token("https://accounts.zoho.eu", "id", "secret", "bad-token")

    @patch("urllib.request.urlopen")
    def test_partial_tokens_does_not_expose_token_in_error(self, mock_urlopen):
        """Verify that error messages never expose token values, even partial ones."""
        mock_urlopen.return_value = _FakeResponse({"access_token": "1000.realtoken", "expires_in": 3600})
        with self.assertRaises(SystemExit) as cm:
            sz.exchange_grant_token("https://accounts.zoho.eu", "id", "secret", "token")
        error_message = str(cm.exception)
        # The token value must never appear in the error message
        self.assertNotIn("1000.realtoken", error_message)
        # The message should indicate what's missing
        self.assertIn("refresh_token", error_message)


class LookupAccountTests(unittest.TestCase):
    @patch("urllib.request.urlopen")
    def test_returns_account_id_and_primary_email(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({
            "data": [{"accountId": 111222333, "primaryEmailAddress": "hello@wardith.co.uk"}]
        })
        account_id, from_address = sz.lookup_account("https://mail.zoho.eu", "1000.at")
        self.assertEqual(account_id, "111222333")
        self.assertEqual(from_address, "hello@wardith.co.uk")

    @patch("urllib.request.urlopen")
    def test_no_accounts_in_response_raises(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({"data": []})
        with self.assertRaises(SystemExit):
            sz.lookup_account("https://mail.zoho.eu", "1000.at")


class MainCliTests(unittest.TestCase):
    @patch("urllib.request.urlopen")
    def test_writes_complete_credentials_file(self, mock_urlopen):
        mock_urlopen.side_effect = [
            _FakeResponse({"refresh_token": "1000.rt", "access_token": "1000.at"}),
            _FakeResponse({"data": [{"accountId": 111222333, "primaryEmailAddress": "hello@wardith.co.uk"}]}),
        ]
        with tempfile.TemporaryDirectory() as d:
            out_path = os.path.join(d, "creds.json")
            sys.argv = [
                "setup_zoho_oauth.py", "--client-id", "cid", "--client-secret", "csecret",
                "--grant-token", "gtoken", "--region", "eu", "--out", out_path,
            ]
            sz.main()
            with open(out_path, "r", encoding="utf-8") as f:
                creds = json.load(f)
        self.assertEqual(creds["refresh_token"], "1000.rt")
        self.assertEqual(creds["account_id"], "111222333")
        self.assertEqual(creds["from_address"], "hello@wardith.co.uk")
        self.assertEqual(creds["api_domain"], "https://mail.zoho.eu")
        self.assertEqual(creds["accounts_domain"], "https://accounts.zoho.eu")


if __name__ == "__main__":
    unittest.main()
