#!/usr/bin/env python3
"""The Wardith CRM's Flask app: local-only, single-user, server-rendered
pages backed by the SQLite database in db.py. No JSON API, no client-side
framework - a form and a redirect covers every write path.

Never bind this to anything but 127.0.0.1 (see main.py) - there is no
authentication because there is exactly one user and it never leaves the
owner's own machine.
"""

import csv
import io
from datetime import date, datetime, timezone
from pathlib import Path

from flask import Flask, g, redirect, render_template, request, Response, url_for

import cadence
import db as db_mod
import ingest
import models


def create_app(db_path=None, runs_dir=None):
    app = Flask(__name__)
    runs_dir = Path(runs_dir).expanduser() if runs_dir else Path.home() / "wardith-runs"
    app.config["RUNS_DIR"] = runs_dir
    app.config["DB_PATH"] = Path(db_path).expanduser() if db_path else runs_dir / "crm" / "wardith.db"

    def get_db():
        if "db" not in g:
            g.db = db_mod.connect(app.config["DB_PATH"])
            db_mod.init_db(g.db)
            models.seed_cadence_if_empty(g.db)
        return g.db

    @app.teardown_appcontext
    def close_db(exception=None):
        conn = g.pop("db", None)
        if conn is not None:
            conn.close()

    @app.context_processor
    def inject_today():
        return {"today": date.today()}

    # -- Today -------------------------------------------------------------

    @app.route("/")
    def today():
        conn = get_db()
        return render_template("today.html", summary=models.today_summary(conn))

    @app.route("/ingest", methods=["POST"])
    def run_ingest():
        conn = get_db()
        n_campaigns, n_prospects, warnings = ingest.import_all(conn, app.config["RUNS_DIR"])
        ingest.record_import_log(conn, warnings)
        conn.commit()
        return redirect(url_for("today", ingested=1, campaigns=n_campaigns, prospects=n_prospects))

    # -- Prospects -----------------------------------------------------------

    @app.route("/prospects")
    def prospects_list():
        conn = get_db()
        campaign_id = request.args.get("campaign_id") or None
        rows = models.prospects_with_state(conn, campaign_id=campaign_id)
        return render_template("prospects_list.html", prospects=rows,
                                campaigns=models.list_campaigns(conn), campaign_id=campaign_id)

    @app.route("/prospects/<prospect_id>", methods=["GET", "POST"])
    def prospect_detail(prospect_id):
        conn = get_db()
        prospect = models.get_prospect(conn, prospect_id)
        if prospect is None:
            return Response("Prospect not found", status=404)

        if request.method == "POST":
            form = request.form
            if form.get("form") == "activity":
                models.add_activity(
                    conn, prospect_id,
                    activity_type=form["activity_type"],
                    activity_date=form["activity_date"],
                    amount_gbp=float(form["amount_gbp"]) if form.get("amount_gbp") else None,
                    plan=form.get("plan") or None,
                    notes=form.get("notes") or None,
                )
            elif form.get("form") == "manual_fields":
                models.set_prospect_manual_fields(
                    conn, prospect_id,
                    do_not_contact_manual=bool(form.get("do_not_contact_manual")),
                    notes=form.get("notes", ""),
                )
            return redirect(url_for("prospect_detail", prospect_id=prospect_id))

        state = models.compute_state_for_prospect(conn, prospect)
        activities = list(reversed(models.list_activities(conn, prospect_id)))
        return render_template(
            "prospect_detail.html", prospect=prospect, state=state, activities=activities,
            cadence_types=cadence.default_cadence_table(),
        )

    @app.route("/prospects/<prospect_id>/convert-to-client", methods=["POST"])
    def convert_to_client(prospect_id):
        conn = get_db()
        prospect = models.get_prospect(conn, prospect_id)
        if prospect is None:
            return Response("Prospect not found", status=404)
        client_id = models.create_client(conn, {
            "prospect_id": prospect_id,
            "business": prospect["business"],
            "contact_person": prospect["contact_person"],
            "role": prospect["role"],
            "contact_email": prospect["contact_email"],
            "contact_phone": prospect["contact_phone"],
        })
        return redirect(url_for("client_detail", client_id=client_id))

    # -- Activities (sales log) --------------------------------------------

    @app.route("/activities")
    def activities_log():
        conn = get_db()
        return render_template(
            "activities_log.html", activities=models.list_recent_activities(conn),
            prospects=models.list_prospects(conn), cadence_types=cadence.default_cadence_table(),
        )

    @app.route("/activities/new", methods=["POST"])
    def activities_new():
        conn = get_db()
        form = request.form
        models.add_activity(
            conn, form["prospect_id"], activity_type=form["activity_type"],
            activity_date=form["activity_date"],
            amount_gbp=float(form["amount_gbp"]) if form.get("amount_gbp") else None,
            plan=form.get("plan") or None, notes=form.get("notes") or None,
        )
        return redirect(url_for("activities_log"))

    # -- Campaigns / Pipeline / Revenue --------------------------------------

    @app.route("/campaigns")
    def campaigns_view():
        conn = get_db()
        return render_template("campaigns.html", rollup=models.campaign_rollup(conn))

    @app.route("/pipeline")
    def pipeline_view():
        conn = get_db()
        return render_template("pipeline.html", funnel=models.pipeline_funnel(conn),
                                rollup=models.campaign_rollup(conn))

    @app.route("/revenue")
    def revenue_view():
        conn = get_db()
        return render_template("revenue.html", summary=models.revenue_summary(conn))

    # -- Settings (editable cadence table) -----------------------------------

    @app.route("/settings/cadence", methods=["GET", "POST"])
    def settings_cadence():
        conn = get_db()
        if request.method == "POST":
            form = request.form
            for key in form.getlist("key"):
                models.update_cadence_setting(
                    conn, key,
                    next_action_label=form.get(f"next_action_label__{key}", ""),
                    cadence_days=int(form[f"cadence_days__{key}"]) if form.get(f"cadence_days__{key}") else None,
                    stage_label=form.get(f"stage_label__{key}", ""),
                    stops_cold_followup=form.get(f"stops_cold_followup__{key}") == "on",
                    blocks_outreach=form.get(f"blocks_outreach__{key}") == "on",
                    is_revenue_event=form.get(f"is_revenue_event__{key}") == "on",
                )
            return redirect(url_for("settings_cadence"))
        return render_template("settings_cadence.html", rows=models.list_cadence_settings(conn))

    # -- Import log -----------------------------------------------------------

    @app.route("/import-log")
    def import_log_view():
        conn = get_db()
        return render_template("import_log.html", entries=models.list_import_log(conn))

    # -- Clients ---------------------------------------------------------------

    @app.route("/clients")
    def clients_list():
        conn = get_db()
        return render_template("clients_list.html", clients=models.list_clients(conn))

    @app.route("/clients/new", methods=["GET", "POST"])
    def clients_new():
        conn = get_db()
        if request.method == "POST":
            form = request.form
            client_id = models.create_client(conn, {
                "business": form["business"], "contact_person": form.get("contact_person") or None,
                "role": form.get("role") or None, "contact_email": form.get("contact_email") or None,
                "contact_phone": form.get("contact_phone") or None,
            })
            return redirect(url_for("client_detail", client_id=client_id))
        return render_template("client_detail.html", client=None, activities=[])

    @app.route("/clients/<int:client_id>", methods=["GET", "POST"])
    def client_detail(client_id):
        conn = get_db()
        client = models.get_client(conn, client_id)
        if client is None:
            return Response("Client not found", status=404)

        if request.method == "POST":
            form = request.form
            if form.get("form") == "client_activity":
                models.add_client_activity(
                    conn, client_id, activity_type=form["activity_type"],
                    activity_date=form["activity_date"], notes=form.get("notes") or None,
                )
            else:
                models.update_client(conn, client_id, {
                    "business": form["business"],
                    "contact_person": form.get("contact_person") or None,
                    "role": form.get("role") or None,
                    "contact_email": form.get("contact_email") or None,
                    "contact_phone": form.get("contact_phone") or None,
                    "plan_tier": form.get("plan_tier") or None,
                    "audit_sold_date": form.get("audit_sold_date") or None,
                    "audit_completed_date": form.get("audit_completed_date") or None,
                    "foundation_sold_date": form.get("foundation_sold_date") or None,
                    "foundation_completed_date": form.get("foundation_completed_date") or None,
                    "ongoing_started_date": form.get("ongoing_started_date") or None,
                    "retention_deletion_due_date": form.get("retention_deletion_due_date") or None,
                    "next_checkin_due_date": form.get("next_checkin_due_date") or None,
                    "do_not_contact": 1 if form.get("do_not_contact") else 0,
                    "notes": form.get("notes", ""),
                })
            return redirect(url_for("client_detail", client_id=client_id))

        return render_template(
            "client_detail.html", client=client,
            activities=models.list_client_activities(conn, client_id),
        )

    # -- CSV export (read-only) -----------------------------------------------

    def _csv_response(fieldnames, rows, filename):
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
        return Response(
            buf.getvalue(), mimetype="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )

    @app.route("/export/prospects.csv")
    def export_prospects():
        conn = get_db()
        rows = models.prospects_with_state(conn)
        for r in rows:
            r["stage"] = r["state"]["stage"]
            r["next_action"] = r["state"]["next_action"]
            r["next_action_due_date"] = r["state"]["next_action_due_date"]
        fields = ["prospect_id", "campaign_id", "business", "area", "priority",
                  "opportunity_type", "accessibility", "contact_person", "role",
                  "contact_email", "contact_phone", "ready_to_email", "stage",
                  "next_action", "next_action_due_date", "do_not_contact_manual", "notes"]
        return _csv_response(fields, rows, "prospects.csv")

    @app.route("/export/clients.csv")
    def export_clients():
        conn = get_db()
        fields = ["client_id", "business", "contact_person", "role", "contact_email",
                  "contact_phone", "plan_tier", "audit_sold_date", "foundation_sold_date",
                  "ongoing_started_date", "retention_deletion_due_date",
                  "next_checkin_due_date", "do_not_contact", "notes"]
        return _csv_response(fields, models.list_clients(conn), "clients.csv")

    @app.route("/export/activities.csv")
    def export_activities():
        conn = get_db()
        fields = ["id", "prospect_id", "business", "activity_type", "activity_date",
                  "amount_gbp", "plan", "notes"]
        return _csv_response(fields, models.list_recent_activities(conn, limit=100000), "activities.csv")

    return app
