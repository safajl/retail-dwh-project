# ============================================================
# KPI C : Top 10 produits
# Master FAVD -- Visualisation des Données Massives
# ============================================================

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import get_kpi_top_produits
from utils.charts import bar_chart_top_produits

# ── Configuration page ───────────────────────────────────────
st.set_page_config(
    page_title="Top Produits",
    page_icon="🏆",
    layout="wide",
)

# ── Titre ────────────────────────────────────────────────────
st.title("🏆 KPI C — Top 10 Produits")
st.markdown("Analyse des produits les plus performants en chiffre d'affaires.")
st.divider()

# ── Chargement des données ───────────────────────────────────
with st.spinner('Chargement des données...'):
    df = get_kpi_top_produits()

if df.empty:
    st.error('Impossible de charger les données. Vérifiez la connexion MySQL.')
    st.stop()

# ── Filtres ──────────────────────────────────────────────────
st.subheader("🔍 Filtres")
col1, col2 = st.columns(2)

with col1:
    categories = ['Toutes'] + sorted(df['category'].unique().tolist())
    selected_cat = st.selectbox('Catégorie', categories)

with col2:
    top_n = st.slider('Nombre de produits', 5, 10, 10)

# Appliquer les filtres
if selected_cat != 'Toutes':
    df_filtered = df[df['category'] == selected_cat]
else:
    df_filtered = df

df_filtered = df_filtered.head(top_n)
st.divider()

# ── Métriques ────────────────────────────────────────────────
st.subheader("📊 Métriques")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="CA Total Top Produits (DT)",
        value=f"{df_filtered['ca_total'].sum():,.0f}"
    )
with col2:
    st.metric(
        label="Meilleur Produit",
        value=df_filtered.iloc[0]['product_name']
        if not df_filtered.empty else 'N/A'
    )
with col3:
    st.metric(
        label="Quantité Totale",
        value=f"{df_filtered['total_qte'].sum():,.0f}"
    )

st.divider()

# ── Graphique ────────────────────────────────────────────────
st.subheader(f"🏆 Top {top_n} Produits par CA")
bar_chart_top_produits(df_filtered)
st.divider()

# ── Tableau détaillé ─────────────────────────────────────────
st.subheader("📋 Tableau Détaillé")
st.dataframe(
    df_filtered[[
        'product_name', 'category', 'brand',
        'total_qte', 'ca_total', 'marge_moyenne'
    ]].rename(columns={
        'product_name': 'Produit',
        'category':     'Catégorie',
        'brand':        'Marque',
        'total_qte':    'Quantité Totale',
        'ca_total':     'CA Total (DT)',
        'marge_moyenne':'Marge Moyenne (DT)',
    }),
    use_container_width=True,
)