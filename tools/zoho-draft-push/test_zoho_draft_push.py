#!/usr/bin/env python3
"""
Tests for zoho_draft_push.py. No real network calls and no real Zoho
credentials anywhere in this file - every urllib.request.urlopen call is
mocked. Fictitious data only, same convention as
tools/prospect-compiler/test_scoring_engine.py.

Run: python3 test_zoho_draft_push.py -v
"""
import io
import json
import os
import tempfile
import unittest
import urllib.error
from unittest.mock import patch

import zoho_draft_push as zdp


class _FakeResponse:
    """Minimal stand-in for the object urllib.request.urlopen() returns
    when used as a context manager."""

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


FAKE_CREDENTIALS = {
    "client_id": "1000.FAKECLIENTID",
    "client_secret": "fakesecret",
    "refresh_token": "1000.fakerefreshtoken",
    "account_id": "111222333",
    "from_address": "hello@wardith.co.uk",
    "api_domain": "https://mail.zoho.eu",
    "accounts_domain": "https://accounts.zoho.eu",
}


class LoadCredentialsTests(unittest.TestCase):
    def test_loads_a_complete_credentials_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "creds.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(FAKE_CREDENTIALS, f)
            creds = zdp.load_credentials(path)
        self.assertEqual(creds["account_id"], "111222333")

    def test_missing_file_raises_with_setup_pointer(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "does-not-exist.json")
            with self.assertRaises(zdp.ZohoAPIError) as ctx:
                zdp.load_credentials(path)
        self.assertIn("setup_zoho_oauth.py", str(ctx.exception))

    def test_missing_required_field_raises(self):
        incomplete = dict(FAKE_CREDENTIALS)
        del incomplete["account_id"]
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "creds.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(incomplete, f)
            with self.assertRaises(zdp.ZohoAPIError) as ctx:
                zdp.load_credentials(path)
        self.assertIn("account_id", str(ctx.exception))


class RefreshAccessTokenTests(unittest.TestCase):
    @patch("urllib.request.urlopen")
    def test_returns_access_token_on_success(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({"access_token": "1000.fakeaccesstoken", "expires_in": 3600})
        token = zdp.refresh_access_token(FAKE_CREDENTIALS)
        self.assertEqual(token, "1000.fakeaccesstoken")

    @patch("urllib.request.urlopen")
    def test_http_error_raises_zoho_api_error(self, mock_urlopen):
        mock_urlopen.side_effect = _http_error(401, {"error": "invalid_client"})
        with self.assertRaises(zdp.ZohoAPIError) as ctx:
            zdp.refresh_access_token(FAKE_CREDENTIALS)
        self.assertIn("401", str(ctx.exception))

    @patch("urllib.request.urlopen")
    def test_response_without_access_token_raises(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({"error": "some_other_shape"})
        with self.assertRaises(zdp.ZohoAPIError):
            zdp.refresh_access_token(FAKE_CREDENTIALS)


class BuildMessagePayloadTests(unittest.TestCase):
    def test_maps_business_fields_to_zoho_payload(self):
        entry = {
            "business": "Sampleford Glazing",
            "contact_route": {"email": "owner@sampleford-glazing.example"},
            "email_subject": "Sampleford Glazing — for the practice owner",
            "email_body": "Hello,\n\nSome finding.",
        }
        payload = zdp.build_message_payload(entry, "hello@wardith.co.uk")
        self.assertEqual(payload["fromAddress"], "hello@wardith.co.uk")
        self.assertEqual(payload["toAddress"], "owner@sampleford-glazing.example")
        self.assertEqual(payload["subject"], "Sampleford Glazing — for the practice owner")
        self.assertEqual(payload["mailFormat"], "html")

    def test_body_html_escapes_special_characters(self):
        entry = {
            "business": "A & B Ltd",
            "contact_route": {"email": "x@example.com"},
            "email_subject": "s",
            "email_body": "You appear less than <competitor>.",
        }
        payload = zdp.build_message_payload(entry, "hello@wardith.co.uk")
        self.assertIn("&lt;competitor&gt;", payload["content"])
        self.assertNotIn("<competitor>", payload["content"])

    def test_body_paragraphs_become_separate_p_tags(self):
        entry = {
            "business": "x", "contact_route": {"email": "x@example.com"},
            "email_subject": "s", "email_body": "First paragraph.\n\nSecond paragraph.",
        }
        payload = zdp.build_message_payload(entry, "hello@wardith.co.uk")
        self.assertEqual(payload["content"].count("<p>"), 2)
        self.assertIn("<p>First paragraph.</p>", payload["content"])
        self.assertIn("<p>Second paragraph.</p>", payload["content"])


if __name__ == "__main__":
    unittest.main()
