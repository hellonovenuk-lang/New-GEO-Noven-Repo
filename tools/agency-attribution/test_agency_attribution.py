#!/usr/bin/env python3
"""
Regression tests for agency_attribution.py. All HTML fixtures inline and
fictitious — no real business or agency name, per CLAUDE.md.

Run: python3 test_agency_attribution.py -v
"""
import os
import tempfile
import unittest

import agency_attribution as aa


class FakeFetcher:
    """A minimal stand-in for Fetcher.get() - no network, no robots, no
    rate limiting. Responses keyed by exact URL; anything else 404s."""

    def __init__(self, responses):
        self.responses = responses
        self.count = 0

    def get(self, url, respect_robots=True):
        self.count += 1
        if url in self.responses:
            body = self.responses[url]
            return {"url": url, "status": 200, "headers": {}, "body": body, "error": None}
        return {"url": url, "status": 404, "headers": {}, "body": "", "error": "HTTP 404"}


class CreditPhraseExtractionTests(unittest.TestCase):
    def test_designed_by_phrase_credits_the_linked_domain(self):
        html = """
        <html><body><p>Welcome</p></body>
        <footer>© 2026 Fictitious Kitchens. Designed by
        <a href="https://brightfern.example/">Brightfern Studio</a></footer>
        </html>
        """
        hits = aa.find_credit_candidates(html, "fictitiouskitchens.example")
        self.assertEqual(len(hits), 1)
        domain, url, method, evidence = hits[0]
        self.assertEqual(domain, "brightfern.example")
        self.assertEqual(method, "phrase")

    def test_anchor_text_itself_carrying_the_phrase_is_credited(self):
        html = """
        <footer><a href="https://oakvine.example/">Site built by Oakvine</a></footer>
        """
        hits = aa.find_credit_candidates(html, "someclient.example")
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0][0], "oakvine.example")

    def test_own_domain_link_is_never_self_credited(self):
        html = """
        <footer>Designed by <a href="https://someclient.example/about">us</a></footer>
        """
        hits = aa.find_credit_candidates(html, "someclient.example")
        self.assertEqual(hits, [])

    def test_social_and_directory_links_excluded_even_with_credit_phrase(self):
        # Deliberately implausible phrasing, but proves the exclude list
        # wins even when a phrase happens to sit near a social link.
        html = """
        <footer>Built by nobody. Find us: <a href="https://facebook.com/someclient">Facebook</a></footer>
        """
        hits = aa.find_credit_candidates(html, "someclient.example")
        self.assertEqual(hits, [])

    def test_no_footer_tag_falls_back_to_last_third_of_page(self):
        filler = "<p>content</p>" * 200
        html = f"<html><body>{filler}<div>Website by <a href=\"https://lastthird.example/\">Lastthird</a></div></body></html>"
        hits = aa.find_credit_candidates(html, "client.example")
        self.assertTrue(any(h[0] == "lastthird.example" for h in hits))

    def test_keyword_fallback_only_fires_when_no_phrase_hit_exists(self):
        html = """
        <footer><a href="https://randomlink.example/">Random Link</a>
        <a href="https://somewebdesignstudio.example/">Some Web Design Studio</a></footer>
        """
        hits = aa.find_credit_candidates(html, "client.example")
        domains = {h[0] for h in hits}
        self.assertIn("somewebdesignstudio.example", domains)
        self.assertNotIn("randomlink.example", domains)
        self.assertTrue(all(h[2] == "keyword" for h in hits))

    def test_phrase_hit_present_suppresses_keyword_fallback_entirely(self):
        html = """
        <footer>Designed by <a href="https://realcredit.example/">Realcredit</a>
        <a href="https://somestudio.example/">Some Studio</a></footer>
        """
        hits = aa.find_credit_candidates(html, "client.example")
        domains = {h[0] for h in hits}
        self.assertEqual(domains, {"realcredit.example"})  # keyword-only link excluded once phrase tier wins


class AgencyTypeClassificationTests(unittest.TestCase):
    def test_pure_web_design_signal(self):
        text = "we offer web design and website development for small businesses, plus wordpress development"
        self.assertEqual(aa.classify_agency_type(text), "WEB_DESIGN")

    def test_pure_seo_signal(self):
        text = "search engine optimisation and ppc management, google ads and paid search specialists"
        self.assertEqual(aa.classify_agency_type(text), "SEO")

    def test_no_signal_is_unknown(self):
        self.assertEqual(aa.classify_agency_type("we make things happen for your business"), "UNKNOWN")

    def test_genuinely_mixed_signal_is_unknown_not_guessed(self):
        text = "web design, website development and search engine optimisation, ppc and paid search"
        self.assertEqual(aa.classify_agency_type(text), "UNKNOWN")

    def test_dominant_signal_wins_over_a_single_incidental_mention(self):
        text = ("web design web design web design website development web developer "
                "ux design ui design responsive design and we also do a bit of seo")
        self.assertEqual(aa.classify_agency_type(text), "WEB_DESIGN")


class KeywordDetectionTests(unittest.TestCase):
    def test_retainer_detected(self):
        self.assertTrue(aa.detect_any("ask about our monthly retainer packages", aa.RETAINER_KEYWORDS))

    def test_retainer_not_detected_on_unrelated_text(self):
        self.assertFalse(aa.detect_any("we build beautiful websites", aa.RETAINER_KEYWORDS))

    def test_schema_aeo_mention_detected(self):
        self.assertTrue(aa.detect_any("we implement structured data and schema markup", aa.SCHEMA_AEO_KEYWORDS))

    def test_sells_ai_visibility_requires_a_service_phrase_not_a_bare_mention(self):
        # A bare mention of "schema" must not trip the DISQUALIFYING field -
        # that's mentions_schema_or_aeo's job, a different, weaker signal.
        self.assertFalse(aa.detect_any("we implement structured data and schema markup", aa.AI_VISIBILITY_SERVICE_KEYWORDS))
        self.assertTrue(aa.detect_any("book your ai visibility audit today", aa.AI_VISIBILITY_SERVICE_KEYWORDS))


class BusinessNameMatchingTests(unittest.TestCase):
    def test_legal_suffix_stripped_before_matching(self):
        self.assertTrue(aa.page_mentions_business(
            "we recently completed a project for fictitious kitchens", "Fictitious Kitchens Ltd"))

    def test_no_match_is_false(self):
        self.assertFalse(aa.page_mentions_business("a page about something else entirely", "Fictitious Kitchens Ltd"))


class PortfolioDiscoveryTests(unittest.TestCase):
    def test_nav_link_discovered_and_confirmed_non_trivial(self):
        homepage = '<nav><a href="/our-work">Our Work</a></nav>'
        portfolio_body = "<p>" + ("A real case study about a real client project. " * 10) + "</p>"
        fetcher = FakeFetcher({"https://agency.example/our-work": portfolio_body})
        url, html = aa.find_portfolio_page(fetcher, "https://agency.example/", homepage)
        self.assertEqual(url, "https://agency.example/our-work")
        self.assertIn("case study", html)

    def test_trivial_stub_page_is_rejected(self):
        homepage = '<nav><a href="/portfolio">Portfolio</a></nav>'
        fetcher = FakeFetcher({"https://agency.example/portfolio": "<p>Coming soon</p>"})
        url, html = aa.find_portfolio_page(fetcher, "https://agency.example/", homepage)
        self.assertIsNone(url)

    def test_falls_back_to_path_guesses_when_no_nav_link_found(self):
        homepage = "<p>no nav links here</p>"
        portfolio_body = "<p>" + ("Client work displayed here in detail. " * 10) + "</p>"
        fetcher = FakeFetcher({"https://agency.example/case-studies": portfolio_body})
        url, html = aa.find_portfolio_page(fetcher, "https://agency.example/", homepage)
        self.assertEqual(url, "https://agency.example/case-studies")

    def test_no_portfolio_found_returns_none(self):
        fetcher = FakeFetcher({})
        url, html = aa.find_portfolio_page(fetcher, "https://agency.example/", "<p>nothing</p>")
        self.assertIsNone(url)
        self.assertEqual(html, "")


class RecentMaintenanceTests(unittest.TestCase):
    def test_recent_copyright_year_detected(self):
        html = "<footer>&copy; 2026 Fictitious Kitchens</footer>"
        fetcher = FakeFetcher({})
        signals = aa.check_recent_maintenance(fetcher, "https://client.example/", html, current_year=2026)
        self.assertTrue(any("copyright" in s for s in signals))

    def test_stale_copyright_year_not_flagged(self):
        html = "<footer>&copy; 2019 Fictitious Kitchens</footer>"
        fetcher = FakeFetcher({})
        signals = aa.check_recent_maintenance(fetcher, "https://client.example/", html, current_year=2026)
        self.assertFalse(any("copyright" in s for s in signals))

    def test_sitemap_lastmod_within_a_year_detected(self):
        sitemap = (
            '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            '<url><loc>https://client.example/</loc><lastmod>2026-06-01</lastmod></url></urlset>'
        )
        fetcher = FakeFetcher({"https://client.example/sitemap.xml": sitemap})
        signals = aa.check_recent_maintenance(fetcher, "https://client.example/", "<html></html>", current_year=2026)
        self.assertTrue(any("sitemap" in s for s in signals))

    def test_no_signals_at_all_returns_empty(self):
        fetcher = FakeFetcher({})
        signals = aa.check_recent_maintenance(fetcher, "https://client.example/", "<html>plain</html>", current_year=2026)
        self.assertEqual(signals, [])


class RankingTests(unittest.TestCase):
    def _agency(self, domain, retainer, publishes, clients, disqualified=False):
        return {
            "agency_domain": domain, "sells_retainer": retainer,
            "publishes_client_work": publishes, "census_clients": clients,
            "sells_ai_visibility": disqualified,
        }

    def test_disqualified_agency_always_ranks_last(self):
        agencies = [
            self._agency("bigagency.example", True, True, 10, disqualified=True),
            self._agency("smallagency.example", False, False, 1),
        ]
        aa.rank_agencies(agencies)
        self.assertEqual(agencies[-1]["agency_domain"], "bigagency.example")

    def test_retainer_and_publishes_both_true_ranks_first(self):
        agencies = [
            self._agency("high-clients-no-retainer.example", False, False, 20),
            self._agency("qualifying-agency.example", True, True, 1),
        ]
        aa.rank_agencies(agencies)
        self.assertEqual(agencies[0]["agency_domain"], "qualifying-agency.example")

    def test_within_qualifying_group_census_clients_breaks_ties(self):
        agencies = [
            self._agency("fewer-clients.example", True, True, 2),
            self._agency("more-clients.example", True, True, 5),
        ]
        aa.rank_agencies(agencies)
        self.assertEqual(agencies[0]["agency_domain"], "more-clients.example")

    def test_rank_field_is_assigned_consecutive_from_one(self):
        agencies = [self._agency(f"a{i}.example", False, False, 1) for i in range(3)]
        aa.rank_agencies(agencies)
        self.assertEqual([a["rank"] for a in agencies], [1, 2, 3])


class OutPathGuardTests(unittest.TestCase):
    def test_out_path_inside_repo_is_rejected(self):
        with tempfile.TemporaryDirectory() as repo:
            inside = os.path.join(repo, "agencies.csv")
            with self.assertRaises(SystemExit):
                aa.check_out_path_outside_repo(inside, repo)

    def test_out_path_outside_repo_is_accepted(self):
        with tempfile.TemporaryDirectory() as repo, tempfile.TemporaryDirectory() as outside:
            out = os.path.join(outside, "agencies.csv")
            aa.check_out_path_outside_repo(out, repo)  # must not raise


if __name__ == "__main__":
    unittest.main()
