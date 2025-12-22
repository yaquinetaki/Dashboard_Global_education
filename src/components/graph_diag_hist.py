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
#test commit

# Fonction pour créer l'histogramme du taux de scolarisation tertiaire par pays
def Histogramme(df):

        # Préparation des données (filtrage et calcul des moyennes par région)
    df_histo_filtre = df.dropna(subset=['Code', 'Year', col_taux_F, col_taux_H])
    df_histo_filtre = df_histo_filtre[df_histo_filtre['Year'] >= 2010]
    df_histo = df_histo_filtre.sort_values('Year').drop_duplicates(subset='Code', keep='last')
    df_histo = df_histo.groupby(col_region)[[col_taux_F, col_taux_H]].mean()
    
    # Tri des régions pour une meilleure lisibilité du graphique
    df_histo = df_histo.sort_values(by=col_taux_F,ascending=False)
    df_histo[col_taux_H]= df_histo[col_taux_H]*(-1) # Valeurs négatives pour afficher un histogramme en miroir
    df_long = df_histo.reset_index().melt(
    id_vars=[col_region],
    value_vars=[col_taux_F, col_taux_H],
    var_name='Genre',
    value_name='Taux_Scolarisation tertiaire'
    )
    df_long['Taux_Scolarisation_tertiaire']= df_long['Taux_Scolarisation tertiaire'].abs()
    mapping_genre = {
        col_taux_F: 'Femmes',
        col_taux_H: 'Hommes'
    }
    df_long['Genre'] = df_long['Genre'].replace(mapping_genre)
    his= px.bar(
        df_long,
        x='Taux_Scolarisation tertiaire',
        y=col_region,
        title="Comparaison des Taux d'Inscription Tertiaire H/F par Région (Dernières années disponibles)",
        orientation='h',
        color='Genre',
        color_discrete_map={'Femmes': 'lightpink', 'Hommes': 'lightblue'},
        hover_data={ 'Taux_Scolarisation tertiaire': False, 'Taux_Scolarisation_tertiaire': ':.1f'},
        height=600
    )