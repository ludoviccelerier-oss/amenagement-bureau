import { site } from '../data/site';

export type Miette = { label: string; href: string };
export type QR = { q: string; r: string };

export const abs = (chemin: string) => new URL(chemin, site.url).href;

export const editeur = {
  '@type': 'Organization',
  '@id': `${site.url}/#editeur`,
  name: site.nom,
  url: site.url,
  logo: abs('/favicon.svg'),
};

export const schemaFilAriane = (miettes: Miette[]) => ({
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  itemListElement: miettes.map((m, i) => ({ '@type': 'ListItem', position: i + 1, name: m.label, item: abs(m.href) })),
});

export const schemaFaq = (liste: QR[]) => ({
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: liste.map((f) => ({ '@type': 'Question', name: f.q, acceptedAnswer: { '@type': 'Answer', text: f.r } })),
});

export const dateFr = (d: Date | string) =>
  new Date(d).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' });

export const dateIso = (d: Date) => d.toISOString().slice(0, 10);
