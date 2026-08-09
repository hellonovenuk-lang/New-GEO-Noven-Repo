#!/usr/bin/env python3
"""
Trade run — asks the three assistants a trade-and-area question set and
logs every answer. Per ops/outreach.md section 4.

**This is a copy of ops/audits/noven-2026-08-02/audit_query.py**, which was
written as a throwaway for the 2 August self-audit and turned out to be
reusable. Three things changed and nothing else: the client name is a flag
rather than the one slug that audit hardcoded, the run count is a flag
rather than that audit's five-vs-ten experiment, and the defaults suit a
trade run. **The original is frozen as part of that audit's record — change this
file, never that one.**

It is still not "the runner" that ops/audit-method.md section 7 defers.
A trade run is prospecting, not a client audit: it asks about a trade and an
area, nobody has paid for it, and it produces the mention table in
ops/outreach.md section 4 rather than a report.

Stdlib only, no pip install needed. Requires Python 3.9+.

Env vars (source ~/.noven/env first, then set the three model vars from
what you recorded in audit-setup.md section 2 — do not guess a model name):
  OPENAI_API_KEY       OPENAI_MODEL
  GEMINI_API_KEY        GEMINI_MODEL
  PERPLEXITY_API_KEY    PERPLEXITY_MODEL

Usage, the checks to run first and what the output is good for are all in
README.md beside this file. Short version, and smoke first, always:

  python3 trade_run.py --questions questions-wirral-dentists.csv \
      --client wirral-dentists --out ~/wardith-runs/wirral-dentists.csv --smoke

  python3 trade_run.py --questions questions-wirral-dentists.csv \
      --client wirral-dentists --out ~/wardith-runs/wirral-dentists.csv --cap 90

**--out must point outside this repository.** Answer text names real
businesses and sometimes real people; ops/audit-method.md section 5 keeps
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
            f"Missing {name} — source ~/.noven/env first, and make sure the "
            f"model env vars are set from what you recorded in "
            f"audit-setup.md section 2."
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


def call_openai(question):
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


def call_gemini(question):
    key = env("GEMINI_API_KEY")
    model = env("GEMINI_MODEL")
    # NB: no documented UK-locale parameter for the google_search grounding
    # tool as of when this was written — this is exactly what smoke-test
    # check 3 ("does the answer look UK-shaped") exists to catch. Verify
    # against the current Gemini API docs before the real run.
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


def call_perplexity(question):
    # Confirmed against the live console 2026-08-02: Perplexity's "Sonar Chat
    # Completions" API was retired in favour of an "Agent API" that mirrors
    # OpenAI's Responses shape (same model/input/tools fields, same
    # response.output[].content[].output_text envelope) — but citations do
    # NOT show up in per-message annotations the way OpenAI does it. They
    # arrive as a separate output item, type "search_results", with its own
    # "results" list of {url, title, ...}. Confirmed via a live query with
    # tools=[{"type": "web_search"}] returning a populated search_results
    # item and empty message annotations.
    key = env("PERPLEXITY_API_KEY")
    model = env("PERPLEXITY_MODEL")
    body = {
        "model": model,
        "input": question,
        "tools": [{
            "type": "web_search",
            "user_location": {"type": "approximate", "country": "GB"},
        }],
    }
    data = post_json(
        "https://api.perplexity.ai/v1/responses",
        {"Authorization": f"Bearer {key}"},
        body,
    )
    # A streamed call wraps the real object as {"type": "response.completed",
    # "response": {...}}; a plain call (what this script sends, no "stream"
    # key) is expected to return the inner object directly. Handle both.
    resp = data.get("response", data)
    model_version = resp.get("model", model)
    text_parts, sources = [], []
    for item in resp.get("output", []):
        if item.get("type") == "message":
            for c in item.get("content", []):
                if c.get("type") == "output_text":
                    text_parts.append(c.get("text", ""))
        elif item.get("type") == "search_results":
            for r in item.get("results", []):
                if r.get("url"):
                    sources.append(r["url"])
    return model_version, "".join(text_parts), sources


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
                print(f"[{count}/{total}] {provider} {q['question_id']} run {run_no}")
                try:
                    model_version, answer, sources = caller(q["question_text"])
                    errors = ""
                except Exception as e:  # noqa: BLE001 — crude script, log and keep going
                    model_version, answer, sources = "", "", []
                    errors = repr(e)
                    print(f"  ERROR: {e}", file=sys.stderr)
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
