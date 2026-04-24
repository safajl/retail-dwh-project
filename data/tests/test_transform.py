# ============================================================
# Tests unitaires -- Transform
# Master FAVD -- Visualisation des Données Massives
# ============================================================

import pytest
import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.transform import DataTransformer


# ── Fixtures ─────────────────────────────────────────────────
@pytest.fixture
def sample_data():
    """Données de test pour le transformer."""
    return {
        'dim_date': pd.DataFrame({
            'date_id':    [20220101, 20220101, 20220102],
            'full_date':  ['2022-01-01', '2022-01-01', '2022-01-02'],
            'year':       [2022, 2022, 2022],
            'quarter':    [1, 1, 1],
            'month':      [1, 1, 1],
            'month_name': ['Janvier', 'Janvier', 'Janvier'],
            'week_iso':   [52, 52, 1],
            'day_name':   ['Samedi', 'Samedi', 'Dimanche'],
            'is_weekend': [True, True, None],
            'is_holiday': [False, False, None],
        }),
        'dim_product': pd.DataFrame({
            'sku':          ['SKU-0001', 'SKU-0001', 'SKU-0002'],
            'product_name': ['  produit a  ', 'produit a', 'PRODUIT B'],
            'category':     ['Électronique', 'Électronique', 'Vêtements'],
            'sub_category': ['Smartphones', 'Smartphones', None],
            'brand':        ['brandA', 'brandA', None],
            'list_price':   [299.99, 299.99, -5.0],
            'is_active':    [True, True, None],
        }),
        'dim_store': pd.DataFrame({
            'store_code':  ['STR-001', 'STR-002'],
            'store_name':  ['RetailTN Tunis', 'RetailTN Sfax'],
            'city':        ['tunis', 'sfax'],
            'governorate': ['Tunis', 'Sfax'],
            'region':      ['Nord', 'Centre'],
            'store_type':  ['Hypermarché', 'Supermarché'],
            'surface_sqm': [3000, None],
        }),
        'dim_customer': pd.DataFrame({
            'customer_code':  ['CLI-00001', 'CLI-00002'],
            'full_name':      ['ahmed ben ali', 'FATMA TRABELSI'],
            'city':           ['tunis', 'sfax'],
            'governorate':    ['Tunis', 'Sfax'],
            'age_group':      ['26-35', None],
            'segment':        ['Gold', None],
            'loyalty_points': [500, None],
        }),
        'dim_promotion': pd.DataFrame({
            'promo_name':    ['Promo Été', 'Promo Hiver'],
            'promo_type':    ['Soldes', 'Remise'],
            'discount_rate': [20.0, 150.0],
            'start_date':    ['2022-06-01', '2022-12-01'],
            'end_date':      ['2022-06-30', '2022-12-31'],
        }),
        'fact_sales': pd.DataFrame({
            'date_id':      [20220101, 20220101, 20220102],
            'product_id':   [1, 1, 2],
            'customer_id':  [1, 1, 2],
            'store_id':     [1, 1, 2],
            'promo_id':     [1, 1, None],
            'quantity':     [3, 3, 5],
            'unit_price':   [299.99, 299.99, 49.99],
            'total_ht':     [719.98, 719.98, 199.96],
            'discount_pct': [20.0, 20.0, None],
            'total_ttc':    [856.77, 856.77, 237.95],
            'cost_price':   [150.0, 150.0, 25.0],
            'gross_margin': [0, 0, 0],
        }),
    }


# ── Tests ─────────────────────────────────────────────────────
class TestDataTransformer:

    def test_no_duplicates_dim_date(self, sample_data):
        """Vérifie la suppression des doublons dans dim_date."""
        transformer = DataTransformer(sample_data)
        result = transformer.transform_dim_date(
            sample_data['dim_date'].copy()
        )
        # date_id 20220101 apparaît 2 fois → doit être réduit à 1
        assert result['date_id'].duplicated().sum() == 0

    def test_no_duplicates_dim_product(self, sample_data):
        """Vérifie la suppression des doublons dans dim_product."""
        transformer = DataTransformer(sample_data)
        result = transformer.transform_dim_product(
            sample_data['dim_product'].copy()
        )
        assert result['sku'].duplicated().sum() == 0

    def test_invalid_price_removed(self, sample_data):
        """Vérifie que les prix négatifs sont supprimés."""
        transformer = DataTransformer(sample_data)
        result = transformer.transform_dim_product(
            sample_data['dim_product'].copy()
        )
        assert (result['list_price'] > 0).all()

    def test_null_filled_dim_product(self, sample_data):
        """Vérifie que les nulls sont remplis dans dim_product."""
        transformer = DataTransformer(sample_data)
        result = transformer.transform_dim_product(
            sample_data['dim_product'].copy()
        )
        assert result['sub_category'].isnull().sum() == 0
        assert result['brand'].isnull().sum() == 0

    def test_text_normalized_dim_customer(self, sample_data):
        """Vérifie la normalisation des textes dans dim_customer."""
        transformer = DataTransformer(sample_data)
        result = transformer.transform_dim_customer(
            sample_data['dim_customer'].copy()
        )
        # Les noms doivent être en Title Case
        assert result['full_name'].iloc[0] == 'Ahmed Ben Ali'
        assert result['full_name'].iloc[1] == 'Fatma Trabelsi'

    def test_null_filled_dim_customer(self, sample_data):
        """Vérifie que les nulls sont remplis dans dim_customer."""
        transformer = DataTransformer(sample_data)
        result = transformer.transform_dim_customer(
            sample_data['dim_customer'].copy()
        )
        assert result['segment'].isnull().sum() == 0
        assert result['age_group'].isnull().sum() == 0
        assert result['loyalty_points'].isnull().sum() == 0

    def test_invalid_discount_removed(self, sample_data):
        """Vérifie que les remises invalides sont supprimées."""
        transformer = DataTransformer(sample_data)
        result = transformer.transform_dim_promotion(
            sample_data['dim_promotion'].copy()
        )
        # discount_rate de 150 doit être supprimé
        assert (result['discount_rate'] <= 100).all()

    def test_no_duplicates_fact_sales(self, sample_data):
        """Vérifie la suppression des doublons dans fact_sales."""
        transformer = DataTransformer(sample_data)
        result = transformer.transform_fact_sales(
            sample_data['fact_sales'].copy()
        )
        assert result.duplicated(
            subset=['date_id', 'product_id', 'customer_id', 'store_id']
        ).sum() == 0

    def test_gross_margin_recalculated(self, sample_data):
        """Vérifie que la marge brute est recalculée correctement."""
        transformer = DataTransformer(sample_data)
        result = transformer.transform_fact_sales(
            sample_data['fact_sales'].copy()
        )
        # Vérifier que gross_margin = total_ht - quantity * cost_price
        expected = round(
            result['total_ht'] - result['quantity'] * result['cost_price'],
            2
        )
        pd.testing.assert_series_equal(
            result['gross_margin'].reset_index(drop=True),
            expected.reset_index(drop=True),
            check_names=False
        )

    def test_discount_pct_null_filled(self, sample_data):
        """Vérifie que discount_pct null est remplacé par 0."""
        transformer = DataTransformer(sample_data)
        result = transformer.transform_fact_sales(
            sample_data['fact_sales'].copy()
        )
        assert result['discount_pct'].isnull().sum() == 0

    def test_run_returns_all_tables(self, sample_data):
        """Vérifie que run() retourne toutes les tables."""
        transformer = DataTransformer(sample_data)
        result = transformer.run()

        assert 'dim_date'      in result
        assert 'dim_product'   in result
        assert 'dim_store'     in result
        assert 'dim_customer'  in result
        assert 'dim_promotion' in result
        assert 'fact_sales'    in result