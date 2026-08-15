#!/usr/bin/env python3
"""
Regression tests for build_workbook.py's validate() and rendering logic,
focused on the decision-maker accessibility fields (accessibility,
decision_maker_linkedin, accessibility_notes). Stdlib unittest only, no
dependency beyond openpyxl (already required by build_workbook.py itself).

Run: python3 test_build_workbook.py -v
"""
import copy
import json
import os
import tempfile
import unittest

import build_workbook as bw

SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "sample", "sample-campaign.json")


def load_sample():
    with open(SAMPLE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class ValidateAccessibilityTests(unittest.TestCase):
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
        with self.assertRaises(bw.ValidationError) as ctx:
            bw.validate(data)
        self.assertIn("accessibility", str(ctx.exception))

    def test_every_accessibility_value_is_individually_valid(self):
        for value in sorted(bw.ACCESSIBILITY_VALUES):
            data = load_sample()
            data["outreach"][0]["accessibility"] = value
            bw.validate(data)  # must not raise for any real enum value

    def test_market_entry_accessibility_is_optional(self):
        data = load_sample()
        # None of the sample's other market entries set accessibility -
        # confirms validate() doesn't silently require it there.
        self.assertNotIn("accessibility", data["market"][0])
        bw.validate(data)  # must not raise

    def test_market_entry_bad_accessibility_value_fails(self):
        data = load_sample()
        data["market"][0]["accessibility"] = "NOT_A_REAL_VALUE"
        with self.assertRaises(bw.ValidationError) as ctx:
            bw.validate(data)
        self.assertIn("accessibility", str(ctx.exception))

    def test_decision_maker_linkedin_and_notes_are_optional(self):
        data = load_sample()
        entry = data["outreach"][1]
        self.assertIn("decision_maker_linkedin", entry)  # present in the sample...
        del entry["decision_maker_linkedin"]
        del entry["accessibility_notes"]
        bw.validate(data)  # ...but validate() must not require either


class RenderAccessibilityTests(unittest.TestCase):
    def test_workbook_builds_and_colors_accessibility_column(self):
        data = load_sample()
        wb = bw.build_workbook(data)
        ws = wb["OUTREACH"]
        headers = [c.value for c in ws[1]]
        self.assertIn("Decision-maker accessibility", headers)
        self.assertIn("Decision-maker LinkedIn", headers)
        self.assertIn("Accessibility notes", headers)
        col = headers.index("Decision-maker accessibility") + 1
        seen_fills = set()
        for r in range(2, ws.max_row + 1):
            cell = ws.cell(row=r, column=col)
            self.assertTrue(cell.fill and cell.fill.fill_type == "solid",
                             f"row {r} accessibility cell has no fill")
            seen_fills.add(cell.value)
        # both sample outreach entries carry a real, distinct accessibility value
        self.assertEqual(seen_fills, {"GATEKEPT", "DIRECT"})

    def test_priority_sort_is_never_reordered_by_accessibility(self):
        # A GATEKEPT priority-A prospect must still sort ahead of a DIRECT
        # priority-B one - accessibility is a tiebreaker within a priority
        # band only, never a promotion across bands.
        rows = [
            {"priority": "B", "accessibility": "DIRECT", "business": "B-direct"},
            {"priority": "A", "accessibility": "GATEKEPT", "business": "A-gatekept"},
            {"priority": "A", "accessibility": "DIRECT", "business": "A-direct"},
        ]
        ordered = [rows[i]["business"] for i in bw.priority_sort_key(rows)]
        self.assertEqual(ordered, ["A-direct", "A-gatekept", "B-direct"])

    def test_end_to_end_write_to_real_file(self):
        data = load_sample()
        bw.validate(data)
        wb = bw.build_workbook(data)
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "out.xlsx")
            wb.save(out)
            self.assertTrue(os.path.exists(out))
            self.assertGreater(os.path.getsize(out), 0)


if __name__ == "__main__":
    unittest.main()
