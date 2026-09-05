import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cadence as c


class TestWeekendHandling(unittest.TestCase):
    def test_saturday_moves_to_monday(self):
        self.assertEqual(c.adjust_for_weekend(date(2026, 8, 15)), date(2026, 8, 17))  # Sat -> Mon

    def test_sunday_moves_to_monday(self):
        self.assertEqual(c.adjust_for_weekend(date(2026, 8, 16)), date(2026, 8, 17))  # Sun -> Mon

    def test_weekday_is_unchanged(self):
        self.assertEqual(c.adjust_for_weekend(date(2026, 8, 17)), date(2026, 8, 17))  # Mon


class TestDueDateCalculation(unittest.TestCase):
    def test_due_date_adds_business_days_with_no_weekend_crossing(self):
        self.assertEqual(date(2026, 8, 10).isoweekday(), 1)  # Monday
        self.assertEqual(c.due_date(date(2026, 8, 10), 1), date(2026, 8, 11))  # Tuesday, no adjustment

    def test_due_date_counts_weekdays_not_calendar_days(self):
        # Monday + five business days is the following Monday.
        self.assertEqual(date(2026, 8, 10).isoweekday(), 1)
        self.assertEqual(c.due_date(date(2026, 8, 10), 5), date(2026, 8, 17))

    def test_no_activity_or_no_cadence_days_gives_no_due_date(self):
        self.assertIsNone(c.due_date(None, 5))
        self.assertIsNone(c.due_date(date(2026, 8, 10), None))


class TestCadenceEditability(unittest.TestCase):
    def test_editing_the_cadence_table_changes_the_computed_due_date_without_code_changes(self):
        table = c.cadence_by_key()
        table["EMAIL_1_SENT"]["cadence_days"] = 10
        state = c.compute_prospect_state(
            {}, [{"activity_type": "EMAIL_1_SENT", "activity_date": date(2026, 8, 3)}],
            cadence=table, today=date(2026, 8, 10),
        )
        self.assertEqual(state["next_action_due_date"], date(2026, 8, 17))  # Mon 08-03 + 10 business days = Mon 08-17


class TestProspectState(unittest.TestCase):
    def test_no_activity_ready_to_email_is_outreach_ready_due_today(self):
        state = c.compute_prospect_state(
            {"pipeline_stage": "OUTREACH_PREPARED", "ready_to_email": "YES", "withheld_at_outreach": False},
            [], today=date(2026, 8, 16),
        )
        self.assertEqual(state["stage"], "Outreach ready")
        self.assertEqual(state["next_action"], "Send Email 1")
        self.assertEqual(state["next_action_due_date"], date(2026, 8, 16))

    def test_withheld_prospect_is_not_outreach_ready(self):
        state = c.compute_prospect_state(
            {"pipeline_stage": "OUTREACH_PREPARED", "ready_to_email": "YES", "withheld_at_outreach": True},
            [], today=date(2026, 8, 16),
        )
        self.assertNotEqual(state["stage"], "Outreach ready")

    def test_withheld_or_review_prospect_reads_as_qualified_not_a_raw_pipeline_stage(self):
        # A campaign that reached OUTREACH_PREPARED but left this specific
        # prospect withheld/REVIEW should never surface the campaign's own
        # internal stage string on the CRM funnel - it belongs in the same
        # "Qualified" bucket as any other not-yet-actionable prospect.
        state = c.compute_prospect_state(
            {"pipeline_stage": "OUTREACH_PREPARED", "ready_to_email": "REVIEW", "withheld_at_outreach": False},
            [], today=date(2026, 8, 16),
        )
        self.assertEqual(state["stage"], "Qualified")

    def test_qualified_with_no_activity_reads_research_complete_style_stage(self):
        state = c.compute_prospect_state({"pipeline_stage": "QUALIFIED", "ready_to_email": "REVIEW"}, [])
        self.assertEqual(state["stage"], "Qualified")
        self.assertEqual(state["next_action"], "")

    def test_email_1_sent_recommends_email_2_within_cadence(self):
        state = c.compute_prospect_state(
            {}, [{"activity_type": "EMAIL_1_SENT", "activity_date": date(2026, 8, 10)}],
            today=date(2026, 8, 12),
        )
        self.assertEqual(state["stage"], "Contacted")
        self.assertEqual(state["next_action"], "Send Email 2")
        self.assertFalse(state["overdue"])

    def test_overdue_contact_becomes_follow_up_due(self):
        # Monday 08-10 + 5 days = Saturday 08-15 -> Monday 08-17. "Today" past that = overdue.
        state = c.compute_prospect_state(
            {}, [{"activity_type": "EMAIL_1_SENT", "activity_date": date(2026, 8, 10)}],
            today=date(2026, 8, 20),
        )
        self.assertEqual(state["stage"], "Follow-up due")
        self.assertTrue(state["overdue"])

    def test_reply_received_stops_cold_followup_recommendation(self):
        state = c.compute_prospect_state(
            {},
            [
                {"activity_type": "EMAIL_1_SENT", "activity_date": date(2026, 8, 1)},
                {"activity_type": "REPLY_RECEIVED", "activity_date": date(2026, 8, 5)},
            ],
            today=date(2026, 8, 20),
        )
        self.assertEqual(state["stage"], "Replied")
        self.assertNotIn("Email", state["next_action"])
        self.assertEqual(state["next_action"], "Respond to reply / book meeting")

    def test_reply_received_never_reverts_to_follow_up_due_even_long_after(self):
        state = c.compute_prospect_state(
            {}, [{"activity_type": "REPLY_RECEIVED", "activity_date": date(2026, 1, 1)}],
            today=date(2026, 8, 20),
        )
        self.assertEqual(state["stage"], "Replied")

    def test_meeting_booked_stops_cold_followup(self):
        state = c.compute_prospect_state(
            {}, [
                {"activity_type": "EMAIL_1_SENT", "activity_date": date(2026, 8, 1)},
                {"activity_type": "REPLY_RECEIVED", "activity_date": date(2026, 8, 2)},
                {"activity_type": "MEETING_BOOKED", "activity_date": date(2026, 8, 3)},
            ],
            today=date(2026, 8, 20),
        )
        self.assertEqual(state["stage"], "Meeting")

    def test_lost_stops_cold_followup_but_is_not_a_permanent_block(self):
        state = c.compute_prospect_state(
            {}, [{"activity_type": "LOST", "activity_date": date(2026, 8, 1)}],
            today=date(2026, 8, 20),
        )
        self.assertEqual(state["stage"], "Lost")
        self.assertEqual(state["next_action"], "")
        self.assertFalse(state["blocked"])

    def test_opted_out_permanently_blocks_outreach(self):
        state = c.compute_prospect_state(
            {}, [
                {"activity_type": "EMAIL_1_SENT", "activity_date": date(2026, 8, 1)},
                {"activity_type": "OPTED_OUT", "activity_date": date(2026, 8, 2)},
            ],
            today=date(2026, 8, 20),
        )
        self.assertEqual(state["stage"], "Do Not Contact")
        self.assertTrue(state["blocked"])
        self.assertTrue(state["do_not_contact"])
        self.assertEqual(state["next_action"], "")
        self.assertIsNone(state["next_action_due_date"])

    def test_opt_out_blocks_even_if_a_later_activity_was_somehow_logged(self):
        # Opt-out is permanent per playbook/records-and-data.md's retention table -
        # it must win regardless of chronological position in the log.
        state = c.compute_prospect_state(
            {}, [
                {"activity_type": "OPTED_OUT", "activity_date": date(2026, 8, 2)},
                {"activity_type": "EMAIL_1_SENT", "activity_date": date(2026, 8, 5)},
            ],
            today=date(2026, 8, 20),
        )
        self.assertTrue(state["blocked"])

    def test_manual_do_not_contact_blocks_even_with_no_opt_out_activity(self):
        state = c.compute_prospect_state(
            {}, [{"activity_type": "EMAIL_1_SENT", "activity_date": date(2026, 8, 1)}],
            manual_do_not_contact=True, today=date(2026, 8, 20),
        )
        self.assertTrue(state["blocked"])
        self.assertFalse(state["do_not_contact"])
        self.assertEqual(state["stage"], "Contact hold")

    def test_email_2_sent_recommends_email_3_after_seven_business_days(self):
        state = c.compute_prospect_state(
            {}, [{"activity_type": "EMAIL_2_SENT", "activity_date": date(2026, 9, 14)}],
            today=date(2026, 9, 22),
        )
        self.assertEqual(state["next_action"], "Send Email 3")
        self.assertEqual(state["next_action_due_date"], date(2026, 9, 23))

    def test_email_3_completes_cold_sequence(self):
        state = c.compute_prospect_state(
            {}, [{"activity_type": "EMAIL_3_SENT", "activity_date": date(2026, 9, 23)}],
            today=date(2026, 10, 1),
        )
        self.assertEqual(state["stage"], "Cold sequence complete")
        self.assertEqual(state["next_action"], "")
        self.assertTrue(state["sequence_complete"])

    def test_linkedin_view_cannot_overwrite_reply_or_sale_stage(self):
        reply = c.compute_prospect_state({}, [
            {"activity_type": "REPLY_RECEIVED", "activity_date": date(2026, 9, 5)},
            {"activity_type": "LINKEDIN_VIEWED", "activity_date": date(2026, 9, 6)},
        ])
        sold = c.compute_prospect_state({}, [
            {"activity_type": "AUDIT_SOLD", "activity_date": date(2026, 9, 5)},
            {"activity_type": "LINKEDIN_VIEWED", "activity_date": date(2026, 9, 6)},
        ])
        self.assertEqual(reply["stage"], "Replied")
        self.assertEqual(sold["stage"], "Audit")

    def test_audit_sold_is_a_revenue_event_and_recommends_delivery(self):
        state = c.compute_prospect_state(
            {}, [{"activity_type": "AUDIT_SOLD", "activity_date": date(2026, 8, 10)}],
            today=date(2026, 8, 11),
        )
        self.assertEqual(state["stage"], "Audit")
        self.assertEqual(state["next_action"], "Deliver the audit")
        self.assertTrue(c.cadence_by_key()["AUDIT_SOLD"]["is_revenue_event"])


if __name__ == "__main__":
    unittest.main()
