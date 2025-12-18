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

# Fonction pour créer le diagramme : enfants non scolarisés par genre pour un pays donné

def Diagramme_enfants_non_scolarisé(df, nom_pays):

    # On sélectionne les données du pays choisi
    df_pays = df[df["Entity"] == nom_pays].sort_values("Year")

    # Création du diagramme en barres empilées
    fig = px.bar(
        df_pays,
        x="Year",
        y=[col_homme, col_femme],
        title=f"Enfants non scolarisés : {nom_pays} (Filles vs Garçons)",
        labels={"value": "Nombre d'enfants", "variable": "Genre"},
        color_discrete_sequence=["lightblue", "lightpink"]
    )
    # Renommage des catégories dans la légende
    new_names = {col_homme: "Garçons", col_femme: "Filles"}
    fig.for_each_trace(lambda t: t.update(name = new_names[t.name]))
    
    return fig
