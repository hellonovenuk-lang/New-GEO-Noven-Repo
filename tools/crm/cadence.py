#!/usr/bin/env python3
"""Cadence and pipeline-stage rules used by the CRM app, its tests, and
every page that shows a prospect's stage/next action/due date.

Ported unchanged from tools/tracker/cadence.py (see that file's own
history) - it was already stdlib-only and fully decoupled from Excel, so
the only thing that changed moving it here is where it's called from: a
Flask route computing state at request time against real database rows,
instead of build_crm.py translating it into Excel formula strings. Keep
this file and tools/tracker/cadence.py in sync until tools/tracker/ is
retired.

Editable without touching code: every column in default_cadence_table()
becomes an editable row in the cadence_settings table via the Settings
page. Changing a cadence_days value or a next_action_label there changes
what the CRM recommends immediately, on the next page load - changing the
code changes nothing else.
"""
from datetime import date, timedelta

# (key, label, next_action_label, cadence_days, stage_label,
#  stops_cold_followup, blocks_outreach, is_revenue_event)
ACTIVITY_TYPES = [
    ("OUTREACH_PREPARED", "Outreach prepared", "Send Email 1", 1, "Prepared",
     False, False, False),
    ("EMAIL_1_SENT", "Email 1 sent", "Send Email 2 / follow-up", 5, "Contacted",
     False, False, False),
    ("EMAIL_2_SENT", "Email 2 / follow-up sent", "Try LinkedIn or call", 5, "Contacted",
     False, False, False),
    ("LINKEDIN_VIEWED", "LinkedIn viewed", "Send LinkedIn connection request", 2, "Contacted",
     False, False, False),
    ("LINKEDIN_FOLLOWED", "LinkedIn followed", "Send LinkedIn connection request", 2, "Contacted",
     False, False, False),
    ("LINKEDIN_CONNECTION_SENT", "LinkedIn connection sent", "Check connection / follow up", 5, "Contacted",
     False, False, False),
    ("LINKEDIN_CONNECTION_ACCEPTED", "LinkedIn connection accepted", "Send LinkedIn message", 1, "Contacted",
     False, False, False),
    ("LINKEDIN_MESSAGE_SENT", "LinkedIn message sent", "Follow up or call", 5, "Contacted",
     False, False, False),
    ("PHONE_CALL", "Phone call", "Follow up", 5, "Contacted",
     False, False, False),
    ("REPLY_RECEIVED", "Reply received", "Respond to reply / book meeting", 1, "Replied",
     True, False, False),
    ("MEETING_BOOKED", "Meeting booked", "Prepare / deliver the audit", 1, "Meeting",
     True, False, False),
    ("AUDIT_SOLD", "Audit sold", "Deliver the audit", 3, "Audit",
     True, False, True),
    ("AUDIT_COMPLETED", "Audit completed", "Propose the Foundation", 3, "Audit",
     True, False, False),
    ("FOUNDATION_SOLD", "Foundation sold", "Deliver the Foundation", 7, "Foundation",
     True, False, True),
    ("FOUNDATION_COMPLETED", "Foundation completed", "Propose an ongoing plan", 7, "Foundation",
     True, False, False),
    ("ONGOING_STARTED", "Ongoing plan started", "Ongoing - periodic check-in", 30, "Ongoing",
     True, False, True),
    ("LOST", "Lost / rejected", "", None, "Lost",
     True, False, False),
    ("OPTED_OUT", "Opted out", "", None, "Do Not Contact",
     True, True, False),
]

CADENCE_FIELDS = [
    "key", "label", "next_action_label", "cadence_days", "stage_label",
    "stops_cold_followup", "blocks_outreach", "is_revenue_event",
]

NON_TERMINAL_STAGES = {"Prepared", "Contacted"}


def default_cadence_table():
    return [dict(zip(CADENCE_FIELDS, row)) for row in ACTIVITY_TYPES]


def cadence_by_key(table=None):
    table = table if table is not None else default_cadence_table()
    return {row["key"]: row for row in table}


def adjust_for_weekend(d):
    """Saturday -> Monday, Sunday -> Monday. Mirrors the workbook's own
    WEEKDAY(cell,2) formula (Monday=1..Sunday=7) so Python and Excel never
    disagree on a due date."""
    wd = d.isoweekday()
    if wd == 6:
        return d + timedelta(days=2)
    if wd == 7:
        return d + timedelta(days=1)
    return d


def due_date(last_activity_date, cadence_days):
    if last_activity_date is None or cadence_days is None:
        return None
    return adjust_for_weekend(last_activity_date + timedelta(days=cadence_days))


def compute_prospect_state(research, activities, manual_do_not_contact=False, cadence=None, today=None):
    """activities: an iterable of {'activity_type': str, 'activity_date': date}
    for ONE prospect, any order. research: the prospect's research fields
    (pipeline_stage, ready_to_email, withheld_at_outreach at minimum).

    Returns {stage, last_activity_type, last_activity_date, next_action,
    next_action_due_date, blocked, do_not_contact, overdue}.
    """
    cadence = cadence if cadence is not None else cadence_by_key()
    today = today or date.today()
    activities = list(activities)

    permanently_blocked = bool(manual_do_not_contact) or any(
        cadence.get(a["activity_type"], {}).get("blocks_outreach") for a in activities
    )
    sorted_activities = sorted(activities, key=lambda a: a["activity_date"])
    last = sorted_activities[-1] if sorted_activities else None

    if permanently_blocked:
        return {
            "stage": "Do Not Contact",
            "last_activity_type": last["activity_type"] if last else None,
            "last_activity_date": last["activity_date"] if last else None,
            "next_action": "", "next_action_due_date": None,
            "blocked": True, "do_not_contact": True, "overdue": False,
        }

    if last is None:
        research = research or {}
        pipeline_stage = research.get("pipeline_stage")
        ready = research.get("ready_to_email") == "YES"
        withheld = bool(research.get("withheld_at_outreach"))
        if ready and not withheld:
            return {
                "stage": "Outreach ready", "last_activity_type": None, "last_activity_date": None,
                "next_action": "Send Email 1", "next_action_due_date": today,
                "blocked": False, "do_not_contact": False, "overdue": False,
            }
        if pipeline_stage == "RESEARCHED":
            stage = "Research complete"
        elif pipeline_stage:
            # QUALIFIED, or a campaign that reached OUTREACH_PREPARED but
            # left this particular prospect withheld/REVIEW - either way,
            # qualified-but-not-personally-actionable-yet is "Qualified",
            # never the campaign's own raw internal stage name.
            stage = "Qualified"
        else:
            stage = ""
        return {
            "stage": stage, "last_activity_type": None, "last_activity_date": None,
            "next_action": "", "next_action_due_date": None,
            "blocked": False, "do_not_contact": False, "overdue": False,
        }

    rule = cadence.get(last["activity_type"], {})
    stage = rule.get("stage_label", "")
    next_action = rule.get("next_action_label") or ""
    due = due_date(last["activity_date"], rule.get("cadence_days"))
    overdue = bool(due and due < today)
    if stage in NON_TERMINAL_STAGES and overdue:
        stage = "Follow-up due"

    return {
        "stage": stage, "last_activity_type": last["activity_type"], "last_activity_date": last["activity_date"],
        "next_action": next_action, "next_action_due_date": due,
        "blocked": False, "do_not_contact": False, "overdue": overdue,
    }
