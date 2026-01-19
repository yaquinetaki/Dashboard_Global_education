from .variables import (
    col_femme,
    col_homme,
    col_taux_F_t,
    col_taux_H_t,
    col_region,
    col_no_education,
    col_lays,
    col_F_P,
    col_M_P,
    col_F_S,
    col_M_S,
)
import plotly.express as px
import folium

def Carte_LAYS(df, world_geo):
    """
    Crée une carte Folium choroplèthe (LAYS) et retourne le HTML prêt à afficher.
    """
    # On garde seulement les pays qui ont des données LAYS complètes
    df_map_filtre = df.dropna(subset=['Code', 'Year', col_lays])
    
    # Pour chaque pays, on prend uniquement la donnée la plus récente
    df_map = (
        df_map_filtre
        .sort_values('Year')
        .drop_duplicates(subset='Code', keep='last')
    )

    # Création de la carte centrée sur le monde
    map_folium = folium.Map(location=[20, 0], tiles='CartoDB positron', zoom_start=2)

    # Préparation des données pour l'info-bulle (tooltip)
    df_tooltip = df_map[["Code", col_lays, "Year"]].copy()
    df_tooltip[col_lays] = df_tooltip[col_lays].round(2)
    
    # On fusionne les données géographiques avec nos données LAYS
    geo_tooltip = world_geo.merge(
        df_tooltip,
        left_on="ADM0_A3",
        right_on="Code",
        how="left",
    )
    
    # Ajout de la couche colorée selon les valeurs LAYS
    if world_geo is not None:
        folium.Choropleth(
            geo_data=world_geo.to_json(),
            name='LAYS',
            data=df_map,
            columns=['Code', col_lays],
            key_on='feature.properties.ADM0_A3',
            fill_color='YlGnBu',
            fill_opacity=0.7,
            line_opacity=0,
            nan_fill_color='lightgray',
            legend_name='LAYS en 2020'
        ).add_to(map_folium)
    
    # Ajout d'une couche invisible pour afficher les infos au survol
    folium.GeoJson(
        geo_tooltip.to_json(),
        style_function=lambda feature: {
            "fillOpacity": 0,
            "color": "transparent",
            "weight": 0,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["NAME", col_lays, "Year"],
            aliases=["Pays :", "LAYS :", "Année :"],
            localize=True,
            sticky=False,
        ),
    ).add_to(map_folium)

    # Conversion de la carte en HTML
    html_string = map_folium.get_root().render()

    # Ajout d'un peu de CSS pour enlever les encadrés noirs au clic
    custom_css = """
    <style>
    .leaflet-interactive:focus {
        outline: none !important;
    }
    .leaflet-interactive {
        outline: none !important;
    }
    </style>
    """
    html_string = html_string.replace('</head>', custom_css + '</head>')
    return html_string


def Camembert_niveaux(df, nom_pays):
    """
    Crée un graphique en camembert qui montre la répartition des élèves 
    entre primaire, secondaire et tertiaire pour un pays donné.
    """
    # On vérifie qu'on a bien les données pour les 3 niveaux
    colonnes_requises = [col_F_P, col_M_P, col_F_S, col_M_S, col_taux_F_t, col_taux_H_t] 
    df_pays_complet = df[df['Entity'] == nom_pays].dropna(subset=colonnes_requises)
    
    # Si aucune année n'a toutes les données, on affiche un message
    if df_pays_complet.empty:
        return px.pie(title=f"Aucune donnée complète disponible pour {nom_pays}")

    # On prend l'année la plus récente
    derniere_ligne = df_pays_complet.sort_values("Year", ascending=False).iloc[0]
    annee_trouvee = derniere_ligne['Year']

    # Calcul des moyennes entre filles et garçons pour chaque niveau
    pri = (derniere_ligne[col_F_P] + derniere_ligne[col_M_P]) / 2
    sec = (derniere_ligne[col_F_S] + derniere_ligne[col_M_S]) / 2
    ter = (derniere_ligne[col_taux_F_t] + derniere_ligne[col_taux_H_t]) / 2

    # Création du graphique camembert avec les 3 niveaux
    fig = px.pie(
        names=['Primaire', 'Secondaire', 'Tertiaire'],
        values=[pri, sec, ter],
        title=f"Niveaux d'éducation : {nom_pays} en {int(annee_trouvee)}",
        hole=0.4,
        color_discrete_sequence=['#FFB6C1', '#FFD700', '#87CEEB']
    )
    return fig


def Diagramme_enfants_non_scolarisé(df, nom_pays):
    """
    Crée un diagramme en barres qui montre l'évolution du nombre d'enfants 
    non scolarisés (filles vs garçons) dans un pays.
    """
    # On filtre pour le pays choisi et on trie par année
    df_pays = df[df["Entity"] == nom_pays].sort_values("Year")

    # Création du diagramme avec deux barres (filles et garçons)
    fig = px.bar(
        df_pays,
        x="Year",
        y=[col_homme, col_femme],
        title=f"Enfants non scolarisés : {nom_pays} (Filles vs Garçons)",
        labels={"value": "Nombre d'enfants", "variable": "Genre"},
        color_discrete_sequence=["lightblue", "lightpink"]
    )
    
    # Calcul d'une marge pour l'axe des années
    annee_min = df_pays["Year"].min()
    annee_max = df_pays["Year"].max()
    diffrence_annees = annee_max - annee_min
    marge = (diffrence_annees * 0.05) if diffrence_annees > 0 else 2

    # Renommage des légendes pour qu'elles soient plus claires
    new_names = {col_homme: "Garçons", col_femme: "Filles"}
    fig.for_each_trace(lambda t: t.update(name=new_names[t.name]))

    # Configuration de l'axe des années avec une marge de chaque côté
    fig.update_xaxes(
        range=[annee_min - marge, annee_max + marge],
        title_text="Année",
        autorange=False,
        title_font=dict(size=13, color="#195a70", style="italic"),
        type='linear'
    )

    # Mise en forme du graphique
    fig.update_layout(
        title=dict(x=0, font=dict(size=15)),
        yaxis_title=dict(
            text="Nombre d'enfants",
            font=dict(size=13, color="#195a70", style="italic")
        )
    )

    return fig


def Histogramme(df):
    """
    Crée un histogramme horizontal montrant les taux de scolarisation 
    tertiaire par région (comparaison femmes/hommes).
    """
    # On garde seulement les données récentes (après 2010)
    df_histo_filtre = df.dropna(subset=["Code", "Year", col_taux_F_t, col_taux_H_t])
    df_histo_filtre = df_histo_filtre[df_histo_filtre["Year"] >= 2010]

    # Pour chaque pays, on prend la dernière année disponible
    # puis on calcule la moyenne par région
    df_histo = (
        df_histo_filtre.sort_values("Year")
        .drop_duplicates(subset="Code", keep="last")
        .groupby(col_region)[[col_taux_F_t, col_taux_H_t]]
        .mean()
    )

    # On trie les régions par taux féminin décroissant
    df_histo = df_histo.sort_values(by=col_taux_F_t, ascending=False)
    
    # On inverse les valeurs hommes pour créer un graphique en miroir
    df_histo[col_taux_H_t] *= -1

    # Transformation des données pour Plotly (format long)
    df_long = df_histo.reset_index().melt(
        id_vars=[col_region],
        value_vars=[col_taux_F_t, col_taux_H_t],
        var_name="Genre",
        value_name="Taux_Scolarisation tertiaire"
    )

    # On remet les valeurs en positif et on renomme les genres
    df_long["Taux_Scolarisation_tertiaire"] = df_long["Taux_Scolarisation tertiaire"].abs()
    df_long["Genre"] = df_long["Genre"].replace({col_taux_F_t: "Femmes", col_taux_H_t: "Hommes"})

    # Création de l'histogramme horizontal
    his = px.bar(
        df_long,
        x="Taux_Scolarisation tertiaire",
        y=col_region,
        title="Taux d'inscription tertiaire H/F par région (dernière année disponible)",
        orientation="h",
        color="Genre",
        color_discrete_map={"Femmes": "lightpink", "Hommes": "lightblue"},
        height=600
    )

    # Personnalisation des titres des axes
    his.update_layout(
        title=dict(x=0, font=dict(size=15)),   
        xaxis=dict(
            title=dict(
                text="Taux Brut d'Inscription Tertiaire (%)",
                font=dict(size=13, color="#195a70", style="italic")
            )
        ),
        yaxis=dict(
            title=dict(
                text="Régions",
                font=dict(size=13, color="#195a70", style="italic")
            ),
            automargin=True
        )
    )

    return his


def Nuage_de_points(df, regions_choisies):
    """
    Crée un nuage de points montrant la relation entre le niveau d'éducation (LAYS) 
    et le pourcentage de population sans éducation, avec possibilité de filtrer par régions.
    """
    # On garde les données de 2020 avec un taux de non-éducation positif
    df_scatter = df.dropna(subset=[col_lays, col_no_education, col_region, "Year"])
    df_scatter = df_scatter[(df_scatter["Year"] == 2020) & (df_scatter[col_no_education] > 0)]

    # Si l'utilisateur a sélectionné des régions, on filtre
    if regions_choisies:
        df_scatter = df_scatter[df_scatter[col_region].isin(regions_choisies)]

    # Création du nuage de points coloré par région
    fig = px.scatter(
        df_scatter,
        x=col_lays,
        y=col_no_education,
        color=col_region,
        hover_name="Entity",
        title="Qualité de l'apprentissage (LAYS) vs Absence d'éducation en 2020"
    )

    # Personnalisation des titres des axes
    fig.update_layout(
        title=dict(x=0, font=dict(size=15)),
        xaxis_title=dict(
            text="Niveau d'éducation (LAYS)",
            font=dict(size=13, color="#195a70", style="italic")
        ),
        yaxis_title=dict(
            text="% Population sans éducation",
            font=dict(size=13, color="#195a70", style="italic")
        )
    )

    return fig