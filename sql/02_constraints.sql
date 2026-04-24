-- ============================================================
-- Contraintes et Index -- DWH Retail
-- ============================================================

USE retail_dwh;

-- ── Index sur la table de faits ──────────────────────────────
ALTER TABLE fact_sales
    ADD INDEX idx_date_id (date_id),
    ADD INDEX idx_product_id (product_id),
    ADD INDEX idx_customer_id (customer_id),
    ADD INDEX idx_store_id (store_id),
    ADD INDEX idx_promo_id (promo_id);

-- ── Index sur les dimensions ─────────────────────────────────
ALTER TABLE dim_product
    ADD UNIQUE INDEX idx_sku (sku);

ALTER TABLE dim_store
    ADD UNIQUE INDEX idx_store_code (store_code);

ALTER TABLE dim_customer
    ADD UNIQUE INDEX idx_customer_code (customer_code);

ALTER TABLE dim_date
    ADD UNIQUE INDEX idx_full_date (full_date);