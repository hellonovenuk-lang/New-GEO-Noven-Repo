import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Production domain. If the Netlify primary domain is set to the www variant
// instead, change this to match and update the Sitemap line in
// public/robots.txt — the two must always agree.
export default defineConfig({
  site: 'https://wardith.co.uk',
  integrations: [sitemap()],
});
