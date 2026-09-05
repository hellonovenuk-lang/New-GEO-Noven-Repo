"""Coverage is census-wide, conservative and never mutates campaign decisions."""
import copy
from datetime import date
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


class CoverageTests(unittest.TestCase):
    def report(self, data, census=()):
        path = Path(__file__).with_name('qualification_coverage.py')
        self.assertTrue(path.exists(), 'Missing census-wide coverage implementation')
        spec = importlib.util.spec_from_file_location('qualification_coverage', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.build_report(data, census)

    def fixture(self):
        return {'run': {'campaign_slug': 'fictional'}, 'market': [],
                'outreach': [], 'excluded': [], 'sources': []}

    def test_zero_visibility_and_census_only_businesses_are_not_dropped(self):
        data = self.fixture()
        data['market'] = [{'business': 'Quiet Ltd', 'total_ai_appearances': 0}]
        report = self.report(data, ['Quiet Ltd', 'Unresearched Ltd'])
        self.assertEqual(report['counts']['REVIEW'], 2)
        self.assertEqual(report['potential_non_top'], 2)
        self.assertEqual(report['missing_from_campaign'], ['Unresearched Ltd'])

    def test_incumbents_are_distinct_from_hard_exclusions(self):
        data = self.fixture()
        data['run']['date'] = date.today().isoformat()
        data['market'] = [{'business': 'Leader Ltd', 'most_named_cohort': True}]
        data['excluded'] = [{'business': 'Closed Ltd', 'reason': 'CLOSED / DORMANT'}]
        report = self.report(data)
        self.assertEqual(report['counts']['INCUMBENT'], 1)
        self.assertEqual(report['counts']['EXCLUDE'], 1)
        self.assertEqual(report['potential_non_top'], 0)

    def test_legacy_visibility_exclusion_needs_reassessment_not_permanent_drop(self):
        data = self.fixture()
        data['excluded'] = [{'business': 'Visible Ltd', 'reason': 'ALREADY STRONGLY VISIBLE'}]
        report = self.report(data)
        self.assertEqual(report['rows'][0]['selection_group'], 'REVIEW')
        self.assertIn('dominance', ' '.join(report['rows'][0]['blockers']))

    def test_unresolved_legal_match_is_review_not_genuine_exclusion(self):
        data = self.fixture()
        data['excluded'] = [{'business': 'Match Needed Ltd', 'reason': 'NO RELIABLE LEGAL MATCH'}]
        self.assertEqual(self.report(data)['counts']['REVIEW'], 1)

    def test_verified_general_inbox_stays_secondary_without_inventing_readiness(self):
        data = self.fixture()
        data['outreach'] = [{'business': 'Generic Ltd', 'company_status': 'Active',
            'company_number': '00000001', 'legal_entity': 'Generic Ltd',
            'eligible_for_outreach': 'YES', 'research_complete': 'YES',
            'contact_route_verified': 'YES', 'contact_email': 'info@example.test',
            'ready_to_email': 'REVIEW', 'direct_dm_route': 2, 'priority': 'B'}]
        report = self.report(data)
        self.assertEqual(report['counts']['SECONDARY'], 1)
        self.assertEqual(data['outreach'][0]['ready_to_email'], 'REVIEW')
        self.assertTrue(report['rows'][0]['blockers'])

    def test_historical_yes_is_not_reported_as_freshly_send_ready(self):
        data = self.fixture()
        data['outreach'] = [{'business': 'Legacy Ltd', 'ready_to_email': 'YES'}]
        report = self.report(data)
        self.assertEqual(report['recorded_ready'], 1)
        self.assertEqual(report['counts']['SEND NOW'], 0)

    def test_current_canonical_ready_record_is_proposed_send_now(self):
        data = self.fixture()
        data['run']['date'] = date.today().isoformat()
        data['outreach'] = [{'business': 'Current Ltd', 'ready_to_email': 'YES',
            'eligible_for_outreach': 'YES', 'research_complete': 'YES',
            'business_verified': 'YES', 'contact_route_verified': 'YES',
            'company_number': '00000002', 'company_status': 'Active',
            'contact_email': 'owner@example.test', 'decision_maker_identified': 4,
            'contact_identity_confidence': 4, 'overall_evidence_confidence': 4,
            'direct_dm_route': 4}]
        self.assertEqual(self.report(data)['counts']['SEND NOW'], 1)

    def test_stale_incumbent_is_review_not_current_confirmation(self):
        data = self.fixture()
        data['run']['date'] = '2020-01-01'
        data['market'] = [{'business': 'Old Leader Ltd', 'most_named_cohort': True}]
        result = self.report(data)
        self.assertEqual(result['counts']['REVIEW'], 1)
        self.assertIn('Historical', ' '.join(result['rows'][0]['blockers']))

    def test_inconsistent_generic_ready_flags_cannot_reach_send_now(self):
        # 2026-09-05: a missing named decision-maker no longer blocks - a
        # verified business inbox is a valid route. A missing email route and
        # unresolved evidence confidence still do, and are named as blockers.
        data = self.fixture()
        data['run']['date'] = date.today().isoformat()
        data['outreach'] = [{'business': 'Unsafe Ltd', 'ready_to_email': 'YES',
            'eligible_for_outreach': 'YES', 'research_complete': 'YES',
            'business_verified': 'YES', 'contact_route_verified': 'YES',
            'company_number': '00000003', 'company_status': 'Active',
            'direct_dm_route': 2, 'decision_maker_identified': 0,
            'contact_identity_confidence': 0}]
        result = self.report(data)
        self.assertEqual(result['counts']['SEND NOW'], 0)
        self.assertIn('email route', ' '.join(result['rows'][0]['blockers']).lower())

    def test_missing_named_contact_alone_does_not_block_send_now(self):
        # A verified active company, a verified generic business inbox and
        # complete research is sendable. No name is invented to get there.
        data = self.fixture()
        data['run']['date'] = date.today().isoformat()
        data['outreach'] = [{'business': 'Generic Inbox Ltd', 'ready_to_email': 'YES',
            'eligible_for_outreach': 'YES', 'research_complete': 'YES',
            'business_verified': 'YES', 'contact_route_verified': 'YES',
            'company_number': '00000004', 'company_status': 'Active',
            'contact_email': 'hello@example.invalid', 'overall_evidence_confidence': 3,
            'direct_dm_route': 2, 'decision_maker_identified': 0,
            'contact_identity_confidence': 0}]
        result = self.report(data)
        self.assertEqual(result['counts']['SEND NOW'], 1)
        self.assertEqual(result['rows'][0]['blockers'], [])

    def test_every_non_send_row_states_a_blocker(self):
        data = self.fixture()
        data['run']['date'] = date.today().isoformat()
        data['outreach'] = [{'business': 'Half Done Ltd', 'ready_to_email': 'YES',
            'eligible_for_outreach': 'YES', 'research_complete': 'YES',
            'business_verified': 'YES', 'contact_route_verified': 'YES',
            'company_number': '00000005', 'company_status': 'Active',
            'contact_email': 'hello@example.invalid', 'overall_evidence_confidence': 2,
            'direct_dm_route': 2}]
        result = self.report(data)
        for row in result['rows']:
            if row['selection_group'] != 'SEND NOW':
                self.assertTrue(row['blockers'], f"{row['business']} has no stated blocker")

    def test_cohort_specific_missing_evidence_is_preserved(self):
        data = self.fixture()
        data['market'] = [{'business': 'Open Ltd'}]
        data['run']['scoring_cohort'] = [{'business': 'Open Ltd', 'status': 'INCOMPLETE',
            'missing_evidence': 'Cannot verify current owner and geography'}]
        result = self.report(data)
        self.assertIn('Cannot verify current owner and geography', result['rows'][0]['blockers'])

    def test_missing_census_business_makes_coverage_incomplete(self):
        data = self.fixture()
        result = self.report(data, ['Missing Ltd'])
        self.assertEqual(result.get('coverage_status'), 'INCOMPLETE')
        self.assertTrue(result.get('completion_blockers'))

    def test_scored_but_unfinished_research_is_not_complete(self):
        data = self.fixture()
        data['run'].update({'cohort_inclusion_min_appearances': 0,
            'scoring_cohort': [{'business': 'Unfinished Ltd', 'status': 'SCORED'}]})
        data['market'] = [{'business': 'Unfinished Ltd', 'service_scope': 'local',
            'overall_rank': 1, 'research_complete': 'NO'}]
        self.assertEqual(self.report(data, ['Unfinished Ltd'])['coverage_status'], 'INCOMPLETE')

    def test_blank_census_names_cannot_pass_completion(self):
        data = self.fixture()
        data['run']['cohort_inclusion_min_appearances'] = 0
        self.assertEqual(self.report(data, [{'business': ' '}])['coverage_status'], 'INCOMPLETE')

    def test_old_secondary_has_freshness_blocker(self):
        data = self.fixture()
        data['run']['date'] = '2020-01-01'
        data['outreach'] = [{'business': 'Old Ltd', 'eligible_for_outreach': 'YES',
            'research_complete': 'YES', 'ready_to_email': 'YES'}]
        result = self.report(data)
        self.assertIn('Historical', ' '.join(result['rows'][0]['blockers']))

    def test_cli_refuses_to_overwrite_a_report(self):
        path = Path(__file__).with_name('qualification_coverage.py')
        spec = importlib.util.spec_from_file_location('qualification_coverage_cli', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'campaign.json'
            output = Path(folder) / 'coverage.json'
            source.write_text(json.dumps(self.fixture()), encoding='utf-8')
            output.write_text('keep', encoding='utf-8')
            with mock.patch('sys.argv', ['coverage', '--input', str(source), '--output', str(output)]):
                self.assertEqual(module.main(), 2)
            self.assertEqual(output.read_text(encoding='utf-8'), 'keep')

    def test_conflicting_market_and_outreach_decisions_are_flagged(self):
        data = self.fixture()
        data['market'] = [{'business': 'Conflict Ltd', 'disposition': 'REVIEW'}]
        data['outreach'] = [{'business': 'Conflict Ltd', 'ready_to_email': 'YES'}]
        report = self.report(data)
        self.assertEqual(len(report['rows']), 1)
        self.assertEqual(report['rows'][0]['selection_group'], 'REVIEW')
        self.assertIn('conflict', ' '.join(report['rows'][0]['blockers']).lower())

    def test_duplicate_names_never_inflate_coverage(self):
        data = self.fixture()
        data['market'] = [{'business': 'Quiet Ltd'}, {'business': ' quiet ltd '}]
        report = self.report(data, ['QUIET LTD'])
        self.assertEqual(report['total_businesses'], 1)
        self.assertTrue(report['rows'][0]['blockers'])

    def test_report_does_not_mutate_input(self):
        data = self.fixture()
        data['market'] = [{'business': 'Untouched Ltd', 'disposition': 'REVIEW'}]
        original = copy.deepcopy(data)
        self.report(data)
        self.assertEqual(data, original)


if __name__ == '__main__':
    unittest.main()
