import { getCollection, type CollectionEntry } from 'astro:content';

export type Guide = CollectionEntry<'guides'>;

export const urlGuide = (g: Guide) => `/guides/${g.id}`;

export const tempsLecture = (g: Guide) => Math.max(2, Math.round((g.body ?? '').split(/\s+/).length / 220));

export const guidesTries = async () =>
  (await getCollection('guides')).sort((a, b) => b.data.updated.getTime() - a.data.updated.getTime());

export const guidesDe = async (rubrique: string) =>
  (await getCollection('guides', (g) => g.data.rubrique === rubrique)).sort((a, b) => a.data.ordre - b.data.ordre);
