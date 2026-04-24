# ============================================================
# Connexion MySQL -- Dashboard Streamlit
# Master FAVD -- Visualisation des Données Massives
# ============================================================

import mysql.connector
import pandas as pd
import streamlit as st
import os


def get_connection():
    """
    Crée et retourne une connexion MySQL.
    Utilise st.cache_resource pour ne pas
    reconnecter à chaque rechargement de page.
    """
    return mysql.connector.connect(
        host     = os.getenv('MYSQL_HOST',          'localhost'),
        port     = int(os.getenv('MYSQL_PORT',      '3307')),
        user     = os.getenv('MYSQL_USER',          'root'),
        password = os.getenv('MYSQL_ROOT_PASSWORD', 'rootpassword'),
        database = os.getenv('MYSQL_DATABASE',      'retail_dwh'),
    )


@st.cache_data(ttl=300)
def run_query(query: str) -> pd.DataFrame:
    """
    Exécute une requête SQL et retourne un DataFrame.
    Les résultats sont mis en cache 5 minutes (ttl=300).

    Args:
        query: Requête SQL à exécuter

    Returns:
        DataFrame avec les résultats
    """
    try:
        conn = get_connection()
        df   = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f'Erreur de connexion : {str(e)}')
        return pd.DataFrame()


def get_kpi_ca_magasins() -> pd.DataFrame:
    """KPI A : CA par magasin."""
    return run_query("""
        SELECT
            s.store_name,
            s.governorate,
            s.region,
            SUM(f.total_ttc)  AS ca_total,
            COUNT(f.sale_id)  AS nb_transactions,
            AVG(f.total_ttc)  AS panier_moyen
        FROM fact_sales f
        JOIN dim_store s ON f.store_id = s.store_id
        GROUP BY s.store_name, s.governorate, s.region
        ORDER BY ca_total DESC
    """)


def get_kpi_evolution_mensuelle() -> pd.DataFrame:
    """KPI B : Evolution mensuelle des ventes."""
    return run_query("""
        SELECT
            d.year,
            d.month,
            d.month_name,
            SUM(f.total_ttc)  AS ca_mensuel,
            SUM(f.quantity)   AS qte_vendue,
            COUNT(f.sale_id)  AS nb_transactions
        FROM fact_sales f
        JOIN dim_date d ON f.date_id = d.date_id
        GROUP BY d.year, d.month, d.month_name
        ORDER BY d.year, d.month
    """)


def get_kpi_top_produits() -> pd.DataFrame:
    """KPI C : Top 10 produits."""
    return run_query("""
        SELECT
            p.product_name,
            p.category,
            p.brand,
            SUM(f.quantity)       AS total_qte,
            SUM(f.total_ttc)      AS ca_total,
            AVG(f.gross_margin)   AS marge_moyenne
        FROM fact_sales f
        JOIN dim_product p ON f.product_id = p.product_id
        GROUP BY p.product_name, p.category, p.brand
        ORDER BY ca_total DESC
        LIMIT 10
    """)


def get_kpi_promotions() -> pd.DataFrame:
    """KPI D : Impact des promotions."""
    return run_query("""
        SELECT
            pr.promo_name,
            pr.promo_type,
            pr.discount_rate,
            COUNT(f.sale_id)      AS nb_ventes_promo,
            SUM(f.total_ttc)      AS ca_promo,
            AVG(f.discount_pct)   AS remise_moyenne_pct
        FROM fact_sales f
        JOIN dim_promotion pr ON f.promo_id = pr.promo_id
        GROUP BY pr.promo_name, pr.promo_type, pr.discount_rate
        ORDER BY ca_promo DESC
    """)


def get_kpi_panier_moyen() -> pd.DataFrame:
    """KPI E : Panier moyen par segment client."""
    return run_query("""
        SELECT
            c.segment,
            c.age_group,
            c.governorate,
            COUNT(DISTINCT f.sale_id)  AS nb_achats,
            AVG(f.total_ttc)           AS panier_moyen,
            SUM(f.total_ttc)           AS ca_total_segment
        FROM fact_sales f
        JOIN dim_customer c ON f.customer_id = c.customer_id
        GROUP BY c.segment, c.age_group, c.governorate
        ORDER BY panier_moyen DESC
    """)