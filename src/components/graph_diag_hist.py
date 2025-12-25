from .variables import (
    col_femme,
    col_homme,
    col_taux_F,
    col_taux_H,
    col_region,
    col_no_education,
    col_lays
)

import plotly.express as px


# Diagramme : enfants non scolarisés par genre
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

    fig.update_layout(title_x=0.5)  #titre centré
    return fig

# Histogramme : taux tertiaire par région

def Histogramme(df):
    #On garde uniquement les lignes utiles + années récentes
    df_histo_filtre = df.dropna(subset=["Code", "Year", col_taux_F, col_taux_H])
    df_histo_filtre = df_histo_filtre[df_histo_filtre["Year"] >= 2010]

    #On garde la dernière année disponible par pays
    df_histo = (
        df_histo_filtre.sort_values("Year")
        .drop_duplicates(subset="Code", keep="last")
        .groupby(col_region)[[col_taux_F, col_taux_H]]
        .mean()
    )

    #Tri des régions 
    df_histo = df_histo.sort_values(by=col_taux_F, ascending=False)
    df_histo[col_taux_H] = df_histo[col_taux_H] * (-1)

    #On transforme les données pour avoir une ligne = une région + un genre
    df_long = df_histo.reset_index().melt(
        id_vars=[col_region],
        value_vars=[col_taux_F, col_taux_H],
        var_name="Genre",
        value_name="Taux_Scolarisation tertiaire"
    )
    df_long["Taux_Scolarisation_tertiaire"] = df_long["Taux_Scolarisation tertiaire"].abs()

    #Renommage des genres pour la légende
    mapping_genre = {col_taux_F: "Femmes", col_taux_H: "Hommes"}
    df_long["Genre"] = df_long["Genre"].replace(mapping_genre)

    #Création du graphique
    his = px.bar(
        df_long,
        x="Taux_Scolarisation tertiaire",
        y=col_region,
        title="Taux d'Inscription Tertiaire H/F par Région(dernière année disponible)",
        orientation="h",
        color="Genre",
        color_discrete_map={"Femmes": "lightpink", "Hommes": "lightblue"},
        hover_data={
            "Taux_Scolarisation tertiaire": False,
            "Taux_Scolarisation_tertiaire": ":.1f"
        },
        height=600
    )

    #Mise en forme (titres + marges et ajout pour mieux centrer/voir)
    his.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=[-100, -75, -50, -25, 0, 25, 50, 75, 100],
            ticktext=["100", "75", "50", "25", "0", "25", "50", "75", "100"],
            title="Taux Brut d'Inscription Tertiaire (%)"
        ),
        yaxis=dict(title="Régions", dtick=1),
        barmode="relative",
        title_x=0.5,                 #titre centré
        margin=dict(l=150, r=150)    #mêmes marges gauche/droite
    )

    return his

# Nuage de points : LAYS vs % sans éducation
def Nuage_de_points(df, regions_choisies):
    df_scatter = df.dropna(subset=[col_lays, col_no_education, col_region, "Year"]).copy()
    df_scatter = df_scatter[df_scatter["Year"] == 2020]
    df_scatter = df_scatter[df_scatter[col_no_education] > 0]

    if regions_choisies:
        df_scatter = df_scatter[df_scatter[col_region].isin(regions_choisies)]

    fig = px.scatter(
        df_scatter,
        x=col_lays,
        y=col_no_education,
        color=col_region,
        hover_name="Entity",
        title="Qualité de l'apprentissage (LAYS) vs Absence d'éducation en 2020",
        labels={
            col_lays: "Niveau d’éducation (LAYS)",
            col_no_education: "% Population sans éducation"
        }
    )

    fig.update_traces(marker=dict(size=10, opacity=0.6))
    fig.update_layout(title_x=0.5)  #titre centré
    return fig