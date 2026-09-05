#!/usr/bin/env python3
"""Build a conservative, census-wide qualification coverage report."""
import argparse
import csv
from datetime import date
import json
import os
import sys

GROUPS = ("SEND NOW", "SECONDARY", "REVIEW", "EXCLUDE", "INCUMBENT")
HARD_EXCLUSIONS = {
    "SOLE TRADER", "ORDINARY PARTNERSHIP", "CHAIN / NO LOCAL DECISION-MAKER",
    "DUPLICATE BRAND", "NOT GENUINELY IN MARKET", "CLOSED / DORMANT",
}
RESEARCHABLE_EXCLUSIONS = {"NO RELIABLE LEGAL MATCH", "OTHER / REVIEW"}


def _key(value):
    return " ".join(str(value or "").split()).casefold()


def _business(record):
    return " ".join(str(record.get("business", "")).split())


# 2026-09-05: SEND NOW mirrors scoring_engine.py's ready_to_email gate exactly -
# a named decision-maker is optional enrichment, a usable route to the business
# is not. The freshness window matches the /qualify Stage 5 rule already in use
# for reusing a CRM record: inside it, evidence is a verified starting point;
# beyond it, contact routes and accessibility have gone stale and the record is
# re-verified before use.
SEND_NOW_FRESHNESS_DAYS = 90
MIN_SEND_DM_ROUTE = 2


def _within_freshness_window(run):
    try:
        run_date = date.fromisoformat(str(run.get("date", "")))
    except ValueError:
        return False
    return 0 <= (date.today() - run_date).days <= SEND_NOW_FRESHNESS_DAYS


def _send_blockers(record, run):
    """Every unmet SEND NOW condition, named. A record that is not SEND NOW
    always says why - that is what the count shortfall is read against."""
    blockers = []
    if not _within_freshness_window(run):
        blockers.append(f"Historical evidence, older than {SEND_NOW_FRESHNESS_DAYS} days: refresh legal status, "
                        "contact route and commercial findings before use.")
    if record.get("business_verified") != "YES":
        blockers.append("Business verification is incomplete.")
    if not record.get("company_number") or str(record.get("company_status", "")).casefold() != "active":
        blockers.append("No confirmed active Ltd/LLP match in the campaign record.")
    if record.get("contact_route_verified") != "YES":
        blockers.append("Contact route verification is incomplete.")
    if record.get("direct_dm_route", 0) < MIN_SEND_DM_ROUTE:
        blockers.append("No usable contact route to the business: contact form or telephone only, or no route at all.")
    if not record.get("contact_email"):
        blockers.append("Verified email route not yet recorded.")
    if record.get("research_complete") != "YES":
        blockers.append("Qualification research is incomplete.")
    if record.get("overall_evidence_confidence", 0) < 3:
        blockers.append("Evidence confidence is below the send threshold: business credibility or research completeness is unresolved.")
    if record.get("eligible_for_outreach") != "YES":
        blockers.append("Not commercially eligible: business fit or service relevance is unresolved.")
    if record.get("ready_to_email") != "YES":
        blockers.append("The campaign record does not carry an approved ready_to_email=YES.")
    return blockers


def _classify(records, run, duplicate_labels):
    blockers = []
    sections = {section for section, _record in records}
    combined = {}
    for _section, record in records:
        combined.update(record)
    if len(records) > 1 and len(sections) > 1:
        dispositions = {r.get("disposition") for _s, r in records if r.get("disposition")}
        if "REVIEW" in dispositions and "outreach" in sections:
            blockers.append("Conflicting campaign records: market says REVIEW but an outreach record also exists.")
    if duplicate_labels:
        blockers.append("Duplicate spelling/capitalisation records were merged for counting; verify the identity match.")
    reason = str(combined.get("reason", "")).upper()
    if combined.get("most_named_cohort") is True:
        if _within_freshness_window(run):
            return "INCUMBENT", ["Held out of the default cold-outreach batch as one of this campaign's most-mentioned incumbents; retained in the market analysis."] + blockers
        return "REVIEW", ["Historical dominance claim needs current canonical verification."] + blockers
    if reason in HARD_EXCLUSIONS:
        return "EXCLUDE", [f"Genuine exclusion recorded: {reason}."] + blockers
    if reason == "ALREADY STRONGLY VISIBLE":
        blockers.append("Historical visibility exclusion needs current canonical dominance evidence.")
    elif reason in RESEARCHABLE_EXCLUSIONS:
        blockers.append(f"Research remains open: {reason}.")
    if blockers:
        return "REVIEW", blockers
    blockers = _send_blockers(combined, run)
    if not blockers:
        return "SEND NOW", []
    if combined.get("eligible_for_outreach") == "YES" and combined.get("research_complete") == "YES":
        if combined.get("direct_dm_route") == 2 and combined.get("contact_email"):
            blockers.append("Verified general business inbox, no named decision-maker: address the business, never an invented name.")
        return "SECONDARY", blockers
    return "REVIEW", blockers


def build_report(data, census=()):
    """Return one non-mutating coverage decision per normalized business name."""
    indexed = {}
    display = {}
    labels = {}
    run = data.get("run", {})
    cohort = {_key(c.get("business")): c for c in run.get("scoring_cohort", [])}
    completion_blockers = []
    if not census:
        completion_blockers.append("Census not supplied; full-market coverage cannot be verified.")
    if run.get("cohort_inclusion_min_appearances") != 0:
        completion_blockers.append("New qualifications require cohort_inclusion_min_appearances=0.")
    for item in census:
        name = _business(item) if isinstance(item, dict) else " ".join(str(item).split())
        if name:
            key = _key(name)
            display.setdefault(key, name)
            labels.setdefault(key, set()).add(name)
            indexed.setdefault(key, [])
        else:
            completion_blockers.append("Census contains a blank business name; resolve the source row.")
    if not indexed:
        completion_blockers.append("Census contains no usable business names.")
    for section in ("market", "outreach", "excluded"):
        for record in data.get(section, []):
            name = _business(record)
            if not name:
                continue
            key = _key(name)
            display.setdefault(key, name)
            labels.setdefault(key, set()).add(name)
            indexed.setdefault(key, []).append((section, record))

    rows = []
    missing = []
    counts = {group: 0 for group in GROUPS}
    for key in sorted(indexed, key=lambda k: display[k].casefold()):
        records = indexed[key]
        if not records:
            group, blockers = "REVIEW", ["Present in the census but missing from campaign assessment."]
            missing.append(display[key])
            combined = {}
        else:
            group, blockers = _classify(records, data.get("run", {}), len(labels[key]) > 1)
            combined = {}
            for _section, record in records:
                combined.update(record)
        assessment = cohort.get(key, {})
        status = assessment.get("status")
        if status == "INCOMPLETE":
            detail = assessment.get("missing_evidence") or "Cohort marked INCOMPLETE without recorded missing evidence."
            blockers.insert(0, detail)
            group = "REVIEW"
            completion_blockers.append(f"{display[key]}: {detail}")
        elif status not in {"SCORED", "EXCLUDED"}:
            completion_blockers.append(f"{display[key]}: no explicit completed cohort assessment.")
        elif status == "EXCLUDED" and not assessment.get("reason"):
            completion_blockers.append(f"{display[key]}: cohort exclusion has no reason.")
        elif status == "SCORED" and not (combined.get("service_scope") and combined.get("overall_rank")):
            completion_blockers.append(f"{display[key]}: cohort says SCORED but canonical scoring is absent.")
        elif status == "SCORED" and group not in {"INCUMBENT", "EXCLUDE"} and combined.get("research_complete") != "YES":
            completion_blockers.append(f"{display[key]}: full qualification research remains incomplete.")
        counts[group] += 1
        rows.append({
            "business": display[key], "selection_group": group,
            "appearances": combined.get("total_ai_appearances"),
            "priority": combined.get("priority", ""),
            "ready_to_email_recorded": combined.get("ready_to_email", ""),
            "cohort_status": status or "UNASSESSED",
            "recorded_notes": combined.get("notes", ""),
            "blockers": blockers,
        })
    return {
        "campaign_slug": data.get("run", {}).get("campaign_slug", ""),
        "total_businesses": len(rows), "counts": counts,
        "potential_non_top": counts["SEND NOW"] + counts["SECONDARY"] + counts["REVIEW"],
        "recorded_ready": sum(1 for r in data.get("outreach", []) if r.get("ready_to_email") == "YES"),
        "missing_from_campaign": missing, "rows": rows,
        "coverage_status": "INCOMPLETE" if completion_blockers or missing else "COMPLETE",
        "completion_blockers": completion_blockers,
        "notice": "Coverage groups are recommendations only. This report sends nothing and does not alter campaign data.",
    }


def _load_census(path):
    if not path:
        return []
    with open(path, newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or "business" not in rows[0]:
        raise ValueError("census must contain a business column")
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Existing campaign JSON")
    parser.add_argument("--census", help="Optional market census CSV with a business column")
    parser.add_argument("--output", required=True, help="New JSON report path")
    parser.add_argument("--require-complete", action="store_true", help="Return failure after saving the report if census coverage is incomplete")
    args = parser.parse_args()
    if os.path.exists(args.output):
        print(f"Refusing to overwrite existing report: {args.output}", file=sys.stderr)
        return 2
    try:
        with open(args.input, encoding="utf-8") as handle:
            data = json.load(handle)
        report = build_report(data, _load_census(args.census))
        with open(args.output, "x", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2, ensure_ascii=False)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"qualification-coverage: {error}", file=sys.stderr)
        return 1
    print(f"Wrote {args.output} ({report['total_businesses']} business record(s) included; coverage {report['coverage_status']})")
    if args.require_complete and report["coverage_status"] != "COMPLETE":
        print("Census-wide qualification is INCOMPLETE; see completion_blockers in the saved report.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
