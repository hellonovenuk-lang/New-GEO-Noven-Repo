# Zoho Mail — finishing `hello@novenstudio.co.uk`

**Internal document.** Written 2026-07-29. Steps to follow inside Zoho's admin
console and the DNS panel, which only the owner can sign into.

This closes the last open item in roadmap 1b — *"Consider a
`hello@novenstudio.co.uk` address to replace the Gmail one"*.

**Where this got to.** The domain is added in Zoho, the Mail Lite plan is
bought, and domain ownership is now **verified** — Zoho has confirmed it. The
account is on the **EU data centre** (`zoho.eu`), which is why every hostname
below ends `.eu` rather than `.com`. If a screen in Zoho shows you a value that
differs from one written here, trust the screen — it knows which data centre
your account is on.

**Do it in this order.** Records first, mailbox second, site last. Mail can
only arrive once the MX records point at Zoho, and the site should not
advertise an address until mail actually reaches it.

---

## 1. Create the mailbox

Zoho Mail Admin Console → **Users** → **Add User**.

- Mailbox address: `hello` @ `novenstudio.co.uk`
- Name: Kieran Smith

One Mail Lite licence covers one user, and `hello@` should be the one that
holds it — it is the address on the site and the one people reply to. If you
later want `kieran@novenstudio.co.uk` as well, add it under that user as an
**alias** (Users → the user → Mail Aliases), not as a second user. Aliases are
free; users are £1/month each.

## 2. Add the DNS records

All of these go wherever you added the verification TXT record. Values shown
without a trailing dot; if your DNS panel requires one, add it.

**MX — delete any existing MX records for the domain first.** Mail follows the
lowest priority number that answers, so a leftover record from a previous setup
silently steals mail.

| Host | Type | Priority | Value |
|---|---|---|---|
| `@` | MX | 10 | `mx.zoho.eu` |
| `@` | MX | 20 | `mx2.zoho.eu` |
| `@` | MX | 50 | `mx3.zoho.eu` |

**SPF — one record only.** SPF is the one record type where having two is worse
than having none: receiving servers treat a domain with two SPF records as a
permanent error and stop checking. If a `v=spf1` record already exists on the
apex, edit it rather than adding a second.

| Host | Type | Value |
|---|---|---|
| `@` | TXT | `v=spf1 include:zoho.eu ~all` |

**DKIM — Zoho generates this one, so it can't be written here in advance.**
Admin Console → **Domains** → `novenstudio.co.uk` → **Email Configuration** →
**DKIM** → **Add** → selector `zmail` → Zoho shows a long `p=...` value. Add it
as:

| Host | Type | Value |
|---|---|---|
| `zmail._domainkey` | TXT | the value Zoho shows |

Then click **Verify** back in Zoho. If the DNS panel rejects the value for
length, it needs splitting into two quoted strings — most panels do this
themselves, and Netlify's does.

**DMARC — not required, worth having.** It tells receiving servers what to do
when a message fails the two checks above, and it is how you find out if
anyone is sending as your domain. Start at `p=none`, which asks for reports
and changes nothing about delivery.

| Host | Type | Value |
|---|---|---|
| `_dmarc` | TXT | `v=DMARC1; p=none; rua=mailto:hello@novenstudio.co.uk` |

## 3. Confirm it works before touching anything else

DNS changes are usually live in minutes but can take a few hours.

1. In Zoho, **Domains → Email Configuration** should show MX verified.
2. Send a message from the Gmail account **to** `hello@novenstudio.co.uk`.
   It should land in Zoho's webmail (`mail.zoho.eu`).
3. Reply **from** `hello@` back to the Gmail account. In Gmail, open the reply,
   choose **Show original**, and check it reads `SPF: PASS`, `DKIM: PASS` and
   `DMARC: PASS`. That is the proof the records are right — a message that
   arrives but fails these will start landing in spam once volume picks up.

Don't skip step 3. A new domain with broken authentication gets quietly
filtered, and the failure looks exactly like nobody replying.

## 4. Keep the Gmail address alive

`hello.noven.uk@gmail.com` is on the live site right now and will be in
caches, crawler indexes and assistant answers for months. Don't close it.

- In Gmail: **Settings → Forwarding** → forward to `hello@novenstudio.co.uk`,
  and leave it forwarding for at least a year.
- Optional, and worth it: in Zoho, add the Gmail address under **Settings →
  Mail Accounts** so old threads can be answered from one inbox.

## 5. Then update the site

One line does it — everything else reads from this value, including the
contact page and the structured data on every page:

- `site/src/data/business.ts` → `email: 'hello@novenstudio.co.uk'`

Also worth updating at the same time:

- Zoho Books — the "from" address on invoices.
- The LinkedIn company page's contact address, if it names the Gmail one.
- `ops/linkedin.md`, which quotes the Gmail address as copy to paste.

Then tick the item in roadmap 1b.
