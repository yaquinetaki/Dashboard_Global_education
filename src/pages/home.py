import dash
from dash import html, dcc, callback, Input, Output
import folium
import pandas as pd

from src.utils.clean_data import get_donnees_pretes
from src.components.graph_diag_hist import Diagramme_enfants_non_scolarisé, Histogramme, Nuage_de_points
from src.components.variables import col_femme, col_homme, col_region, col_lays, col_no_education

# On déclare la page pour Dash
dash.register_page(__name__, path='/')

# Chargement des données 
df_final, world_geo = get_donnees_pretes()

df_ok = df_final.dropna(subset=[col_lays, col_region, col_no_education, "Year"])
liste_regions = sorted(df_ok[col_region].dropna().unique())

# Données utilisées pour la carte Folium
df_map_filtre = df_final.dropna(subset=['Code', 'Year', col_lays])
df_map = df_map_filtre.sort_values('Year').drop_duplicates(subset='Code', keep='last')

# Création Carte
map_folium = folium.Map(location=[20,0], tiles='OpenStreetMap', zoom_start=2)

# Ajout de la carte choroplèthe (LAYS par pays)
if world_geo is not None:
    folium.Choropleth(
        geo_data=world_geo.to_json(),
        name='LAYS',
        data=df_map,
        columns=['Code', col_lays],
        key_on='feature.properties.ADM0_A3',
        fill_color='YlGnBu',
        fill_opacity=0.7,
        line_opacity=0.2,
        nan_fill_color='lightgray',
        legend_name='LAYS (Dernière année disponible par pays)'
    ).add_to(map_folium)

# On convertit la carte en HTML pour l'afficher dans Dash
map_html_string = map_folium.get_root().render()
