-- Wardith CRM database schema. See README.md for the research/activity
-- separation this schema exists to enforce: prospects.* research columns
-- are overwritten wholesale on every ingest run; do_not_contact_manual and
-- notes are hand-edited and ingest never touches them; activities is an
-- append-only log ingest never writes to at all.

CREATE TABLE IF NOT EXISTS campaigns (
    campaign_id           TEXT PRIMARY KEY,
    sector                TEXT,
    geography             TEXT,
    run_date              TEXT,
    pipeline_stage        TEXT,
    market_count          INTEGER,
    outreach_count        INTEGER,
    excluded_count        INTEGER,
    source_run_csv        TEXT,
    source_campaign_json  TEXT,
    source_run_log        TEXT,
    first_imported_at     TEXT,
    last_imported_at      TEXT
);

CREATE TABLE IF NOT EXISTS prospects (
    prospect_id              TEXT PRIMARY KEY,
    campaign_id               TEXT NOT NULL REFERENCES campaigns(campaign_id),
    business_key               TEXT NOT NULL,
    business TEXT, area TEXT, website TEXT,
    priority TEXT, opportunity_type TEXT, outreach_rank INTEGER,
    accessibility TEXT, accessibility_notes TEXT,
    contact_person TEXT, role TEXT, contact_email TEXT, contact_phone TEXT,
    decision_maker_linkedin TEXT, ready_to_email TEXT,
    competitive_gap_finding TEXT, why_prospect TEXT,
    legal_entity TEXT, company_number TEXT, company_status TEXT,
    outreach_angle TEXT, email_subject TEXT, email_body TEXT, linkedin_draft TEXT,
    caveats_json TEXT,
    evidence_source_ids_json TEXT,
    source_campaign_json TEXT,
    source_outreach_prep_json TEXT,
    orphaned_outreach_prep INTEGER NOT NULL DEFAULT 0,
    withheld_at_outreach INTEGER NOT NULL DEFAULT 0,
    withheld_reason TEXT,
    -- hand-edited; never overwritten by ingest
    do_not_contact_manual INTEGER NOT NULL DEFAULT 0,
    notes TEXT NOT NULL DEFAULT '',
    first_imported_at TEXT,
    last_imported_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_prospects_campaign ON prospects(campaign_id);

CREATE TABLE IF NOT EXISTS activities (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    prospect_id    TEXT NOT NULL REFERENCES prospects(prospect_id),
    activity_type  TEXT NOT NULL,
    activity_date  TEXT NOT NULL,
    amount_gbp     REAL,
    plan           TEXT,
    notes          TEXT,
    created_at     TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_activities_prospect ON activities(prospect_id);

CREATE TABLE IF NOT EXISTS cadence_settings (
    key                  TEXT PRIMARY KEY,
    label                TEXT NOT NULL,
    next_action_label    TEXT NOT NULL,
    cadence_days         INTEGER,
    stage_label          TEXT NOT NULL,
    stops_cold_followup  INTEGER NOT NULL DEFAULT 0,
    blocks_outreach      INTEGER NOT NULL DEFAULT 0,
    is_revenue_event     INTEGER NOT NULL DEFAULT 0,
    sort_order           INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS clients (
    client_id                     INTEGER PRIMARY KEY AUTOINCREMENT,
    prospect_id                   TEXT UNIQUE REFERENCES prospects(prospect_id),
    business                      TEXT NOT NULL,
    contact_person TEXT, role TEXT, contact_email TEXT, contact_phone TEXT,
    plan_tier                     TEXT,
    audit_sold_date TEXT, audit_completed_date TEXT,
    foundation_sold_date TEXT, foundation_completed_date TEXT,
    ongoing_started_date TEXT,
    retention_deletion_due_date   TEXT,
    next_checkin_due_date         TEXT,
    do_not_contact                INTEGER NOT NULL DEFAULT 0,
    notes                         TEXT NOT NULL DEFAULT '',
    created_at                    TEXT NOT NULL,
    updated_at                    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS client_activities (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id      INTEGER NOT NULL REFERENCES clients(client_id),
    activity_type  TEXT NOT NULL,
    activity_date  TEXT NOT NULL,
    notes          TEXT,
    created_at     TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_client_activities_client ON client_activities(client_id);

CREATE TABLE IF NOT EXISTS import_log (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp  TEXT NOT NULL,
    message    TEXT NOT NULL
);
