#!/usr/bin/env python3
"""Import completed /90qrun, /qualify and /outreach output into the
campaign tracker. Read-only against ~/wardith-runs/<slug>/ and
~/wardith-runs/<slug>.csv; the only writes are tracker.json and tracker.csv
under ~/wardith-runs/tracker/. See SCHEMA.md for the field-by-field shape
and README.md for usage.
"""

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = 1

ACTIVITY_FIELDS = [
    "outreach_status",
    "prepared_date",
    "sent_date",
    "replied_date",
    "followed_up_date",
    "converted_date",
    "rejected_date",
    "opted_out_date",
    "audit_revenue",
    "foundation_revenue",
    "ongoing_plan",
    "ongoing_plan_revenue",
    "next_action",
    "next_action_due_date",
    "do_not_contact",
]

RESEARCH_FIELDS = [
    "business",
    "area",
    "website",
    "campaign_id",
    "priority",
    "opportunity_type",
    "outreach_rank",
    "accessibility",
    "accessibility_notes",
    "contact_person",
    "role",
    "contact_email",
    "contact_phone",
    "decision_maker_linkedin",
    "ready_to_email",
    "competitive_gap_finding",
    "why_prospect",
    "legal_entity",
    "company_number",
    "company_status",
    "outreach_angle",
    "email_subject",
    "email_body",
    "linkedin_draft",
    "caveats",
    "evidence_source_ids",
    "source_campaign_json",
    "source_outreach_prep_json",
    "orphaned_outreach_prep",
    "withheld_at_outreach",
    "withheld_reason",
]

CSV_COLUMNS = [
    "prospect_id", "campaign_id", "sector", "geography", "run_date",
    "pipeline_stage",
    "business", "area", "website",
    "priority", "opportunity_type", "outreach_rank",
    "accessibility", "contact_person", "role", "contact_email",
    "contact_phone", "decision_maker_linkedin", "ready_to_email",
    "outreach_status", "prepared_date", "sent_date", "replied_date",
    "followed_up_date", "converted_date", "rejected_date", "opted_out_date",
    "do_not_contact",
    "audit_revenue", "foundation_revenue", "ongoing_plan",
    "ongoing_plan_revenue",
    "next_action", "next_action_due_date",
    "source_campaign_json", "source_outreach_prep_json",
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
        return None, f"{path}: could not parse ({e}) — likely mid-write, skipped"


def parse_run_log(path):
    """Pull sector/geography/date from a /90qrun run-log's own structured
    header lines. Never guesses from the slug — only reads what the skill
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
        if d.is_dir() and d.name != "tracker":
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
    """Returns {slugified_business: entry}, using the most recent dated
    file's entry for a given business if more than one file exists."""
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
    """True only for an outreach-prep entry that was actually drafted:
    not withheld at /outreach's own Stage 4 gate, and carrying real email
    copy. A withheld entry (ready_to_email was REVIEW, or the contact route
    died on re-check) is recorded for its research value — contact_route,
    withheld_reason — but must never be reported as a prepared, send-ready
    outreach_status."""
    if not prep_entry:
        return False
    if prep_entry.get("withheld") is True:
        return False
    return bool(prep_entry.get("email_body"))


def build_prospect_research(slug, entry, prep_match):
    prep_entry, prep_path = prep_match if prep_match else (None, None)
    research = {field: None for field in RESEARCH_FIELDS}
    research.update({
        "business": entry.get("business"),
        "area": entry.get("area"),
        "website": entry.get("website"),
        "campaign_id": slug,
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
        "evidence_source_ids": entry.get("evidence_source_ids"),
        "orphaned_outreach_prep": False,
        "withheld_at_outreach": False,
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
        research["caveats"] = prep_entry.get("caveats")
        research["source_outreach_prep_json"] = str(prep_path)
        research["withheld_at_outreach"] = prep_entry.get("withheld") is True
        research["withheld_reason"] = prep_entry.get("withheld_reason")
    return research


def default_activity():
    return {field: None for field in ACTIVITY_FIELDS}


def upsert_campaign(tracker, record):
    campaign_id = record["campaign_id"]
    existing = tracker["campaigns"].get(campaign_id)
    now = now_iso()
    if existing:
        first_seen = existing.get("first_imported_at", now)
    else:
        first_seen = now
    record["first_imported_at"] = first_seen
    record["last_imported_at"] = now
    tracker["campaigns"][campaign_id] = record


def upsert_prospect(tracker, prospect_id, research, prepared_now):
    existing = tracker["prospects"].get(prospect_id)
    now = now_iso()
    if existing:
        activity = existing["activity"]
        first_seen = existing.get("first_imported_at", now)
    else:
        activity = default_activity()
        first_seen = now

    if prepared_now and activity["outreach_status"] is None:
        activity["outreach_status"] = "PREPARED"
        activity["prepared_date"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    elif not prepared_now and activity["outreach_status"] == "PREPARED":
        # PREPARED is the one importer-derived status, never a human decision -
        # it means "the latest outreach-prep draft says this is ready to send".
        # If a fresher run of /outreach now withholds this business (or the
        # match disappears), un-PREPARE it. Anything the owner has since
        # advanced past PREPARED (SENT, REPLIED, ...) is a different string
        # and this branch never touches it.
        activity["outreach_status"] = None
        activity["prepared_date"] = None

    tracker["prospects"][prospect_id] = {
        "prospect_id": prospect_id,
        "research": research,
        "activity": activity,
        "first_imported_at": first_seen,
        "last_imported_at": now,
    }


def is_superseded(slug, record, tracker, warnings):
    """True if this slug's incoming source data is OLDER than what is
    already stored for it (a stale/regenerated campaign JSON re-imported
    after a newer one), per the 'prefer the newest canonical source' rule.
    Only compares when both sides actually carry a run_date — a campaign
    advancing from a dateless RESEARCHED stage into a dated QUALIFIED stage
    is normal progress, never a supersession."""
    existing = tracker["campaigns"].get(slug)
    if not existing:
        return False
    incoming_date, existing_date = record.get("run_date"), existing.get("run_date")
    if not incoming_date or not existing_date:
        return False
    if incoming_date < existing_date:
        warnings.append(
            f"{slug}: incoming source run_date {incoming_date} is older than the stored "
            f"canonical run_date {existing_date} — skipped, existing data kept"
        )
        return True
    return False


def import_all(runs_dir, tracker, slugs=None, warnings=None):
    if warnings is None:
        warnings = []
    slugs = slugs or discover_slugs(runs_dir)
    imported_campaigns = 0
    imported_prospects = 0

    for slug in slugs:
        record, outreach_prep, outreach_entries = build_campaign_record(slug, runs_dir, warnings)
        if record is None:
            warnings.append(f"{slug}: no raw run CSV, campaign JSON, or run-log found — skipped")
            continue
        if is_superseded(slug, record, tracker, warnings):
            continue
        upsert_campaign(tracker, record)
        imported_campaigns += 1

        matched_prep_keys = set()
        for entry in outreach_entries:
            business = entry.get("business")
            if not business:
                continue
            key = slugify(business)
            prospect_id = f"{slug}::{key}"
            prep_match = outreach_prep.get(key)
            if prep_match:
                matched_prep_keys.add(key)
            prep_entry = prep_match[0] if prep_match else None
            research = build_prospect_research(slug, entry, prep_match)
            upsert_prospect(tracker, prospect_id, research, prepared_now=is_genuinely_prepared(prep_entry))
            imported_prospects += 1

        for key, (prep_entry, prep_path) in outreach_prep.items():
            if key in matched_prep_keys:
                continue
            business = prep_entry.get("business", "")
            prospect_id = f"{slug}::{key}"
            research = build_prospect_research(slug, {"business": business, "area": prep_entry.get("area")}, (prep_entry, prep_path))
            research["orphaned_outreach_prep"] = True
            warnings.append(
                f"{slug}: outreach-prep entry for '{business}' has no matching outreach[] "
                f"entry in the campaign JSON — recorded as orphaned, not matched"
            )
            upsert_prospect(tracker, prospect_id, research, prepared_now=is_genuinely_prepared(prep_entry))
            imported_prospects += 1

    return imported_campaigns, imported_prospects, warnings


def export_csv(tracker, csv_path):
    rows = []
    for prospect_id, p in sorted(tracker["prospects"].items()):
        r = p["research"]
        a = p["activity"]
        campaign = tracker["campaigns"].get(r.get("campaign_id"), {})
        rows.append({
            "prospect_id": prospect_id,
            "campaign_id": r.get("campaign_id"),
            "sector": campaign.get("sector"),
            "geography": campaign.get("geography"),
            "run_date": campaign.get("run_date"),
            "pipeline_stage": campaign.get("pipeline_stage"),
            "business": r.get("business"),
            "area": r.get("area"),
            "website": r.get("website"),
            "priority": r.get("priority"),
            "opportunity_type": r.get("opportunity_type"),
            "outreach_rank": r.get("outreach_rank"),
            "accessibility": r.get("accessibility"),
            "contact_person": r.get("contact_person"),
            "role": r.get("role"),
            "contact_email": r.get("contact_email"),
            "contact_phone": r.get("contact_phone"),
            "decision_maker_linkedin": r.get("decision_maker_linkedin"),
            "ready_to_email": r.get("ready_to_email"),
            "outreach_status": a.get("outreach_status"),
            "prepared_date": a.get("prepared_date"),
            "sent_date": a.get("sent_date"),
            "replied_date": a.get("replied_date"),
            "followed_up_date": a.get("followed_up_date"),
            "converted_date": a.get("converted_date"),
            "rejected_date": a.get("rejected_date"),
            "opted_out_date": a.get("opted_out_date"),
            "do_not_contact": a.get("do_not_contact"),
            "audit_revenue": a.get("audit_revenue"),
            "foundation_revenue": a.get("foundation_revenue"),
            "ongoing_plan": a.get("ongoing_plan"),
            "ongoing_plan_revenue": a.get("ongoing_plan_revenue"),
            "next_action": a.get("next_action"),
            "next_action_due_date": a.get("next_action_due_date"),
            "source_campaign_json": r.get("source_campaign_json"),
            "source_outreach_prep_json": r.get("source_outreach_prep_json"),
        })

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


IMPORT_LOG_MAX = 500


def record_import_log(tracker, warnings):
    """Persist this run's warnings/conflicts into tracker.json itself, not
    just stdout — so a conflict (e.g. a superseded campaign JSON skipped by
    is_superseded) stays visible to the CRM's Import Log sheet across runs,
    not just in whichever terminal happened to run the import that day."""
    if not warnings:
        return
    log = tracker.setdefault("import_log", [])
    ts = now_iso()
    for message in warnings:
        log.append({"timestamp": ts, "message": message})
    if len(log) > IMPORT_LOG_MAX:
        del log[: len(log) - IMPORT_LOG_MAX]


def load_tracker(tracker_path):
    if tracker_path.exists():
        with open(tracker_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data.setdefault("campaigns", {})
        data.setdefault("prospects", {})
        data.setdefault("import_log", [])
        return data
    return {"schema_version": SCHEMA_VERSION, "campaigns": {}, "prospects": {}, "import_log": []}


def save_tracker(tracker, tracker_path):
    tracker_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = tracker_path.with_suffix(".json.tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(tracker, f, indent=2, sort_keys=True)
        f.write("\n")
    tmp_path.replace(tracker_path)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs-dir", default=str(Path.home() / "wardith-runs"),
                         help="Where /90qrun, /qualify and /outreach write their output. Default: ~/wardith-runs")
    parser.add_argument("--tracker-dir", default=None,
                         help="Where tracker.json/tracker.csv live. Default: <runs-dir>/tracker")
    parser.add_argument("--slug", action="append", default=None,
                         help="Import only this campaign slug. Repeatable. Default: every slug found.")
    parser.add_argument("--no-csv", action="store_true", help="Skip writing tracker.csv")
    args = parser.parse_args(argv)

    runs_dir = Path(args.runs_dir).expanduser()
    tracker_dir = Path(args.tracker_dir).expanduser() if args.tracker_dir else runs_dir / "tracker"
    tracker_path = tracker_dir / "tracker.json"
    csv_path = tracker_dir / "tracker.csv"

    if not runs_dir.is_dir():
        print(f"error: runs directory not found: {runs_dir}", file=sys.stderr)
        return 1

    tracker = load_tracker(tracker_path)
    warnings = []
    n_campaigns, n_prospects, warnings = import_all(runs_dir, tracker, slugs=args.slug, warnings=warnings)
    record_import_log(tracker, warnings)
    save_tracker(tracker, tracker_path)

    if not args.no_csv:
        export_csv(tracker, csv_path)

    print(f"Campaigns processed: {n_campaigns}")
    print(f"Prospects processed: {n_prospects}")
    print(f"Tracker: {tracker_path}")
    if not args.no_csv:
        print(f"CSV:     {csv_path}")
    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for w in warnings:
            print(f"  - {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
