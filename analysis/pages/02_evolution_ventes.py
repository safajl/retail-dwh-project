# ============================================================
# KPI B : Evolution mensuelle des ventes
# Master FAVD -- Visualisation des Données Massives
# ============================================================

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import get_kpi_evolution_mensuelle
from utils.charts import line_chart_evolution

# ── Configuration page ───────────────────────────────────────
st.set_page_config(
    page_title="Evolution Ventes",
    page_icon="📈",
    layout="wide",
)

# ── Titre ────────────────────────────────────────────────────
st.title("📈 KPI B — Evolution Mensuelle des Ventes")
st.markdown("Analyse de l'évolution du chiffre d'affaires mois par mois.")
st.divider()

# ── Chargement des données ───────────────────────────────────
with st.spinner('Chargement des données...'):
    df = get_kpi_evolution_mensuelle()

if df.empty:
    st.error('Impossible de charger les données. Vérifiez la connexion MySQL.')
    st.stop()

# ── Filtres ──────────────────────────────────────────────────
st.subheader("🔍 Filtres")
years = sorted(df['year'].unique().tolist())
selected_years = st.multiselect(
    'Années à afficher',
    years,
    default=years
)

df_filtered = df[df['year'].isin(selected_years)]
st.divider()

# ── Métriques ────────────────────────────────────────────────
st.subheader("📊 Métriques")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="CA Total (DT)",
        value=f"{df_filtered['ca_mensuel'].sum():,.0f}"
    )
with col2:
    st.metric(
        label="Meilleur Mois",
        value=df_filtered.loc[
            df_filtered['ca_mensuel'].idxmax(), 'month_name'
        ] if not df_filtered.empty else 'N/A'
    )
with col3:
    st.metric(
        label="Quantité Totale",
        value=f"{df_filtered['qte_vendue'].sum():,.0f}"
    )

st.divider()

# ── Graphique ────────────────────────────────────────────────
st.subheader("📈 Evolution du CA Mensuel")
line_chart_evolution(df_filtered)
st.divider()

# ── Tableau détaillé ─────────────────────────────────────────
st.subheader("📋 Tableau Détaillé")
st.dataframe(
    df_filtered[[
        'year', 'month_name', 'ca_mensuel',
        'qte_vendue', 'nb_transactions'
    ]].rename(columns={
        'year':            'Année',
        'month_name':      'Mois',
        'ca_mensuel':      'CA Mensuel (DT)',
        'qte_vendue':      'Quantité Vendue',
        'nb_transactions': 'Nb Transactions',
    }),
    use_container_width=True,
)