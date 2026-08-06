/* Structured data builders.
 *
 * These live apart from the layout because two places need the same object:
 * the <script type="application/ld+json"> in the head, and the code block a
 * page shows the reader. Building both from one function is what lets the
 * site say "this is the code in this page" without it being a figure of
 * speech.
 */

import { business } from './business';

export function organizationSchema(site: URL | undefined) {
  const at = (path: string) => (site ? new URL(path, site).href : path);

  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    '@id': at('/#organization'),
    name: business.name,
    url: site?.href,
    logo: at('/logo.svg'),
    email: business.email,
    description: business.description,
    // Same rule as the founder's: only stated once the page exists.
    ...(business.businessLinkedIn ? { sameAs: [business.businessLinkedIn] } : {}),
    founder: {
      '@type': 'Person',
      name: business.founder,
      // A statement about the founder, not a claim of any relationship between
      // the two businesses: `alumniOf` nested under `founder` says one person
      // used to work somewhere, which is all it says.
      alumniOf: {
        '@type': 'Organization',
        name: business.founderFormerEmployer,
      },
      // Only stated once true. An empty sameAs or a photo that doesn't exist
      // would be exactly the kind of unreliable business information we're
      // paid to remove from other people's sites.
      ...(business.founderPhoto ? { image: at(business.founderPhoto) } : {}),
      ...(business.founderLinkedIn ? { sameAs: [business.founderLinkedIn] } : {}),
    },
    /* **There is deliberately no `address` here, and it is not an oversight.**
     * Added 2026-08-06 to close finding 3 of the self-audit — a `PostalAddress`
     * of locality "Wirral", region "Merseyside" — and taken straight back out
     * the same day, because the footer of every page carries a visible
     * `[PLACEHOLDER: address for service of documents]`. A page that tells a
     * reader it has no address while telling a machine it has one is the exact
     * drift this site claims cannot happen, on the one fact still outstanding.
     *
     * `PostalAddress` is also the wrong instrument for the true statement.
     * "Kieran works from the Wirral" is true today; "post reaches this business
     * at Wirral, Merseyside" is not, because there is no street line and no
     * address for service yet. The type answers the question the footer says is
     * unanswered.
     *
     * **The right fix is the address for service itself**, which is a real
     * postal address, is not the founder's home, and has to be published by law
     * anyway. When it lands, it fills the footer placeholder and this block at
     * the same time, from one fact — and if it turns out not to be in
     * Merseyside, nothing has to be retracted. See ROADMAP 1c and
     * `ops/session-log.md`, 2026-08-06. */
    areaServed: business.areaServed,
    contactPoint: {
      '@type': 'ContactPoint',
      contactType: 'sales and enquiries',
      email: business.email,
      areaServed: business.areaServed,
      availableLanguage: 'English',
    },
    knowsAbout: [
      'AI assistant visibility for businesses',
      'How AI assistants recommend businesses',
      'Structured business information',
    ],
  };
}
