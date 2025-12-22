
import dasH
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
# Liste des pays pour le menu déroulant
df_pour_le_menu = df_final.dropna(subset=[col_homme, col_femme], how='all')
liste_pays = sorted(df_pour_le_menu['Entity'].unique())

# Mise en page du dashboard
layout = html.Div([
    html.H1("Dashboard: L'éducation à travers le monde", style={'textAlign': 'center'}),

    # Carte
    html.Div([
        html.H3("Carte du Monde (LAYS)"),
        html.Iframe(srcDoc=map_html_string, width='100%', height='500', style={'border': 'none'})
    ]),

    html.Hr(),

    # Diagramme
    html.Div([
        html.H3("Diagramme des Enfants Non Scolarisés par Genre"),
        html.Label("Choisis un pays :"),
        dcc.Dropdown(
            id='mon-dropdown',
            options=[{'label': code, 'value': code} for code in liste_pays],
            value='France',
            style={'width': '50%'}
        ),
        dcc.Graph(id='mon-graphique')
    ]),

    html.Hr(),

    # Histogramme
    html.Div([
        html.H3("Histogramme du Taux de Scolarisation Tertiaire par Région"),
        dcc.Graph(figure=Histogramme(df_final))
    ]),

    html.Hr(),

    # Nuage de points (scatter)
    html.Div([
        html.H3("Nuage de points : LAYS vs Enfants non scolarisés (par région)"),
        html.Label("Choisis une année :"),
        dcc.Dropdown(
            id="annee-scatter",
            options=[{"label": int(a), "value": int(a)} for a in liste_annees],
            value=liste_annees[-1] if len(liste_annees) > 0 else None,
            style={"width": "200px"}
        ),
        dcc.Graph(id="graph-scatter")
    ])
])

# Mise à jour du graphique selon le pays sélectionné
@callback(
    Output('mon-graphique', 'figure'),
    Input('mon-dropdown', 'value')
)
def update_graph(pays_choisi):
    return Diagramme_enfants_non_scolarisé(df_final, pays_choisi)
# Mise à jour du nuage de points selon l'année sélectionnée
@callback(
    Output("graph-scatter", "figure"),
    Input("annee-scatter", "value")
)
def update_scatter(annee):
    return Nuage_de_points(df_final, annee)