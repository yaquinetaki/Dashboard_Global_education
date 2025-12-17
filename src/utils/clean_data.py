import pandas as pd
import geopandas as gpd
import os
from config import RAW_DATA_DIR, CLEANED_DATA_DIR, SHP_PATH
from src.components.variables import col_region

# Liste des fichiers CSV à charger
FILE_NAMES = [
    "1-basic-education.csv",
    "2- lays.csv",
    "3- nbr_out_school_children.csv",
    "4- gender-gap-educ-levels.csv"
]

# Chargement et fusion des différents fichiers CSV
def load_and_combine_data():
    df_principal = None
    for file in FILE_NAMES:
        # Construction du chemin du fichier à partir de config.py
        file_path = os.path.join(RAW_DATA_DIR, file)
        try:
            df_actuel = pd.read_csv(file_path)
            if df_principal is None:
                df_principal = df_actuel
            else:
                # Fusion des données sur pays et année
                df_principal = pd.merge(
                    df_principal,
                    df_actuel,
                    on=['Entity', 'Code', 'Year'],
                    how='outer'
                )
        except FileNotFoundError:
            print(f"Fichier {file_path} non trouvé.")
    return df_principal

# Nettoyage des données (on garde uniquement les pays)
def clean_and_remove_data(df_raw):
    df_cleaned = df_raw.copy()
    
    # On conserve uniquement les codes pays (3 lettres)
    est_un_pays = df_cleaned['Code'].str.len() == 3
    df_cleaned = df_cleaned[est_un_pays]

    # Création du dossier cleaned s'il n'existe pas
    if not os.path.exists(CLEANED_DATA_DIR):
        os.makedirs(CLEANED_DATA_DIR)

    # Sauvegarde des données nettoyées
    file_path = os.path.join(CLEANED_DATA_DIR, 'cleaned_data.csv')
    df_cleaned.to_csv(file_path, index=False)

    return df_cleaned

# Fonction principale pour récupérer les données prêtes à l'emploi
def get_donnees_pretes():

    # Chargement et nettoyage des données
    df_raw = load_and_combine_data()
    df_final = clean_and_remove_data(df_raw)

    try:
        # Chargement du fichier géographique (shapefile)
        world_geo = gpd.read_file(SHP_PATH)

        # Préparation des données de régions pour la fusion
        df_regions = world_geo[['ADM0_A3', col_region]].copy()
        df_regions = df_regions.rename(columns={'ADM0_A3': 'Code'})

        # Fusion des régions avec les données principales
        df_final = df_final.merge(df_regions, on='Code', how='left')

    except Exception as e:
        print(f"Erreur chargement shapefile: {e}")
        world_geo = None

    return df_final, world_geo

