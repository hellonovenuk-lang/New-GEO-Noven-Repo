/* Whether the two legal pages are published, and why they might not be.
 *
 * **Both documents are written and finished.** Neither is a draft, and neither
 * is waiting on a decision about what it should say. What they are waiting on
 * is two facts about the world that only the owner can supply, and each page
 * states the fact it needs — so publishing early would not mean publishing an
 * unfinished page, it would mean publishing a false one.
 *
 * That is the lesson of 2026-08-06, when a `[PLACEHOLDER: address for service
 * of documents]` in the site footer went out to every crawler on nine pages: it
 * published the literal token, the name of an internal file, and a written
 * admission that a legal disclosure was outstanding. A placeholder in a
 * *contract* would be worse again. So these pages are not built at all until
 * they are true, on the same principle as the order page.
 *
 * **On 2026-08-10 the two gates were genuinely open at different times for the
 * first time**, and by the end of the day both were shut again — `/terms/`
 * published when the address for service landed, `/privacy/` a few hours later
 * when client storage was settled. The design always allowed the split — two
 * constants, not one — but the *copy* did not: the terms' "Your information"
 * section linked straight to `/privacy/`, which would have published a contract
 * citing a 404. It now branches on `privacyLive`.
 *
 * **That branch is currently dormant and should be left in place.** It costs
 * nothing while both pages are live and it is the only thing standing between a
 * future gap and a published contract pointing at nothing. **The lesson for
 * anything added here later: a gate that can open on its own needs page copy
 * that can too.**
 *
 * **And a second lesson, from the same day, about these gates specifically: a
 * gate should check what its page claims and nothing more.** `privacyLive` was
 * briefly treated as also requiring a tested backup, which `/privacy/` does not
 * mention anywhere — it claims encryption at rest, and that is the whole of what
 * has to be true for it to publish honestly. See the comment on
 * `clientDataStorage` in `./business`.
 */

import { business } from './business';

/**
 * **`/terms/` needs the address for service.** These are the terms somebody
 * enters a contract on, and a contract has to say who the other party is and
 * where they can be reached. The Consumer Contracts and E-Commerce Regulations
 * both ask for a geographic address, not just an email, once you are selling.
 */
export const termsLive = business.addressForService !== null;

/**
 * **`/privacy/` needs the address as well, and one thing more: somewhere for
 * client records to live.**
 *
 * The notice lists who receives personal data and where they hold it. Until the
 * storage decision in `ops/client-record.md` is made, that list has a hole in
 * exactly the place a reader would look first — the place their own business's
 * details end up. Everything else in the notice is settled.
 *
 * **Both halves of the decision are checked, not just the provider.** The
 * provider was named on 2026-08-09 (Microsoft OneDrive) while the country it
 * holds the data in was left as a `[PLACEHOLDER]`, because that is a checkable
 * fact about an account rather than something to assert. A notice that names a
 * supplier and says `[PLACEHOLDER]` where the country goes is worse than no
 * notice, so the gate reads the string as well as the object.
 */
export const privacyLive =
  termsLive &&
  business.clientDataStorage !== null &&
  !business.clientDataStorage.where.includes('PLACEHOLDER');

/**
 * The footer links to whichever of the two exists. Both go live in the same
 * commit in practice; this is here so that if they ever don't, the footer
 * doesn't link to a page that isn't built.
 */
export const legalNavItems = [
  ...(termsLive ? [{ href: '/terms/', label: 'Terms' }] : []),
  ...(privacyLive ? [{ href: '/privacy/', label: 'Privacy' }] : []),
];
