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
from folium.features import GeoJsonTooltip
def Carte_LAYS(df, world_geo):

    # On garde la dernière valeur LAYS par pays
    df_map = (
        df.dropna(subset=["Code", "Year", col_lays])
          .sort_values("Year")
          .drop_duplicates(subset="Code", keep="last")
          [["Code", col_lays]]
    )

    # Fusion géométrie + données (comme dans le cours)
    gdf = world_geo.merge(df_map, left_on="ADM0_A3", right_on="Code", how="left")

    # Carte de base
    m = folium.Map(location=[20, 0], zoom_start=2)

    # 1) Carte colorée (choroplèthe)
    folium.Choropleth(
        geo_data=world_geo,
        data=df_map,
        columns=["Code", col_lays],
        key_on="feature.properties.ADM0_A3",
        fill_color="YlGnBu",   # couleurs d’origine
        fill_opacity=0.7,
        line_opacity=0.2,
        nan_fill_color="lightgray",
        legend_name="LAYS",
    ).add_to(m)

    # 2) Infos au survol (tooltip)
    folium.GeoJson(
        gdf,
        tooltip=folium.GeoJsonTooltip(
            fields=["ADMIN", col_lays],
            aliases=["Pays", "LAYS"],
        ),
    ).add_to(m)

    return m.get_root().render()

def Camembert_niveaux(df, nom_pays):
    colonnes_requises = [col_F_P, col_M_P, col_F_S, col_M_S, col_taux_F_t, col_taux_H_t]
    df_pays_complet = df[df["Entity"] == nom_pays].dropna(subset=colonnes_requises)

    if df_pays_complet.empty:
        return px.pie(title=f"Aucune donnée complète disponible pour {nom_pays}")

    derniere_ligne = df_pays_complet.sort_values("Year", ascending=False).iloc[0]
    annee_trouvee = derniere_ligne["Year"]

    pri = (derniere_ligne[col_F_P] + derniere_ligne[col_M_P]) / 2
    sec = (derniere_ligne[col_F_S] + derniere_ligne[col_M_S]) / 2
    ter = (derniere_ligne[col_taux_F_t] + derniere_ligne[col_taux_H_t]) / 2

    fig = px.pie(
        names=["Primaire", "Secondaire", "Tertiaire"],
        values=[pri, sec, ter],
        title=f"Niveaux d'éducation : {nom_pays} (Dernière année dispo : {int(annee_trouvee)})",
        hole=0.4,
        color_discrete_sequence=["#FFB6C1", "#FFD700", "#87CEEB"],
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
        color_discrete_sequence=["lightblue", "lightpink"],
    )

    new_names = {col_homme: "Garçons", col_femme: "Filles"}
    fig.for_each_trace(lambda t: t.update(name=new_names.get(t.name, t.name)))

    fig.update_layout(
        title=dict(x=0, font=dict(size=15)),
        xaxis_title=dict(text="Année", font=dict(size=13, color="#195a70", style="italic")),
        yaxis_title=dict(text="Nombre d'enfants", font=dict(size=13, color="#195a70", style="italic")),
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
        value_name="Taux_Scolarisation tertiaire",
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
        height=600,
    )

    his.update_layout(
        title=dict(x=0, font=dict(size=15)),
        xaxis=dict(title=dict(text="Taux Brut d'Inscription Tertiaire (%)",
                              font=dict(size=13, color="#195a70", style="italic"))),
        yaxis=dict(title=dict(text="Régions",
                              font=dict(size=13, color="#195a70", style="italic")),
                   automargin=True),
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
        title="Qualité de l'apprentissage (LAYS) vs Absence d'éducation en 2020",
    )

    fig.update_layout(
        title=dict(x=0, font=dict(size=15)),
        xaxis_title=dict(text="Niveau d’éducation (LAYS)",
                         font=dict(size=13, color="#195a70", style="italic")),
        yaxis_title=dict(text="% Population sans éducation",
                         font=dict(size=13, color="#195a70", style="italic")),
    )
    return fig

