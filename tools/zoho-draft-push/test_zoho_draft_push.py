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
import subprocess
import sys
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


def _sent_payload(mock_urlopen):
    """The JSON body of the request the mocked urlopen was last called with."""
    return json.loads(mock_urlopen.call_args[0][0].data.decode("utf-8"))


# The complete, closed set of keys zoho_draft_push.py is allowed to send to
# Zoho's messages endpoint. Kept here, spelled out literally, so widening the
# payload is a deliberate test edit and not a silent side effect.
EXPECTED_PAYLOAD_KEYS = {
    "fromAddress", "toAddress", "subject", "content", "mailFormat", "mode",
}

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


class DraftModeInvariantTests(unittest.TestCase):
    """The load-bearing safety property of this tool.

    Zoho's "Send an Email" and "Save Draft" APIs are the SAME endpoint, the
    same method, and the same OAuth scope - the request body's `mode` field
    is the only thing that tells them apart. So the scope does not prevent a
    send; the payload construction does. These tests are what enforce it:
    every payload this tool builds must carry mode == "draft", and must
    consist of exactly the closed set of literal keys above, so no entry
    field can ever inject or override `mode`.
    """

    def _entry(self, **overrides):
        entry = {
            "business": "Sampleford Glazing",
            "withheld": False,
            "contact_route": {"email": "owner@sampleford-glazing.example"},
            "email_subject": "s",
            "email_body": "b",
        }
        entry.update(overrides)
        return entry

    def test_built_payload_has_mode_draft(self):
        payload = zdp.build_message_payload(self._entry(), "hello@wardith.co.uk")
        self.assertEqual(payload["mode"], "draft")

    def test_built_payload_key_set_is_exactly_the_closed_set(self):
        payload = zdp.build_message_payload(self._entry(), "hello@wardith.co.uk")
        self.assertEqual(set(payload), EXPECTED_PAYLOAD_KEYS)

    def test_entry_cannot_inject_or_override_mode(self):
        """An entry carrying its own `mode`/`askReceipt`/etc. must not reach
        the payload - the payload is built from named fields only, never by
        merging entry data."""
        hostile = self._entry(mode="send", askReceipt="yes", fromAddress="attacker@example.com")
        payload = zdp.build_message_payload(hostile, "hello@wardith.co.uk")
        self.assertEqual(payload["mode"], "draft")
        self.assertEqual(payload["fromAddress"], "hello@wardith.co.uk")
        self.assertEqual(set(payload), EXPECTED_PAYLOAD_KEYS)

    def test_entry_with_hostile_nested_fields_cannot_widen_payload(self):
        hostile = self._entry(contact_route={"email": "x@example.com", "mode": "send"})
        payload = zdp.build_message_payload(hostile, "hello@wardith.co.uk")
        self.assertEqual(payload["mode"], "draft")
        self.assertEqual(set(payload), EXPECTED_PAYLOAD_KEYS)

    @patch("urllib.request.urlopen")
    def test_create_path_sends_mode_draft_and_nothing_else(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({"data": {"messageId": "999888777"}})
        zdp.push_entry(self._entry(), "hello@wardith.co.uk", "https://mail.zoho.eu", "111", "tok")
        sent = _sent_payload(mock_urlopen)
        self.assertEqual(sent["mode"], "draft")
        self.assertEqual(set(sent), EXPECTED_PAYLOAD_KEYS)

    @patch("urllib.request.urlopen")
    def test_update_path_sends_mode_draft_and_nothing_else(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({"data": {"messageId": "999888777"}})
        zdp.push_entry(self._entry(zoho_draft_id="999888777"), "hello@wardith.co.uk",
                       "https://mail.zoho.eu", "111", "tok")
        sent = _sent_payload(mock_urlopen)
        self.assertEqual(sent["mode"], "draft")
        self.assertEqual(set(sent), EXPECTED_PAYLOAD_KEYS)

    @patch("urllib.request.urlopen")
    def test_every_payload_in_a_whole_batch_is_a_draft(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({"data": {"messageId": "1"}})
        entries = [
            self._entry(business="A", mode="send"),
            self._entry(business="B", zoho_draft_id="123456"),
            self._entry(business="C"),
        ]
        zdp.process_outreach_prep(entries, FAKE_CREDENTIALS, "tok")
        sent_bodies = [json.loads(c[0][0].data.decode("utf-8")) for c in mock_urlopen.call_args_list]
        self.assertEqual(len(sent_bodies), 3)
        for body in sent_bodies:
            self.assertEqual(body["mode"], "draft")
            self.assertEqual(set(body), EXPECTED_PAYLOAD_KEYS)

    def test_source_hardcodes_mode_draft_and_never_assigns_it_dynamically(self):
        """Guards the claim in the module docstring: `mode` appears in this
        file only as a literal "draft", never assigned from a variable."""
        src_path = os.path.join(os.path.dirname(__file__), "zoho_draft_push.py")
        with open(src_path, "r", encoding="utf-8") as f:
            source = f.read()
        mode_lines = [ln.strip() for ln in source.splitlines()
                      if '"mode"' in ln and not ln.strip().startswith("#")]
        self.assertEqual(mode_lines, ['"mode": "draft",'])


class PushEntryTests(unittest.TestCase):
    def _entry(self, **overrides):
        entry = {
            "business": "Sampleford Glazing",
            "withheld": False,
            "contact_route": {"email": "owner@sampleford-glazing.example"},
            "email_subject": "Sampleford Glazing — for the practice owner",
            "email_body": "Hello,\n\nSome finding.",
        }
        entry.update(overrides)
        return entry

    def test_withheld_entry_is_skipped_with_no_http_call(self):
        entry = self._entry(withheld=True)
        with patch("urllib.request.urlopen") as mock_urlopen:
            result = zdp.push_entry(entry, "hello@wardith.co.uk", "https://mail.zoho.eu", "111", "tok")
        mock_urlopen.assert_not_called()
        self.assertEqual(result["zoho_push_status"], "SKIPPED (withheld)")

    @patch("urllib.request.urlopen")
    def test_new_entry_posts_and_records_created(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({"data": {"messageId": "999888777"}})
        entry = self._entry()
        result = zdp.push_entry(entry, "hello@wardith.co.uk", "https://mail.zoho.eu", "111", "tok")
        self.assertEqual(result["zoho_draft_id"], "999888777")
        self.assertEqual(result["zoho_push_status"], "OK")
        self.assertEqual(result["zoho_push_action"], "created")
        self.assertIn("zoho_pushed_at", result)
        called_request = mock_urlopen.call_args[0][0]
        self.assertEqual(called_request.get_method(), "POST")
        self.assertIn("111", called_request.full_url)

    @patch("urllib.request.urlopen")
    def test_entry_with_existing_draft_id_puts_and_records_updated(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({"data": {"messageId": "999888777"}})
        entry = self._entry(zoho_draft_id="999888777")
        result = zdp.push_entry(entry, "hello@wardith.co.uk", "https://mail.zoho.eu", "111", "tok")
        self.assertEqual(result["zoho_draft_id"], "999888777")
        self.assertEqual(result["zoho_push_action"], "updated")
        called_request = mock_urlopen.call_args[0][0]
        self.assertEqual(called_request.get_method(), "PUT")
        self.assertIn("999888777", called_request.full_url)

    @patch("urllib.request.urlopen")
    def test_http_error_recorded_as_failed_not_raised(self, mock_urlopen):
        mock_urlopen.side_effect = _http_error(400, {"error": "invalid toAddress"})
        entry = self._entry()
        result = zdp.push_entry(entry, "hello@wardith.co.uk", "https://mail.zoho.eu", "111", "tok")
        self.assertTrue(result["zoho_push_status"].startswith("FAILED"))
        self.assertIn("400", result["zoho_push_status"])

    @patch("urllib.request.urlopen")
    def test_unexpected_response_shape_recorded_as_failed_not_raised(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({"nothing": "useful"})
        entry = self._entry()
        result = zdp.push_entry(entry, "hello@wardith.co.uk", "https://mail.zoho.eu", "111", "tok")
        self.assertTrue(result["zoho_push_status"].startswith("FAILED"))

    @patch("urllib.request.urlopen")
    def test_malformed_json_response_recorded_as_failed_not_raised(self, mock_urlopen):
        fake_resp = _FakeResponse({"data": {"messageId": "123"}})
        fake_resp.read = lambda: b"{ invalid json"
        mock_urlopen.return_value = fake_resp
        entry = self._entry()
        result = zdp.push_entry(entry, "hello@wardith.co.uk", "https://mail.zoho.eu", "111", "tok")
        self.assertTrue(result["zoho_push_status"].startswith("FAILED"))
        self.assertIn("JSONDecodeError", result["zoho_push_status"])

    @patch("urllib.request.urlopen")
    def test_data_field_is_string_recorded_as_failed_not_raised(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({"data": "not a dict or list"})
        entry = self._entry()
        result = zdp.push_entry(entry, "hello@wardith.co.uk", "https://mail.zoho.eu", "111", "tok")
        self.assertTrue(result["zoho_push_status"].startswith("FAILED"))

    @patch("urllib.request.urlopen")
    def test_data_list_with_non_dict_elements_recorded_as_failed_not_raised(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({"data": [1, 2, 3]})
        entry = self._entry()
        result = zdp.push_entry(entry, "hello@wardith.co.uk", "https://mail.zoho.eu", "111", "tok")
        self.assertTrue(result["zoho_push_status"].startswith("FAILED"))

    @patch("urllib.request.urlopen")
    def test_response_is_not_dict_recorded_as_failed_not_raised(self, mock_urlopen):
        fake_resp = _FakeResponse({})
        fake_resp.read = lambda: b'[{"messageId": "123"}]'
        mock_urlopen.return_value = fake_resp
        entry = self._entry()
        result = zdp.push_entry(entry, "hello@wardith.co.uk", "https://mail.zoho.eu", "111", "tok")
        self.assertTrue(result["zoho_push_status"].startswith("FAILED"))

    def test_dry_run_makes_no_http_call(self):
        entry = self._entry()
        with patch("urllib.request.urlopen") as mock_urlopen:
            result = zdp.push_entry(entry, "hello@wardith.co.uk", "https://mail.zoho.eu", "111", "tok", dry_run=True)
        mock_urlopen.assert_not_called()
        self.assertTrue(result["zoho_push_status"].startswith("DRY-RUN"))
        self.assertEqual(result["zoho_push_action"], "create")


class ProcessOutreachPrepTests(unittest.TestCase):
    def _entries(self):
        return [
            {
                "business": "Sampleford Glazing", "withheld": False,
                "contact_route": {"email": "a@example.com"},
                "email_subject": "s1", "email_body": "b1",
            },
            {
                "business": "Withheld Co", "withheld": True,
                "contact_route": {"email": "b@example.com"},
                "email_subject": "s2", "email_body": "b2",
            },
        ]

    @patch("urllib.request.urlopen")
    def test_mutates_entries_in_place_and_returns_results(self, mock_urlopen):
        mock_urlopen.return_value = _FakeResponse({"data": {"messageId": "1"}})
        entries = self._entries()
        results = zdp.process_outreach_prep(entries, FAKE_CREDENTIALS, "tok")
        self.assertEqual(entries[0]["zoho_draft_id"], "1")
        self.assertEqual(entries[1]["zoho_push_status"], "SKIPPED (withheld)")
        self.assertEqual(len(results), 2)

    @patch("urllib.request.urlopen")
    def test_one_entry_failing_does_not_stop_the_rest(self, mock_urlopen):
        mock_urlopen.side_effect = [_http_error(500, {"error": "server error"}), _FakeResponse({"data": {"messageId": "2"}})]
        entries = [
            {"business": "Fails Ltd", "withheld": False, "contact_route": {"email": "a@example.com"}, "email_subject": "s", "email_body": "b"},
            {"business": "Succeeds Ltd", "withheld": False, "contact_route": {"email": "b@example.com"}, "email_subject": "s", "email_body": "b"},
        ]
        zdp.process_outreach_prep(entries, FAKE_CREDENTIALS, "tok")
        self.assertTrue(entries[0]["zoho_push_status"].startswith("FAILED"))
        self.assertEqual(entries[1]["zoho_push_status"], "OK")

    def test_dry_run_with_no_credentials_still_works(self):
        entries = self._entries()
        results = zdp.process_outreach_prep(entries, None, None, dry_run=True)
        self.assertTrue(results[0]["zoho_push_status"].startswith("DRY-RUN"))


class SummarizeTests(unittest.TestCase):
    def test_counts_each_outcome(self):
        results = [
            {"business": "A", "zoho_push_status": "OK", "zoho_push_action": "created"},
            {"business": "B", "zoho_push_status": "OK", "zoho_push_action": "updated"},
            {"business": "C", "zoho_push_status": "FAILED: HTTP 400 x"},
            {"business": "D", "zoho_push_status": "SKIPPED (withheld)"},
        ]
        text = zdp.summarize(results)
        self.assertIn("1 created", text)
        self.assertIn("1 updated", text)
        self.assertIn("1 failed", text)
        self.assertIn("1 skipped", text)
        self.assertIn("C: FAILED: HTTP 400 x", text)


class MainCliTests(unittest.TestCase):
    def _write_json(self, d, path, payload):
        full = os.path.join(d, path)
        with open(full, "w", encoding="utf-8") as f:
            json.dump(payload, f)
        return full

    def test_dry_run_end_to_end_writes_in_place_with_no_credentials_needed(self):
        entries = [{
            "business": "Sampleford Glazing", "withheld": False,
            "contact_route": {"email": "a@example.com"},
            "email_subject": "s1", "email_body": "b1",
        }]
        with tempfile.TemporaryDirectory() as d:
            input_path = self._write_json(d, "prep.json", entries)
            script = os.path.join(os.path.dirname(__file__), "zoho_draft_push.py")
            result = subprocess.run(
                [sys.executable, script, "--input", input_path, "--in-place", "--dry-run"],
                capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Zoho draft push:", result.stdout)
            with open(input_path, "r", encoding="utf-8") as f:
                updated = json.load(f)
            self.assertTrue(updated[0]["zoho_push_status"].startswith("DRY-RUN"))

    def test_missing_output_flag_exits_with_usage_error(self):
        with tempfile.TemporaryDirectory() as d:
            input_path = self._write_json(d, "prep.json", [])
            script = os.path.join(os.path.dirname(__file__), "zoho_draft_push.py")
            result = subprocess.run(
                [sys.executable, script, "--input", input_path],
                capture_output=True, text=True, timeout=30,
            )
        self.assertEqual(result.returncode, 2)
        self.assertIn("--output", result.stderr)

    def test_missing_credentials_exits_before_any_entry_processed(self):
        entries = [{
            "business": "Sampleford Glazing", "withheld": False,
            "contact_route": {"email": "a@example.com"},
            "email_subject": "s1", "email_body": "b1",
        }]
        with tempfile.TemporaryDirectory() as d:
            input_path = self._write_json(d, "prep.json", entries)
            missing_creds = os.path.join(d, "no-such-credentials.json")
            script = os.path.join(os.path.dirname(__file__), "zoho_draft_push.py")
            result = subprocess.run(
                [sys.executable, script, "--input", input_path, "--in-place", "--credentials", missing_creds],
                capture_output=True, text=True, timeout=30,
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("setup_zoho_oauth.py", result.stderr)


if __name__ == "__main__":
    unittest.main()
