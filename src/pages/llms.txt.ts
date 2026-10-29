// Résumé du site pour les assistants IA (convention llms.txt), généré à chaque build.
import type { APIRoute } from 'astro';
import { rubriques, site } from '../data/site';
import { guidesDe, urlGuide } from '../lib/guides';
import { abs } from '../lib/schema';

export const GET: APIRoute = async () => {
  const lignes = [
    `# ${site.nom} – ${site.baseline}`,
    '',
    `> ${site.description} Contenus en français, pour la France, rédigés pour des non-spécialistes. Chaque guide s'ouvre sur un résumé « L'essentiel en 30 secondes » et se termine par une FAQ et ses sources.`,
    '',
  ];
  for (const r of rubriques) {
    const guides = await guidesDe(r.id);
    if (!guides.length) continue;
    lignes.push(`## ${r.titre}`, ...guides.map((g) => `- [${g.data.title}](${abs(urlGuide(g))}) : ${g.data.description}`), '');
  }
  lignes.push('## Référence', `- [Glossaire de l'aménagement de bureaux](${abs('/glossaire')})`, `- [Méthode éditoriale](${abs('/a-propos')})`);
  return new Response(lignes.join('\n') + '\n', { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
