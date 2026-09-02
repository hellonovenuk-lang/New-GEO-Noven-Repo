import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import remote_runner


class DispatchValidationTests(unittest.TestCase):
    def test_paid_run_requires_exact_confirmation(self):
        with self.assertRaisesRegex(ValueError, "confirmation RUN"):
            remote_runner.validate_dispatch("90qrun", "Wirral dentists", "run")

    def test_outreach_requires_exact_confirmation(self):
        with self.assertRaisesRegex(ValueError, "confirmation DRAFT"):
            remote_runner.validate_dispatch("outreach", "wirral-dentists", "")

    def test_preflight_rejects_target(self):
        with self.assertRaisesRegex(ValueError, "target must be blank"):
            remote_runner.validate_dispatch("preflight", "unused", "")

    def test_qualify_rejects_blank_target(self):
        with self.assertRaisesRegex(ValueError, "target is required"):
            remote_runner.validate_dispatch("qualify", "  ", "")

    def test_unknown_operation_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unsupported operation"):
            remote_runner.validate_dispatch("send", "anything", "")


class PromptTests(unittest.TestCase):
    def test_prompt_uses_provider_neutral_skill_and_target(self):
        prompt = remote_runner.build_prompt("qualify", "wirral-dentists")
        self.assertIn(".agents/skills/qualify/SKILL.md", prompt)
        self.assertIn("wirral-dentists", prompt)
        self.assertIn("commit and push only WARDITH_DATA_REPO", prompt)

    def test_outreach_prompt_forbids_sending(self):
        prompt = remote_runner.build_prompt("outreach", "wirral-dentists")
        self.assertIn("Never send email", prompt)
        self.assertIn("Zoho drafts", prompt)

    def test_preflight_has_no_agent_prompt(self):
        with self.assertRaisesRegex(ValueError, "does not use an agent prompt"):
            remote_runner.build_prompt("preflight", "")


class PreflightTests(unittest.TestCase):
    def test_preflight_leaves_no_probe_file(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            core = root_path / "core"
            data = root_path / "data"
            runs = root_path / "runs"
            core.mkdir()
            data.mkdir()
            with mock.patch.object(remote_runner.shutil, "which", return_value="/bin/tool"):
                remote_runner.run_preflight(core, data, runs)
            self.assertTrue(runs.is_dir())
            self.assertFalse((data / ".wardith-write-probe").exists())

    def test_preflight_rejects_missing_data_checkout(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            with self.assertRaisesRegex(ValueError, "data checkout is missing"):
                remote_runner.run_preflight(root_path, root_path / "missing", root_path / "runs")


if __name__ == "__main__":
    unittest.main()
