# ============================================================
# KPI E : Panier moyen par segment client
# Master FAVD -- Visualisation des Données Massives
# ============================================================

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import get_kpi_panier_moyen
from utils.charts import bar_chart_panier_moyen

# ── Configuration page ───────────────────────────────────────
st.set_page_config(
    page_title="Panier Moyen",
    page_icon="🛍️",
    layout="wide",
)

# ── Titre ────────────────────────────────────────────────────
st.title("🛍️ KPI E — Panier Moyen par Segment Client")
st.markdown("Analyse du panier moyen par segment et tranche d'âge.")
st.divider()

# ── Chargement des données ───────────────────────────────────
with st.spinner('Chargement des données...'):
    df = get_kpi_panier_moyen()

if df.empty:
    st.error('Impossible de charger les données. Vérifiez la connexion MySQL.')
    st.stop()

# ── Filtres ──────────────────────────────────────────────────
st.subheader("🔍 Filtres")
col1, col2 = st.columns(2)

with col1:
    segments = ['Tous'] + sorted(df['segment'].unique().tolist())
    selected_segment = st.selectbox('Segment client', segments)

with col2:
    age_groups = ['Tous'] + sorted(df['age_group'].unique().tolist())
    selected_age = st.selectbox("Tranche d'âge", age_groups)

# Appliquer les filtres
df_filtered = df.copy()
if selected_segment != 'Tous':
    df_filtered = df_filtered[df_filtered['segment'] == selected_segment]
if selected_age != 'Tous':
    df_filtered = df_filtered[df_filtered['age_group'] == selected_age]

st.divider()

# ── Métriques ────────────────────────────────────────────────
st.subheader("📊 Métriques")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Panier Moyen Global (DT)",
        value=f"{df_filtered['panier_moyen'].mean():,.2f}"
        if not df_filtered.empty else 'N/A'
    )
with col2:
    st.metric(
        label="CA Total Segment (DT)",
        value=f"{df_filtered['ca_total_segment'].sum():,.0f}"
        if not df_filtered.empty else 'N/A'
    )
with col3:
    st.metric(
        label="Nb Achats Total",
        value=f"{df_filtered['nb_achats'].sum():,.0f}"
        if not df_filtered.empty else 'N/A'
    )

st.divider()

# ── Graphique ────────────────────────────────────────────────
st.subheader("🛍️ Panier Moyen par Segment")
bar_chart_panier_moyen(df_filtered)
st.divider()

# ── Tableau détaillé ─────────────────────────────────────────
st.subheader("📋 Tableau Détaillé")
st.dataframe(
    df_filtered[[
        'segment', 'age_group', 'governorate',
        'nb_achats', 'panier_moyen', 'ca_total_segment'
    ]].rename(columns={
        'segment':          'Segment',
        'age_group':        "Tranche d'âge",
        'governorate':      'Gouvernorat',
        'nb_achats':        'Nb Achats',
        'panier_moyen':     'Panier Moyen (DT)',
        'ca_total_segment': 'CA Total (DT)',
    }),
    use_container_width=True,
)