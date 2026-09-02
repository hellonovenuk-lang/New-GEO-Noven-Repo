import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "scripts" / "wardith_secrets.py"
ZOHO = {
    "client_id": "client-test",
    "client_secret": "secret-test",
    "refresh_token": "refresh-test",
    "account_id": "account-test",
    "api_domain": "https://mail.zoho.eu/api",
    "accounts_domain": "https://accounts.zoho.eu",
}


def secret_items(include_unexpected=True):
    values = {
        "OPENAI_API_KEY": "openai-test",
        "OPENAI_MODEL": "openai-model-test",
        "GEMINI_API_KEY": "gemini-test",
        "GEMINI_MODEL": "gemini-model-test",
        "PERPLEXITY_API_KEY": "perplexity-test",
        "PERPLEXITY_MODEL": "perplexity-model-test",
        "COMPANIES_HOUSE_API_KEY": "companies-test",
        "ZOHO_CREDENTIALS_JSON": json.dumps(ZOHO),
    }
    if include_unexpected:
        values["UNEXPECTED_SECRET"] = "must-not-leak"
    return [{"key": key, "value": value} for key, value in values.items()]


class HostedSecretWrapperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp.name)
        self.bws = self.temp_path / "fake_bws.py"
        self.bws.write_text(
            "import os, pathlib, sys\n"
            "pathlib.Path(os.environ['FAKE_BWS_TOKEN_FILE']).write_text(os.environ.get('BWS_ACCESS_TOKEN',''))\n"
            "print(pathlib.Path(os.environ['FAKE_BWS_JSON']).read_text())\n",
            encoding="utf-8",
        )
        self.payload = self.temp_path / "secrets.json"
        self.payload.write_text(json.dumps(secret_items()), encoding="utf-8")
        self.probe = self.temp_path / "probe.py"
        self.probe.write_text(
            "import json, os, pathlib\n"
            "p=os.environ.get('WARDITH_ZOHO_CREDENTIALS')\n"
            "print(json.dumps({'openai':os.environ.get('OPENAI_API_KEY'),"
            "'unexpected':os.environ.get('UNEXPECTED_SECRET'),"
            "'bws_token':os.environ.get('BWS_ACCESS_TOKEN'),"
            "'zoho_exists':bool(p and pathlib.Path(p).exists()),'zoho_path':p}))\n",
            encoding="utf-8",
        )
        self.token_file = self.temp_path / "token-seen.txt"

    def tearDown(self):
        self.temp.cleanup()

    def run_wrapper(self, *args):
        env = os.environ.copy()
        env.update(
            BWS_ACCESS_TOKEN="bootstrap-test",
            BWS_PROJECT_ID="project-test",
            WARDITH_BWS_CLI=sys.executable,
            WARDITH_BWS_ARGS=json.dumps([str(self.bws)]),
            FAKE_BWS_JSON=str(self.payload),
            FAKE_BWS_TOKEN_FILE=str(self.token_file),
        )
        return subprocess.run(
            [sys.executable, str(WRAPPER), *args],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
        )

    def test_run_exposes_allowlist_but_not_bootstrap_token(self):
        result = self.run_wrapper("run", "--", sys.executable, str(self.probe))
        self.assertEqual(0, result.returncode, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual("openai-test", payload["openai"])
        self.assertIsNone(payload["unexpected"])
        self.assertIsNone(payload["bws_token"])
        self.assertTrue(payload["zoho_exists"])
        self.assertEqual("bootstrap-test", self.token_file.read_text())

    def test_temp_zoho_file_is_removed_after_child(self):
        result = self.run_wrapper("run", "--", sys.executable, str(self.probe))
        self.assertEqual(0, result.returncode, result.stderr)
        path = Path(json.loads(result.stdout)["zoho_path"])
        self.assertFalse(path.exists())
        self.assertFalse(path.parent.exists())

    def test_missing_required_secret_stops_before_child(self):
        items = [item for item in secret_items() if item["key"] != "GEMINI_API_KEY"]
        self.payload.write_text(json.dumps(items), encoding="utf-8")
        result = self.run_wrapper("run", "--", sys.executable, str(self.probe))
        self.assertNotEqual(0, result.returncode)
        self.assertIn("missing required secret", result.stderr)
        self.assertNotIn("openai-test", result.stderr)

    def test_malformed_zoho_json_stops_before_child(self):
        items = secret_items()
        next(item for item in items if item["key"] == "ZOHO_CREDENTIALS_JSON")["value"] = "not-json"
        self.payload.write_text(json.dumps(items), encoding="utf-8")
        result = self.run_wrapper("run", "--", sys.executable, str(self.probe))
        self.assertNotEqual(0, result.returncode)
        self.assertIn("ZOHO_CREDENTIALS_JSON is not valid JSON", result.stderr)


if __name__ == "__main__":
    unittest.main()
