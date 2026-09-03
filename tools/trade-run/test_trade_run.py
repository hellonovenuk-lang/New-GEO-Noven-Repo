"""Provider boundaries tested offline: never load credentials or call APIs."""
import contextlib
import csv
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
import urllib.error

import trade_run as run

FAKE_ENV = {
    "OPENAI_API_KEY": "FAKE_OPENAI_SECRET", "OPENAI_MODEL": "openai-test",
    "GEMINI_API_KEY": "FAKE_GEMINI_SECRET", "GEMINI_MODEL": "gemini-test",
    "PERPLEXITY_API_KEY": "FAKE_PERPLEXITY_SECRET", "PERPLEXITY_MODEL": "sonar-test",
}


def response(data):
    return io.BytesIO(json.dumps(data).encode())


def http_error(code):
    return urllib.error.HTTPError(
        "https://generativelanguage.googleapis.com/test?key=FAKE_GEMINI_SECRET",
        code, "FAKE_GEMINI_SECRET", {}, io.BytesIO(b'{"error":"FAKE_GEMINI_SECRET"}'))


def fixture_response(request, **kwargs):
    if "api.openai.com" in request.full_url:
        return response({"model": "openai-test", "output": [{"type": "message", "content": [
            {"type": "output_text", "text": "UK answer\nSecond line", "annotations": [
                {"type": "url_citation", "url": "https://example.org/openai"}]}]}]})
    if "googleapis.com" in request.full_url:
        return response({"modelVersion": "gemini-test", "candidates": [{"content": {
            "parts": [{"text": "UK answer"}]}, "groundingMetadata": {"groundingChunks": [
                {"web": {"uri": "https://example.org/gemini"}}]}}]})
    return response({"model": "sonar-test", "choices": [{"message": {"content": "UK answer"}}],
                     "citations": ["https://example.org/perplexity"]})


class RequestTests(unittest.TestCase):
    def test_http_error_does_not_expose_url_or_response_body(self):
        with mock.patch.object(run.urllib.request, "urlopen", side_effect=http_error(401)):
            with self.assertRaises(RuntimeError) as caught:
                run.post_json("https://example.org/?key=FAKE_GEMINI_SECRET", {}, {})
        self.assertNotIn("FAKE_GEMINI_SECRET", str(caught.exception))
        self.assertNotIn("https://", str(caught.exception))
        self.assertIn("401", str(caught.exception))

    def test_retries_429_and_503_then_returns_success_after_15_and_45_seconds(self):
        with mock.patch.object(run.urllib.request, "urlopen", side_effect=[
            http_error(429), http_error(503), response({"ok": True})]) as network, \
                mock.patch.object(run.time, "sleep") as sleep:
            self.assertEqual(run.post_json("https://api.openai.com/v1/responses", {}, {}), {"ok": True})
        self.assertEqual(network.call_count, 3)
        self.assertEqual(sleep.call_args_list, [mock.call(15), mock.call(45)])

    def test_stops_after_three_attempts_on_persistent_503(self):
        with mock.patch.object(run.urllib.request, "urlopen", side_effect=lambda *a, **k: (_ for _ in ()).throw(http_error(503))) as network, \
                mock.patch.object(run.time, "sleep") as sleep:
            with self.assertRaisesRegex(RuntimeError, "503"):
                run.post_json("https://api.openai.com/v1/responses", {}, {})
        self.assertEqual(network.call_count, 3)
        self.assertEqual(sleep.call_args_list, [mock.call(15), mock.call(45)])

    def test_authentication_and_other_http_errors_are_not_retried(self):
        for code in (400, 401, 403, 404, 500):
            with self.subTest(code=code), \
                    mock.patch.object(run.urllib.request, "urlopen", side_effect=http_error(code)) as network, \
                    mock.patch.object(run.time, "sleep") as sleep:
                with self.assertRaises(RuntimeError):
                    run.post_json("https://api.openai.com/v1/responses", {}, {})
                self.assertEqual(network.call_count, 1)
                sleep.assert_not_called()

    def test_network_error_does_not_leak_details_or_retry_ambiguous_request(self):
        with mock.patch.object(run.urllib.request, "urlopen", side_effect=urllib.error.URLError("FAKE_GEMINI_SECRET")) as network, \
                mock.patch.object(run.time, "sleep") as sleep:
            with self.assertRaises(RuntimeError) as caught:
                run.post_json("https://api.openai.com/v1/responses", {}, {})
        self.assertNotIn("FAKE_GEMINI_SECRET", str(caught.exception))
        self.assertEqual(network.call_count, 1)
        sleep.assert_not_called()

    def test_gemini_uses_header_auth_not_query_string(self):
        with mock.patch.dict(os.environ, FAKE_ENV), \
                mock.patch.object(run.urllib.request, "urlopen", side_effect=fixture_response) as network:
            model, answer, sources = run.call_gemini("Which provider in Wirral?", "Wirral")
        request = network.call_args.args[0]
        self.assertNotIn("FAKE_GEMINI_SECRET", request.full_url)
        self.assertNotIn("?", request.full_url)
        self.assertEqual(request.get_header("X-goog-api-key"), "FAKE_GEMINI_SECRET")
        self.assertEqual((model, answer, sources), ("gemini-test", "UK answer", ["https://example.org/gemini"]))


class SmokeTests(unittest.TestCase):
    def exercise(self, network_effect=fixture_response, cap="3", seed_empty=False):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "smoke.csv"
            if seed_empty:
                run.ensure_header(output)
                for provider in ("openai", "gemini", "perplexity"):
                    row = {name: "" for name in run.FIELDS}
                    row.update(assistant=provider, question_id="q01", run_no="1")
                    run.append_row(output, row)
            questions = Path(__file__).with_name("questions-wirral-dentists.csv")
            args = ["trade_run.py", "--questions", str(questions), "--out", str(output),
                    "--client", "test", "--location", "Wirral", "--smoke", "--cap", cap]
            stdout, stderr = io.StringIO(), io.StringIO()
            with mock.patch.object(sys, "argv", args), mock.patch.dict(os.environ, FAKE_ENV), \
                    mock.patch.object(run.urllib.request, "urlopen", side_effect=network_effect) as network, \
                    mock.patch.object(run.time, "sleep"), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                code = run.main()
            with output.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            return code, rows, network.call_count, stdout.getvalue() + stderr.getvalue()

    def test_smoke_makes_exactly_three_queries_and_preserves_csv_multiline_text(self):
        code, rows, count, _ = self.exercise()
        self.assertEqual(code, 0)
        self.assertEqual(count, 3)
        self.assertEqual([row["assistant"] for row in rows], ["openai", "gemini", "perplexity"])
        self.assertEqual([row["run_no"] for row in rows], ["1", "1", "1"])
        self.assertEqual(rows[0]["answer_text"], "UK answer\nSecond line")

    def test_failed_provider_returns_nonzero_and_keeps_other_results(self):
        def fail_gemini(request, **kwargs):
            if "googleapis.com" in request.full_url:
                raise http_error(401)
            return fixture_response(request, **kwargs)
        code, rows, count, logs = self.exercise(fail_gemini)
        self.assertEqual(code, 1)
        self.assertEqual(count, 3)
        self.assertTrue(rows[0]["answer_text"])
        self.assertTrue(rows[2]["answer_text"])
        self.assertIn("401", rows[1]["errors"])
        self.assertNotIn("FAKE_GEMINI_SECRET", logs + json.dumps(rows))

    def test_empty_or_ungrounded_provider_response_fails_smoke(self):
        for content in ("", "An answer with no sources"):
            def empty_gemini(request, **kwargs):
                if "googleapis.com" in request.full_url:
                    return response({"modelVersion": "gemini-test", "candidates": [
                        {"content": {"parts": [{"text": content}]}}]})
                return fixture_response(request, **kwargs)
            with self.subTest(content=content):
                code, rows, count, _ = self.exercise(empty_gemini)
                self.assertEqual(code, 1)
                self.assertEqual(count, 3)
                self.assertTrue(rows[1]["errors"])

    def test_malformed_sources_produce_safe_failed_row_instead_of_aborting(self):
        def malformed(request, **kwargs):
            if "perplexity.ai" in request.full_url:
                return response({"model": "sonar-test", "choices": [{"message": {"content": "UK answer"}}],
                                 "citations": [None]})
            return fixture_response(request, **kwargs)
        code, rows, count, _ = self.exercise(malformed)
        self.assertEqual((code, count, len(rows)), (1, 3, 3))
        self.assertTrue(rows[2]["errors"])

    def test_legacy_empty_smoke_rows_do_not_count_as_completed(self):
        code, rows, count, _ = self.exercise(seed_empty=True)
        self.assertEqual((code, count), (0, 3))
        self.assertEqual(len(rows), 6)
        self.assertTrue(all(row["answer_text"] and row["sources_cited"] for row in rows[3:]))


if __name__ == "__main__":
    unittest.main()
