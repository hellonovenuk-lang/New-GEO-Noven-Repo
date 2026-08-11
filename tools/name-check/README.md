# Name-collision check

**Does a candidate business name already belong to somebody else, in the eyes of
the assistants?**

This is the test the 2026-08-02 self-audit ran by accident. It found that "Noven"
resolves to at least four other businesses — a Miami pharmaceutical company, a
North West builder, an AI product at `noven.studio` and a fourth at `noven.io` —
which became finding 1 of that audit and the reason the Foundation work was not
recommended. See `archive/audits/noven-2026-08-02/`.

Running it deliberately, on a shortlist, costs a couple of pounds and about ten
minutes. Discovering the same thing after the domain, the logo, the email and the
company record exist costs a rebrand.

## Use

Needs the three API keys loaded the same way the audit loaded them
(`. "$HOME\.noven\env.ps1"` on Windows), and `archive/audits/noven-2026-08-02/`
present — the provider callers are imported from there rather than duplicated,
so the UK locale settings are identical to the baseline's.

```
cd tools/name-check
notepad names.txt          # one candidate per line; # comments out a rejected one
python name_check.py       # writes names-runs.csv
```

Two questions per name, asked of all three assistants twice each — 12 answers per
candidate, 24 queries for two names, 36 for three. It refuses to fire a single
query if the plan exceeds `--cap` (default 60), and it resumes rather than
repeating if it's interrupted.

## Reading the result

Open `names-runs.csv` and read `answer_text`.

| What comes back | What it means |
|---|---|
| "I don't have information on that" | **Good.** The name is clear |
| A confident answer about a different business | **Collision — reject it.** This is the Noven failure |
| Sources cited from a real company's site | **Collision — reject it** |

The counter-intuitive part is that **no answer is the result you want.** An
assistant that already knows the name is telling you the name is taken.

## What it does not tell you

Not a trade mark search, not a Companies House search, and not a domain
availability check. It answers one narrow question — *will an assistant confuse
this name with something else* — which is the one the audit proved matters and
the one nobody thinks to ask.
