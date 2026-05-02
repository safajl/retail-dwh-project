# 🛒 DWH Retail — Data Warehouse Multi-Environnements

**Master FAVD — Visualisation des Données Massives**

---

## 📌 Présentation du Projet

Ce projet implémente un Data Warehouse complet pour une chaîne de distribution retail tunisienne (**RetailTN**), incluant :

- Modélisation en schéma en étoile (Star Schema)
- Cluster MySQL NDB multi-nœuds
- Pipeline ETL Python automatisé
- 4 environnements isolés (DEV / TEST / PROD / DAC)
- Dashboard analytique Streamlit (5 KPIs)

---

## 🏗️ Architecture
### Schéma en Étoile

- **1 Table de faits** : `fact_sales` (50 000 transactions)
- **5 Dimensions** : `dim_date`, `dim_product`, `dim_store`, `dim_customer`, `dim_promotion`
- **Granularité** : 1 ligne = 1 transaction de vente

---

## ⚙️ Installation

### Prérequis

- Python 3.12+
- Docker Desktop
- Git

### 1. Cloner le repository

```bash
git clone https://github.com/VOTRE_USERNAME/retail-dwh-project.git
cd retail-dwh-project
```

### 2. Installer les dépendances Python

```bash
pip install -r data/requirements.txt
```

### 3. Générer les données

```bash
cd data
python generate_data.py
cd ..
```

---

## 🚀 Exécution

### Démarrer l'environnement DEV

```bash
cd dev
docker-compose up -d
cd ..
```

### Lancer le pipeline ETL

```bash
python data/etl/pipeline.py --mode initial --raw-path data/raw
```

### Lancer les tests

```bash
python -m pytest data/tests/ -v
```

### Lancer le dashboard

```bash
cd analysis
streamlit run app.py
```

Le dashboard est accessible sur **http://localhost:8501**

---

## 📊 Résultats

### Données chargées

| Table | Lignes |
|---|---|
| dim_date | 1 096 |
| dim_product | 200 |
| dim_store | 50 |
| dim_customer | 5 000 |
| dim_promotion | 20 |
| fact_sales | 50 000 |

### Tests
### KPIs disponibles

| KPI | Description |
|---|---|
| KPI A | Chiffre d'affaires par magasin |
| KPI B | Évolution mensuelle des ventes |
| KPI C | Top 10 produits les plus vendus |
| KPI D | Impact des promotions sur les ventes |
| KPI E | Panier moyen par segment client |

---

## 👥 Équipe

- Étudiant(e) 1 : **Safa jlassi**
- Étudiant(e) 2 : **ines boujemaa**
- Étudiant(e) 3 : **Jihen Zaidi**
- Étudiant(e) 3 : **Hamza Marweni**

---

## 📅 Année Universitaire

2025 — 2026     
