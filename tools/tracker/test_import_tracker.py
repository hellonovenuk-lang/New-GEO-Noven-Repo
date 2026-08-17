import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import import_tracker as it


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


def make_campaign_json(slug, sector="estate agents", geography="Chester",
                        outreach=None):
    return {
        "run": {
            "sector": sector,
            "geography": geography,
            "campaign_slug": slug,
            "date": "2026-08-14",
            "questions": [{"question_id": "q01", "text": "Who?"}],
            "providers": [{"provider": "openai", "model": "gpt-5.6-luna"}],
        },
        "market": [],
        "outreach": outreach or [],
        "excluded": [],
        "sources": [{
            "source_id": "S001", "business": "x", "publisher": "x",
            "fact_supported": "x", "url": "https://x", "access_date": "2026-08-14",
        }],
    }


def make_outreach_entry(business, priority="A", ready="YES"):
    return {
        "priority": priority,
        "business": business,
        "area": "Chester",
        "total_ai_appearances": 0,
        "strongest_competitor": "Rival Ltd",
        "competitor_appearances": 10,
        "competitive_gap_finding": "finding",
        "why_prospect": "why",
        "legal_entity": f"{business} Ltd",
        "company_number": "01234567",
        "company_status": "Active",
        "ready_to_email": ready,
        "evidence_source_ids": ["S001"],
        "accessibility": "DIRECT",
    }


class TrackerTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.runs_dir = Path(self.tmp.name) / "wardith-runs"
        self.runs_dir.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def fresh_tracker(self):
        return it.load_tracker(self.runs_dir / "tracker" / "tracker.json")


class TestSlugify(TrackerTestCase):
    def test_lowercases_and_hyphenates(self):
        self.assertEqual(it.slugify("A Move Homes Limited"), "a-move-homes-limited")

    def test_collapses_and_trims(self):
        self.assertEqual(it.slugify("  Foo & Bar!!  "), "foo-bar")


class TestPipelineStages(TrackerTestCase):
    def test_researched_stage_from_run_log_only(self):
        (self.runs_dir / "roofers-wirral.csv").write_text("provider,question\n")
        (self.runs_dir / "roofers-wirral-run-log.md").write_text(
            "# log\n\n**Date:** 2026-08-16\n**Trade:** Roofers\n**Geography:** Wirral\n"
        )
        tracker = self.fresh_tracker()
        n_c, n_p, warnings = it.import_all(self.runs_dir, tracker)
        self.assertEqual(n_c, 1)
        self.assertEqual(n_p, 0)
        campaign = tracker["campaigns"]["roofers-wirral"]
        self.assertEqual(campaign["pipeline_stage"], "RESEARCHED")
        self.assertEqual(campaign["sector"], "Roofers")
        self.assertEqual(campaign["geography"], "Wirral")

    def test_qualified_stage_from_campaign_json(self):
        slug = "estate-agents-chester"
        write_json(
            self.runs_dir / slug / f"{slug}-campaign.json",
            make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes")]),
        )
        tracker = self.fresh_tracker()
        it.import_all(self.runs_dir, tracker)
        campaign = tracker["campaigns"][slug]
        self.assertEqual(campaign["pipeline_stage"], "QUALIFIED")
        self.assertEqual(campaign["outreach_count"], 1)
        prospect = tracker["prospects"][f"{slug}::a-move-homes"]
        self.assertEqual(prospect["research"]["business"], "A Move Homes")
        self.assertEqual(prospect["research"]["priority"], "A")
        self.assertIsNone(prospect["activity"]["outreach_status"])

    def test_outreach_prepared_stage_and_status(self):
        slug = "estate-agents-chester"
        write_json(
            self.runs_dir / slug / f"{slug}-campaign.json",
            make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes")]),
        )
        write_json(
            self.runs_dir / slug / "outreach" / f"outreach-prep-{slug}-2026-08-15.json",
            [{
                "campaign_slug": slug,
                "business": "A Move Homes",
                "area": "Chester",
                "contact_route": {"person": "Sharon", "role": "MD", "email": "s@x.co.uk"},
                "outreach_angle": "angle",
                "email_subject": "subject",
                "email_body": "body",
                "linkedin_draft": None,
                "caveats": [],
                "evidence_source_ids": ["S001"],
            }],
        )
        tracker = self.fresh_tracker()
        it.import_all(self.runs_dir, tracker)
        campaign = tracker["campaigns"][slug]
        self.assertEqual(campaign["pipeline_stage"], "OUTREACH_PREPARED")
        prospect = tracker["prospects"][f"{slug}::a-move-homes"]
        self.assertEqual(prospect["research"]["contact_person"], "Sharon")
        self.assertEqual(prospect["research"]["email_body"], "body")
        self.assertEqual(prospect["activity"]["outreach_status"], "PREPARED")
        self.assertIsNotNone(prospect["activity"]["prepared_date"])


class TestRerunBehaviour(TrackerTestCase):
    def test_rerun_does_not_duplicate(self):
        slug = "estate-agents-chester"
        write_json(
            self.runs_dir / slug / f"{slug}-campaign.json",
            make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes")]),
        )
        tracker = self.fresh_tracker()
        it.import_all(self.runs_dir, tracker)
        it.import_all(self.runs_dir, tracker)
        self.assertEqual(len(tracker["campaigns"]), 1)
        self.assertEqual(len(tracker["prospects"]), 1)

    def test_rerun_updates_research_but_preserves_manual_activity(self):
        slug = "estate-agents-chester"
        json_path = self.runs_dir / slug / f"{slug}-campaign.json"
        write_json(json_path, make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes", priority="B")]))
        tracker = self.fresh_tracker()
        it.import_all(self.runs_dir, tracker)

        prospect_id = f"{slug}::a-move-homes"
        tracker["prospects"][prospect_id]["activity"]["outreach_status"] = "SENT"
        tracker["prospects"][prospect_id]["activity"]["sent_date"] = "2026-08-16"
        tracker["prospects"][prospect_id]["activity"]["audit_revenue"] = 250

        write_json(json_path, make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes", priority="A")]))
        it.import_all(self.runs_dir, tracker)

        prospect = tracker["prospects"][prospect_id]
        self.assertEqual(prospect["research"]["priority"], "A")
        self.assertEqual(prospect["activity"]["outreach_status"], "SENT")
        self.assertEqual(prospect["activity"]["sent_date"], "2026-08-16")
        self.assertEqual(prospect["activity"]["audit_revenue"], 250)

    def test_do_not_contact_never_cleared(self):
        slug = "estate-agents-chester"
        write_json(
            self.runs_dir / slug / f"{slug}-campaign.json",
            make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes")]),
        )
        tracker = self.fresh_tracker()
        it.import_all(self.runs_dir, tracker)
        prospect_id = f"{slug}::a-move-homes"
        tracker["prospects"][prospect_id]["activity"]["do_not_contact"] = True
        it.import_all(self.runs_dir, tracker)
        self.assertTrue(tracker["prospects"][prospect_id]["activity"]["do_not_contact"])


class TestRobustness(TrackerTestCase):
    def test_malformed_campaign_json_is_skipped_not_raised(self):
        slug = "mid-write-campaign"
        path = self.runs_dir / slug / f"{slug}-campaign.json"
        path.parent.mkdir(parents=True)
        path.write_text('{"run": {"sector": "x"')  # truncated, as if mid-write
        (self.runs_dir / f"{slug}.csv").write_text("provider\n")
        tracker = self.fresh_tracker()
        n_c, n_p, warnings = it.import_all(self.runs_dir, tracker)
        self.assertEqual(n_c, 1)
        self.assertEqual(tracker["campaigns"][slug]["pipeline_stage"], "RESEARCHED")
        self.assertTrue(any("could not parse" in w for w in warnings))

    def test_slug_with_no_source_files_is_absent(self):
        tracker = self.fresh_tracker()
        n_c, n_p, warnings = it.import_all(self.runs_dir, tracker)
        self.assertEqual(n_c, 0)
        self.assertEqual(tracker["campaigns"], {})

    def test_never_writes_inside_a_campaign_folder(self):
        slug = "estate-agents-chester"
        campaign_dir = self.runs_dir / slug
        write_json(campaign_dir / f"{slug}-campaign.json",
                   make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes")]))
        before = sorted(p.relative_to(campaign_dir) for p in campaign_dir.rglob("*") if p.is_file())

        tracker = self.fresh_tracker()
        it.import_all(self.runs_dir, tracker)
        it.save_tracker(tracker, self.runs_dir / "tracker" / "tracker.json")
        it.export_csv(tracker, self.runs_dir / "tracker" / "tracker.csv")

        after = sorted(p.relative_to(campaign_dir) for p in campaign_dir.rglob("*") if p.is_file())
        self.assertEqual(before, after)

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
        tracker = self.fresh_tracker()
        n_c, n_p, warnings = it.import_all(self.runs_dir, tracker)
        prospect = tracker["prospects"][f"{slug}::ghost-estates"]
        self.assertTrue(prospect["research"]["orphaned_outreach_prep"])
        self.assertTrue(any("no matching outreach[]" in w for w in warnings))


class TestWithheldOutreachPrep(TrackerTestCase):
    def test_withheld_entry_is_not_marked_prepared(self):
        slug = "estate-agents-chester"
        write_json(
            self.runs_dir / slug / f"{slug}-campaign.json",
            make_campaign_json(slug, outreach=[make_outreach_entry("Changing-Home", ready="REVIEW")]),
        )
        write_json(
            self.runs_dir / slug / "outreach" / f"outreach-prep-{slug}-2026-08-15.json",
            [{
                "campaign_slug": slug,
                "business": "Changing-Home",
                "area": "Chester",
                "ready_to_email_source": "REVIEW",
                "withheld": True,
                "withheld_reason": "ready_to_email is REVIEW in the source campaign JSON, not YES.",
                "contact_route": None,
                "outreach_angle": None,
                "email_subject": None,
                "email_body": None,
                "linkedin_draft": None,
                "caveats": ["Withheld at Stage 1 gate, not processed further."],
                "evidence_source_ids": [],
            }],
        )
        tracker = self.fresh_tracker()
        it.import_all(self.runs_dir, tracker)
        prospect = tracker["prospects"][f"{slug}::changing-home"]
        self.assertIsNone(prospect["activity"]["outreach_status"])
        self.assertIsNone(prospect["activity"]["prepared_date"])
        self.assertTrue(prospect["research"]["withheld_at_outreach"])
        self.assertEqual(prospect["research"]["withheld_reason"],
                          "ready_to_email is REVIEW in the source campaign JSON, not YES.")

    def test_withheld_orphan_entry_is_not_marked_prepared(self):
        slug = "estate-agents-chester"
        write_json(self.runs_dir / slug / f"{slug}-campaign.json", make_campaign_json(slug, outreach=[]))
        write_json(
            self.runs_dir / slug / "outreach" / f"outreach-prep-{slug}-2026-08-15.json",
            [{
                "campaign_slug": slug, "business": "Ghost Estates", "area": "Chester",
                "withheld": True, "withheld_reason": "contact route dead on re-check",
                "contact_route": None, "outreach_angle": None, "email_subject": None,
                "email_body": None, "linkedin_draft": None, "caveats": [], "evidence_source_ids": [],
            }],
        )
        tracker = self.fresh_tracker()
        it.import_all(self.runs_dir, tracker)
        prospect = tracker["prospects"][f"{slug}::ghost-estates"]
        self.assertTrue(prospect["research"]["orphaned_outreach_prep"])
        self.assertIsNone(prospect["activity"]["outreach_status"])

    def test_genuinely_drafted_entry_is_still_marked_prepared(self):
        slug = "estate-agents-chester"
        write_json(
            self.runs_dir / slug / f"{slug}-campaign.json",
            make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes")]),
        )
        write_json(
            self.runs_dir / slug / "outreach" / f"outreach-prep-{slug}-2026-08-15.json",
            [{
                "campaign_slug": slug, "business": "A Move Homes", "area": "Chester",
                "withheld": False, "withheld_reason": None,
                "contact_route": {"person": "Sharon", "role": "MD", "email": "s@x.co.uk"},
                "outreach_angle": "angle", "email_subject": "subject", "email_body": "body",
                "linkedin_draft": None, "caveats": [], "evidence_source_ids": ["S001"],
            }],
        )
        tracker = self.fresh_tracker()
        it.import_all(self.runs_dir, tracker)
        prospect = tracker["prospects"][f"{slug}::a-move-homes"]
        self.assertEqual(prospect["activity"]["outreach_status"], "PREPARED")
        self.assertIsNotNone(prospect["activity"]["prepared_date"])
        self.assertFalse(prospect["research"]["withheld_at_outreach"])


    def test_a_fresher_withheld_draft_un_prepares_a_stale_prepared_status(self):
        slug = "estate-agents-chester"
        write_json(
            self.runs_dir / slug / f"{slug}-campaign.json",
            make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes")]),
        )
        write_json(
            self.runs_dir / slug / "outreach" / f"outreach-prep-{slug}-2026-08-15.json",
            [{
                "campaign_slug": slug, "business": "A Move Homes", "area": "Chester",
                "withheld": False, "contact_route": {"person": "Sharon", "role": "MD", "email": "s@x.co.uk"},
                "outreach_angle": "a", "email_subject": "s", "email_body": "b",
                "linkedin_draft": None, "caveats": [], "evidence_source_ids": ["S001"],
            }],
        )
        tracker = self.fresh_tracker()
        it.import_all(self.runs_dir, tracker)
        prospect_id = f"{slug}::a-move-homes"
        self.assertEqual(tracker["prospects"][prospect_id]["activity"]["outreach_status"], "PREPARED")

        # /outreach re-run on 08-16 now withholds this business (route died, say).
        write_json(
            self.runs_dir / slug / "outreach" / f"outreach-prep-{slug}-2026-08-16.json",
            [{
                "campaign_slug": slug, "business": "A Move Homes", "area": "Chester",
                "withheld": True, "withheld_reason": "contact route no longer resolves",
                "contact_route": None, "outreach_angle": None, "email_subject": None,
                "email_body": None, "linkedin_draft": None, "caveats": [], "evidence_source_ids": [],
            }],
        )
        it.import_all(self.runs_dir, tracker)
        self.assertIsNone(tracker["prospects"][prospect_id]["activity"]["outreach_status"])
        self.assertIsNone(tracker["prospects"][prospect_id]["activity"]["prepared_date"])

    def test_manual_status_past_prepared_is_never_un_prepared(self):
        slug = "estate-agents-chester"
        write_json(
            self.runs_dir / slug / f"{slug}-campaign.json",
            make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes")]),
        )
        write_json(
            self.runs_dir / slug / "outreach" / f"outreach-prep-{slug}-2026-08-15.json",
            [{
                "campaign_slug": slug, "business": "A Move Homes", "area": "Chester",
                "withheld": False, "contact_route": {"person": "Sharon", "role": "MD", "email": "s@x.co.uk"},
                "outreach_angle": "a", "email_subject": "s", "email_body": "b",
                "linkedin_draft": None, "caveats": [], "evidence_source_ids": ["S001"],
            }],
        )
        tracker = self.fresh_tracker()
        it.import_all(self.runs_dir, tracker)
        prospect_id = f"{slug}::a-move-homes"
        tracker["prospects"][prospect_id]["activity"]["outreach_status"] = "SENT"
        tracker["prospects"][prospect_id]["activity"]["sent_date"] = "2026-08-16"

        write_json(
            self.runs_dir / slug / "outreach" / f"outreach-prep-{slug}-2026-08-16.json",
            [{
                "campaign_slug": slug, "business": "A Move Homes", "area": "Chester",
                "withheld": True, "withheld_reason": "contact route no longer resolves",
                "contact_route": None, "outreach_angle": None, "email_subject": None,
                "email_body": None, "linkedin_draft": None, "caveats": [], "evidence_source_ids": [],
            }],
        )
        it.import_all(self.runs_dir, tracker)
        self.assertEqual(tracker["prospects"][prospect_id]["activity"]["outreach_status"], "SENT")
        self.assertEqual(tracker["prospects"][prospect_id]["activity"]["sent_date"], "2026-08-16")


class TestCanonicalSourcePrecedence(TrackerTestCase):
    def test_older_campaign_json_does_not_supersede_newer_stored_data(self):
        slug = "estate-agents-chester"
        json_path = self.runs_dir / slug / f"{slug}-campaign.json"
        newer = make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes", priority="A")])
        newer["run"]["date"] = "2026-08-16"
        write_json(json_path, newer)
        tracker = self.fresh_tracker()
        it.import_all(self.runs_dir, tracker)
        self.assertEqual(tracker["campaigns"][slug]["run_date"], "2026-08-16")

        older = make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes", priority="C")])
        older["run"]["date"] = "2026-08-10"
        write_json(json_path, older)
        n_c, n_p, warnings = it.import_all(self.runs_dir, tracker)
        self.assertEqual(n_c, 0)
        self.assertEqual(tracker["campaigns"][slug]["run_date"], "2026-08-16")
        self.assertEqual(tracker["prospects"][f"{slug}::a-move-homes"]["research"]["priority"], "A")
        self.assertTrue(any("older than the stored canonical run_date" in w for w in warnings))

    def test_newer_campaign_json_does_supersede(self):
        slug = "estate-agents-chester"
        json_path = self.runs_dir / slug / f"{slug}-campaign.json"
        older = make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes", priority="C")])
        older["run"]["date"] = "2026-08-10"
        write_json(json_path, older)
        tracker = self.fresh_tracker()
        it.import_all(self.runs_dir, tracker)

        newer = make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes", priority="A")])
        newer["run"]["date"] = "2026-08-16"
        write_json(json_path, newer)
        it.import_all(self.runs_dir, tracker)
        self.assertEqual(tracker["prospects"][f"{slug}::a-move-homes"]["research"]["priority"], "A")


class TestImportLog(TrackerTestCase):
    def test_warnings_persist_into_tracker_json_across_runs(self):
        slug = "mid-write-campaign"
        path = self.runs_dir / slug / f"{slug}-campaign.json"
        path.parent.mkdir(parents=True)
        path.write_text('{"run": {"sector": "x"')
        (self.runs_dir / f"{slug}.csv").write_text("provider\n")
        tracker = self.fresh_tracker()
        _n_c, _n_p, warnings = it.import_all(self.runs_dir, tracker)
        it.record_import_log(tracker, warnings)
        self.assertTrue(tracker["import_log"])
        self.assertTrue(any("could not parse" in e["message"] for e in tracker["import_log"]))
        self.assertIn("timestamp", tracker["import_log"][0])

        it.save_tracker(tracker, self.runs_dir / "tracker" / "tracker.json")
        reloaded = it.load_tracker(self.runs_dir / "tracker" / "tracker.json")
        self.assertEqual(reloaded["import_log"], tracker["import_log"])

    def test_import_log_survives_a_run_with_no_new_warnings(self):
        slug = "estate-agents-chester"
        write_json(
            self.runs_dir / slug / f"{slug}-campaign.json",
            make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes")]),
        )
        tracker = self.fresh_tracker()
        tracker["import_log"] = [{"timestamp": "2026-08-01T00:00:00Z", "message": "prior warning"}]
        _n_c, _n_p, warnings = it.import_all(self.runs_dir, tracker)
        it.record_import_log(tracker, warnings)
        self.assertEqual(tracker["import_log"][0]["message"], "prior warning")


class TestCsvExport(TrackerTestCase):
    def test_csv_has_expected_columns_and_rows(self):
        slug = "estate-agents-chester"
        write_json(
            self.runs_dir / slug / f"{slug}-campaign.json",
            make_campaign_json(slug, outreach=[make_outreach_entry("A Move Homes")]),
        )
        tracker = self.fresh_tracker()
        it.import_all(self.runs_dir, tracker)
        csv_path = self.runs_dir / "tracker" / "tracker.csv"
        it.export_csv(tracker, csv_path)

        import csv as csv_mod
        with open(csv_path, encoding="utf-8") as f:
            rows = list(csv_mod.DictReader(f))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["business"], "A Move Homes")
        self.assertEqual(rows[0]["sector"], "estate agents")
        self.assertEqual(set(it.CSV_COLUMNS), set(rows[0].keys()))


if __name__ == "__main__":
    unittest.main()
