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
      'Monthly plan to stay found: keeps your information current, monitors how AI assistants answer questions about your business, and fixes drift. £75 per month.',
  },
  {
    id: 'grow',
    name: 'Grow',
    cadence: 'per month',
    price: 125,
    summary: 'Get found more.',
    schemaDescription:
      'Monthly plan to get found more: everything in Maintain, plus new answer-focused content each month so you appear for more of the questions your customers ask. £125 per month.',
  },
  {
    id: 'lead',
    name: 'Lead',
    cadence: 'per month',
    price: 250,
    summary: 'Front of mind.',
    schemaDescription:
      'Monthly plan for businesses that want to be the default recommendation in their field: everything in Grow, at a faster pace and broader coverage, with a quarterly written review. £250 per month.',
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
