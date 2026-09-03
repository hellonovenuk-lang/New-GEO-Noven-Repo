"""Run the cloud smoke entry point against fake provider HTTP responses."""
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

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "trade-run"))
from test_trade_run import FAKE_ENV, fixture_response, http_error


class CloudSmokeTests(unittest.TestCase):
    def exercise(self, directory, effect=fixture_response):
        from scripts import provider_smoke
        with mock.patch.dict(os.environ, FAKE_ENV), \
                mock.patch.object(provider_smoke.runner.urllib.request, "urlopen", side_effect=effect) as network, \
                mock.patch.object(provider_smoke.runner.time, "sleep"), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            code = provider_smoke.main(["--out", str(directory)])
        return code, network.call_count

    def test_cloud_smoke_is_three_queries_with_private_results_and_safe_summary(self):
        with tempfile.TemporaryDirectory() as root:
            out = Path(root) / "smoke-tests" / "123-1"
            code, count = self.exercise(out)
            self.assertEqual((code, count), (0, 3))
            summary = json.loads((out / "summary.json").read_text())
            self.assertTrue(summary["passed"])
            self.assertEqual([p["provider"] for p in summary["providers"]], ["openai", "gemini", "perplexity"])
            self.assertNotIn("UK answer", json.dumps(summary))
            self.assertNotIn("FAKE_", json.dumps(summary))
            with (out / "results.csv").open(newline="", encoding="utf-8") as handle:
                self.assertEqual(len(list(csv.DictReader(handle))), 3)

    def test_cloud_smoke_retains_failure_and_success_rows_when_provider_fails(self):
        def fail_gemini(request, **kwargs):
            if "googleapis.com" in request.full_url:
                raise http_error(503)
            return fixture_response(request, **kwargs)
        with tempfile.TemporaryDirectory() as root:
            out = Path(root) / "new"
            code, count = self.exercise(out, fail_gemini)
            self.assertEqual((code, count), (1, 5))
            summary = json.loads((out / "summary.json").read_text())
            self.assertFalse(summary["passed"])
            self.assertTrue(summary["providers"][0]["passed"])
            self.assertFalse(summary["providers"][1]["passed"])
            self.assertTrue(summary["providers"][2]["passed"])

    def test_existing_result_directory_is_never_overwritten_or_retried(self):
        with tempfile.TemporaryDirectory() as root:
            out = Path(root) / "existing"
            out.mkdir()
            receipt = out / "summary.json"
            receipt.write_text("keep")
            code, count = self.exercise(out)
            self.assertEqual((code, count), (2, 0))
            self.assertEqual(receipt.read_text(), "keep")


if __name__ == "__main__":
    unittest.main()
