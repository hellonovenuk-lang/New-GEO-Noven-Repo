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
    ("EMAIL_1_SENT", "Email 1 sent", "Send Email 2", 5, "Contacted",
     False, False, False),
    ("EMAIL_2_SENT", "Email 2 sent", "Send Email 3", 7, "Contacted",
     False, False, False),
    ("EMAIL_3_SENT", "Email 3 sent", "", None, "Cold sequence complete",
     True, False, False),
    ("EMAIL_BOUNCED", "Email bounced", "Verify contact route before reopening", None, "Contact hold",
     True, False, False),
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
    """Kept for callers outside the CRM: move a weekend date to Monday."""
    while d.isoweekday() > 5:
        d += timedelta(days=1)
    return d


def add_business_days(d, business_days):
    """Return the date after N Monday-Friday business days."""
    for _ in range(business_days):
        d += timedelta(days=1)
        while d.isoweekday() > 5:
            d += timedelta(days=1)
    return d


def due_date(last_activity_date, cadence_days):
    if last_activity_date is None or cadence_days is None:
        return None
    return add_business_days(last_activity_date, cadence_days)


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

    opted_out = any(
        cadence.get(a["activity_type"], {}).get("blocks_outreach") for a in activities
    )
    sorted_activities = sorted(activities, key=lambda a: (a["activity_date"], a.get("id", 0)))
    last = sorted_activities[-1] if sorted_activities else None

    if opted_out:
        return {
            "stage": "Do Not Contact",
            "last_activity_type": last["activity_type"] if last else None,
            "last_activity_date": last["activity_date"] if last else None,
            "next_action": "", "next_action_due_date": None,
            "blocked": True, "do_not_contact": True, "overdue": False, "sequence_complete": False,
        }

    # Existing CRM records used the legacy manual field for temporary bounce
    # holds. It must block cold follow-up without being relabelled an opt-out.
    if manual_do_not_contact:
        return {
            "stage": "Contact hold",
            "last_activity_type": last["activity_type"] if last else None,
            "last_activity_date": last["activity_date"] if last else None,
            "next_action": "Verify contact route before reopening",
            "next_action_due_date": None,
            "blocked": True, "do_not_contact": False, "overdue": False, "sequence_complete": False,
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
                "blocked": False, "do_not_contact": False, "overdue": False, "sequence_complete": False,
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
            "blocked": False, "do_not_contact": False, "overdue": False, "sequence_complete": False,
        }

    # Incidental activity (for example a LinkedIn view) must never displace a
    # reply, sale/client stage, hold, or a completed cold sequence.
    state_activity = next(
        (a for a in reversed(sorted_activities)
         if cadence.get(a["activity_type"], {}).get("stops_cold_followup")),
        last,
    )
    rule = cadence.get(state_activity["activity_type"], {})
    stage = rule.get("stage_label", "")
    next_action = rule.get("next_action_label") or ""
    due = due_date(state_activity["activity_date"], rule.get("cadence_days"))
    overdue = bool(due and due < today)
    if stage in NON_TERMINAL_STAGES and overdue:
        stage = "Follow-up due"

    return {
        "stage": stage, "last_activity_type": state_activity["activity_type"], "last_activity_date": state_activity["activity_date"],
        "next_action": next_action, "next_action_due_date": due,
        "blocked": False, "do_not_contact": False, "overdue": overdue,
        "sequence_complete": state_activity["activity_type"] == "EMAIL_3_SENT",
    }
