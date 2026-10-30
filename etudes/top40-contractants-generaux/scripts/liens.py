# Sites officiels (vérifiés le 29/10/2026) et sources de presse par SIREN.
# Un site de groupe est indiqué quand la filiale n'a pas de site propre.

BOUYGUES = ("Bouygues Construction (site du groupe)", "https://www.bouygues-construction.com")
EIFFAGE = ("Eiffage (site du groupe)", "https://www.eiffage.com")
VINCI = ("VINCI Construction (site du groupe)", "https://vinci-construction.com/fr/")
FAYAT = ("Groupe Fayat (site du groupe)", "https://www.fayat.com")
SPIE = ("Spie batignolles (site du groupe)", "https://www.spiebatignolles.fr")
KARDHAM = ("Groupe Kardham", "https://www.kardham.com")

SITES = {
    "433900834": BOUYGUES, "731620316": BOUYGUES, "321006892": BOUYGUES, "310505748": BOUYGUES, "758801906": BOUYGUES,
    "745420653": ("Léon Grosse", "https://www.leongrosse.fr"),
    "790843411": ("Demathieu Bard", "https://www.demathieu-bard.fr"),
    "407794551": ("GCC Groupe", "https://www.gcc-groupe.com"),
    "493414304": VINCI, "444454326": VINCI,
    "780109856": FAYAT, "321057978": FAYAT,
    "791308836": EIFFAGE, "353286065": EIFFAGE, "791261399": EIFFAGE, "408063436": EIFFAGE,
    "808698880": ("Pradeau Morin", "https://www.pradeau-morin.com"),
    "389612383": ("Rabot Dutilleul", "https://www.rabotdutilleul.com"),
    "582014957": SPIE, "332265032": SPIE,
    "445950074": ("Groupe Ramery", "https://www.ramery.fr"),
    "950033555": ("NGE", "https://www.nge.fr"),
    "925520108": ("Brézillon", "https://www.brezillon.fr"),
    "314209628": ("Groupe Legendre", "https://www.groupe-legendre.com"),
    "488862368": ("GSE", "https://www.gsegroup.com"),
    "428266035": ("GA Smart Building", "https://www.ga.fr"),
    "343183331": ("Linkcity", "https://www.linkcity.com"),
    "308575158": ("Briand", "https://www.briand.fr"),
    "444204374": ("Groupe Elcimaï", "https://www.elcimai.com"),
    "392089934": ("Ossabois", "https://www.ossabois.fr"),
    "444713515": ("Tétris", "https://www.tetris-db.com/fr/"),
    "384407896": KARDHAM, "443422506": KARDHAM,
    "411892607": ("Isospace", "https://www.isospace.fr"),
    "518504493": ("Parella", "https://parella-group.fr"),
    "378184378": ("Archimage", "https://archimage.fr/fr"),
    "537590390": ("Turner & Townsend", "https://www.turnerandtownsend.com"),
    "383381365": ("Korus Group", "https://www.korusgroup.com/fr"),
    "801389156": ("OVGA", "https://ovga.fr"),
}

JDE = "Le Journal des entreprises"
PRESSE = {
    "488862368": [
        (f"{JDE} : l'Avignonnais GSE repris par l'Allemand Goldbeck", "https://www.lejournaldesentreprises.com/breve/lavignonnais-gse-repris-par-lallemand-goldbeck-169226"),
        ("Communiqué GSE : Goldbeck acquiert 100 % du capital (2019)", "https://galivel.com/media/files/190326__cp_gse___changement_actionnariat___goldbeck_vok-1.pdf"),
        ("Communiqué GSE : rachat de DS Gruppen (2022)", "https://galivel.com/media/files/20220628_cpgse_rachat_dsgruppen.pdf"),
        ("Communiqué GSE : un chiffre d'affaires supérieur au milliard d'euros (2023)", "https://www.galivel.com/media/files/230411_cpgse_milliard.pdf"),
        ("Communiqué GSE : ouverture d'une agence en Nouvelle-Aquitaine (2023)", "https://galivel.com/media/files/20230928_cp_gse_ouverture_agence_nouvelle_aquitaine-2.pdf"),
        ("Communiqué GSE : acquisition de Critical Building, data centers (2025)", "https://www.galivel.com/media/files/20251003_cpgse_annonce_acquisition_critical_building_data_centers-1.pdf"),
        ("Immobilien Zeitung : Goldbeck takes over French GSE Group", "https://www.iz.de/translatednews/news/-goldbeck-takes-over-french-gse-group-1000560472"),
    ],
    "444713515": [
        ("JLL : Tétris ouvre une antenne à Rennes", "https://www.jll.com/fr-fr/newsroom/ouverture-nouvelle-antenne-tetris-rennes"),
        ("JLL : Amandine Chizelle à la tête du hub lillois de JLL et Tétris", "https://www.jll.com/fr-fr/newsroom/amandine-chizelle-nommee-a-la-tete-du-hub-lillois-de-jll-et-de-t"),
        ("Defense-92 : Tétris s'offre un showroom au sommet de la tour Aurore", "https://www.defense-92.fr/immobilier/tetris-soffre-un-joli-showroom-au-sommet-de-la-tour-aurore-83270"),
        ("GPO Magazine : Tétris, acteur historique de l'aménagement de bureaux", "https://www.gpomag.fr/tetris-acteur-historique-de-l-amenagement-de-bureaux/"),
        ("Bien-être au travail : top 5 des entreprises d'aménagement de bureaux à Paris", "https://www.bienetretravail.fr/amenagement-bureaux-paris-entreprises/"),
    ],
    "384407896": [("Bien-être au travail : top 5 des entreprises d'aménagement de bureaux à Paris", "https://www.bienetretravail.fr/amenagement-bureaux-paris-entreprises/")],
    "411892607": [("Bien-être au travail : top 5 des entreprises d'aménagement de bureaux à Paris", "https://www.bienetretravail.fr/amenagement-bureaux-paris-entreprises/")],
    "518504493": [("Bien-être au travail : top 5 des entreprises d'aménagement de bureaux à Paris", "https://www.bienetretravail.fr/amenagement-bureaux-paris-entreprises/")],
    "950033555": [(f"{JDE} : NGE franchit les 5 milliards d'euros de chiffre d'affaires en 2025", "https://www.lejournaldesentreprises.com/breve/nge-franchit-les-5-milliards-deuros-de-chiffre-daffaires-en-2025-2140064")],
    "428266035": [
        ("Le Monde du Droit : entrée d'Eurazeo au capital de GA Smart Building", "https://www.lemondedudroit.fr/deals/100613-mcdermott-will-schulte-conseille-eurazeo-lors-de-son-entree-au-capital-de-ga-smart-building.html"),
        (f"{JDE} : le roi du béton GA se met au bois (rachat d'Ossabois)", "https://www.lejournaldesentreprises.com/article/le-roi-du-beton-ga-se-met-au-bois-114772"),
        (f"{JDE} : GA Smart Building prend pied dans le Grand Paris", "https://www.lejournaldesentreprises.com/article/ga-smart-building-prend-pied-dans-le-grand-paris-152413"),
        (f"{JDE} : GA Smart Building lance son futur siège bas carbone", "https://www.lejournaldesentreprises.com/article/ga-smart-building-lance-les-travaux-de-son-futur-siege-social-bas-carbone-2046310"),
        ("Tekla BIM Awards : campus Thales à Bordeaux", "https://www.tekla.com/fr/bim-awards/thales-campus-bordeaux"),
    ],
    "392089934": [(f"{JDE} : le roi du béton GA se met au bois (rachat d'Ossabois)", "https://www.lejournaldesentreprises.com/article/le-roi-du-beton-ga-se-met-au-bois-114772")],
    "383381365": [
        (f"{JDE} : Korus Group veut décarboner les bureaux de ses clients", "https://www.lejournaldesentreprises.com/auvergne-rhone-alpes/article/korus-group-veut-decarboner-les-bureaux-de-ses-clients-2058625"),
        (f"{JDE} : Korus Group confie sa direction générale à Michele Serra", "https://www.lejournaldesentreprises.com/article/korus-group-confie-sa-direction-generale-michele-serra-pour-accelerer-linternational-2138984"),
        (f"{JDE} : Thomas Velty prend la tête de Korus France", "https://www.lejournaldesentreprises.com/breve/lalsacien-thomas-velty-prend-la-tete-de-korus-france-1835140"),
        (f"{JDE} : Korus Group ouvre un showroom mobilier à Lille", "https://www.lejournaldesentreprises.com/breve/korus-group-ouvre-un-showroom-mobilier-lille-2063345"),
        ("Tendance Hôtellerie : Korus s'installe à Dijon", "https://www.tendancehotellerie.fr/articles-breves/communique-de-presse/12194-article/korus-s-installe-a-dijon"),
    ],
    "801389156": [
        ("OVGA : présentation et réalisations", "https://ovga.fr/"),
        ("OVGA Lab : l'IA appliquée au bâtiment", "https://ovga.fr/lab"),
    ],
    "791308836": [("Construction Briefing : résultats d'Eiffage", "https://www.constructionbriefing.com/news/eiffage-reports-steady-contracting-growth-buoyed-by-european-markets/8084164.article")],
}
