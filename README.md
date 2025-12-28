
                                            Arborescence de notre projet : 


Dashboard_Global_education/
│
├── assets/                       # Ressources visuelles : CSS automatiquement chargé par Dash
│   └── style.css
│   ├── images/                   # Captures d’écran du dashboard
│
├── data/                         # Dossier des données
│   │
│   ├── cleaned/                  # Données nettoyées prêtes à l’analyse
│   │   └── cleaned_data.csv
│   │
│   ├── data_geo/                 # Données géographiques (Shapefile Natural Earth)
│   │   ├── ne_50m_admin_0_countries.cpg
│   │   ├── ne_50m_admin_0_countries.dbf
│   │   ├── ne_50m_admin_0_countries.prj
│   │   ├── ne_50m_admin_0_countries.README.html
│   │   ├── ne_50m_admin_0_countries.shp
│   │   └── ne_50m_admin_0_countries.shx
│   │
│   └── raw/                      # Données brutes (CSV sources)
│       ├── 1-basic-education.csv
│       ├── 2-lays.csv
│       ├── 3-nbr_out_school_children.csv
│       └── 4-gender-gap-educ-levels.csv
│
├── src/                          # Code source du dashboard
│   ├── __init__.py               # Rend le dossier src importable
│   │
│   ├── components/               # Composants visuels : graphiques, histogrammes, variables
│   │   ├── __init__.py
│   │   ├── graph_diag_hist.py    # Fonctions générant les graphiques
│   │   └── variables.py          # Définition des constantes et noms de colonnes
│   │
│   ├── pages/                    # Structure des pages de l'application
│   │   ├── __init__.py
│   │   └── home.py               # Page d’accueil
│   │
│   └── utils/                    # Outils de préparation des données
│       ├── __init__.py
│       ├── clean_data.py         # Nettoyage et préparation (Pandas)
│       └── get_data.py           # Chargement et fusion des données
│
├── .gitignore                    # Fichiers exclus du dépôt (venv, cache…)
├── config.py                     # Paramètres globaux de l’application
├── main.py                       # Fichier principal — lance le dashboard
├── README.md                     # Documentation du projet
└── requirements.txt              # Bibliothèques Python nécessaires


                                            🌍 Dashboard Global Education

Notre dashboard conciste en un projet de visualisation interactive de données éducatives mondiales.

I. Présentation générale du projet

Ce projet a pour objectif de concevoir et développer un dashboard interactif permettant l’exploration d’indicateurs relatifs à l’éducation à l’échelle mondiale.
Il s’inscrit dans le cadre d’un travail académique visant à manipuler, analyser et représenter des données à l’aide d’outils professionnels de data science.

Notre dashboard permet notamment :

- la visualisation d’indicateurs éducatifs globaux ;

- l’analyse comparative entre pays ;

- l’identification d’inégalités régionales ;

- la représentation spatiale via une carte du monde ;

- l’utilisation de graphiques interactifs basés sur des données réelles.

Elle repose principalement sur :

- Python pour le traitement et la manipulation des données ;

- Dash et Plotly pour la visualisation interactive ;

- Pandas pour la structuration et la préparation des jeux de données ;

- un shapefile géographique pour la dimension cartographique.


II. Manuel d’utilisation (User Guide)

1. Prérequis

Pour exécuter l’application, l’utilisateur doit disposer :

- d’une version de Python 3.10 ou supérieure ;

- de Git ;

- d’un navigateur web récent.

Une fois le projet installé, aucune connexion internet n’est requise puisque les données sont stockées localement.

2. Installation du projet

Étape 1 – Clonage du dépôt
Le projet doit être cloné depuis GitHub puis ouvert dans l’environnement de travail. Il faut mettre dans le terminal : 

    git clone https://github.com/yaquinetaki/Dashboard_Global_education.gitcd Dashboard_Global_education


Étape 2 – Création de l’environnement virtuel
Un environnement virtuel Python doit être créé puis activé afin d’isoler les dépendances du projet.

- Sous Windows (PowerShell) : 
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1 

- Sous macOS / Linux :
    python -m venv .venv
    source .venv/bin/activate


Étape 3 – Installation des dépendances
L’ensemble des bibliothèques nécessaires est installé à l’aide du fichier requirements.txt.

Dans le terminal, il faut copier coller : 
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

3. Lancement et arrêt du dashboard

L’application est lancée en exécutant le fichier principal du projet. 
Dans le terminal, il faut copier coller : 

    python main.py

Une adresse locale est alors générée (de type http://127.0.0.1:805X/) et 
permet l’accès au dashboard depuis un navigateur.

Pour arrêter l’application, il suffit d’interrompre l’exécution dans le terminal en mettant : 
    CTRL + C
L’environnement virtuel peut ensuite être désactivé en mettant dans le terminal : 
    deactivate

III. Données utilisées

1. Organisation générale

Les données sont structurées en trois catégories :

- données brutes (fichiers CSV sources) ;

- données nettoyées et prêtes à l’analyse ;

- données géographiques destinées à la cartographie.

Le répertoire data/raw regroupe les fichiers CSV originaux.
Le répertoire data/cleaned contient le jeu de données final.
Le répertoire data/data_geo stocke les fichiers géographiques Natural Earth utilisés pour la carte mondiale.

2. Nature des données

Les données portent principalement sur :

- les indicateurs généraux d’éducation ;

- le nombre d’enfants non scolarisés ;

- les écarts entre genres ;

- différents niveaux éducatifs.

Les fichiers géographiques permettent l’association des pays à une dimension spatiale.
Le fichier cleaned_data.csv constitue la version harmonisée, filtrée et prête à être exploité par l’application.

3. Nettoyage et préparation

Le traitement des données est assuré par des scripts dédiés.
Les principales étapes comprennent :

- l’harmonisation des noms de pays ;
- la gestion des valeurs manquantes ;
- l’agrégation des indicateurs pertinents ;
- la fusion des différents ensembles de données ;
- la production d’un fichier final unique.

IV. Guide développeur (Developer Guide)

1. Structure générale du projet

Le projet est structuré de manière modulaire afin de favoriser la lisibilité, la maintenance et l’évolution du code.

Notre Dashboard comprend notamment :

- un répertoire de données organisé par niveaux de traitement ;
- un répertoire src contenant le code source ;
- des fichiers principaux dédiés à la configuration et à l’exécution de l’application.

2. Rôle des modules principaux

- main.py constitue le point d’entrée de l’application. Il initialise Dash, charge les données et pilote l’interface générale.
- clean_data.py gère l’ensemble des opérations de nettoyage et de préparation des données.
- graph_diag_hist.py regroupe les fonctions générant les graphiques et éléments visuels.
- home.py définit la page principale du dashboard et la structure de navigation.
- les éléments du dossier data_geo servent de support cartographique.

3. Possibilités d’évolution

Le projet peut évoluer à travers différents axes tels que : 

- l’ajout de nouveaux graphiques et indicateurs ;
- l’enrichissement des interactions utilisateurs ;
- l’intégration d’une dimension temporelle ;
- l’amélioration de la représentation géographique et de l’ergonomie.

V. Rapport d’analyse synthétique

1. Principaux résultats observés

L’analyse fait apparaître :

- des écarts marqués entre différentes régions du monde ;
- un accès globalement plus favorable à l’éducation dans les pays développés ;
- la persistance d’un nombre important d’enfants non scolarisés dans certaines zones ;
- des inégalités de genre encore visibles dans plusieurs pays.

2. Limites de l’analyse

Certaines limites doivent être prises en compte comme :

- La disponibilité inégale des données selon les pays ;
- L'hétérogénéité des sources ;
- La périodicité variable des indicateurs ;
- La présence de données manquantes.

3. Perspectives d’amélioration

Nous pensons que plusieurs axes d’amélioration sont envisageables :

- L'approfondissement de la dimension temporelle ;
- L'amélioration de la précision géographique ;
- L'ajout d’indicateurs socio-économiques ;
- L'optimisation de l’interface et de l’expérience utilisateur.

VI. Déclaration de conformité – Copyright

Nous certifions que :

- le code contenu dans ce dépôt a été produit par l’équipe projet ;
- toute portion de code issue d’une ressource externe est clairement citée et documentée ;
- toute absence de mention constitue un cas de plagiat conformément aux règles académiques en vigueur.
