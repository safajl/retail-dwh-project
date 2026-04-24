# ============================================================
# KPI A : CA par magasin
# Master FAVD -- Visualisation des Données Massives
# ============================================================

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import get_kpi_ca_magasins
from utils.charts import bar_chart_ca_magasins, display_metrics

# ── Configuration page ───────────────────────────────────────
st.set_page_config(
    page_title="CA par Magasin",
    page_icon="🏪",
    layout="wide",
)

# ── Titre ────────────────────────────────────────────────────
st.title("🏪 KPI A — Chiffre d'Affaires par Magasin")
st.markdown("Analyse du chiffre d'affaires total par magasin et par région.")
st.divider()

# ── Chargement des données ───────────────────────────────────
with st.spinner('Chargement des données...'):
    df = get_kpi_ca_magasins()

if df.empty:
    st.error('Impossible de charger les données. Vérifiez la connexion MySQL.')
    st.stop()

# ── Métriques principales ────────────────────────────────────
st.subheader("📊 Métriques Globales")
display_metrics(df)
st.divider()

# ── Filtres ──────────────────────────────────────────────────
st.subheader("🔍 Filtres")
col1, col2 = st.columns(2)

with col1:
    regions = ['Toutes'] + sorted(df['region'].unique().tolist())
    selected_region = st.selectbox('Région', regions)

with col2:
    top_n = st.slider('Nombre de magasins à afficher', 5, 50, 10)

# Appliquer les filtres
if selected_region != 'Toutes':
    df_filtered = df[df['region'] == selected_region]
else:
    df_filtered = df

df_filtered = df_filtered.head(top_n)
st.divider()

# ── Graphique ────────────────────────────────────────────────
st.subheader(f"📈 CA Total par Magasin (Top {top_n})")
bar_chart_ca_magasins(df_filtered)
st.divider()

# ── Tableau détaillé ─────────────────────────────────────────
st.subheader("📋 Tableau Détaillé")
st.dataframe(
    df_filtered[[
        'store_name', 'governorate', 'region',
        'ca_total', 'nb_transactions', 'panier_moyen'
    ]].rename(columns={
        'store_name':      'Magasin',
        'governorate':     'Gouvernorat',
        'region':          'Région',
        'ca_total':        'CA Total (DT)',
        'nb_transactions': 'Nb Transactions',
        'panier_moyen':    'Panier Moyen (DT)',
    }),
    use_container_width=True,
)