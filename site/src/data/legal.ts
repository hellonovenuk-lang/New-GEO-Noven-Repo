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
 */
export const privacyLive = termsLive && business.clientDataStorage !== null;

/**
 * The footer links to whichever of the two exists. Both go live in the same
 * commit in practice; this is here so that if they ever don't, the footer
 * doesn't link to a page that isn't built.
 */
export const legalNavItems = [
  ...(termsLive ? [{ href: '/terms/', label: 'Terms' }] : []),
  ...(privacyLive ? [{ href: '/privacy/', label: 'Privacy' }] : []),
];
