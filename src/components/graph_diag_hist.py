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
    # Sélection des données utiles (dernière année par pays)
    df_map_filtre = df.dropna(subset=['Code', 'Year', col_lays])
    df_map = (
        df_map_filtre
        .sort_values('Year')
        .drop_duplicates(subset='Code', keep='last')
    )

    # Création de la carte
    map_folium = folium.Map(location=[20, 0], tiles='CartoDB positron', zoom_start=2)

    df_tooltip = df_map[["Code", col_lays, "Year"]].copy()
    df_tooltip[col_lays] = df_tooltip[col_lays].round(2)
    geo_tooltip = world_geo.merge(
    df_tooltip,
    left_on="ADM0_A3",
    right_on="Code",
    how="left",
    )
    # Ajout choroplèthe uniquement si la géométrie existe
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
            legend_name='LAYS (Dernière année disponible par pays)'
        ).add_to(map_folium)

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

    # Conversion en HTML pour Dash
    return map_folium.get_root().render()

def Camembert_niveaux(df, nom_pays):

    colonnes_requises = [col_F_P, col_M_P, col_F_S, col_M_S, col_taux_F_t, col_taux_H_t] 
    df_pays_complet = df[df['Entity'] == nom_pays].dropna(subset=colonnes_requises)
    
    # si aucune année n'a les 3 niveaux complets
    if df_pays_complet.empty:
        return px.pie(title=f"Aucune donnée complète disponible pour {nom_pays}")

    #On trie par année pour prendre la plus récente (la dernière)
    derniere_ligne = df_pays_complet.sort_values("Year", ascending=False).iloc[0]
    annee_trouvee = derniere_ligne['Year']

    # Calcul des moyennes
    pri = (derniere_ligne[col_F_P] + derniere_ligne[col_M_P]) / 2
    sec = (derniere_ligne[col_F_S] + derniere_ligne[col_M_S]) / 2
    ter = (derniere_ligne[col_taux_F_t] + derniere_ligne[col_taux_H_t]) / 2

    # Création du camembert
    fig = px.pie(
        names=['Primaire', 'Secondaire', 'Tertiaire'],
        values=[pri, sec, ter],
        title=f"Niveaux d'éducation : {nom_pays} (Dernière année dispo : {int(annee_trouvee)})",
        hole=0.4,
        color_discrete_sequence=['#FFB6C1', '#FFD700', '#87CEEB']
    )
    return fig

def Diagramme_enfants_non_scolarisé(df, nom_pays):
    df_pays = df[df["Entity"] == nom_pays].sort_values("Year")

    fig = px.bar(
        df_pays,
        x="Year",
        y=[col_homme, col_femme],
        title=f"Enfants non scolarisés : {nom_pays} (Filles vs Garçons)",
        labels={"value": "Nombre d'enfants", "variable": "Genre"},
        color_discrete_sequence=["lightblue", "lightpink"]
    )

    new_names = {col_homme: "Garçons", col_femme: "Filles"}
    fig.for_each_trace(lambda t: t.update(name=new_names[t.name]))

    fig.update_layout(
        title=dict(x=0, font=dict(size=15)),   
        xaxis_title=dict(
            text="Année",
            font=dict(size=13, color="#195a70", style="italic")
        ),
        yaxis_title=dict(
            text="Nombre d'enfants",
            font=dict(size=13, color="#195a70", style="italic")
        )
    )

    return fig


def Histogramme(df):
    df_histo_filtre = df.dropna(subset=["Code", "Year", col_taux_F_t, col_taux_H_t])
    df_histo_filtre = df_histo_filtre[df_histo_filtre["Year"] >= 2010]

    df_histo = (
        df_histo_filtre.sort_values("Year")
        .drop_duplicates(subset="Code", keep="last")
        .groupby(col_region)[[col_taux_F_t, col_taux_H_t]]
        .mean()
    )

    df_histo = df_histo.sort_values(by=col_taux_F_t, ascending=False)
    df_histo[col_taux_H_t] *= -1

    df_long = df_histo.reset_index().melt(
        id_vars=[col_region],
        value_vars=[col_taux_F_t, col_taux_H_t],
        var_name="Genre",
        value_name="Taux_Scolarisation tertiaire"
    )

    df_long["Taux_Scolarisation_tertiaire"] = df_long["Taux_Scolarisation tertiaire"].abs()
    df_long["Genre"] = df_long["Genre"].replace({col_taux_F_t: "Femmes", col_taux_H_t: "Hommes"})

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
    df_scatter = df.dropna(subset=[col_lays, col_no_education, col_region, "Year"])
    df_scatter = df_scatter[(df_scatter["Year"] == 2020) & (df_scatter[col_no_education] > 0)]

    if regions_choisies:
        df_scatter = df_scatter[df_scatter[col_region].isin(regions_choisies)]

    fig = px.scatter(
        df_scatter,
        x=col_lays,
        y=col_no_education,
        color=col_region,
        hover_name="Entity",
        title="Qualité de l'apprentissage (LAYS) vs Absence d'éducation en 2020"
    )

    fig.update_layout(
        title=dict(x=0, font=dict(size=15)),   #titre à gauche
        xaxis_title=dict(
            text="Niveau d’éducation (LAYS)",
            font=dict(size=13, color="#195a70", style="italic")
        ),
        yaxis_title=dict(
            text="% Population sans éducation",
            font=dict(size=13, color="#195a70", style="italic")
        )
    )

    return fig

