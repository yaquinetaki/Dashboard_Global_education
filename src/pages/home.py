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

dash.register_page(__name__, path="/")

# Données
df_final, world_geo = get_donnees_pretes()
map_html_string = Carte_LAYS(df_final, world_geo)

df_ok = df_final.dropna(subset=[col_lays, col_region, col_no_education, "Year"])
liste_regions = sorted(df_ok[col_region].dropna().unique())
df_pour_le_menu = df_final.dropna(subset=[col_homme, col_femme], how="all")
liste_pays = sorted(df_pour_le_menu["Entity"].unique())

# Layout 
layout = html.Div(
    className="container",  
    children=[

        # En-tête du dashboard
        html.Div(
            className="header",
            children=[
                html.H1("Dashboard : L'éducation à travers le monde")
            ],
        ),

        # Système d’onglets
        dcc.Tabs(
            value="tab-carte",  # onglet affiché par défaut
            children=[

                # ONGLET 1 : CARTE 
                dcc.Tab(
                    label="Carte (LAYS)",
                    children=[
                        html.Div(
                            className="card",
                            children=[
                                html.H3("Carte du Monde (LAYS)"),

                                # Texte explicatif
                                html.P(
                                    "LAYS : nombre moyen d’années de scolarité ajustées selon la qualité des apprentissages.",
                                    className="small-text",
                                ),

                                # Carte intégrée via un iframe
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

                # ONGLET 2 : ANALYSE PAR PAYS
                dcc.Tab(
                    label="Analyse par pays",
                    children=[

                        # Carte contenant le choix du pays
                        html.Div(
                            className="card",
                            children=[
                                html.H3("Choix du pays"),

                                # Menu déroulant pour sélectionner un pays
                                dcc.Dropdown(
                                    id="mon-dropdown",  # utilisé dans les callbacks
                                    options=[{"label": p, "value": p} for p in liste_pays],
                                    value="France",  # pays sélectionné par défaut
                                    clearable=False,  # on ne peut pas enlever la sélection
                                    style={"width": "50%"},
                                ),
                            ],
                        ),

                        # Grille contenant les graphiques
                        html.Div(
                            className="grid",
                            children=[

                                # Graphique 1 : enfants non scolarisés
                                html.Div(
                                    className="card",
                                    children=[
                                        html.H3("Enfants non scolarisés"),
                                        dcc.Graph(
                                            id="mon-graphique",
                                            style={"height": "500px"}
                                        ),
                                    ],
                                ),

                                # Graphique 2 : répartition par niveaux scolaires
                                html.Div(
                                    className="card",
                                    children=[
                                        html.H3("Niveaux scolaires"),
                                        dcc.Graph(
                                            id="graph-camembert",
                                            style={"height": "500px"}
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),

                # ===== ONGLET 3 : ANALYSE PAR RÉGIONS =====
                dcc.Tab(
                    label="Analyse par régions",
                    children=[

                        # Histogramme par région
                        html.Div(
                            className="card",
                            children=[
                                html.H3("Taux de scolarisation tertiaire"),
                                dcc.Graph(
                                    figure=Histogramme(df_final),
                                    style={"height": "500px"}
                                ),
                            ],
                        ),

                        # Scatter plot avec sélection de régions
                        html.Div(
                            className="card",
                            children=[
                                html.H3("LAYS vs absence d'éducation"),

                                # Sélection multiple des régions
                                dcc.Dropdown(
                                    id="region-scatter",
                                    options=[{"label": r, "value": r} for r in liste_regions],
                                    multi=True,
                                    placeholder="Toutes les régions",
                                ),

                                dcc.Graph(
                                    id="graph-scatter",
                                    style={"height": "420px"}
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)
# Callbacks
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


@callback(
    Output("graph-scatter", "figure"),
    Input("region-scatter", "value"),
)
def update_scatter(regions_choisies):
    return Nuage_de_points(df_final, regions_choisies)
