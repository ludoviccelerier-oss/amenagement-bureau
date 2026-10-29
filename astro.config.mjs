import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://www.amenagement-bureau.com',
  trailingSlash: 'never',
  build: { format: 'file', inlineStylesheets: 'always' }, // CSS dans la page : rien ne bloque l'affichage
  integrations: [sitemap({ filter: (page) => !/\/(404|mentions-legales)$/.test(page) })],
});
