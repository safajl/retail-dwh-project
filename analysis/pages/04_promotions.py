# ============================================================
# KPI D : Impact des promotions
# Master FAVD -- Visualisation des Données Massives
# ============================================================

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import get_kpi_promotions
from utils.charts import bar_chart_promotions

# ── Configuration page ───────────────────────────────────────
st.set_page_config(
    page_title="Promotions",
    page_icon="🎯",
    layout="wide",
)

# ── Titre ────────────────────────────────────────────────────
st.title("🎯 KPI D — Impact des Promotions")
st.markdown("Analyse de l'impact des promotions sur le chiffre d'affaires.")
st.divider()

# ── Chargement des données ───────────────────────────────────
with st.spinner('Chargement des données...'):
    df = get_kpi_promotions()

if df.empty:
    st.error('Impossible de charger les données. Vérifiez la connexion MySQL.')
    st.stop()

# ── Filtres ──────────────────────────────────────────────────
st.subheader("🔍 Filtres")
promo_types = ['Tous'] + sorted(df['promo_type'].unique().tolist())
selected_type = st.selectbox('Type de promotion', promo_types)

if selected_type != 'Tous':
    df_filtered = df[df['promo_type'] == selected_type]
else:
    df_filtered = df

st.divider()

# ── Métriques ────────────────────────────────────────────────
st.subheader("📊 Métriques")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="CA Total Promos (DT)",
        value=f"{df_filtered['ca_promo'].sum():,.0f}"
    )
with col2:
    st.metric(
        label="Nb Ventes en Promo",
        value=f"{df_filtered['nb_ventes_promo'].sum():,.0f}"
    )
with col3:
    st.metric(
        label="Remise Moyenne (%)",
        value=f"{df_filtered['remise_moyenne_pct'].mean():,.1f}%"
        if not df_filtered.empty else 'N/A'
    )

st.divider()

# ── Graphique ────────────────────────────────────────────────
st.subheader("🎯 CA par Promotion")
bar_chart_promotions(df_filtered)
st.divider()

# ── Tableau détaillé ─────────────────────────────────────────
st.subheader("📋 Tableau Détaillé")
st.dataframe(
    df_filtered[[
        'promo_name', 'promo_type', 'discount_rate',
        'nb_ventes_promo', 'ca_promo', 'remise_moyenne_pct'
    ]].rename(columns={
        'promo_name':        'Promotion',
        'promo_type':        'Type',
        'discount_rate':     'Taux Remise (%)',
        'nb_ventes_promo':   'Nb Ventes',
        'ca_promo':          'CA (DT)',
        'remise_moyenne_pct':'Remise Moyenne (%)',
    }),
    use_container_width=True,
)