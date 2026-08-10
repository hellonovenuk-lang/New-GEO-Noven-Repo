# Records, data and keys

*What we keep, where it lives, and what the law requires. Load-bearing —
`/privacy/` is published and makes claims this file has to keep true.*

## Where client and prospect records live

**On the owner's own machine, encrypted, in the United Kingdom.** Decided
2026-08-10 after a consumer Microsoft account turned out to be unusable for
this: no data-location commitment to publish, no Article 28 processor contract,
and Microsoft's own terms bar commercial use.

Holding it ourselves dissolves all three. No processor means no contract to
need. The country is the United Kingdom, which is true and checkable. And
`/privacy/` gets the stronger sentence: held by us, in the UK, not passed to a
cloud storage provider.

**Two conditions, neither optional:**

1. **Full-disk encryption on and verified**, recovery key stored somewhere that
   is not the encrypted disk. `/privacy/` already claims records are encrypted
   at rest. `[PLACEHOLDER: confirm BitLocker or Device Encryption is on.]`
2. **An encrypted external backup drive, kept off-site, restored at least
   once.** ~£30–60. Article 32 requires being able to restore availability.
   Gates taking on a client, not sending an email.

**Turn OneDrive folder backup off first.** Windows syncs Desktop and Documents
to the consumer account by default, which would undo the whole decision
silently.

**Nothing about a client or prospect ever goes in this repository.** It is
written as though public.

## What we keep

**Per prospect** — business, contact, source; date contacted and what was said;
what came back; do-not-contact.

**Per client** — the above plus the audit folder: filled site checklist,
`runs.csv`, `questions.csv`, the report, the timings. One folder per client per
audit.

## Retention

| | |
|---|---|
| Client records | Life of the relationship plus twelve months, then delete |
| Enquiries that go nowhere | Twelve months |
| **Do-not-contact requests** | **Permanently.** Deleting one defeats its purpose |
| Invoices and payment records | As long as tax law requires — at least five years after the 31 January deadline for that tax year. These outlive everything above, and `/privacy/` says so |

Put the deletion date in the record, so deletion is something you do by looking
rather than by remembering.

## API keys

**Never in this repo.** It is public and a leaked key is somebody else's bill on
your card.

1. Each key goes in Bitwarden as it is created — the copy of last resort.
2. Then into `~/.noven/env`, outside any git repository:

```sh
mkdir -p ~/.noven && chmod 700 ~/.noven
cat > ~/.noven/env <<'EOF'
export OPENAI_API_KEY="..."
export GEMINI_API_KEY="..."
export PERPLEXITY_API_KEY="..."
EOF
chmod 600 ~/.noven/env
```

3. `source ~/.noven/env` only when running. Deliberately not in `.bashrc` — a
   key that is only in the environment when you meant it to be cannot leak into
   an unrelated process.

**If a key is ever committed: revoke it in the provider console first, rewrite
history second.** Revoking is the fix; rewriting is the tidy-up.

## Spend caps

Set before the first call of any run. The failure this prevents is a loop bug at
a penny a query running all night.

| Provider | Cap |
|---|---|
| OpenAI | £10 hard limit, £5 alert |
| Google | £10 budget, alert at 50% (free tier is its own cap) |
| Perplexity | £10 prepaid credit, **auto top-up off** |

The script carries its own `--cap` as a second, independent limit. Provider caps
protect the card; the script cap protects the afternoon.

`[PLACEHOLDER: none of the three provider caps has been confirmed as set.]`
