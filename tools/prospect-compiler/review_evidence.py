"""Offline evidence planner for agent-led research; no fetching, scoring or sending."""
import argparse
import copy
from datetime import datetime, timezone, timedelta
import hashlib
import json
import math
from pathlib import Path
import re
from urllib.parse import urlsplit

from qualification_coverage import build_report as canonical_report

REQUIREMENTS = ('legal_identity', 'active_company', 'services', 'geography',
                'decision_maker', 'contact_route', 'duplicate_identity')
STATES = {'VERIFIED', 'MISSING', 'CONFLICT', 'STALE', 'NOT_APPLICABLE'}
PREREQUISITES = {'legal_identity', 'active_company', 'contact_route'}
OUTCOMES = {'success', 'transient_error', 'auth_error', 'access_error',
            'unavailable', 'permanent_error', 'interrupted'}


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _time(value):
    _require(isinstance(value, str), 'Timestamp must be an aware ISO string')
    try:
        result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as exc:
        raise ValueError('Invalid ISO timestamp') from exc
    _require(result.tzinfo is not None and result.utcoffset() is not None,
             'Timestamp must include timezone')
    return result.astimezone(timezone.utc)


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def _key(name):
    _require(_text(name), 'Business must be a nonempty string')
    return ' '.join(name.split()).casefold()


def _record_id(slug, business):
    return _digest([slug, _key(business)])[:24]


def _seal(ledger):
    ledger.pop('integrity_sha256', None)
    ledger['integrity_sha256'] = _digest(ledger)
    return ledger


def _url(value):
    _require(_text(value) and not any(c.isspace() for c in value), 'Invalid source URL')
    try:
        url = urlsplit(value)
        valid = url.scheme in {'http', 'https'} and bool(url.hostname) and not url.username and not url.password
        url.port
    except ValueError as exc:
        raise ValueError('Invalid source URL') from exc
    _require(valid, 'Source URL must be absolute HTTP(S), without credentials')
    return url


def _number(value):
    return isinstance(value, str) and re.fullmatch(r'(?:[0-9]{8}|[A-Z]{2}[0-9]{6})', value) is not None


def _published(value, excerpt):
    return re.search(r'(?<![\w@.+-])' + re.escape(value.casefold()) + r'(?![\w@.+-])', excerpt.casefold()) is not None


def _finding(item, previous, created):
    _require(isinstance(item, dict), 'Finding must be an object')
    req, state, value = item.get('requirement'), item.get('state'), item.get('value')
    _require(req in REQUIREMENTS and state in STATES and isinstance(value, dict), 'Invalid requirement, state or structured value')
    for field in ('id', 'method', 'rationale', 'reviewer'):
        _require(_text(item.get(field)), 'Finding requires ' + field)
    _require(item['id'] not in previous, 'Repeated finding ID')
    at = _time(item.get('recorded_at'))
    _require(at >= created, 'Finding predates ledger creation')
    sources = item.get('sources')
    _require(isinstance(sources, list), 'Sources must be a list')
    if state in {'VERIFIED', 'CONFLICT', 'STALE'}:
        _require(bool(sources), 'Evidence state needs cited sources')
    for source in sources:
        _require(isinstance(source, dict), 'Source must be an object')
        _url(source.get('url'))
        _require(_time(source.get('retrieved_at')) <= at, 'Source timestamp is in the future')
        for field in ('excerpt', 'publisher', 'role'):
            _require(_text(source.get(field)), 'Source requires ' + field)
        _require(source['role'] in {'business', 'registry', 'independent'}, 'Invalid source role')
        if source['role'] == 'registry':
            _require(_url(source['url']).hostname in {
                'find-and-update.company-information.service.gov.uk',
                'api.company-information.service.gov.uk'}, 'Registry source must be Companies House')
    supersedes = item.get('supersedes')
    _require(isinstance(supersedes, list) and len(set(supersedes)) == len(supersedes), 'Invalid supersession IDs')
    for identifier in supersedes:
        _require(identifier in previous and previous[identifier]['requirement'] == req,
                 'Supersession must reference an earlier finding for the same requirement')
        old = previous[identifier]
        _require(at >= _time(old['recorded_at']), 'Supersession predates old finding')
        if sources and old['sources']:
            _require(min(_time(s['retrieved_at']) for s in sources) >=
                     max(_time(s['retrieved_at']) for s in old['sources']),
                     'Older evidence cannot supersede newer evidence')
    _require(not (state == 'NOT_APPLICABLE' and req in PREREQUISITES),
             'NOT_APPLICABLE cannot bypass legal, status or contact prerequisites')
    if state != 'VERIFIED':
        return
    roles = {s['role'] for s in sources}
    business_text = ' '.join(s['excerpt'] for s in sources if s['role'] == 'business').casefold()
    registry_text = ' '.join(s['excerpt'] for s in sources if s['role'] == 'registry').casefold()
    if req == 'legal_identity':
        _require(_number(value.get('company_number')) and _text(value.get('legal_name')), 'Exact company number and legal name required')
        _require({'business', 'registry'} <= roles, 'Legal identity requires business and registry sources')
        _require(_published(value['company_number'], registry_text), 'Registry excerpt must publish exact company number')
        basis = value.get('basis')
        _require(basis in {'published_number', 'corroborated_name_address'}, 'Name-only company matching is not verification')
        if basis == 'published_number':
            _require(_published(value['company_number'], business_text), 'Business excerpt must publish exact company number')
        else:
            _require(_text(value.get('address')), 'Corroborated identity needs address')
            for excerpt in (business_text, registry_text):
                _require(value['legal_name'].casefold() in excerpt and value['address'].casefold() in excerpt,
                         'Legal name and address must be corroborated in both excerpts')
    elif req == 'active_company':
        _require(_number(value.get('company_number')) and _text(value.get('status')) and
                 _text(value.get('company_type')), 'Status requires exact number, status and company type')
        _require('registry' in roles and _published(value['company_number'], registry_text) and
                 _published(value['status'], registry_text), 'Registry excerpt must support exact number and status')
        _require(any('/company/' + value['company_number'] in _url(s['url']).path for s in sources if s['role'] == 'registry'),
                 'Status registry URL must identify the exact company number')
    elif req == 'contact_route':
        email = value.get('email', '')
        _require(isinstance(email, str) and re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email), 'Valid published email required')
        _require(value.get('published') is True and 'business' in roles and _published(email, business_text),
                 'Contact must be explicitly published by the business, never guessed')
        local, domain = email.casefold().split('@')
        _require(local not in {'example', 'user', 'yourname', 'youremail', 'emailaddress'} and
                 domain not in {'domain.com', 'mysite.com', 'yourdomain.com'} and
                 not any(domain == suffix or domain.endswith('.' + suffix) for suffix in ('sentry.io', 'wixpress.com', 'sentry.wixpress.com')),
                 'Placeholder and telemetry addresses are not business contacts')
        _require(value.get('kind') in {'generic', 'named'}, 'Contact kind must be generic or named')
    elif req in {'services', 'geography', 'duplicate_identity'}:
        field = {'services': 'relevant', 'geography': 'local', 'duplicate_identity': 'duplicate'}[req]
        _require(type(value.get(field)) is bool, req + ' requires boolean ' + field)
        if req == 'geography':
            _require(roles != {'registry'}, 'Registered office alone does not establish trading geography')
    elif req == 'decision_maker':
        _require(_text(value.get('name')) and type(value.get('operational')) is bool,
                 'Decision-maker requires name and operational boolean')
        _require(roles != {'registry'}, 'Directorship alone does not establish operational ownership')


def _seconds(value):
    _require(type(value) in (int, float) and math.isfinite(value) and value >= 0,
             'Seconds must be finite and nonnegative')
    return value


def _account(attempts, start=0, repeat_start=0):
    requests = seconds = retries = 0
    overrun = False
    reservations, completions = {}, {}
    targets = set()
    for index, item in enumerate(attempts):
        _require(isinstance(item, dict) and _text(item.get('id')), 'Attempt needs ID')
        _time(item.get('at'))
        amount = _seconds(item.get('seconds'))
        identifier, action = item['id'], item.get('action')
        if action == 'reserve':
            if index >= start:
                _require(not overrun, 'Time allowance overrun requires explicit review/reset')
            _require(not (reservations.keys() - completions.keys()), 'Pending reservation blocks another action')
            _require(identifier not in reservations, 'Attempt ID already reserved')
            _require(item.get('kind') in {'search', 'page', 'api', 'cache'}, 'Invalid request kind')
            _require(amount > 0, 'Reserve a positive time allowance before acting')
            target = item.get('query') if item['kind'] == 'search' else item.get('url', item.get('query'))
            _require(_text(target), 'Attempt needs search query or source URL')
            if item['kind'] in {'page', 'api'} or item.get('url'):
                _url(target)
            retry = item.get('retry_of')
            if retry:
                wait = _seconds(item.get('retry_after_seconds', 0))
                _require(wait <= amount, 'Retry wait exceeds reserved time; defer request')
                _require(retry in completions and completions[retry]['outcome'] == 'transient_error',
                         'Only transient failures may be retried')
                old = reservations[retry]
                _require(item['kind'] == old['kind'] and item.get('query') == old.get('query') and
                         item.get('url') == old.get('url'), 'Retry must target the original request')
                _require(not any(r.get('retry_of') == retry for r in reservations.values()), 'Failure already retried')
            signature = (item['kind'], target)
            if index >= repeat_start and item['kind'] != 'cache':
                _require(retry or signature not in targets, 'Unchanged request already attempted; reuse evidence or explicitly reopen')
                targets.add(signature)
            if index >= start:
                requests += item['kind'] != 'cache'
                seconds += amount
                retries += bool(retry)
                _require(requests <= 12 and seconds <= 300 and retries <= 2, 'Research budget exhausted')
            reservations[identifier] = item
        elif action == 'complete':
            _require(identifier in reservations and identifier not in completions, 'Completion needs pending reservation')
            reserved = reservations[identifier]
            _require(_time(item['at']) >= _time(reserved['at']), 'Completion predates reservation')
            _require(item.get('outcome') in OUTCOMES, 'Invalid completion outcome')
            if item['outcome'] == 'interrupted':
                _require(amount >= reserved['seconds'], 'Interrupted work consumes at least the full reservation')
            if index >= start:
                seconds += amount - reserved['seconds']
                overrun = overrun or amount > reserved['seconds'] or seconds > 300
            completions[identifier] = item
        else:
            raise ValueError('Attempt action must be reserve or complete')
    return {'requests': requests, 'seconds': seconds, 'retries': retries,
            'pending_reservations': sorted(reservations.keys() - completions.keys()), 'overrun': overrun}


def _validate(ledger):
    _require(isinstance(ledger, dict) and ledger.get('version') == 1, 'Unsupported evidence ledger version')
    snapshot = copy.deepcopy(ledger)
    digest = snapshot.pop('integrity_sha256', None)
    _require(digest == _digest(snapshot), 'Ledger integrity mismatch; use append-only API, not manual edits')
    _require(_text(ledger.get('campaign_slug')) and re.fullmatch('[a-f0-9]{64}', ledger.get('campaign_sha256', '')),
             'Invalid campaign identity')
    created = _time(ledger.get('created_at'))
    _require(isinstance(ledger.get('records'), list), 'Ledger records must be a list')
    ids = set()
    for record in ledger['records']:
        _require(record.get('id') == _record_id(ledger['campaign_slug'], record.get('business')) and record['id'] not in ids,
                 'Invalid or duplicate stable business identity')
        ids.add(record['id'])
        previous = {}
        for item in record['findings']:
            _finding(item, previous, created)
            previous[item['id']] = item
        start = repeat_start = 0
        parked = False
        for event in record['events']:
            _require(_text(event.get('reason')), 'Lifecycle event needs reason')
            _require(_time(event.get('at')) >= created, 'Lifecycle event predates ledger')
            position = event.get('attempt_count')
            _require(type(position) is int and start <= position <= len(record['attempts']), 'Invalid lifecycle attempt position')
            account = _account(record['attempts'][:position], start, repeat_start)
            _require(not account['pending_reservations'], 'Reconcile pending reservation before parking or reopening')
            if event.get('action') == 'park':
                _require(not parked, 'Record already parked')
                parked = True
            elif event.get('action') == 'reopen':
                _require(parked and event.get('reason_type') in {'new_evidence', 'changed_input', 'freshness', 'budget_reset'}, 'Invalid reopen event')
                parked = False
                repeat_start = position
                if event['reason_type'] == 'budget_reset':
                    start = position
            else:
                raise ValueError('Invalid lifecycle action')
        _account(record['attempts'], start, repeat_start)
    return ledger


def _record(ledger, business):
    matches = [r for r in ledger['records'] if r['id'] == business or _key(r['business']) == _key(business)]
    _require(len(matches) == 1, 'Business is not uniquely present in ledger')
    return matches[0]


def _copy(ledger):
    _validate(ledger)
    return copy.deepcopy(ledger)


def new_ledger(campaign, businesses, now):
    """Create an unapproved sidecar; prior notes remain leads, not evidence."""
    _time(now)
    slug = campaign.get('run', {}).get('campaign_slug')
    _require(_text(slug), 'Campaign slug required')
    _require(isinstance(businesses, list) and bool(businesses), 'Supply selected census business names')
    records = [{'id': _record_id(slug, name), 'business': name, 'findings': [],
                'attempts': [], 'events': []} for name in businesses]
    ledger = _seal({'version': 1, 'campaign_slug': slug, 'campaign_sha256': _digest(campaign),
                    'created_at': now, 'records': records})
    _validate(ledger)
    return ledger


def add_finding(ledger, business, finding, now):
    """Append cited assessment, including historical evidence, without billing a request."""
    result = _copy(ledger)
    record = _record(result, business)
    item = copy.deepcopy(finding)
    item.setdefault('id', record['id'] + '-f' + str(len(record['findings']) + 1))
    item['recorded_at'] = now
    item.setdefault('supersedes', [])
    record['findings'].append(item)
    _seal(result)
    _validate(result)
    return result


def _lifecycle(record):
    parked, start, repeat_start = False, 0, 0
    for event in record['events']:
        parked = event['action'] == 'park'
        if event['action'] == 'reopen':
            repeat_start = event['attempt_count']
        if event.get('reason_type') == 'budget_reset':
            start = event['attempt_count']
    return parked, start, repeat_start


def record_attempt(ledger, business, attempt):
    """Reserve durably before an external action; append completion afterward."""
    result = _copy(ledger)
    record = _record(result, business)
    _require(_time(attempt.get('at')) >= _time(result['created_at']), 'Attempt predates ledger')
    if attempt.get('action') == 'reserve':
        _require(not _lifecycle(record)[0], 'Parked record requires explicit reopening')
    record['attempts'].append(copy.deepcopy(attempt))
    _seal(result)
    _validate(result)
    return result


def _assess(record, requirement, now):
    items = [f for f in record['findings'] if f['requirement'] == requirement]
    superseded = {identifier for f in items for identifier in f['supersedes']}
    items = [f for f in items if f['id'] not in superseded]
    if not items:
        return {'state': 'MISSING', 'reason': 'No cited assessment for ' + requirement, 'value': {}, 'finding_ids': []}
    ids = [f['id'] for f in items]
    verified = [f for f in items if f['state'] == 'VERIFIED']
    if any(f['state'] == 'CONFLICT' for f in items) or len({_digest(f['value']) for f in verified}) > 1:
        return {'state': 'CONFLICT', 'reason': 'Unresolved contradictory evidence; explicit supersession required', 'value': {}, 'finding_ids': ids}
    # A newer unresolved assessment cannot be hidden by older positive evidence.
    item = max(items, key=lambda f: (_time(f['recorded_at']), items.index(f)))
    if verified and item['state'] != 'VERIFIED':
        state = 'CONFLICT'
    else:
        state = item['state']
    if state == 'VERIFIED':
        retrieved = min(_time(s['retrieved_at']) for s in item['sources'])
        reusable = (now - retrieved <= timedelta(days=30) if requirement in {'services', 'geography'}
                    else now.date() == retrieved.date())
        if not reusable:
            state = 'STALE'
    return {'state': state, 'reason': ('Evidence freshness check required' if state == 'STALE' else item['rationale']),
            'value': copy.deepcopy(item['value']), 'finding_ids': ids}


def _positive(req, assessment):
    if assessment['state'] == 'NOT_APPLICABLE':
        return req not in PREREQUISITES
    if assessment['state'] != 'VERIFIED':
        return False
    value = assessment['value']
    if req == 'active_company':
        return value['status'].casefold() == 'active' and value['company_type'] in {'ltd', 'llp'}
    if req == 'services':
        return value['relevant']
    if req == 'geography':
        return value['local']
    if req == 'decision_maker':
        return value['operational']
    if req == 'duplicate_identity':
        return not value['duplicate']
    return True


def build_plan(ledger, now):
    """Describe only outstanding facts/actions. This function never requests anything."""
    _validate(ledger)
    current = _time(now)
    _require(current >= _time(ledger['created_at']), 'Planning time predates ledger')
    rows = []
    for record in ledger['records']:
        timestamps = [f['recorded_at'] for f in record['findings']] + [a['at'] for a in record['attempts']] + [e['at'] for e in record['events']]
        _require(all(_time(at) <= current for at in timestamps), 'Planning time predates recorded history')
        assessments = {req: _assess(record, req, current) for req in REQUIREMENTS}
        legal, status = assessments['legal_identity'], assessments['active_company']
        if status['state'] == 'VERIFIED' and (legal['state'] != 'VERIFIED' or
                legal['value'].get('company_number') != status['value'].get('company_number')):
            status.update(state='CONFLICT', reason='Active status must agree with a verified exact legal company number')
        pending = [req for req, a in assessments.items() if a['state'] not in {'VERIFIED', 'NOT_APPLICABLE'}]
        parked, start, repeat_start = _lifecycle(record)
        budget = _account(record['attempts'], start, repeat_start)
        can_request = bool(pending) and not parked and not budget['overrun'] and not budget['pending_reservations'] and budget['requests'] < 12 and budget['seconds'] < 300
        rows.append({'id': record['id'], 'business': record['business'], 'pending': pending,
                     'requirements': assessments, 'budget': budget, 'parked': parked,
                     'can_request': can_request,
                     'evidence_ready': all(_positive(req, a) for req, a in assessments.items())})
    return {'campaign_slug': ledger['campaign_slug'], 'as_of': now, 'records': rows,
            'notice': 'Agent-led research planner only; no external requests, scoring, qualification or approval performed.'}


def park(ledger, business, reason, now):
    result = _copy(ledger)
    record = _record(result, business)
    record['events'].append({'action': 'park', 'reason': reason, 'at': now,
                             'attempt_count': len(record['attempts']), 'finding_count': len(record['findings'])})
    _seal(result)
    _validate(result)
    return result


def reopen(ledger, business, reason_type, reason, now):
    result = _copy(ledger)
    record = _record(result, business)
    _require(_lifecycle(record)[0], 'Only parked records can be reopened')
    if reason_type == 'new_evidence':
        _require(len(record['findings']) > record['events'][-1]['finding_count'], 'New evidence must be appended before reopening')
    if reason_type == 'freshness':
        row = next(r for r in build_plan(result, now)['records'] if r['id'] == record['id'])
        _require(any(a['state'] == 'STALE' for a in row['requirements'].values()), 'No due freshness check')
    record['events'].append({'action': 'reopen', 'reason_type': reason_type, 'reason': reason,
                             'at': now, 'attempt_count': len(record['attempts']),
                             'finding_count': len(record['findings'])})
    _seal(result)
    _validate(result)
    return result


def _match_campaign(ledger, campaign):
    _require(_digest(campaign) == ledger['campaign_sha256'], 'Campaign fingerprint mismatch; preserve original campaign input')


def _approval(draft, original):
    return {'status': 'NOT_APPROVED', 'draft_sha256': _digest(draft),
            'proposed': [{'business': r.get('business'), 'priority': r.get('priority'),
                          'ready_to_email': r.get('ready_to_email')} for r in original.get('outreach', [])]}


def _proposals(row):
    assessments = row['requirements']
    result = {}
    legal, status, contact = (assessments[r] for r in ('legal_identity', 'active_company', 'contact_route'))
    if _positive('legal_identity', legal) and _positive('active_company', status):
        result['company_number'] = ('legal_identity', legal['value']['company_number'])
        result['company_status'] = ('active_company', 'Active')
        result['legal_entity'] = ('active_company', 'Private limited company' if status['value']['company_type'] == 'ltd' else 'Limited liability partnership')
    if _positive('contact_route', contact):
        result['contact_email'] = ('contact_route', contact['value']['email'])
    return result


def reconcile(ledger, campaign, now):
    """Return a new draft envelope. Only existing outreach rows accept reconciled fields."""
    plan = build_plan(ledger, now)
    _match_campaign(ledger, campaign)
    draft, conflicts, remaining = copy.deepcopy(campaign), [], []
    source_ids = {s.get('source_id') for s in draft.get('sources', [])}
    for row in plan['records']:
        record = _record(ledger, row['id'])
        proposals = _proposals(row)
        matches = [(section, r) for section in ('market', 'outreach', 'excluded')
                   for r in draft.get(section, []) if _key(r.get('business', '')) == _key(row['business'])]
        conflicting_requirements = set()
        for section, target in matches:
            for field, req in [('company_number', 'legal_identity'), ('company_status', 'active_company'), ('legal_entity', 'active_company'),
                               ('contact_email', 'contact_route')]:
                old = target.get(field)
                if old and old != '[PLACEHOLDER]' and (field not in proposals or str(old).casefold() != str(proposals[field][1]).casefold()):
                    conflicts.append({'business': row['business'], 'requirement': req, 'field': field,
                                      'reason': 'Existing canonical fact is unsupported or conflicts with current evidence', 'next_actor': 'agent'})
                    conflicting_requirements.add(req)
            for field in ('research_complete', 'business_verified', 'contact_route_verified', 'eligible_for_outreach'):
                if target.get(field) == 'YES' and not row['evidence_ready']:
                    conflicts.append({'business': row['business'], 'requirement': 'canonical_scoring', 'field': field,
                                      'reason': 'Existing positive gate needs evidence-backed canonical scoring review', 'next_actor': 'agent'})
        if {'legal_identity', 'active_company'} & conflicting_requirements:
            conflicting_requirements.update({'legal_identity', 'active_company'})
        targets = [r for section, r in matches if section == 'outreach']
        if len(targets) > 1:
            conflicts.append({'business': row['business'], 'requirement': 'duplicate_identity',
                              'reason': 'Multiple outreach rows require identity resolution', 'next_actor': 'agent'})
            targets = []
        for target in targets:
            for field, (req, value) in proposals.items():
                if req in conflicting_requirements:
                    continue
                target[field] = value
                for finding_id in row['requirements'][req]['finding_ids']:
                    item = next(f for f in record['findings'] if f['id'] == finding_id)
                    for i, source in enumerate(item['sources']):
                        marker = 'finding=' + finding_id + '; ' + req + '; ' + source['excerpt']
                        existing = next((s for s in draft.get('sources', []) if s.get('business') == row['business'] and s.get('fact_supported') == marker and s.get('url') == source['url']), None)
                        source_id = existing['source_id'] if existing else 'S' + str(max([int(s[1:]) for s in source_ids if isinstance(s, str) and re.fullmatch(r'S[0-9]+', s)] + [0]) + 1).zfill(3)
                        if not existing:
                            draft.setdefault('sources', []).append({'source_id': source_id, 'business': row['business'],
                                'publisher': source['publisher'], 'fact_supported': marker,
                                'url': source['url'], 'access_date': _time(source['retrieved_at']).date().isoformat()})
                            source_ids.add(source_id)
                        if source_id not in target.setdefault('evidence_source_ids', []):
                            target['evidence_source_ids'].append(source_id)
        remaining.append({'business': row['business'], 'requirements': row['pending'],
                          'next_actor': 'agent', 'reason': 'Existing scoring rubric, canonical reconciliation and strict validation remain required; no scores or completion gates were generated.' +
                          (' No unique existing outreach row; verified facts remain in the sidecar.' if not targets else '')})
    return {'draft': draft, 'conflicts': conflicts, 'remaining_requirements': remaining,
            'approval_batch': _approval(draft, campaign)}


def build_report(ledger, campaign, now):
    """Separate review attempts/exceptions from unchanged authoritative coverage."""
    plan = build_plan(ledger, now)
    reconciled = reconcile(ledger, campaign, now)
    exceptions = copy.deepcopy(reconciled['conflicts'])
    for row in plan['records']:
        record = _record(ledger, row['id'])
        for attempt in record['attempts']:
            if attempt['action'] == 'complete' and attempt['outcome'] != 'success':
                exceptions.append({'business': row['business'], 'kind': 'operational_failure',
                    'requirement': 'research_access', 'attempt_id': attempt['id'],
                    'reason': attempt['outcome'], 'next_actor': 'agent' if attempt['outcome'] == 'transient_error' and row['can_request'] else 'external-information'})
        if row['budget']['overrun'] or row['budget']['pending_reservations']:
            exceptions.append({'business': row['business'], 'kind': 'operational_failure',
                'requirement': 'research_budget', 'reason': 'Reconcile pending reservation or review recorded time overrun', 'next_actor': 'agent'})
        for req, assessment in row['requirements'].items():
            if not _positive(req, assessment):
                exceptions.append({'business': row['business'], 'requirement': req, 'state': assessment['state'],
                    'reason': assessment['reason'], 'next_actor': 'agent' if row['can_request'] else 'external-information',
                    'resolution': 'Supply current cited facts or explicitly resolve contradictory findings; owner approval cannot verify missing facts.',
                    'attempts': copy.deepcopy(record['attempts'])})
        if any(c['business'] == row['business'] for c in reconciled['conflicts']):
            row['evidence_ready'] = False
    return {**plan, 'exceptions': exceptions,
            'attempt_completion': 'COMPLETE' if all(r['parked'] or r['evidence_ready'] for r in plan['records']) else 'INCOMPLETE',
            'canonical_coverage': canonical_report(campaign),
            'remaining_requirements': reconciled['remaining_requirements'],
            'approval_batch': {**reconciled['approval_batch'], 'next_actor': 'owner-policy'},
            'notice': 'Attempt completion is not qualification completion. Missing email is not an owner approval request. Approval binds only to the exact draft digest.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    for name in ('init', 'finding', 'attempt', 'plan', 'report', 'reconcile', 'park', 'reopen'):
        command = commands.add_parser(name)
        command.add_argument('--out', required=True)
        if name != 'attempt':
            command.add_argument('--now', required=True)
        if name != 'init':
            command.add_argument('--ledger', required=True)
        if name in {'init', 'report', 'reconcile'}:
            command.add_argument('--campaign', required=True)
        if name == 'init':
            command.add_argument('--businesses', required=True, help='JSON list of selected census business names')
        if name in {'finding', 'attempt', 'park', 'reopen'}:
            command.add_argument('--business', required=True)
        if name in {'finding', 'attempt'}:
            command.add_argument('--' + name, required=True, help='JSON input file')
        if name in {'park', 'reopen'}:
            command.add_argument('--reason', required=True)
        if name == 'reopen':
            command.add_argument('--reason-type', required=True)
    args = parser.parse_args(argv)
    def load(path):
        return json.loads(Path(path).read_text(encoding='utf-8-sig'))
    try:
        _require(not Path(args.out).exists(), 'Output already exists; choose a new path')
        if args.command == 'init':
            result = new_ledger(load(args.campaign), load(args.businesses), args.now)
        else:
            ledger = load(args.ledger)
            if args.command == 'finding':
                result = add_finding(ledger, args.business, load(args.finding), args.now)
            elif args.command == 'attempt':
                result = record_attempt(ledger, args.business, load(args.attempt))
            elif args.command == 'plan':
                result = build_plan(ledger, args.now)
            elif args.command in {'report', 'reconcile'}:
                result = globals()[args.command if args.command == 'reconcile' else 'build_report'](ledger, load(args.campaign), args.now)
            elif args.command == 'park':
                result = park(ledger, args.business, args.reason, args.now)
            else:
                result = reopen(ledger, args.business, args.reason_type, args.reason, args.now)
        serialized = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + '\n'
        with Path(args.out).open('x', encoding='utf-8') as stream:
            stream.write(serialized)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, str(exc) + '\n')


if __name__ == '__main__':
    main()
