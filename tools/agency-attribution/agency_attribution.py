#!/usr/bin/env python3
"""
Agency attribution — for each business in a completed market census, finds
the web designer or SEO agency credited on its own site, then researches
each agency once for whether it's a plausible white-label buyer.

Why this exists (playbook/agency-product.md, decisions.md 2026-08-19): the
70% of outreach effort aimed at agencies and web designers needs a list of
agencies to approach, built from public evidence rather than a cold guess.
Most footer credits point at web designers, not SEO agencies — workable,
since a web designer can fix everything the Foundation touches (on-site:
schema, crawlability, structure) even though they usually can't touch the
off-site half (directories, Google Business Profile, review platforms).

What this is a re-engagement asset for (2026-08-23 product pivot — see
playbook/agency-product.md): an agency doesn't buy this as delivery
verification, it has no reason to want past work checked. What it actually
has is lumpy project revenue and a dormant client list with no natural
reason to re-contact it. A branded report about a past client is a
re-engagement email the agency can send with a straight face. So the
qualifying fields here are not "did the schema work land" but "does this
agency have the sales motion (a recurring-revenue mindset, a habit of
writing about clients) that makes forwarding a report make sense to them":

  PRIMARY  sells_retainer          — care plan / maintenance / hosting
                                      retainer / any recurring service
  PRIMARY  publishes_client_work   — case studies, portfolio, client news
  SECONDARY mentions_schema_or_aeo — advertises schema/structured-data/
                                      GEO/AEO work (kept, no longer primary)
  DISQUALIFYING sells_ai_visibility — already sells an LLM-visibility/
                                      AI-visibility audit or monitoring
                                      product — this is why the Max Web
                                      approach failed: a sample of their own
                                      client reads as an accusation that
                                      their own monitoring missed something

Everything here is public information and read-only fetching: robots.txt is
checked before every request, requests are rate-limited, and the tool
identifies itself in the User-Agent. Nothing is submitted to any site and no
end client or agency is ever contacted by this script.

Stdlib only, Python 3.9+. Pattern (Fetcher, robots handling, HTML-stripping)
follows tools/site-check/site_check.py — the closest existing analogue.

Output: an agency list written wherever --out points. CLAUDE.md's "no
client or prospect names in this repository" rule is absolute and covers
agency names too (they're personal/business data about real companies found
through real client relationships) — --out must resolve outside this repo,
and the tool refuses to write inside it.

Usage:
  python3 agency_attribution.py \
      --census ~/wardith-runs/<slug>/market-census-<slug>.csv \
      --out ~/wardith-runs/<slug>/agencies.csv
"""
import argparse
import csv
import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.request
import urllib.robotparser
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree

USER_AGENT = (
    "WardithAgencyAttributionBot/1.0 "
    "(+https://wardith.co.uk; research tool building an agency contact "
    "list from public credit links; read-only, no forms submitted; "
    "respects robots.txt)"
)

# ---------------------------------------------------------------------------
# Fetching — robots-aware, rate-limited, capped. Never fetches a URL its own
# robots.txt check disallows for USER_AGENT; every fetch sleeps --delay
# seconds first (except the very first request of the run).
# ---------------------------------------------------------------------------

class RobotsCache:
    """One RobotFileParser per origin, fetched at most once each."""

    def __init__(self, raw_get):
        self._raw_get = raw_get
        self._parsers = {}

    def _parser_for(self, origin):
        if origin not in self._parsers:
            rp = urllib.robotparser.RobotFileParser()
            result = self._raw_get(urljoin(origin, "/robots.txt"))
            if result["status"] == 200 and result["body"]:
                rp.parse(result["body"].splitlines())
            else:
                rp.parse([])  # no robots.txt / fetch failed -> allow by default, matches RFC 9309
            self._parsers[origin] = rp
        return self._parsers[origin]

    def allowed(self, url):
        origin = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        try:
            return self._parser_for(origin).can_fetch(USER_AGENT, url)
        except Exception:  # noqa: BLE001 - a broken robots.txt must never block a whole run
            return True


class Fetcher:
    """Wraps urllib with a hard request cap, a UA, a timeout, rate-limiting
    and robots.txt compliance. One instance per run, shared across every
    business and agency fetched, so the cap is a genuine run-wide ceiling."""

    def __init__(self, cap, timeout, delay):
        self.cap = cap
        self.timeout = timeout
        self.delay = delay
        self.count = 0
        self._first = True
        self.robots = RobotsCache(self._raw_get)

    def _raw_get(self, url):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = resp.read(2_000_000)  # 2MB cap - a homepage/portfolio page, not a video
                return {
                    "url": url, "status": resp.status,
                    "headers": dict(resp.headers.items()),
                    "body": body.decode(resp.headers.get_content_charset() or "utf-8", errors="replace"),
                    "error": None,
                }
        except urllib.error.HTTPError as e:
            return {"url": url, "status": e.code, "headers": {}, "body": "", "error": f"HTTP {e.code}"}
        except (urllib.error.URLError, socket.timeout, TimeoutError) as e:
            return {"url": url, "status": None, "headers": {}, "body": "", "error": str(e)}

    def get(self, url, respect_robots=True):
        if respect_robots and not self.robots.allowed(url):
            return {"url": url, "status": None, "headers": {}, "body": "", "error": "blocked by robots.txt"}
        self.count += 1
        if self.count > self.cap:
            raise RuntimeError(
                f"Request cap ({self.cap}) reached — stopping before fetching {url}. "
                f"Raise --cap if this census genuinely needs more requests."
            )
        if not self._first:
            time.sleep(self.delay)
        self._first = False
        return self._raw_get(url)


# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------

def strip_html(html):
    text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


ANCHOR_RE = re.compile(r'(?is)<a\s[^>]*href=["\']([^"\'#][^"\']*)["\'][^>]*>(.*?)</a>')


def find_anchors(html):
    """Every (href, visible_text) pair in html, visible_text HTML-stripped."""
    return [(href, strip_html(text)) for href, text in ANCHOR_RE.findall(html)]


def extract_footer_region(html):
    """The <footer>...</footer> block if present, else the last third of the
    stripped page (a common, crude-but-reasonable approximation when a site
    has no explicit footer tag — good enough for finding a credit link,
    which is footer-shaped even without the semantic element)."""
    m = re.search(r"(?is)<footer\b.*?</footer>", html)
    if m:
        return m.group(0)
    third = max(len(html) // 3, 1)
    return html[-third:]


# ---------------------------------------------------------------------------
# Domain filtering — links that are never a credited agency, however they're
# worded. Not sector-specific: these are directories/social/utility domains
# that appear in almost every small-business footer regardless of trade.
# ---------------------------------------------------------------------------

EXCLUDE_DOMAIN_SUBSTRINGS = [
    "facebook.com", "instagram.com", "twitter.com", "x.com", "linkedin.com",
    "youtube.com", "youtu.be", "tiktok.com", "pinterest.", "wa.me",
    "whatsapp.com", "google.com", "goo.gl", "maps.app", "g.page",
    "checkatrade.com", "trustpilot.com", "yell.com", "which.co.uk",
    "freeindex.co.uk", "bark.com", "thomsonlocal.com", "gov.uk",
    "companieshouse.gov.uk", "cookielaw.org", "cookiebot.com",
    "gdpr", "wordpress.com", "wix.com", "squarespace.com", "shopify.com",
    "apple.com", "microsoft.com", "godaddy.com",
]


def domain_of(url):
    netloc = urlparse(url).netloc.lower()
    return netloc[4:] if netloc.startswith("www.") else netloc


def is_excluded_domain(domain):
    return any(s in domain for s in EXCLUDE_DOMAIN_SUBSTRINGS)


# ---------------------------------------------------------------------------
# Credit extraction — two tiers. Tier 1 (phrase-anchored) is high confidence:
# a link immediately preceded by a known credit phrase. Tier 2 (keyword
# fallback) only runs when tier 1 found nothing for this business, and only
# looks at footer-region links whose own anchor text reads as an agency.
# ---------------------------------------------------------------------------

CREDIT_PHRASES = [
    "designed by", "design by", "built by", "built with", "developed by",
    "development by", "web design by", "website by", "site by",
    "created by", "crafted by", "made by",
]

AGENCY_ANCHOR_KEYWORDS = [
    "web design", "webdesign", "web development", "digital agency",
    "creative agency", "creative studio", "design studio", "digital studio",
    "marketing agency", "seo agency", "web agency", ".digital", "studio",
]


def find_credit_candidates(html, own_domain):
    """[(domain, url, method, evidence)] - method is 'phrase' or 'keyword'.
    own_domain is excluded so a business linking to its own other pages
    never gets credited as its own agency."""
    footer = extract_footer_region(html)
    anchors = find_anchors(footer)

    phrase_hits = []
    lower_footer = footer.lower()
    for href, text in anchors:
        domain = domain_of(urljoin("https://" + own_domain, href))
        if not domain or domain == own_domain or is_excluded_domain(domain):
            continue
        idx = lower_footer.find(href.lower()) if href.lower() in lower_footer else -1
        # window of raw HTML immediately before this href, to catch
        # "Designed by <a href=...>Agency</a>" phrasing that precedes the link
        window = lower_footer[max(0, idx - 80):idx] if idx >= 0 else ""
        anchor_text_lower = text.lower()
        if any(p in window for p in CREDIT_PHRASES) or any(p in anchor_text_lower for p in CREDIT_PHRASES):
            phrase_hits.append((domain, urljoin("https://" + own_domain, href), "phrase", text or href))

    if phrase_hits:
        return phrase_hits

    keyword_hits = []
    for href, text in anchors:
        domain = domain_of(urljoin("https://" + own_domain, href))
        if not domain or domain == own_domain or is_excluded_domain(domain):
            continue
        haystack = f"{text.lower()} {domain.lower()}"
        if any(k in haystack for k in AGENCY_ANCHOR_KEYWORDS):
            keyword_hits.append((domain, urljoin("https://" + own_domain, href), "keyword", text or href))
    return keyword_hits


# ---------------------------------------------------------------------------
# Agency-page classification — all keyword-heuristic, all labelled as such
# in the output notes. Never presented as a confirmed fact.
# ---------------------------------------------------------------------------

WEB_DESIGN_KEYWORDS = [
    "web design", "website design", "web development", "website development",
    "ecommerce development", "wordpress development", "shopify development",
    "web developer", "ux design", "ui design", "responsive design",
]
SEO_KEYWORDS = [
    "search engine optimisation", "search engine optimization", " seo ",
    "seo services", "digital marketing agency", "ppc", "pay-per-click",
    "paid search", "content marketing", "link building", "google ads",
]

RETAINER_KEYWORDS = [
    "retainer", "care plan", "website care", "maintenance package",
    "maintenance plan", "support plan", "hosting plan", "monthly plan",
    "monthly retainer", "ongoing support", "website management plan",
    "managed hosting", "website support package",
]

SCHEMA_AEO_KEYWORDS = [
    "schema markup", "structured data", "generative engine optimi",
    "answer engine optimi", " geo ", " aeo ", "llm seo", "ai search optimi",
]

AI_VISIBILITY_SERVICE_KEYWORDS = [
    "ai visibility audit", "ai-visibility audit", "llm visibility audit",
    "llm visibility monitoring", "chatgpt seo audit", "ai search visibility service",
    "generative engine optimization service", "generative engine optimisation service",
    "ai visibility monitoring", "monitor your ai visibility", "track your ai visibility",
    "ai visibility report",
]


def _hit_count(text_lower, keywords):
    return sum(1 for k in keywords if k in text_lower)


def classify_agency_type(text_lower):
    web = _hit_count(text_lower, WEB_DESIGN_KEYWORDS)
    seo = _hit_count(text_lower, SEO_KEYWORDS)
    if web == 0 and seo == 0:
        return "UNKNOWN"
    if web >= seo * 2 and web > 0:
        return "WEB_DESIGN"
    if seo >= web * 2 and seo > 0:
        return "SEO"
    if web > 0 and seo > 0:
        return "UNKNOWN"  # genuinely mixed signal, not a guess either way
    return "WEB_DESIGN" if web else "SEO"


def detect_any(text_lower, keywords):
    return any(k in text_lower for k in keywords)


# ---------------------------------------------------------------------------
# Portfolio / case-study discovery
# ---------------------------------------------------------------------------

PORTFOLIO_PATH_GUESSES = ["/portfolio", "/work", "/our-work", "/case-studies",
                           "/case-study", "/clients", "/projects"]
PORTFOLIO_LINK_KEYWORDS = ["portfolio", "our work", "case stud", "clients", "projects", "our clients"]


def find_portfolio_page(fetcher, agency_origin, homepage_html):
    """Returns (url, html) for the first working, non-trivial portfolio-ish
    page found, or (None, "") if none. Tries the homepage's own nav/footer
    links first (more reliable than guessing), falling back to common path
    guesses only if nothing on the page itself looks like a portfolio link."""
    candidates = []
    for href, text in find_anchors(homepage_html):
        text_low = text.lower()
        if any(k in text_low for k in PORTFOLIO_LINK_KEYWORDS):
            url = urljoin(agency_origin, href)
            if urlparse(url).netloc == urlparse(agency_origin).netloc:
                candidates.append(url)
    for path in PORTFOLIO_PATH_GUESSES:
        candidates.append(urljoin(agency_origin, path))

    seen = set()
    for url in candidates:
        if url in seen:
            continue
        seen.add(url)
        result = fetcher.get(url)
        if result["status"] == 200 and result["body"]:
            word_count = len(strip_html(result["body"]).split())
            if word_count >= 60:  # a real page, not an empty stub
                return url, result["body"]
    return None, ""


# ---------------------------------------------------------------------------
# Business-name matching (lightweight, self-contained — not
# tools/mention-count's alias machinery, which is tuned for AI answer text,
# not agency portfolio prose). Good enough to confirm "this business's name
# appears somewhere on this page", not a mention-counting tool.
# ---------------------------------------------------------------------------

_LEGAL_SUFFIX_RE = re.compile(r"\s+(ltd\.?|limited|llp)$", re.I)


def _simplify_name(name):
    base = _LEGAL_SUFFIX_RE.sub("", name.strip())
    return re.sub(r"\s+", " ", base).strip().lower()


def page_mentions_business(text_lower, business_name):
    simplified = _simplify_name(business_name)
    return bool(simplified) and simplified in text_lower


# ---------------------------------------------------------------------------
# Recent-maintenance signal, on the CLIENT's own site — distinguishes a
# current relationship from an old build credit, per the brief.
# ---------------------------------------------------------------------------

COPYRIGHT_RE = re.compile(r"(?:©|&copy;|\(c\)|copyright)\s*(?:\d{4}\s*[-–]\s*)?(\d{4})", re.I)


def check_recent_maintenance(fetcher, origin, homepage_html, current_year):
    signals = []
    years_found = [int(y) for y in COPYRIGHT_RE.findall(homepage_html)]
    if years_found:
        latest = max(years_found)
        if latest >= current_year - 1:
            signals.append(f"copyright year {latest}")

    sitemap = fetcher.get(urljoin(origin, "/sitemap.xml"))
    if sitemap["status"] == 200 and sitemap["body"]:
        try:
            root = ElementTree.fromstring(sitemap["body"])
            lastmods = [el.text for el in root.iter() if el.tag.rsplit("}", 1)[-1] == "lastmod" and el.text]
            recent = [d for d in lastmods if d[:4].isdigit() and int(d[:4]) >= current_year - 1]
            if recent:
                signals.append(f"sitemap lastmod within the last year ({len(recent)} url(s))")
        except ElementTree.ParseError:
            pass

    return signals


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def load_census(path, business_col, website_col):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if rows and business_col not in rows[0]:
        sys.exit(f"--business-column '{business_col}' not found. Columns present: {', '.join(rows[0].keys())}")
    if rows and website_col not in rows[0]:
        sys.exit(f"--website-column '{website_col}' not found. Columns present: {', '.join(rows[0].keys())}")
    return rows


def run(census_path, business_col, website_col, cap, timeout, delay, current_year=None):
    census = load_census(census_path, business_col, website_col)
    current_year = current_year or datetime.now(timezone.utc).year
    fetcher = Fetcher(cap=cap, timeout=timeout, delay=delay)

    skipped_no_website = []
    business_fetch_errors = []
    credits = []  # list of dicts: business, agency_domain, agency_url, method, evidence
    maintenance_by_business = {}

    for row in census:
        business = row[business_col].strip()
        website = (row.get(website_col) or "").strip()
        if not website:
            skipped_no_website.append(business)
            continue
        if not website.startswith(("http://", "https://")):
            website = "https://" + website
        origin = f"{urlparse(website).scheme}://{urlparse(website).netloc}"
        own_domain = domain_of(website)

        result = fetcher.get(website)
        if result["status"] != 200 or not result["body"]:
            business_fetch_errors.append({"business": business, "url": website,
                                           "error": result["error"] or f"HTTP {result['status']}"})
            continue

        maintenance_by_business[business] = check_recent_maintenance(
            fetcher, origin, result["body"], current_year
        )

        for domain, url, method, evidence in find_credit_candidates(result["body"], own_domain):
            credits.append({"business": business, "agency_domain": domain, "agency_url": url,
                             "method": method, "evidence": evidence})

    # Group by agency domain
    by_domain = {}
    for c in credits:
        by_domain.setdefault(c["agency_domain"], []).append(c)

    agencies = []
    for domain, entries in sorted(by_domain.items()):
        agency_url = f"https://{domain}/"
        result = fetcher.get(agency_url)
        fetch_status = "ok"
        homepage_html = ""
        if result["status"] != 200 or not result["body"]:
            # retry once over plain http, some smaller agency sites don't do https cleanly
            alt = fetcher.get(f"http://{domain}/")
            if alt["status"] == 200 and alt["body"]:
                result = alt
                agency_url = f"http://{domain}/"
            else:
                fetch_status = result["error"] or f"HTTP {result['status']}"

        if result["status"] == 200 and result["body"]:
            homepage_html = result["body"]
            text_lower = strip_html(homepage_html).lower()
        else:
            text_lower = ""

        portfolio_url, portfolio_html = ("", "")
        if homepage_html:
            portfolio_url, portfolio_html = find_portfolio_page(fetcher, agency_url, homepage_html)
        combined_text_lower = f"{text_lower} {strip_html(portfolio_html).lower()}"

        client_list = sorted({e["business"] for e in entries})
        confirmed = []
        for business in client_list:
            if page_mentions_business(combined_text_lower, business):
                confirmed.append(business)

        maintenance_hits = sum(1 for b in client_list if maintenance_by_business.get(b))

        agencies.append({
            "agency_domain": domain,
            "agency_url": agency_url,
            "fetch_status": fetch_status,
            "agency_type": classify_agency_type(combined_text_lower) if combined_text_lower else "UNKNOWN",
            "sells_retainer": detect_any(combined_text_lower, RETAINER_KEYWORDS),
            "publishes_client_work": bool(portfolio_url),
            "mentions_schema_or_aeo": detect_any(combined_text_lower, SCHEMA_AEO_KEYWORDS),
            "sells_ai_visibility": detect_any(combined_text_lower, AI_VISIBILITY_SERVICE_KEYWORDS),
            "census_clients": len(client_list),
            "census_clients_confirmed": len(confirmed),
            "census_clients_list": ";".join(client_list),
            "census_clients_confirmed_list": ";".join(confirmed),
            "recent_maintenance_signal_count": maintenance_hits,
            "portfolio_url": portfolio_url or "",
            "credit_method": ";".join(sorted({e["method"] for e in entries})),
            "evidence_notes": "; ".join(sorted({e["evidence"] for e in entries}))[:300],
        })

    rank_agencies(agencies)

    return {
        "census_path": census_path,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_census_businesses": len(census),
        "skipped_no_website": skipped_no_website,
        "business_fetch_errors": business_fetch_errors,
        "agencies": agencies,
        "requests_made": fetcher.count,
    }


def rank_agencies(agencies):
    """Sorts in place and assigns 'rank'. Disqualified agencies
    (sells_ai_visibility) always sort last, regardless of every other
    field - the ranking exists to surface who to approach, and a
    disqualified agency is never a candidate to approach with this pitch.
    Among the rest: sells_retainer AND publishes_client_work first (the
    agencies most likely to actually forward something), then
    census_clients descending, tied by agency_domain for determinism."""
    def key(a):
        return (
            a["sells_ai_visibility"],  # False (0) sorts before True (1)
            not (a["sells_retainer"] and a["publishes_client_work"]),
            -a["census_clients"],
            a["agency_domain"],
        )
    agencies.sort(key=key)
    for i, a in enumerate(agencies, 1):
        a["rank"] = i


CSV_FIELDS = [
    "rank", "agency_domain", "agency_url", "agency_type",
    "sells_retainer", "publishes_client_work", "mentions_schema_or_aeo",
    "sells_ai_visibility", "census_clients", "census_clients_confirmed",
    "census_clients_list", "census_clients_confirmed_list",
    "recent_maintenance_signal_count", "portfolio_url", "credit_method",
    "evidence_notes", "fetch_status",
]


def write_csv(agencies, out_path):
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for a in agencies:
            w.writerow({k: a.get(k, "") for k in CSV_FIELDS})


def summarise(report):
    agencies = report["agencies"]
    web = sum(1 for a in agencies if a["agency_type"] == "WEB_DESIGN")
    seo = sum(1 for a in agencies if a["agency_type"] == "SEO")
    unknown = sum(1 for a in agencies if a["agency_type"] == "UNKNOWN")
    retainer = sum(1 for a in agencies if a["sells_retainer"])
    publishes = sum(1 for a in agencies if a["publishes_client_work"])
    multi = sum(1 for a in agencies if a["census_clients"] > 1)
    disqualified = sum(1 for a in agencies if a["sells_ai_visibility"])

    lines = [
        f"agency-attribution — {report['census_path']}",
        f"{report['total_census_businesses']} census businesses; "
        f"{len(report['skipped_no_website'])} had no recorded website; "
        f"{len(report['business_fetch_errors'])} failed to fetch",
        f"{len(agencies)} distinct agency domain(s) credited",
        f"  WEB_DESIGN: {web}   SEO: {seo}   UNKNOWN: {unknown}",
        f"  sells_retainer: {retainer}   publishes_client_work: {publishes}",
        f"  serves >1 census business: {multi}",
        f"  DISQUALIFIED (sells_ai_visibility): {disqualified}",
        f"{report['requests_made']} request(s) made this run.",
    ]
    return "\n".join(lines)


def check_out_path_outside_repo(out_path, repo_root):
    """Raises SystemExit if out_path resolves inside repo_root. Split out
    from main() so it's directly testable without argparse/network."""
    out_abs = os.path.abspath(out_path)
    repo_abs = os.path.abspath(repo_root)
    if out_abs == repo_abs or out_abs.startswith(repo_abs + os.sep):
        raise SystemExit(
            f"--out resolves inside this repository ({out_abs}). CLAUDE.md: no client or prospect "
            f"names in this repository — agency relationships found through real clients are exactly "
            f"that. Point --out somewhere outside the repo, e.g. ~/wardith-runs/<slug>/agencies.csv."
        )


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--census", required=True, help="Market census CSV (business,website,... — tools/qualify's market-census-*.csv shape)")
    ap.add_argument("--out", required=True, help="Where to write agencies.csv — must resolve outside this repository")
    ap.add_argument("--business-column", default="business")
    ap.add_argument("--website-column", default="website")
    ap.add_argument("--cap", type=int, default=250, help="Hard cap on HTTP requests this run (default 250)")
    ap.add_argument("--timeout", type=int, default=15, help="Per-request timeout in seconds")
    ap.add_argument("--delay", type=float, default=1.5, help="Seconds to sleep between requests (default 1.5)")
    ap.add_argument("--report-json", default=None, help="Optional: also write the full structured report here")
    args = ap.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    check_out_path_outside_repo(args.out, repo_root)

    try:
        report = run(args.census, args.business_column, args.website_column,
                     cap=args.cap, timeout=args.timeout, delay=args.delay)
    except RuntimeError as e:
        sys.exit(str(e))

    print(summarise(report))

    write_csv(report["agencies"], args.out)
    print(f"\nWrote {len(report['agencies'])} agency row(s) to {args.out}")

    if args.report_json:
        with open(args.report_json, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"Full report written to {args.report_json}")


if __name__ == "__main__":
    main()
