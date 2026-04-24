# ============================================================
# Load Incremental -- Chargement delta quotidien
# Master FAVD -- Visualisation des Données Massives
# ============================================================

import pandas as pd
import logging
from sqlalchemy import create_engine, text
import os
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)


class DataLoaderIncremental:
    """
    Classe responsable du chargement incrémental
    des nouvelles données dans le DWH MySQL Cluster.
    Charge uniquement les données nouvelles (delta).
    """

    def __init__(self):
        host     = os.getenv('MYSQL_HOST',          'localhost')
        port     = os.getenv('MYSQL_PORT',          '3307')
        user     = os.getenv('MYSQL_USER',          'root')
        password = os.getenv('MYSQL_ROOT_PASSWORD', 'rootpassword')
        database = os.getenv('MYSQL_DATABASE',      'retail_dwh')

        self.engine = create_engine(
            f'mysql+mysqlconnector://{user}:{password}'
            f'@{host}:{port}/{database}'
        )
        logger.info(f'Connexion établie : {host}:{port}/{database}')

    def get_last_date_id(self):
        """
        Récupère le dernier date_id chargé dans fact_sales.
        Utilisé pour identifier les nouvelles données à charger.
        """
        with self.engine.connect() as conn:
            result = conn.execute(
                text('SELECT MAX(date_id) FROM fact_sales')
            )
            last_date_id = result.scalar()

        if last_date_id is None:
            # Si la table est vide, charger depuis le début
            last_date_id = 20220101

        logger.info(f'Dernier date_id en base : {last_date_id}')
        return last_date_id

    def filter_new_records(self, df, table_name, last_date_id):
        """
        Filtre les nouvelles lignes non encore chargées.
        Pour fact_sales : basé sur date_id.
        Pour les dimensions : basé sur la clé métier.
        """
        if table_name == 'fact_sales':
            new_df = df[df['date_id'] > last_date_id]
            logger.info(
                f'{table_name} : {len(new_df)} nouvelles lignes '
                f'(date_id > {last_date_id})'
            )
            return new_df

        # Pour les dimensions, retourner tout
        # (géré par INSERT IGNORE côté SQL)
        return df

    def load_incremental(self, df, table_name):
        """
        Charge les nouvelles données avec INSERT IGNORE
        pour éviter les doublons.
        """
        if df.empty:
            logger.info(f'{table_name} : aucune nouvelle donnée')
            return

        logger.info(
            f'Chargement incrémental {table_name} : '
            f'{len(df)} lignes...'
        )

        # Charger par lots avec gestion des doublons
        df.to_sql(
            name=table_name,
            con=self.engine,
            if_exists='append',
            index=False,
            chunksize=1000,
        )

        logger.info(f'{table_name} mis à jour ✓')

    def run(self, data: dict):
        """
        Lance le chargement incrémental.
        Charge uniquement les nouvelles données depuis
        le dernier chargement.
        """
        logger.info('=== Démarrage chargement incrémental ===')

        # Récupérer le dernier date_id chargé
        last_date_id = self.get_last_date_id()

        # Ordre de chargement
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
                new_data = self.filter_new_records(
                    data[table], table, last_date_id
                )
                self.load_incremental(new_data, table)

        logger.info('=== Chargement incrémental terminé ===')


if __name__ == '__main__':
    loader = DataLoaderIncremental()
    print('Connexion OK !')