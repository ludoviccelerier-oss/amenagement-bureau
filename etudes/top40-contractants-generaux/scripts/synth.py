import json, os, sys
OUT = sys.argv[1]
R = json.load(open(os.path.join(os.path.dirname(__file__), "rows.json")))
SEG = {"A": "Majors / EG", "B": "CG clé en main", "C": "Fit-out tertiaire", "D": "AMO"}

def f(v, d=1, suf=""):
    return "n.d." if v is None else f"{v:,.{d}f}".replace(",", " ").replace(".", ",") + suf

def link(x):
    return f"[{x['name']}](fiches/{x['rank']:02d}-{x['slug']}.md)"

rank = "| # | Entreprise | Segment | Exercice | CA (M€) | Var. N-1 | TCAM | Marge EBE moy. 3 ans | Autonomie fin. | BFR (j) | Solidité | Score tertiaire | Note |\n|--:|---|---|---|--:|--:|--:|--:|--:|--:|:-:|:-:|:-:|\n"
for x in R:
    rank += f"| {x['rank']} | {link(x)}{' *(conso.)*' if x['conso'] else ''} | {SEG[x['seg']]} | {x['year'] or 'n.d.'} | {f(x['ca'])} | {f(x['yoy'], 1, ' %')} | {f(x['cagr'], 1, ' %')} | {f(x['me3'], 1, ' %')} | {f(x['af'], 1, ' %')} | {f(x['bfr'], 0)} | {'n.d.' if x['sol'] is None else str(x['sol']) + '/5'} | {x['hip_score']} | **{x['global_score']}** |\n"

top_rent = sorted([x for x in R if x["me3"] is not None], key=lambda x: -x["me3"])[:10]
rent = "| Entreprise | Marge EBE moy. 3 ans | CA (M€) |\n|---|--:|--:|\n" + "".join(f"| {link(x)} | {f(x['me3'], 1, ' %')} | {f(x['ca'])} |\n" for x in top_rent)
loss = sorted([x for x in R if (x["me3"] or 0) < 0], key=lambda x: x["me3"])
lossT = "| Entreprise | Marge EBE moy. 3 ans | Autonomie fin. |\n|---|--:|--:|\n" + "".join(f"| {link(x)} | {f(x['me3'], 1, ' %')} | {f(x['af'], 1, ' %')} |\n" for x in loss)

hip = sorted(R, key=lambda x: (-x["hip_score"], -x["tert"]))
hipT = "| Entreprise | Expertise tertiaire | Score tertiaire | Rôle dans l'écosystème |\n|---|:-:|:-:|---|\n" + "".join(f"| {link(x)} | {x['tert']}/5 | {x['hip_score']} | {x['role']} |\n" for x in hip[:15])

def q(x):  # quadrant : x = expertise tertiaire, y = taille (log du CA)
    import math
    n = x['name'].split(' (')[0].split(' –')[0].replace('&', 'et')[:28]
    return f"    {n}: [{(x['tert'] - 0.5) / 5:.2f}, {min(0.98, max(0.02, (math.log10(max(x['ca'] or 1, 1)) - 0.3) / 3)):.2f}]"
quad = "```mermaid\nquadrantChart\n    title Cartographie concurrentielle : taille vs expertise tertiaire\n    x-axis Faible expertise tertiaire --> Forte expertise tertiaire\n    y-axis Petite taille --> Grande taille\n    quadrant-1 Grands acteurs tertiaires\n    quadrant-2 Généralistes de volume\n    quadrant-3 Spécialistes non tertiaires\n    quadrant-4 Spécialistes tertiaires agiles\n" + "\n".join(q(x) for x in R if x["rank"] <= 30 or x["seg"] == "C") + "\n```\n"

import statistics as st
LBL = {"A": "Majors / entreprises générales", "B": "Contractants généraux clé en main / ensembliers", "C": "Fit-out et design & build tertiaire", "D": "AMO / project management"}
segT = "| Segment | Nb | CA cumulé (M€) | Marge EBE médiane | BFR médian (j) | Autonomie fin. médiane |\n|---|--:|--:|--:|--:|--:|\n"
for k in "ABCD":
    xs = [x for x in R if x["seg"] == k]
    med = lambda v: st.median(v) if v else None
    segT += f"| {LBL[k]} | {len(xs)} | {f(sum(x['ca'] or 0 for x in xs), 0)} | {f(med([x['me3'] for x in xs if x['me3'] is not None]), 1, ' %')} | {f(med([x['bfr'] for x in xs if x['bfr'] is not None]), 0)} | {f(med([x['af'] for x in xs if x['af'] is not None]), 1, ' %')} |\n"
md = f"""# Synthèse stratégique : les principaux contractants généraux en France ({len(R)} acteurs)

*Étude réalisée le 29/10/2026 à partir des comptes déposés (INPI, jeu « ratios_inpi_bce »), du registre national des entreprises et de sources publiques. Fiches détaillées dans [`fiches/`](fiches/) ; base comparative dans [`base-comparative.xlsx`](base-comparative.xlsx).*

## 1. Messages clés

1. **Un marché à trois étages.** Les filiales des majors (Bouygues, VINCI, Eiffage, Spie batignolles, Fayat) écrasent le marché en volume : à elle seule, Bouygues Bâtiment Île-de-France réalise 1,7 Md€. Les ETI indépendantes (Léon Grosse, Demathieu Bard, GCC) dépassent chacune 700 M€. Le contractant général « pur » est dominé par **GSE** (933 M€ consolidés). Le fit-out tertiaire reste concentré sur **Tétris** (236 M€), loin devant Korus (environ 155-168 M€ revendiqués au niveau du groupe, dont 67 M€ dans l'entité française DASA), Kardham (environ 100 M€) et une longue traîne de PME de moins de 50 M€.
2. **Une rentabilité structurellement mince.** La marge d'EBE médiane du panel ressort à **{f(st.median([x['me3'] for x in R if x['me3'] is not None]), 1, ' %')}** sur trois ans et {sum(1 for x in R if (x['me3'] or 0) < 0)} acteurs sur {len(R)} ont un EBE moyen négatif. Les marges supérieures à 5 % relèvent de modèles particuliers : industrialisation (Briand, 13 %), petites structures spécialisées (Isospace 7 %, Cicad 6 %) ou honoraires (Turner & Townsend 15 %, Archimage 7 %).
3. **Le BFR est un critère clé.** Le modèle Bouygues fonctionne avec un BFR négatif (−24 jours de CA chez BB IDF) : les clients financent le chantier. À l'inverse, les filiales Eiffage, VINCI et Fayat portent plus de 100 jours de CA, adossées à la trésorerie de leur groupe. Côté fit-out, Tétris immobilise **103 jours de CA** : les spécialistes de l'aménagement financent une part importante des chantiers et négocient des échéanciers d'acomptes.
4. **Le CA publié surestime la valeur ajoutée.** Chez un CG, le CA inclut l'intégralité des travaux sous-traités. Tétris affiche ainsi une « marge brute » de 89 % du CA, alors que sa valeur ajoutée réelle est bien plus faible (sous-traitance classée en charges externes). La comparaison des marges doit se faire sur l'EBE et, idéalement, sur la marge sur travaux tirée des liasses.
5. **Peu d'acteurs maîtrisent vraiment l'aménagement tertiaire.** Une dizaine seulement combinent expertise des plateaux, capacité multi-sites et solidité financière. La dynamique concurrentielle est portée par les **offres intégrées des conseils internationaux** (JLL avec Tétris, CBRE avec Turner & Townsend) et par les **ensembliers** (Linkcity, GA), qui associent montage, conception, travaux et services.

## 2. Classement général (CA du dernier exercice publié)

Chaque ligne correspond à **une entité juridique**, sans addition entre filiales et groupes. Les comptes consolidés (type K) ne sont retenus que pour Léon Grosse, GSE et Quartus.

{rank}
*Note globale = moyenne de l'attractivité (jugée), de la solidité (calculée) et du potentiel (jugé). Le score tertiaire est la moyenne des 5 critères de la grille de lecture tertiaire : expertise tertiaire, accès aux donneurs d'ordre, capacité de réalisation, modèle de marge et capacité financière.*

## 3. Lecture par segment

{segT}

- **Majors et EG.** Leur force tient au volume, à l'ingénierie et à la trésorerie du groupe. Les filiales Bouygues sont les plus homogènes (BFR négatif, EBE de 2 à 8 %). Les filiales Eiffage et VINCI ont des fonds propres très faibles (1 à 5 % du bilan) et vivent de la garantie implicite du groupe. Les indépendants (Léon Grosse, Demathieu Bard, GCC) croissent vite (TCAM de 6 à 12 %) mais avec des marges de 2 à 3 % ; la dégradation de GCC en 2025 (EBE ramené de 34 à 4 M€, BFR de 162 jours) mérite d'être suivie.
- **CG clé en main.** GSE est la référence du modèle (conception intégrée, 100 % des travaux sous-traités, BFR social négatif, adossement à GOLDBECK). GA et Briand illustrent l'intégration industrielle (usines béton, métal, bois), qui produit soit des marges élevées (Briand), soit un BFR et un levier lourds (GA). Les ensembliers (Linkcity, Quartus) souffrent de la crise de la promotion.
- **Fit-out tertiaire.** C'est un marché fragmenté : Tétris détient une position de leader incontestée, Kardham et Korus jouent l'intégration du conseil au mobilier (Korus y ajoute la maintenance de réseaux multi-sites, mais avec des marges quasi nulles dans son entité française), les architectes-contractants comme OVGA se placent sur la transformation d'immeubles, et les PME agiles (Isospace, Cicad) sont rentables mais limitées en capacité. Les acteurs hybrides conseil-CG (Parella) sont fragiles financièrement.
- **AMO.** Les marges sont élevées et le capital engagé faible, mais ces acteurs ne réalisent pas. Ce sont des **prescripteurs** à cultiver plutôt que des partenaires travaux.

## 4. Rentabilité : leaders et acteurs en difficulté

**Top 10 de la marge d'EBE (moyenne sur 3 ans)**

{rent}
**Acteurs à EBE moyen négatif (vigilance contrepartie)**

{lossT}
*Les marges de Chantiers Modernes (EBE 2024 exceptionnel) et d'Elcimaï Réalisations (CA très volatil) sont à confirmer dans les liasses.*

## 5. Cartographie concurrentielle

{quad}
*Lecture : en haut à droite, les grands acteurs tertiaires (Bouygues Bâtiment IDF, Eiffage Construction Tertiaire, Tétris) ; en bas à droite, les spécialistes tertiaires agiles (Isospace, Cicad, Pradeau Morin, Spie batignolles Présance) ; en haut à gauche, les généralistes de volume orientés logement, industrie ou logistique.*

## 6. Analyse des modèles économiques

| Modèle | Exemples | Source de marge | Portage du risque | BFR | Pertinence pour l'aménagement de bureaux |
|---|---|---|---|---|---|
| **Entreprise générale de major** | Bouygues, Eiffage, VINCI | Marge sur travaux, production propre de gros œuvre | Prix-délai forfaitaire | Négatif (Bouygues) à très positif (Eiffage, VINCI) | Faible : seuils trop élevés pour un plateau seul |
| **EG indépendante** | Léon Grosse, Demathieu Bard, GCC | Marge sur travaux | Forfait | Proche de zéro à élevé | Moyen : restructuration d'immeubles entiers |
| **Contractant général pur** | GSE, Elcimaï Réalisations | Marge sur achats et ingénierie, 100 % sous-traité | Forfait global + conception | Négatif à modéré | Faible : orienté logistique et industrie |
| **CG industrialisé** | GA, Briand, Ossabois | Marge industrielle + CG | Forfait + risque usine | Élevé | Moyen : modules et bureaux hors-site |
| **Fit-out design & build** | Tétris, Korus, Kardham, Isospace, OVGA | Honoraires de design + marge sur travaux (et mobilier) | Forfait prix-délai sur plateau | Environ 100 jours | **Forte : cœur de métier** |
| **Agenceur / second œuvre** | AGB, Spie batignolles Présance | Marge de production | Lots ou TCE | Modéré | **Fort : maîtrise du coût au m²** |
| **Ensemblier / promoteur** | Linkcity, Quartus | Marge de promotion | Risque foncier et commercial | Très élevé | Moyenne : reconversion d'actifs |
| **AMO / PM** | Turner & Townsend, Archimage, Parella | Honoraires | Faible (obligation de moyens) | Élevé mais peu de capital | Prescription et pilotage |

**Points de méthode.** (1) La marge sur travaux d'un fit-out se situe en pratique entre 8 et 15 % du montant des travaux (ordre de grandeur de marché, à valider par liasse) et l'EBE publié n'en conserve que 3 à 7 % après frais de structure. (2) Les honoraires de conception et de pilotage sont rarement isolés dans les comptes : il faut les demander dans les propositions (décomposition « études / travaux / mobilier / honoraires »). (3) Pour mémoire, les ordres de grandeur de prix retenus sur ce site sont de 150 à 400 €/m² HT pour un rafraîchissement, 500 à 900 €/m² pour un aménagement standard et plus de 1 000 €/m² pour un projet haut de gamme.

## 7. Lecture tertiaire : quels acteurs pour quels projets

**Classement selon la grille de lecture tertiaire (top 15)**

{hipT}
### Typologie des projets et acteurs adaptés

| Type de projet | Acteurs les mieux positionnés | Pourquoi |
|---|---|---|
| Déploiement multi-sites ou grand siège (> 5 000 m²) | **Tétris**, **Kardham**, **Korus** | Couverture nationale, conception intégrée et capacité à mener plusieurs chantiers en parallèle ; Tétris est le plus solide financièrement (autonomie de 19 %, aucune dette) ; Korus est le seul à intégrer aussi la maintenance des sites. |
| Plateau de 150 à 2 000 m² en Île-de-France | **Isospace**, **Cicad** | PME rentables (marge d'EBE moyenne de 7 % et 6 %), sans endettement significatif ; capacité limitée à quelques chantiers importants en parallèle. |
| Achat de second œuvre en direct ou en contrat-cadre | **AGB**, **Spie batignolles Présance** | Production en propre ou TCE de petits travaux, ce qui supprime un étage de marge de CG ; Présance est adapté au site occupé. |
| Restructuration lourde d'immeuble parisien | **Pradeau Morin**, **OVGA** (conception + CG), **Eiffage Construction Tertiaire**, **Bouygues Bâtiment IDF** | Ingénierie de réhabilitation et capacité à porter des immeubles entiers ; Pradeau Morin reste fragile financièrement et OVGA ne publie pas ses comptes. |
| Reconversion d'actif obsolète | **Linkcity IDF**, **GA Smart Building** | Montage et conception-réalisation intégrés ; tous deux exposés au cycle de l'investissement. |
| Pilotage et contrôle des coûts | **Turner & Townsend**, **Archimage**, **Parella** | AMO et project management, sans portage du risque travaux. |

### Dynamiques concurrentielles

- **Intégration conseil + travaux.** JLL (avec Tétris) et CBRE (avec Turner & Townsend) assemblent transaction, conseil, project management et réalisation. Cette offre unique capte une part croissante des projets des grands utilisateurs.
- **Ensembliers.** Linkcity et GA intègrent le montage, la conception et le produit industrialisé, ce qui leur permet de proposer des immeubles ou plateaux « prêts à l'emploi ».
- **Pression sur les PME.** Le marché du fit-out reste fragmenté. Les PME rentables (Isospace, Cicad) sont des cibles naturelles de croissance externe, tandis que les hybrides conseil-CG fragiles (Parella) sont exposés.

**Points de contrôle pour un maître d'ouvrage avant contractualisation** (à partir des risques observés) : attestations décennale et RC, garantie de paiement des sous-traitants (loi de 1975), part de travaux sous-traités, BFR et délais fournisseurs (au-delà de 120 jours, signal de tension), retenue de garantie de 5 % et caution de restitution d'acompte.

## 8. Limites de l'étude et prochaines étapes

- **Panel raisonné.** Aucun classement officiel des « contractants généraux » n'existe : le périmètre retenu mélange CG, EG, fit-out et AMO, conformément à la méthode. Les grands groupes sont représentés par leurs filiales opérationnelles, pour éviter les doubles comptes. Certains acteurs du fit-out francilien de taille moyenne n'ont pu être identifiés avec certitude au registre et restent à ajouter (Majorelle, BW, Genesis Group).
- **Données financières.** Elles proviennent des comptes déposés (ratios normalisés INPI/BCE). Les comptes confidentiels (Kardham après 2022, OVGA après 2016) et les comptes consolidés manquants (groupe Korus) et les exercices manquants (Léon Grosse 2022) sont signalés. La part de sous-traitance et la répartition du CA par activité nécessitent les liasses complètes (Pappers, Infogreffe) ou un échange avec les entreprises.
- **Éléments qualitatifs.** Les références de chantiers, montants de contrats et parts de marchés publics sont marqués « non compilées » ou « à vérifier » quand aucune source primaire n'a été consultée. **Ils doivent être vérifiés avant tout usage externe.**
- **Prochaines étapes recommandées** : (1) achat ou extraction des liasses des 10 acteurs prioritaires ; (2) entretiens avec les principaux acteurs du fit-out (Tétris, Korus, Kardham, Isospace, OVGA, AGB) pour documenter marges sur travaux, honoraires et références ; (3) compléter le panel avec les acteurs de taille moyenne non identifiés au registre.
"""
open(os.path.join(OUT, "synthese-strategique.md"), "w").write(md)

readme = """# Étude : les principaux contractants généraux en France (octobre 2026)

L'étude suit une méthode en 8 axes : identité, activités, marchés, modèle économique, finances sur 5 ans, références, stratégie, risques et SWOT. Elle y ajoute une grille de lecture tertiaire : 5 critères notés et le rôle de chaque acteur dans l'écosystème des projets de bureaux.

## Livrables (3 niveaux)

1. **[Fiches entreprises](fiches/)** : """ + str(len(R)) + """ fiches standardisées (identité registre, comptes sur 5 ans, SWOT, grille de lecture tertiaire, notes).
2. **[Base comparative](base-comparative.xlsx)** : une ligne par entreprise, plus un onglet de séries financières sur 5 ans et un onglet de méthode (version [CSV](base-comparative.csv)).
3. **[Synthèse stratégique](synthese-strategique.md)** : classement, lecture par segment, cartographie concurrentielle, modèles économiques, lecture tertiaire et dynamiques concurrentielles.

## Sources

- Registre national des entreprises (INPI / INSEE), via l'API publique recherche-entreprises.api.gouv.fr : identité, dirigeants, établissements, tranche d'effectifs.
- Jeu de données « ratios_inpi_bce » (data.economie.gouv.fr), issu des comptes annuels déposés : CA, marge brute, EBE, EBIT, résultat net, BFR, délais clients et fournisseurs, autonomie financière, endettement.
- Sites, communiqués et presse spécialisée (GSE/GOLDBECK, JLL/Tétris, GA, NGE, Eiffage, etc.).

## Règles de méthode

- Une ligne = une entité juridique, sans addition entre filiales et groupes.
- Comptes sociaux (C) par défaut ; comptes consolidés (K) pour Léon Grosse, GSE et Quartus.
- La solidité est **calculée** à partir des comptes ; l'attractivité et le potentiel sont des **appréciations d'analyste**.
- Les mentions « à vérifier » ou « non compilées » signalent des éléments à consolider avant diffusion externe.

## Régénérer

Les scripts sont dans [`scripts/`](scripts/) : `fetch.py` (collecte registre + comptes à partir de `panel.json`), `qual.py` (éléments qualitatifs), `gen.py` (fiches, base et export `src/data/contractants.json` qui alimente les pages du site), `liens.py` (sites officiels et sources de presse) et `synth.py` (synthèse). Pour actualiser l'étude :

```bash
cd scripts && python3 fetch.py panel.json data.json && python3 gen.py .. ../../../src/data/contractants.json && python3 synth.py ..
```
"""
open(os.path.join(OUT, "README.md"), "w").write(readme)
print("ok")
