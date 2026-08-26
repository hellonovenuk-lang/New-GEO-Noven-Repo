import json
import os
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import app as app_mod
import cadence as cad
import db as db_mod


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


SAMPLE_CAMPAIGN = {
    "run": {"sector": "plumbers", "geography": "Sampleford",
            "campaign_slug": "plumbers-sampleford-2026-01", "date": "2026-01-15"},
    "market": [],
    "outreach": [
        {"priority": "A", "opportunity_type": "GAP", "business": "Fictional Plumbing Ltd",
         "area": "Sampleford", "company_number": "00000001", "company_status": "Active",
         "contact_email": "[PLACEHOLDER]", "ready_to_email": "REVIEW",
         "evidence_source_ids": ["S001"]},
        {"priority": "B", "opportunity_type": "GAP", "business": "Sampleford Rapid Plumbers Ltd",
         "area": "Sampleford", "company_number": "00000002", "company_status": "Active",
         "contact_person": "J. Fictional", "contact_email": "j@example.invalid",
         "ready_to_email": "YES", "evidence_source_ids": ["S003"]},
    ],
    "excluded": [],
    "sources": [],
}


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.runs_dir = Path(self.tmp.name) / "wardith-runs"
        slug = "plumbers-sampleford-2026-01"
        write_json(self.runs_dir / slug / f"{slug}-campaign.json", SAMPLE_CAMPAIGN)
        self.db_path = Path(self.tmp.name) / "wardith.db"
        self.flask_app = app_mod.create_app(db_path=self.db_path, runs_dir=self.runs_dir)
        self.flask_app.testing = True
        self.client = self.flask_app.test_client()
        # Prime the database the same way the "Refresh from campaigns" button does.
        self.client.post("/ingest")

    def tearDown(self):
        self.tmp.cleanup()


class TestDbPathDefaultsFromRunsDir(unittest.TestCase):
    """Regression: create_app(db_path=None, runs_dir=X) must read/write
    <X>/crm/wardith.db, not db.py's own hardcoded ~/wardith-runs default -
    otherwise a non-default --runs-dir silently talks to the wrong (or a
    real) database instead of the one it was just pointed at."""

    def test_db_path_is_derived_from_runs_dir_when_omitted(self):
        with tempfile.TemporaryDirectory() as tmp:
            runs_dir = Path(tmp) / "wardith-runs"
            flask_app = app_mod.create_app(db_path=None, runs_dir=runs_dir)
            self.assertEqual(flask_app.config["DB_PATH"], runs_dir / "crm" / "wardith.db")
            with flask_app.test_client() as client:
                client.get("/")  # triggers get_db(), which must create the DB at that path
            self.assertTrue((runs_dir / "crm" / "wardith.db").exists())


class TestPagesRender(AppTestCase):
    def test_every_page_returns_200(self):
        for path in ("/", "/prospects", "/activities", "/campaigns", "/pipeline",
                     "/revenue", "/settings/cadence", "/import-log", "/clients"):
            with self.subTest(path=path):
                resp = self.client.get(path)
                self.assertEqual(resp.status_code, 200)

    def test_prospect_detail_renders_and_never_fabricates_a_placeholder(self):
        resp = self.client.get("/prospects/plumbers-sampleford-2026-01::cn-00000001")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"[PLACEHOLDER]", resp.data)

    def test_unknown_prospect_is_404(self):
        resp = self.client.get("/prospects/does-not-exist")
        self.assertEqual(resp.status_code, 404)


class TestActivityLogging(AppTestCase):
    def test_logging_an_activity_persists_and_changes_computed_stage(self):
        # Dated today, so its due date (today + cadence_days) is always in
        # the future regardless of what "today" is in the environment the
        # test runs in - deterministic without needing to freeze the clock.
        prospect_id = "plumbers-sampleford-2026-01::cn-00000002"
        resp = self.client.post(f"/prospects/{prospect_id}", data={
            "form": "activity", "activity_type": "EMAIL_1_SENT", "activity_date": date.today().isoformat(),
        })
        self.assertEqual(resp.status_code, 302)

        detail = self.client.get(f"/prospects/{prospect_id}")
        self.assertIn(b"Contacted", detail.data)

        # Persists across a fresh connection (a new process would see the same row).
        conn = db_mod.connect(self.db_path)
        rows = conn.execute(
            "SELECT * FROM activities WHERE prospect_id = ?", (prospect_id,)
        ).fetchall()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["activity_type"], "EMAIL_1_SENT")
        conn.close()

    def test_weekend_due_date_rolls_to_monday_through_the_live_ui(self):
        # Monday 2026-08-10 + 5 days (EMAIL_1_SENT's cadence) = Saturday
        # 2026-08-15 -> should roll to Monday 2026-08-17. Checked against
        # cadence.due_date() directly rather than a hardcoded literal, so
        # this test doesn't depend on what "today" happens to be (it may
        # render as overdue in the far future - the due *date* itself,
        # which the template always shows, must still be right).
        activity_date = date(2026, 8, 10)
        self.assertEqual(activity_date.isoweekday(), 1)  # confirm it's a Monday
        expected_due = cad.due_date(activity_date, cad.cadence_by_key()["EMAIL_1_SENT"]["cadence_days"])
        self.assertEqual(expected_due, date(2026, 8, 17))

        prospect_id = "plumbers-sampleford-2026-01::cn-00000002"
        self.client.post(f"/prospects/{prospect_id}", data={
            "form": "activity", "activity_type": "EMAIL_1_SENT", "activity_date": activity_date.isoformat(),
        })
        resp = self.client.get(f"/prospects/{prospect_id}")
        self.assertIn(expected_due.isoformat().encode(), resp.data)


class TestCadenceSettingsEdit(AppTestCase):
    def test_editing_a_cadence_row_changes_due_date_immediately(self):
        conn = db_mod.connect(self.db_path)
        rows = conn.execute("SELECT key FROM cadence_settings").fetchall()
        keys = [r["key"] for r in rows]
        conn.close()

        activity_date = date.today()
        prospect_id = "plumbers-sampleford-2026-01::cn-00000002"
        self.client.post(f"/prospects/{prospect_id}", data={
            "form": "activity", "activity_type": "EMAIL_1_SENT", "activity_date": activity_date.isoformat(),
        })

        form_data = {"key": keys}
        for key in keys:
            form_data[f"next_action_label__{key}"] = "x"
            form_data[f"stage_label__{key}"] = "x"
            form_data[f"cadence_days__{key}"] = "3" if key == "EMAIL_1_SENT" else ""
        self.client.post("/settings/cadence", data=form_data)

        detail = self.client.get(f"/prospects/{prospect_id}")
        expected_due = cad.adjust_for_weekend(activity_date + timedelta(days=3))
        self.assertIn(expected_due.isoformat().encode(), detail.data)
        self.assertNotIn(b"cadence_days__", detail.data)  # sanity: not looking at the settings form itself


class TestClientsModule(AppTestCase):
    def test_convert_prospect_to_client_prefills_and_is_separate_from_sales_activities(self):
        prospect_id = "plumbers-sampleford-2026-01::cn-00000002"
        resp = self.client.post(f"/prospects/{prospect_id}/convert-to-client")
        self.assertEqual(resp.status_code, 302)
        client_list = self.client.get("/clients")
        self.assertIn(b"Sampleford Rapid Plumbers Ltd", client_list.data)

        conn = db_mod.connect(self.db_path)
        client_row = conn.execute(
            "SELECT * FROM clients WHERE prospect_id = ?", (prospect_id,)
        ).fetchone()
        self.assertIsNotNone(client_row)
        self.assertEqual(client_row["contact_person"], "J. Fictional")
        client_id = client_row["client_id"]
        conn.close()

        self.client.post(f"/clients/{client_id}", data={
            "form": "client_activity", "activity_type": "Check-in", "activity_date": "2026-08-10",
        })
        conn = db_mod.connect(self.db_path)
        sales_activities = conn.execute(
            "SELECT * FROM activities WHERE prospect_id = ?", (prospect_id,)
        ).fetchall()
        client_activities = conn.execute(
            "SELECT * FROM client_activities WHERE client_id = ?", (client_id,)
        ).fetchall()
        conn.close()
        self.assertEqual(sales_activities, [])
        self.assertEqual(len(client_activities), 1)


if __name__ == "__main__":
    unittest.main()
