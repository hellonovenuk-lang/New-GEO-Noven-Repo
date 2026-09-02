# Phone-triggered Remote Runner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Run Wardith `90qrun`, `qualify`, `outreach`, and a free preflight from GitHub Actions on a phone while the laptop is off.

**Architecture:** A manually dispatched GitHub Actions workflow validates its inputs, checks out the core and private data repositories, retrieves an allowlisted set of secrets from Bitwarden for the minimum required process, and invokes the official `openai/codex-action`. A small Python controller creates deterministic prompts and preflight checks; the existing operational skills remain the source of business behaviour.

**Tech Stack:** GitHub Actions YAML, Python 3 standard library, Bash, Bitwarden Secrets Manager CLI, `openai/codex-action@v1`, `unittest`.

**Spec:** `docs/superpowers/specs/2026-09-02-phone-triggered-remote-runner-design.md`

## Global Constraints

- Work directly on `main`; make scoped commits and push each completed task.
- The core repository receives workflow/configuration changes only; prospect and run data stay in `wardith-crm-data`.
- `90qrun` requires the exact confirmation `RUN`; `outreach` requires `DRAFT`.
- No remote code path sends email, posts to LinkedIn, or submits a contact form.
- The workflow stores only `BWS_ACCESS_TOKEN` and `WARDITH_DATA_DEPLOY_KEY` as bootstrap secrets.
- The Bitwarden token is read-only, separate from the Windows token, and never reaches the Codex child process.
- Provider and Zoho values are allowlisted, masked in GitHub logs, and removed after use.
- Operational jobs are serialized with one repository-level concurrency group.

---

### Task 1: Deterministic dispatch controller

**Files:**
- Create: `scripts/remote_runner.py`
- Create: `scripts/test_remote_runner.py`

**Interfaces:**
- Consumes: CLI arguments `validate|prompt|preflight`, `--operation`, `--target`, `--confirmation`, and environment paths `WARDITH_DATA_REPO`/`WARDITH_RUNS_DIR`.
- Produces: `validate_dispatch(operation, target, confirmation) -> None`, `build_prompt(operation, target) -> str`, and a zero/non-zero process result with secret-free messages.

- [ ] **Step 1: Write failing validation and prompt tests**

```python
class DispatchTests(unittest.TestCase):
    def test_paid_run_requires_exact_confirmation(self):
        with self.assertRaisesRegex(ValueError, "confirmation RUN"):
            remote_runner.validate_dispatch("90qrun", "Wirral dentists", "run")

    def test_outreach_requires_exact_confirmation(self):
        with self.assertRaisesRegex(ValueError, "confirmation DRAFT"):
            remote_runner.validate_dispatch("outreach", "wirral-dentists", "")

    def test_preflight_rejects_target(self):
        with self.assertRaisesRegex(ValueError, "target must be blank"):
            remote_runner.validate_dispatch("preflight", "unused", "")

    def test_prompt_uses_provider_neutral_skill(self):
        prompt = remote_runner.build_prompt("qualify", "wirral-dentists")
        self.assertIn(".agents/skills/qualify/SKILL.md", prompt)
        self.assertIn("wirral-dentists", prompt)
```

- [ ] **Step 2: Run the tests and confirm they fail**

Run: `python -m unittest scripts/test_remote_runner.py -v`

Expected: `ModuleNotFoundError` for `scripts.remote_runner`.

- [ ] **Step 3: Implement the controller**

Implement exact operation allowlisting, non-empty target checks for the three operational stages, the two confirmation gates, and prompts that tell Codex to read the matching `.agents/skills/<operation>/SKILL.md`, execute it completely, use `WARDITH_RUNS_DIR`, never alter the core checkout, and never broaden outreach into sending.

The `preflight` command must verify that the core checkout, data checkout, runs directory, `git`, `python`, and `bws` exist; it must create and remove a file inside the data checkout without committing it; and it must print names/status only.

- [ ] **Step 4: Run controller tests**

Run: `python -m unittest scripts/test_remote_runner.py -v`

Expected: all tests pass.

- [ ] **Step 5: Commit Task 1**

```bash
git add scripts/remote_runner.py scripts/test_remote_runner.py
git commit -m "Add remote Wardith dispatch controller"
git push origin main
```

### Task 2: Linux Bitwarden process wrapper

**Files:**
- Create: `scripts/wardith-secrets.sh`
- Create: `scripts/test_wardith_secrets.py`

**Interfaces:**
- Consumes: `BWS_ACCESS_TOKEN`, `BWS_PROJECT_ID`, optional `WARDITH_BWS_CLI`, and `status|run -- <command...>`.
- Produces: the eight approved variables for only the requested child process; `WARDITH_ZOHO_CREDENTIALS` points to a temporary JSON file; `BWS_ACCESS_TOKEN` is absent in the child.

- [ ] **Step 1: Write failing isolation tests with a fake `bws`**

```python
def test_run_exposes_allowlist_but_not_bootstrap_token(self):
    result = run_wrapper("run", "--", sys.executable, child_probe)
    payload = json.loads(result.stdout)
    assert payload["openai"] == "openai-test"
    assert payload["unexpected"] is None
    assert payload["bws_token"] is None
    assert payload["zoho_exists"] is True

def test_temp_zoho_file_is_removed_after_child(self):
    result = run_wrapper("run", "--", sys.executable, child_probe)
    path = json.loads(result.stdout)["zoho_path"]
    assert not Path(path).exists()
```

Also test missing required keys, malformed Zoho JSON, a failing `bws`, and propagation of the child exit code.

- [ ] **Step 2: Run and confirm failure**

Run: `python -m unittest scripts/test_wardith_secrets.py -v`

Expected: failure because `scripts/wardith-secrets.sh` does not exist.

- [ ] **Step 3: Implement the wrapper**

Use `set -euo pipefail`, retrieve only the configured Bitwarden project, parse JSON with Python rather than interpolating shell values, validate the exact eight-key allowlist and six Zoho fields, emit GitHub `::add-mask::` commands when `GITHUB_ACTIONS=true`, write Zoho JSON under `mktemp -d`, unset `BWS_ACCESS_TOKEN` before `exec`-equivalent child invocation, restore the child exit code, and remove the temporary directory in a trap.

- [ ] **Step 4: Run wrapper and Windows regression tests**

Run: `python -m unittest scripts/test_wardith_secrets.py -v`

Run: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/test_wardith_secrets.ps1`

Expected: both suites pass; no test output contains fixture secret values other than explicit fake assertions.

- [ ] **Step 5: Commit Task 2**

```bash
git add scripts/wardith-secrets.sh scripts/test_wardith_secrets.py
git commit -m "Add hosted Wardith secrets wrapper"
git push origin main
```

### Task 3: Phone-triggered GitHub Actions workflow

**Files:**
- Create: `.github/workflows/wardith-remote.yml`
- Create: `.github/wardith-codex/config.toml`
- Create: `.github/wardith-codex/prompt.md`
- Create: `scripts/test_remote_workflow.py`

**Interfaces:**
- Consumes: `workflow_dispatch` inputs `operation`, `target`, `confirmation`; GitHub Environment `wardith-production`; encrypted secrets `BWS_ACCESS_TOKEN`, `WARDITH_DATA_DEPLOY_KEY`.
- Produces: a serialized GitHub Actions run, a Codex final-message artifact, and validated data-repository commits for successful operational runs.

- [ ] **Step 1: Write failing structural workflow tests**

```python
def test_workflow_has_manual_inputs_and_concurrency(self):
    text = WORKFLOW.read_text(encoding="utf-8")
    for value in ("workflow_dispatch:", "operation:", "target:", "confirmation:"):
        assert value in text
    assert "group: wardith-operational-runs" in text
    assert "cancel-in-progress: false" in text

def test_workflow_uses_narrow_secrets_and_official_action(self):
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "secrets.BWS_ACCESS_TOKEN" in text
    assert "secrets.WARDITH_DATA_DEPLOY_KEY" in text
    assert "openai/codex-action@v1" in text
    assert "permission-profile: \"" + ":workspace" + "\"" in text
```

Also assert validation occurs before secret retrieval, `persist-credentials: false` is used for both checkouts, the data checkout uses the deploy key, the action is the last privileged execution step, and artifacts upload on failure.

- [ ] **Step 2: Run and confirm failure**

Run: `python -m unittest scripts/test_remote_workflow.py -v`

Expected: failure because `.github/workflows/wardith-remote.yml` does not exist.

- [ ] **Step 3: Implement the workflow and trusted Codex configuration**

Use `actions/checkout@v5` for the core repository and a second checkout of `hellonovenuk-lang/wardith-crm-data` at `../wardith-data`. Install a pinned `bws` release and verify its published checksum before use. Validate inputs before exporting either bootstrap secret. Generate the prompt with `remote_runner.py`; retrieve only `OPENAI_API_KEY` for the action proxy before the Codex step, while the Wardith wrapper retrieves the operational allowlist for provider commands. Invoke `openai/codex-action@v1` with `permission-profile: ":workspace"`, `safety-strategy: drop-sudo`, a trusted config directory, and `--search`.

Place post-processing that copies, validates, commits, and pushes data in a separate job so the Codex action remains the final step after privilege reduction. Pass artifacts between jobs; never pass a plaintext credential artifact.

- [ ] **Step 4: Run workflow tests and a local YAML parse**

Run: `python -m unittest scripts/test_remote_workflow.py -v`

Run: `python -c "import pathlib; t=pathlib.Path('.github/workflows/wardith-remote.yml').read_text(); assert '\\t' not in t"`

Expected: all tests pass and no tab characters are present.

- [ ] **Step 5: Commit Task 3**

```bash
git add .github scripts/test_remote_workflow.py
git commit -m "Add phone-triggered Wardith workflow"
git push origin main
```

### Task 4: Align skills and operating documentation

**Files:**
- Modify: `.agents/skills/90qrun/SKILL.md`
- Modify: `.agents/skills/qualify/SKILL.md`
- Modify: `.agents/skills/outreach/SKILL.md`
- Modify: `.claude/skills/90qrun/SKILL.md`
- Modify: `.claude/skills/qualify/SKILL.md`
- Modify: `.claude/skills/outreach/SKILL.md`
- Create: `docs/remote-runner.md`

**Interfaces:**
- Consumes: `WARDITH_REMOTE=true`, `WARDITH_RUNS_DIR`, and the hosted wrapper from Task 2.
- Produces: identical provider-neutral and Claude skill rules for hosted GitHub execution, plus simple phone instructions.

- [ ] **Step 1: Add failing consistency assertions**

Extend `scripts/test_remote_workflow.py` to assert that all six skills name `scripts/wardith-secrets.sh`, that remote provider commands use its `run --` interface, and that every outreach copy retains the explicit no-send rule.

- [ ] **Step 2: Run and confirm the assertions fail**

Run: `python -m unittest scripts/test_remote_workflow.py -v`

Expected: failures identifying the Windows-only `.agents` instructions.

- [ ] **Step 3: Update skills and write the operator guide**

Document four phone steps: open the Wardith repository, open Actions, choose `Wardith remote run`, select the operation/target, and type the required confirmation. Document outputs, typical failures, token rotation, deploy-key rotation, and the rule that Zoho drafts are never sent automatically. Remove Claude-only assumptions from shared behaviour while retaining its valid hosted adapter.

- [ ] **Step 4: Run consistency and existing tool tests**

Run: `python -m unittest scripts/test_remote_workflow.py scripts/test_remote_runner.py scripts/test_wardith_secrets.py -v`

Run: `python -m unittest discover -s tools -p 'test_*.py'`

Expected: all tests pass.

- [ ] **Step 5: Commit Task 4**

```bash
git add .agents .claude docs/remote-runner.md scripts/test_remote_workflow.py
git commit -m "Document provider-neutral remote operations"
git push origin main
```

### Task 5: Provision credentials and prove the phone path

**Files:**
- Modify only if verification reveals a defect: files introduced in Tasks 1-4.

**Interfaces:**
- Consumes: a new Bitwarden read-only machine account and a write deploy key restricted to `hellonovenuk-lang/wardith-crm-data`.
- Produces: GitHub secrets `BWS_ACCESS_TOKEN` and `WARDITH_DATA_DEPLOY_KEY`, environment `wardith-production`, and successful laptop/phone preflight runs.

- [ ] **Step 1: Create the repository-restricted deploy key**

Generate an Ed25519 keypair named `wardith-actions-data`; add only its public key to the data repository as a write-enabled deploy key; add the private key to the core repository Actions secret `WARDITH_DATA_DEPLOY_KEY`; delete the local private-key staging file after GitHub confirms storage.

- [ ] **Step 2: Create the hosted Bitwarden identity**

Create machine account `wardith-github-actions`, grant read-only access to project `6ab59b25-f5ae-4e3e-8518-b4b30131120f`, create one non-expiring revocable token, add it directly to GitHub secret `BWS_ACCESS_TOKEN`, and ensure it is never placed in chat, a command argument, or Git history.

- [ ] **Step 3: Configure the protected environment**

Create GitHub Environment `wardith-production`. Enable required reviewers when the repository/account plan exposes that control; otherwise retain the workflow's literal confirmation gates and document the unavailable plan feature.

- [ ] **Step 4: Run laptop preflight**

Dispatch `operation=preflight`, blank target, blank confirmation. Expected: core checkout, data checkout, Bitwarden allowlist, dependencies, and reversible data write check all pass; no provider usage and no Zoho draft occur.

- [ ] **Step 5: Run phone preflight**

Repeat Step 4 from the GitHub mobile app or mobile browser with the laptop powered off. Expected: the workflow completes and its final-message artifact is readable from the phone.

- [ ] **Step 6: Run the complete verification suite**

Run locally: `python -m unittest scripts/test_remote_runner.py scripts/test_wardith_secrets.py scripts/test_remote_workflow.py -v`

Run locally: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/test_wardith_secrets.ps1`

Expected: every test passes.

- [ ] **Step 7: Record rollout completion**

Add one dated line to `playbook/decisions.md` stating that GitHub Actions is the provider-neutral phone runner and that remote outreach creates Zoho drafts only. Commit and push only that operational decision.
