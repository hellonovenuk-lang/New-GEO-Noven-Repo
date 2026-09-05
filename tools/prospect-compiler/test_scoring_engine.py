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
        # 5. High-scoring candidate withheld for incomplete evidence
        # (research_completeness below RESEARCH_COMPLETE_MIN).
        base_outreach_entry("Incomplete Evidence Star", service_scope="combined",
                             question_appearances={"q01": 9, "q02": 9, "q03": 9, "q04": 9},
                             business_credibility=5, commercial_fit=5, ability_to_buy=5,
                             decision_maker_identified=5, direct_dm_route=5, contact_route_quality=5,
                             contact_identity_confidence=5, research_completeness=2),
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


def lone_scope_incumbent_fixture():
    """A campaign whose single most-mentioned business is the only member of
    its own service_scope AND commercially ineligible (commercial_fit=0).
    Kept separate from make_fixture() so the shared fixture's ranking is not
    bent to serve two tests."""
    run = {
        "sector": "x", "geography": "x", "campaign_slug": "lone-scope", "date": "2026-08-16",
        "questions": [{"question_id": "q01", "text": "inclusive question"}],
        "providers": [{"provider": "openai", "model": "x"}],
        "responses_per_question": 100,
        "service_scopes": [
            {"label": "chain_central", "applicable_services": ["A"], "structure": "CENTRALLY_CONTROLLED_CHAIN"},
            {"label": "indie", "applicable_services": ["A"], "structure": "INDEPENDENT_LOCAL"},
        ],
        "question_relevance": [{"question_id": "q01", "type": "SINGLE_SERVICE_INCLUSIVE", "rationale": "x"}],
    }
    outreach = [
        base_outreach_entry("Central Chain", service_scope="chain_central",
                             question_appearances={"q01": 60}, commercial_fit=0,
                             business_structure="CENTRALLY_CONTROLLED_CHAIN", business_credibility=5),
        base_outreach_entry("Indie Leader", service_scope="indie",
                             question_appearances={"q01": 20}, business_credibility=4),
        base_outreach_entry("Indie Follower", service_scope="indie",
                             question_appearances={"q01": 5}, business_credibility=4),
    ]
    data = {"run": run, "market": [], "outreach": outreach, "excluded": [],
            "sources": [{"source_id": "S001", "business": "x", "publisher": "x", "fact_supported": "x",
                         "url": "x", "access_date": "2026-08-16"}]}
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


class IncumbentExclusionTests(unittest.TestCase):
    """2026-09-05: the incumbent hold-out is campaign-wide and fixed at
    INCUMBENT_EXCLUSION_COUNT, ranked by relevant_appearances - not a rank
    within each service_scope group. Also the standing regression test for a
    real bug class: a SECOND loop re-reading a stale `label` left over from
    the LAST iteration of a FIRST loop instead of each entry's own
    service_scope, so a per-entry check was silently evaluated against
    whichever scope happened to be processed last. relative_position is still
    computed that shape, so the fixture keeps a deliberately
    differently-sized, differently-ordered second group to keep catching it."""

    def build(self):
        run = {
            "sector": "x", "geography": "x", "campaign_slug": "x", "date": "2026-08-16",
            "questions": [{"question_id": "q01", "text": "inclusive question"}],
            "providers": [{"provider": "openai", "model": "x"}],
            "responses_per_question": 100,
            "service_scopes": [
                {"label": "big_group", "applicable_services": ["A"]},
                {"label": "zzz_solo_group", "applicable_services": ["A"]},  # sorts/inserts last
            ],
            "question_relevance": [{"question_id": "q01", "type": "SINGLE_SERVICE_INCLUSIVE", "rationale": "x"}],
        }
        # big_group: 7 members at 100/95/90/85/80/75/71% visibility_rate -
        # every member clears the absolute floor (>=3) and the
        # relative-position band (>=0.7 of the group's own 100% top rate;
        # 71% is deliberately the lowest value that still clears 0.7), so
        # only the campaign-wide count cap can separate them.
        big_group = [
            base_outreach_entry(f"Big Group Member {i}", service_scope="big_group",
                                 question_appearances={"q01": appearances}, business_credibility=5)
            for i, appearances in enumerate([100, 95, 90, 85, 80, 75, 71], start=1)
        ]
        # Deliberately the LAST entry, so its scope is the last one touched
        # by the group-computation loop - this is exactly the condition that
        # exposed the stale-variable bug.
        outreach = big_group + [
            base_outreach_entry("Solo Group Member", service_scope="zzz_solo_group",
                                 question_appearances={"q01": 50}, business_credibility=5),
        ]
        data = {"run": run, "market": [], "outreach": outreach, "excluded": [],
                "sources": [{"source_id": "S001", "business": "x", "publisher": "x", "fact_supported": "x",
                             "url": "x", "access_date": "2026-08-16"}]}
        se.run_engine(data)
        return {e["business"]: e for e in data["outreach"]}

    def test_only_the_two_most_mentioned_are_held_out_campaign_wide(self):
        by_name = self.build()
        held_out = sorted(b for b, e in by_name.items() if e["most_named_cohort"])
        self.assertEqual(held_out, ["Big Group Member 1", "Big Group Member 2"])
        self.assertEqual(len(held_out), se.INCUMBENT_EXCLUSION_COUNT)

    def test_remaining_qualifying_businesses_stay_prospects(self):
        # Ranks 3-7 clear the absolute floor and the relative-position band
        # but are no longer held out - this is the change that puts a market's
        # sendable batch back into double figures. They KEEP their DEFEND
        # classification: filling the two exclusion places does not reclassify
        # a strongly visible business as GROWTH.
        by_name = self.build()
        for i in range(3, 8):
            e = by_name[f"Big Group Member {i}"]
            self.assertFalse(e["most_named_cohort"], f"member {i} should not be held out")
            self.assertEqual(e["opportunity_type"], "DEFEND", f"member {i} keeps its classification")
            self.assertEqual(e["disposition_recommendation"], "OUTREACH")
            self.assertEqual(e["ready_to_email"], "YES")

    def test_classification_is_independent_of_the_exclusion_cap(self):
        # Every business meeting the dominance conditions is DEFEND; only the
        # two most-mentioned of them are held out.
        by_name = self.build()
        defend = {b for b, e in by_name.items() if e["opportunity_type"] == "DEFEND"}
        held_out = {b for b, e in by_name.items() if e["most_named_cohort"]}
        # Every big_group member plus the solo-group leader, which is dominant
        # within its own scope but nowhere near the two most-mentioned.
        self.assertEqual(defend, {f"Big Group Member {i}" for i in range(1, 8)} | {"Solo Group Member"})
        self.assertTrue(held_out < defend)
        self.assertEqual(len(held_out), se.INCUMBENT_EXCLUSION_COUNT)

    def test_relative_position_stays_scoped_to_each_businesss_own_group(self):
        # The stale-`label` regression: Solo Group Member is rank 1 of its own
        # 1-member group, so its relative_position is 1.0 against itself, not
        # a fraction of big_group's 100% leader.
        by_name = self.build()
        self.assertEqual(by_name["Solo Group Member"]["relative_position"], 1.0)
        self.assertEqual(by_name["Solo Group Member"]["group_top_visibility_rate"],
                          by_name["Solo Group Member"]["visibility_rate"])
        self.assertFalse(by_name["Solo Group Member"]["most_named_cohort"])


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

    def test_gap_no_longer_requires_credibility(self):
        # 2026-08-24: GAP is unconditional at zero visibility now - credibility
        # is irrelevant to the classification (it still drives ready_to_email
        # separately, via overall_evidence_confidence).
        for e in self.s.values():
            if e["opportunity_type"] == "GAP":
                self.assertEqual(e["visibility_score"], 0)

    def test_no_opportunity_type_is_ever_review(self):
        # 2026-08-24: the REVIEW-for-uncertain-credibility branch is gone -
        # every scored entry gets DEFEND, GAP or GROWTH, never REVIEW.
        for e in self.s.values():
            self.assertIn(e["opportunity_type"], ("DEFEND", "GAP", "GROWTH"))

    def test_defend_requires_absolute_and_relative_evidence(self):
        for e in self.s.values():
            if e["opportunity_type"] == "DEFEND":
                self.assertGreaterEqual(e["visibility_score"], se.MOST_NAMED_COHORT_MIN_VISIBILITY_SCORE)
                self.assertGreaterEqual(e["relative_position"], se.MOST_NAMED_COHORT_MIN_RELATIVE_POSITION)

    def test_every_held_out_business_is_defend_but_not_the_reverse(self):
        # The hold-out is a subset of DEFEND, never its definition.
        for e in self.s.values():
            if e["most_named_cohort"]:
                self.assertEqual(e["opportunity_type"], "DEFEND")

    def test_defend_no_longer_requires_a_group_of_two(self):
        # 2026-08-24: the "comparable same-scope peer exists" requirement is
        # dropped - a business alone in its service_scope can now reach
        # DEFEND on the strength of its own absolute visibility and relative
        # position alone (relative_position=1.0 against itself, trivially).
        data = make_fixture()
        data["outreach"] = [base_outreach_entry(
            "Lone Scope Business", service_scope="combined",
            question_appearances={"q01": 10, "q02": 10, "q03": 10, "q04": 10}, business_credibility=5,
        )]
        se.run_engine(data)
        self.assertEqual(data["outreach"][0]["opportunity_type"], "DEFEND")
        self.assertTrue(data["outreach"][0]["most_named_cohort"])


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
        # Zero visibility_score, deliberately low credibility - proves GAP is
        # unconditional at zero visibility now (2026-08-24), not gated on
        # credibility the way "Fixture Bathroom Co" above (visibility_score=1,
        # GROWTH under the current rule) used to be.
        base_outreach_entry("Fixture Bathroom Ghost", service_scope="bathroom_only",
                             question_appearances={"q01": 0, "q05": 0, "q06": 0},
                             business_credibility=2),
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
        self.assertIn("strongest AI-recommendation position", e["why_prospect"])

    def test_growth_rationale(self):
        e = narrative_scored()["Fixture Kitchen Co"]
        self.assertEqual(e["opportunity_type"], "GROWTH")
        self.assertIn("room to strengthen", e["why_prospect"])

    def test_gap_rationale(self):
        e = narrative_scored()["Fixture Bathroom Ghost"]
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


class MostNamedCohortReclassificationTests(unittest.TestCase):
    """2026-08-24: opportunity_type is redefined around most_named_cohort -
    DEFEND targets only the businesses already dominating a market's answers
    (visibility_score >= 3, relative_position >= 0.7, and - since 2026-09-05 -
    among the INCUMBENT_EXCLUSION_COUNT most-mentioned campaign-wide); GAP is
    unconditional at visibility_score == 0; GROWTH is everything else. These
    fixture businesses each land on a different opportunity_type than the
    pre-2026-08-24 rule gave them - the real behaviour change this
    redefinition exists to make, not a hypothetical."""

    def setUp(self):
        self.s = scored()

    def test_zero_visibility_low_credibility_business_is_gap_not_review(self):
        # Weak Field Runner-up: visibility_score=0, business_credibility=2.
        # Previously REVIEW (credibility below GAP_MIN_CREDIBILITY, no
        # lighter-gate fields set) - now GAP outright, since credibility no
        # longer gates GAP at all.
        e = self.s["Weak Field Runner-up"]
        self.assertEqual(e["visibility_score"], 0)
        self.assertLess(e["business_credibility"], 3)
        self.assertEqual(e["opportunity_type"], "GAP")

    def test_low_nonzero_visibility_no_longer_qualifies_for_gap(self):
        # Generic Inbox Confirmed Owner and Inferred Contact Only both sit at
        # visibility_score=1 (nonzero). Previously GAP (vis_score <= 1, real
        # credibility) - now GROWTH, since GAP requires visibility_score
        # == 0 exactly, not merely low.
        for business in ("Generic Inbox Confirmed Owner", "Inferred Contact Only"):
            e = self.s[business]
            self.assertEqual(e["visibility_score"], 1)
            self.assertEqual(e["opportunity_type"], "GROWTH")

    def test_lone_business_in_its_scope_can_now_defend(self):
        # A business alone in its service_scope is not blocked from the cohort
        # by having no comparable peer (relative_position is 1.0 against
        # itself): it reaches DEFEND on its own absolute visibility, provided
        # it is also among the campaign's most-mentioned.
        e = lone_scope_incumbent_fixture()["Central Chain"]
        self.assertGreaterEqual(e["visibility_score"], se.MOST_NAMED_COHORT_MIN_VISIBILITY_SCORE)
        self.assertEqual(e["relative_position"], 1.0)
        self.assertTrue(e["most_named_cohort"])
        self.assertEqual(e["opportunity_type"], "DEFEND")


class LeaderOutsideExclusionTests(unittest.TestCase):
    """2026-09-05 regression. Three service scopes, each with a clear leader
    that meets both dominance conditions. Only two exclusion places exist, so
    the third scope's leader falls outside them. It must (a) keep DEFEND
    rather than being reclassified GROWTH because the places are full,
    (b) stay available for outreach, and (c) never be told in prose that it
    sits behind a visibility rate that is its own."""

    BEHIND_PHRASES = ("materially behind", "materially underrepresented against",
                      "% of the group's highest visibility rate")

    def build(self):
        run = {
            "sector": "x", "geography": "x", "campaign_slug": "leaders", "date": "2026-08-16",
            "questions": [{"question_id": "q01", "text": "inclusive question"}],
            "providers": [{"provider": "openai", "model": "x"}],
            "responses_per_question": 100,
            "service_scopes": [
                {"label": f"scope_{n}", "applicable_services": ["A"]} for n in ("a", "b", "c")
            ],
            "question_relevance": [{"question_id": "q01", "type": "SINGLE_SERVICE_INCLUSIVE", "rationale": "x"}],
        }
        outreach = []
        # Leaders at 90 / 70 / 50 appearances; the scope_c leader is third
        # most-mentioned campaign-wide, so it falls outside the two places.
        for label, lead, follow in (("scope_a", 90, 20), ("scope_b", 70, 15), ("scope_c", 50, 10)):
            outreach.append(base_outreach_entry(f"{label} leader", service_scope=label,
                                                 question_appearances={"q01": lead}, business_credibility=5))
            outreach.append(base_outreach_entry(f"{label} follower", service_scope=label,
                                                 question_appearances={"q01": follow}, business_credibility=4))
        data = {"run": run, "market": [], "outreach": outreach, "excluded": [],
                "sources": [{"source_id": "S001", "business": "x", "publisher": "x", "fact_supported": "x",
                             "url": "x", "access_date": "2026-08-16"}]}
        se.run_engine(data)
        return {e["business"]: e for e in data["outreach"]}

    def test_only_two_leaders_are_held_out(self):
        by_name = self.build()
        held_out = sorted(b for b, e in by_name.items() if e["most_named_cohort"])
        self.assertEqual(held_out, ["scope_a leader", "scope_b leader"])

    def test_leader_outside_the_cap_keeps_defend_and_stays_available(self):
        e = self.build()["scope_c leader"]
        self.assertFalse(e["most_named_cohort"])
        self.assertEqual(e["opportunity_type"], "DEFEND")
        self.assertEqual(e["disposition_recommendation"], "OUTREACH")
        self.assertNotIn("disposition_recommendation_reason", e)
        self.assertEqual(e["ready_to_email"], "YES")
        self.assertIn("outreach_rank", e)

    def test_leader_outside_the_cap_gets_truthful_wording(self):
        e = self.build()["scope_c leader"]
        self.assertEqual(e["relative_position"], 1.0)
        self.assertIn("strongest AI-recommendation position", e["why_prospect"])
        for phrase in self.BEHIND_PHRASES:
            self.assertNotIn(phrase, e["why_prospect"],
                              f"a group leader must not be described with {phrase!r}")

    def test_no_group_leader_anywhere_is_described_as_behind_its_own_rate(self):
        for name, e in self.build().items():
            if not se.leads_its_group(e):
                continue
            for phrase in self.BEHIND_PHRASES:
                self.assertNotIn(phrase, e["why_prospect"], f"{name}: {phrase!r}")

    def test_a_growth_group_leader_is_also_described_truthfully(self):
        # Weak Field Leader leads its a_only group (relative_position 1.0) but
        # sits below the absolute floor, so it stays GROWTH - the wording must
        # still not claim it trails a rate that is its own.
        e = scored()["Weak Field Leader"]
        self.assertEqual(e["opportunity_type"], "GROWTH")
        self.assertEqual(e["relative_position"], 1.0)
        self.assertIn("highest visibility rate in its own service-scope group", e["why_prospect"])
        for phrase in self.BEHIND_PHRASES:
            self.assertNotIn(phrase, e["why_prospect"])


class SendGateTests(unittest.TestCase):
    """2026-09-05: the ready_to_email gate keeps business verification, contact
    route, commercial fit and evidence accuracy, and drops the named
    decision-maker requirement. Optional enrichment does not block; a business
    with no usable route still does."""

    def ready(self, **overrides):
        data = {"run": copy.deepcopy(make_fixture()["run"]), "market": [], "excluded": [],
                "sources": [{"source_id": "S001", "business": "x", "publisher": "x",
                             "fact_supported": "x", "url": "x", "access_date": "2026-08-16"}]}
        data["outreach"] = [base_outreach_entry("Subject", service_scope="a_only",
                                                 question_appearances={"q01": 1}, **overrides)]
        se.run_engine(data)
        return data["outreach"][0]

    def test_no_named_contact_does_not_block_a_verified_route(self):
        e = self.ready(decision_maker_identified=0, contact_identity_confidence=0, direct_dm_route=2)
        self.assertEqual(e["ready_to_email"], "YES")
        self.assertEqual(e["identity_confidence"], "UNKNOWN")
        self.assertEqual(e["named_decision_maker_verified"], "NO")
        self.assertEqual(e["accessibility_grade"], "GENERIC_INBOX_ONLY")

    def test_no_usable_route_still_blocks(self):
        for route in (0, 1):
            e = self.ready(direct_dm_route=route)
            self.assertEqual(e["ready_to_email"], "REVIEW", f"direct_dm_route={route} must block")

    def test_unverified_business_still_blocks(self):
        e = self.ready(business_credibility=2)
        self.assertEqual(e["business_verified"], "REVIEW")
        self.assertEqual(e["ready_to_email"], "REVIEW")

    def test_unverified_contact_route_still_blocks(self):
        e = self.ready(contact_route_quality=2)
        self.assertEqual(e["contact_route_verified"], "REVIEW")
        self.assertEqual(e["ready_to_email"], "REVIEW")

    def test_incomplete_research_still_blocks(self):
        e = self.ready(research_completeness=se.RESEARCH_COMPLETE_MIN - 1)
        self.assertEqual(e["research_complete"], "NO")
        self.assertEqual(e["ready_to_email"], "REVIEW")

    def test_evidence_confidence_is_credibility_and_research_only(self):
        e = self.ready(business_credibility=4, research_completeness=3,
                       decision_maker_identified=0, contact_identity_confidence=0)
        self.assertEqual(e["overall_evidence_confidence"], 3)


class DispositionRecommendationTests(unittest.TestCase):
    """2026-08-24: disposition_recommendation on an outreach[] entry follows
    most_named_cohort, not opportunity_type generally - only the dominant
    cluster defaults to EXCLUDED; GAP and GROWTH default exactly as before
    (OUTREACH if eligible_for_outreach, else REVIEW)."""

    def setUp(self):
        self.s = scored()

    def test_most_named_cohort_defaults_to_excluded_already_strongly_visible(self):
        # Combined Leader is most_named_cohort (DEFEND) and otherwise fully
        # eligible - proves the EXCLUDED default comes from most_named_cohort
        # itself, not from some other disqualifying factor.
        e = self.s["Combined Leader"]
        self.assertTrue(e["most_named_cohort"])
        self.assertEqual(e["eligible_for_outreach"], "YES")
        self.assertEqual(e["disposition_recommendation"], "EXCLUDED")
        self.assertEqual(e["disposition_recommendation_reason"], "ALREADY STRONGLY VISIBLE")

    def test_most_named_cohort_excluded_even_when_otherwise_ineligible(self):
        # A held-out incumbent that is also eligible_for_outreach=REVIEW
        # (commercial_fit=0) must still recommend EXCLUDED, not REVIEW, since
        # most_named_cohort is checked first.
        e = lone_scope_incumbent_fixture()["Central Chain"]
        self.assertTrue(e["most_named_cohort"])
        self.assertEqual(e["eligible_for_outreach"], "REVIEW")
        self.assertEqual(e["disposition_recommendation"], "EXCLUDED")
        self.assertEqual(e["disposition_recommendation_reason"], "ALREADY STRONGLY VISIBLE")

    def test_gap_and_growth_default_outreach_or_review_same_as_today(self):
        for business, expected_eligible in (
            ("Invisible But Credible", "YES"),  # GAP, eligible
            ("Weak Field Leader", "YES"),  # GROWTH, eligible
        ):
            e = self.s[business]
            self.assertFalse(e["most_named_cohort"])
            self.assertEqual(e["eligible_for_outreach"], expected_eligible)
            self.assertEqual(e["disposition_recommendation"], "OUTREACH")
            self.assertNotIn("disposition_recommendation_reason", e)


if __name__ == "__main__":
    unittest.main()
