#!/usr/bin/env python3
"""
Regression tests for mention_count.py's alias generation and overlap-aware
matching. All fixture businesses are fictitious (tests/fixtures/) — no real
client/prospect name belongs in this repository (CLAUDE.md).

Covers two real defects found on real runs:
  1. Case-sensitive &/and alias generation silently missing a Title-Case
     brand's "&" form (confirmed against a real run: 5 recorded vs. 12
     actual mentions).
  2. Unsafe substring matching crediting a short business name's own
     appearance for text that only ever named a longer, unrelated business
     containing that substring (e.g. a "Builders Wirral" style collision) —
     fixed here with longest-match-wins overlap resolution rather than a
     permanent cross-census drop, since a permanent drop would itself
     undercount every answer where the short business is genuinely named
     on its own.

Run: python3 test_mention_count.py -v
"""
import json
import os
import unittest

import mention_count as mc

FIXTURES = os.path.join(os.path.dirname(__file__), "tests", "fixtures")
CENSUS_PATH = os.path.join(FIXTURES, "sample_census.csv")
RUN_PATH = os.path.join(FIXTURES, "sample_run.csv")
VARIANTS_PATH = os.path.join(FIXTURES, "sample_variants.json")


def run_fixture(manual_variants=None):
    census = mc.load_census(CENSUS_PATH, "business")
    run_rows = mc.load_run(RUN_PATH)
    mv = manual_variants or {}
    return mc.count_mentions(census, run_rows, "business", {"anytown"}, mv)


class VariantGenerationTests(unittest.TestCase):
    """Direct checks on variants() — the alias-generation step."""

    def test_and_ampersand_case_insensitive(self):
        # The real-run bug: a Title-Case "And" brand must still generate the
        # "&" form, not just re-emit the same string unchanged.
        vs = mc.variants("Meadow Kitchens And Bathrooms Limited", set())
        self.assertIn("Meadow Kitchens & Bathrooms Limited", vs)
        self.assertIn("Meadow Kitchens & Bathrooms", vs)  # Ltd-stripped too

    def test_ampersand_to_and_also_generated(self):
        vs = mc.variants("Fox & Sons Ltd", set())
        self.assertTrue(any("and" in v.lower() for v in vs))

    def test_ltd_and_limited_both_stripped(self):
        vs = mc.variants("Example Builders Limited", set())
        self.assertIn("Example Builders", vs)
        vs2 = mc.variants("Example Builders Ltd", set())
        self.assertIn("Example Builders", vs2)

    def test_stopword_floor_still_applies(self):
        # An area-name stopword must still be filtered out post-fix.
        vs = mc.variants("Anytown Homes", {"anytown"})
        self.assertNotIn("anytown", {v.lower() for v in vs})


class MatchingCaseAndPunctuationTests(unittest.TestCase):
    def test_matches_regardless_of_capitalization(self):
        results, _log = run_fixture()
        # q02/perplexity used "MEADOW kitchens and bathrooms" (different
        # case, lowercase "and") and must still match.
        matched_q02 = results["Meadow Kitchens And Bathrooms Limited"]["per_question"].get("q02", 0)
        self.assertGreaterEqual(matched_q02, 1)

    def test_markdown_bold_touching_the_name_still_matches(self):
        # q05/gemini: "Recommended: **Ridgeline Home Improvement**, based..."
        # - asterisks and a trailing comma immediately touch the name.
        results, _log = run_fixture()
        self.assertIn("q05", results["Ridgeline Home Improvement Ltd"]["per_question"])
        self.assertTrue(any(
            r["assistant"] == "gemini" for r in results["Ridgeline Home Improvement Ltd"]["matched_rows"]
        ))

    def test_possessive_apostrophe_does_not_block_match(self):
        # q05/perplexity: "Ridgeline Home Improvement's reviews are..."
        results, _log = run_fixture()
        self.assertTrue(any(
            r["assistant"] == "perplexity" for r in results["Ridgeline Home Improvement Ltd"]["matched_rows"]
        ))

    def test_short_alias_does_not_match_inside_unrelated_longer_word(self):
        # Direct check on the anchoring mechanism itself: a short alias must
        # not match as a bare mid-word substring of an unrelated word.
        pattern = mc.to_pattern("Ace")
        self.assertIsNone(pattern.search("Please replace the tiles before the surface cracks."))
        self.assertIsNone(pattern.search("The spacecraft launched on schedule."))
        self.assertIsNotNone(pattern.search("Ace Roofing did a great job on our extension."))
        self.assertIsNotNone(pattern.search("We used Ace for our roof last year."))


class PluralSingularAliasTests(unittest.TestCase):
    """The Apex-style regression: a census brand's singular final token must
    match a plural real-world mention, generated as an explicit, narrow
    alias rather than by loosening the match boundary."""

    def test_plural_final_token_generated_from_singular_brand(self):
        vs = mc.variants("Ridgeline Home Improvement Ltd", set())
        self.assertIn("Ridgeline Home Improvements", vs)

    def test_plural_brand_final_token_never_shortened(self):
        # One-directional by design: a brand already ending in "s" gets no
        # generated singular form at all - see
        # test_shortened_alias_does_not_misattribute_a_different_business
        # for the real defect this prevents.
        vs = mc.variants("Meadow Kitchens And Bathrooms", set())
        self.assertNotIn("Meadow Kitchens And Bathroom", vs)

    def test_short_final_token_not_pluralized(self):
        # "Ltd"/"LLP"-shaped short final tokens must never be pluralized.
        vs = mc.variants("Crestline Ltd", set())
        self.assertNotIn("Crestline Ltds", vs)

    def test_word_ending_in_s_generates_no_variant(self):
        forms = mc.pluralize_final_token("Northgate Glass")
        self.assertEqual(forms, set())

    def test_word_ending_in_ch_not_naively_pluralized(self):
        # Real English pluralizes "Church" as "Churches", not "Churchs" -
        # generating the wrong form is exactly what "narrow and auditable"
        # rules out, so this case is skipped entirely rather than guessed.
        forms = mc.pluralize_final_token("Riverside Church")
        self.assertEqual(forms, set())

    def test_plural_alias_reproduces_apex_style_regression(self):
        # End-to-end: the exact real-run shape (singular census brand,
        # plural real answer text), reproduced with a fictitious business.
        results, _log = run_fixture()
        r = results["Ridgeline Home Improvement Ltd"]
        self.assertEqual(r["openai"], 1)   # q05/openai: "...Improvements..."
        self.assertEqual(r["total"], 3)    # plural + bold-touching + possessive rows

    def test_shortened_alias_does_not_misattribute_a_different_business(self):
        # Reproduces the second real regression, fictionally: stripping
        # "Bathrooms" -> "Bathroom" from "Seaside Bathrooms Limited" (a real
        # run's shape, "Wirral Bathrooms Limited") generated an alias
        # generic enough to (a) match unrelated prose ("a seaside bathroom
        # specialist") and (b) prefix-match a completely different, distinct
        # business ("Seaside Bathroom Studio") that shares no connection to
        # it at all. Neither of q06's first two rows may be credited to
        # "Seaside Bathrooms Limited" - only its own, exact q06/perplexity
        # mention may.
        results, _log = run_fixture()
        r = results["Seaside Bathrooms Limited"]
        self.assertEqual(r["total"], 1)
        self.assertEqual(r["matched_rows"], [
            {"assistant": "perplexity", "question_id": "q06", "run_no": "3"}
        ])

    def test_unrelated_business_with_shared_prefix_is_not_in_census_at_all(self):
        # "Seaside Bathroom Studio" is deliberately NOT a census entry here
        # (mirroring the real run, where "Wirral Bathroom Company" was a
        # genuine competitor the census simply hadn't captured yet) - this
        # documents that its mention is correctly attributed to nobody,
        # rather than silently absorbed into a similarly-named business.
        results, _log = run_fixture()
        self.assertNotIn("Seaside Bathroom Studio", results)


class TimelessStyleUndercountRegressionTests(unittest.TestCase):
    """Reproduces the confirmed real-run defect with a fictitious business:
    an ampersand-form mention and a title-case 'And ... Limited' mention
    must both be counted, across different providers/questions."""

    def test_all_forms_counted(self):
        results, _log = run_fixture()
        r = results["Meadow Kitchens And Bathrooms Limited"]
        # openai q01 (&), gemini q01 (And ... Limited), perplexity q02 (case-varied)
        self.assertEqual(r["openai"], 1)
        self.assertEqual(r["gemini"], 1)
        self.assertEqual(r["perplexity"], 1)
        self.assertEqual(r["total"], 3)

    def test_errored_row_is_never_counted(self):
        results, _log = run_fixture()
        r = results["Meadow Kitchens And Bathrooms Limited"]
        # q04/perplexity carries an ampersand mention but errors="timeout" -
        # must not contribute.
        self.assertNotIn("q04", r["per_question"])


class OverlapSubstringCollisionTests(unittest.TestCase):
    """The Builders-Wirral-style collision, reproduced with fictitious
    census names: two longer businesses ('Harborview Builders Anytown',
    'Crestline Builders Anytown') both literally contain the shorter
    business name 'Builders Anytown'."""

    def test_nested_mention_credited_to_longer_business_only(self):
        results, _log = run_fixture()
        # q02/openai names only "Harborview Builders Anytown" - the short
        # "Builders Anytown" must NOT be credited for that row.
        self.assertIn("q02", results["Harborview Builders Anytown"]["per_question"])
        self.assertNotIn("q02", results["Builders Anytown"].get("per_question", {}))

    def test_second_longer_business_also_wins_its_own_nested_mention(self):
        results, _log = run_fixture()
        self.assertIn("q02", results["Crestline Builders Anytown"]["per_question"])

    def test_standalone_short_name_counts_normally(self):
        results, _log = run_fixture()
        # q03/perplexity names ONLY "Builders Anytown", with neither longer
        # business present in that row's text. (q03's count is 2, not 1,
        # because a second q03 row - openai/run2 - also names it
        # independently; see test_non_overlapping_mentions_of_both_are_both_counted.)
        self.assertIn("q03", results["Builders Anytown"]["per_question"])
        self.assertEqual(
            results["Builders Anytown"]["matched_rows"][0],
            {"assistant": "perplexity", "question_id": "q03", "run_no": "1"},
        )

    def test_non_overlapping_mentions_of_both_are_both_counted(self):
        results, _log = run_fixture()
        # q03/openai names "Harborview Builders Anytown" AND, separately and
        # non-overlapping later in the same answer, standalone
        # "Builders Anytown" - both must be credited for this row.
        self.assertIn(
            {"assistant": "openai", "question_id": "q03", "run_no": "2"},
            results["Harborview Builders Anytown"]["matched_rows"],
        )
        self.assertIn(
            {"assistant": "openai", "question_id": "q03", "run_no": "2"},
            results["Builders Anytown"]["matched_rows"],
        )

    def test_suppressed_overlap_is_logged_for_audit(self):
        results, overlap_log = run_fixture()
        # The nested "Builders Anytown" candidate inside q02/openai's
        # "Harborview Builders Anytown" text must appear in the audit log,
        # naming both the suppressed and winning business.
        matches = [
            e for e in overlap_log
            if e["question_id"] == "q02" and e["assistant"] == "openai"
            and e["suppressed_business"] == "Builders Anytown"
        ]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["winning_business"], "Harborview Builders Anytown")

    def test_short_business_total_excludes_nested_occurrences(self):
        results, _log = run_fixture()
        # Builders Anytown should be credited exactly twice overall: once
        # for its standalone q03/perplexity mention, once for its
        # non-overlapping q03/openai mention - never for the two nested
        # occurrences inside the two longer business names.
        self.assertEqual(results["Builders Anytown"]["total"], 2)


class ManualAliasTests(unittest.TestCase):
    """Genuine alias handling via --variants-file, and confirmation that a
    manual alias still goes through the same overlap-safety resolution as
    an auto-generated one (it is not exempt)."""

    def test_manual_alias_is_matched(self):
        manual = mc.load_manual_variants(VARIANTS_PATH)
        results, _log = run_fixture(manual_variants=manual)
        r = results["Silverline Design Studio"]
        self.assertEqual(r["total"], 1)
        self.assertIn("q04", r["per_question"])

    def test_manual_alias_absent_without_variants_file(self):
        results, _log = run_fixture(manual_variants={})
        self.assertEqual(results["Silverline Design Studio"]["total"], 0)

    def test_manual_alias_recorded_in_variants_used(self):
        manual = mc.load_manual_variants(VARIANTS_PATH)
        results, _log = run_fixture(manual_variants=manual)
        self.assertIn("SDS Home Renovations", results["Silverline Design Studio"]["variants_used"])


class OverlapResolutionUnitTests(unittest.TestCase):
    """Direct tests on resolve_overlaps(), independent of file I/O."""

    def test_longest_wins_when_spans_overlap(self):
        candidates = [
            (0, 27, "Harborview Builders Anytown", "Harborview Builders Anytown"),
            (11, 27, "Builders Anytown", "Builders Anytown"),
        ]
        accepted, suppressed = mc.resolve_overlaps(candidates)
        self.assertEqual(len(accepted), 1)
        self.assertEqual(accepted[0][2], "Harborview Builders Anytown")
        self.assertEqual(len(suppressed), 1)
        self.assertEqual(suppressed[0][0][2], "Builders Anytown")

    def test_non_overlapping_spans_both_accepted(self):
        candidates = [
            (0, 27, "Harborview Builders Anytown", "Harborview Builders Anytown"),
            (50, 66, "Builders Anytown", "Builders Anytown"),
        ]
        accepted, suppressed = mc.resolve_overlaps(candidates)
        self.assertEqual({c[2] for c in accepted}, {"Harborview Builders Anytown", "Builders Anytown"})
        self.assertEqual(suppressed, [])

    def test_deterministic_tie_break_on_equal_length_overlap(self):
        # Two different businesses' aliases of identical length at the same
        # position is a genuine census data collision - must resolve the
        # same way every run rather than depending on set/dict ordering.
        candidates = [
            (0, 10, "Zebra Co", "Zebra Co."),
            (0, 10, "Aardvark Co", "Aardvark C"),
        ]
        r1, _ = mc.resolve_overlaps(candidates)
        r2, _ = mc.resolve_overlaps(list(reversed(candidates)))
        self.assertEqual(r1[0][2], r2[0][2])


if __name__ == "__main__":
    unittest.main()
