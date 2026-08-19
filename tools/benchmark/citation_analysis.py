#!/usr/bin/env python3
"""
Citation analysis — what the assistants built their answers out of.

Every Wardith run since the first has recorded `sources_cited` and nothing
has ever read it. This does. Given a completed `tools/trade-run/` CSV it
aggregates the cited URLs by domain, splits them by assistant and question,
and — where a `mention-counts.json` is supplied — answers the question an
SEO team can actually act on:

  **which domains are cited in answers that name a competitor, and are
  cited in no answer that names the client?**

That is a list of specific pages to go and get on, not a general
recommendation. It is the reason this file exists.

Stdlib only, Python 3.9+. Deterministic: same inputs, same output, no
network, no API key, no judgement. Reading what the domains *mean* is the
analyst's job and happens in the report, not here.

  python3 citation_analysis.py --run ~/wardith-runs/<slug>.csv \
      --mention-counts ~/wardith-runs/<slug>/mention-counts.json \
      --client "Example Ltd" --client-domain example.co.uk \
      --out ~/wardith-runs/<slug>/citation-analysis.json

`--mention-counts` and `--client` are optional together: without them you
get the domain census and the per-assistant split, but not the
client-versus-competitor comparison, which is the useful half.

**Domain normalisation is deliberately shallow** — lowercase the host and
drop a leading `www.`, nothing more. There is no Public Suffix List in the
standard library, so `example.co.uk` and `blog.example.co.uk` stay separate
entries rather than being wrongly merged (or wrongly split) by a hand-rolled
suffix guess. A human reading the output can see they are related; a script
guessing at it silently cannot be checked.
"""

import argparse
import csv
import json
import sys
from collections import defaultdict
from urllib.parse import urlsplit

# A run row's identity, and the same three fields mention_count.py records in
# its own `matched_rows` — this is the join key between "who was named in this
# answer" and "what that answer cited".
IDENTITY_FIELDS = ("assistant", "question_id", "run_no")


def normalise_domain(url):
    """Host, lowercased, `www.` dropped. Returns None for anything that
    doesn't parse as a URL with a host — a provider occasionally returns a
    bare title or an empty string in its citation list, and counting that as
    a domain would put junk at the top of the table."""
    url = (url or "").strip()
    if not url:
        return None
    if "://" not in url:
        # Perplexity has returned bare `example.com/page` forms. urlsplit
        # puts those entirely in `path` unless a scheme is present.
        url = "https://" + url
    host = urlsplit(url).netloc.lower()
    if "@" in host:                      # strip any userinfo
        host = host.rsplit("@", 1)[1]
    if ":" in host:                      # strip any port
        host = host.rsplit(":", 1)[0]
    if host.startswith("www."):
        host = host[4:]
    return host or None


def row_identity(row):
    return tuple(str(row.get(f, "")).strip() for f in IDENTITY_FIELDS)


def load_run(path):
    """Successful rows only. A row that errored has no answer and no
    citations, and including it would deflate every per-answer share below."""
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    kept, errored, smoke = [], 0, 0
    for row in rows:
        if "smoke" in (row.get("notes") or "").lower():
            smoke += 1
            continue
        if (row.get("errors") or "").strip():
            errored += 1
            continue
        kept.append(row)
    return kept, errored, smoke


def load_mention_counts(path):
    """business -> set of run identities that named it. `_overlap_log` is
    mention_count.py's own audit trail, not a business."""
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    named = {}
    for business, entry in data.items():
        if business.startswith("_"):
            continue
        named[business] = {
            (str(m.get("assistant", "")), str(m.get("question_id", "")), str(m.get("run_no", "")))
            for m in entry.get("matched_rows", [])
        }
    return named


def analyse(rows, named_by_business=None, client=None, client_domain=None):
    named_by_business = named_by_business or {}
    if client is not None and client not in named_by_business:
        # Being named in zero answers is a real and common finding; having no
        # entry at all means the census the counts were built from never
        # included the client, which is a setup mistake worth stopping on.
        raise SystemExit(
            f"--client {client!r} has no entry in the mention counts. The peer "
            f"census must include the client itself, or nothing below can "
            f"compare it against anyone. Businesses present: "
            f"{sorted(named_by_business)}"
        )

    client_answers = named_by_business.get(client, set()) if client else set()
    competitor_answers = set()
    for business, identities in named_by_business.items():
        if business != client:
            competitor_answers |= identities

    domains = defaultdict(lambda: {
        "citations": 0,
        "answers": set(),
        "by_provider": defaultdict(int),
        "by_question": defaultdict(int),
        "in_client_answers": 0,
        "in_competitor_answers": 0,
    })

    answers_total = 0
    answers_with_citations = 0
    for row in rows:
        answers_total += 1
        identity = row_identity(row)
        raw = (row.get("sources_cited") or "").strip()
        urls = [u for u in (part.strip() for part in raw.split(";")) if u]
        if urls:
            answers_with_citations += 1
        seen_here = set()
        for url in urls:
            domain = normalise_domain(url)
            if domain is None:
                continue
            entry = domains[domain]
            entry["citations"] += 1
            entry["answers"].add(identity)
            entry["by_provider"][identity[0]] += 1
            entry["by_question"][identity[1]] += 1
            # Per-answer flags count each domain once per answer, however many
            # of its pages that one answer cited — otherwise a single answer
            # citing six pages of one directory looks like six answers.
            if domain not in seen_here:
                seen_here.add(domain)
                if identity in client_answers:
                    entry["in_client_answers"] += 1
                if identity in competitor_answers:
                    entry["in_competitor_answers"] += 1

    table = []
    for domain, entry in domains.items():
        table.append({
            "domain": domain,
            "citations": entry["citations"],
            "answers_citing": len(entry["answers"]),
            "by_provider": dict(sorted(entry["by_provider"].items())),
            "by_question": dict(sorted(entry["by_question"].items())),
            "answers_naming_client_that_cite_it": entry["in_client_answers"],
            "answers_naming_a_competitor_that_cite_it": entry["in_competitor_answers"],
            "is_client_own_domain": bool(client_domain) and domain == normalise_domain(client_domain),
        })
    table.sort(key=lambda d: (-d["citations"], -d["answers_citing"], d["domain"]))

    # The actionable list. A domain qualifies only if a competitor was
    # genuinely named in an answer citing it AND the client was named in no
    # such answer. A domain nobody was named alongside is not evidence of a
    # gap, it is just a source.
    competitor_only = [
        d for d in table
        if d["answers_naming_a_competitor_that_cite_it"] > 0
        and d["answers_naming_client_that_cite_it"] == 0
        and not d["is_client_own_domain"]
    ] if client else []

    client_own = [d for d in table if d["is_client_own_domain"]]

    return {
        "answers_analysed": answers_total,
        "answers_with_at_least_one_citation": answers_with_citations,
        "distinct_domains": len(table),
        "client": client,
        "client_domain": normalise_domain(client_domain) if client_domain else None,
        "answers_naming_client": len(client_answers) if client else None,
        "answers_naming_a_competitor": len(competitor_answers) if named_by_business else None,
        "client_own_domain_cited": bool(client_own),
        "client_own_domain_citations": client_own[0]["citations"] if client_own else 0,
        "client_own_domain_questions": sorted(client_own[0]["by_question"]) if client_own else [],
        "domains": table,
        "competitor_cited_client_absent": competitor_only,
    }


def render_text(result, limit=15):
    out = []
    a, c = result["answers_analysed"], result["answers_with_at_least_one_citation"]
    out.append(f"{a} answers analysed, {c} of them citing at least one source.")
    out.append(f"{result['distinct_domains']} distinct domains cited.")
    if result["client"]:
        out.append(
            f"{result['client']} was named in {result['answers_naming_client']} answers; "
            f"a competitor was named in {result['answers_naming_a_competitor']}."
        )
        if result["client_domain"]:
            if result["client_own_domain_cited"]:
                qs = ", ".join(result["client_own_domain_questions"])
                out.append(
                    f"The client's own domain ({result['client_domain']}) was cited "
                    f"{result['client_own_domain_citations']} times, on {qs}."
                )
            else:
                out.append(
                    f"The client's own domain ({result['client_domain']}) was never cited."
                )
    out.append("")
    out.append(f"Most-cited domains (top {limit}):")
    for d in result["domains"][:limit]:
        out.append(
            f"  {d['citations']:>4}  {d['domain']}  "
            f"(in {d['answers_citing']} answers; "
            f"client {d['answers_naming_client_that_cite_it']}, "
            f"competitor {d['answers_naming_a_competitor_that_cite_it']})"
        )
    if result["client"]:
        out.append("")
        gaps = result["competitor_cited_client_absent"]
        if gaps:
            out.append(f"Cited alongside a competitor, never alongside the client ({len(gaps)}):")
            for d in gaps[:limit]:
                out.append(
                    f"  {d['citations']:>4}  {d['domain']}  "
                    f"({d['answers_naming_a_competitor_that_cite_it']} competitor answers)"
                )
        else:
            out.append("No domain was cited alongside a competitor and never alongside the client.")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True, help="Completed trade-run CSV")
    ap.add_argument("--mention-counts", default=None,
                    help="mention-counts.json from tools/mention-count/. Needed for the "
                         "client-versus-competitor half; without it you get the domain census only")
    ap.add_argument("--client", default=None,
                    help="The focal business, exactly as it appears in the mention counts")
    ap.add_argument("--client-domain", default=None,
                    help="The client's own website domain, so its own citations are separated out")
    ap.add_argument("--out", default=None, help="Write the full JSON here (outside this repo)")
    ap.add_argument("--limit", type=int, default=15, help="Rows in the printed summary (default 15)")
    args = ap.parse_args()

    if args.client and not args.mention_counts:
        sys.exit("--client needs --mention-counts: who was named in which answer comes from there.")

    rows, errored, smoke = load_run(args.run)
    if not rows:
        sys.exit(f"No successful rows in {args.run}.")
    named = load_mention_counts(args.mention_counts) if args.mention_counts else None

    result = analyse(rows, named, args.client, args.client_domain)
    result["rows_skipped_errored"] = errored
    result["rows_skipped_smoke"] = smoke

    print(render_text(result, args.limit))
    if errored or smoke:
        print(f"\nSkipped {errored} errored and {smoke} smoke rows.")
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2, ensure_ascii=False)
        print(f"\nWritten to {args.out}")


if __name__ == "__main__":
    main()
