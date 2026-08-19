#!/usr/bin/env python3
"""
Regression tests for benchmark_metrics.py and citation_analysis.py.

Every business, place and domain used here is invented — `tests/fixtures/` is
built by `tests/make_fixture.py` on the RFC 2606 `.example` TLD, because this
repository is written as though public and holds no real client or prospect
name (CLAUDE.md).

The tests that matter most are the ones covering things that would silently
produce a wrong number rather than an error:

  1. **The prompted/unprompted split.** A question whose own wording names
     the client is answered by an assistant that was handed the name. In the
     fixture that inflates the headline from 13.3% to 40% if it is not
     separated out. playbook/audit-process.md's own q08 template does exactly
     this, so it is not a hypothetical.
  2. **A band is only emitted at five runs.** Bands were defined against five
     runs and mean nothing stretched over another denominator.
  3. **A domain counts once per answer, not once per cited page**, or one
     answer citing six pages of a directory reads as six answers.
  4. **The competitor-only list requires a competitor to have been named.**
     A domain nobody was named alongside is a source, not a gap.

Run: python3 test_benchmark.py -v
"""
import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import benchmark_metrics as bm  # noqa: E402
import citation_analysis as ca  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, "tests", "fixtures")
RUN = os.path.join(FIXTURES, "run-sampleford-glazing.csv")
QUESTIONS = os.path.join(FIXTURES, "questions-sampleford-glazing.csv")
CENSUS = os.path.join(FIXTURES, "census-sampleford-glazing.csv")
MENTION_COUNT = os.path.join(HERE, "..", "mention-count", "mention_count.py")
CLIENT = "Sampleford Glazing Ltd"
AREA = "Sampleford"


def build_counts(tmpdir):
    """Run the real mention_count.py rather than hand-writing its output —
    these tests are meant to break if that tool's behaviour changes under
    them, which a hand-written fixture would hide."""
    out = os.path.join(tmpdir, "mention-counts.json")
    subprocess.run(
        [sys.executable, MENTION_COUNT, "--run", RUN, "--census", CENSUS,
         "--area", AREA, "--out", out],
        check=True, capture_output=True,
    )
    with open(out, encoding="utf-8") as fh:
        return {k: v for k, v in json.load(fh).items() if not k.startswith("_")}, out


class Shared(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.counts, cls.counts_path = build_counts(cls.tmp.name)
        with open(QUESTIONS, newline="", encoding="utf-8") as fh:
            cls.questions = list(csv.DictReader(fh))
        with open(RUN, newline="", encoding="utf-8") as fh:
            cls.run_rows = list(csv.DictReader(fh))
        high_intent = {q["question_id"] for q in cls.questions
                       if q["category"] in bm.DEFAULT_HIGH_INTENT_CATEGORIES}
        cls.baseline = bm.build(cls.run_rows, cls.questions, cls.counts, CLIENT, 5, high_intent)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()


class TestPromptedSplit(Shared):
    def test_comparison_and_named_business_are_prompted(self):
        prompted = {q["question_id"] for q in self.baseline["questions"] if q["prompted"]}
        # q05 names the client in its wording; q06 is the named-business category.
        self.assertEqual(prompted, {"q05", "q06"})

    def test_headline_excludes_prompted_questions(self):
        overall = self.baseline["client_visibility"]["overall"]
        self.assertEqual(overall["opportunities"], 60)      # 4 questions x 3 x 5
        self.assertEqual(overall["appearances"], 8)
        self.assertEqual(overall["rate_percent"], 13.3)

    def test_prompted_reported_separately_and_is_much_higher(self):
        prompted = self.baseline["client_visibility"]["prompted"]
        self.assertEqual(prompted["opportunities"], 30)
        self.assertEqual(prompted["appearances"], 28)
        # The whole point: folding these in would nearly triple the headline.
        self.assertGreater(prompted["rate_percent"],
                           self.baseline["client_visibility"]["overall"]["rate_percent"] * 3)

    def test_peer_table_uses_the_same_denominator(self):
        client_row = next(p for p in self.baseline["peers"] if p["is_client"])
        self.assertEqual(client_row["appearances"], 8)
        for peer in self.baseline["peers"]:
            self.assertLessEqual(peer["appearances"], 60)

    def test_legal_suffix_does_not_defeat_the_check(self):
        self.assertTrue(bm.question_names_client(
            "Who are the main alternatives to Sampleford Glazing?", "comparison", CLIENT))
        self.assertFalse(bm.question_names_client(
            "Who's a good double glazing company in Sampleford?", "discovery", CLIENT))

    def test_all_prompted_is_a_hard_stop(self):
        only_prompted = [q for q in self.questions if q["question_id"] in ("q05", "q06")]
        with self.assertRaises(SystemExit):
            bm.build(self.run_rows, only_prompted, self.counts, CLIENT, 5, set())


class TestBands(Shared):
    def test_bands_match_the_audit_process_definition(self):
        self.assertEqual(bm.band_for(0, 5), "Never appeared")
        self.assertEqual(bm.band_for(2, 5), "Occasionally")
        self.assertEqual(bm.band_for(4, 5), "Often")
        self.assertEqual(bm.band_for(5, 5), "Consistently")

    def test_no_band_at_any_other_run_count(self):
        self.assertIsNone(bm.band_for(2, 3))
        self.assertIsNone(bm.band_for(0, 10))

    def test_band_cells_cover_unprompted_questions_only(self):
        counts = self.baseline["client_visibility"]["overall"]["band_cell_counts"]
        self.assertEqual(sum(counts.values()), 12)          # 4 questions x 3 assistants


class TestPositionAndShape(Shared):
    def test_client_is_behind_a_clear_leader(self):
        pos = self.baseline["position"]
        self.assertEqual(pos["top_competitor"], "Northgate Windows Ltd")
        self.assertEqual(pos["visibility_shape"], "BEHIND")
        self.assertLess(pos["relative_position"], bm.DEFEND_MIN_RELATIVE_POSITION)

    def test_high_intent_gap_is_visible(self):
        v = self.baseline["client_visibility"]
        self.assertEqual(v["by_category"]["qualified-discovery"]["appearances"], 0)
        self.assertLess(v["high_intent"]["rate_percent"], v["overall"]["rate_percent"])

    def test_one_assistant_never_names_the_client(self):
        silent = [p for p, s in self.baseline["client_visibility"]["by_provider"].items()
                  if s["appearances"] == 0]
        self.assertEqual(silent, ["gemini"])

    def test_thresholds_come_from_the_scoring_engine(self):
        self.assertIn("scoring_engine.py", self.baseline["thresholds_used"]["source"])


class TestRunIntegrity(Shared):
    def test_complete_run(self):
        run = self.baseline["run"]
        self.assertTrue(run["complete"])
        self.assertEqual(run["successful_responses"], 90)
        self.assertEqual(run["errored_rows"], 0)

    def test_mixed_model_versions_are_flagged_not_averaged(self):
        rows = [dict(r) for r in self.run_rows]
        rows[0]["model_version"] = "gpt-something-else"
        _, integrity = bm.run_integrity(rows, self.questions, 5)
        self.assertEqual(integrity["providers_with_mixed_model_versions"], ["openai"])

    def test_errored_and_smoke_rows_are_excluded(self):
        rows = [dict(r) for r in self.run_rows]
        rows[0]["errors"] = "HTTP 500"
        rows[1]["notes"] = "smoke — delete this row"
        _, integrity = bm.run_integrity(rows, self.questions, 5)
        self.assertEqual(integrity["successful_responses"], 88)
        self.assertFalse(integrity["complete"])


class TestCitationAnalysis(Shared):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        named = ca.load_mention_counts(cls.counts_path)
        rows, _, _ = ca.load_run(RUN)
        cls.result = ca.analyse(rows, named, CLIENT, "sampleford-glazing.example")

    def test_domain_normalisation(self):
        self.assertEqual(ca.normalise_domain("https://WWW.Example.com/a/b"), "example.com")
        self.assertEqual(ca.normalise_domain("example.co.uk/page"), "example.co.uk")
        self.assertEqual(ca.normalise_domain("https://example.com:8443/x"), "example.com")
        self.assertIsNone(ca.normalise_domain(""))
        self.assertIsNone(ca.normalise_domain("   "))

    def test_subdomains_are_not_merged(self):
        # Deliberate: there is no Public Suffix List in the stdlib, so a guess
        # would be unverifiable. Keeping them separate is the honest default.
        self.assertNotEqual(ca.normalise_domain("https://blog.example.co.uk"),
                            ca.normalise_domain("https://example.co.uk"))

    def test_competitor_only_domains_are_the_actionable_list(self):
        gaps = {d["domain"] for d in self.result["competitor_cited_client_absent"]}
        # sashwindow-guide is cited on every answer to the sash-window question,
        # which the client never appears on. That is the finding.
        self.assertIn("sashwindow-guide.example", gaps)
        self.assertNotIn("sampleford-glazing.example", gaps)

    def test_a_domain_with_no_competitor_named_is_not_a_gap(self):
        for d in self.result["competitor_cited_client_absent"]:
            self.assertGreater(d["answers_naming_a_competitor_that_cite_it"], 0)
            self.assertEqual(d["answers_naming_client_that_cite_it"], 0)

    def test_client_own_domain_is_separated_and_never_a_gap(self):
        self.assertTrue(self.result["client_own_domain_cited"])
        self.assertEqual(self.result["client_own_domain_questions"], ["q06"])

    def test_one_answer_citing_several_pages_of_a_domain_counts_once(self):
        rows = [{
            "assistant": "openai", "question_id": "q01", "run_no": "1", "errors": "", "notes": "",
            "sources_cited": "https://d.example/a;https://d.example/b;https://d.example/c",
        }]
        named = {CLIENT: {("openai", "q01", "1")}}
        result = ca.analyse(rows, named, CLIENT, None)
        row = result["domains"][0]
        self.assertEqual(row["citations"], 3)
        self.assertEqual(row["answers_naming_client_that_cite_it"], 1)

    def test_client_missing_from_the_census_is_a_hard_stop(self):
        rows, _, _ = ca.load_run(RUN)
        with self.assertRaises(SystemExit):
            ca.analyse(rows, {"Someone Else Ltd": set()}, CLIENT, None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
