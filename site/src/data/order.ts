/* The order page, and the hand-off to the Revolut payment link.
 *
 * **This file is a switch, and it is off.** Everything the order route needs is
 * built and merged; none of it reaches the internet until the payment link
 * below is set *and* the terms and privacy notice are published, which in turn
 * waits on the address for service. `orderPageLive` is read by the two route
 * files, by the sitemap filter in `astro.config.mjs`, by the header and footer
 * buttons and by the contact page, so nothing can end up half published.
 *
 * **Why a switch instead of just building it later.** Taking money on the site
 * moves four items from "deferred" to "legally required" — the terms of
 * service, the privacy notice, the ICO registration (done) and the address for
 * service. The code was the fast part. Gating it means the slow parts can't be
 * skipped by accident, and the page can't go out because somebody forgot which
 * of them was still outstanding. ROADMAP.md 1c, "What the pay button changes".
 *
 * **Business facts do not live here — they live in `business.ts`.** The audit's
 * price is read from there, so this file never restates it. What is here is
 * operational: one URL and the rules about it.
 */

import { termsLive, privacyLive } from './legal';

/**
 * **The Revolut Pro payment link for the £250 audit.** Null until the owner
 * creates it and pastes it in.
 *
 * Rules for the value, all of which matter:
 *
 * - It must be a **fixed-amount** link for the audit price in `business.ts`,
 *   not an open "enter any amount" link. The page states a price next to the
 *   button; a link that lets the payer type their own figure makes that a lie
 *   and creates underpaid orders nobody notices.
 * - **No custom fields on the Revolut side.** Field values only surface against
 *   a *successful* payment, so anything typed there is lost the moment somebody
 *   abandons the card screen. Our own form submits first, which is the entire
 *   reason the order page exists rather than a bare link. Decided 2026-07-30 —
 *   see `ops/session-log.md`.
 * - **Check the trading name shown on the link is "Wardith"** before this is
 *   set. It is what the customer reads at the card screen and what appears on
 *   their statement, and a different name there is the single most effective way
 *   to cause a chargeback. `ops/rename-to-wardith.md` F7.
 * - It is a public URL that will be published on a public page. It authorises
 *   nobody to do anything except pay us, and it carries no session or account
 *   token. Never put a Revolut login, API key or account number in this file.
 */
export const paymentLink: string | null = null;

/**
 * True only when every prerequisite is met. When false the two order routes
 * build no HTML at all — they are not unlinked pages or `noindex` pages, they
 * do not exist in `dist` — and every "order the audit" button on the site keeps
 * pointing at the contact page, which sells the same thing by email.
 *
 * **The other three conditions are not booleans anybody has to remember to
 * flip.** `termsLive` and `privacyLive` are true when those pages will actually
 * be built, which in turn depends on the address for service and on the storage
 * decision — see `legal.ts`. So the form cannot ship linking to a document the
 * site hasn't got, and the address requirement is met by the same one value
 * that fills the footer rather than by somebody asserting it separately.
 *
 * Which leaves exactly one thing for a person to set: the payment link above.
 */
export const orderPageLive = paymentLink !== null && termsLive && privacyLive;

/**
 * Where every "order the audit" control on the site points. One import, so the
 * header, the footer and the body CTAs can never disagree about it.
 */
export const orderHref = orderPageLive ? '/order/' : '/contact/';

/**
 * The Netlify form's name. Netlify keys submissions by this string, so changing
 * it starts a new, empty collection in the dashboard and orphans everything
 * already received — treat it as permanent. It appears twice on the page (the
 * `name` attribute and the hidden `form-name` input) and must match in both.
 */
export const formName = 'audit-order';

/**
 * The honeypot field's name, declared to Netlify by the form's
 * `netlify-honeypot` attribute. It is hidden from people and from screen
 * readers; a bot fills it in and the submission is dropped silently.
 *
 * This is the whole of the spam defence on purpose. The alternative Netlify
 * offers is reCAPTCHA, which needs client-side JavaScript from Google on a site
 * that ships none and is built as a demonstration that it does not need any.
 * A honeypot costs nothing and stops the indiscriminate traffic; anything that
 * gets past it arrives in a mailbox a person reads.
 */
export const honeypotName = 'bot-field';
