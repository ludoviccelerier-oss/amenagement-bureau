// Glossaire : chaque terme a une ancre /glossaire#<id> ; `voir` pointe vers le guide qui le développe
export type Terme = { terme: string; def: string; voir?: string };

const termes: Terme[] = [
  { terme: 'AMO (assistance à maîtrise d’ouvrage)', def: "Conseil indépendant qui aide l'entreprise à définir son besoin, choisir ses prestataires et piloter le projet. L'AMO ne conçoit pas et ne réalise pas les travaux : il défend les intérêts du client.", voir: 'contractant-general-entreprise-generale-lots-separes' },
  { terme: 'APS / APD', def: "Avant-projet sommaire puis avant-projet détaillé : les deux niveaux de conception qui précisent progressivement le plan, les matériaux et le budget avant la consultation des entreprises.", voir: 'etapes-projet-amenagement-bureaux' },
  { terme: 'BACS (décret)', def: "Obligation d'équiper certains bâtiments tertiaires d'un système d'automatisation et de contrôle (GTB) selon la puissance de leurs installations de chauffage ou de climatisation.", voir: 'reglementation-bureaux-decret-tertiaire-code-du-travail' },
  { terme: 'Capex / Opex', def: "Capex : dépense d'investissement, inscrite à l'actif et amortie. Opex : dépense de fonctionnement, passée en charge (loyers, entretien). Le mode de financement choisi déplace souvent une dépense de l'un vers l'autre.", voir: 'financer-travaux-amenagement-bureaux' },
  { terme: 'CAT A', def: "Niveau de livraison d'un plateau de bureaux par le bailleur : faux plafonds, éclairage de base, chauffage-climatisation, faux plancher ou goulottes, sanitaires. Le plateau est fonctionnel mais pas cloisonné ni décoré.", voir: 'cat-a-cat-b-definition' },
  { terme: 'CAT B', def: "Aménagements réalisés pour un occupant précis sur un plateau CAT A : cloisons, salles de réunion, espaces de pause, câblage, finitions, signalétique, souvent mobilier.", voir: 'cat-a-cat-b-definition' },
  { terme: 'Contractant général', def: "Entreprise unique qui prend en charge la conception et la réalisation des travaux, avec un engagement global de prix et de délai. On parle aussi de « design & build ».", voir: 'contractant-general-entreprise-generale-lots-separes' },
  { terme: 'Corps d’état', def: "Spécialité de travaux (électricité, plomberie, cloisons, peinture…). « Tous corps d'état » (TCE) désigne une prestation qui les regroupe tous." },
  { terme: 'Crédit-bail', def: "Location d'un bien avec option d'achat en fin de contrat. Les loyers sont en principe déductibles ; le bien n'apparaît pas à l'actif en comptes sociaux français.", voir: 'financer-travaux-amenagement-bureaux' },
  { terme: 'CVC', def: 'Chauffage, ventilation, climatisation : le poste technique le plus coûteux et le plus contraint lors d’un redécoupage de plateau.' },
  { terme: 'DCE (dossier de consultation des entreprises)', def: "Ensemble des pièces (plans, descriptif, quantitatif, planning) envoyées aux entreprises pour qu'elles chiffrent les travaux sur une base identique.", voir: 'etapes-projet-amenagement-bureaux' },
  { terme: 'Décret tertiaire', def: "Obligation de réduire la consommation d'énergie des bâtiments tertiaires d'au moins 1 000 m² : –40 % en 2030, –50 % en 2040, –60 % en 2050 par rapport à une année de référence.", voir: 'reglementation-bureaux-decret-tertiaire-code-du-travail' },
  { terme: 'DOE (dossier des ouvrages exécutés)', def: "Dossier remis à la fin des travaux : plans à jour, fiches techniques, notices. Indispensable pour l'exploitation et pour les travaux suivants." },
  { terme: 'Dommages-ouvrage', def: "Assurance souscrite par le maître d'ouvrage qui préfinance les réparations relevant de la garantie décennale, sans attendre de recherche de responsabilité.", voir: 'reception-travaux-reserves-garanties' },
  { terme: 'Durée d’usage', def: "Durée d'amortissement admise par l'usage dans chaque profession, servant de référence fiscale. Pour les agencements, elle se situe généralement entre 10 et 20 ans.", voir: 'travaux-bureaux-charge-ou-immobilisation' },
  { terme: 'Entreprise générale', def: "Entreprise qui réalise l'ensemble des travaux sous un seul contrat, à partir d'une conception faite par un autre (architecte, space planner).", voir: 'contractant-general-entreprise-generale-lots-separes' },
  { terme: 'ERP / ERT', def: "Établissement recevant du public / établissement recevant des travailleurs. Des bureaux sans accueil du public relèvent du Code du travail (ERT) ; un accueil du public ajoute les règles ERP.", voir: 'reglementation-bureaux-decret-tertiaire-code-du-travail' },
  { terme: 'Flex office', def: "Organisation sans poste attribué, où le nombre de postes est inférieur au nombre de collaborateurs. On parle de taux de partage (par exemple 0,8 poste par personne)." },
  { terme: 'Franchise de loyer', def: "Période sans loyer accordée par le bailleur à la signature du bail, souvent en contrepartie des travaux d'aménagement pris en charge par le locataire.", voir: 'financer-travaux-amenagement-bureaux' },
  { terme: 'Garantie biennale', def: "Garantie de bon fonctionnement de deux ans sur les équipements dissociables du bâtiment (portes, appareils, éléments démontables).", voir: 'reception-travaux-reserves-garanties' },
  { terme: 'Garantie décennale', def: "Responsabilité de dix ans des constructeurs pour les dommages qui compromettent la solidité de l'ouvrage ou le rendent impropre à sa destination.", voir: 'reception-travaux-reserves-garanties' },
  { terme: 'Garantie de parfait achèvement', def: "Obligation pendant un an après la réception de réparer tous les désordres signalés, qu'ils figurent dans les réserves ou qu'ils apparaissent ensuite.", voir: 'reception-travaux-reserves-garanties' },
  { terme: 'GTB', def: 'Gestion technique du bâtiment : système qui pilote et mesure chauffage, ventilation, éclairage pour réduire les consommations.' },
  { terme: 'IFRS 16', def: "Norme comptable internationale qui impose d'inscrire au bilan la plupart des contrats de location (droit d'utilisation et dette), y compris les baux de bureaux, pour les groupes qui l'appliquent.", voir: 'travaux-bureaux-charge-ou-immobilisation' },
  { terme: 'Immobilisation', def: "Dépense inscrite à l'actif du bilan parce qu'elle profite à l'entreprise sur plusieurs exercices ; elle est ensuite amortie.", voir: 'travaux-bureaux-charge-ou-immobilisation' },
  { terme: 'Location financière', def: "Location d'équipements sur une durée fixe, sans option d'achat obligatoire. Les loyers sont des charges ; utilisée pour le mobilier, l'informatique, l'audiovisuel.", voir: 'financer-travaux-amenagement-bureaux' },
  { terme: 'Lots séparés', def: "Mode de réalisation où l'entreprise signe un contrat avec chaque corps d'état, coordonnés par un maître d'œuvre. Souvent moins cher, mais plus exigeant à piloter.", voir: 'contractant-general-entreprise-generale-lots-separes' },
  { terme: 'Maître d’ouvrage', def: "Celui pour qui les travaux sont réalisés et qui les paie : ici, l'entreprise occupante (ou le bailleur pour les travaux qui lui incombent)." },
  { terme: 'Maîtrise d’œuvre', def: "Équipe qui conçoit le projet et dirige les travaux pour le compte du maître d'ouvrage : architecte, architecte d'intérieur, bureau d'études." },
  { terme: 'OPERAT', def: "Plateforme de l'ADEME sur laquelle les assujettis au décret tertiaire déclarent chaque année leurs consommations d'énergie.", voir: 'reglementation-bureaux-decret-tertiaire-code-du-travail' },
  { terme: 'Participation du bailleur', def: "Somme versée par le propriétaire pour financer une partie des travaux du locataire, négociée à la signature du bail.", voir: 'financer-travaux-amenagement-bureaux' },
  { terme: 'Programmation', def: "Étape qui traduit l'organisation de l'entreprise (effectifs, façons de travailler, besoins de réunion) en surfaces et en espaces à créer.", voir: 'etapes-projet-amenagement-bureaux' },
  { terme: 'Réception des travaux', def: "Acte par lequel le maître d'ouvrage accepte les travaux, avec ou sans réserves. Elle fait courir les garanties légales.", voir: 'reception-travaux-reserves-garanties' },
  { terme: 'Remise en état', def: "Obligation éventuelle du locataire, en fin de bail, de rendre les locaux dans l'état prévu au bail. À chiffrer dès le départ.", voir: 'amenager-ses-bureaux-par-ou-commencer' },
  { terme: 'Réserves', def: "Défauts ou non-conformités listés au procès-verbal de réception, que l'entreprise doit corriger.", voir: 'reception-travaux-reserves-garanties' },
  { terme: 'Retenue de garantie', def: "Part du prix des travaux (5 % au maximum) conservée pendant un an pour garantir la levée des réserves. Elle peut être remplacée par une caution bancaire.", voir: 'reception-travaux-reserves-garanties' },
  { terme: 'Space planning', def: "Conception de l'implantation des espaces et des postes de travail sur un plateau, à partir du programme." },
  { terme: 'SUBL', def: "Surface utile brute locative : surface louée hors parties communes générales, base habituelle du loyer et des ratios en bureaux." },
];

export const glossaire = termes
  .map((t) => ({ ...t, id: t.terme.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') }))
  .sort((a, b) => a.terme.localeCompare(b.terme, 'fr'));
