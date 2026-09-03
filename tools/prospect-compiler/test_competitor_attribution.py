"""Synthetic regressions: a nearest peer must not inherit the leader's rate."""
import unittest

import scoring_engine as se
from test_scoring_engine import base_outreach_entry, make_fixture


class CompetitorAttributionTests(unittest.TestCase):
    def campaign(self):
        data = make_fixture()
        data['outreach'] = [
            base_outreach_entry(name, service_scope='combined',
                                question_appearances={'q01': count})
            for name, count in [('Leader', 15), ('Near Peer', 2), ('Prospect', 0)]
        ]
        return data

    def test_nearest_peer_does_not_inherit_group_leader_percentage(self):
        data = self.campaign()
        se.run_engine(data)
        prospect = data['outreach'][2]
        self.assertEqual(prospect['nearest_competitor'], 'Near Peer')
        self.assertEqual(prospect['group_top_visibility_rate'], 25.0)
        for field in ('competitive_gap_finding', 'why_prospect'):
            self.assertNotIn('Near Peer', prospect[field])
            self.assertIn('25.0%', prospect[field])

    def test_leader_does_not_assign_its_own_rate_to_runner_up(self):
        data = self.campaign()
        data['outreach'][0]['question_appearances'] = {'q01': 15, 'q02': 15}
        se.run_engine(data)
        leader = data['outreach'][0]
        self.assertEqual(leader['opportunity_type'], 'DEFEND')
        for field in ('competitive_gap_finding', 'why_prospect'):
            self.assertNotIn('Near Peer', leader[field])
            self.assertIn('50.0%', leader[field])

    def test_old_signature_does_not_preserve_faulty_narrative(self):
        data = self.campaign()
        se.run_engine(data)
        prospect = data['outreach'][2]
        # The historical signature was just these fields, without a generator version.
        prospect['narrative_generated_from'] = '|'.join(
            f'{field}={prospect.get(field)}' for field in se.NARRATIVE_SIGNATURE_FIELDS)
        prospect['competitive_gap_finding'] = 'Near Peer incorrectly has 25.0% visibility.'
        prospect['why_prospect'] = 'Near Peer incorrectly has 25.0% visibility.'
        se.run_engine(data)
        self.assertNotIn('incorrectly', prospect['competitive_gap_finding'])
        self.assertNotIn('incorrectly', prospect['why_prospect'])


if __name__ == '__main__':
    unittest.main()
