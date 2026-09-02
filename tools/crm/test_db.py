import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import db as db_mod
import models


class TestSchemaInit(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp.name) / "wardith.db"
        self.conn = None

    def tearDown(self):
        if self.conn is not None:
            self.conn.close()
        self.tmp.cleanup()

    def test_init_db_creates_all_tables(self):
        conn = self.conn = db_mod.connect(self.db_path)
        db_mod.init_db(conn)
        tables = {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()}
        for expected in ("campaigns", "prospects", "activities", "cadence_settings",
                          "clients", "client_activities", "import_log"):
            self.assertIn(expected, tables)

    def test_init_db_is_idempotent(self):
        conn = self.conn = db_mod.connect(self.db_path)
        db_mod.init_db(conn)
        db_mod.init_db(conn)  # must not raise or wipe data
        conn.execute("INSERT INTO campaigns (campaign_id) VALUES ('x')")
        conn.commit()
        db_mod.init_db(conn)
        row = conn.execute("SELECT campaign_id FROM campaigns WHERE campaign_id='x'").fetchone()
        self.assertIsNotNone(row)

    def test_db_file_created_outside_repo_path_given(self):
        conn = self.conn = db_mod.connect(self.db_path)
        db_mod.init_db(conn)
        conn.close()
        self.conn = None
        self.assertTrue(self.db_path.exists())


class TestCadenceSeeding(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.conn = db_mod.connect(Path(self.tmp.name) / "wardith.db")
        db_mod.init_db(self.conn)

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def test_seed_populates_18_activity_types(self):
        models.seed_cadence_if_empty(self.conn)
        rows = models.list_cadence_settings(self.conn)
        self.assertEqual(len(rows), 18)

    def test_seed_is_a_noop_once_populated(self):
        models.seed_cadence_if_empty(self.conn)
        models.update_cadence_setting(
            self.conn, "EMAIL_1_SENT", next_action_label="Custom", cadence_days=3,
            stage_label="Contacted", stops_cold_followup=False, blocks_outreach=False,
            is_revenue_event=False,
        )
        models.seed_cadence_if_empty(self.conn)  # must not overwrite the edit
        row = models.cadence_dict_from_db(self.conn)["EMAIL_1_SENT"]
        self.assertEqual(row["next_action_label"], "Custom")
        self.assertEqual(row["cadence_days"], 3)


if __name__ == "__main__":
    unittest.main()
