import streamlit as st

# --- Titre de la page ---
st.set_page_config(page_title="À Propos - Gestion des Déchets à Kinshasa", page_icon=":recycle:", layout="centered")
st.title("Page À Propos")

# --- Section Description ---
st.header("À propos de cette application")
st.markdown("""
    🌍 **Cette application est dédiée à la gestion des déchets et au recyclage à Kinshasa.**
    Son objectif est d'améliorer l'efficacité des points de collecte, de promouvoir le recyclage et de 
    fournir une visibilité en temps réel sur l'état des déchets collectés.

    **Les principales fonctionnalités de l'application incluent :**
    - 🌍 **Visualisation des points de collecte** sur une carte interactive.
    - 📊 **Suivi des niveaux de remplissage** des bacs.
    - ♻️ **Estimation du recyclage potentiel** des déchets.
    - 💡 **Recommandations pour améliorer le recyclage**.

    Cette application a été développée pour **sensibiliser les citoyens** et les **autorités locales** à l'importance de la gestion des déchets et du recyclage, afin de contribuer à un environnement plus propre et durable.
""")

# --- Section des Liens ---
st.markdown("""
    **Revenez à la page principale de l'application :**
    - [Cliquez ici pour revenir à la page principale](app.py)
""")

# --- Contact ---
st.subheader("Contact")
st.markdown("""
    Si vous avez des questions ou des suggestions concernant cette application, n'hésitez pas à nous contacter :

    📧 **Email :** [juniorboukassa02@gmail.com](mailto:juniorboukassa02@gmail.com)  
    📱 **Téléphone :** +243 850 130 917

    **Adresse :** Kinshasa, République Démocratique du Congo.
""")

