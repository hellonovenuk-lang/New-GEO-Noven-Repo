#!/usr/bin/env python3
"""
Mention count — matches a market census against a completed trade-run CSV,
producing per-business AI-mention counts by provider and question.

Generalised from the matching logic proven on two real runs:
wardith-runs/estate-agents-wirral/crossref.py (the original — name-variant
handling for &/and, apostrophes, Ltd/Estate Agents suffixes) and its Chester
evolution (adds a stopword floor so a stripped-down variant can't collapse
into a common word, a manual-override file for a model's own misspellings,
per-question counts, and skips errored rows). This script is that second
version, with the hardcoded paths and Chester-only stopword replaced by
flags so it works against any completed run.

Matching is alias-based and overlap-aware (added after two real defects):
1. The &/and swap that generates alias forms is case-insensitive, so a
   census brand capitalized "Timeless Kitchens And Bathrooms Limited" still
   generates the "Timeless Kitchens & Bathrooms" alias a model's answer text
   actually used — the previous case-sensitive str.replace() silently never
   produced that alias, undercounting a real business (confirmed against a
   real run: 5 recorded vs. 12 actual).
2. Every alias across every census business is matched within an answer
   FIRST, then overlapping spans are resolved longest-match-wins, so a
   short business name that is literally a substring of a longer one (e.g.
   "Builders Wirral" inside "Abbey Builders Wirral") is credited to the
   longer, more specific business where the two overlap, while a genuinely
   independent, non-overlapping mention of the short name elsewhere still
   counts normally. This replaces an earlier, cruder design that would have
   permanently dropped the shorter alias campaign-wide — that undercounts
   every answer where the short business is genuinely named on its own.
   Every suppressed candidate is recorded in the output's "overlap_log" for
   audit.
3. Every match is anchored so it may not be immediately preceded or
   followed by a letter or digit — a short alias can never match mid-word
   inside an unrelated longer word. This alone would have re-broken a real
   business ("Apex Kitchens Home Improvement Ltd", answer text only ever
   said "...Improvements") that an earlier, fully-unanchored version of
   this script matched by accident. Rather than loosen the boundary back
   up, pluralize_final_token() generates the plural of a brand's final
   token as its own explicit, narrow, auditable, one-directional (extend
   only, never shorten) alias — see its docstring for exactly what it will
   and won't attempt, including a second real defect (a shortened alias
   misattributing a different, unrelated business's mentions) that is why
   it never strips a final token down.

Nothing here decides who is a prospect. It counts mentions; the qualification
skill and CAMPAIGN-HANDOFF.md do the judgement.

Stdlib only, no pip install needed. Requires Python 3.9+.

Usage:
  python3 mention_count.py --run ~/wardith-runs/{trade}-{area}.csv \
      --census market-census-{trade}-{area}.csv --area {area} \
      --out mention-counts.json

  # with a model-misspelling / genuine-alias override file (see
  # --variants-file below):
  python3 mention_count.py --run ... --census ... --area {area} \
      --out ... --variants-file variant-overrides.json
"""

import argparse
import csv
import json
import re
import sys
from collections import Counter

# Generic stopwords a suffix-stripped variant can collapse into — matched
# against real false positives found on the Wirral and Chester runs (e.g.
# "Home Estate Agents" stripping to "Home" matched almost every answer).
GENERIC_STOPWORDS = {
    "home", "homes", "property", "properties", "estate", "estates",
    "agents", "agent", "group", "key", "let", "lets", "letting",
    "lettings", "move", "rent", "centre", "center", "house", "houses",
    "residential", "management", "services", "sales", "premium",
    "the", "partnership", "partners",
}


# Suffix words that are never a genuine plural/singular target — pluralizing
# "Limited" -> "Limiteds" is nonsense, not a real alias. Belt-and-suspenders
# alongside the length-4 floor in pluralize_final_token, which already
# excludes "Ltd"/"LLP" on length alone.
_NON_PLURALIZABLE_FINAL_TOKENS = {"ltd", "llp", "limited"}


def pluralize_final_token(v):
    """A narrow, auditable singular->plural alias of v's FINAL token only —
    not a general English pluralizer, and deliberately one-directional.
    Exists for exactly one confirmed real case: a census brand "Apex
    Kitchens Home Improvement Ltd" only ever appeared in real answer text
    as "Apex Kitchens Home Improvements" (plural). Alphanumeric-boundary
    anchoring in to_pattern() correctly blocks the singular form matching
    mid-word inside the plural one, so the fix is to generate the plural
    form as its own explicit, whole-word alias instead of loosening the
    boundary.

    Only ever EXTENDS the final token (adds "s") — never strips one. A
    second real run proved why the reverse direction is unsafe, not just
    unnecessary: stripping "Bathrooms" -> "Bathroom" from a census brand
    "Wirral Bathrooms Limited" generated an alias generic enough to match
    unrelated prose ("a Wirral bathroom refit") AND to prefix-match a
    completely different, distinct real business ("Wirral Bathroom
    Company") that happened to share no legal connection at all —
    misattributing that business's mentions to this one. Extending a name
    can only make the search pattern MORE specific (still anchored on both
    sides, strictly longer than the original), so it can't become a generic
    prefix of something else; shortening does the opposite. That asymmetry,
    not just "avoid the one bug found", is why this stays one-directional.

    Further conservative guards, so a name that merely ends in a consonant
    for its own reasons isn't mangled:
      - skipped for a final token under 4 characters, or a known non-noun
        suffix word (Ltd/LLP/Limited);
      - skipped entirely if the final token already ends in "s" — nothing
        to extend, and (per above) never stripped either;
      - generated only for the simple, regular "+s" case — skipped for
        endings (x/z/ch/sh) where real English pluralizes with "es" or
        similar, since guessing that beyond a plain "+s" is exactly the
        kind of naive transformation that could produce a wrong form.
    Anything outside this one narrow case (e.g. "Company" -> "Companies",
    or any plural-to-singular need) is not attempted here — use
    --variants-file for that, spot-checked per run, the same as any other
    genuine alias this script can't safely guess.
    """
    m = re.match(r"^(.*\s)?(\S+)$", v)
    if not m:
        return set()
    prefix, last = m.group(1) or "", m.group(2)
    trailing_punct_m = re.match(r"^(.*?)([.,;:!?]*)$", last)
    core, trailing_punct = trailing_punct_m.group(1), trailing_punct_m.group(2)
    if len(core) < 4 or core.lower() in _NON_PLURALIZABLE_FINAL_TOKENS:
        return set()
    low = core.lower()
    if low.endswith(("s", "x", "z", "ch", "sh")):
        return set()
    plural = f"{prefix}{core}s{trailing_punct}"  # Improvement -> Improvements
    return {plural} if plural.strip() else set()


def variants(brand, extra_stopwords):
    v = {brand.strip()}
    base_noparen = re.sub(r"\s*\([^)]*\)", "", brand).strip()
    v.add(base_noparen)
    for b in [brand.strip(), base_noparen]:
        # Case-insensitive &/and swap. A plain str.replace(" and ", " & ")
        # is case-sensitive and silently fails to fire on a Title-Case brand
        # like "Timeless Kitchens And Bathrooms Limited" — the bug that
        # undercounted a real business (5 recorded vs. 12 actual: the "&"
        # form, used in most of the real answer text, was never generated
        # as a variant to search for). re.sub with re.I fires regardless of
        # how the source brand happens to be capitalized.
        v.add(re.sub(r"\s*&\s*", " and ", b, flags=re.I))
        v.add(re.sub(r"\s+and\s+", " & ", b, flags=re.I))
    more = set()
    for b in list(v):
        more.add(re.sub(r"\s+Ltd\.?$", "", b, flags=re.I))
        more.add(re.sub(r"\s+Limited$", "", b, flags=re.I))
        more.add(re.sub(r"\s+LLP$", "", b, flags=re.I))
        more.add(re.sub(r"\s+Estate Agents?$", "", b, flags=re.I))
        more.add(re.sub(r"\s+Estates?$", "", b, flags=re.I))
        more.add(re.sub(r"\s+Property( Group)?$", "", b, flags=re.I))
        more.add(re.sub(r"\s+Sales( & | and )Lettings$", "", b, flags=re.I))
    v |= more
    plural_forms = set()
    for b in list(v):
        plural_forms |= pluralize_final_token(b)
    v |= plural_forms
    stopwords = GENERIC_STOPWORDS | extra_stopwords
    safe = {x.strip() for x in v if x.strip() and len(x.strip()) > 2}
    safe = {x for x in safe if x.lower() not in stopwords}
    return safe


def to_pattern(v):
    # straight and curly apostrophes are equivalent; single-pass substitution
    # so it doesn't rescan and corrupt the bracket expression it just inserted.
    #
    # Alphanumeric-boundary anchored: a match may not be immediately preceded
    # or followed by a letter or digit, so a short alias can never match
    # mid-word inside an unrelated longer word (the earlier, unanchored
    # version let "Apex Kitchens Home Improvement" match as a bare substring
    # of "...Improvements" — technically correct there, but only by luck;
    # nothing stopped it matching mid-word somewhere unrelated too).
    # Deliberately narrower than \b, which treats underscore as a word
    # character and is Unicode-\w-based; an explicit [A-Za-z0-9] lookaround
    # says exactly "alphanumeric", matching the actual requirement. This
    # does NOT block real matches followed by punctuation, markdown
    # (`**Business**`), or a possessive apostrophe ("Business' report") —
    # all non-alphanumeric, so the boundary already holds there; it only
    # blocks genuine mid-word continuation, which is what broke the Apex
    # case. That case is fixed instead by pluralize_final_token() above,
    # generating the plural as its own explicit whole-word alias.
    esc = re.escape(v)
    esc = re.sub(r"'|’", "['’]", esc)
    return re.compile(r"(?<![A-Za-z0-9])" + esc + r"(?![A-Za-z0-9])", re.I)


def load_census(path, business_column):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if rows and business_column not in rows[0]:
        sys.exit(
            f"--business-column '{business_column}' not found in {path}. "
            f"Columns present: {', '.join(rows[0].keys())}"
        )
    return rows


def load_run(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_manual_variants(path):
    if not path:
        return {}
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    return {k: set(v) for k, v in raw.items()}


def build_business_patterns(census, business_column, extra_stopwords, manual_variants):
    """One (business, alias_text, compiled_pattern) tuple per alias, across
    every census business. Manual aliases (--variants-file) are merged in
    here too, so they go through the exact same overlap-safety resolution
    as auto-generated ones — a human vouching for an alias's identity does
    not exempt it from the "don't double-count an overlapping match" rule."""
    business_patterns = []
    variants_by_business = {}
    for entry in census:
        brand = entry[business_column]
        vs = variants(brand, extra_stopwords) | manual_variants.get(brand, set())
        variants_by_business[brand] = vs
        for v in vs:
            business_patterns.append((brand, v, to_pattern(v)))
    return business_patterns, variants_by_business


def find_candidates(text, business_patterns):
    """Every raw regex match, from every business's every alias, within one
    answer's text — before any overlap resolution."""
    candidates = []
    for business, alias_text, pattern in business_patterns:
        for m in pattern.finditer(text):
            candidates.append((m.start(), m.end(), business, alias_text))
    return candidates


def _spans_overlap(a_start, a_end, b_start, b_end):
    return a_start < b_end and b_start < a_end


def resolve_overlaps(candidates):
    """Longest-match-wins, non-overlapping resolution across every business's
    candidate spans in one answer. Deterministic tie-break: longest span
    first, then earliest start, then business name — so two exactly-equal-
    length overlapping candidates (a genuine census data collision) resolve
    the same way every run instead of depending on dict/set ordering.

    Returns (accepted, suppressed):
      accepted   — candidates that survived, each (start, end, business, alias)
      suppressed — candidates beaten by a longer/earlier-claimed span, each
                   as (candidate, blocking_accepted_candidate) so the loser
                   and winner are both recorded for audit.
    """
    ordered = sorted(candidates, key=lambda c: (-(c[1] - c[0]), c[0], c[2]))
    claimed = []
    accepted = []
    suppressed = []
    for cand in ordered:
        cstart, cend = cand[0], cand[1]
        blocker = next(
            (c for c in claimed if _spans_overlap(cstart, cend, c[0], c[1])),
            None,
        )
        if blocker is not None:
            suppressed.append((cand, blocker))
            continue
        claimed.append(cand)
        accepted.append(cand)
    return accepted, suppressed


def count_mentions(census, run_rows, business_column, extra_stopwords, manual_variants):
    business_patterns, variants_by_business = build_business_patterns(
        census, business_column, extra_stopwords, manual_variants
    )

    results = {
        brand: {
            "total": 0,
            "openai": 0,
            "gemini": 0,
            "perplexity": 0,
            "per_question": Counter(),
            "variants_used": sorted(vs),
            "matched_rows": [],
        }
        for brand, vs in variants_by_business.items()
    }
    overlap_log = []

    for row in run_rows:
        if row.get("errors"):
            continue
        text = row.get("answer_text", "") or ""
        if not text:
            continue
        candidates = find_candidates(text, business_patterns)
        if not candidates:
            continue
        accepted, suppressed = resolve_overlaps(candidates)

        row_info = {
            "assistant": row.get("assistant", ""),
            "question_id": row.get("question_id", ""),
            "run_no": row.get("run_no", ""),
        }
        matched_businesses = sorted({c[2] for c in accepted})
        for business in matched_businesses:
            r = results[business]
            r["total"] += 1
            provider = row_info["assistant"]
            if provider in ("openai", "gemini", "perplexity"):
                r[provider] += 1
            r["per_question"][row_info["question_id"]] += 1
            r["matched_rows"].append(dict(row_info))

        for cand, blocker in suppressed:
            overlap_log.append({
                **row_info,
                "suppressed_business": cand[2],
                "suppressed_alias": cand[3],
                "winning_business": blocker[2],
                "winning_alias": blocker[3],
            })

    for r in results.values():
        r["per_question"] = dict(r["per_question"])

    return results, overlap_log


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True, help="Completed trade-run CSV (tools/trade-run/ output)")
    ap.add_argument("--census", required=True, help="Market census CSV — one row per business")
    ap.add_argument("--area", required=True, help="Campaign geography (e.g. 'Chester'). Added to the stopword list automatically — a variant that strips down to just the area name is a guaranteed false-positive risk, not a real match")
    ap.add_argument("--out", required=True, help="Where to write mention-counts.json")
    ap.add_argument("--business-column", default="business", help="Census CSV column holding the business name (default: business). Older census files may use 'brand' instead")
    ap.add_argument("--variants-file", default=None, help="Optional JSON file of {business_name: [extra misspellings/genuine aliases]}, for a model's own recurring misspelling of a brand or a business's known alternate trading name — spot-checked and added per run, not guessed in advance. Goes through the same overlap-safety resolution as every other alias")
    args = ap.parse_args()

    census = load_census(args.census, args.business_column)
    if not census:
        sys.exit(f"No rows in {args.census}")
    run_rows = load_run(args.run)
    if not run_rows:
        sys.exit(f"No rows in {args.run}")

    extra_stopwords = {args.area.strip().lower()}
    manual_variants = load_manual_variants(args.variants_file)

    print(f"Loaded {len(run_rows)} run rows, {len(census)} census businesses", file=sys.stderr)

    results, overlap_log = count_mentions(census, run_rows, args.business_column, extra_stopwords, manual_variants)

    output = dict(results)
    output["_overlap_log"] = overlap_log

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"\n{'business':38s} {'total':>5s} {'oai':>4s} {'gem':>4s} {'ppx':>4s}  questions")
    for brand, r in sorted(results.items(), key=lambda x: -x[1]["total"]):
        qs = ",".join(sorted(r["per_question"].keys()))
        print(f"{brand:38s} {r['total']:5d} {r['openai']:4d} {r['gemini']:4d} {r['perplexity']:4d}  {qs}")
    if overlap_log:
        print(f"\n{len(overlap_log)} overlap-suppressed candidate(s) — see _overlap_log in the output for detail:", file=sys.stderr)
        for entry in overlap_log:
            print(f"  {entry['assistant']}/{entry['question_id']}/run{entry['run_no']}: "
                  f"'{entry['suppressed_alias']}' ({entry['suppressed_business']}) suppressed by "
                  f"'{entry['winning_alias']}' ({entry['winning_business']})", file=sys.stderr)
    print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()
