import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
import random

# --- Configuration de la page ---
st.set_page_config(
    page_title="Gestion des Déchets et Recyclage",
    page_icon=":recycle:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Titre ---
st.title("Tableau de Bord de Gestion des Déchets et Recyclage à Kinshasa")
st.header("Optimisation de la Gestion des Déchets et Encouragement au Recyclage")

# --- Introduction Professionnelle ---
st.markdown("""
Bienvenue dans l'outil de gestion des déchets et recyclage pour la ville de Kinshasa. Cette plateforme permet de suivre en temps réel 
les points de collecte des déchets, leur taux de remplissage, et d'estimer le recyclage potentiel de la ville. Notre objectif est de 
promouvoir une gestion efficace des déchets et encourager un recyclage responsable au sein de la communauté.

Grâce à cet outil, les autorités locales, les citoyens, et les entreprises peuvent collaborer pour améliorer la gestion des déchets 
et réduire l'empreinte écologique de la ville.
""")

# --- Données Simulées --- (exemple de points de collecte)
locations = {
    "Nom": ["Point A", "Point B", "Point C", "Point D", "Point E"],
    "Latitude": [-4.441, -4.453, -4.462, -4.437, -4.421],
    "Longitude": [15.266, 15.279, 15.285, 15.267, 15.253],
    "Capacité (kg)": [500, 800, 650, 700, 450],
    "Remplissage (%)": [random.randint(30, 90) for _ in range(5)]
}

df_locations = pd.DataFrame(locations)

# --- Affichage des données ---
st.subheader("Liste des Points de Collecte")
st.dataframe(df_locations, use_container_width=True)

# --- Carte interactive des points de collecte ---
st.subheader("Carte des Points de Collecte")

# Créer une carte de Kinshasa
map_kinshasa = folium.Map(location=[-4.441, 15.266], zoom_start=12, tiles="cartodb positron")

# Ajouter les points de collecte sur la carte
marker_cluster = MarkerCluster().add_to(map_kinshasa)
for idx, row in df_locations.iterrows():
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=f"<strong>{row['Nom']}</strong><br>Capacité: {row['Capacité (kg)']} kg<br>Remplissage: {row['Remplissage (%)']}%",
        icon=folium.Icon(color="green" if row["Remplissage (%)"] < 50 else "red")
    ).add_to(marker_cluster)

# Afficher la carte
st.components.v1.html(map_kinshasa._repr_html_(), width=700, height=500)

# --- Suivi des déchets ---
st.subheader("Suivi des Déchets : Capacité et Remplissage")
point_choisi = st.selectbox("Sélectionnez un point de collecte", df_locations["Nom"])

# Afficher les données du point choisi
point_data = df_locations[df_locations["Nom"] == point_choisi].iloc[0]
st.write(f"**Nom du Point de Collecte :** {point_data['Nom']}")
st.write(f"**Capacité Totale :** {point_data['Capacité (kg)']} kg")
st.write(f"**Remplissage Actuel :** {point_data['Remplissage (%)']}%")

# --- Graphique de remplissage des points ---
st.subheader("Graphique de Remplissage des Points de Collecte")

fig, ax = plt.subplots(figsize=(10, 6))
colors = ["green" if x < 50 else "red" for x in df_locations["Remplissage (%)"]]
ax.bar(df_locations["Nom"], df_locations["Remplissage (%)"], color=colors)
ax.set_xlabel("Points de Collecte", fontsize=12)
ax.set_ylabel("Remplissage (%)", fontsize=12)
ax.set_title("Taux de Remplissage des Points de Collecte", fontsize=14)
ax.grid(True, axis="y", linestyle="--", alpha=0.7)

st.pyplot(fig)

# --- Estimation du recyclage ---
st.subheader("Estimation du Taux de Recyclage")
taux_recyclage = st.slider("Sélectionnez un taux de recyclage estimé (%)", min_value=0, max_value=100, value=50)

# Calcul des déchets recyclés
dechets_recycles = (df_locations["Capacité (kg)"] * taux_recyclage / 100).sum()
st.write(f"En supposant un taux de recyclage de {taux_recyclage}%, vous pourriez recycler jusqu'à **{dechets_recycles} kg** de déchets.")

# --- Recommandations pour améliorer le recyclage ---
st.subheader("Recommandations pour Améliorer le Recyclage")
if taux_recyclage < 50:
    st.warning("Le taux de recyclage est relativement faible. Voici quelques recommandations :")
    st.write("1. Installer davantage de points de collecte séparés pour les matériaux recyclables.")
    st.write("2. Augmenter les campagnes de sensibilisation à la population sur l'importance du recyclage.")
    st.write("3. Offrir des incitations pour les citoyens qui trient leurs déchets.")
else:
    st.success("Le taux de recyclage semble optimal. Continuez ainsi pour maintenir une ville propre et durable!")

# --- Effets visuels ---
st.success("Analyse et suivi des déchets réalisés avec succès!")
st.info("Données mises à jour en temps réel.")
