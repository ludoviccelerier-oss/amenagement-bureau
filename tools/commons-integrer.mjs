// Télécharge les photos Commons retenues (1 800 px de large) dans src/assets/photos
// et écrit leurs crédits dans src/data/photos.json. Usage : node tools/commons-integrer.mjs <candidats.json>
import { readFileSync, writeFileSync } from 'node:fs';
const UA = 'amenagement-bureau-site/1.0 (https://www.amenagement-bureau.com)';
const choix = {
  accueil: 83, 'plateau-vide': 99, 'bureau-vide': 25, 'couloir-vitre': 84, 'cloisons-vitrees': 77, 'postes-bois': 20,
  'grand-plateau': 23, 'bureau-blanc': 30, 'salon-plateau': 32, 'espace-detente': 146,
  'salon-fauteuils': 145, 'hall-immeuble': 176,
};
const liste = JSON.parse(readFileSync(process.argv[2]));
const credits = {};
for (const [nom, i] of Object.entries(choix)) {
  const p = liste[i];
  const url = 'https://commons.wikimedia.org/w/api.php?' + new URLSearchParams({ action: 'query', format: 'json', titles: p.titre, prop: 'imageinfo', iiprop: 'url', iiurlwidth: '1800' });
  const j = await (await fetch(url, { headers: { 'User-Agent': UA } })).json();
  const ii = Object.values(j.query.pages)[0].imageinfo[0];
  const buf = Buffer.from(await (await fetch(ii.thumburl, { headers: { 'User-Agent': UA } })).arrayBuffer());
  writeFileSync(`src/assets/photos/${nom}.jpg`, buf);
  credits[nom] = { auteur: p.auteur, licence: p.licence, source: p.page };
  console.log(nom, Math.round(buf.length / 1024), 'Ko');
}
writeFileSync('src/data/photos.json', JSON.stringify(credits, null, 2) + '\n');
