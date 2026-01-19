import dash
from dash import html, dcc, callback, Input, Output
from src.utils.clean_data import get_donnees_pretes
from src.components.graph_diag_hist import (
    Diagramme_enfants_non_scolarisé,
    Histogramme,
    Nuage_de_points,
    Camembert_niveaux,
    Carte_LAYS,
)
from src.components.variables import col_femme, col_homme, col_region, col_lays, col_no_education

# Enregistrement de la page comme page d'accueil
dash.register_page(__name__, path="/")

# Chargement des données
df_final, world_geo = get_donnees_pretes()
map_html_string = Carte_LAYS(df_final, world_geo)

# Préparation des listes pour les menus déroulants
df_ok = df_final.dropna(subset=[col_lays, col_region, col_no_education, "Year"])
liste_regions = sorted(df_ok[col_region].dropna().unique())

df_pour_le_menu = df_final.dropna(subset=[col_homme, col_femme], how="all")
liste_pays = sorted(df_pour_le_menu["Entity"].unique())

# Structure de la page
layout = html.Div(
    className="container",
    children=[
        # En-tête du dashboard
        html.Div(
            className="header",
            children=[html.H1("Dashboard : L'éducation à travers le monde")],
        ),

        # Système d'onglets pour organiser les différentes visualisations
        dcc.Tabs(
            value="tab-carte",
            children=[
                # Premier onglet : carte mondiale
                dcc.Tab(
                    label="Carte (LAYS)",
                    children=[
                        html.Div(
                            className="card",
                            children=[
                                html.H3("Carte du Monde (LAYS)"),
                                html.P(
                                    "LAYS : nombre moyen d'années de scolarité ajustées selon la qualité des apprentissages.",
                                    className="small-text",
                                ),
                                html.Iframe(
                                    srcDoc=map_html_string,
                                    width="100%",
                                    height="520",
                                    style={"border": "none"},
                                ),
                            ],
                        ),
                    ],
                ),

                # Deuxième onglet : analyse détaillée par pays
                dcc.Tab(
                    label="Analyse par pays",
                    children=[
                        html.Div(
                            className="card",
                            children=[
                                html.H3("Choix du pays"),
                                dcc.Dropdown(
                                    id="mon-dropdown",
                                    options=[{"label": p, "value": p} for p in liste_pays],
                                    value="France",
                                    clearable=False,
                                    style={"width": "50%"},
                                ),
                            ],
                        ),

                        html.Div(
                            className="grid",
                            children=[
                                html.Div(
                                    className="card",
                                    children=[
                                        html.H3("Enfants non scolarisés"),
                                        dcc.Graph(id="mon-graphique", style={"height": "500px"}),
                                    ],
                                ),
                                html.Div(
                                    className="card",
                                    children=[
                                        html.H3("Niveaux scolaires"),
                                        dcc.Graph(id="graph-camembert", style={"height": "500px"}),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),

                # Troisième onglet : analyse par régions du monde
                dcc.Tab(
                    label="Analyse par régions",
                    children=[
                        html.Div(
                            className="card",
                            children=[
                                html.H3("Taux de scolarisation tertiaire"),
                                dcc.Graph(figure=Histogramme(df_final), style={"height": "500px"}),
                            ],
                        ),
                        html.Div(
                            className="card",
                            children=[
                                html.H3("LAYS vs absence d'éducation"),
                                dcc.Dropdown(
                                    id="region-scatter",
                                    options=[{"label": r, "value": r} for r in liste_regions],
                                    multi=True,
                                    placeholder="Toutes les régions",
                                ),
                                dcc.Graph(id="graph-scatter", style={"height": "420px"}),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)

# Callback : mise à jour des graphiques selon le pays choisi
@callback(
    Output("mon-graphique", "figure"),
    Output("graph-camembert", "figure"),
    Input("mon-dropdown", "value"),
)
def update_visuals(pays_choisi):
    return (
        Diagramme_enfants_non_scolarisé(df_final, pays_choisi),
        Camembert_niveaux(df_final, pays_choisi),
    )

# Callback : mise à jour du nuage de points selon les régions sélectionnées
@callback(
    Output("graph-scatter", "figure"),
    Input("region-scatter", "value"),
)
def update_scatter(regions_choisies):
    return Nuage_de_points(df_final, regions_choisies)