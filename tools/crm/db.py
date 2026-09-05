#!/usr/bin/env python3
"""SQLite connection + schema management for the Wardith CRM.

The database file lives outside this repository, at
~/wardith-runs/crm/wardith.db by default - the same "code in the repo,
data next to the campaign folders it was built from" split
tools/tracker/ already keeps. Nothing here ever writes inside the repo.
"""

import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path.home() / "wardith-runs" / "crm" / "wardith.db"

SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def connect(db_path=None):
    db_path = Path(db_path).expanduser() if db_path else DEFAULT_DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn):
    """Idempotent - safe to call on every startup. CREATE TABLE IF NOT
    EXISTS means a rerun never touches existing data."""
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    # Existing databases already have editable cadence rows; add only missing
    # sequence defaults and preserve any owner changes.
    from models import migrate_cadence_defaults
    migrate_cadence_defaults(conn)
    conn.commit()
