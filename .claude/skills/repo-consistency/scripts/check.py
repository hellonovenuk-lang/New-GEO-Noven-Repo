#!/usr/bin/env python3
"""
Repo consistency check — the mechanical half of a consistency pass.

Written because the expensive part of keeping this repo honest is not deciding
what to fix, it is *finding* what drifted: eleven thousand lines of markdown
where a price, a file name or a line count can be restated in a dozen places
and go stale in one of them. Reading all of it costs a fortune in tokens and
still misses things, because a stale number looks exactly like a fresh one.

So the machine does the sweep and the model does the judgement. Everything in
here is a check that can be decided by comparison rather than by taste:
does this price match the canonical price, does this file exist, does this
count match the thing it counts. Anything requiring an opinion — is this
paragraph worth keeping, should these two files be one file — is deliberately
left to the caller, with the evidence laid out.

Stdlib only, Python 3.9+. No network, no API keys, no writes: this reports and
never edits. Sits beside ops/site-check/ and ops/name-check/ as the third tool
in that shape.

Usage:
  python check.py                          # full sweep, text report
  python check.py --only facts,refs        # just those checks
  python check.py --json                   # machine-readable, for piping
  python check.py --root /path/to/repo     # default: repo containing this file
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------- setup

CHECKS = ["facts", "names", "refs", "sections", "counts", "dupes", "status", "bloat"]

TEXT_SUFFIXES = {".md", ".txt"}
CODE_SUFFIXES = {".ts", ".astro", ".css", ".mjs", ".js", ".py", ".html", ".json"}

NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
    "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20,
}


class Finding:
    """One thing that looks wrong, with enough context to judge it."""

    def __init__(self, check, severity, path, line, message, evidence="", fix=""):
        self.check = check
        self.severity = severity  # "error" | "verify" | "note"
        self.path = path
        self.line = line
        self.message = message
        self.evidence = evidence
        self.fix = fix  # a concrete suggested replacement, when there is one

    def as_dict(self):
        return {
            "check": self.check,
            "severity": self.severity,
            "path": self.path,
            "line": self.line,
            "message": self.message,
            "evidence": self.evidence,
            "fix": self.fix,
        }


def load_config(skill_dir):
    with open(skill_dir / "config.json", encoding="utf-8") as fh:
        return json.load(fh)


def find_root(start):
    """Walk up to the git root, so the script works from anywhere."""
    cur = start.resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / ".git").exists():
            return candidate
    return cur


def is_historical(rel_path, config):
    """Old facts are correct in files whose job is to record the past."""
    return any(rel_path.startswith(p) for p in config["historical_paths"])


def collect_files(root, config, suffixes):
    out = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in suffixes:
            continue
        rel = str(path.relative_to(root))
        if any(rel.startswith(p) for p in ("node_modules/", ".git/")):
            continue
        out.append((rel, path))
    return out


def read_lines(path):
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, OSError):
        return []


# ---------------------------------------------------------------- canonical facts

def parse_canonical(root, config):
    """
    Pull the current facts out of the source of truth.

    Deliberately regex rather than a TypeScript parse: the file is hand-written
    and stable in shape, and a dependency-free checker is one that still runs in
    two years. If this stops matching, the check reports that loudly rather than
    silently finding nothing — an empty fact set is treated as a failure below.
    """
    src_path = root / config["canonical_source"]
    if not src_path.exists():
        return None, f"canonical source not found: {config['canonical_source']}"

    src = src_path.read_text(encoding="utf-8")
    facts = {"prices": {}, "emails": set(), "name": None}

    m = re.search(r"^\s*name:\s*'([^']+)'", src, re.M)
    if m:
        facts["name"] = m.group(1)

    for m in re.finditer(r"[\w.+-]+@[\w-]+\.[\w.]+", src):
        facts["emails"].add(m.group(0))

    # Plan objects: id, then price a few lines later. Non-greedy across the
    # object body so an id never pairs with the next plan's price.
    for m in re.finditer(r"id:\s*'(\w+)'.*?price:\s*(\d+)", src, re.S):
        facts["prices"][m.group(1)] = int(m.group(2))

    if not facts["prices"] or not facts["name"]:
        return facts, (
            "parsed the canonical source but found no prices or no name — the "
            "file's shape has changed and check.py needs updating before its "
            "fact checks can be trusted"
        )
    return facts, None


# ---------------------------------------------------------------- checks

def check_facts(root, config, facts, findings):
    """
    A price stated in prose that disagrees with the canonical price.

    This is the check that matters most. Prices live in business.ts and are
    rendered from there, so the site is always right — but the operating
    documents restate them in prose, and prose does not recompile. A doc that
    says the audit is £125 when it is £250 is not a typo, it is a document that
    will be believed and acted on.
    """
    if not facts or not facts["prices"]:
        return

    alias_to_plan = {}
    for plan_id, aliases in config["plan_aliases"].items():
        for alias in aliases:
            alias_to_plan[alias.lower()] = plan_id

    # Digit-anchored so a lone "£," never parses, and pence-free: "£1.20 per
    # 150 queries" is a running cost, not a price, and matching it as "£1"
    # produced a confident, wrong finding on the first run of this script.
    money = re.compile(r"£\s?(\d[\d,]*)(?!\.\d)")
    record_heading = config["record_section_heading"]
    current_prices = set(facts["prices"].values())
    canonical_ladder = [facts["prices"][k] for k in config["plan_aliases"]
                        if k in facts["prices"]]
    seen_amounts = defaultdict(list)

    for rel, path in collect_files(root, config, TEXT_SUFFIXES | CODE_SUFFIXES):
        if is_historical(rel, config) or rel == config["canonical_source"]:
            continue
        record_level = None
        prev_line = ""
        for n, line in enumerate(read_lines(path), 1):

            # A live document can contain sections whose job is to record a
            # price change — "## 9. The repricing — 2026-07-31" is the argument
            # for today's prices and has to state yesterday's. Flagging those is
            # not merely noise: acting on it would rewrite the reasoning into
            # nonsense ("Audit £250 → £250").
            #
            # The pattern is deliberately narrow. An earlier version accepted any
            # dated heading containing "changed", which swallowed ROADMAP.md's
            # "What changed on 2026-08-06" — a status section describing the
            # present — and with it a genuinely stale £95 sitting underneath.
            # Suppressing a real finding is far worse than printing a noisy one,
            # so this errs towards reporting.
            heading = re.match(r"^(#{1,6})\s+(.*)$", line)
            if heading:
                level, text = len(heading.group(1)), heading.group(2)
                # Subsections stay inside their parent record section; only a
                # heading at the same or higher level closes it.
                if record_level is not None and level <= record_level:
                    record_level = None
                if record_level is None and re.search(
                        record_heading, text, re.I):
                    record_level = level
            if record_level is not None:
                prev_line = line
                continue

            matches = list(money.finditer(line))
            if not matches:
                prev_line = line
                continue
            lowered = line.lower()

            # Where each plan is named on this line, so an amount can be
            # attributed to the nearest one. A row like "Grow | £250/month |
            # Maintain across 15 questions" names two plans and one price;
            # charging that price to both plans invents a fault that isn't there.
            alias_positions = []
            for alias, plan_id in alias_to_plan.items():
                for m in re.finditer(rf"\b{re.escape(alias)}\b", lowered):
                    alias_positions.append((m.start(), plan_id))

            # A line comparing old and new, quoting a range, or weighing a price
            # that does not exist yet is discussing prices rather than stating
            # one. The arrow is the giveaway for a move ("Audit £125 → £250");
            # the hedges are the giveaway for a hypothetical ("whether a deeper
            # tier nearer £750 is worth having").
            discursive = bool(re.search(
                r"→|->|[–—]|\bwas\b|\bpreviously\b|\bold\b|\bsuperseded\b|"
                # "whether" was tried here and removed: it is ordinary English
                # ("re-check whether Maintain's £95/month still holds") and it
                # demoted two genuinely stale prices to a softer grade.
                r"\bused to\b|\bfrom £|\bwhat changed\b|\bnearer\b|"
                r"\baround\b|\broughly\b|\bcirca\b|\bhigher-priced\b|"
                r"\bwould be\b|\bcould be\b",
                line + " " + prev_line, re.I))

            # Every £ figure on the line, pence included. The attribution test
            # below needs to see fees like "£0.20" even though they are never
            # candidates themselves — otherwise a fee column is invisible and an
            # amount binds to a plan name three columns away.
            all_money = [m.start() for m in re.finditer(r"£\s?\d", line)]

            # A ladder quoted without naming its plans — "Monthly plans (£95 /
            # £250 / £495)" — carries no alias for the rule below to bind to, so
            # it slipped through entirely until a heading in ROADMAP.md was found
            # still advertising the superseded ladder. Three or more amounts on
            # one line, not one of them a current price, is that shape.
            # Bound to lines that actually claim to be listing our plans. An
            # unbound version flagged the ICO fee and the domain renewal, and
            # "none of them current" also missed this very case, because £250 is
            # a current price — the audit's — sitting inside a stale monthly
            # ladder. What matters is that every amount in a plan ladder should
            # be a current plan price.
            if len(matches) >= 3 and not discursive and re.search(
                    r"\b(plans?|tiers?|ladder|pricing)\b", lowered):
                values = [int(m.group(1).replace(",", "")) for m in matches]
                stale = [v for v in values if v not in current_prices]
                if stale:
                    findings.append(Finding(
                        "facts", "error", rel, n,
                        "price ladder containing "
                        + ", ".join(f"£{v:,}" for v in stale)
                        + ", which "
                        + ("is not a" if len(stale) == 1 else "are not")
                        + " current price"
                        + ("" if len(stale) == 1 else "s")
                        + " — the ladder is now "
                        + " / ".join(f"£{p:,}" for p in canonical_ladder),
                        evidence=line.strip()[:200],
                    ))

            for m in matches:
                value = int(m.group(1).replace(",", ""))
                seen_amounts[value].append(f"{rel}:{n}")
                if not alias_positions:
                    continue
                pos, plan_id = min(alias_positions,
                                   key=lambda ap: abs(ap[0] - m.start()))

                # Only bind an amount to a plan name when no other £ figure sits
                # between the two. A table row like "£800 Foundation | invoice |
                # £0 (bank transfer)" names one plan and two amounts, and the £0
                # is a bank fee — attaching it to Foundation invents a fault.
                lo, hi = min(pos, m.start()), max(pos, m.start())
                if any(lo < other < hi for other in all_money
                       if other != m.start()):
                    continue

                expected = facts["prices"].get(plan_id)
                if expected is None or value == expected:
                    continue

                # If the line already states this plan's correct price, the
                # other number is something else — a fee, a competitor's rate, a
                # running cost. "an audit's tool cost lands under £2 against a
                # £250 audit" is the document being right, not wrong.
                if re.search(rf"£\s?{expected:,}(?![\d.])".replace(",", "[,]?"), line):
                    continue
                findings.append(Finding(
                    "facts", "verify" if discursive else "error", rel, n,
                    f"£{value:,} stated next to the {plan_id} plan, "
                    f"but the canonical price is £{expected:,}"
                    + (" (line reads as discussion or a range — read it before "
                       "changing)" if discursive else ""),
                    evidence=line.strip()[:200],
                    fix="" if discursive else f"£{expected:,}",
                ))

            prev_line = line

    current = set(facts["prices"].values())
    for value, places in sorted(seen_amounts.items()):
        if value in current or len(places) < 3:
            continue
        findings.append(Finding(
            "facts", "note", places[0].split(":")[0], int(places[0].split(":")[1]),
            f"£{value:,} appears {len(places)} times and is not a current price — "
            f"check whether it is a superseded figure or an unrelated cost",
            evidence=", ".join(places[:6]),
        ))


def check_names(root, config, facts, findings):
    """
    A superseded name or domain outside the files that record history.

    A half-finished rename is the most embarrassing kind of inconsistency,
    because the business sells consistency of its own facts. Historical paths
    are skipped: the session log saying "Noven" is the log doing its job.
    """
    # Aggregated per file and term rather than per line. A half-finished rename
    # is fixed one file at a time — a reader who gets 224 separate findings for
    # one rename has been given noise, not a list of decisions.
    hits = defaultdict(lambda: {"live": [], "historical": []})

    for rel, path in collect_files(root, config, TEXT_SUFFIXES | CODE_SUFFIXES):
        if is_historical(rel, config):
            continue
        for n, line in enumerate(read_lines(path), 1):
            for term in config["superseded_terms"]:
                if not re.search(rf"(?<![\w@.]){re.escape(term)}(?![\w-])", line, re.I):
                    continue
                # A line recording what happened is not a victim of it. Ticked
                # checklist items and past-tense narration are the two shapes
                # that recur: "[x] Decide whether Noven keeps its name. It does
                # not." is the record working correctly.
                narrating = bool(re.match(r"\s*[-*]\s*\[[xX]\]", line)) or re.search(
                    r"\b(was|were|formerly|renamed|previously|old|deleted|until|"
                    r"superseded|used to|history|legacy|redirect|alias|archived|"
                    r"belongs to somebody else|returned|before)\b", line, re.I)
                bucket = "historical" if narrating else "live"
                hits[(rel, term)][bucket].append((n, line.strip()[:160]))
                break

    # Pairs a previous run judged correct-as-history, with the reason. Recorded
    # rather than pattern-matched, because "the Noven self-audit" is the name of
    # a past event and no regex reliably tells that from a stale fact. They are
    # still printed — downgraded, with the reason — so the judgement stays
    # visible and can be reversed, instead of silently disappearing.
    reviewed = {(r["path"], r["term"]): r.get("reason", "")
                for r in config.get("reviewed_names", [])}

    for (rel, term), buckets in sorted(hits.items()):
        live, hist = buckets["live"], buckets["historical"]
        if (rel, term) in reviewed:
            findings.append(Finding(
                "names", "note", rel, (live or hist)[0][0],
                f"'{term}' appears {len(live) + len(hist)}x — reviewed and kept: "
                f"{reviewed[(rel, term)]}",
            ))
            continue
        if live:
            where = ", ".join(f"line {n}" for n, _ in live[:4])
            more = f" and {len(live) - 4} more" if len(live) > 4 else ""
            findings.append(Finding(
                "names", "error", rel, live[0][0],
                f"'{term}' used as a current fact {len(live)}x ({where}{more})"
                + (f"; {len(hist)} further mentions read as history and are "
                   f"probably correct" if hist else ""),
                evidence=live[0][1],
                fix=facts["name"] if facts and term.lower() == "noven" else "",
            ))
        elif hist:
            findings.append(Finding(
                "names", "note", rel, hist[0][0],
                f"'{term}' appears {len(hist)}x, all in lines that read as a "
                f"record of the rename — leave unless the file is meant to "
                f"describe only the present",
                evidence=hist[0][1],
            ))


def check_refs(root, config, findings):
    """
    A backticked path that points at nothing.

    Docs here reference each other constantly and by name. When a file is
    renamed or deleted the references do not move, and a reader following one
    hits a wall — the cheapest possible failure to detect and the most annoying
    to hit.
    """
    ref = re.compile(r"`([A-Za-z0-9_][A-Za-z0-9_./-]*\.(?:md|ts|astro|css|py|txt|json|mjs|html))`")

    # Docs cite files by bare name — `robots.txt`, `business.ts` — and mean the
    # one file in the repo with that name, wherever it lives. Resolving only
    # against the current directory reports those as broken, which is worse
    # than useless: it trains the reader to ignore this check.
    by_basename = defaultdict(list)
    for path in root.rglob("*"):
        if path.is_file():
            rel_p = str(path.relative_to(root))
            if not rel_p.startswith(("node_modules/", ".git/")):
                by_basename[path.name].append(rel_p)

    # Paths that are built rather than committed. `dist/index.html` is missing
    # from a clean checkout by design, and reporting it teaches the reader to
    # skim this check.
    built = re.compile(r"^(dist|build|out|\.astro|node_modules)/")

    # Files a document legitimately names but that live outside this repo.
    # `ops/audit-method.md` §5 puts client audit data in the client's own folder
    # on purpose — the per-run `timings.md` is supposed to be absent here.
    external_files = set(config.get("external_files", []))

    for rel, path in collect_files(root, config, TEXT_SUFFIXES):
        if is_historical(rel, config):
            continue
        here = Path(rel).parent
        in_deleted_section = False
        for n, line in enumerate(read_lines(path), 1):

            # A section headed "Deleted 2026-07-31" exists to say what is gone.
            # Its references dangle on purpose, and the explanation is the point.
            heading = re.match(r"^#{1,6}\s+(.*)$", line)
            if heading:
                in_deleted_section = bool(re.search(
                    r"\b(deleted|removed|retired|closed)\b", heading.group(1), re.I))

            for target in ref.findall(line):
                candidates = [
                    root / target,
                    root / here / target,
                    root / "ops" / target,
                ]
                if any(c.exists() for c in candidates):
                    continue
                if "/" not in target and by_basename.get(target):
                    continue
                if built.match(target) or target in external_files:
                    continue
                # Deliberate mentions of deleted files are a record, not a bug —
                # as is a ticked checklist item recording the deletion.
                historical = in_deleted_section or re.match(
                    r"\s*[-*]\s*\[[xX]\]", line) or re.search(
                    r"\b(deleted|removed|renamed|formerly|was|used to|no longer|"
                    r"replaced|never|resolved|if either becomes real)\b", line, re.I)
                findings.append(Finding(
                    "refs", "note" if historical else "error", rel, n,
                    f"reference to `{target}` which does not exist"
                    + (" (line reads as a deliberate historical mention)" if historical else ""),
                    evidence=line.strip()[:200],
                ))


def check_sections(root, config, findings):
    """
    A cross-file pointer to a numbered section, resolved.

    "See service-tiers.md section 9" is only useful if section 9 is still the
    section that was meant. Sections get inserted above one another, and the
    pointer silently starts meaning something else. This cannot be decided
    mechanically — so the check resolves the pointer and prints the heading it
    lands on, and the caller reads whether it matches the sentence around it.
    """
    pointer = re.compile(
        r"`([A-Za-z0-9_./-]+\.md)`[^.\n]{0,60}?(?:section|§)\s*(\d+)", re.I)

    heading_cache = {}

    def headings_for(target_rel):
        if target_rel in heading_cache:
            return heading_cache[target_rel]
        found = {}
        tpath = root / target_rel
        if tpath.exists():
            for line in read_lines(tpath):
                m = re.match(r"^#{1,3}\s+(\d+)\.\s+(.+)$", line)
                if m:
                    found[int(m.group(1))] = m.group(2).strip()
        heading_cache[target_rel] = found
        return found

    for rel, path in collect_files(root, config, TEXT_SUFFIXES):
        if is_historical(rel, config):
            continue
        here = Path(rel).parent
        for n, line in enumerate(read_lines(path), 1):
            for target, num in pointer.findall(line):
                resolved = None
                for candidate in (target, str(here / target), f"ops/{target}"):
                    if (root / candidate).exists():
                        resolved = candidate
                        break
                if not resolved:
                    continue
                headings = headings_for(resolved)
                if not headings:
                    continue
                title = headings.get(int(num))
                if title is None:
                    findings.append(Finding(
                        "sections", "error", rel, n,
                        f"points at `{target}` section {num}, which does not exist "
                        f"(that file has sections {min(headings)}–{max(headings)})",
                        evidence=line.strip()[:200],
                    ))
                else:
                    findings.append(Finding(
                        "sections", "verify", rel, n,
                        f"`{target}` section {num} is \"{title}\" — does that match "
                        f"what this sentence claims is there?",
                        evidence=line.strip()[:200],
                    ))


def check_counts(root, config, findings):
    """
    A document counting something, checked against the thing it counts.

    Self-describing prose is the quietest liar in a repo: "fourteen files",
    "1,100 lines". It was true when written, nobody re-reads it, and it decays
    on every commit. Both forms below are real drift found in this repo.
    """
    line_claim = re.compile(r"`([A-Za-z0-9_./-]+\.md)`[^.\n]{0,40}?([\d,]{3,})\s+lines", re.I)
    line_claim_rev = re.compile(r"([\d,]{3,})\s+lines[^.\n]{0,40}?`([A-Za-z0-9_./-]+\.md)`", re.I)
    file_claim = re.compile(r"\b([A-Za-z]+|\d+)\s+(?:other\s+|more\s+)?files\b", re.I)

    for rel, path in collect_files(root, config, TEXT_SUFFIXES):
        if is_historical(rel, config):
            continue
        here = Path(rel).parent
        for n, line in enumerate(read_lines(path), 1):

            pairs = [(t, c) for t, c in line_claim.findall(line)]
            pairs += [(t, c) for c, t in line_claim_rev.findall(line)]
            for target, claimed_raw in pairs:
                resolved = next(
                    (c for c in (target, str(here / target), f"ops/{target}")
                     if (root / c).exists()), None)
                if not resolved:
                    continue
                actual = len(read_lines(root / resolved))
                claimed = int(claimed_raw.replace(",", ""))
                # Round claims ("1,100 lines") are approximations; allow 10%.
                if abs(actual - claimed) > max(50, claimed * 0.1):
                    findings.append(Finding(
                        "counts", "error", rel, n,
                        f"says `{target}` is {claimed:,} lines; it is {actual:,}",
                        evidence=line.strip()[:200],
                        fix=f"{actual:,} lines",
                    ))

            # "N files" is only checkable when the sentence says which folder it
            # is counting. Prose like "six files agreeing with each other" counts
            # an argument, not a directory, and guessing at it produced findings
            # that were simply wrong.
            named_dir = re.search(r"`([A-Za-z0-9_./-]+/)`", line)
            index_line = Path(rel).name.lower() == "readme.md" and n <= 10
            if not (named_dir or index_line):
                continue
            target_dir = root / named_dir.group(1) if named_dir else root / here
            if not target_dir.is_dir():
                continue

            for word in file_claim.findall(line):
                claimed = NUMBER_WORDS.get(word.lower())
                if claimed is None and word.isdigit():
                    claimed = int(word)
                if claimed is None:
                    continue
                siblings = [p for p in target_dir.glob("*.md")
                            if p.name.lower() != "readme.md"]
                actual = len(siblings)
                if actual and claimed != actual:
                    rel_dir = target_dir.relative_to(root)
                    findings.append(Finding(
                        "counts", "error", rel, n,
                        f"claims {claimed} files; {rel_dir}/ holds {actual} .md "
                        f"files besides its index",
                        evidence=line.strip()[:200],
                        fix=f"{actual} files",
                    ))


def check_dupes(root, config, findings):
    """
    The same passage written twice in two places.

    Duplication is where inconsistency comes from: two copies of a fact are two
    chances to update one and forget the other. It is also pure token cost —
    every session that reads both pays twice for one idea. Near-duplicates are
    reported rather than exact ones, because the dangerous case is two copies
    that have already started to diverge.
    """
    min_chars = config["duplicate_min_chars"]
    threshold = config["duplicate_similarity"]

    paragraphs = []
    for rel, path in collect_files(root, config, TEXT_SUFFIXES):
        if is_historical(rel, config):
            continue
        lines = read_lines(path)
        buf, start = [], 1
        for n, line in enumerate(lines + [""], 1):
            if line.strip():
                if not buf:
                    start = n
                buf.append(line)
                continue
            if buf:
                text = " ".join(buf)
                if len(text) >= min_chars:
                    words = re.findall(r"[a-z0-9£]+", text.lower())
                    shingles = {tuple(words[i:i + 4]) for i in range(len(words) - 3)}
                    if shingles:
                        paragraphs.append((rel, start, text, shingles))
                buf = []

    for i in range(len(paragraphs)):
        rel_a, line_a, text_a, sh_a = paragraphs[i]
        for j in range(i + 1, len(paragraphs)):
            rel_b, line_b, _, sh_b = paragraphs[j]
            if abs(len(sh_a) - len(sh_b)) > max(len(sh_a), len(sh_b)) * 0.5:
                continue
            overlap = len(sh_a & sh_b)
            if not overlap:
                continue
            score = overlap / len(sh_a | sh_b)
            if score >= threshold:
                findings.append(Finding(
                    "dupes", "verify", rel_a, line_a,
                    f"{int(score * 100)}% the same as {rel_b}:{line_b} — "
                    f"decide which copy is canonical and make the other point at it",
                    evidence=text_a[:200],
                ))


def check_status(root, config, findings):
    """
    An operating document with no status line.

    ops/README.md defines a four-word vocabulary — Live, Decided-unvalidated,
    Closed, Stub — and says it is "worth adding to each file's header". The
    distinction it draws is the one most easily got wrong: a decision written
    down reads exactly like a thing that works.
    """
    vocab = config["status_vocabulary"]
    for rel, path in collect_files(root, config, TEXT_SUFFIXES):
        if is_historical(rel, config) or Path(rel).name == "README.md":
            continue
        if not any(rel.startswith(p) for p in config["status_required_in"]):
            continue
        head = " ".join(read_lines(path)[:15])
        if not any(word.lower() in head.lower() for word in vocab):
            findings.append(Finding(
                "status", "note", rel, 1,
                "no status in the first 15 lines — a reader cannot tell whether "
                f"this describes something working or something merely decided "
                f"(vocabulary: {', '.join(vocab)})",
            ))


def check_bloat(root, config, findings):
    """
    Where the reading cost actually is.

    Not a fault on its own — length is often earned. This exists so a condensing
    pass starts at the twenty thousand words that cost the most to read rather
    than at whatever file happened to be open.
    """
    sizes = []
    for rel, path in collect_files(root, config, TEXT_SUFFIXES):
        if any(rel.startswith(p) for p in ("node_modules/", ".git/")):
            continue
        lines = read_lines(path)
        words = sum(len(l.split()) for l in lines)
        sizes.append((words, len(lines), rel))

    total = sum(w for w, _, _ in sizes)
    for words, lines, rel in sorted(sizes, reverse=True)[:12]:
        share = (words / total * 100) if total else 0
        findings.append(Finding(
            "bloat", "note", rel, 1,
            f"{words:,} words / {lines:,} lines — {share:.0f}% of all prose in the repo",
        ))


# ---------------------------------------------------------------- reporting

SEVERITY_ORDER = {"error": 0, "verify": 1, "note": 2}


def report_text(findings, facts, warning):
    out = []
    out.append("REPO CONSISTENCY CHECK")
    out.append("=" * 70)
    if facts and facts.get("prices"):
        prices = ", ".join(f"{k} £{v:,}" for k, v in facts["prices"].items())
        out.append(f"Canonical: {facts['name']} | {prices}")
    if warning:
        out.append(f"!! {warning}")
    out.append("")

    by_check = defaultdict(list)
    for f in findings:
        by_check[f.check].append(f)

    counts = defaultdict(int)
    for f in findings:
        counts[f.severity] += 1
    out.append(f"{counts['error']} errors, {counts['verify']} to verify, "
               f"{counts['note']} notes")
    out.append("")

    for check in CHECKS:
        items = by_check.get(check)
        if not items:
            continue
        out.append(f"--- {check.upper()} ({len(items)}) " + "-" * (50 - len(check)))
        items.sort(key=lambda f: (SEVERITY_ORDER[f.severity], f.path, f.line))
        for f in items:
            marker = {"error": "[!]", "verify": "[?]", "note": "[ ]"}[f.severity]
            out.append(f"{marker} {f.path}:{f.line}  {f.message}")
            if f.evidence:
                out.append(f"      | {f.evidence}")
            if f.fix:
                out.append(f"      -> suggested: {f.fix}")
        out.append("")

    if not findings:
        out.append("Nothing found.")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", help="repo root (default: git root above this script)")
    parser.add_argument("--only", help=f"comma-separated subset of: {','.join(CHECKS)}")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parent
    root = Path(args.root).resolve() if args.root else find_root(skill_dir)
    config = load_config(skill_dir)

    selected = CHECKS
    if args.only:
        selected = [c.strip() for c in args.only.split(",") if c.strip() in CHECKS]
        if not selected:
            parser.error(f"--only must name one of: {', '.join(CHECKS)}")

    facts, warning = parse_canonical(root, config)
    findings = []

    runners = {
        "facts": lambda: check_facts(root, config, facts, findings),
        "names": lambda: check_names(root, config, facts, findings),
        "refs": lambda: check_refs(root, config, findings),
        "sections": lambda: check_sections(root, config, findings),
        "counts": lambda: check_counts(root, config, findings),
        "dupes": lambda: check_dupes(root, config, findings),
        "status": lambda: check_status(root, config, findings),
        "bloat": lambda: check_bloat(root, config, findings),
    }
    for check in selected:
        runners[check]()

    if args.json:
        print(json.dumps({
            "root": str(root),
            "canonical": {
                "name": facts.get("name") if facts else None,
                "prices": facts.get("prices") if facts else {},
                "emails": sorted(facts.get("emails", [])) if facts else [],
            },
            "warning": warning,
            "findings": [f.as_dict() for f in findings],
        }, indent=2))
    else:
        print(report_text(findings, facts, warning))

    return 1 if any(f.severity == "error" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
