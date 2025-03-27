import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium
import plotly.express as px
from datetime import datetime, timedelta
import random

# --- Configuration de la page ---
st.set_page_config(
    page_title="EcoTrack Kinshasa - Gestion des Déchets par Commune",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Liste des 24 communes de Kinshasa ---
COMMUNES = [
    "Bandalungwa", "Barumbu", "Bumbu", "Gombe", "Kalamu", "Kasa-Vubu",
    "Kimbanseke", "Kinshasa", "Kintambo", "Kisenso", "Lemba", "Limete",
    "Lingwala", "Makala", "Maluku", "Masina", "Matete", "Mont-Ngafula",
    "Ndjili", "Ngaba", "Ngaliema", "Ngiri-Ngiri", "Nsele", "Selembao"
]

# --- Style CSS personnalisé ---
st.markdown("""
    <style>
        .main {
            background-color: #f5f5f5;
        }
        .header {
            color: #2e8b57;
        }
        .metric-card {
            background-color: white;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 15px;
        }
        .commune-selector {
            background-color: #2e8b57;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
        }
        .stSelectbox > div > div > div {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Fonctions de chargement des données ---
@st.cache_data(ttl=3600)
def load_waste_data():
    """Charge les données simulées des points de collecte avec répartition par commune"""
    np.random.seed(42)
    num_points = 240  # 10 points par commune en moyenne
    
    # Création des données avec répartition par commune
    data = {
        "ID": [f"P-{i:04d}" for i in range(1, num_points+1)],
        "Nom": [f"Point {chr(65+i%26)}{i//26}" for i in range(num_points)],
        "Commune": np.random.choice(COMMUNES, num_points),
        "Latitude": [],
        "Longitude": [],
        "Type": np.random.choice(["Standard", "Recyclage", "Dangereux", "Organique"], num_points, p=[0.5, 0.3, 0.1, 0.1]),
        "Capacité (kg)": np.random.randint(200, 1200, num_points),
        "Remplissage (%)": np.random.randint(10, 95, num_points),
        "Dernière collecte": [datetime.now() - timedelta(days=np.random.randint(1, 30)) for _ in range(num_points)],
        "Statut": np.random.choice(["Actif", "Maintenance", "Plein"], num_points, p=[0.85, 0.1, 0.05])
    }
    
    # Génération de coordonnées réalistes par commune
    commune_centers = {
        "Gombe": (-4.3056, 15.3017),
        "Kinshasa": (-4.3250, 15.3222),
        "Ngaliema": (-4.3500, 15.2500),
        # ... (ajouter les centres pour les autres communes)
    }
    
    for i in range(num_points):
        commune = data["Commune"][i]
        base_lat, base_lon = commune_centers.get(commune, (-4.441, 15.266))
        data["Latitude"].append(base_lat + random.uniform(-0.03, 0.03))
        data["Longitude"].append(base_lon + random.uniform(-0.03, 0.03))
    
    df = pd.DataFrame(data)
    df["Prochaine collecte"] = df["Dernière collecte"] + pd.to_timedelta(np.random.randint(3, 14, num_points), 'days')
    return df

# --- Chargement des données ---
df_locations = load_waste_data()

# --- Sidebar ---
with st.sidebar:
    st.image("https://via.placeholder.com/150x50?text=EcoTrack+Logo", width=150)
    st.title("Filtres")
    
    # Sélection de la commune
    selected_commune = st.selectbox(
        "Sélectionnez une commune",
        options=["Toutes les communes"] + COMMUNES,
        index=0
    )
    
    # Filtres supplémentaires
    selected_types = st.multiselect(
        "Types de points de collecte",
        options=df_locations["Type"].unique(),
        default=df_locations["Type"].unique()
    )
    
    fill_level = st.slider(
        "Niveau de remplissage minimum (%)",
        min_value=0, max_value=100, value=0
    )
    
    status_filter = st.multiselect(
        "Statut des points",
        options=df_locations["Statut"].unique(),
        default=["Actif"]
    )
    
    st.divider()
    st.markdown("**Métriques clés**")
    
    # Filtrage des données en fonction de la commune sélectionnée
    if selected_commune != "Toutes les communes":
        commune_df = df_locations[df_locations["Commune"] == selected_commune]
    else:
        commune_df = df_locations
    
    total_capacity = commune_df["Capacité (kg)"].sum()
    avg_fill = commune_df["Remplissage (%)"].mean()
    urgent_points = commune_df[commune_df["Remplissage (%)"] > 80].shape[0]
    
    st.metric("Capacité totale", f"{total_capacity:,} kg")
    st.metric("Remplissage moyen", f"{avg_fill:.1f}%")
    st.metric("Points urgents", urgent_points)

# --- Filtrage des données ---
filtered_df = df_locations[
    (df_locations["Type"].isin(selected_types)) &
    (df_locations["Remplissage (%)"] >= fill_level) &
    (df_locations["Statut"].isin(status_filter))
]

if selected_commune != "Toutes les communes":
    filtered_df = filtered_df[filtered_df["Commune"] == selected_commune]

# --- En-tête ---
st.title(f"♻ EcoTrack Kinshasa - {selected_commune if selected_commune != 'Toutes les communes' else 'Ville de Kinshasa'}")
st.markdown("**Tableau de bord intelligent pour la gestion des déchets par commune**")

# --- KPI Cards ---
st.subheader("Indicateurs Clés de Performance")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f'<div class="metric-card"><h3>Points de Collecte</h3><p style="font-size: 24px; color: #2e8b57;">{len(filtered_df):,}</p></div>', unsafe_allow_html=True)

with kpi2:
    critical_points = filtered_df[filtered_df["Remplissage (%)"] > 85].shape[0]
    color = "#d62728" if critical_points > 0 else "#2e8b57"
    st.markdown(f'<div class="metric-card"><h3>Points Critiques</h3><p style="font-size: 24px; color: {color};">{critical_points}</p></div>', unsafe_allow_html=True)

with kpi3:
    recycling_points = filtered_df[filtered_df["Type"] == "Recyclage"].shape[0]
    st.markdown(f'<div class="metric-card"><h3>Points de Recyclage</h3><p style="font-size: 24px; color: #2e8b57;">{recycling_points}</p></div>', unsafe_allow_html=True)

with kpi4:
    next_collections = filtered_df[filtered_df["Prochaine collecte"] < datetime.now() + timedelta(days=3)].shape[0]
    st.markdown(f'<div class="metric-card"><h3>Collectes Imminentes</h3><p style="font-size: 24px; color: #d62728;">{next_collections}</p></div>', unsafe_allow_html=True)

# --- Carte Interactive ---
st.markdown("---")
st.subheader("🌍 Carte Interactive des Points de Collecte")

if not filtered_df.empty:
    col1, col2 = st.columns([3, 1])
    with col1:
        map_center = [filtered_df["Latitude"].mean(), filtered_df["Longitude"].mean()]
        m = folium.Map(location=map_center, zoom_start=13 if selected_commune != "Toutes les communes" else 11, tiles="cartodb positron")
        
        marker_cluster = MarkerCluster().add_to(m)
        
        for idx, row in filtered_df.iterrows():
            fill_color = "green" if row["Remplissage (%)"] < 50 else "orange" if row["Remplissage (%)"] < 80 else "red"
            
            popup_content = f"""
            <div style="width: 250px;">
                <h4>{row['Nom']}</h4>
                <p><strong>Commune:</strong> {row['Commune']}</p>
                <p><strong>Type:</strong> {row['Type']}</p>
                <p><strong>Remplissage:</strong> <span style="color: {fill_color}">{row['Remplissage (%)']}%</span></p>
            </div>
            """
            
            folium.Marker(
                location=[row["Latitude"], row["Longitude"]],
                popup=folium.Popup(popup_content, max_width=300),
                icon=folium.Icon(color=fill_color, icon="trash", prefix="fa")
            ).add_to(marker_cluster)
        
        st_folium(m, width=1200, height=500)
    
    with col2:
        st.markdown("**Légende de la carte**")
        st.markdown("""
        - 🟢 Remplissage < 50%
        - 🟠 Remplissage 50-80%
        - 🔴 Remplissage > 80%
        """)
        
        st.markdown("**Répartition par type**")
        type_counts = filtered_df["Type"].value_counts()
        fig_type = px.pie(type_counts, values=type_counts.values, names=type_counts.index)
        st.plotly_chart(fig_type, use_container_width=True)
else:
    st.warning("Aucun point de collecte ne correspond aux filtres sélectionnés")

# --- Analyse par Commune ---
st.markdown("---")
st.subheader("📊 Analyse Comparative par Commune")

commune_stats = df_locations.groupby("Commune").agg({
    "ID": "count",
    "Capacité (kg)": "sum",
    "Remplissage (%)": "mean",
    "Type": lambda x: (x == "Recyclage").sum()
}).rename(columns={
    "ID": "Nombre de points",
    "Capacité (kg)": "Capacité totale (kg)",
    "Type": "Points de recyclage"
})

# Ajout d'une colonne de classement
commune_stats["Classement"] = commune_stats["Nombre de points"].rank(ascending=False)

tab1, tab2, tab3 = st.tabs(["Tableau des communes", "Cartographie des performances", "Indicateurs clés"])

with tab1:
    st.dataframe(
        commune_stats.sort_values("Classement"),
        use_container_width=True
    )

with tab2:
    # Création d'une carte choroplèthe des communes
    st.markdown("### Taux de remplissage moyen par commune")
    
    # Création d'un DataFrame avec des coordonnées approximatives pour chaque commune
    commune_geo = pd.DataFrame({
        "Commune": COMMUNES,
        "Latitude": [-4.3 + i*0.01 for i in range(24)],  # Coordonnées simulées
        "Longitude": [15.3 - i*0.01 for i in range(24)]   # Coordonnées simulées
    })
    
    commune_merged = commune_geo.merge(commune_stats.reset_index(), on="Commune")
    
    fig = px.scatter_mapbox(
        commune_merged,
        lat="Latitude",
        lon="Longitude",
        size="Nombre de points",
        color="Remplissage (%)",
        hover_name="Commune",
        hover_data=["Capacité totale (kg)", "Points de recyclage"],
        zoom=10,
        title="Performance des communes en gestion des déchets",
        color_continuous_scale="RdYlGn_r"  # Rouge pour haut remplissage, vert pour bas
    )
    
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("### Top 5 des communes")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Plus de points de collecte**")
        top_capacity = commune_stats.sort_values("Nombre de points", ascending=False).head(5)
        st.dataframe(top_capacity[["Nombre de points"]])
    
    with col2:
        st.markdown("**Meilleur remplissage**")
        best_fill = commune_stats.sort_values("Remplissage (%)").head(5)
        st.dataframe(best_fill[["Remplissage (%)"]].style.format("{:.1f}%"))
    
    with col3:
        st.markdown("**Plus de recyclage**")
        top_recycle = commune_stats.sort_values("Points de recyclage", ascending=False).head(5)
        st.dataframe(top_recycle[["Points de recyclage"]])

# --- Module de Recyclage par Commune ---
st.markdown("---")
st.subheader("♻ Stratégie de Recyclage par Commune")

if selected_commune != "Toutes les communes":
    st.markdown(f"### Analyse pour la commune de {selected_commune}")
    
    commune_data = df_locations[df_locations["Commune"] == selected_commune]
    total_waste = commune_data["Capacité (kg)"].sum() * (commune_data["Remplissage (%)"].mean() / 100)
    recyclable_waste = total_waste * 0.65
    
    col1, col2 = st.columns(2)
    
    with col1:
        taux_recyclage = st.slider(
            f"Taux de recyclage cible pour {selected_commune} (%)",
            min_value=0, max_value=100, value=30
        )
        
        potential_recycled = recyclable_waste * (taux_recyclage / 100)
        st.metric("Potentiel de recyclage", f"{potential_recycled:,.0f} kg")
    
    with col2:
        st.markdown("**Comparaison avec la moyenne de Kinshasa**")
        avg_city_recycle = 35  # Valeur simulée
        diff = taux_recyclage - avg_city_recycle
        
        if diff > 0:
            st.success(f"Supérieur de {diff}% à la moyenne urbaine")
        elif diff < 0:
            st.error(f"Inférieur de {abs(diff)}% à la moyenne urbaine")
        else:
            st.info("Égal à la moyenne urbaine")
        
        st.markdown("**Recommandations spécifiques**")
        if taux_recyclage < 25:
            st.error("Niveau critique - Actions immédiates nécessaires")
        elif taux_recyclage < 40:
            st.warning("Niveau modéré - Plan d'amélioration requis")
        else:
            st.success("Performance satisfaisante - Maintenir les efforts")
else:
    st.markdown("Sélectionnez une commune spécifique pour voir les recommandations de recyclage détaillées")

# --- Pied de page ---
st.markdown("---")
st.markdown('<div style="text-align: center; padding: 10px; background-color: #2e8b57; color: white;">© 2023 EcoTrack Kinshasa - Données simulées pour démonstration</div>', unsafe_allow_html=True)
