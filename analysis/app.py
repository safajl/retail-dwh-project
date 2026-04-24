# ============================================================
# Application principale -- Dashboard Streamlit
# Master FAVD -- Visualisation des Données Massives
# ============================================================

import streamlit as st
import sys
import os

# Ajouter le dossier parent au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ── Configuration de la page ─────────────────────────────────
st.set_page_config(
    page_title="DWH Retail — Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Style CSS personnalisé ───────────────────────────────────
st.markdown("""
    <style>
        .main-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1B2A4A;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        .sub-title {
            font-size: 1.2rem;
            color: #6B7280;
            text-align: center;
            margin-bottom: 2rem;
        }
        .kpi-card {
            background-color: #EFF6FF;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# ── Titre principal ──────────────────────────────────────────
st.markdown(
    '<div class="main-title">🛒 DWH Retail — Dashboard Analytique</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="sub-title">Master FAVD — Visualisation des Données Massives</div>',
    unsafe_allow_html=True
)

st.divider()

# ── Description ──────────────────────────────────────────────
st.markdown("""
### 📊 Bienvenue sur le Dashboard DWH Retail

Ce dashboard présente les **5 KPIs** principaux de l'analyse des ventes
de la chaîne RetailTN, basés sur un Data Warehouse MySQL Cluster NDB.

---

### 📌 Navigation

Utilisez le **menu à gauche** pour accéder aux analyses :

| Page | KPI | Description |
|------|-----|-------------|
| 🏪 CA Magasins | KPI A | Chiffre d'affaires par magasin |
| 📈 Evolution Ventes | KPI B | Evolution mensuelle des ventes |
| 🏆 Top Produits | KPI C | Top 10 produits les plus vendus |
| 🎯 Promotions | KPI D | Impact des promotions sur les ventes |
| 🛍️ Panier Moyen | KPI E | Panier moyen par segment client |

---

### 🏗️ Architecture

- **Base de données** : MySQL Cluster NDB (1 Management + 2 Data Nodes + 1 SQL Node)
- **ETL** : Python 3.12 (Faker, Pandas, SQLAlchemy)
- **Environnements** : DEV / TEST / PROD / DAC
- **Modélisation** : Schéma en étoile (Star Schema)
""")

st.divider()

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.image(
        "https://img.icons8.com/color/96/000000/shopping-cart.png",
        width=80
    )
    st.title("DWH Retail")
    st.markdown("**Master FAVD**")
    st.markdown("Visualisation des Données Massives")
    st.divider()
    st.markdown("### 📋 Informations")
    st.markdown(f"- **Environnement** : {os.getenv('ENVIRONMENT_NAME', 'DEV')}")
    st.markdown(f"- **Base** : {os.getenv('MYSQL_DATABASE', 'retail_dwh')}")
    st.markdown(f"- **Port** : {os.getenv('MYSQL_PORT', '3307')}")
    st.divider()
    st.markdown("### 🔗 Pages disponibles")
    st.page_link("pages/01_ca_magasins.py",      label="🏪 CA Magasins")
    st.page_link("pages/02_evolution_ventes.py",  label="📈 Evolution Ventes")
    st.page_link("pages/03_top_produits.py",      label="🏆 Top Produits")
    st.page_link("pages/04_promotions.py",        label="🎯 Promotions")
    st.page_link("pages/05_panier_moyen.py",      label="🛍️ Panier Moyen")