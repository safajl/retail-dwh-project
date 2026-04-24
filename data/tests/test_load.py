# ============================================================
# Tests unitaires -- Load
# Master FAVD -- Visualisation des Données Massives
# ============================================================

import pytest
import pandas as pd
import os
import sys
from unittest.mock import MagicMock, patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.load_initial import DataLoaderInitial
from etl.load_incremental import DataLoaderIncremental


# ── Fixtures ─────────────────────────────────────────────────
@pytest.fixture
def sample_data():
    """Données de test pour le loader."""
    return {
        'dim_date': pd.DataFrame({
            'date_id':    [20220101, 20220102],
            'full_date':  ['2022-01-01', '2022-01-02'],
            'year':       [2022, 2022],
            'quarter':    [1, 1],
            'month':      [1, 1],
            'month_name': ['Janvier', 'Janvier'],
            'week_iso':   [52, 1],
            'day_name':   ['Samedi', 'Dimanche'],
            'is_weekend': [True, True],
            'is_holiday': [False, False],
        }),
        'dim_product': pd.DataFrame({
            'sku':          ['SKU-0001', 'SKU-0002'],
            'product_name': ['Produit A', 'Produit B'],
            'category':     ['Électronique', 'Vêtements'],
            'sub_category': ['Smartphones', 'Homme'],
            'brand':        ['BrandA', 'BrandB'],
            'list_price':   [299.99, 49.99],
            'is_active':    [True, True],
        }),
        'dim_store': pd.DataFrame({
            'store_code':  ['STR-001', 'STR-002'],
            'store_name':  ['RetailTN Tunis', 'RetailTN Sfax'],
            'city':        ['Tunis', 'Sfax'],
            'governorate': ['Tunis', 'Sfax'],
            'region':      ['Nord', 'Centre'],
            'store_type':  ['Hypermarché', 'Supermarché'],
            'surface_sqm': [3000, 1500],
        }),
        'dim_customer': pd.DataFrame({
            'customer_code':  ['CLI-00001', 'CLI-00002'],
            'full_name':      ['Ahmed Ben Ali', 'Fatma Trabelsi'],
            'city':           ['Tunis', 'Sfax'],
            'governorate':    ['Tunis', 'Sfax'],
            'age_group':      ['26-35', '36-50'],
            'segment':        ['Gold', 'Silver'],
            'loyalty_points': [500, 200],
        }),
        'dim_promotion': pd.DataFrame({
            'promo_name':    ['Promo Été', 'Promo Hiver'],
            'promo_type':    ['Soldes', 'Remise'],
            'discount_rate': [20.0, 15.0],
            'start_date':    ['2022-06-01', '2022-12-01'],
            'end_date':      ['2022-06-30', '2022-12-31'],
        }),
        'fact_sales': pd.DataFrame({
            'date_id':      [20220101, 20220102],
            'product_id':   [1, 2],
            'customer_id':  [1, 2],
            'store_id':     [1, 2],
            'promo_id':     [1, 0],
            'quantity':     [3, 5],
            'unit_price':   [299.99, 49.99],
            'total_ht':     [719.98, 199.96],
            'discount_pct': [20.0, 0.0],
            'total_ttc':    [856.77, 237.95],
            'cost_price':   [150.0, 25.0],
            'gross_margin': [269.98, 74.96],
        }),
    }


# ── Tests DataLoaderInitial ───────────────────────────────────
class TestDataLoaderInitial:

    @patch('etl.load_initial.create_engine')
    def test_loader_initial_created(self, mock_engine):
        """Vérifie que le loader initial se crée sans erreur."""
        mock_engine.return_value = MagicMock()
        loader = DataLoaderInitial()
        assert loader is not None

    @patch('etl.load_initial.create_engine')
    def test_load_table_called_for_each_table(
        self, mock_engine, sample_data
    ):
        """
        Vérifie que load_table est appelé
        pour chaque table dans run().
        """
        mock_engine.return_value = MagicMock()
        loader = DataLoaderInitial()

        # Mock la méthode load_table et verify_load
        loader.load_table   = MagicMock()
        loader.verify_load  = MagicMock()

        loader.run(sample_data)

        # Vérifier que load_table a été appelé 6 fois
        assert loader.load_table.call_count == 6

    @patch('etl.load_initial.create_engine')
    def test_load_order_dimensions_before_facts(
        self, mock_engine, sample_data
    ):
        """
        Vérifie que les dimensions sont chargées
        avant la table de faits.
        """
        mock_engine.return_value = MagicMock()
        loader = DataLoaderInitial()

        call_order = []
        loader.load_table  = MagicMock(
            side_effect=lambda df, name: call_order.append(name)
        )
        loader.verify_load = MagicMock()

        loader.run(sample_data)

        # fact_sales doit être le dernier chargé
        assert call_order[-1] == 'fact_sales'

        # Toutes les dimensions avant fact_sales
        fact_index = call_order.index('fact_sales')
        dims = [
            'dim_date', 'dim_product', 'dim_store',
            'dim_customer', 'dim_promotion'
        ]
        for dim in dims:
            assert call_order.index(dim) < fact_index


# ── Tests DataLoaderIncremental ───────────────────────────────
class TestDataLoaderIncremental:

    @patch('etl.load_incremental.create_engine')
    def test_loader_incremental_created(self, mock_engine):
        """Vérifie que le loader incrémental se crée sans erreur."""
        mock_engine.return_value = MagicMock()
        loader = DataLoaderIncremental()
        assert loader is not None

    @patch('etl.load_incremental.create_engine')
    def test_filter_new_records_fact_sales(
        self, mock_engine, sample_data
    ):
        """
        Vérifie que seules les nouvelles lignes
        sont chargées pour fact_sales.
        """
        mock_engine.return_value = MagicMock()
        loader = DataLoaderIncremental()

        df = sample_data['fact_sales']

        # Filtrer avec last_date_id = 20220101
        # → seule la ligne avec date_id=20220102 doit passer
        result = loader.filter_new_records(df, 'fact_sales', 20220101)
        assert len(result) == 1
        assert result.iloc[0]['date_id'] == 20220102

    @patch('etl.load_incremental.create_engine')
    def test_filter_returns_all_for_dimensions(
        self, mock_engine, sample_data
    ):
        """
        Vérifie que toutes les lignes sont retournées
        pour les dimensions (pas de filtre sur date).
        """
        mock_engine.return_value = MagicMock()
        loader = DataLoaderIncremental()

        df = sample_data['dim_product']
        result = loader.filter_new_records(
            df, 'dim_product', 20220101
        )

        # Toutes les lignes doivent être retournées
        assert len(result) == len(df)

    @patch('etl.load_incremental.create_engine')
    def test_empty_dataframe_not_loaded(
        self, mock_engine
    ):
        """
        Vérifie qu'un DataFrame vide n'est pas chargé
        (pas d'appel SQL inutile).
        """
        mock_engine.return_value = MagicMock()
        loader = DataLoaderIncremental()
        loader.engine = MagicMock()

        empty_df = pd.DataFrame()

        # Ne doit pas lever d'erreur
        loader.load_incremental(empty_df, 'fact_sales')

        # Vérifier que to_sql n'a pas été appelé
        loader.engine.connect.assert_not_called()