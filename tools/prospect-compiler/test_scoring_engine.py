#!/usr/bin/env python3
"""
Regression tests for scoring_engine.py. One shared fixture campaign covers
the 9 named regression scenarios from the Kitchen and Bathroom Design &
Installation, Wirral v2.1 generalization: a combined-service market leader,
a specialist absent from an irrelevant question, a weak-field group leader
that must remain GROWTH, a credible-but-nearly-invisible GAP prospect, a
high-scoring candidate withheld for incomplete evidence, a confirmed owner
reached through a generic inbox, an inferred contact that must remain
PROBABLE/POSSIBLE, a locally owned franchise, and a centrally controlled
chain. No business names, sectors, or question text here are drawn from a
real campaign - this is a fictitious fixture, same convention as
sample-campaign.json.

Run: python3 test_scoring_engine.py -v
"""
import copy
import unittest

import scoring_engine as se


def base_outreach_entry(business, **overrides):
    entry = {
        "priority": "REVIEW", "business": business, "area": "Sampleford",
        "strongest_competitor": "x", "competitor_appearances": 0,
        "competitive_gap_finding": "x", "why_prospect": "x",
        "legal_entity": "x", "company_number": "1", "company_status": "Active",
        "ready_to_email": "REVIEW", "evidence_source_ids": ["S001"], "accessibility": "REVIEW",
        "total_ai_appearances": 0,
        "commercial_fit": 4, "service_relevance": 4, "business_credibility": 4, "ability_to_buy": 3,
        "decision_maker_identified": 4, "direct_dm_route": 4, "contact_route_quality": 4,
        "contact_identity_confidence": 4, "research_completeness": 5,
        "question_appearances": {},
    }
    entry.update(overrides)
    return entry


def make_fixture():
    run = {
        "sector": "fictitious trade", "geography": "Sampleford", "campaign_slug": "fixture", "date": "2026-08-16",
        "questions": [
            {"question_id": "q01", "text": "best A and B providers (inclusive)"},
            {"question_id": "q02", "text": "B-only question"},
            {"question_id": "q03", "text": "A-only question"},
            {"question_id": "q04", "text": "handles both A and B, not just one trade"},
        ],
        "providers": [{"provider": "openai", "model": "x"}],
        "responses_per_question": 15,
        "service_scopes": [
            {"label": "a_only", "applicable_services": ["A"], "structure": "INDEPENDENT_LOCAL"},
            {"label": "b_only", "applicable_services": ["B"], "structure": "INDEPENDENT_LOCAL"},
            {"label": "combined", "applicable_services": ["A", "B"], "structure": "INDEPENDENT_LOCAL"},
            {"label": "franchise_local", "applicable_services": ["A"], "structure": "LOCALLY_OWNED_FRANCHISE"},
            {"label": "chain_central", "applicable_services": ["A"], "structure": "CENTRALLY_CONTROLLED_CHAIN"},
        ],
        "question_relevance": [
            {"question_id": "q01", "type": "SINGLE_SERVICE_INCLUSIVE", "rationale": "inclusive ask"},
            {"question_id": "q02", "type": "SERVICE_ONLY", "service": "B", "rationale": "b only"},
            {"question_id": "q03", "type": "SERVICE_ONLY", "service": "A", "rationale": "a only"},
            {"question_id": "q04", "type": "EXPLICITLY_COMBINED", "rationale": "combined only"},
        ],
    }
    outreach = [
        # 1. Combined-service market leader - real peer, high absolute visibility, DEFEND expected.
        base_outreach_entry("Combined Leader", service_scope="combined",
                             question_appearances={"q01": 10, "q02": 8, "q03": 8, "q04": 12},
                             business_credibility=5),
        # peer for Combined Leader, weaker - so Combined Leader has someone to lead against
        base_outreach_entry("Combined Runner-up", service_scope="combined",
                             question_appearances={"q01": 3, "q02": 2, "q03": 2, "q04": 3},
                             business_credibility=4),
        # 2. Specialist absent from an irrelevant question (b_only absent from q03, an A-only question) -
        # must not be penalized: q03 weight is 0 for b_only, so absence there doesn't touch its denominator.
        base_outreach_entry("Bathroom Specialist", service_scope="b_only",
                             question_appearances={"q01": 8, "q02": 10, "q03": 0, "q04": 0},
                             business_credibility=5),
        # peer for b_only group
        base_outreach_entry("Bathroom Specialist Peer", service_scope="b_only",
                             question_appearances={"q01": 2, "q02": 3, "q03": 0, "q04": 0},
                             business_credibility=3),
        # 3. Weak-field group leader - leads a_only group (relative_position=1.0) but visibility_score=2
        # (mid-band, not <=1 so it dodges GAP, not >=3 so it dodges DEFEND) - must land GROWTH either way.
        base_outreach_entry("Weak Field Leader", service_scope="a_only",
                             question_appearances={"q01": 2, "q02": 0, "q03": 2, "q04": 0},
                             business_credibility=3),
        base_outreach_entry("Weak Field Runner-up", service_scope="a_only",
                             question_appearances={"q01": 0, "q02": 0, "q03": 0, "q04": 0},
                             business_credibility=2),
        # 4. Credible but nearly invisible GAP prospect.
        base_outreach_entry("Invisible But Credible", service_scope="combined",
                             question_appearances={"q01": 0, "q02": 0, "q03": 0, "q04": 0},
                             business_credibility=5),
        # 5. High-scoring candidate withheld for incomplete evidence (research_completeness < 4).
        base_outreach_entry("Incomplete Evidence Star", service_scope="combined",
                             question_appearances={"q01": 9, "q02": 9, "q03": 9, "q04": 9},
                             business_credibility=5, commercial_fit=5, ability_to_buy=5,
                             decision_maker_identified=5, direct_dm_route=5, contact_route_quality=5,
                             contact_identity_confidence=5, research_completeness=3),
        # 6. Confirmed owner reached through a generic inbox (direct_dm_route=4, not 5).
        base_outreach_entry("Generic Inbox Confirmed Owner", service_scope="a_only",
                             question_appearances={"q01": 1, "q03": 1},
                             decision_maker_identified=5, direct_dm_route=4, contact_identity_confidence=4,
                             research_completeness=5, business_credibility=4),
        # 7. Inferred contact that must remain PROBABLE/POSSIBLE, never CONFIRMED.
        base_outreach_entry("Inferred Contact Only", service_scope="a_only",
                             question_appearances={"q01": 1, "q03": 1},
                             decision_maker_identified=2, contact_identity_confidence=2,
                             direct_dm_route=2, research_completeness=3),
        # 8. Locally owned franchise - real commercial_fit, should be able to reach eligible.
        base_outreach_entry("Local Franchise", service_scope="franchise_local",
                             question_appearances={"q01": 2, "q03": 2},
                             commercial_fit=3, business_structure="LOCALLY_OWNED_FRANCHISE",
                             business_credibility=4, contact_route_quality=4, direct_dm_route=4,
                             decision_maker_identified=4, contact_identity_confidence=4, research_completeness=5),
        # 9. Centrally controlled chain - low commercial_fit must block eligible_for_outreach regardless of score.
        base_outreach_entry("Central Chain", service_scope="chain_central",
                             question_appearances={"q01": 5, "q03": 5},
                             commercial_fit=0, business_structure="CENTRALLY_CONTROLLED_CHAIN",
                             business_credibility=5, contact_route_quality=5, direct_dm_route=5,
                             decision_maker_identified=5, contact_identity_confidence=5, research_completeness=5),
    ]
    sources = [{"source_id": "S001", "business": "x", "publisher": "x", "fact_supported": "x", "url": "x", "access_date": "2026-08-16"}]
    return {"run": run, "market": [], "outreach": outreach, "excluded": [], "sources": sources}


def scored():
    data = make_fixture()
    se.run_engine(data)
    return {e["business"]: e for e in data["outreach"]}


class RelevanceWeightTests(unittest.TestCase):
    def test_service_only_excludes_non_matching_scope(self):
        rel = {"question_id": "q02", "type": "SERVICE_ONLY", "service": "B"}
        self.assertEqual(se.question_weight_for_business(rel, {"A"}), 0.0)
        self.assertEqual(se.question_weight_for_business(rel, {"B"}), 1.0)

    def test_explicitly_combined_requires_multi_service(self):
        rel = {"question_id": "q04", "type": "EXPLICITLY_COMBINED"}
        self.assertEqual(se.question_weight_for_business(rel, {"A"}), 0.0)
        self.assertEqual(se.question_weight_for_business(rel, {"A", "B"}), 1.0)

    def test_single_service_inclusive_is_full_weight_for_any_real_scope(self):
        rel = {"question_id": "q01", "type": "SINGLE_SERVICE_INCLUSIVE"}
        self.assertEqual(se.question_weight_for_business(rel, {"A"}), 1.0)
        self.assertEqual(se.question_weight_for_business(rel, {"B"}), 1.0)
        self.assertEqual(se.question_weight_for_business(rel, set()), 0.0)

    def test_ambiguous_uses_explicit_weight_never_defaults_to_full(self):
        rel = {"question_id": "q05", "type": "AMBIGUOUS", "weight": 0.5}
        self.assertEqual(se.question_weight_for_business(rel, {"A"}), 0.5)

    def test_missing_ambiguous_weight_raises(self):
        run = make_fixture()["run"]
        run["question_relevance"].append({"question_id": "q99", "type": "AMBIGUOUS", "rationale": "x"})
        run["questions"].append({"question_id": "q99", "text": "x"})
        with self.assertRaises(se.ScoringError):
            se.build_relevance_index(run)

    def test_missing_question_relevance_entry_raises(self):
        run = make_fixture()["run"]
        run["questions"].append({"question_id": "q99", "text": "x"})
        with self.assertRaises(se.ScoringError):
            se.build_relevance_index(run)


class PeerGroupSizeBugRegressionTests(unittest.TestCase):
    """Dedicated regression test for a real bug caught during development:
    the peer-count loop in score_pool() computed group_size correctly, but
    a SECOND loop re-read a stale `label` variable left over from the LAST
    iteration of the FIRST loop instead of each entry's own service_scope -
    so every business's _has_comparable_peer check was silently evaluated
    against whichever scope happened to be processed last, not its own.
    This fixture is shaped specifically to catch that class of bug: scopes
    are given deliberately different group sizes, and the scope most likely
    to be iterated last (alphabetically/insertion-order last) has size 1 -
    if the stale-variable bug ever returns, every business in a >=2-member
    group would wrongly see group_size=1 and never reach DEFEND."""

    def test_business_in_large_group_not_contaminated_by_smaller_last_group(self):
        run = {
            "sector": "x", "geography": "x", "campaign_slug": "x", "date": "2026-08-16",
            "questions": [{"question_id": "q01", "text": "inclusive question"}],
            "providers": [{"provider": "openai", "model": "x"}],
            "responses_per_question": 15,
            "service_scopes": [
                {"label": "big_group", "applicable_services": ["A"]},
                {"label": "zzz_solo_group", "applicable_services": ["A"]},  # sorts/inserts last
            ],
            "question_relevance": [{"question_id": "q01", "type": "SINGLE_SERVICE_INCLUSIVE", "rationale": "x"}],
        }
        outreach = [
            base_outreach_entry("Big Group Member A", service_scope="big_group",
                                 question_appearances={"q01": 10}, business_credibility=5),
            base_outreach_entry("Big Group Member B", service_scope="big_group",
                                 question_appearances={"q01": 9}, business_credibility=5),
            base_outreach_entry("Big Group Member C", service_scope="big_group",
                                 question_appearances={"q01": 9}, business_credibility=5),
            # Deliberately the LAST entry, so its scope is the last one touched
            # by the first (group-counting) loop - this is exactly the
            # condition that exposed the stale-variable bug.
            base_outreach_entry("Solo Group Member", service_scope="zzz_solo_group",
                                 question_appearances={"q01": 10}, business_credibility=5),
        ]
        data = {"run": run, "market": [], "outreach": outreach, "excluded": [],
                "sources": [{"source_id": "S001", "business": "x", "publisher": "x", "fact_supported": "x",
                             "url": "x", "access_date": "2026-08-16"}]}
        se.run_engine(data)
        by_name = {e["business"]: e for e in data["outreach"]}
        # The big_group leader has a real peer (3 members) and should reach
        # DEFEND. Under the bug, it would incorrectly inherit
        # zzz_solo_group's group_size=1 and be blocked from DEFEND entirely.
        self.assertEqual(by_name["Big Group Member A"]["opportunity_type"], "DEFEND")
        # The solo group member has NO real peer and must never reach DEFEND,
        # regardless of its own visibility.
        self.assertNotEqual(by_name["Solo Group Member"]["opportunity_type"], "DEFEND")


class FixtureScenarioTests(unittest.TestCase):
    def setUp(self):
        self.s = scored()

    def test_1_combined_service_market_leader_is_defend(self):
        self.assertEqual(self.s["Combined Leader"]["opportunity_type"], "DEFEND")
        self.assertGreaterEqual(self.s["Combined Leader"]["visibility_score"], 3)
        self.assertGreaterEqual(self.s["Combined Leader"]["relative_position"], 0.85)

    def test_2_specialist_not_penalized_for_irrelevant_question(self):
        e = self.s["Bathroom Specialist"]
        # q03 is A-only (SERVICE_ONLY, service=A) - irrelevant to a b_only business.
        # relevant_opportunities must reflect only q01+q02 (2 questions), not all 4.
        self.assertEqual(e["relevant_opportunities"], 2 * 15)
        # full marks on both its actually-relevant questions -> 100% coverage despite 0 on q03/q04
        self.assertEqual(e["question_coverage"], 1.0)

    def test_3_weak_field_leader_stays_growth_not_defend(self):
        e = self.s["Weak Field Leader"]
        self.assertEqual(e["opportunity_type"], "GROWTH")
        self.assertLess(e["visibility_score"], 3)  # fails the absolute floor even though it leads its group
        self.assertGreater(e["visibility_score"], 1)  # and isn't near-zero either, so GAP's floor doesn't apply
        self.assertEqual(e["relative_position"], 1.0)  # confirms it WOULD look like a leader by relative measure alone

    def test_4_credible_but_invisible_is_gap(self):
        e = self.s["Invisible But Credible"]
        self.assertEqual(e["opportunity_type"], "GAP")
        self.assertEqual(e["visibility_score"], 0)
        self.assertGreaterEqual(e["business_credibility"], 3)

    def test_5_high_score_withheld_for_incomplete_evidence(self):
        e = self.s["Incomplete Evidence Star"]
        self.assertGreaterEqual(e["final_score"], 70)  # genuinely a high scorer
        self.assertEqual(e["research_complete"], "NO")
        self.assertEqual(e["ready_to_email"], "REVIEW")
        self.assertNotIn("outreach_rank", e)  # never ranked for outreach despite the high score

    def test_6_confirmed_owner_generic_inbox_gets_correct_grade(self):
        e = self.s["Generic Inbox Confirmed Owner"]
        self.assertEqual(e["accessibility_grade"], "CONFIRMED_GENERIC_ROUTE")
        self.assertNotEqual(e["accessibility_grade"], "CONFIRMED_DIRECT")

    def test_7_inferred_contact_never_confirmed(self):
        e = self.s["Inferred Contact Only"]
        self.assertIn(e["identity_confidence"], ("PROBABLE", "POSSIBLE"))
        self.assertNotEqual(e["identity_confidence"], "CONFIRMED")

    def test_8_locally_owned_franchise_can_be_eligible(self):
        e = self.s["Local Franchise"]
        self.assertEqual(e["business_structure"], "LOCALLY_OWNED_FRANCHISE")
        self.assertEqual(e["eligible_for_outreach"], "YES")

    def test_9_centrally_controlled_chain_blocked_by_commercial_fit(self):
        e = self.s["Central Chain"]
        self.assertEqual(e["business_structure"], "CENTRALLY_CONTROLLED_CHAIN")
        self.assertEqual(e["eligible_for_outreach"], "REVIEW")  # commercial_fit=0 blocks it regardless of score
        self.assertEqual(e["ready_to_email"], "REVIEW")


class QCChecklistTests(unittest.TestCase):
    def setUp(self):
        self.s = scored()

    def test_overall_rank_covers_complete_pool_no_gaps(self):
        ranks = sorted(e["overall_rank"] for e in self.s.values())
        self.assertEqual(ranks, list(range(1, len(self.s) + 1)))

    def test_outreach_rank_consecutive_and_ready_only(self):
        ready = [e for e in self.s.values() if e.get("ready_to_email") == "YES"]
        ranks = sorted(e["outreach_rank"] for e in ready)
        self.assertEqual(ranks, list(range(1, len(ready) + 1)))
        for e in self.s.values():
            if e.get("ready_to_email") != "YES":
                self.assertNotIn("outreach_rank", e)

    def test_final_score_reproduces_from_components(self):
        for e in self.s.values():
            raw = (e["commercial_fit"] * 3 + e["service_relevance"] * 2 + e["visibility_score"] * 2
                   + e["gap_strength"] * 4 + e["business_credibility"] * 3 + e["ability_to_buy"] * 2
                   + e["decision_maker_identified"] * 2 + e["direct_dm_route"] * 3 + e["contact_route_quality"])
            expected = round(raw / se.FINAL_SCORE_MAX_RAW * 100, 1)
            self.assertAlmostEqual(e["final_score"], expected, places=6)

    def test_gap_requires_credibility(self):
        for e in self.s.values():
            if e["opportunity_type"] == "GAP":
                self.assertGreaterEqual(e["business_credibility"], 3)

    def test_defend_requires_absolute_and_relative_evidence(self):
        for e in self.s.values():
            if e["opportunity_type"] == "DEFEND":
                self.assertGreaterEqual(e["visibility_score"], 3)
                self.assertGreaterEqual(e["relative_position"], 0.85)

    def test_defend_never_from_a_group_of_one(self):
        # No business in this fixture is alone in its scope except via a
        # dedicated check: force one and confirm it cannot reach DEFEND.
        data = make_fixture()
        data["outreach"] = [base_outreach_entry(
            "Lone Scope Business", service_scope="combined",
            question_appearances={"q01": 10, "q02": 10, "q03": 10, "q04": 10}, business_credibility=5,
        )]
        se.run_engine(data)
        self.assertNotEqual(data["outreach"][0]["opportunity_type"], "DEFEND")


# ===========================================================================
# Mandatory narrative generation (competitive_gap_finding / why_prospect)
# ===========================================================================
# Fictitious fixture reproducing the real defect found on the Kitchen and
# Bathroom Design & Installation, Wirral campaign: "A J Kitchen Installations"
# had relevant_appearances=13, relevant_opportunities=60 (a kitchen-only
# specialist relevant to 4 of the campaign's 6 questions), but its hand-typed
# competitive_gap_finding said "13 of the 90 raw answers" - the raw total,
# not its own relevance-aware denominator. This fixture's 6-question,
# 15-responses-per-question shape (raw total 90) reproduces the same
# 60/45/90 denominator split real campaigns of this kind actually produce:
# a kitchen-style specialist relevant to 4 questions (60), a bathroom-style
# specialist relevant to 3 (45), and a combined provider relevant to all 6
# (90) - none of it copied from the real business, sector, or numbers.

def narrative_fixture():
    run = {
        "sector": "fictitious trade", "geography": "Sampleford", "campaign_slug": "narrative-fixture",
        "date": "2026-08-16",
        "questions": [
            {"question_id": f"q{i:02d}", "text": f"question {i}"} for i in range(1, 7)
        ],
        "providers": [{"provider": "openai", "model": "x"}],
        "responses_per_question": 15,
        "service_scopes": [
            {"label": "kitchen_only", "applicable_services": ["kitchen"], "structure": "INDEPENDENT_LOCAL"},
            {"label": "bathroom_only", "applicable_services": ["bathroom"], "structure": "INDEPENDENT_LOCAL"},
            {"label": "combined", "applicable_services": ["kitchen", "bathroom"], "structure": "INDEPENDENT_LOCAL"},
        ],
        "question_relevance": [
            {"question_id": "q01", "type": "SINGLE_SERVICE_INCLUSIVE", "rationale": "inclusive kitchen+bathroom ask"},
            {"question_id": "q02", "type": "SERVICE_ONLY", "service": "kitchen", "rationale": "kitchen only"},
            {"question_id": "q03", "type": "SERVICE_ONLY", "service": "kitchen", "rationale": "kitchen only"},
            {"question_id": "q04", "type": "SERVICE_ONLY", "service": "kitchen", "rationale": "kitchen only"},
            {"question_id": "q05", "type": "SERVICE_ONLY", "service": "bathroom", "rationale": "bathroom only"},
            {"question_id": "q06", "type": "SERVICE_ONLY", "service": "bathroom", "rationale": "bathroom only"},
        ],
    }
    # kitchen_only: relevant to q01-q04 (4 questions x 15 = 60)
    # bathroom_only: relevant to q01, q05, q06 (3 questions x 15 = 45)
    # combined: relevant to every question (6 x 15 = 90) - offers both services,
    #           so it gets full weight on every SERVICE_ONLY question too.
    outreach = [
        base_outreach_entry("Fixture Kitchen Co", service_scope="kitchen_only",
                             question_appearances={"q01": 4, "q02": 3, "q03": 3, "q04": 3},
                             business_credibility=4),
        base_outreach_entry("Fixture Kitchen Leader", service_scope="kitchen_only",
                             question_appearances={"q01": 10, "q02": 10, "q03": 10, "q04": 10},
                             business_credibility=4),
        base_outreach_entry("Fixture Bathroom Co", service_scope="bathroom_only",
                             question_appearances={"q01": 1, "q05": 0, "q06": 0},
                             business_credibility=5),
        base_outreach_entry("Fixture Bathroom Peer", service_scope="bathroom_only",
                             question_appearances={"q01": 10, "q05": 10, "q06": 10},
                             business_credibility=4),
        base_outreach_entry("Fixture Combined Co", service_scope="combined",
                             question_appearances={"q01": 10, "q02": 10, "q03": 10, "q04": 10, "q05": 10, "q06": 10},
                             business_credibility=5),
        base_outreach_entry("Fixture Combined Peer", service_scope="combined",
                             question_appearances={"q01": 3, "q02": 3, "q03": 3, "q04": 3, "q05": 3, "q06": 3},
                             business_credibility=4),
    ]
    sources = [{"source_id": "S001", "business": "x", "publisher": "x", "fact_supported": "x", "url": "x", "access_date": "2026-08-16"}]
    return {"run": run, "market": [], "outreach": outreach, "excluded": [], "sources": sources}


def narrative_scored():
    data = narrative_fixture()
    se.run_engine(data)
    return {e["business"]: e for e in data["outreach"]}


class NarrativeDenominatorTests(unittest.TestCase):
    """The core defect this whole change exists to prevent: a specialist's
    primary visibility claim must use its own relevant denominator, never
    the raw campaign total, unless the two genuinely coincide."""

    def test_kitchen_style_specialist_uses_60_never_90(self):
        e = narrative_scored()["Fixture Kitchen Co"]
        self.assertEqual(e["relevant_appearances"], 13)
        self.assertEqual(e["relevant_opportunities"], 60)
        self.assertIn("13 of 60", e["competitive_gap_finding"])
        self.assertNotIn("13 of 90", e["competitive_gap_finding"])
        self.assertNotIn("of the 90", e["competitive_gap_finding"])

    def test_bathroom_style_specialist_uses_45_denominator(self):
        e = narrative_scored()["Fixture Bathroom Co"]
        self.assertEqual(e["relevant_opportunities"], 45)
        # Primary claim uses 45. The raw 90-answer campaign total may still
        # appear as a clearly separate, distinctly-worded clause (requirement
        # 6: preserve raw counts for auditability) - it must just never be
        # the PRIMARY claim's own denominator for a scoped specialist.
        self.assertIn("1 of 45", e["competitive_gap_finding"])
        self.assertNotIn("1 of 90", e["competitive_gap_finding"])
        self.assertNotIn("1 of the 90", e["competitive_gap_finding"])

    def test_combined_provider_90_denominator_is_labelled_not_ambiguous(self):
        e = narrative_scored()["Fixture Combined Co"]
        self.assertEqual(e["relevant_opportunities"], 90)
        self.assertIn("of 90", e["competitive_gap_finding"])
        # Requirement: when raw and relevant totals coincide, label the
        # measure accurately rather than silently reusing ambiguous "90"
        # language indistinguishable from the legacy raw-count bug.
        self.assertIn("every one of this campaign's questions was relevant", e["competitive_gap_finding"])


class OpportunityRationaleTests(unittest.TestCase):
    """why_prospect must explain the actual opportunity type, not merely
    restate service_scope/business_type_notes."""

    def test_defend_rationale(self):
        e = narrative_scored()["Fixture Combined Co"]
        self.assertEqual(e["opportunity_type"], "DEFEND")
        self.assertIn("strongest AI-recommendation positions", e["why_prospect"])

    def test_growth_rationale(self):
        e = narrative_scored()["Fixture Kitchen Co"]
        self.assertEqual(e["opportunity_type"], "GROWTH")
        self.assertIn("room to strengthen", e["why_prospect"])

    def test_gap_rationale(self):
        e = narrative_scored()["Fixture Bathroom Co"]
        self.assertEqual(e["opportunity_type"], "GAP")
        self.assertIn("actionable gap", e["why_prospect"])

    def test_why_prospect_is_never_just_business_type_notes(self):
        data = narrative_fixture()
        for o in data["outreach"]:
            o["business_type_notes"] = "Kitchen specialist (design/supply/install); independently owned"
        se.run_engine(data)
        for o in data["outreach"]:
            self.assertNotEqual(o["why_prospect"].strip(), o["business_type_notes"].strip())


class NarrativeSignatureRegenerationTests(unittest.TestCase):
    """Requirement 7: correcting a mention count and rescoring must
    automatically change the narrative - never left stale merely because
    the field was already non-empty. Reproduces the Timeless-style
    undercount-then-fix shape with a fictitious business."""

    def test_rescoring_after_a_corrected_mention_count_regenerates_narrative(self):
        data = narrative_fixture()
        target = next(o for o in data["outreach"] if o["business"] == "Fixture Bathroom Co")
        target["question_appearances"] = {"q01": 1, "q05": 1, "q06": 0}  # understated, like "5" before the fix
        se.run_engine(data)
        first_finding = target["competitive_gap_finding"]
        first_signature = target["narrative_generated_from"]
        first_appearances = target["relevant_appearances"]

        # Simulate the mention-count correction (5 -> 12 shape): more real
        # appearances discovered, then scoring_engine.py is rerun exactly as
        # /qualify's own Stage 11 would do after any re-score.
        target["question_appearances"] = {"q01": 3, "q05": 3, "q06": 3}
        se.run_engine(data)

        self.assertNotEqual(target["relevant_appearances"], first_appearances)
        self.assertNotEqual(target["narrative_generated_from"], first_signature)
        self.assertNotEqual(target["competitive_gap_finding"], first_finding)
        self.assertIn(f"{se._fmt_num(target['relevant_appearances'])} of 45", target["competitive_gap_finding"])

    def test_untouched_entry_narrative_is_not_regenerated_unnecessarily(self):
        # A signature match means "already current" - re-running the engine
        # with nothing changed must not churn the text (e.g. if a human had
        # refined it by hand on top of the generated baseline, that
        # refinement must survive an unrelated rescore).
        data = narrative_fixture()
        se.run_engine(data)
        entry = next(o for o in data["outreach"] if o["business"] == "Fixture Kitchen Co")
        entry["why_prospect"] += " Hand-added detail from a real competitor comparison."
        stamped_signature = entry["narrative_generated_from"]
        hand_edited_text = entry["why_prospect"]

        se.run_engine(data)  # nothing about the scored values changed

        self.assertEqual(entry["narrative_generated_from"], stamped_signature)
        self.assertEqual(entry["why_prospect"], hand_edited_text)


class OpportunityTypeRankingTests(unittest.TestCase):
    """2026-08-23: opportunity_type is the PRIMARY rank (GAP > GROWTH >
    DEFEND > REVIEW); final_score is only the tiebreak within a type. The
    real defect this fixes: final_score measures evidence quality, which
    correlates with business size, which correlates negatively with
    willingness to buy - the two most-visible, least-motivated DEFEND
    businesses in a real campaign outranked the one prospect with a real,
    actionable gap under the old final_score-first sort."""

    def test_gap_outranks_defend_even_with_a_lower_final_score(self):
        s = scored()
        gap, defend = s["Invisible But Credible"], s["Combined Leader"]
        self.assertEqual(gap["opportunity_type"], "GAP")
        self.assertEqual(defend["opportunity_type"], "DEFEND")
        # Precondition this test actually proves something: DEFEND scores
        # higher on final_score alone, yet must still rank behind GAP.
        self.assertGreater(defend["final_score"], gap["final_score"])
        self.assertLess(gap["overall_rank"], defend["overall_rank"])
        self.assertLess(gap["outreach_rank"], defend["outreach_rank"])

    def test_final_score_still_breaks_ties_within_one_type(self):
        # Both GROWTH in the main fixture, with different final_score -
        # within the same opportunity_type, the higher final_score must
        # still rank first, exactly as before this change.
        s = scored()
        higher, lower = s["Combined Runner-up"], s["Weak Field Leader"]
        self.assertEqual(higher["opportunity_type"], lower["opportunity_type"])
        self.assertGreater(higher["final_score"], lower["final_score"])
        self.assertLess(higher["overall_rank"], lower["overall_rank"])


class GapLighterGateTests(unittest.TestCase):
    """2026-08-23: GAP_LIGHTER_GATE_FIELDS lets a zero/low-visibility
    business reach GAP without business_credibility >= 3 - the bar was
    circular for exactly this cohort, since a business absent from every
    answer is typically thin on the web too. All three fields are Claude's
    judgement calls from a deliberately lighter research pass; missing or
    false on any one leaves the existing business_credibility path as the
    only route, unchanged."""

    def _entry(self, **overrides):
        data = make_fixture()
        defaults = {
            "service_scope": "combined",
            "question_appearances": {"q01": 0, "q02": 0, "q03": 0, "q04": 0},
            "business_credibility": 1,  # deliberately below GAP_MIN_CREDIBILITY
        }
        defaults.update(overrides)
        entry = base_outreach_entry("Lighter Gate Candidate", **defaults)
        data["outreach"].append(entry)
        se.run_engine(data)
        return next(o for o in data["outreach"] if o["business"] == "Lighter Gate Candidate")

    def test_all_three_fields_true_reaches_gap_despite_low_credibility(self):
        e = self._entry(active_entity_verified=True, live_website_verified=True, contact_route_exists=True)
        self.assertTrue(e["gap_lighter_gate_passed"])
        self.assertEqual(e["opportunity_type"], "GAP")

    def test_one_field_missing_gate_does_not_fire(self):
        e = self._entry(active_entity_verified=True, live_website_verified=True)  # contact_route_exists unset
        self.assertFalse(e["gap_lighter_gate_passed"])
        self.assertEqual(e["opportunity_type"], "REVIEW")  # unchanged from pre-existing behaviour

    def test_one_field_false_gate_does_not_fire(self):
        e = self._entry(active_entity_verified=True, live_website_verified=True, contact_route_exists=False)
        self.assertFalse(e["gap_lighter_gate_passed"])
        self.assertEqual(e["opportunity_type"], "REVIEW")

    def test_no_fields_set_behaves_exactly_as_before(self):
        e = self._entry()
        self.assertFalse(e["gap_lighter_gate_passed"])
        self.assertEqual(e["opportunity_type"], "REVIEW")

    def test_lighter_gate_never_overrides_a_real_visibility_score(self):
        # The gate only ever applies at vis_score <= GAP_MAX_VISIBILITY_SCORE
        # (1) - it says nothing about visibility strength, so a business with
        # real appearances must not be pulled into GAP just because the
        # three lighter-gate fields happen to be true.
        e = self._entry(
            question_appearances={"q01": 10, "q02": 10, "q03": 10, "q04": 10},
            active_entity_verified=True, live_website_verified=True, contact_route_exists=True,
        )
        self.assertNotEqual(e["opportunity_type"], "GAP")

    def test_lighter_gate_does_not_relax_ready_to_email(self):
        # opportunity_type and outreach-readiness are separate questions
        # (outreach-process.md): passing the lighter gate classifies the
        # opportunity, it does not manufacture the decision-maker/contact
        # evidence ready_to_email still requires.
        e = self._entry(active_entity_verified=True, live_website_verified=True, contact_route_exists=True,
                         decision_maker_identified=1, contact_identity_confidence=1, research_completeness=1)
        self.assertEqual(e["opportunity_type"], "GAP")
        self.assertEqual(e["ready_to_email"], "REVIEW")


if __name__ == "__main__":
    unittest.main()
