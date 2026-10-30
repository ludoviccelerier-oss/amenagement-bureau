import { writeFileSync } from 'node:fs';
const UA = 'amenagement-bureau-site/1.0 (https://www.amenagement-bureau.com)';
const requetes = ['modern office interior', 'open plan office', 'office meeting room', 'coworking space interior', 'empty office floor', 'office workspace desks', 'office lounge', 'office building lobby', 'office renovation works', 'office kitchen break room', 'office chairs desk window'];
const OK = /^(CC0|CC BY( |-|$)|CC BY-SA|Public domain)/i;
const vus = new Map();
for (const q of requetes) {
  const url = 'https://commons.wikimedia.org/w/api.php?' + new URLSearchParams({
    action: 'query', format: 'json', generator: 'search', gsrnamespace: '6', gsrlimit: '50', gsrsearch: `${q} filetype:bitmap`,
    prop: 'imageinfo', iiprop: 'url|size|extmetadata|mime', iiurlwidth: '400',
  });
  const j = await (await fetch(url, { headers: { 'User-Agent': UA } })).json();
  for (const p of Object.values(j.query?.pages ?? {})) {
    const ii = p.imageinfo?.[0]; if (!ii) continue;
    const m = ii.extmetadata ?? {};
    const licence = (m.LicenseShortName?.value ?? '').trim();
    const r = ii.width / ii.height;
    if (!/jpeg/.test(ii.mime) || ii.width < 2000 || r < 1.3 || r > 2) continue;
    if (!OK.test(licence)) continue;
    const auteur = (m.Artist?.value ?? '').replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
    vus.set(p.title, { q, titre: p.title, l: ii.width, h: ii.height, licence, auteur, original: ii.url, vignette: ii.thumburl, page: ii.descriptionurl });
  }
}
const liste = [...vus.values()];
writeFileSync(process.argv[2], JSON.stringify(liste, null, 1));
console.log(liste.length);
