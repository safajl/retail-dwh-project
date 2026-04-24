-- ============================================================
-- DWH Retail -- Schéma en étoile
-- Master FAVD -- Visualisation des Données Massives
-- ============================================================

CREATE DATABASE IF NOT EXISTS retail_dwh;
USE retail_dwh;

-- ── Dimension Date ───────────────────────────────────────────
CREATE TABLE dim_date (
    date_id     INT          NOT NULL,
    full_date   DATE         NOT NULL,
    year        SMALLINT     NOT NULL,
    quarter     TINYINT      NOT NULL,
    month       TINYINT      NOT NULL,
    month_name  VARCHAR(20)  NOT NULL,
    week_iso    TINYINT      NOT NULL,
    day_name    VARCHAR(10)  NOT NULL,
    is_weekend  BOOLEAN      DEFAULT FALSE,
    is_holiday  BOOLEAN      DEFAULT FALSE,
    PRIMARY KEY (date_id)
) ENGINE=InnoDB;

-- ── Dimension Produit ────────────────────────────────────────
CREATE TABLE dim_product (
    product_id    INT           NOT NULL AUTO_INCREMENT,
    sku           VARCHAR(30)   NOT NULL,
    product_name  VARCHAR(100)  NOT NULL,
    category      VARCHAR(50)   NOT NULL,
    sub_category  VARCHAR(50),
    brand         VARCHAR(50),
    list_price    DECIMAL(10,2) NOT NULL,
    is_active     BOOLEAN       DEFAULT TRUE,
    PRIMARY KEY (product_id)
) ENGINE=InnoDB;

-- ── Dimension Magasin ────────────────────────────────────────
CREATE TABLE dim_store (
    store_id      INT          NOT NULL AUTO_INCREMENT,
    store_code    VARCHAR(20)  NOT NULL,
    store_name    VARCHAR(100) NOT NULL,
    city          VARCHAR(50)  NOT NULL,
    governorate   VARCHAR(50)  NOT NULL,
    region        VARCHAR(30)  NOT NULL,
    store_type    VARCHAR(30)  NOT NULL,
    surface_sqm   INT,
    PRIMARY KEY (store_id)
) ENGINE=InnoDB;

-- ── Dimension Client ─────────────────────────────────────────
CREATE TABLE dim_customer (
    customer_id    INT          NOT NULL AUTO_INCREMENT,
    customer_code  VARCHAR(20)  NOT NULL,
    full_name      VARCHAR(100) NOT NULL,
    city           VARCHAR(50),
    governorate    VARCHAR(50),
    age_group      VARCHAR(20),
    segment        VARCHAR(30),
    loyalty_points INT          DEFAULT 0,
    PRIMARY KEY (customer_id)
) ENGINE=InnoDB;

-- ── Dimension Promotion ──────────────────────────────────────
CREATE TABLE dim_promotion (
    promo_id      INT           NOT NULL AUTO_INCREMENT,
    promo_name    VARCHAR(100)  NOT NULL,
    promo_type    VARCHAR(30)   NOT NULL,
    discount_rate DECIMAL(5,2)  NOT NULL,
    start_date    DATE          NOT NULL,
    end_date      DATE          NOT NULL,
    PRIMARY KEY (promo_id)
) ENGINE=InnoDB;

-- ── Table de Faits : fact_sales ──────────────────────────────
CREATE TABLE fact_sales (
    sale_id       BIGINT         NOT NULL AUTO_INCREMENT,
    date_id       INT            NOT NULL,
    product_id    INT            NOT NULL,
    customer_id   INT            NOT NULL,
    store_id      INT            NOT NULL,
    promo_id      INT,
    quantity      INT            NOT NULL,
    unit_price    DECIMAL(10,2)  NOT NULL,
    total_ht      DECIMAL(12,2)  NOT NULL,
    discount_pct  DECIMAL(5,2)   DEFAULT 0,
    total_ttc     DECIMAL(12,2)  NOT NULL,
    cost_price    DECIMAL(10,2)  NOT NULL,
    gross_margin  DECIMAL(12,2)  NOT NULL,
    PRIMARY KEY (sale_id)
) ENGINE=InnoDB;