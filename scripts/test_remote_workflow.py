import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "wardith-remote.yml"


class RemoteWorkflowTests(unittest.TestCase):
    def workflow(self):
        return WORKFLOW.read_text(encoding="utf-8")

    def test_manual_dispatch_exposes_all_four_operations(self):
        text = self.workflow()
        self.assertIn("workflow_dispatch:", text)
        for operation in ("preflight", "90qrun", "qualify", "outreach"):
            self.assertIn(f"- {operation}", text)
        self.assertIn("confirmation:", text)

    def test_validation_precedes_bootstrap_secret_use(self):
        text = self.workflow()
        self.assertLess(text.index("Validate dispatch"), text.index("Bootstrap Wardith secrets"))
        self.assertLess(text.index("Validate dispatch"), text.index("secrets.BWS_ACCESS_TOKEN"))

    def test_workflow_serializes_operational_runs(self):
        text = self.workflow()
        self.assertIn("group: wardith-operational-runs", text)
        self.assertIn("cancel-in-progress: false", text)

    def test_core_checkout_does_not_persist_credentials(self):
        text = self.workflow()
        core = text[text.index("Check out Wardith core"):text.index("Check out Wardith data")]
        self.assertIn("persist-credentials: false", core)

    def test_data_checkout_uses_only_deploy_key(self):
        text = self.workflow()
        data = text[text.index("Check out Wardith data"):text.index("Install Bitwarden CLI")]
        self.assertIn("repository: hellonovenuk-lang/wardith-crm-data", data)
        self.assertIn("ssh-key: ${{ secrets.WARDITH_DATA_DEPLOY_KEY }}", data)
        self.assertNotIn("github.token", data)

    def test_official_codex_action_is_last_execution_step(self):
        text = self.workflow()
        action = text.index("uses: openai/codex-action@v1")
        self.assertIn('permission-profile: "wardith-remote"', text[action:])
        self.assertIn("safety-strategy: drop-sudo", text[action:])
        self.assertNotIn("\n      - name:", text[action:])


if __name__ == "__main__":
    unittest.main()
