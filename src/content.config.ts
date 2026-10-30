import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';
import { rubriques } from './data/site';

const ids = rubriques.map((r) => r.id) as [string, ...string[]];

// Guides : /guides/<nom du fichier>
const guides = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/guides' }),
  schema: z.object({
    title: z.string(),
    seoTitle: z.string(),
    description: z.string(),
    rubrique: z.enum(ids),
    date: z.coerce.date(),
    updated: z.coerce.date(),
    ordre: z.number().default(50), // rang dans la rubrique
    photo: z.string(), // nom d'un fichier de src/assets/photos (sans .jpg)
    photoAlt: z.string(),
    // « L'essentiel » : réponse directe en tête d'article, reprise par les moteurs et assistants IA
    essentiel: z.array(z.string()).min(3),
    faq: z.array(z.object({ q: z.string(), r: z.string() })).default([]),
    sources: z.array(z.object({ label: z.string(), url: z.string().url() })).default([]),
  }),
});

export const collections = { guides };
