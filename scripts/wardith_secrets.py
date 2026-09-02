#!/usr/bin/env python3
"""Run one hosted Wardith command with an allowlisted Bitwarden environment."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


REQUIRED_KEYS = (
    "OPENAI_API_KEY",
    "OPENAI_MODEL",
    "GEMINI_API_KEY",
    "GEMINI_MODEL",
    "PERPLEXITY_API_KEY",
    "PERPLEXITY_MODEL",
    "COMPANIES_HOUSE_API_KEY",
    "ZOHO_CREDENTIALS_JSON",
)
ZOHO_FIELDS = (
    "client_id",
    "client_secret",
    "refresh_token",
    "account_id",
    "api_domain",
    "accounts_domain",
)


class SecretError(RuntimeError):
    pass


def load_secrets(environment: dict[str, str]) -> tuple[dict[str, str], set[str]]:
    token = environment.get("BWS_ACCESS_TOKEN", "").strip()
    project = environment.get("BWS_PROJECT_ID", "").strip()
    if not token or not project:
        raise SecretError("BWS_ACCESS_TOKEN and BWS_PROJECT_ID are required")
    cli = environment.get("WARDITH_BWS_CLI", "bws")
    try:
        extra_args = json.loads(environment.get("WARDITH_BWS_ARGS", "[]"))
    except json.JSONDecodeError as error:
        raise SecretError("WARDITH_BWS_ARGS must be a JSON string array") from error
    if not isinstance(extra_args, list) or not all(isinstance(item, str) for item in extra_args):
        raise SecretError("WARDITH_BWS_ARGS must be a JSON string array")
    command = [cli, *extra_args, "secret", "list", project, "--output", "json"]
    result = subprocess.run(command, env=environment, text=True, capture_output=True)
    if result.returncode or not result.stdout.strip():
        raise SecretError("Bitwarden secret retrieval failed")
    try:
        items = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise SecretError("Bitwarden returned malformed secret data") from error
    returned_keys = {str(item.get("key", "")) for item in items}
    returned = {str(item.get("key", "")): str(item.get("value", "")) for item in items}
    missing = [key for key in REQUIRED_KEYS if not returned.get(key)]
    if missing:
        raise SecretError("missing required secret(s): " + ", ".join(missing))
    values = {key: returned[key] for key in REQUIRED_KEYS}
    try:
        zoho = json.loads(values["ZOHO_CREDENTIALS_JSON"])
    except json.JSONDecodeError as error:
        raise SecretError("ZOHO_CREDENTIALS_JSON is not valid JSON") from error
    missing_zoho = [field for field in ZOHO_FIELDS if not str(zoho.get(field, "")).strip()]
    if missing_zoho:
        raise SecretError("ZOHO_CREDENTIALS_JSON is missing field(s): " + ", ".join(missing_zoho))
    return values, returned_keys


def child_environment(base: dict[str, str], values: dict[str, str], returned_keys: set[str], zoho_path: Path) -> dict[str, str]:
    child = base.copy()
    child.pop("BWS_ACCESS_TOKEN", None)
    for key in returned_keys:
        child.pop(key, None)
    for key in REQUIRED_KEYS:
        if key != "ZOHO_CREDENTIALS_JSON":
            child[key] = values[key]
    child["WARDITH_ZOHO_CREDENTIALS"] = str(zoho_path)
    return child


def mask_for_github(values: dict[str, str], environment: dict[str, str]) -> None:
    if environment.get("GITHUB_ACTIONS") == "true":
        for value in values.values():
            print(f"::add-mask::{value}")


def run_child(command: list[str], environment: dict[str, str]) -> int:
    if not command:
        raise SecretError("run requires a command after --")
    values, returned_keys = load_secrets(environment)
    mask_for_github(values, environment)
    temp_dir = Path(tempfile.mkdtemp(prefix="wardith-secrets-"))
    zoho_path = temp_dir / "zoho-credentials.json"
    try:
        zoho_path.write_text(values["ZOHO_CREDENTIALS_JSON"], encoding="utf-8")
        child = child_environment(environment, values, returned_keys, zoho_path)
        return subprocess.run(command, env=child).returncode
    finally:
        values.clear()
        shutil.rmtree(temp_dir, ignore_errors=True)


def export_github_environment(environment: dict[str, str]) -> None:
    github_env = environment.get("GITHUB_ENV", "").strip()
    if not github_env:
        raise SecretError("GITHUB_ENV is required for github-env")
    values, _ = load_secrets(environment)
    mask_for_github(values, environment)
    try:
        with Path(github_env).open("a", encoding="utf-8", newline="\n") as output:
            for key in REQUIRED_KEYS:
                export_name = "WARDITH_ZOHO_CREDENTIALS_JSON" if key == "ZOHO_CREDENTIALS_JSON" else key
                value = values[key]
                if "\n" in value or "\r" in value:
                    raise SecretError(f"{key} must be stored as a single line")
                output.write(f"{export_name}={value}\n")
            output.write(f"WARDITH_SECRETS_READY={len(REQUIRED_KEYS)}\n")
    finally:
        values.clear()


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    environment = os.environ.copy()
    try:
        if args == ["status"]:
            values, _ = load_secrets(environment)
            mask_for_github(values, environment)
            values.clear()
            print(f"Bitwarden connection ready: {len(REQUIRED_KEYS)} required secrets available.")
            return 0
        if args and args[0] == "run":
            command = args[2:] if len(args) > 1 and args[1] == "--" else args[1:]
            return run_child(command, environment)
        if args == ["github-env"]:
            export_github_environment(environment)
            return 0
        raise SecretError("use status or run -- <command>")
    except SecretError as error:
        print(f"wardith-secrets: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
