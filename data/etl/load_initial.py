# ============================================================
# Load Initial -- Chargement complet dans le DWH
# Master FAVD -- Visualisation des Données Massives
# ============================================================

import pandas as pd
import logging
from sqlalchemy import create_engine, text
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)


class DataLoaderInitial:
    """
    Classe responsable du chargement initial complet
    des données dans le DWH MySQL Cluster.
    """

    def __init__(self):
        # Récupérer les variables d'environnement
        host     = os.getenv('MYSQL_HOST',          'localhost')
        port     = os.getenv('MYSQL_PORT',          '3307')
        user     = os.getenv('MYSQL_USER',          'root')
        password = os.getenv('MYSQL_ROOT_PASSWORD', 'rootpassword')
        database = os.getenv('MYSQL_DATABASE',      'retail_dwh')

        # Créer la connexion SQLAlchemy
        self.engine = create_engine(
            f'mysql+mysqlconnector://{user}:{password}'
            f'@{host}:{port}/{database}'
        )
        logger.info(f'Connexion établie : {host}:{port}/{database}')

    def load_table(self, df, table_name):
        """
        Charge un DataFrame dans une table MySQL.
        Remplace la table entière (chargement initial).
        """
        logger.info(f'Chargement {table_name} : {len(df)} lignes...')

        df.to_sql(
            name=table_name,
            con=self.engine,
            if_exists='append',   # append car la table existe déjà
            index=False,
            chunksize=1000,       # Charger par lots de 1000
        )

        logger.info(f'{table_name} chargé avec succès ✓')

    def verify_load(self, table_name, expected_count):
        """Vérifie que le nombre de lignes chargées est correct."""
        with self.engine.connect() as conn:
            result = conn.execute(
                text(f'SELECT COUNT(*) FROM {table_name}')
            )
            actual_count = result.scalar()

        if actual_count >= expected_count:
            logger.info(
                f'Vérification {table_name} OK : '
                f'{actual_count} lignes chargées'
            )
        else:
            logger.warning(
                f'Vérification {table_name} : '
                f'attendu {expected_count}, chargé {actual_count}'
            )

    def run(self, data: dict):
        """
        Lance le chargement initial de toutes les tables.
        Ordre important : dimensions avant faits.
        """
        logger.info('=== Démarrage chargement initial ===')

        # Ordre de chargement : dimensions d'abord
        order = [
            'dim_date',
            'dim_product',
            'dim_store',
            'dim_customer',
            'dim_promotion',
            'fact_sales',
        ]

        for table in order:
            if table in data:
                self.load_table(data[table], table)
                self.verify_load(table, len(data[table]))

        logger.info('=== Chargement initial terminé ===')


if __name__ == '__main__':
    # Test rapide
    loader = DataLoaderInitial()
    print('Connexion OK !')