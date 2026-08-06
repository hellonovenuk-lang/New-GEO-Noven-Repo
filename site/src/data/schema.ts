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
    // Finding 3 of the 2 August self-audit: nothing told a machine where this
    // business works. `areaServed: GB` says which country will be served, not
    // where the business is, and the two are different questions — an
    // assistant asked for someone on the Wirral has nothing to match against.
    // Locality and region only; see the note in `business.ts` for why a street
    // line never goes here.
    address: {
      '@type': 'PostalAddress',
      addressLocality: business.locality,
      addressRegion: business.region,
      addressCountry: business.areaServed,
    },
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
