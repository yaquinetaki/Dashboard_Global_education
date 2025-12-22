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