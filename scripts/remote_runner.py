#!/usr/bin/env python3
"""Validate and prepare phone-triggered Wardith operations."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


OPERATIONS = {"preflight", "90qrun", "qualify", "outreach"}


def validate_dispatch(operation: str, target: str, confirmation: str) -> None:
    if operation not in OPERATIONS:
        raise ValueError(f"unsupported operation: {operation}")
    if operation == "preflight":
        if target.strip():
            raise ValueError("preflight target must be blank")
        if confirmation.strip():
            raise ValueError("preflight confirmation must be blank")
        return
    if not target.strip():
        raise ValueError(f"target is required for {operation}")
    if operation == "90qrun" and confirmation != "RUN":
        raise ValueError("90qrun requires confirmation RUN")
    if operation == "outreach" and confirmation != "DRAFT":
        raise ValueError("outreach requires confirmation DRAFT")
    if operation == "qualify" and confirmation.strip():
        raise ValueError("qualify confirmation must be blank")


def build_prompt(operation: str, target: str) -> str:
    if operation == "preflight":
        raise ValueError("preflight does not use an agent prompt")
    if operation not in OPERATIONS:
        raise ValueError(f"unsupported operation: {operation}")
    safety = ""
    if operation == "outreach":
        safety = (
            " Never send email, submit forms, or post to LinkedIn. "
            "Create or update Zoho drafts only."
        )
    return (
        f"Read .agents/skills/{operation}/SKILL.md completely and execute it "
        f"for target {target!r}. Use WARDITH_RUNS_DIR for all operational "
        "outputs and do not modify the Wardith core checkout. Complete every "
        "stage that does not require new owner judgment, then report genuine "
        f"blockers plainly.{safety}"
    )


def run_preflight(core: Path, data: Path, runs: Path) -> None:
    for label, path in (("core", core), ("data", data)):
        if not path.is_dir():
            raise ValueError(f"{label} checkout is missing: {path}")
    runs.mkdir(parents=True, exist_ok=True)
    for command in ("git", "python", "bws"):
        if shutil.which(command) is None:
            raise ValueError(f"required command is missing: {command}")
    probe = data / ".wardith-write-probe"
    try:
        probe.write_text("preflight\n", encoding="utf-8")
    finally:
        probe.unlink(missing_ok=True)
    print("Wardith remote preflight ready: repositories, runtime, and reversible data write passed.")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("validate", "prompt", "preflight"))
    parser.add_argument("--operation", required=True, choices=sorted(OPERATIONS))
    parser.add_argument("--target", default="")
    parser.add_argument("--confirmation", default="")
    parser.add_argument("--core", type=Path, default=Path.cwd())
    parser.add_argument("--data", type=Path)
    parser.add_argument("--runs", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        validate_dispatch(args.operation, args.target, args.confirmation)
        if args.action == "prompt":
            print(build_prompt(args.operation, args.target))
        elif args.action == "preflight":
            if args.operation != "preflight" or args.data is None or args.runs is None:
                raise ValueError("preflight requires operation=preflight, --data, and --runs")
            run_preflight(args.core, args.data, args.runs)
    except ValueError as error:
        print(f"remote-runner: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
