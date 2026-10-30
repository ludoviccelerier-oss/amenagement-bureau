import json, os, csv, sys
sys.path.insert(0, os.path.dirname(__file__))
from qual import Q
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

OUT = sys.argv[1]
D = json.load(open(os.path.join(os.path.dirname(__file__), "data.json")))
P = json.load(open(os.path.join(os.path.dirname(__file__), "panel.json")))
SEG = {"A": "Majors et entreprises générales", "B": "Contractants généraux clé en main / ensembliers",
       "C": "Fit-out et design & build tertiaire", "D": "AMO / project management (benchmark)"}
TRANCHE = {"00": (0, "0"), "01": (1.5, "1-2"), "02": (4, "3-5"), "03": (7.5, "6-9"), "11": (15, "10-19"), "12": (35, "20-49"),
           "21": (75, "50-99"), "22": (150, "100-199"), "31": (225, "200-249"), "32": (375, "250-499"), "41": (750, "500-999"),
           "42": (1500, "1 000-1 999"), "51": (3500, "2 000-4 999"), "52": (7500, "5 000-9 999"), "53": (10000, "10 000 +")}
CONSO = {"745420653", "488862368", "821143039"}  # groupes publiant des comptes consolidés (K)

def series(siren, typ):
    rs = [r for r in D[siren]["ratios"] if r.get("type_bilan") == typ]
    seen = {}
    for r in sorted(rs, key=lambda r: r["date_cloture_exercice"], reverse=True):
        y = r["date_cloture_exercice"][:4]
        if y not in seen and (r.get("chiffre_d_affaires") or 0) > 0 and int(y) >= 2020:  # exercices antérieurs à 2020 jugés obsolètes
            seen[y] = r
    return [seen[y] for y in sorted(seen)][-5:]

def m(v):  # M€
    return None if v is None else v / 1e6

def f1(v, suf=""):
    return "n.d." if v is None else f"{v:,.1f}".replace(",", " ").replace(".", ",") + suf

def pct(a, b):
    return None if not a or b is None else (b / a - 1) * 100

rows = []
for siren, name, seg in P:
    q = Q[siren]
    main = series(siren, "K") if siren in CONSO else series(siren, "C")
    soc = series(siren, "C")
    last = main[-1] if main else {}
    first = main[0] if main else {}
    ident = D[siren]["ident"]; siege = ident.get("siege", {})
    tr = ident.get("tranche_effectif_salarie")
    eff_mid, eff_lbl = TRANCHE.get(tr, (None, "n.d."))
    ca = m(last.get("chiffre_d_affaires")); ebe = m(last.get("ebe")); rn = m(last.get("resultat_net"))
    n = len(main)
    cagr = ((last["chiffre_d_affaires"] / first["chiffre_d_affaires"]) ** (1 / (int(last["date_cloture_exercice"][:4]) - int(first["date_cloture_exercice"][:4]))) - 1) * 100 if n >= 2 and int(last["date_cloture_exercice"][:4]) > int(first["date_cloture_exercice"][:4]) else None
    yoy = pct(main[-2]["chiffre_d_affaires"], last["chiffre_d_affaires"]) if n >= 2 else None
    me = [r.get("marge_ebe") for r in main[-3:] if r.get("marge_ebe") is not None]
    me3 = sum(me) / len(me) if me else None
    af = last.get("autonomie_financiere")
    pos_rn = sum(1 for r in main if (r.get("resultat_net") or 0) > 0)
    # Solidité (1-5) : autonomie financière, marge d'EBE moyenne 3 ans, régularité du résultat net
    s = 0
    s += 2 if (af or 0) >= 15 else 1 if (af or 0) >= 7 else 0
    s += 2 if (me3 or 0) >= 4 else 1 if (me3 or 0) >= 1.5 else 0
    s += 1 if n and pos_rn == n else 0
    sol = max(1, min(5, s)) if main else None
    hip = q["hip"]
    hip_score = round((hip["tert"] + hip["acces"] + hip["real"] + hip["marge"] + hip["fin"]) / 5, 1)
    notes = [q["attr"], q["pot"]] + ([sol] if sol else [])
    global_score = round(sum(notes) / len(notes), 1)
    rows.append(dict(siren=siren, name=name, seg=seg, q=q, main=main, soc=soc, last=last, ident=ident, siege=siege,
                     eff_mid=eff_mid, eff_lbl=eff_lbl, eff_year=ident.get("annee_tranche_effectif_salarie"), ca=ca, ebe=ebe, rn=rn,
                     cagr=cagr, yoy=yoy, me3=me3, af=af, sol=sol, hip_score=hip_score, global_score=global_score,
                     conso=siren in CONSO, year=last.get("date_cloture_exercice", "")[:7]))

rows.sort(key=lambda r: -(r["ca"] or 0))
for i, r in enumerate(rows, 1):
    r["rank"] = i

os.makedirs(os.path.join(OUT, "fiches"), exist_ok=True)

def fin_table(rs, title):
    if not rs:
        return f"*{title} : aucune donnée publiée.*\n"
    hdr = "| Indicateur | " + " | ".join(r["date_cloture_exercice"][:7] for r in rs) + " |\n|---|" + "---:|" * len(rs) + "\n"
    def line(lbl, fn):
        return f"| {lbl} | " + " | ".join(fn(r, i) for i, r in enumerate(rs)) + " |\n"
    g = lambda r, i: f1(pct(rs[i - 1]["chiffre_d_affaires"], r["chiffre_d_affaires"]), " %") if i > 0 else "–"
    t = f"**{title}**\n\n" + hdr
    t += line("Chiffre d'affaires (M€)", lambda r, i: f1(m(r["chiffre_d_affaires"])))
    t += line("Croissance du CA", g)
    t += line("Marge brute (M€)", lambda r, i: f1(m(r.get("marge_brute"))))
    t += line("EBE (M€)", lambda r, i: f1(m(r.get("ebe"))))
    t += line("Marge d'EBE", lambda r, i: f1(r.get("marge_ebe"), " %"))
    t += line("Résultat d'exploitation (EBIT, M€)", lambda r, i: f1(m(r.get("ebit"))))
    t += line("Résultat net (M€)", lambda r, i: f1(m(r.get("resultat_net"))))
    t += line("Marge nette", lambda r, i: f1(r["resultat_net"] / r["chiffre_d_affaires"] * 100 if r.get("resultat_net") is not None else None, " %"))
    t += line("CAF / CA", lambda r, i: f1(r.get("caf_sur_ca"), " %"))
    t += line("BFR d'exploitation (jours de CA)", lambda r, i: f1(r.get("poids_bfr_exploitation_sur_ca_jours")))
    t += line("Crédit clients (jours)", lambda r, i: f1(r.get("credit_clients_jours")))
    t += line("Crédit fournisseurs (jours)", lambda r, i: f1(r.get("credit_fournisseurs_jours")))
    t += line("Autonomie financière (FP / total bilan)", lambda r, i: f1(r.get("autonomie_financiere"), " %"))
    t += line("Taux d'endettement (dettes fin. / FP)", lambda r, i: f1(r.get("taux_d_endettement"), " %"))
    return t + "\n"

def stars(n):
    return "n.d." if n is None else "●" * int(n) + "○" * (5 - int(n))

for r in rows:
    q = r["q"]; h = q["hip"]; s = r["siege"]; ident = r["ident"]
    dirs = [d for d in (ident.get("dirigeants") or []) if (d.get("qualite") or "").lower().find("commissaire") < 0][:4]
    dir_txt = "; ".join(((d.get("prenoms") or "").split(" ")[0].title() + " " + (d.get("nom") or "").title()).strip() + f" ({d.get('qualite')})" if d.get("nom") else f"{d.get('denomination')} ({d.get('qualite')})" for d in dirs) or "n.d."
    cap = [d.get("denomination") for d in (ident.get("dirigeants") or []) if "Commissaire" in (d.get("qualite") or "") and d.get("denomination")]
    caps = ", ".join(cap[:2]) or "n.d."
    caps_sal = f"{r['ca'] / r['eff_mid'] * 1000:,.0f} k€".replace(",", " ") if r["ca"] and r["eff_mid"] else "n.d."
    md = f"""# {r['rank']:02d}. {r['name']}

> **Segment** : {SEG[r['seg']]} · **Positionnement** : {q['pos']}
> **SIREN** {r['siren']} · **Dernier exercice** {r['year'] or 'aucun publié depuis 2020'} · **CA** {f1(r['ca'])} M€{' (consolidé)' if r['conso'] else ''} · **Note globale** {r['global_score']}/5

| Attractivité | Solidité financière (calculée) | Potentiel stratégique | Score tertiaire |
|:-:|:-:|:-:|:-:|
| {stars(q['attr'])} {q['attr']}/5 | {stars(r['sol'])}{'' if r['sol'] is None else ' ' + str(r['sol']) + '/5'} | {stars(q['pot'])} {q['pot']}/5 | {r['hip_score']}/5 |

## 1. Identité et profil

| | |
|---|---|
| Raison sociale | {ident.get('nom_complet', r['name'])} |
| Création (immatriculation de l'entité) | {ident.get('date_creation') or 'n.d.'} |
| Siège | {s.get('adresse', 'n.d.')} |
| Établissements ouverts | {ident.get('nombre_etablissements_ouverts', 'n.d.')} |
| Catégorie INSEE | {ident.get('categorie_entreprise') or 'n.d.'} |
| Code NAF | {s.get('activite_principale', 'n.d.')} |
| Effectif (tranche INSEE) | {r['eff_lbl']} salariés ({r['eff_year'] or 'année n.d.'}) |
| Dirigeants (registre) | {dir_txt} |
| Commissaires aux comptes | {caps} |

**Actionnariat et groupe.** {q['groupe']}

**Historique et étapes clés.** {q['histo']}

**Positionnement.** {q['pos']}.

## 2. Activités et offre de services

- **Typologie de travaux** : {q['activ']}
- **Niveau d'intégration (internalisé ou sous-traité)** : {q['integ']}
- **Offre clé en main, engagements et offres complémentaires** : {q['offre']}

## 3. Positionnement commercial et marchés

- **Segments clients** : {q['clients']}
- **Typologie d'actifs** : {q['actifs']}
- **Taille moyenne des projets** : {q['taille']}
- **Couverture géographique** : {q['geo']}
- **Positionnement prix** : {q['prix']}

## 4. Modèle économique

{q['modele']}

*Point de vigilance méthodologique* : dans les comptes sociaux, la sous-traitance est enregistrée en « autres achats et charges externes ». Une marge brute proche du CA ne signale donc pas une forte valeur ajoutée. La part de sous-traitance doit se lire dans la liasse fiscale (comptes 604/611). Le CA publié par un contractant général inclut en principe 100 % des travaux sous-traités.

## 5. Performances financières

{fin_table(r['main'], 'Comptes consolidés du groupe (type K)' if r['conso'] else 'Comptes sociaux de l’entité (type C)')}{fin_table(r['soc'], 'Comptes sociaux de la société tête (type C), pour comparaison') if r['conso'] else ''}
- **TCAM du CA sur la période** : {f1(r['cagr'], ' %')} · **Croissance sur le dernier exercice** : {f1(r['yoy'], ' %')}
- **CA par salarié (approximation sur le milieu de la tranche d'effectif)** : {caps_sal}
- **Marge d'EBE moyenne sur 3 ans** : {f1(r['me3'], ' %')}

## 6. Références et capacité d'exécution

{q['refs']} Le registre recense {ident.get('nombre_etablissements_ouverts', 'n.d.')} établissement(s) ouvert(s), ce qui donne un indicateur de capacité multi-chantiers. Sinistralité et litiges : aucune procédure collective n'apparaît dans le registre à la date de collecte (BODACC à contrôler).

## 7. Stratégie et avantages concurrentiels

{q['strat']}

## 8. Risques, perspectives et SWOT

**Risques.** {q['risques']}

| Forces | Faiblesses |
|---|---|
| {q['F']} | {q['Fa']} |
| **Opportunités** | **Menaces** |
| {q['O']} | {q['M']} |

## Grille de lecture tertiaire

| Critère | Note |
|---|:-:|
| Expertise tertiaire (plateaux, actifs vacants) | {h['tert']}/5 |
| Accès aux donneurs d'ordre (foncières, AM, PM, utilisateurs) | {h['acces']}/5 |
| Capacité de réalisation (volumes, multi-sites) | {h['real']}/5 |
| Modèle de marge (services, honoraires, récurrence) | {h['marge']}/5 |
| Capacité financière (portage de travaux, décalages d'encaissement) | {h['fin']}/5 |
| **Rôle dans l'écosystème tertiaire** | **{h['role']}** |

## Note de synthèse

Attractivité **{q['attr']}/5** · solidité **{'non évaluable (comptes non publiés)' if r['sol'] is None else str(r['sol']) + '/5'}** · potentiel **{q['pot']}/5**, soit une note globale de **{r['global_score']}/5**.

---
*Sources : registre national des entreprises (INPI/INSEE, API recherche-entreprises), jeu de données « ratios_inpi_bce » (comptes déposés, data.economie.gouv.fr), sites et communiqués des entreprises, presse spécialisée. Données collectées le 29/10/2026. Les éléments qualitatifs marqués « à vérifier » ou « non compilées » doivent être consolidés avant tout usage externe.*
"""
    open(os.path.join(OUT, "fiches", f"{r['rank']:02d}-{q['slug']}.md"), "w").write(md)

# ---------- Base comparative (xlsx + csv) ----------
cols = ["Rang", "Entreprise", "SIREN", "Segment", "Positionnement", "Groupe / actionnariat", "Siège", "Création entité", "Effectif (tranche)",
        "Dernier exercice", "Type comptes", "CA (M€)", "Croissance N-1 (%)", "TCAM période (%)", "EBE (M€)", "Marge EBE (%)", "Marge EBE moy. 3 ans (%)",
        "Résultat net (M€)", "Marge nette (%)", "CA/salarié approx. (k€)", "BFR (jours CA)", "Crédit clients (j)", "Crédit fournisseurs (j)",
        "Autonomie financière (%)", "Endettement (%)", "Segments clients", "Actifs", "Géographie", "Prix", "Expertise tertiaire", "Accès donneurs d'ordre",
        "Capacité réalisation", "Modèle de marge", "Capacité financière", "Score tertiaire", "Rôle écosystème tertiaire", "Attractivité", "Solidité", "Potentiel", "Note globale"]
data = []
for r in rows:
    L = r["last"]; q = r["q"]; h = q["hip"]
    data.append([r["rank"], r["name"], r["siren"], SEG[r["seg"]], q["pos"], q["groupe"][:160], r["siege"].get("libelle_commune"), r["ident"].get("date_creation"), r["eff_lbl"],
                 r["year"], "Consolidés" if r["conso"] else "Sociaux", round(r["ca"], 1) if r["ca"] else None, round(r["yoy"], 1) if r["yoy"] is not None else None,
                 round(r["cagr"], 1) if r["cagr"] is not None else None, round(r["ebe"], 1) if r["ebe"] is not None else None,
                 round(L.get("marge_ebe"), 1) if L.get("marge_ebe") is not None else None, round(r["me3"], 1) if r["me3"] is not None else None,
                 round(r["rn"], 1) if r["rn"] is not None else None, round(r["rn"] / r["ca"] * 100, 1) if r["ca"] and r["rn"] is not None else None,
                 round(r["ca"] / r["eff_mid"] * 1000) if r["ca"] and r["eff_mid"] else None,
                 round(L.get("poids_bfr_exploitation_sur_ca_jours"), 0) if L.get("poids_bfr_exploitation_sur_ca_jours") is not None else None,
                 round(L.get("credit_clients_jours"), 0) if L.get("credit_clients_jours") is not None else None,
                 round(L.get("credit_fournisseurs_jours"), 0) if L.get("credit_fournisseurs_jours") is not None else None,
                 round(r["af"], 1) if r["af"] is not None else None, round(L.get("taux_d_endettement"), 1) if L.get("taux_d_endettement") is not None else None,
                 q["clients"], q["actifs"], q["geo"], q["prix"], h["tert"], h["acces"], h["real"], h["marge"], h["fin"], r["hip_score"], h["role"],
                 q["attr"], r["sol"], q["pot"], r["global_score"]])

with open(os.path.join(OUT, "base-comparative.csv"), "w", newline="") as fh:
    w = csv.writer(fh, delimiter=";"); w.writerow(cols); w.writerows(data)

wb = Workbook()
ws = wb.active; ws.title = "Base comparative"
ws.append(cols)
for d in data: ws.append(d)
hdr_fill = PatternFill("solid", fgColor="1F3A5F")
for c in ws[1]:
    c.font = Font(bold=True, color="FFFFFF"); c.fill = hdr_fill; c.alignment = Alignment(wrap_text=True, vertical="center")
ws.row_dimensions[1].height = 45
for i, col in enumerate(cols, 1):
    ws.column_dimensions[get_column_letter(i)].width = 34 if col in ("Positionnement", "Groupe / actionnariat", "Segments clients", "Actifs", "Rôle écosystème tertiaire") else 13
ws.freeze_panes = "C2"; ws.auto_filter.ref = ws.dimensions

ws2 = wb.create_sheet("Séries 5 ans")
ws2.append(["Entreprise", "SIREN", "Type", "Clôture", "CA (M€)", "Marge brute (M€)", "EBE (M€)", "Marge EBE (%)", "EBIT (M€)", "Résultat net (M€)", "CAF/CA (%)",
            "BFR (j)", "Clients (j)", "Fournisseurs (j)", "Autonomie fin. (%)", "Endettement (%)", "Liquidité"])
for r in rows:
    for typ, rs in (("K", r["main"]) if r["conso"] else ("C", r["main"]),) + ((("C", r["soc"]),) if r["conso"] else ()):
        for x in rs:
            ws2.append([r["name"], r["siren"], typ, x["date_cloture_exercice"], *(round(m(x.get(k)), 2) if x.get(k) is not None else None for k in ("chiffre_d_affaires", "marge_brute", "ebe")),
                        x.get("marge_ebe"), round(m(x.get("ebit")), 2) if x.get("ebit") is not None else None, round(m(x.get("resultat_net")), 2) if x.get("resultat_net") is not None else None,
                        x.get("caf_sur_ca"), x.get("poids_bfr_exploitation_sur_ca_jours"), x.get("credit_clients_jours"), x.get("credit_fournisseurs_jours"),
                        x.get("autonomie_financiere"), x.get("taux_d_endettement"), x.get("ratio_de_liquidite")])
for c in ws2[1]:
    c.font = Font(bold=True, color="FFFFFF"); c.fill = hdr_fill
ws2.freeze_panes = "C2"; ws2.auto_filter.ref = ws2.dimensions
for i in range(1, 18): ws2.column_dimensions[get_column_letter(i)].width = 14
ws2.column_dimensions["A"].width = 38

ws3 = wb.create_sheet("Méthode")
for line in ["Panel : " + str(len(rows)) + " entités juridiques françaises actives en contractant général, entreprise générale, fit-out ou AMO, classées par CA du dernier exercice publié.",
             "Comptes : jeu « ratios_inpi_bce » (data.economie.gouv.fr), issu des comptes déposés à l'INPI. Type C = comptes sociaux, K = comptes consolidés.",
             "Règle de non-double compte : chaque ligne correspond à une entité juridique ; ne pas additionner une filiale et son groupe (ex. Ossabois dans GA, Linkcity et les filiales régionales dans Bouygues Construction).",
             "Effectifs : tranche INSEE ; le CA par salarié est calculé sur le milieu de la tranche et reste un ordre de grandeur.",
             "Solidité (1-5), calculée : autonomie financière (≥15 % → 2 pts ; ≥7 % → 1 pt), marge d'EBE moyenne sur 3 ans (≥4 % → 2 ; ≥1,5 % → 1), résultat net positif sur toute la période (+1).",
             "Attractivité et potentiel : appréciation d'analyste (1-5). Grille de lecture tertiaire : 5 critères notés de 1 à 5 + rôle dans l'écosystème.",
             "Part de sous-traitance : non disponible dans les ratios publics ; à extraire des liasses (comptes 604/611)."]:
    ws3.append([line])
ws3.column_dimensions["A"].width = 160
wb.save(os.path.join(OUT, "base-comparative.xlsx"))

json.dump([{k: v for k, v in r.items() if k in ("rank", "name", "siren", "seg", "ca", "yoy", "cagr", "ebe", "me3", "rn", "af", "sol", "hip_score", "global_score", "year", "conso")}
           | {"slug": r["q"]["slug"], "role": r["q"]["hip"]["role"], "attr": r["q"]["attr"], "pot": r["q"]["pot"], "tert": r["q"]["hip"]["tert"],
              "bfr": r["last"].get("poids_bfr_exploitation_sur_ca_jours"), "eff": r["eff_lbl"], "pos": r["q"]["pos"]} for r in rows],
          open(os.path.join(os.path.dirname(__file__), "rows.json"), "w"), ensure_ascii=False, indent=0)
print("ok", len(rows))

# ---------- Export pour le site (src/data/contractants.json) ----------
if len(sys.argv) > 2:
    import re
    from liens import SITES, PRESSE

    def propre(txt):  # retire les mentions de travail interne avant publication
        return re.sub(r"\s*\(((détail )?non compilé(e)?s?( en détail)?)\)", "", txt).strip()

    def serie(rs):
        out = []
        for i, x in enumerate(rs):
            ca_ = m(x["chiffre_d_affaires"])
            out.append(dict(exercice=x["date_cloture_exercice"][:7], ca=ca_,
                            croissance=pct(rs[i - 1]["chiffre_d_affaires"], x["chiffre_d_affaires"]) if i else None,
                            margeBrute=m(x.get("marge_brute")), ebe=m(x.get("ebe")), margeEbe=x.get("marge_ebe"), ebit=m(x.get("ebit")),
                            rn=m(x.get("resultat_net")), margeNette=(x["resultat_net"] / x["chiffre_d_affaires"] * 100) if x.get("resultat_net") is not None else None,
                            caf=x.get("caf_sur_ca"), bfr=x.get("poids_bfr_exploitation_sur_ca_jours"), clients=x.get("credit_clients_jours"),
                            fournisseurs=x.get("credit_fournisseurs_jours"), autonomie=x.get("autonomie_financiere"), endettement=x.get("taux_d_endettement")))
        return out

    export = []
    for r in rows:
        q = r["q"]; ident = r["ident"]; s = r["siege"]; siren = r["siren"]
        dirs = [d for d in (ident.get("dirigeants") or []) if "commissaire" not in (d.get("qualite") or "").lower()][:4]
        site_ = SITES.get(siren)
        refs = propre(q["refs"])
        export.append(dict(
            rang=r["rank"], slug=q["slug"], nom=r["name"], siren=siren, segment=r["seg"], segmentNom=SEG[r["seg"]], positionnement=q["pos"],
            site=dict(label=site_[0], url=site_[1]) if site_ else None,
            identite=dict(raison=ident.get("nom_complet", r["name"]), creation=ident.get("date_creation"), adresse=s.get("adresse"),
                          etablissements=ident.get("nombre_etablissements_ouverts"), categorie=ident.get("categorie_entreprise"), naf=s.get("activite_principale"),
                          effectif=r["eff_lbl"], effectifAnnee=r["eff_year"],
                          dirigeants=[(((d.get("prenoms") or "").split(" ")[0].title() + " " + (d.get("nom") or "").title()).strip() if d.get("nom") else d.get("denomination")) + f" ({d.get('qualite')})" for d in dirs],
                          cac=[d.get("denomination") for d in (ident.get("dirigeants") or []) if "Commissaire" in (d.get("qualite") or "") and d.get("denomination")][:2]),
            texte={k: propre(q[k]) for k in ("groupe", "histo", "activ", "integ", "offre", "clients", "actifs", "taille", "geo", "prix", "modele", "strat", "risques", "F", "Fa", "O", "M")}
                  | dict(refs="" if refs.lower().startswith("non compil") else refs),
            comptes=dict(type="consolidés" if r["conso"] else "sociaux", principal=serie(r["main"]), societe=serie(r["soc"]) if r["conso"] else []),
            indicateurs=dict(exercice=r["year"] or None, ca=r["ca"], croissance=r["yoy"], tcam=r["cagr"], margeEbe3=r["me3"], autonomie=r["af"],
                             bfr=r["last"].get("poids_bfr_exploitation_sur_ca_jours"), caParSalarie=round(r["ca"] / r["eff_mid"] * 1000) if r["ca"] and r["eff_mid"] else None),
            notes=dict(attractivite=q["attr"], solidite=r["sol"], potentiel=q["pot"], globale=r["global_score"], tertiaire=r["hip_score"]),
            grille=dict(q["hip"]),
            sources=[dict(label=f"Annuaire des entreprises (État) : fiche {r['name']}", url=f"https://annuaire-entreprises.data.gouv.fr/entreprise/{siren}"),
                     dict(label=f"Pappers : comptes et documents de {r['name']}", url=f"https://www.pappers.fr/entreprise/{siren}"),
                     *[dict(label=a, url=b) for a, b in PRESSE.get(siren, [])]],
        ))
    json.dump(export, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
    print("export site", len(export))
