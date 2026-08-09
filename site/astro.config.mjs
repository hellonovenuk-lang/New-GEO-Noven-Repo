import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Production domain. If the Netlify primary domain is set to the www variant
// instead, change this to match and update the Sitemap line in
// public/robots.txt — the two must always agree.
export default defineConfig({
  site: 'https://wardith.co.uk',
  integrations: [
    sitemap({
      // `/order/pay/` is the second half of a transaction and carries
      // `noindex`. Listing it here as well would be a straight contradiction:
      // a sitemap is a request to index. It is excluded by path rather than by
      // a flag because when the order page is switched off (see
      // `src/data/order.ts`) the page is never built, and this filter simply
      // never matches anything.
      filter: (page) => !page.includes('/order/pay/'),
    }),
  ],
});
