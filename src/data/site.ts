export const site = {
  nom: 'amenagement-bureau.com', // charte : toujours en minuscules, avec le .com
  domaine: 'amenagement-bureau.com',
  url: 'https://www.amenagement-bureau.com',
  baseline: "Le guide pratique de l'aménagement de bureaux",
  description:
    "Aménager ses bureaux expliqué simplement aux dirigeants, directeurs immobiliers et bailleurs : étapes, prix au m², financement, fiscalité, choix du contractant.",
  redaction: 'La rédaction d’amenagement-bureau.com',
};

// Les rubriques structurent la navigation, les URL /rubriques/<id> et le fil d'Ariane
export const rubriques = [
  {
    id: 'comprendre',
    photo: 'salon-plateau',
    nom: 'Comprendre',
    titre: "Comprendre l'aménagement de bureaux",
    intro: 'Le vocabulaire, les ordres de grandeur et les bonnes questions à se poser avant de lancer quoi que ce soit.',
  },
  {
    id: 'etapes',
    photo: 'couloir-vitre',
    nom: 'Les étapes',
    titre: "Les étapes d'un projet de bureaux",
    intro: "Du premier besoin à la réception des travaux : qui intervient, quand, et ce que vous devez valider à chaque étape.",
  },
  {
    id: 'prestataires',
    photo: 'postes-bois',
    nom: 'Prestataires',
    titre: 'Choisir ses prestataires',
    intro: "Contractant général, entreprise générale, space planner, AMO : les comparer et les choisir partout en France.",
  },
  {
    id: 'budget-financement',
    photo: 'espace-detente',
    nom: 'Budget & financement',
    titre: 'Budget et financement des travaux',
    intro: "Combien prévoir au mètre carré, et comment payer : fonds propres, crédit, leasing, participation du bailleur.",
  },
  {
    id: 'fiscalite-comptabilite',
    photo: 'bureau-blanc',
    nom: 'Fiscalité & compta',
    titre: 'Fiscalité et comptabilité des travaux',
    intro: "Charge ou immobilisation, amortissement, TVA, normes IFRS : ce que le directeur financier va vous demander.",
  },
  {
    id: 'bailleurs',
    photo: 'hall-immeuble',
    nom: 'Bailleurs',
    titre: 'Propriétaires et bailleurs',
    intro: "Remettre un plateau en état, l'aménager pour le louer plus vite, répartir et financer les travaux avec le locataire.",
  },
  {
    id: 'reglementation',
    photo: 'cloisons-vitrees',
    nom: 'Réglementation',
    titre: 'Réglementation des bureaux',
    intro: 'Décret tertiaire, Code du travail, accessibilité, sécurité incendie : les règles qui encadrent votre projet.',
  },
] as const;

export type RubriqueId = (typeof rubriques)[number]['id'];
export const rubrique = (id: string) => rubriques.find((r) => r.id === id)!;
