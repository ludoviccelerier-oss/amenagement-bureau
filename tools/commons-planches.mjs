import sharp from 'sharp';
import { readFileSync } from 'node:fs';
const [,, fichier, dossier] = process.argv;
const liste = JSON.parse(readFileSync(fichier));
const UA = 'amenagement-bureau-site/1.0 (https://www.amenagement-bureau.com)';
const W = 260, H = 170, C = 7, PAR = 42;
for (let s = 0; s * PAR < liste.length; s++) {
  const lot = liste.slice(s * PAR, (s + 1) * PAR);
  const comps = [];
  for (const [i, p] of lot.entries()) {
    const n = s * PAR + i;
    try {
      const buf = Buffer.from(await (await fetch(p.vignette, { headers: { 'User-Agent': UA } })).arrayBuffer());
      const img = await sharp(buf).resize(W, H, { fit: 'cover' }).toBuffer();
      const lab = Buffer.from(`<svg width="${W}" height="${H}"><rect width="46" height="28" fill="#000"/><text x="6" y="21" font-size="20" font-family="Arial" fill="#ff0">${n}</text></svg>`);
      comps.push({ input: await sharp(img).composite([{ input: lab }]).toBuffer(), left: (i % C) * W, top: Math.floor(i / C) * H });
    } catch {}
  }
  await sharp({ create: { width: C * W, height: Math.ceil(lot.length / C) * H, channels: 3, background: '#fff' } }).composite(comps).jpeg({ quality: 70 }).toFile(`${dossier}/planche-${s}.jpg`);
}
console.log('ok');
