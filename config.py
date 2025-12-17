import os

# Racine du projet
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Chemins des dossiers
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
CLEANED_DATA_DIR = os.path.join(DATA_DIR, 'cleaned')

# Chemin vers ton fichier Shapefile (carte)
SHP_PATH = os.path.join(DATA_DIR, 'data_geo', 'ne_50m_admin_0_countries.shp')