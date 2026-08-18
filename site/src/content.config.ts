/* Content collections.
 *
 * `context` holds approved finds from the /context-watch skill, promoted one
 * at a time by the owner. This file only defines the shape — no page reads
 * from it yet, so nothing here is live on the site.
 */

import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const context = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/context' }),
  schema: z.object({
    title: z.string(),
    url: z.string().url(),
    publisher: z.string(),
    date: z.coerce.date(),
    excerpt: z.string(),
    note: z.string(),
    promotedDate: z.coerce.date(),
  }),
});

export const collections = { context };
