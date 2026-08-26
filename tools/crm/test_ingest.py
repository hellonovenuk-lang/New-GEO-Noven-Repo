import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import db as db_mod
import ingest as it


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


def make_campaign_json(slug, sector="estate agents", geography="Chester", outreach=None):
    return {
        "run": {
            "sector": sector, "geography": geography, "campaign_slug": slug,
            "date": "2026-08-14",
            "questions": [{"question_id": "q01", "text": "Who?"}],
            "providers": [{"provider": "openai", "model": "gpt-5.6-luna"}],
        },
        "market": [], "outreach": outreach or [], "excluded": [],
        "sources": [{
            "source_id": "S001", "business": "x", "publisher": "x",
            "fact_supported": "x", "url": "https://x", "access_date": "2026-08-14",
        }],
    }


def make_outreach_entry(business, priority="A", ready="YES", company_number="01234567"):
    return {
        "priority": priority, "business": business, "area": "Chester",
        "total_ai_appearances": 0, "strongest_competitor": "Rival Ltd",
        "competitor_appearances": 10, "competitive_gap_finding": "finding",
        "why_prospect": "why", "legal_entity": f"{business} Ltd",
        "company_number": company_number, "company_status": "Active",
        "ready_to_email": ready, "evidence_source_ids": ["S001"],
        "accessibility": "DIRECT",
    }


class IngestTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.runs_dir = Path(self.tmp.name) / "wardith-runs"
        self.runs_dir.mkdir()
        self.conn = db_mod.connect(Path(self.tmp.name) / "wardith.db")
        db_mod.init_db(self.conn)

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()


class TestSlugify(IngestTestCase):
    def test_lowercases_and_hyphenates(self):
        self.assertEqual(it.slugify("A Move Homes Limited"), "a-move-homes-limited")

    def test_collapses_and_trims(self):
        self.assertEqual(it.slugify("  Foo & Bar!!  "), "foo-bar")


class TestPipelineStages(IngestTestCase):
    def test_researched_stage_from_run_log_only(self):
        (self.runs_dir / "roofers-wirral.csv").write_text("provider,question\n")
        (self.runs_dir / "roofers-wirral-run-log.md").write_text(
            "# log\n\n**Date:** 2026-08-16\n**Trade:** Roofers\n**Geography:** Wirral\n"
        )
        n_c, n_p, warnings = it.import_all(self.conn, self.runs_dir)
        self.assertEqual(n_c, 1)
        self.assertEqual(n_p, 0)
        campaign = it.get_campaign(self.conn, "roofers-wirral")
        self.assertEqual(campaign["pipeline_stage"], "RESEARCHED")
        self.assertEqual(campaign["sector"], "Roofers")
        self.assertEqual(campaign["geography"], "Wirral")

    def test_qualified_stage_from_campaign_json(self):
        slug = "estate-agents-chester"
        write_json(self.runs_dir / slug / f"{slug}-campaign.json",
                   make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes")]))
        it.import_all(self.conn, self.runs_dir)
        campaign = it.get_campaign(self.conn, slug)
        self.assertEqual(campaign["pipeline_stage"], "QUALIFIED")
        self.assertEqual(campaign["outreach_count"], 1)
        prospect = it.get_prospect(self.conn, f"{slug}::cn-01234567")
        self.assertEqual(prospect["business"], "A Move Homes")
        self.assertEqual(prospect["priority"], "A")

    def test_outreach_prepared_stage_and_activity_unaffected(self):
        slug = "estate-agents-chester"
        write_json(self.runs_dir / slug / f"{slug}-campaign.json",
                   make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes")]))
        write_json(
            self.runs_dir / slug / "outreach" / f"outreach-prep-{slug}-2026-08-15.json",
            [{
                "campaign_slug": slug, "business": "A Move Homes", "area": "Chester",
                "contact_route": {"person": "Sharon", "role": "MD", "email": "s@x.co.uk"},
                "outreach_angle": "angle", "email_subject": "subject", "email_body": "body",
                "linkedin_draft": None, "caveats": [], "evidence_source_ids": ["S001"],
            }],
        )
        it.import_all(self.conn, self.runs_dir)
        campaign = it.get_campaign(self.conn, slug)
        self.assertEqual(campaign["pipeline_stage"], "OUTREACH_PREPARED")
        prospect = it.get_prospect(self.conn, f"{slug}::cn-01234567")
        self.assertEqual(prospect["contact_person"], "Sharon")
        self.assertEqual(prospect["email_body"], "body")
        # No "activity" concept lives on the prospect row itself any more -
        # ingest never writes to the activities table at all.
        activities = self.conn.execute(
            "SELECT * FROM activities WHERE prospect_id = ?", (prospect["prospect_id"],)
        ).fetchall()
        self.assertEqual(activities, [])


class TestRerunBehaviour(IngestTestCase):
    def test_rerun_does_not_duplicate(self):
        slug = "estate-agents-chester"
        write_json(self.runs_dir / slug / f"{slug}-campaign.json",
                   make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes")]))
        it.import_all(self.conn, self.runs_dir)
        it.import_all(self.conn, self.runs_dir)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM campaigns").fetchone()[0], 1)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM prospects").fetchone()[0], 1)

    def test_rerun_updates_research_but_never_touches_activities_or_manual_fields(self):
        slug = "estate-agents-chester"
        json_path = self.runs_dir / slug / f"{slug}-campaign.json"
        write_json(json_path, make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes", priority="B")]))
        it.import_all(self.conn, self.runs_dir)

        prospect_id = f"estate-agents-chester::cn-01234567"
        self.conn.execute(
            "UPDATE prospects SET do_not_contact_manual = 1, notes = 'hand-typed note' WHERE prospect_id = ?",
            (prospect_id,),
        )
        self.conn.execute(
            "INSERT INTO activities (prospect_id, activity_type, activity_date, created_at) "
            "VALUES (?, 'EMAIL_1_SENT', '2026-08-16', '2026-08-16T00:00:00Z')",
            (prospect_id,),
        )
        self.conn.commit()

        write_json(json_path, make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes", priority="A")]))
        it.import_all(self.conn, self.runs_dir)

        prospect = it.get_prospect(self.conn, prospect_id)
        self.assertEqual(prospect["priority"], "A")
        self.assertEqual(prospect["do_not_contact_manual"], 1)
        self.assertEqual(prospect["notes"], "hand-typed note")
        activities = self.conn.execute(
            "SELECT * FROM activities WHERE prospect_id = ?", (prospect_id,)
        ).fetchall()
        self.assertEqual(len(activities), 1)


class TestBusinessKeyIdentity(IngestTestCase):
    def test_company_number_anchors_identity_across_a_rename(self):
        slug = "estate-agents-chester"
        write_json(
            self.runs_dir / slug / f"{slug}-campaign.json",
            make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes", company_number="09999999")]),
        )
        it.import_all(self.conn, self.runs_dir)
        prospect_id = f"{slug}::cn-09999999"
        self.assertIsNotNone(it.get_prospect(self.conn, prospect_id))

        # Same company, renamed - the company number keeps it the same row.
        write_json(
            self.runs_dir / slug / f"{slug}-campaign.json",
            make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes Ltd (rebrand)", company_number="09999999")]),
        )
        it.import_all(self.conn, self.runs_dir)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM prospects").fetchone()[0], 1)
        prospect = it.get_prospect(self.conn, prospect_id)
        self.assertEqual(prospect["business"], "A Move Homes Ltd (rebrand)")

    def test_falls_back_to_slugified_name_with_no_company_number(self):
        slug = "estate-agents-chester"
        entry = make_outreach_entry("A Move Homes")
        del entry["company_number"]
        write_json(self.runs_dir / slug / f"{slug}-campaign.json", make_campaign_json(slug, outreach=[entry]))
        it.import_all(self.conn, self.runs_dir)
        self.assertIsNotNone(it.get_prospect(self.conn, f"{slug}::a-move-homes"))


class TestRobustness(IngestTestCase):
    def test_malformed_campaign_json_is_skipped_not_raised(self):
        slug = "mid-write-campaign"
        path = self.runs_dir / slug / f"{slug}-campaign.json"
        path.parent.mkdir(parents=True)
        path.write_text('{"run": {"sector": "x"')
        (self.runs_dir / f"{slug}.csv").write_text("provider\n")
        n_c, n_p, warnings = it.import_all(self.conn, self.runs_dir)
        self.assertEqual(n_c, 1)
        self.assertEqual(it.get_campaign(self.conn, slug)["pipeline_stage"], "RESEARCHED")
        self.assertTrue(any("could not parse" in w for w in warnings))

    def test_orphaned_outreach_prep_entry_is_recorded_not_dropped(self):
        slug = "estate-agents-chester"
        write_json(self.runs_dir / slug / f"{slug}-campaign.json", make_campaign_json(slug, outreach=[]))
        write_json(
            self.runs_dir / slug / "outreach" / f"outreach-prep-{slug}-2026-08-15.json",
            [{
                "campaign_slug": slug, "business": "Ghost Estates", "area": "Chester",
                "contact_route": {"person": None, "role": None, "email": None},
                "outreach_angle": "a", "email_subject": "s", "email_body": "b",
                "linkedin_draft": None, "caveats": [], "evidence_source_ids": [],
            }],
        )
        n_c, n_p, warnings = it.import_all(self.conn, self.runs_dir)
        prospect = it.get_prospect(self.conn, f"{slug}::ghost-estates")
        self.assertEqual(prospect["orphaned_outreach_prep"], 1)
        self.assertTrue(any("no matching outreach[]" in w for w in warnings))

    def test_never_writes_inside_a_campaign_folder(self):
        slug = "estate-agents-chester"
        campaign_dir = self.runs_dir / slug
        write_json(campaign_dir / f"{slug}-campaign.json",
                   make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes")]))
        before = sorted(p.relative_to(campaign_dir) for p in campaign_dir.rglob("*") if p.is_file())
        it.import_all(self.conn, self.runs_dir)
        after = sorted(p.relative_to(campaign_dir) for p in campaign_dir.rglob("*") if p.is_file())
        self.assertEqual(before, after)


class TestWithheldOutreachPrep(IngestTestCase):
    def test_withheld_entry_is_recorded_but_not_hidden(self):
        slug = "estate-agents-chester"
        write_json(
            self.runs_dir / slug / f"{slug}-campaign.json",
            make_campaign_json(slug, outreach=[make_outreach_entry("Changing-Home", ready="REVIEW")]),
        )
        write_json(
            self.runs_dir / slug / "outreach" / f"outreach-prep-{slug}-2026-08-15.json",
            [{
                "campaign_slug": slug, "business": "Changing-Home", "area": "Chester",
                "withheld": True,
                "withheld_reason": "ready_to_email is REVIEW in the source campaign JSON, not YES.",
                "contact_route": None, "outreach_angle": None, "email_subject": None,
                "email_body": None, "linkedin_draft": None,
                "caveats": ["Withheld at Stage 1 gate, not processed further."],
                "evidence_source_ids": [],
            }],
        )
        it.import_all(self.conn, self.runs_dir)
        prospect = it.get_prospect(self.conn, f"{slug}::cn-01234567")
        self.assertEqual(prospect["withheld_at_outreach"], 1)
        self.assertEqual(
            prospect["withheld_reason"],
            "ready_to_email is REVIEW in the source campaign JSON, not YES.",
        )


class TestCanonicalSourcePrecedence(IngestTestCase):
    def test_older_campaign_json_does_not_supersede_newer_stored_data(self):
        slug = "estate-agents-chester"
        json_path = self.runs_dir / slug / f"{slug}-campaign.json"
        newer = make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes", priority="A")])
        newer["run"]["date"] = "2026-08-16"
        write_json(json_path, newer)
        it.import_all(self.conn, self.runs_dir)
        self.assertEqual(it.get_campaign(self.conn, slug)["run_date"], "2026-08-16")

        older = make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes", priority="C")])
        older["run"]["date"] = "2026-08-10"
        write_json(json_path, older)
        n_c, n_p, warnings = it.import_all(self.conn, self.runs_dir)
        self.assertEqual(n_c, 0)
        self.assertEqual(it.get_campaign(self.conn, slug)["run_date"], "2026-08-16")
        self.assertEqual(it.get_prospect(self.conn, f"{slug}::cn-01234567")["priority"], "A")
        self.assertTrue(any("older than the stored canonical run_date" in w for w in warnings))


class TestImportLog(IngestTestCase):
    def test_warnings_persist_across_runs(self):
        slug = "mid-write-campaign"
        path = self.runs_dir / slug / f"{slug}-campaign.json"
        path.parent.mkdir(parents=True)
        path.write_text('{"run": {"sector": "x"')
        (self.runs_dir / f"{slug}.csv").write_text("provider\n")
        n_c, n_p, warnings = it.import_all(self.conn, self.runs_dir)
        it.record_import_log(self.conn, warnings)
        self.conn.commit()
        rows = self.conn.execute("SELECT * FROM import_log").fetchall()
        self.assertTrue(rows)
        self.assertTrue(any("could not parse" in r["message"] for r in rows))


if __name__ == "__main__":
    unittest.main()
