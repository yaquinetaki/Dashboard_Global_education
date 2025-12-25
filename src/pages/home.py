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


# Liste des pays pour le menu déroulant
df_pour_le_menu = df_final.dropna(subset=[col_homme, col_femme], how='all')
liste_pays = sorted(df_pour_le_menu['Entity'].unique())


# Mise en page du dashboard
layout = html.Div(
    className="container",
    children=[
        # En-tête
        html.Div(
            className="header",
            children=[
                html.H1("Dashboard : L'éducation à travers le monde", style={"textAlign": "center"}),
                html.P(
                    "LAYS (Learning-Adjusted Years of School) : nombre moyen d’années de scolarité ajustées selon la qualité des apprentissages.",
                    className="small-text",
                ),
            ],
        ),

        # Carte du monde
        html.Div(
            className="card",
            children=[
                html.H3("Carte du Monde (LAYS)", style={"textAlign": "center"}),
                html.Iframe(
                    srcDoc=map_html_string,
                    width="100%",
                    height="520",
                    style={"border": "none"},
                ),
            ],
        ),

        # Graphiques côte à côte
        html.Div(
            className="grid",
            children=[
                # Diagramme enfants non scolarisés
                html.Div(
                    className="card",
                    children=[
                        html.H3("Enfants Non Scolarisés par Genre", style={"textAlign": "center"}),
                        html.Label("Choisis un pays :", className="label"),
                        dcc.Dropdown(
                            id="mon-dropdown",
                            options=[{"label": p, "value": p} for p in liste_pays],
                            value="France",
                            style={"width": "80%"},
                        ),
                        dcc.Graph(
                            id="mon-graphique",
                            className="graph",
                            style={"height": "460px"},
                        ),
                    ],
                ),

                # Histogramme tertiaire
                html.Div(
                    className="card",
                    children=[
                        html.H3(
                            "Taux de Scolarisation Tertiaire par Région",
                            style={"textAlign": "center"},
                        ),
                        dcc.Graph(
                            figure=Histogramme(df_final),
                            className="graph",
                            style={"height": "540px"},
                        ),
                    ],
                ),
            ],
        ),

        # Nuage de points
        html.Div(
            className="card",
            children=[
                html.H3(
                    "Qualité d'apprentissage vs Absence de scolarisation",
                    style={"textAlign": "center"},
                ),
                html.Label("Sélectionnez une ou plusieurs régions :", className="label"),
                dcc.Dropdown(
                    id="region-scatter",
                    options=[{"label": r, "value": r} for r in liste_regions],
                    multi=True,
                    placeholder="Toutes les régions",
                ),
                dcc.Graph(
                    id="graph-scatter",
                    className="graph",
                    style={"height": "520px"},
                ),
            ],
        ),
    ],
)

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
    Input("region-scatter", "value")
)
def update_scatter(regions_choisies):
    return Nuage_de_points(df_final, regions_choisies)