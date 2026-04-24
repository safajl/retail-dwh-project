-- ============================================================
-- Requêtes KPI -- DWH Retail
-- ============================================================

USE retail_dwh;

-- ── KPI A : Chiffre d'affaires par magasin ───────────────────
SELECT
    s.store_name,
    s.governorate,
    s.region,
    SUM(f.total_ttc)   AS ca_total,
    COUNT(f.sale_id)   AS nb_transactions,
    AVG(f.total_ttc)   AS panier_moyen
FROM fact_sales f
JOIN dim_store s ON f.store_id = s.store_id
GROUP BY s.store_name, s.governorate, s.region
ORDER BY ca_total DESC;

-- ── KPI B : Evolution mensuelle des ventes ───────────────────
SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(f.total_ttc)   AS ca_mensuel,
    SUM(f.quantity)    AS qte_vendue,
    LAG(SUM(f.total_ttc)) OVER (
        ORDER BY d.year, d.month
    ) AS ca_mois_precedent
FROM fact_sales f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

-- ── KPI C : Top 10 produits ──────────────────────────────────
SELECT
    p.product_name,
    p.category,
    p.brand,
    SUM(f.quantity)    AS total_qte,
    SUM(f.total_ttc)   AS ca_total,
    AVG(f.gross_margin) AS marge_moyenne
FROM fact_sales f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.product_name, p.category, p.brand
ORDER BY ca_total DESC
LIMIT 10;

-- ── KPI D : Impact des promotions ────────────────────────────
SELECT
    pr.promo_name,
    pr.promo_type,
    pr.discount_rate,
    COUNT(f.sale_id)     AS nb_ventes_promo,
    SUM(f.total_ttc)     AS ca_promo,
    AVG(f.discount_pct)  AS remise_moyenne_pct
FROM fact_sales f
JOIN dim_promotion pr ON f.promo_id = pr.promo_id
GROUP BY pr.promo_name, pr.promo_type, pr.discount_rate
ORDER BY ca_promo DESC;

-- ── KPI E : Panier moyen par segment client ───────────────────
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
ORDER BY panier_moyen DESC;