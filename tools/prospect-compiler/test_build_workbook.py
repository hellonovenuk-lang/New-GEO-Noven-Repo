#!/usr/bin/env python3
"""
Regression tests for build_workbook.py's validate() and rendering logic.
Stdlib unittest + openpyxl (used read-only, to confirm data-only reopening
returns populated calculated values - see README.md).

Run: python3 test_build_workbook.py -v
"""
import copy
import json
import os
import tempfile
import unittest

from openpyxl import load_workbook

import build_workbook as bw
import scoring_engine as se

SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "sample", "sample-campaign.json")


def load_sample():
    with open(SAMPLE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def scored_fixture():
    """A small, schema-valid, fully-scored campaign (2 outreach businesses,
    one ready, one not) - enough to exercise every sheet builder without
    depending on any real campaign's data."""
    data = {
        "run": {
            "sector": "fictitious trade", "geography": "Sampleford", "campaign_slug": "wb-test", "date": "2026-08-16",
            "questions": [
                {"question_id": "q01", "text": "best A and B providers"},
                {"question_id": "q02", "text": "B only question"},
            ],
            "providers": [{"provider": "openai", "model": "x"}],
            "responses_per_question": 15,
            "service_scopes": [{"label": "combined", "applicable_services": ["A", "B"]}],
            "question_relevance": [
                {"question_id": "q01", "type": "SINGLE_SERVICE_INCLUSIVE", "rationale": "inclusive"},
                {"question_id": "q02", "type": "SERVICE_ONLY", "service": "B", "rationale": "b only"},
            ],
        },
        "market": [],
        "outreach": [
            {
                "priority": "REVIEW", "business": "Ready Co", "area": "Sampleford", "total_ai_appearances": 0,
                "strongest_competitor": "x", "competitor_appearances": 0, "competitive_gap_finding": "x",
                "why_prospect": "x", "legal_entity": "x", "company_number": "1", "company_status": "Active",
                "ready_to_email": "REVIEW", "evidence_source_ids": ["S001"], "accessibility": "DIRECT",
                "service_scope": "combined", "question_appearances": {"q01": 5, "q02": 5},
                "commercial_fit": 5, "service_relevance": 5, "business_credibility": 5, "ability_to_buy": 5,
                "decision_maker_identified": 5, "direct_dm_route": 5, "contact_route_quality": 5,
                "contact_identity_confidence": 5, "research_completeness": 5,
            },
            {
                "priority": "REVIEW", "business": "Not Ready Co", "area": "Sampleford", "total_ai_appearances": 0,
                "strongest_competitor": "x", "competitor_appearances": 0, "competitive_gap_finding": "x",
                "why_prospect": "x", "legal_entity": "x", "company_number": "2", "company_status": "Active",
                "ready_to_email": "REVIEW", "evidence_source_ids": ["S001"], "accessibility": "REVIEW",
                "service_scope": "combined", "question_appearances": {"q01": 1, "q02": 0},
                "commercial_fit": 2, "service_relevance": 2, "business_credibility": 1, "ability_to_buy": 1,
                "decision_maker_identified": 0, "direct_dm_route": 0, "contact_route_quality": 0,
                "contact_identity_confidence": 0, "research_completeness": 1,
            },
        ],
        "excluded": [],
        "sources": [{"source_id": "S001", "business": "x", "publisher": "x", "fact_supported": "x",
                     "url": "x", "access_date": "2026-08-16", "fact_category": "AI_APPEARANCE"}],
    }
    se.run_engine(data)
    return data


class ValidateLegacyFieldsTests(unittest.TestCase):
    """The pre-v2 required fields/enums /outreach depends on - unchanged."""

    def test_sample_campaign_validates_as_shipped(self):
        data = load_sample()
        bw.validate(data)  # must not raise

    def test_outreach_entry_missing_accessibility_fails(self):
        data = load_sample()
        del data["outreach"][0]["accessibility"]
        with self.assertRaises(bw.ValidationError) as ctx:
            bw.validate(data)
        self.assertIn("accessibility", str(ctx.exception))

    def test_outreach_entry_bad_accessibility_value_fails(self):
        data = load_sample()
        data["outreach"][0]["accessibility"] = "SOMEWHERE_ELSE"
        with self.assertRaises(bw.ValidationError):
            bw.validate(data)

    def test_market_entry_accessibility_is_optional(self):
        data = load_sample()
        self.assertNotIn("accessibility", data["market"][0])
        bw.validate(data)  # must not raise

    def test_opportunity_type_review_is_now_valid(self):
        # Section 3a supersedes the old "REVIEW is not an opportunity type"
        # rule for a scored business - confirm the schema-level enum allows it.
        data = load_sample()
        data["outreach"][0]["opportunity_type"] = "REVIEW"
        bw.validate(data)  # must not raise


class ValidateScoringFieldsTests(unittest.TestCase):
    def test_scored_fixture_validates(self):
        data = scored_fixture()
        bw.validate(data)  # must not raise

    def test_service_scope_without_value_fields_fails(self):
        data = scored_fixture()
        del data["outreach"][0]["commercial_fit"]
        with self.assertRaises(bw.ValidationError) as ctx:
            bw.validate(data)
        self.assertIn("commercial_fit", str(ctx.exception))

    def test_service_scope_without_derived_fields_fails(self):
        # Simulates forgetting to run scoring_engine.py before build_workbook.py.
        data = scored_fixture()
        del data["outreach"][0]["final_score"]
        with self.assertRaises(bw.ValidationError) as ctx:
            bw.validate(data)
        self.assertIn("final_score", str(ctx.exception))

    def test_service_scope_requires_run_level_definitions(self):
        data = scored_fixture()
        del data["run"]["service_scopes"]
        with self.assertRaises(bw.ValidationError) as ctx:
            bw.validate(data)
        self.assertIn("service_scopes", str(ctx.exception))

    def test_outreach_rank_on_non_ready_entry_fails(self):
        data = scored_fixture()
        data["outreach"][1]["ready_to_email"] = "REVIEW"
        data["outreach"][1]["outreach_rank"] = 1
        with self.assertRaises(bw.ValidationError) as ctx:
            bw.validate(data)
        self.assertIn("outreach_rank", str(ctx.exception))

    def test_non_consecutive_outreach_ranks_fail(self):
        data = scored_fixture()
        data["outreach"][0]["ready_to_email"] = "YES"
        data["outreach"][0]["outreach_rank"] = 2  # should be 1, the only ready entry
        with self.assertRaises(bw.ValidationError):
            bw.validate(data)


class RenderTests(unittest.TestCase):
    def test_workbook_builds_all_five_sheets(self):
        data = scored_fixture()
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "out.xlsx")
            n = bw.build_workbook(data, out)
            self.assertEqual(n, 1)  # Ready Co only
            self.assertTrue(os.path.exists(out))
            wb = load_workbook(out)
            self.assertEqual(set(wb.sheetnames), {"Methodology", "Scoring", "Shortlist", "Evidence", "QC"})

    def test_sample_campaign_still_renders_without_scoring(self):
        # A campaign with nothing scored (no service_scope anywhere) must
        # still render cleanly - Scoring/Shortlist are simply empty.
        data = load_sample()
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "out.xlsx")
            bw.validate(data)
            n = bw.build_workbook(data, out)
            self.assertEqual(n, 0)
            self.assertTrue(os.path.exists(out))

    def test_data_only_reopen_returns_populated_values(self):
        data = scored_fixture()
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "out.xlsx")
            bw.build_workbook(data, out)
            wb = load_workbook(out, data_only=True)
            ws = wb["Scoring"]
            headers = [c.value for c in ws[1]]
            idx = {h: i for i, h in enumerate(headers)}
            check_cols = ["Overall rank", "Final qualification score (0-100)",
                          "Relevance-normalized visibility %", "Opportunity type", "Business verified"]
            blanks = 0
            for row in ws.iter_rows(min_row=2, max_row=ws.max_row, values_only=True):
                if row[idx["Business"]] is None:
                    continue
                for col in check_cols:
                    if row[idx[col]] is None:
                        blanks += 1
            self.assertEqual(blanks, 0)

    def test_shortlist_contains_only_ready_business(self):
        data = scored_fixture()
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "out.xlsx")
            bw.build_workbook(data, out)
            wb = load_workbook(out)
            ws = wb["Shortlist"]
            businesses = [row[0].value for row in ws.iter_rows(min_row=2) if row[0].value]
            # column 0 is "Overall rank" not business - re-fetch by header
            headers = [c.value for c in ws[1]]
            biz_col = headers.index("Business")
            names = [row[biz_col].value for row in ws.iter_rows(min_row=2, max_row=ws.max_row) if row[biz_col].value]
            self.assertEqual(names, ["Ready Co"])

    def test_end_to_end_write_to_real_file(self):
        data = load_sample()
        bw.validate(data)
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "out.xlsx")
            bw.build_workbook(data, out)
            self.assertTrue(os.path.exists(out))
            self.assertGreater(os.path.getsize(out), 0)


if __name__ == "__main__":
    unittest.main()
