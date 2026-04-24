# ============================================================
# Extract -- Lecture des fichiers CSV générés
# Master FAVD -- Visualisation des Données Massives
# ============================================================

import pandas as pd
import logging
import os

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)


class DataExtractor:
    """
    Classe responsable de l'extraction des données
    depuis les fichiers CSV sources.
    """

    def __init__(self, raw_path='data/raw'):
        self.raw_path = raw_path
        self.tables = [
            'dim_date',
            'dim_product',
            'dim_store',
            'dim_customer',
            'dim_promotion',
            'fact_sales',
        ]

    def extract_table(self, table_name):
        """Lit un fichier CSV et retourne un DataFrame."""
        filepath = os.path.join(self.raw_path, f'{table_name}.csv')

        if not os.path.exists(filepath):
            logger.error(f'Fichier introuvable : {filepath}')
            raise FileNotFoundError(f'Fichier introuvable : {filepath}')

        df = pd.read_csv(filepath)
        logger.info(f'Extrait {table_name} : {len(df)} lignes')
        return df

    def validate(self, df, table_name):
        """Valide les données extraites."""
        # Vérifier que le DataFrame n'est pas vide
        if df.empty:
            raise ValueError(f'{table_name} est vide !')

        # Vérifier les colonnes obligatoires selon la table
        required_cols = {
            'dim_date':      ['date_id', 'full_date', 'year', 'month'],
            'dim_product':   ['sku', 'product_name', 'category'],
            'dim_store':     ['store_code', 'store_name', 'governorate'],
            'dim_customer':  ['customer_code', 'full_name'],
            'dim_promotion': ['promo_name', 'promo_type', 'discount_rate'],
            'fact_sales':    ['date_id', 'product_id', 'customer_id',
                              'store_id', 'quantity', 'total_ttc'],
        }

        if table_name in required_cols:
            for col in required_cols[table_name]:
                if col not in df.columns:
                    raise ValueError(
                        f'Colonne manquante dans {table_name} : {col}'
                    )

        logger.info(f'Validation OK pour {table_name}')
        return True

    def run(self):
        """
        Lance l'extraction complète de toutes les tables.
        Retourne un dictionnaire {table_name: DataFrame}.
        """
        logger.info('=== Démarrage extraction ===')
        data = {}

        for table in self.tables:
            df = self.extract_table(table)
            self.validate(df, table)
            data[table] = df

        logger.info(f'=== Extraction terminée : {len(data)} tables ===')
        return data


if __name__ == '__main__':
    extractor = DataExtractor()
    data = extractor.run()
    for table, df in data.items():
        print(f'{table} : {len(df)} lignes')