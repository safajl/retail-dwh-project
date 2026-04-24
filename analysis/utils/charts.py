# ============================================================
# Fonctions de visualisation -- Dashboard Streamlit
# Master FAVD -- Visualisation des Données Massives
# ============================================================

import pandas as pd
import streamlit as st


def bar_chart_ca_magasins(df: pd.DataFrame):
    """
    Affiche un bar chart du CA par magasin.
    Args:
        df: DataFrame avec colonnes store_name, ca_total
    """
    if df.empty:
        st.warning('Aucune donnée disponible.')
        return

    st.bar_chart(
        df.set_index('store_name')['ca_total']
    )


def line_chart_evolution(df: pd.DataFrame):
    """
    Affiche un line chart de l'évolution mensuelle.
    Args:
        df: DataFrame avec colonnes month_name, ca_mensuel
    """
    if df.empty:
        st.warning('Aucune donnée disponible.')
        return

    # Créer une colonne période pour l'axe X
    df['periode'] = df['year'].astype(str) + '-' + \
                    df['month'].astype(str).str.zfill(2)

    st.line_chart(
        df.set_index('periode')['ca_mensuel']
    )


def bar_chart_top_produits(df: pd.DataFrame):
    """
    Affiche un bar chart des top 10 produits.
    Args:
        df: DataFrame avec colonnes product_name, ca_total
    """
    if df.empty:
        st.warning('Aucune donnée disponible.')
        return

    st.bar_chart(
        df.set_index('product_name')['ca_total']
    )


def bar_chart_promotions(df: pd.DataFrame):
    """
    Affiche un bar chart de l'impact des promotions.
    Args:
        df: DataFrame avec colonnes promo_name, ca_promo
    """
    if df.empty:
        st.warning('Aucune donnée disponible.')
        return

    st.bar_chart(
        df.set_index('promo_name')['ca_promo']
    )


def bar_chart_panier_moyen(df: pd.DataFrame):
    """
    Affiche un bar chart du panier moyen par segment.
    Args:
        df: DataFrame avec colonnes segment, panier_moyen
    """
    if df.empty:
        st.warning('Aucune donnée disponible.')
        return

    st.bar_chart(
        df.groupby('segment')['panier_moyen'].mean()
    )


def display_metrics(df: pd.DataFrame):
    """
    Affiche les métriques principales en haut de page.
    Args:
        df: DataFrame fact_sales agrégé
    """
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label='CA Total (DT)',
            value=f"{df['ca_total'].sum():,.0f}"
            if 'ca_total' in df.columns else 'N/A'
        )
    with col2:
        st.metric(
            label='Nb Transactions',
            value=f"{df['nb_transactions'].sum():,.0f}"
            if 'nb_transactions' in df.columns else 'N/A'
        )
    with col3:
        st.metric(
            label='Panier Moyen (DT)',
            value=f"{df['panier_moyen'].mean():,.2f}"
            if 'panier_moyen' in df.columns else 'N/A'
        )
    with col4:
        st.metric(
            label='Nb Magasins',
            value=f"{len(df)}"
            if not df.empty else 'N/A'
        )