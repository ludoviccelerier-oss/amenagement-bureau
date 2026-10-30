# Étude : les principaux contractants généraux en France (octobre 2026)

L'étude suit une méthode en 8 axes : identité, activités, marchés, modèle économique, finances sur 5 ans, références, stratégie, risques et SWOT. Elle y ajoute une grille de lecture tertiaire : 5 critères notés et le rôle de chaque acteur dans l'écosystème des projets de bureaux.

## Livrables (3 niveaux)

1. **[Fiches entreprises](fiches/)** : 42 fiches standardisées (identité registre, comptes sur 5 ans, SWOT, grille de lecture tertiaire, notes).
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
