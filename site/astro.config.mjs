import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// [PLACEHOLDER] Replace with the real production domain before launch,
// then update the Sitemap line in public/robots.txt to match.
export default defineConfig({
  site: 'https://www.noven.co.uk',
  integrations: [sitemap()],
});
