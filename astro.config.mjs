import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import fs from 'node:fs';

// Date de mise à jour de chaque guide (champ updated, sinon date), pour le <lastmod> du sitemap
const majGuides = Object.fromEntries(
  fs.readdirSync('src/content/guides').filter((f) => f.endsWith('.md')).map((f) => {
    const front = fs.readFileSync(`src/content/guides/${f}`, 'utf8');
    const date = (front.match(/^updated:\s*(\S+)/m) ?? front.match(/^date:\s*(\S+)/m))?.[1];
    return [`/guides/${f.replace(/\.md$/, '')}`, date];
  }),
);
// Même date que MAJ dans src/lib/contractants.ts
const majContractants = fs.readFileSync('src/lib/contractants.ts', 'utf8').match(/MAJ = new Date\('([\d-]+)'\)/)?.[1];

export default defineConfig({
  site: 'https://www.amenagement-bureau.com',
  trailingSlash: 'never',
  build: { format: 'file', inlineStylesheets: 'always' }, // CSS dans la page : rien ne bloque l'affichage
  integrations: [
    sitemap({
      filter: (page) => !/\/(404|mentions-legales)$/.test(page),
      serialize(item) {
        const chemin = new URL(item.url).pathname;
        const date = majGuides[chemin] ?? (chemin.startsWith('/prestataires/') ? majContractants : undefined);
        if (date) item.lastmod = new Date(date).toISOString();
        return item;
      },
    }),
  ],
});
