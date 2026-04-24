# Architecture Multi-Environnements — DWH Retail

## Vue Globale

```mermaid
graph TB
    subgraph Sources["📦 Sources de Données"]
        CSV[Fichiers CSV<br/>Données Simulées]
    end

    subgraph ETL["🐍 Pipeline ETL Python"]
        EXT[Extracteur]
        TRF[Transformateur]
        LOD[Chargeur]
        EXT --> TRF --> LOD
    end

    subgraph DEV["🛠️ DEV — Port 3307"]
        MYSQL_DEV[MySQL 8.0<br/>retail_dwh]
    end

    subgraph TEST["🧪 TEST — Port 3308"]
        MYSQL_TEST[MySQL 8.0<br/>retail_dwh_test]
    end

    subgraph PROD["🚀 PROD — Port 3309"]
        NDB_MGM[Management Node]
        NDB_D1[Data Node 1]
        NDB_D2[Data Node 2]
        NDB_SQL[SQL Node]
        NDB_MGM --> NDB_D1
        NDB_MGM --> NDB_D2
        NDB_D1 --> NDB_SQL
        NDB_D2 --> NDB_SQL
    end

    subgraph DAC["🔁 DAC — Port 3310"]
        REPLICA[MySQL Replica<br/>Disaster Recovery]
    end

    subgraph VIZ["📊 Visualisation"]
        STREAMLIT[Dashboard Streamlit<br/>localhost:8501]
    end

    CSV --> EXT
    LOD --> MYSQL_DEV
    LOD --> MYSQL_TEST
    LOD --> NDB_SQL
    NDB_SQL -->|Réplication| REPLICA
    MYSQL_DEV --> STREAMLIT
```

## Description des Environnements

| Environnement | Port | Rôle | Technologie |
|---|---|---|---|
| DEV | 3307 | Développement & tests locaux | MySQL 8.0 Standard |
| TEST | 3308 | Validation & tests automatisés | MySQL 8.0 Standard |
| PROD | 3309 | Production — haute disponibilité | MySQL Cluster NDB |
| DAC | 3310 | Disaster Recovery & Analytics | MySQL Replica |

## Schéma en Étoile

- **1 Table de faits** : `fact_sales` (50 000 lignes)
- **5 Dimensions** : `dim_date`, `dim_product`, `dim_store`, `dim_customer`, `dim_promotion`
- **Granularité** : 1 ligne = 1 transaction de vente

## KPIs Implémentés

| KPI | Description | Page Dashboard |
|---|---|---|
| KPI A | Chiffre d'affaires par magasin | 🏪 CA Magasins |
| KPI B | Évolution mensuelle des ventes | 📈 Evolution Ventes |
| KPI C | Top 10 produits les plus vendus | 🏆 Top Produits |
| KPI D | Impact des promotions | 🎯 Promotions |
| KPI E | Panier moyen par segment client | 🛍️ Panier Moyen |