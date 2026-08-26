#!/usr/bin/env python3
"""Wardith CRM entry point.

    python3 tools/crm/main.py serve   # start the local web app
    python3 tools/crm/main.py ingest  # pull in the latest campaign/outreach output

Invoked the same way as the other tools/*/*.py scripts in this repo
(direct script execution, not `python -m`) so its imports and test
discovery follow the same convention as tools/tracker/.
"""

import argparse
import sys
from pathlib import Path

import db as db_mod
import ingest
import models


def cmd_serve(args):
    import app as app_mod

    flask_app = app_mod.create_app(db_path=args.db_path, runs_dir=args.runs_dir)
    print(f"Wardith CRM: http://127.0.0.1:{args.port}  (Ctrl+C to stop)")
    print(f"Data: {args.db_path or (Path(args.runs_dir).expanduser() / 'crm' / 'wardith.db')}")
    flask_app.run(host="127.0.0.1", port=args.port, debug=args.debug)


def cmd_ingest(args):
    return ingest.main([
        "--runs-dir", args.runs_dir,
        *(["--db-path", args.db_path] if args.db_path else []),
        *([a for slug in (args.slug or []) for a in ("--slug", slug)]),
    ])


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python3 tools/crm/main.py", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    serve_p = sub.add_parser("serve", help="Start the local web app")
    serve_p.add_argument("--port", type=int, default=8420)
    serve_p.add_argument("--debug", action="store_true")
    serve_p.set_defaults(func=cmd_serve)

    ingest_p = sub.add_parser("ingest", help="Import the latest campaign/outreach output")
    ingest_p.add_argument("--slug", action="append", default=None)
    ingest_p.set_defaults(func=cmd_ingest)

    for p in (serve_p, ingest_p):
        p.add_argument("--runs-dir", default=str(Path.home() / "wardith-runs"),
                        help="Where /90qrun, /qualify and /outreach write their output.")
        p.add_argument("--db-path", default=None,
                        help="Where the CRM database lives. Default: <runs-dir>/crm/wardith.db")

    args = parser.parse_args(argv)
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
