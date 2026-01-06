import dash
from dash import html, dcc, callback, Input, Output
from src.utils.clean_data import get_donnees_pretes
from src.components.graph_diag_hist import Diagramme_enfants_non_scolarisé, Histogramme, Nuage_de_points, Camembert_niveaux, Carte_LAYS
from src.components.variables import col_femme, col_homme, col_region, col_lays, col_no_education

# On déclare la page pour Dash
dash.register_page(__name__, path='/')

# Chargement des données
df_final, world_geo = get_donnees_pretes()
map_html_string = Carte_LAYS(df_final, world_geo)

df_ok = df_final.dropna(subset=[col_lays, col_region, col_no_education, "Year"])
liste_regions = sorted(df_ok[col_region].dropna().unique())

# Liste des pays pour le menu déroulant
df_pour_le_menu = df_final.dropna(subset=[col_homme, col_femme], how='all')
liste_pays = sorted(df_pour_le_menu['Entity'].unique())

# Mise en page du dashboard
layout = html.Div(
    className="container",
    children=[

        # Header (SANS la définition LAYS)
        html.Div(
            className="header",
            children=[
                html.H1("Dashboard : L'éducation à travers le monde"),
            ],
        ),
        
        # Carte du monde
        html.Div(
            className="card",
            children=[
                html.H3("Carte du Monde (LAYS)"),

                # Définition LAYS sous la carte
                html.P(
                    "LAYS (Learning-Adjusted Years of School) : nombre moyen d’années de scolarité ajustées selon la qualité des apprentissages.",
                    className="small-text"
                ),

                html.Iframe(
                    srcDoc=map_html_string,
                    width="100%",
                    height="520",
                    style={"border": "none"}
                ),
            ],
        ),

        # Sélecteur de pays (Interactivité pour les graphiques suivants)
        html.Div(
            className="card",
            children=[
                html.H3("Sélection du Pays"),
                html.Label("Choisis un pays pour mettre à jour les graphiques :", className="label"),
                dcc.Dropdown(
                    id="mon-dropdown",
                    options=[{"label": p, "value": p} for p in liste_pays],
                    value="France",
                    clearable=False,
                    style={"width": "50%"},
                ),
            ]
        ),

        # Graphiques interactifs (Diagramme et Camembert)
        html.Div(
            className="grid",
            children=[
                html.Div(
                    className="card",
                    children=[
                        html.H3("Enfants Non Scolarisés par Genre"),
                        dcc.Graph(id="mon-graphique", style={"height": "500px"}),
                    ],
                ),
                html.Div(
                    className="card",
                    children=[
                        html.H3("Répartition par niveau scolaire"),
                        dcc.Graph(id='graph-camembert', style={"height": "500px"})
                    ]
                ),
            ],
        ),

        # Graphiques de synthèse (Histogramme et Nuage)
        html.Div(
            className="grid",
            children=[
                # Histogramme tertiaire
                html.Div(
                    className="card",
                    children=[
                        html.H3("Taux de Scolarisation Tertiaire par Région"),
                        dcc.Graph(
                            figure=Histogramme(df_final),
                            style={"height": "500px"},
                        ),
                    ],
                ),
                # Nuage de points
                html.Div(
                    className="card",
                    children=[
                        html.H3("Apprentissage vs Absence de scolarisation"),
                        dcc.Dropdown(
                            id="region-scatter",
                            options=[{"label": r, "value": r} for r in liste_regions],
                            multi=True,
                            placeholder="Toutes les régions",
                        ),
                        dcc.Graph(
                            id="graph-scatter",
                            style={"height": "420px"},
                        ),
                    ],
                ),
            ],
        ),
    ],
)

# Callback unique pour mettre à jour le Diagramme ET le Camembert selon le pays
@callback(
    Output('mon-graphique', 'figure'),
    Output('graph-camembert', 'figure'),
    Input('mon-dropdown', 'value')
)
def update_visuals(pays_choisi):
    fig_barres = Diagramme_enfants_non_scolarisé(df_final, pays_choisi)
    fig_camembert = Camembert_niveaux(df_final, pays_choisi)
    return fig_barres, fig_camembert

# Mise à jour du nuage de points selon les régions
@callback(
    Output("graph-scatter", "figure"),
    Input("region-scatter", "value")
)
def update_scatter(regions_choisies):
    return Nuage_de_points(df_final, regions_choisies)