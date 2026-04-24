# ============================================================
# Transform -- Nettoyage et transformation des données
# Master FAVD -- Visualisation des Données Massives
# ============================================================

import pandas as pd
import numpy as np
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)


class DataTransformer:
    """
    Classe responsable du nettoyage et de la transformation
    des données avant chargement dans le DWH.
    """

    def __init__(self, data: dict):
        self.data = data

    def transform_dim_date(self, df):
        """Transforme la dimension date."""
        logger.info('Transformation dim_date...')

        # Convertir full_date en datetime
        df['full_date'] = pd.to_datetime(df['full_date'])

        # Supprimer les doublons
        df = df.drop_duplicates(subset=['date_id'])

        # Remplir les valeurs nulles
        df['is_weekend'] = df['is_weekend'].fillna(False)
        df['is_holiday'] = df['is_holiday'].fillna(False)

        logger.info(f'dim_date transformée : {len(df)} lignes')
        return df

    def transform_dim_product(self, df):
        """Transforme la dimension produit."""
        logger.info('Transformation dim_product...')

        # Supprimer les doublons sur SKU
        df = df.drop_duplicates(subset=['sku'])

        # Normaliser les textes
        df['product_name'] = df['product_name'].str.strip().str.title()
        df['category']     = df['category'].str.strip()
        df['brand']        = df['brand'].str.strip().str.title()

        # Remplir les valeurs nulles
        df['sub_category'] = df['sub_category'].fillna('Général')
        df['brand']        = df['brand'].fillna('Sans Marque')
        df['is_active']    = df['is_active'].fillna(True)

        # Valider les prix
        df = df[df['list_price'] > 0]

        logger.info(f'dim_product transformée : {len(df)} lignes')
        return df

    def transform_dim_store(self, df):
        """Transforme la dimension magasin."""
        logger.info('Transformation dim_store...')

        # Supprimer les doublons
        df = df.drop_duplicates(subset=['store_code'])

        # Normaliser les textes
        df['store_name']  = df['store_name'].str.strip()
        df['city']        = df['city'].str.strip().str.title()
        df['governorate'] = df['governorate'].str.strip()
        df['region']      = df['region'].str.strip()

        # Remplir les valeurs nulles
        df['surface_sqm'] = df['surface_sqm'].fillna(0)

        logger.info(f'dim_store transformée : {len(df)} lignes')
        return df

    def transform_dim_customer(self, df):
        """Transforme la dimension client."""
        logger.info('Transformation dim_customer...')

        # Supprimer les doublons
        df = df.drop_duplicates(subset=['customer_code'])

        # Normaliser les textes
        df['full_name']   = df['full_name'].str.strip().str.title()
        df['city']        = df['city'].str.strip().str.title()
        df['governorate'] = df['governorate'].str.strip()

        # Remplir les valeurs nulles
        df['age_group']      = df['age_group'].fillna('Inconnu')
        df['segment']        = df['segment'].fillna('Bronze')
        df['loyalty_points'] = df['loyalty_points'].fillna(0)

        logger.info(f'dim_customer transformée : {len(df)} lignes')
        return df

    def transform_dim_promotion(self, df):
        """Transforme la dimension promotion."""
        logger.info('Transformation dim_promotion...')

        # Supprimer les doublons
        df = df.drop_duplicates(subset=['promo_name'])

        # Valider les taux de remise (entre 0 et 100)
        df = df[
            (df['discount_rate'] >= 0) &
            (df['discount_rate'] <= 100)
        ]

        # Convertir les dates
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['end_date']   = pd.to_datetime(df['end_date'])

        logger.info(f'dim_promotion transformée : {len(df)} lignes')
        return df

    def transform_fact_sales(self, df):
        """Transforme la table de faits."""
        logger.info('Transformation fact_sales...')

        # Supprimer les doublons
        df = df.drop_duplicates(
            subset=['date_id', 'product_id', 'customer_id', 'store_id']
        )

        # Remplir les valeurs nulles
        df['discount_pct'] = df['discount_pct'].fillna(0)
        df['promo_id']     = df['promo_id'].fillna(0).astype(int)

        # Valider les montants
        df = df[df['total_ht']  > 0]
        df = df[df['total_ttc'] > 0]
        df = df[df['quantity']  > 0]
        df = df[df['discount_pct'].between(0, 100)]

        # Recalculer la marge brute pour garantir la cohérence
        df['gross_margin'] = round(
            df['total_ht'] - df['quantity'] * df['cost_price'], 2
        )

        logger.info(f'fact_sales transformée : {len(df)} lignes')
        return df

    def run(self):
        """
        Lance la transformation complète de toutes les tables.
        Retourne un dictionnaire {table_name: DataFrame}.
        """
        logger.info('=== Démarrage transformation ===')

        transformed = {
            'dim_date':      self.transform_dim_date(
                                self.data['dim_date'].copy()),
            'dim_product':   self.transform_dim_product(
                                self.data['dim_product'].copy()),
            'dim_store':     self.transform_dim_store(
                                self.data['dim_store'].copy()),
            'dim_customer':  self.transform_dim_customer(
                                self.data['dim_customer'].copy()),
            'dim_promotion': self.transform_dim_promotion(
                                self.data['dim_promotion'].copy()),
            'fact_sales':    self.transform_fact_sales(
                                self.data['fact_sales'].copy()),
        }

        logger.info('=== Transformation terminée ===')
        return transformed