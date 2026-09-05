#!/usr/bin/env python3
"""Query and write helpers over the CRM database. Not an ORM - thin
functions per table/view, kept deliberately simple and auditable.

compute_state_for_prospect() is the one function every page calls to turn
a prospect's stored research + activity history into a stage/next-action/
due-date, via cadence.compute_prospect_state() - the same rule the old
Excel workbook's formulas encoded, now evaluated directly in Python at
request time instead of being translated into a spreadsheet formula.
"""

from datetime import date, datetime, timezone

import cadence
import ingest

# ---------------------------------------------------------------------------
# Campaigns


def list_campaigns(conn):
    rows = conn.execute("SELECT * FROM campaigns ORDER BY campaign_id").fetchall()
    return [dict(r) for r in rows]


def get_campaign(conn, campaign_id):
    row = conn.execute("SELECT * FROM campaigns WHERE campaign_id = ?", (campaign_id,)).fetchone()
    return dict(row) if row else None


# ---------------------------------------------------------------------------
# Prospects

_PROSPECT_QUERY = """
    SELECT p.*, c.pipeline_stage AS campaign_pipeline_stage,
           c.sector AS sector, c.geography AS geography, c.run_date AS run_date
    FROM prospects p
    JOIN campaigns c ON c.campaign_id = p.campaign_id
"""


def list_prospects(conn, campaign_id=None):
    if campaign_id:
        rows = conn.execute(_PROSPECT_QUERY + " WHERE p.campaign_id = ? ORDER BY p.business",
                             (campaign_id,)).fetchall()
    else:
        rows = conn.execute(_PROSPECT_QUERY + " ORDER BY p.business").fetchall()
    return [dict(r) for r in rows]


def get_prospect(conn, prospect_id):
    row = conn.execute(_PROSPECT_QUERY + " WHERE p.prospect_id = ?", (prospect_id,)).fetchone()
    return dict(row) if row else None


def find_prospect(conn, business=None, company_number=None):
    """Read-only lookup for /qualify's optional CRM-backed research reuse
    (Stage 5/6, `.claude/skills/qualify/SKILL.md`): does this business
    already have a researched prospect record from a past campaign? Matches
    on the same business_key ingest.business_key_for() computes when
    writing a row - a verified company_number preferred, a slugified
    business name as fallback - across every campaign, returning the most
    recently imported match if more than one campaign has researched the
    same business. Never called by ingest itself; this is the only read
    path into `prospects` that runs *before* the row it might be reading -
    a business appearing in a run for the first time (the common case)
    simply gets no match, which is not an error."""
    if company_number and str(company_number).strip() and "[PLACEHOLDER]" not in str(company_number):
        key = f"cn-{ingest.slugify(str(company_number))}"
    elif business and business.strip():
        key = ingest.slugify(business)
    else:
        return None
    row = conn.execute(
        "SELECT * FROM prospects WHERE business_key = ? ORDER BY last_imported_at DESC LIMIT 1",
        (key,),
    ).fetchone()
    return dict(row) if row else None


def set_prospect_manual_fields(conn, prospect_id, do_not_contact_manual=None, notes=None):
    updates, params = [], {}
    if do_not_contact_manual is not None:
        updates.append("do_not_contact_manual = :do_not_contact_manual")
        params["do_not_contact_manual"] = 1 if do_not_contact_manual else 0
    if notes is not None:
        updates.append("notes = :notes")
        params["notes"] = notes
    if not updates:
        return
    params["prospect_id"] = prospect_id
    conn.execute(f"UPDATE prospects SET {', '.join(updates)} WHERE prospect_id = :prospect_id", params)
    conn.commit()


# ---------------------------------------------------------------------------
# Activities (sales pipeline - append-only, never touched by ingest)


def list_activities(conn, prospect_id):
    rows = conn.execute(
        "SELECT * FROM activities WHERE prospect_id = ? ORDER BY activity_date, id",
        (prospect_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def add_activity(conn, prospect_id, activity_type, activity_date, amount_gbp=None, plan=None, notes=None):
    conn.execute(
        """INSERT INTO activities (prospect_id, activity_type, activity_date, amount_gbp, plan, notes, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (prospect_id, activity_type, activity_date, amount_gbp, plan, notes,
         datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")),
    )
    conn.commit()


def list_recent_activities(conn, limit=50):
    rows = conn.execute(
        """SELECT a.*, p.business FROM activities a
           JOIN prospects p ON p.prospect_id = a.prospect_id
           ORDER BY a.activity_date DESC, a.id DESC LIMIT ?""",
        (limit,),
    ).fetchall()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Cadence settings (the editable Settings table)


def seed_cadence_if_empty(conn):
    count = conn.execute("SELECT COUNT(*) FROM cadence_settings").fetchone()[0]
    if count:
        return
    for i, row in enumerate(cadence.default_cadence_table()):
        conn.execute(
            """INSERT INTO cadence_settings
               (key, label, next_action_label, cadence_days, stage_label,
                stops_cold_followup, blocks_outreach, is_revenue_event, sort_order)
               VALUES (:key, :label, :next_action_label, :cadence_days, :stage_label,
                       :stops_cold_followup, :blocks_outreach, :is_revenue_event, :sort_order)""",
            {**row, "stops_cold_followup": int(row["stops_cold_followup"]),
             "blocks_outreach": int(row["blocks_outreach"]),
             "is_revenue_event": int(row["is_revenue_event"]), "sort_order": i},
        )
    conn.commit()


def migrate_cadence_defaults(conn):
    """Add sequence rows to existing databases without overwriting edits."""
    existing = {r["key"]: dict(r) for r in conn.execute("SELECT * FROM cadence_settings")}
    if not existing:
        return
    next_order = max(r["sort_order"] for r in existing.values()) + 1
    for row in cadence.default_cadence_table():
        if row["key"] not in existing:
            conn.execute(
                """INSERT INTO cadence_settings
                   (key, label, next_action_label, cadence_days, stage_label,
                    stops_cold_followup, blocks_outreach, is_revenue_event, sort_order)
                   VALUES (:key, :label, :next_action_label, :cadence_days, :stage_label,
                           :stops_cold_followup, :blocks_outreach, :is_revenue_event, :sort_order)""",
                {**row, "stops_cold_followup": int(row["stops_cold_followup"]),
                 "blocks_outreach": int(row["blocks_outreach"]),
                 "is_revenue_event": int(row["is_revenue_event"]), "sort_order": next_order},
            )
            next_order += 1
    legacy = existing.get("EMAIL_2_SENT")
    if legacy and (legacy["next_action_label"], legacy["cadence_days"], legacy["stage_label"]) == (
        "Try LinkedIn or call", 5, "Contacted"
    ):
        new = cadence.cadence_by_key()["EMAIL_2_SENT"]
        conn.execute(
            """UPDATE cadence_settings SET label=?, next_action_label=?, cadence_days=?,
               stage_label=?, stops_cold_followup=?, blocks_outreach=?, is_revenue_event=?
               WHERE key='EMAIL_2_SENT'""",
            (new["label"], new["next_action_label"], new["cadence_days"], new["stage_label"],
             int(new["stops_cold_followup"]), int(new["blocks_outreach"]), int(new["is_revenue_event"])),
        )


def list_cadence_settings(conn):
    rows = conn.execute("SELECT * FROM cadence_settings ORDER BY sort_order").fetchall()
    return [dict(r) for r in rows]


def cadence_dict_from_db(conn):
    out = {}
    for row in list_cadence_settings(conn):
        out[row["key"]] = {
            "key": row["key"], "label": row["label"],
            "next_action_label": row["next_action_label"],
            "cadence_days": row["cadence_days"], "stage_label": row["stage_label"],
            "stops_cold_followup": bool(row["stops_cold_followup"]),
            "blocks_outreach": bool(row["blocks_outreach"]),
            "is_revenue_event": bool(row["is_revenue_event"]),
        }
    return out


def update_cadence_setting(conn, key, next_action_label, cadence_days, stage_label,
                            stops_cold_followup, blocks_outreach, is_revenue_event):
    conn.execute(
        """UPDATE cadence_settings SET next_action_label=?, cadence_days=?, stage_label=?,
           stops_cold_followup=?, blocks_outreach=?, is_revenue_event=? WHERE key=?""",
        (next_action_label, cadence_days, stage_label, int(stops_cold_followup),
         int(blocks_outreach), int(is_revenue_event), key),
    )
    conn.commit()


# ---------------------------------------------------------------------------
# Stage/next-action computation - the cadence engine wired to real data


def compute_state_for_prospect(conn, prospect, cadence_table=None, today=None):
    cadence_table = cadence_table if cadence_table is not None else cadence_dict_from_db(conn)
    research = {
        "pipeline_stage": prospect.get("campaign_pipeline_stage"),
        "ready_to_email": prospect.get("ready_to_email"),
        "withheld_at_outreach": bool(prospect.get("withheld_at_outreach")),
    }
    activities = [
        {"id": a["id"], "activity_type": a["activity_type"], "activity_date": date.fromisoformat(a["activity_date"])}
        for a in list_activities(conn, prospect["prospect_id"])
    ]
    return cadence.compute_prospect_state(
        research, activities,
        manual_do_not_contact=bool(prospect.get("do_not_contact_manual")),
        cadence=cadence_table, today=today,
    )


def prospects_with_state(conn, campaign_id=None, today=None):
    cadence_table = cadence_dict_from_db(conn)
    out = []
    for p in list_prospects(conn, campaign_id=campaign_id):
        state = compute_state_for_prospect(conn, p, cadence_table=cadence_table, today=today)
        out.append({**p, "state": state})
    return out


def today_summary(conn):
    today = date.today()
    rows = prospects_with_state(conn, today=today)
    overdue, due_today, upcoming, outreach_ready, replies = [], [], [], [], []
    for row in rows:
        state = row["state"]
        due = state["next_action_due_date"]
        if state["stage"] == "Replied":
            replies.append(row)
        if state["stage"] == "Outreach ready":
            outreach_ready.append(row)
        if state["overdue"]:
            overdue.append(row)
        elif due == today:
            due_today.append(row)
        elif due and 0 < (due - today).days <= 7:
            upcoming.append(row)
    return {
        "overdue": overdue, "due_today": due_today, "upcoming": upcoming,
        "outreach_ready": outreach_ready, "replies": replies,
    }


def pipeline_funnel(conn):
    rows = prospects_with_state(conn)
    counts = {}
    for row in rows:
        stage = row["state"]["stage"] or "(none)"
        counts[stage] = counts.get(stage, 0) + 1
    return counts


def campaign_rollup(conn):
    rows = prospects_with_state(conn)
    by_campaign = {}
    for row in rows:
        cid = row["campaign_id"]
        by_campaign.setdefault(cid, {}).setdefault(row["state"]["stage"] or "(none)", 0)
        by_campaign[cid][row["state"]["stage"] or "(none)"] += 1
    campaigns = list_campaigns(conn)
    return [{"campaign": c, "stage_counts": by_campaign.get(c["campaign_id"], {})} for c in campaigns]


# ---------------------------------------------------------------------------
# Revenue - a display-only sum over activities flagged is_revenue_event.
# No invoicing, no payment status: a typed-in amount against a sold/started
# activity, same convention the Excel Activities sheet already used.


def revenue_activities(conn):
    cadence_by_key = cadence_dict_from_db(conn)
    revenue_types = [k for k, v in cadence_by_key.items() if v["is_revenue_event"]]
    if not revenue_types:
        return []
    placeholders = ", ".join("?" for _ in revenue_types)
    rows = conn.execute(
        f"""SELECT a.*, p.business FROM activities a
            JOIN prospects p ON p.prospect_id = a.prospect_id
            WHERE a.activity_type IN ({placeholders})
            ORDER BY a.activity_date""",
        revenue_types,
    ).fetchall()
    return [dict(r) for r in rows]


def revenue_summary(conn):
    items = revenue_activities(conn)
    monthly = {}
    running_total = 0.0
    itemised = []
    for item in items:
        amount = item["amount_gbp"] or 0
        running_total += amount
        month = item["activity_date"][:7]
        monthly[month] = monthly.get(month, 0) + amount
        itemised.append({**item, "running_total": running_total})
    return {"itemised": itemised, "monthly": monthly, "total": running_total}


# ---------------------------------------------------------------------------
# Clients - structured record + append-only service activity log


def list_clients(conn):
    # Soonest check-in/deletion due first, nulls last - a to-look-at list,
    # not an alphabetical one, per playbook/records-and-data.md's "deletion
    # is something you do by looking rather than by remembering".
    rows = conn.execute(
        """SELECT * FROM clients
           ORDER BY (next_checkin_due_date IS NULL), next_checkin_due_date,
                    (retention_deletion_due_date IS NULL), retention_deletion_due_date,
                    business"""
    ).fetchall()
    return [dict(r) for r in rows]


def get_client(conn, client_id):
    row = conn.execute("SELECT * FROM clients WHERE client_id = ?", (client_id,)).fetchone()
    return dict(row) if row else None


def create_client(conn, fields):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    fields = {**fields, "created_at": now, "updated_at": now}
    columns = list(fields.keys())
    conn.execute(
        f"INSERT INTO clients ({', '.join(columns)}) VALUES ({', '.join(':' + c for c in columns)})",
        fields,
    )
    conn.commit()
    return conn.execute("SELECT last_insert_rowid()").fetchone()[0]


def update_client(conn, client_id, fields):
    fields = dict(fields)
    fields["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    fields["client_id"] = client_id
    set_clause = ", ".join(f"{c} = :{c}" for c in fields if c != "client_id")
    conn.execute(f"UPDATE clients SET {set_clause} WHERE client_id = :client_id", fields)
    conn.commit()


def list_client_activities(conn, client_id):
    rows = conn.execute(
        "SELECT * FROM client_activities WHERE client_id = ? ORDER BY activity_date DESC, id DESC",
        (client_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def add_client_activity(conn, client_id, activity_type, activity_date, notes=None):
    conn.execute(
        """INSERT INTO client_activities (client_id, activity_type, activity_date, notes, created_at)
           VALUES (?, ?, ?, ?, ?)""",
        (client_id, activity_type, activity_date, notes,
         datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")),
    )
    conn.commit()


# ---------------------------------------------------------------------------
# Import log


def list_import_log(conn, limit=500):
    rows = conn.execute(
        "SELECT * FROM import_log ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    return [dict(r) for r in rows]
