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
        title=dict(x=0, font=dict(size=15)),   # ✅ titre à gauche
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
    df_histo_filtre = df.dropna(subset=["Code", "Year", col_taux_F, col_taux_H])
    df_histo_filtre = df_histo_filtre[df_histo_filtre["Year"] >= 2010]

    df_histo = (
        df_histo_filtre.sort_values("Year")
        .drop_duplicates(subset="Code", keep="last")
        .groupby(col_region)[[col_taux_F, col_taux_H]]
        .mean()
    )

    df_histo = df_histo.sort_values(by=col_taux_F, ascending=False)
    df_histo[col_taux_H] *= -1

    df_long = df_histo.reset_index().melt(
        id_vars=[col_region],
        value_vars=[col_taux_F, col_taux_H],
        var_name="Genre",
        value_name="Taux_Scolarisation tertiaire"
    )

    df_long["Taux_Scolarisation_tertiaire"] = df_long["Taux_Scolarisation tertiaire"].abs()
    df_long["Genre"] = df_long["Genre"].replace({col_taux_F: "Femmes", col_taux_H: "Hommes"})

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
        title=dict(x=0, font=dict(size=15)),   # ✅ titre à gauche
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

