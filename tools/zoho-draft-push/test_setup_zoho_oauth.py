#!/usr/bin/env python3
"""
Tests for setup_zoho_oauth.py. No real network calls, no real Zoho
credentials - every urllib.request.urlopen call is mocked.

Run: python3 test_setup_zoho_oauth.py -v
"""
import json
import io
import urllib.error
from contextlib import redirect_stdout
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
    def test_http_error_body_is_never_exposed(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError("https://accounts.zoho.eu", 400, "bad", {}, io.BytesIO(b"secret-value"))
        with self.assertRaises(SystemExit) as error:
            sz.exchange_grant_token("https://accounts.zoho.eu", "id", "secret", "grant")
        self.assertNotIn("secret-value", str(error.exception))

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

    @patch("urllib.request.urlopen")
    def test_no_accounts_error_does_not_echo_the_response(self, mock_urlopen):
        """Same rule as exchange_grant_token above: report what was missing,
        never the raw remote response - it can carry tokens or noise."""
        mock_urlopen.return_value = _FakeResponse({"data": [], "oauthToken": "1000.realtoken"})
        with self.assertRaises(SystemExit) as cm:
            sz.lookup_account("https://mail.zoho.eu", "1000.at")
        self.assertNotIn("1000.realtoken", str(cm.exception))

    @patch("urllib.request.urlopen")
    def test_missing_account_fields_error_names_fields_not_raw_data(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({
            "data": [{"accountId": 111222333, "incomingBlocked": False,
                      "oauthToken": "1000.realtoken"}]
        })
        with self.assertRaises(SystemExit) as cm:
            sz.lookup_account("https://mail.zoho.eu", "1000.at")
        message = str(cm.exception)
        self.assertNotIn("1000.realtoken", message)
        self.assertIn("primaryEmailAddress", message)

    @patch("urllib.request.urlopen")
    def test_account_record_that_is_not_a_dict_is_rejected_cleanly(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({"data": ["not-an-account-object"]})
        with self.assertRaises(SystemExit) as cm:
            sz.lookup_account("https://mail.zoho.eu", "1000.at")
        self.assertNotIn("not-an-account-object", str(cm.exception))


class MainCliTests(unittest.TestCase):
    def test_interactive_refuses_captured_terminal_before_reading_credentials(self):
        with patch.object(sys.stdin, "isatty", return_value=False):
            with self.assertRaises(SystemExit):
                sz.interactive_setup("eu")

    @patch("urllib.request.urlopen")
    def test_interactive_exchange_uses_hidden_inputs_and_displays_only_refresh_token(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({"refresh_token": "replacement-refresh", "access_token": "private-access"})
        output = io.StringIO()
        with patch.object(sys.stdin, "isatty", return_value=True), patch.object(sys.stdout, "isatty", return_value=True), patch.dict(os.environ, {}, clear=True), patch("getpass.getpass", side_effect=["new-client", "private-secret", "private-grant"]), patch("builtins.input", return_value=""), redirect_stdout(output):
            with patch.object(output, "isatty", return_value=True):
                sz.interactive_setup("eu")
        self.assertIn("replacement-refresh", output.getvalue())
        for secret in ("private-secret", "private-grant", "private-access"):
            self.assertNotIn(secret, output.getvalue())

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

    @patch("urllib.request.urlopen")
    def test_secret_file_and_its_directory_get_restrictive_modes(self, mock_urlopen):
        """playbook/records-and-data.md's settled pattern for secrets is a
        0700 directory holding a 0600 file. The mode must be established at
        creation, not chmod'd on afterwards, so the refresh token never sits
        in a default-permission file even momentarily. Asserted on the calls
        rather than on os.stat, since Windows does not honour POSIX modes."""
        mock_urlopen.side_effect = [
            _FakeResponse({"refresh_token": "1000.rt", "access_token": "1000.at"}),
            _FakeResponse({"data": [{"accountId": 111222333, "primaryEmailAddress": "hello@wardith.co.uk"}]}),
        ]
        real_os_open = os.open
        opened = {}
        chmodded = {}

        def spy_open(path, flags, mode=0o777, **kwargs):
            opened[os.path.abspath(path)] = mode
            return real_os_open(path, flags, mode, **kwargs)

        def spy_chmod(path, mode, **kwargs):
            chmodded[os.path.abspath(path)] = mode

        with tempfile.TemporaryDirectory() as d:
            secret_dir = os.path.join(d, "dotwardith")
            out_path = os.path.join(secret_dir, "zoho-credentials.json")
            sys.argv = [
                "setup_zoho_oauth.py", "--client-id", "cid", "--client-secret", "csecret",
                "--grant-token", "gtoken", "--region", "eu", "--out", out_path,
            ]
            with patch("os.open", side_effect=spy_open), patch("os.chmod", side_effect=spy_chmod):
                sz.main()
            self.assertEqual(opened.get(os.path.abspath(out_path)), 0o600)
            self.assertEqual(chmodded.get(os.path.abspath(secret_dir)), 0o700)
            with open(out_path, "r", encoding="utf-8") as f:
                self.assertEqual(json.load(f)["refresh_token"], "1000.rt")


if __name__ == "__main__":
    unittest.main()
