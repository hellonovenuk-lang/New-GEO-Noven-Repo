/* Canonical business facts.
 *
 * This file is the single source of truth. The JSON-LD in the page head and
 * the visible "record" panels both read from here, so what a person sees and
 * what an assistant reads can never drift apart. That claim is made out loud
 * on the homepage, so it has to stay true — change a fact here, not in a page.
 */

export const business = {
  name: 'Noven',
  legalNote: 'Noven is a trading name of Kieran Smith, a sole trader.',
  founder: 'Kieran Smith',
  email: 'hello.noven.uk@gmail.com',
  basedIn: 'the Wirral, UK',
  basedInShort: 'Wirral, UK',
  areaServed: 'GB',
  areaServedLabel: 'United Kingdom',
  vatRegistered: false,
  description:
    'Noven helps service businesses get found and recommended when their customers ask AI assistants — ChatGPT, Google, Copilot and Perplexity — who to use.',
  serviceName: 'AI assistant visibility for service businesses',
  serviceType: 'Business visibility in AI assistant recommendations',

  /**
   * The founder's previous employer, named. Used twice: in the About page bio
   * and as the founder's `alumniOf` in the structured data. Naming it is the
   * point — it is the most checkable fact this business has, and a site that
   * sells consistent, verifiable information cannot be vague about its own.
   */
  founderFormerEmployer: 'Maersk',

  /**
   * The founder's LinkedIn profile. Set this and two things happen at once:
   * the About page links to it, and it joins the Person in the structured
   * data as `sameAs` — a machine-readable claim that this business and that
   * profile are the same person. That is exactly what we sell, so it's worth
   * having on ourselves. Null until the URL is supplied.
   *
   * Supplied by the owner. Stored stripped: the shared link carried `utm_*`
   * tracking parameters, which say how the link was shared and belong to
   * nobody reading the page. Nothing beyond the `/in/` handle goes in here,
   * and nothing resembling a login or session token ever does — this value is
   * published twice on a public page and again in a public repo.
   */
  founderLinkedIn: 'https://www.linkedin.com/in/kieran-smith-50b953143' as string | null,

  /**
   * Noven's own LinkedIn page, once it exists. Separate from the founder's
   * profile: this one joins the *Organization* in the structured data as
   * `sameAs`, which is the business claiming a second page as its own. Null
   * until the page is created — an empty or wrong `sameAs` is precisely the
   * unreliable business information we're paid to remove from other people's
   * sites. Roadmap 1a covers creating it.
   */
  businessLinkedIn: null as string | null,

  /**
   * Path to the founder's photograph in site/public. Setting it does two
   * things: the About page renders the portrait, and the file joins the
   * founder's Person in the structured data as `image`. The file is 880x1100,
   * so anything rendering it should keep the 4:5 ratio.
   */
  founderPhoto: '/founder-portrait.webp' as string | null,
} as const;

/** The assistants named across the site, in one place. */
export const assistants = ['ChatGPT', 'Google', 'Copilot', 'Perplexity'] as const;

type Plan = {
  id: string;
  name: string;
  /** Short trailing label, e.g. "one-off" or "per month". */
  cadence: string;
  price: number;
  /** Sentence-case summary used in the record panels. */
  summary: string;
  /** Longer description used for the Offer structured data. */
  schemaDescription: string;
};

export const oneOffs: Plan[] = [
  {
    id: 'audit',
    name: 'Audit',
    cadence: 'one-off',
    price: 30,
    summary: 'A written report on where you show up today.',
    schemaDescription:
      'One-off written report on how AI assistants currently answer questions about your business, what they believe about you, and what is blocking you from being recommended.',
  },
  {
    id: 'foundation',
    name: 'Foundation',
    cadence: 'one-off',
    price: 350,
    summary: 'The setup that makes your business readable to these systems.',
    schemaDescription:
      'One-off setup on your existing website: crawler access, structured data, consistent business facts, and pages that answer the questions your customers ask AI assistants.',
  },
];

export const monthlies: Plan[] = [
  {
    id: 'maintain',
    name: 'Maintain',
    cadence: 'per month',
    price: 75,
    summary: 'Stay found.',
    schemaDescription:
      'Monthly plan to hold your position: ten questions your customers ask, put to the AI assistants five times each every month, with a written record of where you appeared and which questions you are still missing from. Business facts kept current and corrected when they drift. £75 per month.',
  },
  {
    id: 'grow',
    name: 'Grow',
    cadence: 'per month',
    price: 125,
    summary: 'Get found more.',
    schemaDescription:
      'Monthly plan to close the gaps: everything in Maintain across twenty-five questions, plus one new page each month answering a question you are currently missing from. £125 per month.',
  },
  {
    id: 'lead',
    name: 'Lead',
    cadence: 'per month',
    price: 250,
    summary: 'Front of mind.',
    schemaDescription:
      'Monthly plan for businesses that want to be the first name an assistant gives: fifty questions checked fortnightly, two new answer pages each month, and a quarterly written review of the competitors being named ahead of you and why. £250 per month.',
  },
];

export const plans: Plan[] = [...oneOffs, ...monthlies];

/** Look a plan up by id, so pages never restate a price as a literal. */
export function plan(id: string): Plan {
  const found = plans.find((p) => p.id === id);
  if (!found) throw new Error(`Unknown plan: ${id}`);
  return found;
}

/** "£30", "£1,250" — prices on this site are always whole pounds. */
export function money(amount: number): string {
  return `£${amount.toLocaleString('en-GB')}`;
}

/** Offer objects for Service structured data, built from the same numbers. */
export function offerSchema() {
  return plans.map((p) => ({
    '@type': 'Offer',
    name: p.cadence === 'per month' ? `${p.name} (monthly)` : p.name,
    price: String(p.price),
    priceCurrency: 'GBP',
    description: p.schemaDescription,
  }));
}
