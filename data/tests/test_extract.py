# ============================================================
# Tests unitaires -- Extract
# Master FAVD -- Visualisation des Données Massives
# ============================================================

import pytest
import pandas as pd
import os
import sys

# Ajouter le dossier parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.extract import DataExtractor


# ── Fixtures ─────────────────────────────────────────────────
@pytest.fixture
def sample_csv(tmp_path):
    """
    Crée des fichiers CSV temporaires pour les tests.
    tmp_path est un dossier temporaire créé par pytest.
    """
    # Créer dim_date
    pd.DataFrame({
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
    }).to_csv(tmp_path / 'dim_date.csv', index=False)

    # Créer dim_product
    pd.DataFrame({
        'sku':          ['SKU-0001', 'SKU-0002'],
        'product_name': ['Produit A', 'Produit B'],
        'category':     ['Électronique', 'Vêtements'],
        'sub_category': ['Smartphones', 'Homme'],
        'brand':        ['BrandA', 'BrandB'],
        'list_price':   [299.99, 49.99],
        'is_active':    [True, True],
    }).to_csv(tmp_path / 'dim_product.csv', index=False)

    # Créer dim_store
    pd.DataFrame({
        'store_code':  ['STR-001', 'STR-002'],
        'store_name':  ['RetailTN Tunis 1', 'RetailTN Sfax 1'],
        'city':        ['Tunis', 'Sfax'],
        'governorate': ['Tunis', 'Sfax'],
        'region':      ['Nord', 'Centre'],
        'store_type':  ['Hypermarché', 'Supermarché'],
        'surface_sqm': [3000, 1500],
    }).to_csv(tmp_path / 'dim_store.csv', index=False)

    # Créer dim_customer
    pd.DataFrame({
        'customer_code':  ['CLI-00001', 'CLI-00002'],
        'full_name':      ['Ahmed Ben Ali', 'Fatma Trabelsi'],
        'city':           ['Tunis', 'Sfax'],
        'governorate':    ['Tunis', 'Sfax'],
        'age_group':      ['26-35', '36-50'],
        'segment':        ['Gold', 'Silver'],
        'loyalty_points': [500, 200],
    }).to_csv(tmp_path / 'dim_customer.csv', index=False)

    # Créer dim_promotion
    pd.DataFrame({
        'promo_name':    ['Promo Été', 'Promo Hiver'],
        'promo_type':    ['Soldes', 'Remise'],
        'discount_rate': [20.0, 15.0],
        'start_date':    ['2022-06-01', '2022-12-01'],
        'end_date':      ['2022-06-30', '2022-12-31'],
    }).to_csv(tmp_path / 'dim_promotion.csv', index=False)

    # Créer fact_sales
    pd.DataFrame({
        'date_id':      [20220101, 20220102],
        'product_id':   [1, 2],
        'customer_id':  [1, 2],
        'store_id':     [1, 2],
        'promo_id':     [1, None],
        'quantity':     [3, 5],
        'unit_price':   [299.99, 49.99],
        'total_ht':     [719.98, 199.96],
        'discount_pct': [20.0, 0.0],
        'total_ttc':    [856.77, 237.95],
        'cost_price':   [150.0, 25.0],
        'gross_margin': [269.98, 74.96],
    }).to_csv(tmp_path / 'fact_sales.csv', index=False)

    return str(tmp_path)


# ── Tests ─────────────────────────────────────────────────────
class TestDataExtractor:

    def test_extract_returns_all_tables(self, sample_csv):
        """Vérifie que toutes les tables sont extraites."""
        extractor = DataExtractor(raw_path=sample_csv)
        data = extractor.run()

        # Vérifier que les 6 tables sont présentes
        assert 'dim_date'      in data
        assert 'dim_product'   in data
        assert 'dim_store'     in data
        assert 'dim_customer'  in data
        assert 'dim_promotion' in data
        assert 'fact_sales'    in data

    def test_extract_not_empty(self, sample_csv):
        """Vérifie que les DataFrames ne sont pas vides."""
        extractor = DataExtractor(raw_path=sample_csv)
        data = extractor.run()

        for table_name, df in data.items():
            assert not df.empty, f'{table_name} ne doit pas être vide'

    def test_dim_date_required_columns(self, sample_csv):
        """Vérifie les colonnes obligatoires de dim_date."""
        extractor = DataExtractor(raw_path=sample_csv)
        data = extractor.run()
        df = data['dim_date']

        assert 'date_id'   in df.columns
        assert 'full_date' in df.columns
        assert 'year'      in df.columns
        assert 'month'     in df.columns

    def test_fact_sales_required_columns(self, sample_csv):
        """Vérifie les colonnes obligatoires de fact_sales."""
        extractor = DataExtractor(raw_path=sample_csv)
        data = extractor.run()
        df = data['fact_sales']

        required = [
            'date_id', 'product_id', 'customer_id',
            'store_id', 'quantity', 'total_ttc'
        ]
        for col in required:
            assert col in df.columns, f'Colonne manquante : {col}'

    def test_fact_sales_no_null_fk(self, sample_csv):
        """Vérifie qu'il n'y a pas de nulls sur les clés étrangères."""
        extractor = DataExtractor(raw_path=sample_csv)
        data = extractor.run()
        df = data['fact_sales']

        fk_cols = ['date_id', 'product_id', 'customer_id', 'store_id']
        for col in fk_cols:
            assert df[col].isnull().sum() == 0, \
                f'Null trouvé dans la FK {col}'

    def test_file_not_found_raises_error(self, tmp_path):
        """Vérifie qu'une erreur est levée si le fichier est absent."""
        extractor = DataExtractor(raw_path=str(tmp_path))
        with pytest.raises(FileNotFoundError):
            extractor.run()