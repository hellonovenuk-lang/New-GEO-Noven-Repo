/* Canonical business facts.
 *
 * This file is the single source of truth. The JSON-LD in the page head and
 * the visible "record" panels both read from here, so what a person sees and
 * what an assistant reads can never drift apart. That claim is made out loud
 * on the homepage, so it has to stay true — change a fact here, not in a page.
 */

/** A UK postal address, in the parts `schema.org/PostalAddress` asks for, so
 *  the visible address and the machine-readable one are built from one value
 *  rather than typed twice. */
export type PostalAddress = {
  /** Building and street, e.g. "Unit 4, 12 Example Street". */
  line1: string;
  /** Second street line, where the address genuinely has one. */
  line2?: string;
  /** Town or city. */
  locality: string;
  /** County, where the address carries one. */
  region?: string;
  postcode: string;
  /** ISO country code. Always 'GB' — an address for service has to be UK. */
  country: 'GB';
};

export const business = {
  name: 'Wardith',
  legalNote: 'Wardith is a trading name of Kieran Smith, a sole trader.',
  founder: 'Kieran Smith',
  /**
   * **Flipped to the live domain 2026-08-06, once mail actually arrived.**
   *
   * This held `hello@novenstudio.co.uk` for two days after the site published
   * as Wardith, deliberately: the value goes into the structured data and the
   * contact page on *every* page, and it is the only inbound channel on a
   * business with no phone and no contact form. A working address on the dead
   * domain was a smaller fault than a bouncing one on the live domain, because
   * an enquiry lost to a bounce is lost silently — nobody tells you.
   *
   * **The condition for flipping it was "the alias exists and a test message
   * has arrived", and both were met before this changed.** The owner confirmed
   * mail to `hello@wardith.co.uk` lands in the Zoho inbox, and the zone was
   * read independently: MX to `mx.zoho.eu`, exactly one `v=spf1` record, a
   * `zmail._domainkey` DKIM key, and DMARC `p=none` whose `rua` now points at a
   * mailbox that exists.
   *
   * **`hello@novenstudio.co.uk` must keep receiving for at least twelve
   * months** — it is in the ICO record, on both LinkedIn pages and in whatever
   * is already cached. It is an alias on the same licence, not a second user.
   * See `ops/rename-to-wardith.md` E3.
   *
   * **Still owed, and it is not visible from the site:** nobody has confirmed
   * mail sent *from* this address passes SPF, DKIM and DMARC at the receiving
   * end. DNS being present is not the same as authentication passing, and a new
   * domain that fails it gets quietly filtered — a failure that looks exactly
   * like nobody replying. `ops/rename-to-wardith.md` D0.4 step 5 is the test.
   */
  email: 'hello@wardith.co.uk',
  basedIn: 'the Wirral, UK',
  basedInShort: 'Wirral, UK',
  /* Both of the above are prose, read by people, and say only what is true
   * today: the founder works from the Wirral. **Neither is a postal address and
   * neither should be turned into one.** The postal address is the separate
   * value below, and it may not be in Merseyside. */

  /**
   * **The address for service of documents. Live from 2026-08-10.**
   *
   * Trading under a name that is not the founder's surname carries a duty to
   * show a name and a UK address where documents can be served, and selling
   * online adds the same requirement again. UK Postbox's Business Street
   * Address, Poole — ordered 7 August, confirmed by the owner on the 10th.
   * `ops/third-party-services.md` B1b holds the account facts and the terms
   * worth knowing; B1c holds what was done to get here.
   *
   * **Never the founder's home address.** The footer can be edited; indexes,
   * archives and assistants' caches cannot. That is also why this is the
   * mailbox line and not the courier line: UK Postbox issues a second address
   * for parcels (`Unit 171036, Courier Point`, `BH16 6FH`), which is a
   * delivery instruction for carriers, not a place documents are served. It is
   * recorded in `ops/accounts.md` and is deliberately published nowhere.
   *
   * **Setting this one value does four things at once**, which is the whole
   * reason it lives here rather than being typed into four files: it fills the
   * footer on every page, it adds `address` to the Organization structured
   * data, it publishes `/terms/`, and it satisfies half of what `/privacy/`
   * and the order page need. Each of those is a statement about where this
   * business can be reached. See `src/data/legal.ts`.
   *
   * **What it does not do is publish `/privacy/`.** That still waits on
   * `clientDataStorage.where` below, which is a `[PLACEHOLDER]`. The gap is
   * handled rather than ignored: the "Your information" section of `/terms/`
   * drops its link to the notice while the notice does not exist, because a
   * published contract pointing at a 404 is worse than one that doesn't.
   *
   * **The locality question is answered here, deliberately.** `ROADMAP.md` and
   * `ops/third-party-services.md` both flagged that a real address would say
   * Dorset while the founder works from the Wirral, and asked for a decision
   * rather than a default. The decision: publish the real locality. `basedIn`
   * above stays "the Wirral" because it is true and is prose about a person;
   * this is where post arrives. Two different facts, both stated plainly, is
   * the honest shape — inventing a Merseyside postal address to make them
   * match would be the exact fault this business is paid to find.
   */
  addressForService: {
    line1: 'Lytchett House, 13 Freeland Park',
    line2: 'Wareham Road',
    locality: 'Poole',
    region: 'Dorset',
    postcode: 'BH16 6FA',
    country: 'GB',
  } as PostalAddress | null,

  /**
   * The ICO data protection registration, taken out 2026-07-30. Published in
   * the privacy notice because a reader can check it against the ICO's own
   * public register in about fifteen seconds, and a business that sells
   * verifiable facts should hand them the reference rather than make them
   * search.
   */
  icoRegistration: 'C1995412',

  /**
   * **Where client and prospect records are kept. Set 2026-08-10.**
   *
   * Not a technical detail: whoever holds the files is a recipient of personal
   * data and has to be named in the privacy notice, along with where they hold
   * it. `ops/client-record.md` has the constraint that rules out the obvious
   * wrong answer — **it cannot be this repository**, which is written as though
   * it were public — and `ROADMAP.md` 3d carries the decision itself. What is
   * needed is one named provider, encryption at rest, and a backup that has
   * been restored once.
   *
   * `/privacy/` does not publish until this is set, for the same reason it does
   * not publish without the address: a notice that is vague about where the
   * data goes is worse than no notice, because it is a published claim to have
   * thought about it.
   *
   * **The history below runs to four entries in one day and is kept in full**,
   * because two of the wrong turns are the useful part and a later session that
   * only sees the answer will take one of them again.
   */
  /**
   * **Decided by the owner 2026-08-09: Microsoft OneDrive.** Chosen because
   * Office is already paid for, so it adds no supplier and no cost; the `.docx`
   * audit masters live there natively rather than being moved by hand; and
   * version history gives a restore that can actually be tested, which is the
   * condition above that a new account would not have met for weeks.
   *
   * **This does not publish `/privacy/` on its own** — the address for service
   * was the other half, and it landed on 2026-08-10. **Nor is it finished until
   * a backup has been restored once.** Setting a value here is a decision; the
   * restore is the proof, and `ops/client-record.md` carries it as the open
   * step — though see the correction at the end of this comment about *when*
   * that proof is owed.
   *
   * **`where` is deliberately a `[PLACEHOLDER]` and must not be guessed.** The
   * privacy notice states, in published wording, which country holds the data.
   * Microsoft's answer depends on the account type and the tenant's configured
   * data residency, and it is not something to assert from general knowledge.
   * `/privacy/` will not publish while this string is a placeholder, which is
   * the correct behaviour rather than a bug.
   *
   * **That instinct was right for a reason nobody had yet found. Researched
   * 2026-08-10: the account opened is a *consumer* Microsoft account, and it
   * cannot hold client records at all.** There is no country to look up —
   * Microsoft commits to none for consumer services and says so in its privacy
   * statement. There is no Article 28 processor contract — Microsoft's Data
   * Protection Addendum attaches to Commercial Licensing, and UK GDPR requires
   * that contract before any processing starts. And Microsoft Services
   * Agreement §13.h.i says the consumer Microsoft 365 plans are for personal,
   * non-commercial use. **Three independent failures, so no setting inside the
   * account can fix it.**
   *
   * **One fix is a Microsoft 365 Business subscription with the tenant created
   * as United Kingdom**, which yields a Product Terms data residency commitment
   * for OneDrive. It costs £261/year for the tier that also covers the Office
   * apps.
   *
   * **The better fix, recommended the same day: hold the records locally, on
   * the founder's own encrypted machine.** With no third party in the storage,
   * there is no Article 28 contract to need, no supplier's data location to
   * publish, and no consumer-terms problem — and `where` becomes a truthful
   * `'the United Kingdom'` for £0 a month. It is also the plainer sentence to
   * publish, which is worth something on this site in particular.
   *
   * **Two conditions come with it and neither is optional**: full-disk
   * encryption switched on and verified, and a backup — an encrypted drive kept
   * off-site, not a cloud sync — that has been restored once. Article 32 asks
   * for both, the second as an availability requirement rather than as
   * prudence. Full reasoning, the OneDrive-autosync trap, and sources:
   * `ops/client-record.md`.
   *
   * **"Do not set this value until those two conditions are met" — corrected
   * within the hour, and this is the entry worth reading.** The owner pointed
   * out that the business holds zero customer data and needed to launch. The
   * gate was checking more than the page claims, and *reading the page* settled
   * it where reasoning about it had not: `/privacy/` asserts "records are
   * encrypted at rest" and **says nothing about backups at all**.
   *
   * - **Encryption is a precondition of publishing**, because the page claims it.
   * - **The tested restore is a precondition of taking on a client**, because
   *   that is when there is data whose availability Article 32 protects.
   *
   * **The general rule: a page gates on what the page claims, not on everything
   * that is owed.** Bundling the two turned a same-day launch into a shopping
   * trip on a business whose stated constraint is to launch as early as
   * possible.
   *
   * **Set 2026-08-10, and `/privacy/` publishes.** The notice renders "It is
   * held by us, on our own encrypted computer, in the United Kingdom." **The one
   * thing that must be true before this merges is full-disk encryption actually
   * being on** — that is the page's claim, and nothing else here depends on it.
   *
   * **`name` is a sentence fragment rather than a supplier, on purpose.** The
   * privacy page reads "held by {name}, in {where}", which was "held *with*
   * {name}" until this changed — grammar that had silently assumed the holder
   * was always a third party. If a provider is ever named here again, keep the
   * preposition working for both.
   *
   * **It is not a claim that anything is stored anywhere today.** Nothing is:
   * there is no client, and no record goes into the consumer Microsoft account.
   * The sentence is a commitment about where records *will* live, published
   * before the first one exists — which is the right way round, since a notice
   * that arrives after the data is the failure it exists to prevent.
   */
  clientDataStorage: {
    name: 'us, on our own encrypted computer',
    where: 'the United Kingdom',
  } as { name: string; where: string } | null,

  areaServed: 'GB',
  areaServedLabel: 'United Kingdom',
  vatRegistered: false,
  description:
    'Wardith helps service businesses get found and recommended when their customers ask AI assistants — ChatGPT, Google, Copilot and Perplexity — who to use.',
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
   * published twice on a public page, and again in a repo we write as public.
   */
  founderLinkedIn: 'https://www.linkedin.com/in/kieran-smith-50b953143' as string | null,

  /**
   * Wardith's own LinkedIn page. Separate from the founder's profile: this one
   * joins the *Organization* in the structured data as `sameAs`, which is the
   * business claiming a second page as its own.
   *
   * **Null on purpose from 2026-08-04, and it should stay null until somebody
   * has opened the new URL in a browser.** The page's old slug was
   * `novenstudio`; renaming the page changes the slug, and the moment it
   * changes the old URL is dead. A `sameAs` is a machine-readable claim that
   * this business and that address are the same thing — so a stale one is not
   * a broken link, it is a false statement, published on a site whose entire
   * pitch is that its own facts are correct.
   *
   * A missing `sameAs` costs nothing: the builder in `schema.ts` omits the
   * key entirely rather than emitting an empty array. Set this only once the
   * renamed page has been loaded and the URL copied from the address bar —
   * and store it without the `?viewAsMember=true` LinkedIn appends when you
   * preview your own page, which is a view-mode flag rather than the
   * canonical public URL. See `ops/rename-to-wardith.md` D0.5.
   *
   * **Set 2026-08-06**, once the page had been renamed and the URL supplied
   * from the address bar. The slug changed with the name, so the old
   * `novenstudio` URL is dead — which is exactly why this stayed null through
   * the rename rather than shipping a `sameAs` pointing nowhere.
   *
   * Stored verbatim as supplied, trailing slash included: that is what
   * LinkedIn serves as the page's own address, and this value is a claim that
   * the two are the same thing rather than a link for a person to click.
   */
  businessLinkedIn: 'https://www.linkedin.com/company/wardith/' as string | null,

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

/* Prices, repriced 2026-08-05. The reasoning is in `ops/service-tiers.md`
 * section 11. The short version: the 2026-07-31 ladder (125/750/95/250/495)
 * was set against estimated effort, and the self-audit that followed showed
 * the audit was worth materially more than £125 — four assistants, repeated
 * runs, a diagnosis a person actually reads. Raising the audit left £95
 * Maintain looking out of place beside it, so the whole ladder moved together.
 *
 * Round numbers on purpose, decided by the owner 2026-08-05. Charm pricing
 * (ending 5 or 9) is a mild sales tactic, and this is a business that has
 * already refused founding rates, bundles and discounts on the grounds that
 * they sit badly on a brand built on plain dealing. The prices should read the
 * same way.
 *
 * These are still launch prices, set before the first sale on purpose: raising
 * a price on a client already paying it is a churn event, and the monthly
 * plans have no minimum term by design. */
export const oneOffs: Plan[] = [
  {
    id: 'audit',
    name: 'Audit',
    cadence: 'one-off',
    price: 250,
    summary: 'A written report on where you show up today.',
    schemaDescription:
      'One-off written report on how AI assistants currently answer questions about your business, what they believe about you, and what is blocking you from being recommended.',
  },
  {
    id: 'foundation',
    name: 'Foundation',
    cadence: 'one-off',
    price: 800,
    summary: 'The setup that makes your business readable to these systems.',
    schemaDescription:
      'One-off setup on your existing website: crawler access, structured data for your business, your facts made consistent across the web, and two permanent pages answering questions your customers ask AI assistants.',
  },
];

export const monthlies: Plan[] = [
  {
    id: 'maintain',
    name: 'Maintain',
    cadence: 'per month',
    price: 150,
    summary: 'Stay found.',
    schemaDescription:
      'Monthly plan to hold your position: ten questions your customers ask, put to the AI assistants five times each every month, with a written record of where you appeared and which questions you are still missing from. Business facts kept current and corrected when they drift. £150 per month.',
  },
  {
    id: 'grow',
    name: 'Grow',
    cadence: 'per month',
    price: 400,
    summary: 'Get found more.',
    schemaDescription:
      'Monthly plan to close the gaps: everything in Maintain across fifteen questions, plus one new permanent page each month answering a question you are currently missing from. £400 per month.',
  },
  {
    id: 'lead',
    name: 'Lead',
    cadence: 'per month',
    price: 700,
    summary: 'Front of mind.',
    schemaDescription:
      'Monthly plan for competitive markets: twenty-five questions checked every month, two new permanent answer pages each month, and a quarterly written review of the competitors being named ahead of you and why. £700 per month.',
  },
];

export const plans: Plan[] = [...oneOffs, ...monthlies];

/** Look a plan up by id, so pages never restate a price as a literal. */
export function plan(id: string): Plan {
  const found = plans.find((p) => p.id === id);
  if (!found) throw new Error(`Unknown plan: ${id}`);
  return found;
}

/** The address as a person reads it, one element per line. Empty when there is
 *  no address yet, so a caller that forgets to check renders nothing rather
 *  than the word "null". */
export function addressLines(address: PostalAddress | null): string[] {
  if (!address) return [];
  return [address.line1, address.line2, address.locality, address.region, address.postcode].filter(
    (line): line is string => Boolean(line),
  );
}

/** "£250", "£1,250" — prices on this site are always whole pounds. */
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
