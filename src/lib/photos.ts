import credits from '../data/photos.json';

// Photos libres de droits : src/assets/photos/<nom>.jpg, crédits dans src/data/photos.json
const fichiers = import.meta.glob<{ default: ImageMetadata }>('../assets/photos/*.jpg', { eager: true });

export type Credit = { auteur: string; licence: string; source: string };

export const photo = (nom: string) => {
  const image = fichiers[`../assets/photos/${nom}.jpg`]?.default;
  if (!image) throw new Error(`Photo introuvable : src/assets/photos/${nom}.jpg`);
  return image;
};
export const credit = (nom: string): Credit | undefined => (credits as Record<string, Credit>)[nom];
