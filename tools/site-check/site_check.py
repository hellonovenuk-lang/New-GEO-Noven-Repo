#!/usr/bin/env python3
"""
Site-check — the technical/crawlability half of the audit
(playbook/audit-site-checklist.md groups 1 and 2), run from nothing but a public
URL.

Written because the only time this checklist has been run — the Noven
self-audit — quietly used access that only exists for our own site: robots.txt
read from the source repo, redirect/header/password checks read from the
Netlify dashboard, JSON-LD "validity" reasoned from knowing the code that
generates it. None of that is available for a client's site. This script does
only what a real crawler could do: fetch the public URL and read what comes
back.

Stdlib only, Python 3.9+. No API keys, no per-query cost, so — unlike
audit_query.py — this is a reusable tool, not a per-audit throwaway. Sits
beside tools/name-check/ as the second tool in that shape.

What it deliberately does NOT do, and why, is in README.md — read that before
treating a clean report as a clean site.

Usage:
  python site_check.py --url https://client-site.example
  python site_check.py --url https://client-site.example --out report.json
"""

import argparse
import json
import re
import socket
import sys
import urllib.error
import urllib.request
import urllib.robotparser
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree

USER_AGENT = "Wardith-Audit/1.0 (+https://wardith.co.uk; technical audit check)"

# The crawler names playbook/audit-site-checklist.md group 1.1 asks about.
# Keep this list in step with that file — it's the source of truth for which
# names matter, this just automates checking them.
CRAWLERS = [
    ("GPTBot", "OpenAI — training and retrieval"),
    ("OAI-SearchBot", "OpenAI — ChatGPT search index"),
    ("ChatGPT-User", "OpenAI — live fetch when a user asks"),
    ("ClaudeBot", "Anthropic"),
    ("Claude-SearchBot", "Anthropic"),
    ("PerplexityBot", "Perplexity"),
    ("Perplexity-User", "Perplexity"),
    ("Google-Extended", "Google — Gemini grounding control"),
    ("Googlebot", "Google — the index everything else leans on"),
    ("Bingbot", "Microsoft — Copilot depends on this"),
    ("Applebot-Extended", "Apple"),
]

# Crude but effective: the strings real interstitial/challenge pages actually
# print. A false negative here just means the fetch results speak for
# themselves; a false positive costs a sentence a human discards in seconds.
CHALLENGE_MARKERS = [
    "checking your browser",
    "just a moment",
    "enable javascript and cookies",
    "verify you are human",
    "cf-chl",
    "attention required",
    "access denied",
    "captcha",
]


class Fetcher:
    """Wraps urllib with a hard cap on requests, a UA, a timeout, and a
    redirect chain logger — so one run can never hammer a client's site by
    accident, and a redirect's actual path is visible rather than silently
    followed."""

    def __init__(self, cap, timeout):
        self.cap = cap
        self.timeout = timeout
        self.count = 0

    def get(self, url, max_redirects=5):
        chain = []
        current = url
        for _ in range(max_redirects + 1):
            self.count += 1
            if self.count > self.cap:
                raise RuntimeError(
                    f"Request cap ({self.cap}) reached — stopping before "
                    f"fetching {current}. Raise --cap if this site genuinely "
                    f"needs more requests."
                )
            req = urllib.request.Request(current, headers={"User-Agent": USER_AGENT})
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    body = resp.read(2_000_000)  # 2MB cap — a homepage is not a video
                    return {
                        "requested_url": url,
                        "final_url": current,
                        "redirect_chain": chain,
                        "status": resp.status,
                        "headers": dict(resp.headers.items()),
                        "body": body.decode(resp.headers.get_content_charset() or "utf-8", errors="replace"),
                        "error": None,
                    }
            except urllib.error.HTTPError as e:
                if e.code in (301, 302, 303, 307, 308) and e.headers.get("Location"):
                    chain.append({"from": current, "status": e.code})
                    current = urljoin(current, e.headers["Location"])
                    continue
                return {
                    "requested_url": url, "final_url": current, "redirect_chain": chain,
                    "status": e.code, "headers": dict(e.headers.items()) if e.headers else {},
                    "body": "", "error": f"HTTP {e.code}",
                }
            except (urllib.error.URLError, socket.timeout, TimeoutError) as e:
                return {
                    "requested_url": url, "final_url": current, "redirect_chain": chain,
                    "status": None, "headers": {}, "body": "", "error": str(e),
                }
        return {
            "requested_url": url, "final_url": current, "redirect_chain": chain,
            "status": None, "headers": {}, "body": "",
            "error": f"More than {max_redirects} redirects — stopped following.",
        }


def check_robots(fetcher, origin):
    robots_url = urljoin(origin, "/robots.txt")
    result = fetcher.get(robots_url)

    if result["error"] and result["status"] != 404:
        return {
            "url": robots_url, "exists": False, "fetch_error": result["error"],
            "note": "Could not fetch robots.txt at all — not the same as a 404. Check by hand.",
        }
    if result["status"] == 404:
        return {
            "url": robots_url, "exists": False, "fetch_error": None,
            "note": "No robots.txt (404). This means allowed by default, not a problem — say so plainly.",
            "crawlers": {name: "allowed (no robots.txt)" for name, _ in CRAWLERS},
            "blanket_disallow": False,
        }

    raw = result["body"]
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(raw.splitlines())

    crawlers = {}
    for name, _who in CRAWLERS:
        allowed = rp.can_fetch(name, "/")
        named = bool(re.search(rf"(?im)^\s*user-agent:\s*{re.escape(name)}\s*$", raw))
        if named:
            crawlers[name] = "allowed (named)" if allowed else "blocked (named)"
        else:
            crawlers[name] = "allowed (not mentioned, falls to catch-all)" if allowed else "blocked (catch-all disallow)"

    blanket_disallow = not rp.can_fetch("*", "/")

    try:
        sitemaps = list(rp.site_maps() or [])
    except AttributeError:
        sitemaps = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", raw)

    return {
        "url": robots_url,
        "exists": True,
        "fetch_error": None,
        "raw_bytes": len(raw.encode("utf-8")),
        "crawlers": crawlers,
        "blanket_disallow": blanket_disallow,
        "sitemaps_declared": sitemaps,
    }


def check_homepage_access(fetcher, url):
    result = fetcher.get(url)
    headers = {k.lower(): v for k, v in result["headers"].items()}
    body_lower = result["body"].lower()

    challenge_hits = [m for m in CHALLENGE_MARKERS if m in body_lower]
    password_wall = result["status"] in (401, 403) or "www-authenticate" in headers

    cdn_signals = []
    if any(k.startswith("cf-") for k in headers) or "cloudflare" in headers.get("server", "").lower():
        cdn_signals.append("cloudflare")
    if "x-served-by" in headers or "fastly" in headers.get("server", "").lower():
        cdn_signals.append("fastly")

    return {
        "requested_url": result["requested_url"],
        "final_url": result["final_url"],
        "status": result["status"],
        "fetch_error": result["error"],
        "redirect_chain": result["redirect_chain"],
        "https": urlparse(result["final_url"]).scheme == "https",
        "apex_vs_www_changed": urlparse(url).netloc != urlparse(result["final_url"]).netloc,
        "likely_password_or_login_wall": password_wall,
        "cdn_signals": cdn_signals,
        "challenge_page_markers_found": challenge_hits,
        "note": (
            "This approximates what the Netlify/hosting dashboard would show "
            "(password walls, redirect rules, CDN) from the outside, since a "
            "client audit has no access to that dashboard. It's what a real "
            "crawler actually meets, which is arguably the more honest test."
        ),
    }


def strip_html(html):
    text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def check_readability(html):
    visible_text = strip_html(html)
    word_count = len(visible_text.split())
    return {
        "word_count_in_raw_source": word_count,
        "likely_js_rendered_shell": word_count < 40,
        "note": (
            "Heuristic, not a verdict: word_count is everything left after "
            "stripping tags/scripts from the raw HTML a non-JS crawler sees. "
            "A very low count on a page that clearly has content on-screen "
            "means it's assembled by JavaScript after load — verify by hand "
            "before writing this up as a finding."
        ),
    }


def check_sitemap(fetcher, origin, declared):
    candidates = list(declared) if declared else []
    for guess in ("/sitemap.xml", "/sitemap_index.xml", "/sitemap-index.xml"):
        guess_url = urljoin(origin, guess)
        if guess_url not in candidates:
            candidates.append(guess_url)

    for sitemap_url in candidates:
        result = fetcher.get(sitemap_url)
        if result["error"] or result["status"] != 200:
            continue
        try:
            root = ElementTree.fromstring(result["body"])
        except ElementTree.ParseError as e:
            return {"url": sitemap_url, "status": result["status"], "valid_xml": False, "parse_error": str(e)}
        tag = root.tag.rsplit("}", 1)[-1]
        ns = {"sm": root.tag.split("}")[0].strip("{")} if "}" in root.tag else {}
        loc_path = "sm:sitemap/sm:loc" if ns else "sitemap/loc"
        if tag == "sitemapindex":
            locs = [el.text for el in root.findall(loc_path, ns)]
            return {"url": sitemap_url, "status": 200, "valid_xml": True, "type": "sitemap_index", "child_sitemaps": locs}
        loc_path = "sm:url/sm:loc" if ns else "url/loc"
        locs = [el.text for el in root.findall(loc_path, ns)]
        return {"url": sitemap_url, "status": 200, "valid_xml": True, "type": "urlset", "url_count": len(locs), "sample_urls": locs[:15]}

    return {"url": None, "status": None, "valid_xml": False, "note": "No sitemap found at the declared location or common paths."}


JSONLD_RE = re.compile(r'(?is)<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>')
COMMON_FIELDS = ["name", "address", "telephone", "areaServed", "openingHours", "email", "priceRange", "offers", "sameAs"]


def check_structured_data(html):
    blocks = JSONLD_RE.findall(html)
    parsed_ok, parse_errors, types_found, fields_present = [], [], set(), set()

    def walk(obj):
        if isinstance(obj, dict):
            t = obj.get("@type")
            if isinstance(t, list):
                types_found.update(str(x) for x in t)
            elif t:
                types_found.add(str(t))
            for k in obj:
                if k in COMMON_FIELDS:
                    fields_present.add(k)
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    for i, raw in enumerate(blocks):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            parse_errors.append({"block": i, "error": str(e)})
            continue
        parsed_ok.append(i)
        graph = data.get("@graph") if isinstance(data, dict) else None
        walk(graph if graph is not None else data)

    return {
        "blocks_found": len(blocks),
        "blocks_parsed_ok": len(parsed_ok),
        "parse_errors": parse_errors,
        "types_found": sorted(types_found),
        "common_fields_present": sorted(fields_present),
        "common_fields_absent": sorted(set(COMMON_FIELDS) - fields_present),
        "note": (
            "Field presence is a structural check only — it says whether a key "
            "like 'address' exists somewhere in the graph, not whether the "
            "value is correct or matches the visible page. Read against the "
            "rendered site by hand, per audit-site-checklist.md group 2."
        ),
    }


# How a platform gives itself away. Each entry: (label, [html markers],
# [header names]). Matching is case-insensitive substring — crude on purpose,
# because these are strings vendors put in their own output and they don't
# need parsing to be recognised.
#
# THESE GO STALE. Vendors rename CDNs and drop generator tags. A miss means
# "unknown", never "bespoke" — the script says so in the output, and
# audit-site-checklist.md's platform table is where the consequences live.
# Do not duplicate that guidance here; one copy, per service-tiers.md section 4.
PLATFORM_SIGNALS = [
    ("WordPress", ["/wp-content/", "/wp-includes/", "wp-json", 'content="wordpress'], ["x-pingback"]),
    ("Wix", ["wixstatic.com", "wix.com website builder", "_wixcssimports"], ["x-wix-request-id", "x-wix-published-version"]),
    ("Squarespace", ["squarespace.com", "squarespace-cdn.com", "static1.squarespace.com"], []),
    ("Shopify", ["cdn.shopify.com", "shopify.theme", "myshopify.com"], ["x-shopid", "x-shopify-stage"]),
    ("GoDaddy Website Builder", ["img1.wsimg.com", "starfield technologies", "wsimg.com"], []),
    ("Webflow", ["assets.website-files.com", "website-files.com", "data-wf-page", 'content="webflow'], []),
    ("Duda", ["irp.cdn-website.com", "static.cdn-website.com", 'content="duda'], []),
    ("Weebly", ["editmysite.com", 'content="weebly'], []),
    ("Drupal", ["/sites/default/files/", 'content="drupal'], ["x-generator"]),
    ("Joomla", ['content="joomla'], []),
]

# Where it's served from. Not the same question as what built it, and useful
# for a different reason: these say a developer was involved, so the access
# conversation is about a deploy path and a repository, not a CMS login.
HOSTING_SIGNALS = [
    ("Netlify", [], ["x-nf-request-id"]),
    ("Vercel", [], ["x-vercel-id", "x-vercel-cache"]),
    ("GitHub Pages", [], ["x-github-request-id"]),
    ("Cloudflare Pages", [], ["cf-ray"]),
]

# Static site generators. Their presence is strong evidence of a bespoke,
# developer-built site — which is an access question about people, not plans.
SSG_MARKERS = ["astro", "hugo", "next.js", "gatsby", "jekyll", "eleventy", "nuxt"]


def check_platform(html, headers):
    haystack = html.lower()
    header_keys = {k.lower(): v for k, v in headers.items()}

    def matches(markers, header_names):
        hits = [m for m in markers if m in haystack]
        hits += [f"header:{h}" for h in header_names if h in header_keys]
        return hits

    platforms = []
    for label, markers, header_names in PLATFORM_SIGNALS:
        hits = matches(markers, header_names)
        if hits:
            platforms.append({"platform": label, "signals": hits})

    hosting = []
    for label, markers, header_names in HOSTING_SIGNALS:
        hits = matches(markers, header_names)
        if hits:
            hosting.append({"host": label, "signals": hits})

    generator = re.search(r'(?is)<meta[^>]+name=["\']generator["\'][^>]+content=["\'](.*?)["\']', html)
    generator_text = generator.group(1).strip() if generator else None

    ssg = []
    if generator_text:
        low = generator_text.lower()
        ssg = [s for s in SSG_MARKERS if s in low]

    return {
        "generator_meta_tag": generator_text,
        "platforms_detected": platforms,
        "hosting_detected": hosting,
        "static_site_generator_signals": ssg,
        "verdict": (
            platforms[0]["platform"] if len(platforms) == 1
            else "multiple signals — read them" if len(platforms) > 1
            else "developer-built (static site generator)" if ssg
            else "unknown"
        ),
        "note": (
            "Signals, not proof, and they go stale — vendors rename CDNs and "
            "drop generator tags. 'unknown' means not detected, NOT 'bespoke': "
            "a hand-built site and an unrecognised builder look identical from "
            "here. Multiple platforms is normal and real (a Shopify store on a "
            "WordPress site, a builder behind a CDN). What each platform means "
            "for the Foundation access ask is in audit-site-checklist.md's "
            "platform table — deliberately not repeated here, so the two can't "
            "drift apart."
        ),
    }


def check_page_meta(html):
    title = re.search(r"(?is)<title[^>]*>(.*?)</title>", html)
    h1s = re.findall(r"(?is)<h1[^>]*>(.*?)</h1>", html)
    desc = re.search(r'(?is)<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', html)
    return {
        "title": strip_html(title.group(1)) if title else None,
        "h1_count": len(h1s),
        "h1_text": [strip_html(h) for h in h1s],
        "meta_description": strip_html(desc.group(1)) if desc else None,
    }


STILL_MANUAL = {
    "site_index_checks": (
        "Bing and Google 'site:domain' searches (checklist group 3.1/3.2) are "
        "public searches, not a webmaster-tools lookup, and this script "
        "deliberately doesn't automate them — scraping search-results pages "
        "is fragile and likely against those providers' terms. Two minutes by "
        "hand in a browser."
    ),
    "google_url_inspection": (
        "The definitive 'can this page be indexed' answer comes from Search "
        "Console's URL Inspection tool, which needs verified ownership of the "
        "client's domain. Not available unless the client grants it — treat "
        "as an optional upgrade, same two-stage access pattern as the "
        "Foundation, not a baseline requirement."
    ),
    "off_site_consistency": (
        "Checklist group 3's off-site half — Google Business Profile, Bing "
        "Places, Companies House, professional registers, directories, "
        "LinkedIn, review counts — is comparative work across sources this "
        "script has no access to. Stays manual."
    ),
    "content_answers_the_question": (
        "Checklist group 4 — does a page genuinely answer each of the "
        "client's ten questions — is a judgement call about the writing, not "
        "a fetchable fact. Stays manual."
    ),
    "visible_price_and_location_claims": (
        "Whether the page states a price or names real towns (not just 'the "
        "North West') needs a person reading the rendered page, not a regex "
        "guessing at currency symbols in the wrong context."
    ),
}


def run(url, cap, timeout):
    parsed = urlparse(url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    fetcher = Fetcher(cap=cap, timeout=timeout)

    report = {
        "audit_tool": "site_check.py",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "url": url,
    }

    report["robots"] = check_robots(fetcher, origin)

    homepage = fetcher.get(url)
    report["homepage_access"] = check_homepage_access(fetcher, url)
    report["readability"] = check_readability(homepage["body"]) if homepage["body"] else {
        "note": "Homepage body unavailable — see homepage_access.fetch_error."
    }
    report["structured_data"] = check_structured_data(homepage["body"]) if homepage["body"] else {
        "note": "Homepage body unavailable — see homepage_access.fetch_error."
    }
    report["page_meta"] = check_page_meta(homepage["body"]) if homepage["body"] else {}
    report["platform"] = check_platform(homepage["body"], homepage["headers"]) if homepage["body"] else {
        "note": "Homepage body unavailable — see homepage_access.fetch_error."
    }

    declared_sitemaps = report["robots"].get("sitemaps_declared", [])
    report["sitemap"] = check_sitemap(fetcher, origin, declared_sitemaps)

    report["requests_made"] = fetcher.count
    report["still_needs_manual_checking"] = STILL_MANUAL
    return report


def summarise(report):
    lines = [f"site-check — {report['url']} — {report['checked_at']}", ""]

    robots = report["robots"]
    if not robots.get("exists"):
        lines.append(f"robots.txt: {robots.get('note', 'not found')}")
    else:
        blocked = [n for n, v in robots["crawlers"].items() if v.startswith("blocked")]
        lines.append(f"robots.txt: {'BLANKET DISALLOW' if robots['blanket_disallow'] else 'no blanket disallow'}"
                      + (f"; blocked by name: {', '.join(blocked)}" if blocked else "; nothing blocked by name"))
        lines.append(f"  sitemap declared: {robots['sitemaps_declared'] or 'none'}")

    ha = report["homepage_access"]
    lines.append(f"homepage: status {ha['status']}, https={ha['https']}"
                 + (f", REDIRECT CHAIN {len(ha['redirect_chain'])} hop(s)" if ha["redirect_chain"] else ""))
    if ha["likely_password_or_login_wall"]:
        lines.append("  WARNING: looks like a password/login wall")
    if ha["challenge_page_markers_found"]:
        lines.append(f"  WARNING: challenge-page markers found: {ha['challenge_page_markers_found']}")

    rd = report["readability"]
    if rd.get("likely_js_rendered_shell"):
        lines.append(f"readability: WARNING — only {rd['word_count_in_raw_source']} words in raw source, possible JS shell")
    elif "word_count_in_raw_source" in rd:
        lines.append(f"readability: {rd['word_count_in_raw_source']} words in raw source, looks fine")

    sd = report["structured_data"]
    if sd.get("blocks_found") is not None:
        lines.append(f"structured data: {sd['blocks_found']} JSON-LD block(s), {sd['blocks_parsed_ok']} parsed OK, types: {sd['types_found'] or 'none'}")
        if sd["common_fields_absent"]:
            lines.append(f"  fields absent from the graph: {sd['common_fields_absent']}")

    pf = report.get("platform", {})
    if pf.get("verdict"):
        lines.append(f"platform: {pf['verdict']}"
                     + (f" (generator tag: {pf['generator_meta_tag']})" if pf.get("generator_meta_tag") else ""))
        if pf.get("hosting_detected"):
            lines.append(f"  hosted on: {', '.join(h['host'] for h in pf['hosting_detected'])}")
        lines.append("  -> access implications: see the platform table in audit-site-checklist.md")

    sm = report["sitemap"]
    if sm.get("valid_xml"):
        lines.append(f"sitemap: valid, {sm.get('url_count', 'index — see child_sitemaps')} at {sm['url']}")
    else:
        lines.append("sitemap: not found or invalid — check by hand")

    lines.append("")
    lines.append(f"{report['requests_made']} request(s) made this run.")
    lines.append("See still_needs_manual_checking in the JSON for what this script doesn't cover.")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", required=True, help="The client's homepage URL, e.g. https://example.co.uk")
    ap.add_argument("--out", default=None, help="Write the full JSON report here. Point this at the client's "
                                                  "own folder outside the repo — never leave client data in git.")
    ap.add_argument("--cap", type=int, default=8, help="Hard cap on HTTP requests this run (default 8)")
    ap.add_argument("--timeout", type=int, default=15, help="Per-request timeout in seconds (default 15)")
    args = ap.parse_args()

    if not args.url.startswith(("http://", "https://")):
        sys.exit("--url must start with http:// or https://")

    try:
        report = run(args.url, cap=args.cap, timeout=args.timeout)
    except RuntimeError as e:
        sys.exit(str(e))

    print(summarise(report))

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\nFull report written to {args.out}")
    else:
        print("\n(No --out given — full JSON not written anywhere. "
              "Pass --out pointed at the client's folder outside the repo to keep it.)")


if __name__ == "__main__":
    main()
