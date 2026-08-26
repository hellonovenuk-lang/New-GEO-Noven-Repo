#!/usr/bin/env python3
"""Import completed /90qrun, /qualify and /outreach output into the CRM
database. Read-only against ~/wardith-runs/<slug>/ and
~/wardith-runs/<slug>.csv; the only writes are to the SQLite database
(default ~/wardith-runs/crm/wardith.db, see db.py).

Ported from tools/tracker/import_tracker.py: every pure record-building
function below (discover_slugs, build_campaign_record,
build_prospect_research, is_genuinely_prepared, slugify, ...) is unchanged
from that file. Only the write side changed - a SQL upsert per
campaign/prospect instead of merging into a tracker.json dict - because
tracker.json existed only so build_crm.py had one blob to render an Excel
workbook from in a single pass. That intermediate step has no equivalent
need once the target is a database queried directly at request time, and
dropping it removes a second copy of the same data that would otherwise
need its own research/activity merge rules kept in sync with these.

The two-kind-of-field rule is unchanged: prospects.* research columns are
overwritten wholesale on every ingest; activities is a separate,
append-only table this module never writes to at all (an ingest run
cannot create sales activity - only the CRM's own forms can).
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import db as db_mod

RESEARCH_FIELDS = [
    "business", "area", "website", "priority", "opportunity_type",
    "outreach_rank", "accessibility", "accessibility_notes",
    "contact_person", "role", "contact_email", "contact_phone",
    "decision_maker_linkedin", "ready_to_email", "competitive_gap_finding",
    "why_prospect", "legal_entity", "company_number", "company_status",
    "outreach_angle", "email_subject", "email_body", "linkedin_draft",
    "caveats_json", "evidence_source_ids_json",
    "source_campaign_json", "source_outreach_prep_json",
    "orphaned_outreach_prep", "withheld_at_outreach", "withheld_reason",
]


def slugify(text):
    text = text.strip().casefold()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path):
    """Returns (data, error). Tolerant of a file mid-write by a running
    /qualify or /outreach job: a decode error is reported, never raised."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f), None
    except FileNotFoundError:
        return None, None
    except json.JSONDecodeError as e:
        return None, f"{path}: could not parse ({e}) - likely mid-write, skipped"


def parse_run_log(path):
    """Pull sector/geography/date from a /90qrun run-log's own structured
    header lines. Never guesses from the slug - only reads what the skill
    already wrote down."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    out = {}
    for field, key in (("Trade", "sector"), ("Geography", "geography"), ("Date", "run_date")):
        m = re.search(rf"\*\*{field}:\*\*\s*(.+)", text)
        if m:
            out[key] = m.group(1).strip()
    return out


def discover_slugs(runs_dir):
    slugs = set()
    for csv_path in runs_dir.glob("*.csv"):
        slugs.add(csv_path.stem)
    for d in runs_dir.iterdir():
        if d.is_dir() and d.name != "crm" and d.name != "tracker":
            slugs.add(d.name)
    return sorted(slugs)


def find_outreach_prep_files(campaign_dir, slug):
    outreach_dir = campaign_dir / "outreach"
    if not outreach_dir.is_dir():
        return []
    files = sorted(outreach_dir.glob(f"outreach-prep-{slug}-*.json"))
    # Latest-dated file first, by filename (YYYY-MM-DD sorts lexically).
    return list(reversed(files))


def load_latest_outreach_prep(campaign_dir, slug, warnings):
    """Returns {slugified_business: (entry, path)}, using the most recent
    dated file's entry for a given business if more than one file exists."""
    merged = {}
    for path in find_outreach_prep_files(campaign_dir, slug):
        data, err = load_json(path)
        if err:
            warnings.append(err)
            continue
        if data is None:
            continue
        for entry in data:
            key = slugify(entry.get("business", ""))
            if key and key not in merged:
                merged[key] = (entry, path)
    return merged


def build_campaign_record(slug, runs_dir, warnings):
    campaign_dir = runs_dir / slug
    raw_csv = runs_dir / f"{slug}.csv"
    campaign_json_path = campaign_dir / f"{slug}-campaign.json"
    run_log_path = runs_dir / f"{slug}-run-log.md"

    campaign_data, err = load_json(campaign_json_path)
    if err:
        warnings.append(err)

    outreach_prep = load_latest_outreach_prep(campaign_dir, slug, warnings)

    if outreach_prep:
        stage = "OUTREACH_PREPARED"
    elif campaign_data is not None:
        stage = "QUALIFIED"
    elif raw_csv.exists():
        stage = "RESEARCHED"
    else:
        return None, {}, []

    record = {
        "campaign_id": slug,
        "sector": None,
        "geography": None,
        "run_date": None,
        "pipeline_stage": stage,
        "market_count": None,
        "outreach_count": None,
        "excluded_count": None,
        "source_run_csv": str(raw_csv) if raw_csv.exists() else None,
        "source_campaign_json": str(campaign_json_path) if campaign_data is not None else None,
        "source_run_log": None,
    }

    if campaign_data is not None:
        run = campaign_data.get("run", {})
        record["sector"] = run.get("sector")
        record["geography"] = run.get("geography")
        record["run_date"] = run.get("date")
        record["market_count"] = len(campaign_data.get("market", []))
        record["outreach_count"] = len(campaign_data.get("outreach", []))
        record["excluded_count"] = len(campaign_data.get("excluded", []))
    elif run_log_path.exists():
        parsed = parse_run_log(run_log_path)
        record["sector"] = parsed.get("sector")
        record["geography"] = parsed.get("geography")
        record["run_date"] = parsed.get("run_date")
        record["source_run_log"] = str(run_log_path)

    outreach_entries = campaign_data.get("outreach", []) if campaign_data else []
    return record, outreach_prep, outreach_entries


def is_genuinely_prepared(prep_entry):
    """True only for an outreach-prep entry that was actually drafted: not
    withheld at /outreach's own Stage 4 gate, and carrying real email copy.
    A withheld entry is recorded for its research value - contact_route,
    withheld_reason - but never marks the prospect send-ready."""
    if not prep_entry:
        return False
    if prep_entry.get("withheld") is True:
        return False
    return bool(prep_entry.get("email_body"))


def business_key_for(entry, prep_entry):
    """Prefer a verified Companies House company_number over the slugified
    business name when one is known, so a business rename doesn't silently
    create a duplicate prospect. Falls back to the slug - the only anchor
    available for the (currently near-universal) case with no company
    number yet."""
    company_number = (entry or {}).get("company_number") or (prep_entry or {}).get("company_number")
    if company_number and str(company_number).strip() and "[PLACEHOLDER]" not in str(company_number):
        return f"cn-{slugify(str(company_number))}"
    return slugify((entry or {}).get("business") or (prep_entry or {}).get("business") or "")


def build_prospect_research(entry, prep_match):
    prep_entry, prep_path = prep_match if prep_match else (None, None)
    research = {field: None for field in RESEARCH_FIELDS}
    research.update({
        "business": entry.get("business"),
        "area": entry.get("area"),
        "website": entry.get("website"),
        "priority": entry.get("priority"),
        "opportunity_type": entry.get("opportunity_type"),
        "outreach_rank": entry.get("outreach_rank"),
        "accessibility": entry.get("accessibility"),
        "accessibility_notes": entry.get("accessibility_notes"),
        "contact_person": entry.get("contact_person"),
        "role": entry.get("role"),
        "contact_email": entry.get("contact_email"),
        "contact_phone": entry.get("contact_phone"),
        "decision_maker_linkedin": entry.get("decision_maker_linkedin"),
        "ready_to_email": entry.get("ready_to_email"),
        "competitive_gap_finding": entry.get("competitive_gap_finding"),
        "why_prospect": entry.get("why_prospect"),
        "legal_entity": entry.get("legal_entity"),
        "company_number": entry.get("company_number"),
        "company_status": entry.get("company_status"),
        "evidence_source_ids_json": json.dumps(entry.get("evidence_source_ids")),
        "orphaned_outreach_prep": 0,
        "withheld_at_outreach": 0,
        "withheld_reason": None,
    })
    if prep_entry:
        contact_route = prep_entry.get("contact_route") or {}
        research["contact_person"] = contact_route.get("person") or research["contact_person"]
        research["role"] = contact_route.get("role") or research["role"]
        research["contact_email"] = contact_route.get("email") or research["contact_email"]
        research["outreach_angle"] = prep_entry.get("outreach_angle")
        research["email_subject"] = prep_entry.get("email_subject")
        research["email_body"] = prep_entry.get("email_body")
        research["linkedin_draft"] = prep_entry.get("linkedin_draft")
        research["caveats_json"] = json.dumps(prep_entry.get("caveats"))
        research["source_outreach_prep_json"] = str(prep_path)
        research["withheld_at_outreach"] = 1 if prep_entry.get("withheld") is True else 0
        research["withheld_reason"] = prep_entry.get("withheld_reason")
    return research


def get_campaign(conn, campaign_id):
    row = conn.execute("SELECT * FROM campaigns WHERE campaign_id = ?", (campaign_id,)).fetchone()
    return dict(row) if row else None


def get_prospect(conn, prospect_id):
    row = conn.execute("SELECT * FROM prospects WHERE prospect_id = ?", (prospect_id,)).fetchone()
    return dict(row) if row else None


def is_superseded(conn, slug, record, warnings):
    """True if this slug's incoming source data is OLDER than what is
    already stored for it. Only compares when both sides carry a run_date -
    a campaign advancing from a dateless RESEARCHED stage into a dated
    QUALIFIED stage is normal progress, never a supersession."""
    existing = get_campaign(conn, slug)
    if not existing:
        return False
    incoming_date, existing_date = record.get("run_date"), existing.get("run_date")
    if not incoming_date or not existing_date:
        return False
    if incoming_date < existing_date:
        warnings.append(
            f"{slug}: incoming source run_date {incoming_date} is older than the stored "
            f"canonical run_date {existing_date} - skipped, existing data kept"
        )
        return True
    return False


def upsert_campaign(conn, record):
    now = now_iso()
    existing = get_campaign(conn, record["campaign_id"])
    first_seen = existing["first_imported_at"] if existing else now
    conn.execute(
        """
        INSERT INTO campaigns (campaign_id, sector, geography, run_date, pipeline_stage,
            market_count, outreach_count, excluded_count, source_run_csv,
            source_campaign_json, source_run_log, first_imported_at, last_imported_at)
        VALUES (:campaign_id, :sector, :geography, :run_date, :pipeline_stage,
            :market_count, :outreach_count, :excluded_count, :source_run_csv,
            :source_campaign_json, :source_run_log, :first_imported_at, :last_imported_at)
        ON CONFLICT(campaign_id) DO UPDATE SET
            sector=excluded.sector, geography=excluded.geography, run_date=excluded.run_date,
            pipeline_stage=excluded.pipeline_stage, market_count=excluded.market_count,
            outreach_count=excluded.outreach_count, excluded_count=excluded.excluded_count,
            source_run_csv=excluded.source_run_csv, source_campaign_json=excluded.source_campaign_json,
            source_run_log=excluded.source_run_log, last_imported_at=excluded.last_imported_at
        """,
        {**record, "first_imported_at": first_seen, "last_imported_at": now},
    )


def upsert_prospect(conn, prospect_id, campaign_id, business_key, research):
    now = now_iso()
    existing = get_prospect(conn, prospect_id)
    first_seen = existing["first_imported_at"] if existing else now
    row = dict(research)
    row["prospect_id"] = prospect_id
    row["campaign_id"] = campaign_id
    row["business_key"] = business_key
    row["first_imported_at"] = first_seen
    row["last_imported_at"] = now
    columns = list(row.keys())
    placeholders = ", ".join(f":{c}" for c in columns)
    update_clause = ", ".join(
        f"{c}=excluded.{c}" for c in columns
        if c not in ("prospect_id", "first_imported_at", "do_not_contact_manual", "notes")
    )
    conn.execute(
        f"""
        INSERT INTO prospects ({', '.join(columns)})
        VALUES ({placeholders})
        ON CONFLICT(prospect_id) DO UPDATE SET {update_clause}
        """,
        row,
    )


IMPORT_LOG_MAX = 500


def record_import_log(conn, warnings):
    if not warnings:
        return
    ts = now_iso()
    conn.executemany(
        "INSERT INTO import_log (timestamp, message) VALUES (?, ?)",
        [(ts, message) for message in warnings],
    )
    count = conn.execute("SELECT COUNT(*) FROM import_log").fetchone()[0]
    if count > IMPORT_LOG_MAX:
        conn.execute(
            "DELETE FROM import_log WHERE id IN "
            "(SELECT id FROM import_log ORDER BY id ASC LIMIT ?)",
            (count - IMPORT_LOG_MAX,),
        )


def import_all(conn, runs_dir, slugs=None, warnings=None):
    if warnings is None:
        warnings = []
    slugs = slugs or discover_slugs(runs_dir)
    imported_campaigns = 0
    imported_prospects = 0

    for slug in slugs:
        record, outreach_prep, outreach_entries = build_campaign_record(slug, runs_dir, warnings)
        if record is None:
            warnings.append(f"{slug}: no raw run CSV, campaign JSON, or run-log found - skipped")
            continue
        if is_superseded(conn, slug, record, warnings):
            continue
        upsert_campaign(conn, record)
        imported_campaigns += 1

        matched_prep_keys = set()
        for entry in outreach_entries:
            business = entry.get("business")
            if not business:
                continue
            name_key = slugify(business)
            prep_match = outreach_prep.get(name_key)
            if prep_match:
                matched_prep_keys.add(name_key)
            prep_entry = prep_match[0] if prep_match else None
            business_key = business_key_for(entry, prep_entry)
            prospect_id = f"{slug}::{business_key}"
            research = build_prospect_research(entry, prep_match)
            upsert_prospect(conn, prospect_id, slug, business_key, research)
            imported_prospects += 1

        for name_key, (prep_entry, prep_path) in outreach_prep.items():
            if name_key in matched_prep_keys:
                continue
            business = prep_entry.get("business", "")
            business_key = business_key_for({"business": business}, prep_entry)
            prospect_id = f"{slug}::{business_key}"
            research = build_prospect_research(
                {"business": business, "area": prep_entry.get("area")}, (prep_entry, prep_path)
            )
            research["orphaned_outreach_prep"] = 1
            warnings.append(
                f"{slug}: outreach-prep entry for '{business}' has no matching outreach[] "
                f"entry in the campaign JSON - recorded as orphaned, not matched"
            )
            upsert_prospect(conn, prospect_id, slug, business_key, research)
            imported_prospects += 1

    conn.commit()
    return imported_campaigns, imported_prospects, warnings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-dir", default=str(Path.home() / "wardith-runs"),
                         help="Where /90qrun, /qualify and /outreach write their output. Default: ~/wardith-runs")
    parser.add_argument("--db-path", default=None,
                         help="Where the CRM database lives. Default: <runs-dir>/crm/wardith.db")
    parser.add_argument("--slug", action="append", default=None,
                         help="Import only this campaign slug. Repeatable. Default: every slug found.")
    args = parser.parse_args(argv)

    runs_dir = Path(args.runs_dir).expanduser()
    db_path = Path(args.db_path).expanduser() if args.db_path else runs_dir / "crm" / "wardith.db"

    if not runs_dir.is_dir():
        print(f"error: runs directory not found: {runs_dir}", file=sys.stderr)
        return 1

    conn = db_mod.connect(db_path)
    db_mod.init_db(conn)
    warnings = []
    n_campaigns, n_prospects, warnings = import_all(conn, runs_dir, slugs=args.slug, warnings=warnings)
    record_import_log(conn, warnings)
    conn.commit()

    print(f"Campaigns processed: {n_campaigns}")
    print(f"Prospects processed: {n_prospects}")
    print(f"Database: {db_path}")
    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for w in warnings:
            print(f"  - {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
