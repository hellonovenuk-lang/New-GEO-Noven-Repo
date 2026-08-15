#!/usr/bin/env python3
"""
Prospect compiler — renders a validated campaign JSON file (schema.json) into
an .xlsx workbook: OUTREACH, MARKET, EXCLUDED, SOURCES, RUN.

This script does not research businesses or judge who is a prospect. The
input JSON is prepared by Claude/human judgement during a Wardith market
campaign; this script deterministically renders it. Fails loudly on
malformed input rather than filling gaps with guesses.

Usage:
  python3 build_workbook.py --input campaign.json --output workbook.xlsx

Requires openpyxl (pip install openpyxl) — the one non-stdlib dependency.
"""

import argparse
import json
import re
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

EXCLUDED_REASONS = {
    "SOLE TRADER",
    "ORDINARY PARTNERSHIP",
    "CHAIN / NO LOCAL DECISION-MAKER",
    "DUPLICATE BRAND",
    "NOT GENUINELY IN MARKET",
    "CLOSED / DORMANT",
    "ALREADY STRONGLY VISIBLE",
    "NO RELIABLE LEGAL MATCH",
    "OTHER / REVIEW",
}
PRIORITIES = {"A", "B", "C", "REVIEW"}
READY_VALUES = {"YES", "REVIEW"}
DISPOSITIONS = {"OUTREACH", "EXCLUDED", "REVIEW"}
OPPORTUNITY_TYPES = {"GAP", "GROWTH", "DEFEND", "NO OPPORTUNITY"}
ACCESSIBILITY_VALUES = {"DIRECT", "IDENTIFIABLE", "GATEKEPT", "CORPORATE", "REVIEW"}
SOURCE_ID_RE = re.compile(r"^S[0-9]{3,}$")

# Named decision-maker with an obvious direct professional contact route (DIRECT)
# down to filtered-through-reception with no clear route (GATEKEPT/REVIEW).
# Colours are a triage aid only - they never change priority or disposition.
ACCESSIBILITY_FILLS = {
    "DIRECT": PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid"),
    "IDENTIFIABLE": PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid"),
    "GATEKEPT": PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid"),
    "CORPORATE": PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid"),
    "REVIEW": PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid"),
}

OUTREACH_COLUMNS = [
    ("priority", "Priority", 10, False),
    ("opportunity_type", "Opportunity type", 16, False),
    ("accessibility", "Decision-maker accessibility", 18, False),
    ("business", "Business", 24, False),
    ("area", "Area", 16, False),
    ("website", "Website", 26, False),
    ("total_ai_appearances", "Total AI appearances", 12, False),
    ("openai_appearances", "OpenAI appearances", 12, False),
    ("gemini_appearances", "Gemini appearances", 12, False),
    ("perplexity_appearances", "Perplexity appearances", 14, False),
    ("strongest_competitor", "Strongest relevant competitor", 24, False),
    ("competitor_appearances", "Competitor appearances", 14, False),
    ("competitive_gap_finding", "Competitive-gap finding", 42, True),
    ("why_prospect", "Why this is a prospect", 42, True),
    ("legal_entity", "Legal entity", 22, False),
    ("company_number", "Company number", 16, False),
    ("company_status", "Company status", 14, False),
    ("contact_person", "Contact person", 18, False),
    ("role", "Role", 16, False),
    ("contact_email", "Contact email", 26, False),
    ("decision_maker_linkedin", "Decision-maker LinkedIn", 30, False),
    ("accessibility_notes", "Accessibility notes", 40, True),
    ("ready_to_email", "Ready to email", 14, False),
    ("evidence_source_ids", "Evidence source IDs", 20, False),
]

MARKET_COLUMNS = [
    ("business", "Business", 24, False),
    ("area", "Area", 16, False),
    ("disposition", "Disposition", 14, False),
    ("opportunity_type", "Opportunity type", 16, False),
    ("accessibility", "Decision-maker accessibility", 18, False),
    ("total_ai_appearances", "Total AI appearances", 12, False),
    ("openai_appearances", "OpenAI appearances", 12, False),
    ("gemini_appearances", "Gemini appearances", 12, False),
    ("perplexity_appearances", "Perplexity appearances", 14, False),
    ("notes", "Notes", 40, True),
]

EXCLUDED_COLUMNS = [
    ("business", "Business", 24, False),
    ("area", "Area", 16, False),
    ("reason", "Reason", 28, False),
    ("notes", "Notes", 40, True),
]

SOURCES_COLUMNS = [
    ("source_id", "Source ID", 12, False),
    ("business", "Business", 24, False),
    ("publisher", "Publisher/source", 24, False),
    ("fact_supported", "Fact supported", 36, True),
    ("url", "URL", 40, False),
    ("access_date", "Access date", 14, False),
]


class ValidationError(Exception):
    pass


def fail(message):
    raise ValidationError(message)


def require_keys(obj, required, where):
    if not isinstance(obj, dict):
        fail(f"{where}: expected an object, got {type(obj).__name__}")
    missing = [k for k in required if k not in obj or obj[k] in (None, "")]
    if missing:
        fail(f"{where}: missing required field(s): {', '.join(missing)}")


def validate(data):
    require_keys(data, ["run", "market", "outreach", "excluded", "sources"], "top level")

    run = data["run"]
    require_keys(run, ["sector", "geography", "campaign_slug", "date", "questions", "providers"], "run")
    if not isinstance(run["questions"], list) or not run["questions"]:
        fail("run.questions: must be a non-empty list")
    if not isinstance(run["providers"], list) or not run["providers"]:
        fail("run.providers: must be a non-empty list")
    for i, p in enumerate(run["providers"]):
        require_keys(p, ["provider", "model"], f"run.providers[{i}]")

    if not isinstance(data["sources"], list) or not data["sources"]:
        fail("sources: must be a non-empty list")
    known_source_ids = set()
    for i, s in enumerate(data["sources"]):
        require_keys(s, ["source_id", "business", "publisher", "fact_supported", "url", "access_date"], f"sources[{i}]")
        if not SOURCE_ID_RE.match(s["source_id"]):
            fail(f"sources[{i}].source_id: '{s['source_id']}' does not match S### (e.g. S001)")
        known_source_ids.add(s["source_id"])

    if not isinstance(data["market"], list):
        fail("market: must be a list")
    for i, m in enumerate(data["market"]):
        require_keys(m, ["business", "area", "disposition", "total_ai_appearances"], f"market[{i}]")
        if m["disposition"] not in DISPOSITIONS:
            fail(f"market[{i}].disposition: '{m['disposition']}' not one of {sorted(DISPOSITIONS)}")
        # opportunity_type is optional - not every census business gets one -
        # but if present it must be a real value, not a typo silently ignored
        if "opportunity_type" in m and m["opportunity_type"] not in OPPORTUNITY_TYPES:
            fail(f"market[{i}].opportunity_type: '{m['opportunity_type']}' not one of {sorted(OPPORTUNITY_TYPES)}")
        # accessibility is optional here too - most of a census never gets
        # contact-route research; it's required once a business reaches outreach[]
        if "accessibility" in m and m["accessibility"] not in ACCESSIBILITY_VALUES:
            fail(f"market[{i}].accessibility: '{m['accessibility']}' not one of {sorted(ACCESSIBILITY_VALUES)}")

    if not isinstance(data["outreach"], list):
        fail("outreach: must be a list")
    required_outreach = [
        "priority", "business", "area", "total_ai_appearances",
        "strongest_competitor", "competitor_appearances",
        "competitive_gap_finding", "why_prospect",
        "legal_entity", "company_number", "company_status",
        "ready_to_email", "evidence_source_ids", "accessibility",
    ]
    for i, o in enumerate(data["outreach"]):
        require_keys(o, required_outreach, f"outreach[{i}]")
        if o["priority"] not in PRIORITIES:
            fail(f"outreach[{i}].priority: '{o['priority']}' not one of {sorted(PRIORITIES)}")
        if "opportunity_type" in o and o["opportunity_type"] not in OPPORTUNITY_TYPES:
            fail(f"outreach[{i}].opportunity_type: '{o['opportunity_type']}' not one of {sorted(OPPORTUNITY_TYPES)}")
        if o["accessibility"] not in ACCESSIBILITY_VALUES:
            fail(f"outreach[{i}].accessibility: '{o['accessibility']}' not one of {sorted(ACCESSIBILITY_VALUES)}")
        if o["ready_to_email"] not in READY_VALUES:
            fail(f"outreach[{i}].ready_to_email: '{o['ready_to_email']}' not one of {sorted(READY_VALUES)}")
        if not isinstance(o["evidence_source_ids"], list) or not o["evidence_source_ids"]:
            fail(f"outreach[{i}].evidence_source_ids: must be a non-empty list")
        unknown = [sid for sid in o["evidence_source_ids"] if sid not in known_source_ids]
        if unknown:
            fail(f"outreach[{i}] ({o['business']}): evidence_source_ids references unknown source(s): {', '.join(unknown)}")

    if not isinstance(data["excluded"], list):
        fail("excluded: must be a list")
    for i, e in enumerate(data["excluded"]):
        require_keys(e, ["business", "area", "reason"], f"excluded[{i}]")
        if e["reason"] not in EXCLUDED_REASONS:
            fail(f"excluded[{i}].reason: '{e['reason']}' not one of {sorted(EXCLUDED_REASONS)}")


def style_header(ws, ncols):
    bold = Font(bold=True)
    for col in range(1, ncols + 1):
        ws.cell(row=1, column=col).font = bold
    ws.freeze_panes = "A2"
    last_col = get_column_letter(ncols)
    ws.auto_filter.ref = f"A1:{last_col}1"


def write_table(ws, columns, rows):
    headers = [label for _, label, _, _ in columns]
    ws.append(headers)
    for row in rows:
        values = []
        for key, _, _, _ in columns:
            v = row.get(key, "")
            if isinstance(v, list):
                v = "; ".join(str(x) for x in v)
            values.append(v)
        ws.append(values)
    for idx, (_, _, width, wrap) in enumerate(columns, start=1):
        ws.column_dimensions[get_column_letter(idx)].width = width
        if wrap:
            for row_cells in ws.iter_rows(min_row=2, min_col=idx, max_col=idx):
                for cell in row_cells:
                    cell.alignment = Alignment(wrap_text=True, vertical="top")
    style_header(ws, len(columns))


def priority_sort_key(rows):
    # REVIEW sorts last, deliberately - it means commercial priority hasn't
    # been settled yet, not that it's a fourth tier below C. Accessibility is
    # a secondary tiebreaker only, within the same priority band - it never
    # promotes a business past a higher-priority one. A GATEKEPT priority-A
    # prospect always outranks a DIRECT priority-B one.
    priority_order = {"A": 0, "B": 1, "C": 2, "REVIEW": 3}
    accessibility_order = {"DIRECT": 0, "IDENTIFIABLE": 1, "GATEKEPT": 2, "CORPORATE": 3, "REVIEW": 4}
    return sorted(
        range(len(rows)),
        key=lambda i: (
            priority_order.get(rows[i]["priority"], 99),
            accessibility_order.get(rows[i].get("accessibility"), 99),
        ),
    )


def color_accessibility_column(ws, columns):
    col_idx = next((i for i, (key, *_rest) in enumerate(columns, start=1) if key == "accessibility"), None)
    if col_idx is None:
        return
    for row_cells in ws.iter_rows(min_row=2, min_col=col_idx, max_col=col_idx):
        for cell in row_cells:
            fill = ACCESSIBILITY_FILLS.get(cell.value)
            if fill is not None:
                cell.fill = fill


def build_outreach_sheet(wb, outreach_rows):
    ws = wb.create_sheet("OUTREACH")
    ordered = [outreach_rows[i] for i in priority_sort_key(outreach_rows)]
    write_table(ws, OUTREACH_COLUMNS, ordered)
    color_accessibility_column(ws, OUTREACH_COLUMNS)


def build_market_sheet(wb, market_rows):
    ws = wb.create_sheet("MARKET")
    write_table(ws, MARKET_COLUMNS, market_rows)
    color_accessibility_column(ws, MARKET_COLUMNS)


def build_excluded_sheet(wb, excluded_rows):
    ws = wb.create_sheet("EXCLUDED")
    write_table(ws, EXCLUDED_COLUMNS, excluded_rows)


def build_sources_sheet(wb, source_rows):
    ws = wb.create_sheet("SOURCES")
    write_table(ws, SOURCES_COLUMNS, source_rows)


def build_run_sheet(wb, run):
    ws = wb.create_sheet("RUN")
    bold = Font(bold=True)
    providers_text = "; ".join(f"{p['provider']}: {p['model']}" for p in run["providers"])
    pairs = [
        ("Sector", run.get("sector", "")),
        ("Geography", run.get("geography", "")),
        ("Campaign slug", run.get("campaign_slug", "")),
        ("Date", run.get("date", "")),
        ("Questions", "\n".join(run.get("questions", []))),
        ("Provider/model identifiers", providers_text),
        ("Expected responses", run.get("expected_responses", "")),
        ("Successful responses", run.get("successful_responses", "")),
        ("Raw data path", run.get("raw_data_path", "")),
        ("Methodology notes", run.get("methodology_notes", "")),
    ]
    for label, value in pairs:
        ws.append([label, value])
    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 70
    for row_cells in ws.iter_rows(min_row=1, max_row=len(pairs), min_col=1, max_col=1):
        for cell in row_cells:
            cell.font = bold
    for row_cells in ws.iter_rows(min_row=1, max_row=len(pairs), min_col=2, max_col=2):
        for cell in row_cells:
            cell.alignment = Alignment(wrap_text=True, vertical="top")


def build_workbook(data):
    wb = Workbook()
    wb.remove(wb.active)
    build_outreach_sheet(wb, data["outreach"])
    build_market_sheet(wb, data["market"])
    build_excluded_sheet(wb, data["excluded"])
    build_sources_sheet(wb, data["sources"])
    build_run_sheet(wb, data["run"])
    return wb


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", required=True, help="Campaign JSON file, matching schema.json")
    ap.add_argument("--output", required=True, help="Path to write the .xlsx workbook")
    args = ap.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Malformed JSON in {args.input}: {e}", file=sys.stderr)
            sys.exit(1)

    try:
        validate(data)
    except ValidationError as e:
        print(f"Invalid campaign data: {e}", file=sys.stderr)
        sys.exit(1)

    wb = build_workbook(data)
    wb.save(args.output)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
