import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import db as db_mod
import models


def _seed_prospect(conn, prospect_id, campaign_id, business_key, business,
                    company_number=None, last_imported_at="2026-08-01T00:00:00Z"):
    conn.execute(
        """INSERT OR IGNORE INTO campaigns (campaign_id, sector, geography, run_date)
           VALUES (?, ?, ?, ?)""",
        (campaign_id, "estate agents", "Chester", "2026-08-01"),
    )
    conn.execute(
        """INSERT INTO prospects
           (prospect_id, campaign_id, business_key, business, company_number,
            contact_person, first_imported_at, last_imported_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (prospect_id, campaign_id, business_key, business, company_number,
         "Jane Smith", last_imported_at, last_imported_at),
    )
    conn.commit()


class FindProspectTests(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.db_path = Path(self._tmpdir.name) / "wardith.db"
        self.conn = db_mod.connect(self.db_path)
        db_mod.init_db(self.conn)
        self.addCleanup(self._tmpdir.cleanup)
        self.addCleanup(self.conn.close)

    def test_no_match_returns_none(self):
        self.assertIsNone(models.find_prospect(self.conn, business="Nobody Ltd"))

    def test_matches_by_company_number_over_name(self):
        _seed_prospect(self.conn, "campaign-a::cn-01234567", "campaign-a",
                        "cn-01234567", "Acme Plumbing Ltd", company_number="01234567")
        found = models.find_prospect(self.conn, business="A Completely Different Name",
                                      company_number="01234567")
        self.assertIsNotNone(found)
        self.assertEqual(found["business"], "Acme Plumbing Ltd")
        self.assertEqual(found["contact_person"], "Jane Smith")

    def test_falls_back_to_slugified_name_with_no_company_number(self):
        _seed_prospect(self.conn, "campaign-a::acme-plumbing-ltd", "campaign-a",
                        "acme-plumbing-ltd", "Acme Plumbing Ltd")
        found = models.find_prospect(self.conn, business="Acme Plumbing Ltd")
        self.assertIsNotNone(found)
        self.assertEqual(found["business"], "Acme Plumbing Ltd")

    def test_placeholder_company_number_is_ignored(self):
        _seed_prospect(self.conn, "campaign-a::acme-plumbing-ltd", "campaign-a",
                        "acme-plumbing-ltd", "Acme Plumbing Ltd")
        found = models.find_prospect(self.conn, business="Acme Plumbing Ltd",
                                      company_number="[PLACEHOLDER]")
        self.assertIsNotNone(found)

    def test_matches_across_a_different_campaign(self):
        _seed_prospect(self.conn, "campaign-a::acme-plumbing-ltd", "campaign-a",
                        "acme-plumbing-ltd", "Acme Plumbing Ltd")
        found = models.find_prospect(self.conn, business="Acme Plumbing Ltd")
        self.assertEqual(found["campaign_id"], "campaign-a")

    def test_returns_most_recently_imported_match(self):
        _seed_prospect(self.conn, "campaign-a::acme-plumbing-ltd", "campaign-a",
                        "acme-plumbing-ltd", "Acme Plumbing Ltd",
                        last_imported_at="2026-06-01T00:00:00Z")
        _seed_prospect(self.conn, "campaign-b::acme-plumbing-ltd", "campaign-b",
                        "acme-plumbing-ltd", "Acme Plumbing Ltd",
                        last_imported_at="2026-08-20T00:00:00Z")
        found = models.find_prospect(self.conn, business="Acme Plumbing Ltd")
        self.assertEqual(found["campaign_id"], "campaign-b")

    def test_no_business_or_company_number_returns_none(self):
        self.assertIsNone(models.find_prospect(self.conn))
        self.assertIsNone(models.find_prospect(self.conn, business=""))


if __name__ == "__main__":
    unittest.main()
