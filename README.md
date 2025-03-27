# EcoTrack Kinshasa - Plateforme de Gestion des Déchets

## 📌 Description

EcoTrack Kinshasa est une application web interactive conçue pour optimiser la gestion des déchets et promouvoir le recyclage dans les 24 communes de Kinshasa. Cette plateforme permet de :

- Visualiser en temps réel les points de collecte
- Analyser les taux de remplissage
- Planifier les tournées de collecte
- Évaluer le potentiel de recyclage par commune
- Comparer les performances entre communes

## ✨ Fonctionnalités Principales

### 🗺️ Cartographie Interactive
- Visualisation des points de collecte sur une carte dynamique
- Filtrage par type de déchets, niveau de remplissage et statut
- Clustering automatique des points
- Affichage heatmap des zones critiques

### 📊 Tableaux de Bord
- Indicateurs clés de performance (KPI) en temps réel
- Analyse comparative entre communes
- Classements des communes par différents critères
- Visualisations graphiques interactives

### ♻ Module Recyclage
- Estimation du potentiel de recyclage par commune
- Calcul des impacts environnementaux
- Recommandations personnalisées
- Comparaison avec les moyennes urbaines

### ⚙️ Fonctionnalités Avancées
- Filtres dynamiques multicritères
- Export des données filtrées
- Simulation d'optimisation des tournées
- Système d'alertes et de signalement

## 🛠 Installation

1. **Prérequis** :
   - Python 3.8+
   - pip

2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application** :
   ```bash
   streamlit run app.py
   ```

## 📦 Structure du Projet

```
EcoTrack-Kinshasa/
├── app.py                # Code principal de l'application
├── requirements.txt      # Dépendances Python
├── README.md             # Ce fichier
└── assets/               # Dossier pour les ressources
    ├── images/           # Images et logos
    └── data/             # Jeux de données (optionnel)
```

## 📚 Dépendances

- `streamlit` - Framework pour l'interface web
- `pandas` - Manipulation des données
- `numpy` - Calculs scientifiques
- `folium` - Cartographie interactive
- `plotly` - Visualisations avancées
- `streamlit-folium` - Intégration Folium dans Streamlit

## 🌍 Données

L'application utilise actuellement des données simulées pour :
- 240 points de collecte répartis sur 24 communes
- 4 types de déchets (Standard, Recyclage, Dangereux, Organique)
- Niveaux de remplissage actualisés en temps réel

## 🚀 Déploiement

L'application peut être déployée sur :
- Streamlit Sharing
- Heroku
- AWS Elastic Beanstalk
- Google Cloud Run

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.


---

<div align="center">
  <em>Fait avec ♥ pour une Kinshasa plus propre</em>
</div>
