# ============================================================
# Génération des données simulées -- DWH Retail
# Master FAVD -- Visualisation des Données Massives
# ============================================================

import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker('fr_FR')
random.seed(42)
np.random.seed(42)

# ── Données de référence ─────────────────────────────────────
CATEGORIES = {
    'Électronique':  ['Smartphones', 'Laptops', 'Tablettes', 'TV'],
    'Vêtements':     ['Homme', 'Femme', 'Enfant', 'Sport'],
    'Alimentation':  ['Épicerie', 'Boissons', 'Boulangerie', 'Bio'],
    'Maison':        ['Meubles', 'Décoration', 'Cuisine', 'Jardin'],
    'Sport':         ['Fitness', 'Football', 'Natation', 'Cyclisme'],
}

GOVERNORATES = [
    'Tunis', 'Sfax', 'Sousse', 'Nabeul', 'Bizerte',
    'Gabès', 'Monastir', 'Gafsa', 'Kairouan', 'Béja',
    'Ariana', 'Ben Arous', 'Manouba', 'Zaghouan', 'Siliana',
    'Le Kef', 'Kasserine', 'Sidi Bouzid', 'Médenine', 'Tataouine',
    'Kebili', 'Tozeur', 'Mahdia', 'Jendouba'
]

REGIONS = {
    'Tunis': 'Nord', 'Ariana': 'Nord', 'Ben Arous': 'Nord',
    'Manouba': 'Nord', 'Bizerte': 'Nord', 'Nabeul': 'Nord',
    'Zaghouan': 'Nord', 'Béja': 'Nord', 'Jendouba': 'Nord',
    'Le Kef': 'Nord', 'Siliana': 'Nord',
    'Sousse': 'Centre', 'Monastir': 'Centre', 'Mahdia': 'Centre',
    'Sfax': 'Centre', 'Kairouan': 'Centre', 'Kasserine': 'Centre',
    'Sidi Bouzid': 'Centre',
    'Gabès': 'Sud', 'Médenine': 'Sud', 'Tataouine': 'Sud',
    'Gafsa': 'Sud', 'Tozeur': 'Sud', 'Kebili': 'Sud',
}

STORE_TYPES = ['Hypermarché', 'Supermarché', 'Magasin de proximité']
SEGMENTS    = ['Gold', 'Silver', 'Bronze']
AGE_GROUPS  = ['18-25', '26-35', '36-50', '50+']
PROMO_TYPES = ['Remise', 'Soldes', 'Fidélité', 'Flash']
BRANDS      = ['TunisiaShop', 'RetailTN', 'MedStore', 'SudMarket', 'NordPlus']


def generate_dates(start='2022-01-01', end='2024-12-31'):
    """Génère la table dim_date complète."""
    dates = []
    current = datetime.strptime(start, '%Y-%m-%d')
    end_dt  = datetime.strptime(end,   '%Y-%m-%d')
    while current <= end_dt:
        dates.append({
            'date_id':    int(current.strftime('%Y%m%d')),
            'full_date':  current.strftime('%Y-%m-%d'),
            'year':       current.year,
            'quarter':    (current.month - 1) // 3 + 1,
            'month':      current.month,
            'month_name': current.strftime('%B'),
            'week_iso':   current.isocalendar()[1],
            'day_name':   current.strftime('%A'),
            'is_weekend': current.weekday() >= 5,
            'is_holiday': False,
        })
        current += timedelta(days=1)
    return pd.DataFrame(dates)


def generate_products(n=200):
    """Génère la table dim_product."""
    products = []
    for i in range(n):
        cat     = random.choice(list(CATEGORIES.keys()))
        sub_cat = random.choice(CATEGORIES[cat])
        products.append({
            'sku':          f'SKU-{i+1:04d}',
            'product_name': f'{fake.word().title()} {sub_cat}',
            'category':     cat,
            'sub_category': sub_cat,
            'brand':        random.choice(BRANDS),
            'list_price':   round(random.uniform(5, 800), 2),
            'is_active':    True,
        })
    return pd.DataFrame(products)


def generate_stores(n=50):
    """Génère la table dim_store."""
    stores = []
    for i in range(n):
        gov = random.choice(GOVERNORATES)
        stores.append({
            'store_code':  f'STR-{i+1:03d}',
            'store_name':  f'RetailTN {gov} {i+1}',
            'city':        fake.city(),
            'governorate': gov,
            'region':      REGIONS.get(gov, 'Centre'),
            'store_type':  random.choice(STORE_TYPES),
            'surface_sqm': random.randint(200, 5000),
        })
    return pd.DataFrame(stores)


def generate_customers(n=5000):
    """Génère la table dim_customer."""
    customers = []
    for i in range(n):
        gov = random.choice(GOVERNORATES)
        customers.append({
            'customer_code':  f'CLI-{i+1:05d}',
            'full_name':      fake.name(),
            'city':           fake.city(),
            'governorate':    gov,
            'age_group':      random.choice(AGE_GROUPS),
            'segment':        random.choice(SEGMENTS),
            'loyalty_points': random.randint(0, 10000),
        })
    return pd.DataFrame(customers)


def generate_promotions(n=20):
    """Génère la table dim_promotion."""
    promos = []
    start = datetime(2022, 1, 1)
    for i in range(n):
        s = start + timedelta(days=random.randint(0, 700))
        e = s + timedelta(days=random.randint(7, 30))
        promos.append({
            'promo_name':    f'Promo {i+1} -- {random.choice(PROMO_TYPES)}',
            'promo_type':    random.choice(PROMO_TYPES),
            'discount_rate': round(random.uniform(5, 40), 2),
            'start_date':    s.strftime('%Y-%m-%d'),
            'end_date':      e.strftime('%Y-%m-%d'),
        })
    return pd.DataFrame(promos)


def generate_sales(products, stores, customers, promotions, n=50000):
    """Génère la table fact_sales."""
    start  = datetime(2022, 1, 1)
    sales  = []
    p_ids  = list(range(len(products)))
    s_ids  = list(range(len(stores)))
    c_ids  = list(range(len(customers)))
    pr_ids = list(range(len(promotions)))

    for _ in range(n):
        date      = start + timedelta(days=random.randint(0, 1095))
        p_idx     = random.choice(p_ids)
        s_idx     = random.choice(s_ids)
        c_idx     = random.choice(c_ids)
        use_promo = random.random() < 0.3
        pr_idx    = random.choice(pr_ids) if use_promo else None

        qty        = random.randint(1, 20)
        unit_price = round(products.iloc[p_idx]['list_price'], 2)
        discount   = round(promotions.iloc[pr_idx]['discount_rate'] / 100
                           if use_promo else random.uniform(0, 0.1), 2)
        cost       = round(unit_price * random.uniform(0.4, 0.7), 2)
        total_ht   = round(qty * unit_price * (1 - discount), 2)
        total_ttc  = round(total_ht * 1.19, 2)
        margin     = round(total_ht - qty * cost, 2)

        sales.append({
            'date_id':      int(date.strftime('%Y%m%d')),
            'product_id':   p_idx + 1,
            'customer_id':  c_idx + 1,
            'store_id':     s_idx + 1,
            'promo_id':     pr_idx + 1 if use_promo else None,
            'quantity':     qty,
            'unit_price':   unit_price,
            'total_ht':     total_ht,
            'discount_pct': round(discount * 100, 2),
            'total_ttc':    total_ttc,
            'cost_price':   cost,
            'gross_margin': margin,
        })
    return pd.DataFrame(sales)


if __name__ == '__main__':
    print('Génération des données en cours...')

    os.makedirs('raw', exist_ok=True)

    print('  → Dates...')
    dates = generate_dates()
    dates.to_csv('raw/dim_date.csv', index=False)

    print('  → Produits...')
    products = generate_products(200)
    products.to_csv('raw/dim_product.csv', index=False)

    print('  → Magasins...')
    stores = generate_stores(50)
    stores.to_csv('raw/dim_store.csv', index=False)

    print('  → Clients...')
    customers = generate_customers(5000)
    customers.to_csv('raw/dim_customer.csv', index=False)

    print('  → Promotions...')
    promotions = generate_promotions(20)
    promotions.to_csv('raw/dim_promotion.csv', index=False)

    print('  → Ventes (50 000 lignes)...')
    sales = generate_sales(products, stores, customers, promotions, 50000)
    sales.to_csv('raw/fact_sales.csv', index=False)

    print('Données générées avec succès dans data/raw/ !')
    print(f'  dim_date     : {len(dates)} lignes')
    print(f'  dim_product  : {len(products)} lignes')
    print(f'  dim_store    : {len(stores)} lignes')
    print(f'  dim_customer : {len(customers)} lignes')
    print(f'  dim_promotion: {len(promotions)} lignes')
    print(f'  fact_sales   : {len(sales)} lignes')
    