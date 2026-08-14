#!/usr/bin/env python3
"""
Trade run — asks the three assistants a trade-and-area question set and
logs every answer. Per archive/outreach.md section 4.

**This is a copy of archive/audits/noven-2026-08-02/audit_query.py**, which was
written as a throwaway for the 2 August self-audit and turned out to be
reusable. Three things changed and nothing else: the client name is a flag
rather than the one slug that audit hardcoded, the run count is a flag
rather than that audit's five-vs-ten experiment, and the defaults suit a
trade run. **The original is frozen as part of that audit's record — change this
file, never that one.**

It is still not "the runner" that archive/audit-method.md section 7 defers.
A trade run is prospecting, not a client audit: it asks about a trade and an
area, nobody has paid for it, and it produces the mention table in
archive/outreach.md section 4 rather than a report.

Stdlib only, no pip install needed. Requires Python 3.9+.

Env vars — six of them, loaded from the keys file before running. On Windows
that is `. "$HOME\.noven\env.ps1"`; elsewhere `source ~/.noven/env`. See
"Setting up the machine" in README.md, and do not guess a model name:
  OPENAI_API_KEY       OPENAI_MODEL
  GEMINI_API_KEY        GEMINI_MODEL
  PERPLEXITY_API_KEY    PERPLEXITY_MODEL

Usage, the checks to run first and what the output is good for are all in
README.md beside this file. Short version, and smoke first, always:

  python3 trade_run.py --questions questions-wirral-dentists.csv \
      --client wirral-dentists --location Wirral \
      --out ~/wardith-runs/wirral-dentists.csv --smoke

  python3 trade_run.py --questions questions-wirral-dentists.csv \
      --client wirral-dentists --location Wirral \
      --out ~/wardith-runs/wirral-dentists.csv --cap 90

**--out must point outside this repository.** Answer text names real
businesses and sometimes real people; archive/audit-method.md section 5 keeps
that out of a repo written as though it were public.
"""

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

PROVIDERS = ["openai", "gemini", "perplexity"]

# Five runs per question, the same default the self-audit settled on: one run
# tells you about a phrasing, five tell you about a business. The self-audit's
# five-vs-ten experiment on q01/q06/q09 is not repeated here — it belongs to
# that audit's design, and a trade run wants an even sample across questions
# so the mention counts are comparable between them.
DEFAULT_RUNS = 5

FIELDS = [
    "audit_id", "client", "run_at", "assistant", "surface", "model_version",
    "question_id", "run_no", "outcome", "competitors", "errors",
    "sources_cited", "answer_text", "notes",
]


def env(name):
    v = os.environ.get(name)
    if not v:
        sys.exit(
            f"Missing {name} — load the keys file first "
            f"(Windows: . \"$HOME\\.noven\\env.ps1\"), and make sure all six "
            f"variables are set. See 'Setting up the machine' in README.md."
        )
    return v


def post_json(url, headers, body, timeout=120):
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        url, data=data,
        headers={**headers, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        # Surface the provider's actual error body (why, not just the status
        # code) instead of losing it — that's the thing worth logging.
        detail = e.read().decode(errors="replace")
        raise RuntimeError(f"HTTP {e.code} from {url}: {detail[:800]}") from None


def call_openai(question, location):
    # location is unused here — OpenAI's web_search tool only takes a
    # country, not a city, and "GB" already covers every trade-run area.
    del location
    key = env("OPENAI_API_KEY")
    model = env("OPENAI_MODEL")
    body = {
        "model": model,
        "input": question,
        "tools": [{
            "type": "web_search",
            "user_location": {"type": "approximate", "country": "GB"},
        }],
        # Confirmed via the Playground's own "View code" 2026-08-02: without
        # this, web_search_call sources are not returned at all, regardless
        # of the tool being enabled.
        "include": ["web_search_call.action.sources"],
    }
    data = post_json(
        "https://api.openai.com/v1/responses",
        {"Authorization": f"Bearer {key}"},
        body,
    )
    model_version = data.get("model", model)
    text_parts, sources = [], []
    for item in data.get("output", []):
        if item.get("type") == "message":
            for c in item.get("content", []):
                if c.get("type") == "output_text":
                    text_parts.append(c.get("text", ""))
                    for ann in c.get("annotations", []):
                        if ann.get("type") == "url_citation" and ann.get("url"):
                            sources.append(ann["url"])
        elif item.get("type") == "web_search_call":
            for src in item.get("action", {}).get("sources", []):
                if isinstance(src, dict) and src.get("url"):
                    sources.append(src["url"])
                elif isinstance(src, str):
                    sources.append(src)
    return model_version, "".join(text_parts), sources


def call_gemini(question, location):
    # NB: no documented UK-locale parameter for the google_search grounding
    # tool as of when this was written — this is exactly what smoke-test
    # check 3 ("does the answer look UK-shaped") exists to catch. Verify
    # against the current Gemini API docs before the real run. location is
    # accepted for signature parity with the other two callers but unused
    # until Google documents a locale parameter at this API tier.
    del location
    key = env("GEMINI_API_KEY")
    model = env("GEMINI_MODEL")
    body = {
        "contents": [{"parts": [{"text": question}]}],
        "tools": [{"google_search": {}}],
    }
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={key}"
    )
    data = post_json(url, {}, body)
    model_version = data.get("modelVersion", model)
    text_parts, sources = [], []
    for cand in data.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            if "text" in part:
                text_parts.append(part["text"])
        gm = cand.get("groundingMetadata", {})
        for chunk in gm.get("groundingChunks", []):
            uri = chunk.get("web", {}).get("uri")
            if uri:
                sources.append(uri)
    return model_version, "".join(text_parts), sources


def call_perplexity(question, location):
    # Corrected 2026-08-13: the previous version of this function called
    # /v1/responses, which is Perplexity's separate Agent API (a multi-
    # provider orchestration endpoint whose model field expects
    # provider-prefixed names like "openai/gpt-5.6-sol" or a curated preset)
    # — not a retired Sonar. Sonar Chat Completions is still live, at
    # /v1/sonar (or the /chat/completions OpenAI-SDK alias), confirmed
    # against docs.perplexity.ai. It takes a plain chat-completions body —
    # grounding is built into the model, there is no tools field to set —
    # and returns the standard choices[].message.content shape plus a
    # top-level "citations" array of URLs.
    #
    # Added 2026-08-14, confirmed against docs.perplexity.ai's API
    # reference: web_search_options.user_location narrows Sonar's own
    # search step by geography — the same job OpenAI's user_location does;
    # Gemini has no equivalent. `location` is the run's own --location value
    # (wired through from main() 2026-08-14, replacing an earlier version
    # that hardcoded a single campaign's city here) — only `city` varies per
    # run; country/region stay GB/England because every trade run so far has
    # been UK-only.
    key = env("PERPLEXITY_API_KEY")
    model = env("PERPLEXITY_MODEL")
    body = {
        "model": model,
        "messages": [{"role": "user", "content": question}],
        "web_search_options": {
            "user_location": {
                "country": "GB",
                "region": "England",
                "city": location,
            }
        },
    }
    data = post_json(
        "https://api.perplexity.ai/v1/sonar",
        {"Authorization": f"Bearer {key}"},
        body,
    )
    model_version = data.get("model", model)
    answer = data["choices"][0]["message"]["content"]
    sources = data.get("citations", [])
    return model_version, answer, sources


CALLERS = {"openai": call_openai, "gemini": call_gemini, "perplexity": call_perplexity}


def load_questions(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_done(path):
    # Only a row that actually succeeded counts as done. A row carrying an
    # error is a failed attempt, and re-running must retry it rather than
    # skip it — otherwise a provider rate-limiting halfway through leaves
    # holes that can only be fixed by hand-editing the CSV.
    #
    # NB an empty answer_text with no error is a real result, not a failure:
    # that is how an ungrounded Gemini run looks (audit-setup.md 8b), and
    # those rows stay.
    done = set()
    if os.path.exists(path):
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("errors"):
                    continue
                done.add((row["assistant"], row["question_id"], row["run_no"]))
    return done


PROVIDER_LABELS = {"openai": "OpenAI", "gemini": "Gemini", "perplexity": "Perplexity"}
_PROVIDER_WIDTH = max(len(v) for v in PROVIDER_LABELS.values())
_BAR_WIDTH = 20


def format_progress_line(current, total, provider, question_id, run_no, n_runs, status):
    # `current` is overall position through the plan's own calls — including
    # ones already satisfied by resume, not just this invocation's new
    # attempts — so a resumed run reports e.g. [32/90], never a misleading
    # [1/59]. See the progress_count seeding in main().
    #
    # ASCII bar characters, not block-drawing Unicode (#/░): a Git-Bash
    # console on cp1252 raised UnicodeEncodeError on the block characters
    # during testing, even though PowerShell (UTF-8) printed them fine —
    # plain ASCII is the one choice guaranteed not to crash a paid run
    # partway through on some terminal's codepage.
    pct = (current / total * 100) if total else 0.0
    filled = round(_BAR_WIDTH * current / total) if total else 0
    bar = "#" * filled + "-" * (_BAR_WIDTH - filled)
    width = len(str(total))
    label = PROVIDER_LABELS.get(provider, provider).ljust(_PROVIDER_WIDTH)
    return (
        f"[{bar}] {str(current).zfill(width)}/{total} {pct:5.1f}% | "
        f"{label} | {question_id.upper()} | run {run_no}/{n_runs} | {status}"
    )


def ensure_header(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDS, quoting=csv.QUOTE_ALL).writeheader()


def append_row(path, row):
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, quoting=csv.QUOTE_ALL)
        w.writerow(row)
        f.flush()
        os.fsync(f.fileno())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--questions", required=True)
    ap.add_argument("--out", required=True, help="Write this OUTSIDE the repo — see the module docstring")
    ap.add_argument("--client", required=True, help="Slug for the trade and area, e.g. wirral-dentists. Goes in the client column")
    ap.add_argument("--location", required=True, help="The area's plain-English place name, e.g. Chester. Passed to Perplexity's user_location.city — every question should already name this same place")
    ap.add_argument("--audit-id", default=None)
    ap.add_argument("--runs", type=int, default=DEFAULT_RUNS, help=f"Runs per question per assistant (default {DEFAULT_RUNS})")
    ap.add_argument("--cap", type=int, default=100, help="Hard cap on total queries this invocation")
    ap.add_argument("--smoke", action="store_true", help="1 query per provider on the first question, tagged 'smoke' in notes")
    args = ap.parse_args()

    questions = load_questions(args.questions)
    if not questions:
        sys.exit(f"No questions in {args.questions}")
    audit_id = args.audit_id or questions[0]["audit_id"]
    done = load_done(args.out)
    ensure_header(args.out)

    if args.smoke:
        plan = [(questions[0], 1)]
    else:
        plan = [(q, args.runs) for q in questions]

    total = sum(n for _, n in plan) * len(PROVIDERS)
    if total > args.cap:
        sys.exit(f"Planned {total} queries exceeds cap {args.cap} — stopping before the first call.")

    print(f"Plan: {total} queries across {len(PROVIDERS)} providers. Cap {args.cap}.")
    # Resume-aware progress counter: how many of THIS plan's own
    # (provider, question, run_no) keys are already satisfied in `done` —
    # the same source of truth and the same key shape the skip check below
    # uses — so the printed counter reflects overall campaign position
    # rather than restarting from 1 on a resumed run.
    plan_keys = [
        (provider, q["question_id"], str(run_no))
        for provider in PROVIDERS
        for q, n_runs in plan
        for run_no in range(1, n_runs + 1)
    ]
    progress_count = sum(1 for k in plan_keys if k in done)
    count = 0
    for provider in PROVIDERS:
        caller = CALLERS[provider]
        for q, n_runs in plan:
            for run_no in range(1, n_runs + 1):
                key = (provider, q["question_id"], str(run_no))
                if key in done:
                    print(f"skip (already in {args.out}): {key}")
                    continue
                count += 1
                if count > args.cap:
                    sys.exit(f"Hard cap {args.cap} reached mid-run — stopping. "
                             f"Delete nothing; re-run this command to resume.")
                try:
                    model_version, answer, sources = caller(q["question_text"], args.location)
                    errors = ""
                except Exception as e:  # noqa: BLE001 — crude script, log and keep going
                    model_version, answer, sources = "", "", []
                    errors = repr(e)
                    print(f"  ERROR: {e}", file=sys.stderr)
                progress_count += 1
                print(format_progress_line(
                    progress_count, total, provider, q["question_id"],
                    run_no, n_runs, "ERROR" if errors else "OK",
                ))
                row = {
                    "audit_id": audit_id,
                    "client": args.client,
                    "run_at": datetime.now(timezone.utc).isoformat(),
                    "assistant": provider,
                    "surface": "api",
                    "model_version": model_version,
                    "question_id": q["question_id"],
                    "run_no": run_no,
                    "outcome": "",
                    "competitors": "",
                    "errors": errors,
                    "sources_cited": ";".join(sources),
                    "answer_text": answer,
                    "notes": "smoke — delete this row" if args.smoke else "",
                }
                append_row(args.out, row)
                time.sleep(0.5)

    if args.smoke:
        print("Smoke test done. Check the 5 things in audit-setup.md section 8 "
              "on these 3 rows, then delete them from runs.csv before the real run.")
    else:
        errored = sum(1 for r in csv.DictReader(
            open(args.out, newline="", encoding="utf-8")) if r.get("errors"))
        print("Done.")
        if errored:
            print(f"\n{errored} row(s) carry an error. Re-run this same command "
                  f"to retry just those — they are not counted as done.\n"
                  f"After a successful retry the failed row is still in the file "
                  f"alongside its replacement: sort by the errors column and "
                  f"delete the non-empty ones before reading the answers.")


if __name__ == "__main__":
    main()
