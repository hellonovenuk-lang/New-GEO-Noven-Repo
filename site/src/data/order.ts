/* The order page, and the hand-off to the Revolut payment link.
 *
 * **This file is a switch, and it is off.** Everything the order route needs is
 * built and merged; none of it reaches the internet until all four conditions
 * below hold. Two of them check themselves — `/terms/` and `/privacy/` are true
 * when those pages exist — so what the owner actually sets by hand is the
 * payment link and one line about the footer. `orderPageLive` is read by the
 * two route files, by the sitemap filter in `astro.config.mjs`, by the header
 * and footer buttons and by the contact page, so nothing can end up half
 * published.
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
 * operational: one URL, two pages that either exist or don't, and one statement
 * about the footer.
 */

/* Every page file in the project, listed at build time. `import.meta.glob` is
 * resolved by the bundler from the source tree rather than by reading the disk
 * at run time, so this is a list of what will actually be built. Lazy: nothing
 * here is imported or executed, only counted. */
const pageFiles = Object.keys(import.meta.glob('/src/pages/**/*.{astro,md}'));

/** Whether a page is actually going to be built at `/<route>/`. Covers both
 *  shapes a page takes in this project, so moving `terms.astro` to
 *  `terms/index.astro` doesn't silently turn the gate off. */
function pagePublished(route: string): boolean {
  return pageFiles.some(
    (file) => file === `/src/pages/${route}.astro` || file.startsWith(`/src/pages/${route}/index.`),
  );
}

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
 * **The terms of service, at `/terms/`.** Not a boolean somebody has to
 * remember to flip: it is true when the page exists and false when it doesn't,
 * so it cannot claim a document the site hasn't got. The order form links to it
 * and makes the reader tick it, and a payment form linking to a 404 is the
 * worst possible place for a broken link.
 *
 * What the page has to carry, over and above the ordinary terms, is the refund
 * position: dead or typo'd URLs, a social profile where a website was needed, a
 * business outside our area, duplicate or accidental payments, a change of mind
 * before work starts, and a business we look at and genuinely cannot help.
 * ROADMAP.md 1c has the reasoning — a chargeback costs more than a refund we
 * control, and a plain refund line sells.
 */
export const termsPublished = pagePublished('terms');

/**
 * **The privacy notice, at `/privacy/`.** Derived the same way, for the same
 * reason.
 *
 * One thing about this build changes what the notice has to say: the order form
 * is a **Netlify** form. Submissions are stored on Netlify's infrastructure and
 * shown in their dashboard before they ever reach the inbox, which makes
 * Netlify a processor of customer data and a disclosable fact about where that
 * data goes. Whoever writes the notice needs that sentence in it.
 */
export const privacyPublished = pagePublished('privacy');

/**
 * **The address for service of documents is in the site footer.** This one is
 * asserted by hand, because unlike the two above it is not a file that either
 * exists or doesn't — it is a fact about the rendered footer, and it lands with
 * whatever fills the placeholder described in the long comment at the bottom of
 * `Base.astro`.
 *
 * It gates the pay button because taking payment on the site is visibly
 * trading, and trading under a name that is not the founder's surname carries a
 * duty to show a name and a UK address where documents can be served. Set this
 * to `true` in the same commit that fills the footer, not before.
 */
export const addressPublished = false;

/**
 * True only when every prerequisite is met. When false the two order routes
 * build no HTML at all — they are not unlinked pages or `noindex` pages, they
 * do not exist in `dist` — and every "order the audit" button on the site keeps
 * pointing at the contact page, which sells the same thing by email.
 */
export const orderPageLive =
  paymentLink !== null && termsPublished && privacyPublished && addressPublished;

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
