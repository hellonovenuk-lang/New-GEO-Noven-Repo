"""Synthetic, offline behavior tests for evidence-led qualification."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from qualification_coverage import build_report as coverage_report
try:
    from review_evidence import (new_ledger, add_finding, record_attempt, build_plan,
                                 build_report, reconcile, park, reopen)
except ModuleNotFoundError:
    def missing(*args, **kwargs):
        raise AssertionError('Evidence helper behavior is not implemented')
    new_ledger = add_finding = record_attempt = build_plan = build_report = missing
    reconcile = park = reopen = missing

NOW = '2026-09-03T12:00:00+00:00'
LATER = '2026-09-03T13:00:00+00:00'
TOMORROW = '2026-09-04T12:00:00+00:00'


def campaign():
    return {'run': {'campaign_slug': 'sample', 'date': '2026-09-01'},
            'market': [{'business': 'Example', 'notes': 'active company'}],
            'outreach': [], 'excluded': [], 'sources': []}


def finding(requirement, value, state='VERIFIED', at=NOW, supersedes=()):
    sources = [{'url': 'https://example.test/contact', 'retrieved_at': at,
                'excerpt': 'Example Ltd 00000001 info@example.test provides installation locally',
                'publisher': 'Example business', 'role': 'business'}]
    if requirement in {'legal_identity', 'active_company'}:
        sources.append({'url': 'https://find-and-update.company-information.service.gov.uk/company/00000001',
                        'retrieved_at': at, 'excerpt': 'Example Ltd 00000001 active limited company',
                        'publisher': 'Companies House', 'role': 'registry'})
    return {'requirement': requirement, 'state': state, 'value': value,
            'sources': sources, 'method': 'published_page',
            'rationale': 'The cited pages explicitly support this assessment.',
            'reviewer': 'agent', 'supersedes': list(supersedes)}


LEGAL = {'company_number': '00000001', 'legal_name': 'Example Ltd', 'basis': 'published_number'}
ACTIVE = {'company_number': '00000001', 'status': 'active', 'company_type': 'ltd'}
CONTACT = {'email': 'info@example.test', 'published': True, 'kind': 'generic'}


class EvidenceTests(unittest.TestCase):
    def ledger(self):
        return new_ledger(campaign(), ['Example'], NOW)

    def positive(self, ledger=None):
        ledger = ledger or self.ledger()
        for req, value in [('legal_identity', LEGAL), ('active_company', ACTIVE),
                           ('services', {'relevant': True}), ('geography', {'local': True}),
                           ('decision_maker', {'name': 'Synthetic Owner', 'operational': True}),
                           ('contact_route', CONTACT), ('duplicate_identity', {'duplicate': False})]:
            ledger = add_finding(ledger, 'Example', finding(req, value), NOW)
        return ledger

    def test_notes_are_not_verified_evidence(self):
        ledger = self.ledger()
        self.assertIn('legal_identity', build_plan(ledger, NOW)['records'][0]['pending'])

    def test_verified_generic_inbox_is_usable_without_named_contact(self):
        ledger = add_finding(self.ledger(), 'Example', finding('contact_route', CONTACT), NOW)
        row = build_plan(ledger, NOW)['records'][0]
        self.assertNotIn('contact_route', row['pending'])
        self.assertIn('decision_maker', row['pending'])

    def test_legal_name_only_and_missing_business_source_are_rejected(self):
        for value, role in [({**LEGAL, 'basis': 'name_only'}, None), (LEGAL, 'registry')]:
            item = finding('legal_identity', value)
            if role:
                item['sources'] = [item['sources'][1]]
            with self.assertRaises(ValueError):
                add_finding(self.ledger(), 'Example', item, NOW)

    def test_contact_guess_and_not_applicable_prerequisites_are_rejected(self):
        for item in [finding('contact_route', {**CONTACT, 'published': False}),
                     finding('contact_route', {**CONTACT, 'email': 'guessed@example.test'}),
                     finding('legal_identity', {}, 'NOT_APPLICABLE'),
                     finding('active_company', {}, 'NOT_APPLICABLE'),
                     finding('contact_route', {}, 'NOT_APPLICABLE')]:
            with self.assertRaises(ValueError):
                add_finding(self.ledger(), 'Example', item, NOW)

    def test_mismatched_active_number_is_a_conflict(self):
        ledger = add_finding(self.ledger(), 'Example', finding('legal_identity', LEGAL), NOW)
        item = finding('active_company', {**ACTIVE, 'company_number': '00000002'})
        item['sources'][1]['excerpt'] = '00000002 active limited company'
        item['sources'][1]['url'] = item['sources'][1]['url'].replace('00000001', '00000002')
        ledger = add_finding(ledger, 'Example', item, NOW)
        self.assertEqual(build_plan(ledger, NOW)['records'][0]['requirements']['active_company']['state'], 'CONFLICT')

    def test_sources_require_valid_urls_aware_times_excerpts_and_rationale(self):
        for field, value in [('url', 'javascript:alert(1)'), ('url', 'https://'),
                             ('retrieved_at', '2026-09-03T12:00:00'), ('excerpt', '')]:
            item = finding('services', {'relevant': True})
            item['sources'][0][field] = value
            with self.assertRaises(ValueError):
                add_finding(self.ledger(), 'Example', item, NOW)
        item = finding('services', {'relevant': True})
        item['rationale'] = ' '
        with self.assertRaises(ValueError):
            add_finding(self.ledger(), 'Example', item, NOW)

    def test_negative_services_and_locality_are_facts_not_missing(self):
        ledger = self.ledger()
        for req, key in [('services', 'relevant'), ('geography', 'local')]:
            ledger = add_finding(ledger, 'Example', finding(req, {key: False}), NOW)
        row = build_plan(ledger, NOW)['records'][0]
        self.assertEqual(row['requirements']['services']['state'], 'VERIFIED')
        self.assertNotIn('services', row['pending'])
        self.assertFalse(row['evidence_ready'])
        self.assertIn('geography', [x['requirement'] for x in build_report(ledger, campaign(), NOW)['exceptions']])

    def test_newer_contradiction_persists_until_explicit_supersession(self):
        ledger = add_finding(self.ledger(), 'Example', finding('services', {'relevant': True}), NOW)
        ledger = add_finding(ledger, 'Example', finding('services', {'relevant': False}, at=LATER), LATER)
        self.assertEqual(build_plan(ledger, LATER)['records'][0]['requirements']['services']['state'], 'CONFLICT')
        ids = [f['id'] for f in ledger['records'][0]['findings']]
        ledger = add_finding(ledger, 'Example', finding('services', {'relevant': True}, at=LATER, supersedes=ids), LATER)
        self.assertNotIn('services', build_plan(ledger, LATER)['records'][0]['pending'])
        self.assertEqual(len(ledger['records'][0]['findings']), 3)

    def test_stale_company_contact_and_owner_refresh_but_services_reuse(self):
        row = build_plan(self.positive(), TOMORROW)['records'][0]
        for req in ['legal_identity', 'active_company', 'decision_maker', 'contact_route']:
            self.assertEqual(row['requirements'][req]['state'], 'STALE')
        self.assertNotIn('services', row['pending'])
        self.assertIn('services', build_plan(self.positive(), '2026-10-04T12:00:00+00:00')['records'][0]['pending'])

    def test_suspected_duplicates_are_exceptions_not_merged(self):
        ledger = add_finding(self.ledger(), 'Example', finding('duplicate_identity', {'duplicate': True, 'candidate_id': 'other'}, 'CONFLICT'), NOW)
        report = build_report(ledger, campaign(), NOW)
        self.assertEqual(len(report['records']), 1)
        self.assertIn('duplicate_identity', [x['requirement'] for x in report['exceptions']])
        self.assertEqual(reconcile(ledger, campaign(), NOW)['draft']['market'], campaign()['market'])

    def test_all_transformations_preserve_inputs(self):
        original = campaign()
        saved = copy.deepcopy(original)
        ledger = new_ledger(original, ['Example'], NOW)
        before = copy.deepcopy(ledger)
        add_finding(ledger, 'Example', finding('services', {'relevant': True}), NOW)
        build_plan(ledger, NOW)
        build_report(ledger, original, NOW)
        reconcile(ledger, original, NOW)
        self.assertEqual(original, saved)
        self.assertEqual(ledger, before)

    def test_tampered_loaded_finding_and_stable_identity_are_rejected(self):
        ledger = self.positive()
        ledger['records'][0]['findings'][0]['value']['basis'] = 'name_only'
        with self.assertRaises(ValueError):
            build_plan(ledger, NOW)
        ledger = self.ledger()
        ledger['records'][0]['business'] = 'Different'
        with self.assertRaises(ValueError):
            build_plan(ledger, NOW)

    def test_positive_evidence_keeps_canonical_coverage_and_scoring_gates(self):
        ledger = self.positive()
        report = build_report(ledger, campaign(), NOW)
        self.assertTrue(report['records'][0]['evidence_ready'])
        self.assertEqual(report['canonical_coverage'], coverage_report(campaign()))
        self.assertEqual(report['canonical_coverage']['coverage_status'], 'INCOMPLETE')
        self.assertEqual(report['approval_batch']['status'], 'NOT_APPROVED')
        result = reconcile(ledger, campaign(), NOW)
        self.assertEqual(result['draft']['outreach'], [])
        self.assertNotIn('research_complete', result['draft']['market'][0])
        self.assertNotIn('service_scope', result['draft']['market'][0])
        self.assertTrue(result['remaining_requirements'])

    def test_reconcile_exact_facts_with_schema_shaped_traceable_sources(self):
        original = campaign()
        original['outreach'] = [{'business': 'Example', 'priority': 'B', 'ready_to_email': 'REVIEW'}]
        result = reconcile(self.positive(new_ledger(original, ['Example'], NOW)), original, NOW)
        record = result['draft']['outreach'][0]
        self.assertEqual(record['company_number'], '00000001')
        self.assertEqual(record['company_status'], 'Active')
        self.assertEqual(record['contact_email'], 'info@example.test')
        self.assertEqual(result['draft']['run']['date'], '2026-09-01')
        self.assertEqual(result['draft']['market'], original['market'])
        self.assertTrue(record['evidence_source_ids'])
        for source in result['draft']['sources']:
            self.assertEqual(set(source), {'source_id', 'business', 'publisher', 'fact_supported', 'url', 'access_date'})
            self.assertRegex(source['source_id'], r'^S[0-9]{3,}$')
            self.assertIn('finding=', source['fact_supported'])
        encoded = json.dumps(result['draft'], sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
        self.assertEqual(result['approval_batch']['draft_sha256'], hashlib.sha256(encoded).hexdigest())

    def test_unsupported_existing_positive_facts_are_conflicts(self):
        original = campaign()
        original['market'][0].update({'company_number': '99999999', 'contact_email': 'old@example.test'})
        ledger = self.positive(new_ledger(original, ['Example'], NOW))
        result = reconcile(ledger, original, NOW)
        self.assertEqual(result['draft']['market'][0]['company_number'], '99999999')
        self.assertEqual(result['draft']['market'][0]['contact_email'], 'old@example.test')
        self.assertTrue(result['conflicts'])
        self.assertFalse(build_report(ledger, original, NOW)['records'][0]['evidence_ready'])

    def test_fingerprint_mismatch_and_invalid_now_are_rejected(self):
        other = campaign()
        other['run']['date'] = '2026-09-03'
        with self.assertRaises(ValueError):
            reconcile(self.ledger(), other, NOW)
        with self.assertRaises(ValueError):
            build_plan(self.ledger(), '2026-09-03T12:00:00')

    def test_placeholder_and_telemetry_addresses_are_not_business_contacts(self):
        for email in ['example@mysite.com', 'user@domain.com', 'abcd@sentry.io', 'abc@wixpress.com']:
            item = finding('contact_route', {**CONTACT, 'email': email})
            item['sources'][0]['excerpt'] = 'Contact ' + email
            with self.assertRaises(ValueError):
                add_finding(self.ledger(), 'Example', item, NOW)

    def test_published_gmail_is_allowed_and_company_name_address_is_corroborated(self):
        item = finding('contact_route', {**CONTACT, 'email': 'synthetictrade@gmail.com'})
        item['sources'][0]['excerpt'] = 'Email us synthetictrade@gmail.com'
        ledger = add_finding(self.ledger(), 'Example', item, NOW)
        self.assertNotIn('contact_route', build_plan(ledger, NOW)['records'][0]['pending'])
        item = finding('legal_identity', {**LEGAL, 'basis': 'corroborated_name_address', 'address': '1 Sample Lane'})
        for source in item['sources']:
            source['excerpt'] += ' Example Ltd 1 Sample Lane'
        ledger = add_finding(ledger, 'Example', item, NOW)
        self.assertNotIn('legal_identity', build_plan(ledger, NOW)['records'][0]['pending'])

    def test_untrusted_legal_entity_or_completion_flag_is_reported_not_overwritten(self):
        original = campaign()
        original['outreach'] = [{'business': 'Example', 'legal_entity': 'Wrong corporate type', 'research_complete': 'YES'}]
        result = reconcile(new_ledger(original, ['Example'], NOW), original, NOW)
        self.assertIn('legal_entity', [c['field'] for c in result['conflicts']])
        self.assertIn('research_complete', [c['field'] for c in result['conflicts']])

    def test_registry_only_owner_or_locality_cannot_be_verified(self):
        for req, value in [('decision_maker', {'name': 'Synthetic Owner', 'operational': True}), ('geography', {'local': True})]:
            item = finding(req, value)
            item['sources'] = finding('active_company', ACTIVE)['sources'][1:]
            with self.assertRaises(ValueError):
                add_finding(self.ledger(), 'Example', item, NOW)

    def test_number_and_email_must_match_whole_published_tokens(self):
        for req, value, bad_excerpt in [('legal_identity', LEGAL, 'Example Ltd 100000001'),
                                        ('contact_route', CONTACT, 'Contact xinfo@example.test')]:
            item = finding(req, value)
            item['sources'][0]['excerpt'] = bad_excerpt
            with self.assertRaises(ValueError):
                add_finding(self.ledger(), 'Example', item, NOW)

    def test_active_status_cannot_match_inactive_or_wrong_registry_url(self):
        for field, value in [('excerpt', '00000001 inactive limited company'),
                             ('url', 'https://find-and-update.company-information.service.gov.uk/company/99999999')]:
            item = finding('active_company', ACTIVE)
            item['sources'][1][field] = value
            with self.assertRaises(ValueError):
                add_finding(self.ledger(), 'Example', item, NOW)

    def test_planning_cannot_precede_recorded_evidence(self):
        ledger = add_finding(self.ledger(), 'Example', finding('services', {'relevant': True}, at=LATER), LATER)
        with self.assertRaises(ValueError):
            build_plan(ledger, NOW)

    def test_loaded_semantics_are_checked_even_with_recomputed_integrity(self):
        ledger = self.positive()
        ledger['records'][0]['findings'][0]['value']['basis'] = 'name_only'
        ledger.pop('integrity_sha256')
        ledger['integrity_sha256'] = hashlib.sha256(json.dumps(ledger, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
        with self.assertRaises(ValueError):
            build_plan(ledger, NOW)

    def test_same_utc_day_is_required_across_timezone_offsets(self):
        ledger = self.positive()
        row = build_plan(ledger, '2026-09-04T00:30:00+02:00')['records'][0]
        self.assertNotIn('contact_route', row['pending'])
        row = build_plan(ledger, '2026-09-03T23:30:00-02:00')['records'][0]
        self.assertIn('contact_route', row['pending'])

    def test_market_only_reconciliation_keeps_strict_shape(self):
        original = campaign()
        result = reconcile(self.positive(), original, NOW)
        self.assertEqual(result['draft'], original)
        self.assertIn('sidecar', result['remaining_requirements'][0]['reason'])


class BudgetTests(unittest.TestCase):
    def ledger(self):
        return new_ledger(campaign(), ['Example'], NOW)

    def reserve(self, ledger, identifier='r1', seconds=20, **extra):
        return record_attempt(ledger, 'Example', {'action': 'reserve', 'id': identifier,
            'at': NOW, 'kind': 'search', 'query': 'synthetic business', 'seconds': seconds, **extra})

    def complete(self, ledger, identifier='r1', seconds=10, outcome='success'):
        return record_attempt(ledger, 'Example', {'action': 'complete', 'id': identifier,
            'at': NOW, 'seconds': seconds, 'outcome': outcome})

    def test_reservation_survives_resume_and_blocks_next_action(self):
        ledger = self.reserve(self.ledger())
        loaded = json.loads(json.dumps(ledger))
        row = build_plan(loaded, NOW)['records'][0]
        self.assertEqual(row['budget']['requests'], 1)
        self.assertEqual(row['budget']['seconds'], 20)
        self.assertFalse(row['can_request'])
        with self.assertRaises(ValueError):
            self.reserve(loaded, 'r2')
        done = self.complete(loaded)
        self.assertEqual(build_plan(done, NOW)['records'][0]['budget']['seconds'], 10)
        self.assertEqual(len(done['records'][0]['attempts']), 2)

    def test_request_limit_counts_searches_failures_and_no_reset_on_resume(self):
        ledger = self.ledger()
        for i in range(12):
            ledger = self.complete(self.reserve(ledger, str(i), 1, query='synthetic query ' + str(i)), str(i), 1, 'access_error')
        self.assertEqual(build_plan(ledger, TOMORROW)['records'][0]['budget']['requests'], 12)
        with self.assertRaises(ValueError):
            self.reserve(ledger, 'extra')

    def test_time_limit_and_nonfinite_negative_values_are_rejected(self):
        for seconds in [-1, float('nan'), float('inf'), True, 301]:
            with self.assertRaises(ValueError):
                self.reserve(self.ledger(), seconds=seconds)
        ledger = self.complete(self.reserve(self.ledger(), seconds=300), seconds=300)
        with self.assertRaises(ValueError):
            self.reserve(ledger, 'more', seconds=1)

    def test_completion_preserves_overrun_and_blocks_more_work(self):
        ledger = self.reserve(self.ledger())
        overrun = self.complete(ledger, seconds=301)
        row = build_plan(overrun, NOW)['records'][0]
        self.assertEqual(row['budget']['seconds'], 301)
        self.assertTrue(row['budget']['overrun'])
        self.assertFalse(row['can_request'])
        with self.assertRaises(ValueError):
            self.reserve(overrun, 'next')

    def test_interrupted_work_cannot_underreport_reserved_time(self):
        ledger = self.reserve(self.ledger())
        done = self.complete(ledger, seconds=20, outcome='interrupted')
        self.assertEqual(build_plan(done, NOW)['records'][0]['budget']['seconds'], 20)
        with self.assertRaises(ValueError):
            self.complete(ledger, seconds=1, outcome='interrupted')

    def test_two_transient_retries_maximum_and_auth_failures_not_retryable(self):
        ledger = self.complete(self.reserve(self.ledger()), outcome='transient_error')
        ledger = self.complete(self.reserve(ledger, 'r2', retry_of='r1'), 'r2', outcome='transient_error')
        ledger = self.complete(self.reserve(ledger, 'r3', retry_of='r2'), 'r3', outcome='transient_error')
        with self.assertRaises(ValueError):
            self.reserve(ledger, 'r4', retry_of='r3')
        blocked = self.complete(self.reserve(self.ledger()), outcome='auth_error')
        with self.assertRaises(ValueError):
            self.reserve(blocked, 'r2', retry_of='r1')

    def test_cache_reads_do_not_use_requests_and_findings_are_historical(self):
        ledger = add_finding(self.ledger(), 'Example', finding('services', {'relevant': True}), NOW)
        self.assertEqual(build_plan(ledger, NOW)['records'][0]['budget']['requests'], 0)
        ledger = self.complete(self.reserve(ledger, kind='cache'), seconds=10)
        self.assertEqual(build_plan(ledger, NOW)['records'][0]['budget']['requests'], 0)
        ledger = self.complete(self.reserve(ledger, 'cache-2', kind='cache'), 'cache-2', seconds=10)
        self.assertEqual(build_plan(ledger, NOW)['records'][0]['budget']['requests'], 0)
        self.assertEqual(build_plan(ledger, NOW)['records'][0]['budget']['seconds'], 20)

    def test_tampered_loaded_attempts_are_revalidated(self):
        ledger = self.reserve(self.ledger())
        ledger['records'][0]['attempts'][0]['seconds'] = -100
        with self.assertRaises(ValueError):
            build_plan(ledger, NOW)

    def test_missing_email_parking_does_not_require_owner_and_reopen_is_explicit(self):
        ledger = park(self.ledger(), 'Example', 'Published email unavailable', NOW)
        row = build_plan(ledger, NOW)['records'][0]
        self.assertFalse(row['can_request'])
        exceptions = build_report(ledger, campaign(), NOW)['exceptions']
        contact = next(x for x in exceptions if x['requirement'] == 'contact_route')
        self.assertEqual(contact['next_actor'], 'external-information')
        with self.assertRaises(ValueError):
            reopen(ledger, 'Example', 'unchanged', '', NOW)
        reopened = reopen(ledger, 'Example', 'budget_reset', 'Explicit research reset after operator review', NOW)
        self.assertTrue(build_plan(reopened, NOW)['records'][0]['can_request'])

    def test_new_evidence_reopen_does_not_reset_consumed_budget(self):
        ledger = self.complete(self.reserve(self.ledger()))
        ledger = park(ledger, 'Example', 'No published route', NOW)
        with self.assertRaises(ValueError):
            reopen(ledger, 'Example', 'new_evidence', 'No finding added', NOW)
        ledger = add_finding(ledger, 'Example', finding('contact_route', CONTACT), NOW)
        reopened = reopen(ledger, 'Example', 'new_evidence', 'Published contact supplied', NOW)
        self.assertEqual(build_plan(reopened, NOW)['records'][0]['budget']['requests'], 1)

    def test_resume_cannot_repeat_a_request_or_disguise_retry(self):
        for outcome in ['success', 'transient_error', 'auth_error', 'access_error']:
            ledger = self.complete(self.reserve(self.ledger()), outcome=outcome)
            with self.assertRaises(ValueError):
                self.reserve(ledger, 'repeat')

    def test_explicit_reset_preserves_history_and_resets_only_future_budget(self):
        ledger = self.complete(self.reserve(self.ledger()))
        ledger = park(ledger, 'Example', 'Research paused', NOW)
        ledger = reopen(ledger, 'Example', 'budget_reset', 'Explicit operator reset', NOW)
        row = build_plan(ledger, NOW)['records'][0]
        self.assertEqual(row['budget']['requests'], 0)
        self.assertEqual(len(ledger['records'][0]['attempts']), 2)

    def test_auth_failure_is_an_operational_exception_not_absence(self):
        ledger = self.complete(self.reserve(self.ledger()), outcome='auth_error')
        report = build_report(ledger, campaign(), NOW)
        self.assertIn('operational_failure', [e.get('kind') for e in report['exceptions']])
        self.assertEqual(report['records'][0]['requirements']['contact_route']['state'], 'MISSING')

    def test_retry_wait_must_fit_reserved_time_and_budget(self):
        ledger = self.complete(self.reserve(self.ledger()), outcome='transient_error')
        with self.assertRaises(ValueError):
            self.reserve(ledger, 'retry', seconds=20, retry_of='r1', retry_after_seconds=30)

    def test_pending_reservation_cannot_be_erased_by_reopen(self):
        ledger = self.reserve(self.ledger())
        with self.assertRaises(ValueError):
            park(ledger, 'Example', 'Reset please', NOW)

    def test_parking_and_planning_preserve_attempts_and_inputs(self):
        ledger = self.reserve(self.ledger())
        original = copy.deepcopy(ledger)
        self.complete(ledger)
        self.assertEqual(ledger, original)
        done = self.complete(ledger)
        original = copy.deepcopy(done)
        parked = park(done, 'Example', 'No further evidence', NOW)
        reopen(parked, 'Example', 'changed_input', 'New business site URL supplied for research', NOW)
        self.assertEqual(done, original)

    def test_loaded_attempt_semantics_are_checked_even_after_rehash(self):
        ledger = self.reserve(self.ledger())
        ledger['records'][0]['attempts'][0]['seconds'] = -1
        ledger.pop('integrity_sha256')
        ledger['integrity_sha256'] = hashlib.sha256(json.dumps(ledger, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
        with self.assertRaises(ValueError):
            build_plan(ledger, NOW)

    def test_explicit_changed_input_reopen_allows_refresh_without_budget_reset(self):
        ledger = self.complete(self.reserve(self.ledger()))
        ledger = park(ledger, 'Example', 'No source update yet', NOW)
        ledger = reopen(ledger, 'Example', 'changed_input', 'Business published an updated contact page', NOW)
        ledger = self.complete(self.reserve(ledger, 'refresh'), 'refresh')
        self.assertEqual(build_plan(ledger, NOW)['records'][0]['budget']['requests'], 2)

    def test_freshness_reopen_requires_stale_evidence(self):
        ledger = add_finding(self.ledger(), 'Example', finding('contact_route', CONTACT), NOW)
        ledger = park(ledger, 'Example', 'Review tomorrow', NOW)
        with self.assertRaises(ValueError):
            reopen(ledger, 'Example', 'freshness', 'Not actually stale', NOW)
        ledger = reopen(ledger, 'Example', 'freshness', 'Same-day mutable facts now need refresh', TOMORROW)
        self.assertTrue(build_plan(ledger, TOMORROW)['records'][0]['can_request'])


class CliTests(unittest.TestCase):
    def test_all_ledger_commands_preserve_evidence_budget_and_lifecycle(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ledger = new_ledger(campaign(), ['Example'], NOW)
            (root / 'ledger-0.json').write_text(json.dumps(ledger), encoding='utf-8')
            (root / 'finding.json').write_text(json.dumps(finding('contact_route', CONTACT)), encoding='utf-8')
            reservation = {'action': 'reserve', 'id': 'r1', 'at': NOW, 'kind': 'page', 'url': 'https://example.test/about', 'seconds': 20}
            (root / 'reserve.json').write_text(json.dumps(reservation), encoding='utf-8')
            (root / 'complete.json').write_text(json.dumps({'action': 'complete', 'id': 'r1', 'at': NOW, 'seconds': 5, 'outcome': 'success'}), encoding='utf-8')
            steps = [
                ['finding', '--finding', str(root / 'finding.json'), '--now', NOW],
                ['attempt', '--attempt', str(root / 'reserve.json')],
                ['attempt', '--attempt', str(root / 'complete.json')],
                ['park', '--reason', 'No further published information', '--now', NOW],
                ['reopen', '--reason-type', 'changed_input', '--reason', 'New website supplied', '--now', NOW],
            ]
            for index, step in enumerate(steps):
                output = root / ('ledger-' + str(index + 1) + '.json')
                result = subprocess.run([sys.executable, '-B', str(Path(__file__).with_name('review_evidence.py'))] + step +
                    ['--ledger', str(root / ('ledger-' + str(index) + '.json')), '--business', 'Example', '--out', str(output)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                ledger = json.loads(output.read_text(encoding='utf-8'))
            row = build_plan(ledger, NOW)['records'][0]
            self.assertEqual(row['budget']['requests'], 1)
            self.assertNotIn('contact_route', row['pending'])
            self.assertFalse(row['parked'])

    def test_init_plan_reconcile_and_overwrite_refusal(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'campaign.json').write_text(json.dumps(campaign()), encoding='utf-8')
            (root / 'businesses.json').write_text('["Example"]', encoding='utf-8')
            script = Path(__file__).with_name('review_evidence.py')
            base = [sys.executable, '-B', str(script)]
            args = ['init', '--campaign', str(root / 'campaign.json'), '--businesses', str(root / 'businesses.json'), '--now', NOW, '--out', str(root / 'ledger.json')]
            first = subprocess.run(base + args, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            original = (root / 'ledger.json').read_bytes()
            second = subprocess.run(base + args, capture_output=True, text=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual((root / 'ledger.json').read_bytes(), original)
            for command in ['plan', 'report', 'reconcile']:
                args = [command, '--ledger', str(root / 'ledger.json'), '--now', NOW, '--out', str(root / (command + '.json'))]
                if command != 'plan':
                    args += ['--campaign', str(root / 'campaign.json')]
                result = subprocess.run(base + args, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
