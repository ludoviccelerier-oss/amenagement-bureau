// Classement des contractants généraux : données générées par etudes/top40-contractants-generaux/scripts/gen.py
import donnees from '../data/contractants.json';

export type Exercice = {
  exercice: string; ca: number | null; croissance: number | null; margeBrute: number | null; ebe: number | null;
  margeEbe: number | null; ebit: number | null; rn: number | null; margeNette: number | null; caf: number | null;
  bfr: number | null; clients: number | null; fournisseurs: number | null; autonomie: number | null; endettement: number | null;
};
export type Contractant = (typeof donnees)[number] & { comptes: { type: string; principal: Exercice[]; societe: Exercice[] } };

export const contractants = donnees as Contractant[];

export const urlClassement = '/prestataires/top-40-contractants-generaux';
export const urlFiche = (c: { slug: string }) => `/prestataires/contractants-generaux/${c.slug}`;
export const MAJ = new Date('2026-10-29');

export const SEGMENTS = {
  A: { nom: 'Majors et entreprises générales', court: 'Majors / EG' },
  B: { nom: 'Contractants généraux clé en main et ensembliers', court: 'CG clé en main' },
  C: { nom: 'Fit-out et design & build tertiaire', court: 'Fit-out tertiaire' },
  D: { nom: 'AMO et project management', court: 'AMO' },
} as const;

// Nombres au format français : 1 718,7
export const nb = (v: number | null | undefined, dec = 1, suffixe = '') =>
  v === null || v === undefined || Number.isNaN(v)
    ? 'n.d.'
    : v.toLocaleString('fr-FR', { minimumFractionDigits: dec, maximumFractionDigits: dec }) + suffixe;

export const pct = (v: number | null | undefined) => nb(v, 1, ' %');

export const mediane = (valeurs: (number | null | undefined)[]) => {
  const v = valeurs.filter((x): x is number => typeof x === 'number').sort((a, b) => a - b);
  if (!v.length) return null;
  const m = Math.floor(v.length / 2);
  return v.length % 2 ? v[m] : (v[m - 1] + v[m]) / 2;
};

// Sources communes à l'ensemble de l'étude
export const sourcesEtude = [
  { label: 'Annuaire des entreprises (État) : identité, dirigeants, établissements', url: 'https://annuaire-entreprises.data.gouv.fr' },
  { label: 'API Recherche d’entreprises (DINUM)', url: 'https://recherche-entreprises.api.gouv.fr/docs/' },
  { label: 'Ministère de l’Économie : ratios financiers issus des comptes déposés à l’INPI (jeu « ratios_inpi_bce »)', url: 'https://data.economie.gouv.fr/explore/dataset/ratios_inpi_bce/' },
  { label: 'INPI : registre national des entreprises et comptes annuels', url: 'https://data.inpi.fr' },
  { label: 'BODACC : annonces civiles et commerciales (procédures, cessions)', url: 'https://www.bodacc.fr' },
  { label: 'INSEE : nomenclature d’activités française (codes NAF)', url: 'https://www.insee.fr/fr/information/2406147' },
  { label: 'Pappers : comptes et documents juridiques des sociétés', url: 'https://www.pappers.fr' },
  { label: 'Fédération française du bâtiment (FFB) : conjoncture du bâtiment', url: 'https://www.ffbatiment.fr' },
  { label: 'Xerfi : études sectorielles du BTP', url: 'https://www.xerfi.com' },
];
