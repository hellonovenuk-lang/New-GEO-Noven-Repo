# zoho-draft-push

Pushes `/outreach`'s drafted emails into Zoho Mail as real drafts, ready to
open, edit, and send by hand. Never sends, replies, or deletes anything —
see `zoho_draft_push.py`'s own docstring for the exact three API calls this
tool is capable of making, and no others, and for exactly what stops it
sending (summarised under "What this tool will and won't do" below).

## One-time setup

1. **Register a Self Client** at
   [api-console.zoho.com](https://api-console.zoho.com/) (log in with the
   same Zoho account as your mailbox). Choose **Self Client**. Note which
   regional domain your console URL uses (`accounts.zoho.com`,
   `accounts.zoho.eu`, etc.) — that's your `--region` below.
2. **Generate a grant token** for that Self Client with scopes:
   - `ZohoMail.messages.CREATE`
   - `ZohoMail.accounts.READ`

   Set the validity to the shortest option offered (these tokens expire in
   minutes and are only used once, immediately, by the command below).
3. **Run the setup script**, using the client ID, client secret, and grant
   token Zoho just showed you (all copied from Zoho's own console — never
   typed anywhere else, never shared with Claude):

   ```
   python3 tools/zoho-draft-push/setup_zoho_oauth.py \
       --client-id "1000.XXXXXXXX" \
       --client-secret "your-client-secret" \
       --grant-token "your-grant-token" \
       --region eu
   ```

   This writes `~/.wardith/zoho-credentials.json` (outside this repo,
   never committed) containing a long-lived refresh token, your account id,
   and your from-address. The directory is created `0700` and the file
   `0600`, following `playbook/records-and-data.md`'s rule for secrets. The
   grant token itself is single-use and expires within minutes either way,
   so there's nothing further to revoke if this step is repeated.
4. Store the complete generated JSON as `ZOHO_CREDENTIALS_JSON` in the Wardith
   Bitwarden Secrets Manager project. On Windows, delete the plaintext file
   after verifying `scripts/wardith-secrets.ps1 status`; the wrapper creates
   a restricted temporary copy only while `/outreach` is running.

## How to revoke access

**Delete the Self Client at [api-console.zoho.com](https://api-console.zoho.com/).**
That is the whole revocation, and it is the only thing that actually works:
the refresh token in `~/.wardith/zoho-credentials.json` is long-lived and
does not expire on its own, and it is what this tool exchanges for a fresh
access token on every run.

- Deleting `~/.wardith/zoho-credentials.json` stops *this machine* using the
  token, which is worth doing too — but the token itself stays valid at
  Zoho's end until the Self Client is gone. Do both, in that order: console
  first, file second.
- The **grant token** from setup step 2 needs no revocation. It is single-use
  and expires within minutes, so by the time setup has finished it is already
  dead.
- Revoking does not touch anything in the mailbox. Drafts already pushed stay
  where they are, for the owner to send or delete by hand as usual.

## What this tool will and won't do

- **Will:** create a new Zoho draft for each business `/outreach` drafted
  an email for, or update the existing draft if one was already pushed for
  that business on a previous run of the same campaign.
- **Known-unverified — watch for this on the first re-run of a campaign.**
  Creating a draft is documented by Zoho; *updating* one is not clearly
  documented. The update path issues
  `PUT .../api/accounts/{accountId}/messages/{messageId}`, which is a
  reasonable reading of the API but has never been exercised against a real
  Zoho account. If a re-run reports `FAILED: HTTP 404`/`405` for every
  business already pushed once, this is why — delete those drafts in Zoho by
  hand so the create path runs, and tell the owner the update path needs
  correcting. A 404 on the update path is handled specially: the stored
  draft id is cleared, so the next run creates a fresh draft rather than
  retrying a message that no longer exists.
- **Won't:** send, reply to, or delete anything, in Zoho or anywhere else.
  Reply, delete and folder-move are separate Zoho API surfaces this code
  never calls — not surfaces the granted scope is incapable of reaching.
  Delete and folder-move do need scopes this token lacks, but Reply is
  documented under this same `ZohoMail.messages.CREATE` scope, same as
  Send below — the scope alone rules out neither.
- **Won't send — and here's the actual reason, which is not the OAuth
  scope.** Zoho's "Send an Email" and "Save Draft or Template" APIs are the
  *same* endpoint (`POST .../messages`), the same method, and the same
  scope (`ZohoMail.messages.CREATE` is documented as valid for both). The
  only difference is the `mode` field in the request body. What stops a send
  is that `zoho_draft_push.py`'s `build_message_payload()` returns a closed
  dict of six literal keys — `fromAddress`, `toAddress`, `subject`,
  `content`, `mailFormat`, `mode` — with `mode` hardcoded to `"draft"` and
  never derived from entry data. No business's outreach content is ever
  merged into that dict, so nothing in a campaign can reach or override
  `mode`. `test_zoho_draft_push.py`'s `DraftModeInvariantTests` asserts
  exactly that on every payload the tool builds, so the guarantee is checked
  by the test suite rather than only asserted in prose.
- **Won't:** touch the email signature. That's Zoho's own account-level
  "signature for new mail" setting (see `assets/brand/email-signature.html`
  for how it's installed) — this tool doesn't duplicate it into the draft
  body. **Confirmed on first real use (2026-08-26): Zoho does NOT apply the
  signature automatically to an API-created draft** the way it does for one
  composed by hand in the web UI. The owner adds it manually per draft
  before sending. This tool still won't duplicate the signature into the
  draft body itself — that would just create the second copy of it
  `assets/brand/email-signature.html` already warns against — so this stays
  a manual step, by design, not a gap to code around.

## Manual usage

Normally run automatically as part of `/outreach`'s Stage 7.5. To run by
hand against an existing `outreach-prep-*.json` file:

```
python3 tools/zoho-draft-push/zoho_draft_push.py \
    --input ~/wardith-runs/<slug>/outreach/outreach-prep-<slug>-<date>.json \
    --in-place
```

Add `--dry-run` to see what would be pushed (business, recipient, subject)
without calling Zoho at all — works even before setup has been run.

## Running the tests

```
cd tools/zoho-draft-push
python3 test_zoho_draft_push.py -v
python3 test_setup_zoho_oauth.py -v
```

No real network calls, no real Zoho credentials required — every
`urllib.request.urlopen` call is mocked.
