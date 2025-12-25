Dashboard_global_education/
├── data/                         # Dossier des données
│   ├── data_geo/                 # Données géographiques (fichiers .SHP...)
│   └── raw/                      # Fichiers CSV sources
│       ├── 1-basic-education.csv
│       ├── 2- lays.csv
│       ├── 3- nbr_out_school_children.csv
│       └── 4- gender-gap-educ-levels.csv
├── images/                       
├── src/                          # Code source du dashboard
│   ├── __init__.py               # Rend le dossier src importable
│   ├── components/               # Composants visuels du dashboard (graphique, histogramme,diagramme etc...) + variables
│   │   ├── __init__.py
│   │   ├── graph_diag_hist.py    # Code des différents visuels 
│   │   └── variables.py          # Définition des constantes et noms de colonnes
│   ├── pages/                    # Structure des pages de l'application
│   │   ├── __init__.py
│   │   └── home.py               # Page d'accueil du dashboard
│   └── utils/                    # Outils de traitement de données
│       ├── __init__.py
│       ├── clean_data.py         # Fonctions de nettoyage (Pandas)
│       └── get_data.py           # Fonctions de chargement des fichiers
├── .gitignore                    # Fichiers à exclure de Git (ex: venv)
├── config.py                     # Paramètres de configuration
├── main.py                       # Fichier principal à exécuter
├── README.md                     # Documentation (recommandé)
└── requirements.txt              # Bibliothèques à installer