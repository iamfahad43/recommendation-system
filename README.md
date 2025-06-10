# E-Commerce Recommendation Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> A professional end-to-end recommendation system built on the Olist E-Commerce dataset, featuring automated ETL, star-schema analytics in PostgreSQL, collaborative- & content-based models, and five Power BI dashboards.

---

## Table of Contents

- [Project Overview](#project-overview)  
- [Dataset](#dataset)  
- [Architecture](#architecture)  
- [Folder Structure](#folder-structure)  
- [Installation](#installation)  
- [ETL Pipeline](#etl-pipeline)  
- [Modeling & Generating Recommendations](#modeling--generating-recommendations)  
- [Power BI Dashboards](#power-bi-dashboards)  
- [Results](#results)  
- [Future Enhancements](#future-enhancements)  
- [Contributing](#contributing)  
- [Thanks](#thanks)  

---

## Project Overview

This repository contains a full-lifecycle recommendation engine for a real-world e-commerce use case. It demonstrates:

- **Data Engineering**: Automated ETL of raw CSVs → staging → star schema in PostgreSQL  
- **Data Science**: Collaborative filtering (SVD) & content-based recommenders  
- **Business Intelligence**: **Five** interactive Power BI dashboards for KPI tracking and personalized recommendations

---

## Dataset

I used the [Olist E-Commerce Public Dataset](https://www.kaggle.com/olistbr/brazilian-ecommerce), which includes:

- **Orders**, **Order Items**, **Payments**, **Reviews**  
- **Customers**, **Products**, **Sellers**, **Geolocation**  
- Rich temporal & geographic granularity for deep analytics

---

## Architecture

```text
  +-------------+        +-------------+       +--------------+
  |  Raw CSVs   |  ETL   |  Staging    |       | Analytics    |
  | data/raw/   |----->  | PostgreSQL  |  DML  | star schema  |
  +-------------+        +-------------+       +--------------+
                                                         |
                                                         v
                                                 +----------------+
                                                 | Modeling (Py)  |
                                                 +----------------+
                                                         |
                                                         v
                                              +----------------------+
                                              | Generate Recs Script |
                                              +----------------------+
                                                         |
                                                         v
                                               +--------------------+
                                               | Power BI Dashboards|
                                               +--------------------+
```

---

## Folder Structure
```text
recommendation-system/
├── data/
│   ├── raw/                  # Olist CSVs
│   └── processed/            # Cleaned parquet files
├── sql/
│   ├── ddl/                  # CREATE TABLE for staging & analytics
│   └── dml/                  # CTAS transforms for analytics
├── src/
│   ├── db_utils.py           # DB connection & logging
│   ├── etl.py                # Ingest & transform raw data into Postgres
│   ├── load.py               # Load pipeline (Parquet → Postgres)
│   ├── modeling.py           # Train CF & content models
│   └── generate_recommendations.py # Top-10 recommendations per user
├── models/                   # Serialized models (.joblib, JSON)
├── notebooks/                # EDA scripts & figures
├── docs/                     # Screenshots & exported images
├── powerbi/                  # Five .pbix dashboards (01–05)
│   ├── 01_SalesOverview.pbix
│   ├── 02_CustomerInsights.pbix
│   ├── 03_ProductPerformance.pbix
│   ├── 04_DeliveryAnalysis.pbix
│   └── 05_RecommendationExplorer.pbix
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation

```

---


## Installation
1. **Clone the repo**:

   ```bash
   git clone https://github.com/iamfahad43/recommendation-system.git
   cd cd recommendation-system
   ```

2. **Create a virtual environment & install dependencies**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate        # (or .\venv\Scripts\activate on Windows)
   pip install -r requirements.txt
   ```

3. **Configure your postgreSQL**:

   * Install PostgreSQL locally.
   * sudo service postgresql start (WSL)
   * Create a database & user (`olist_db`) and grant privileges.
   * createdb olist_db (WSL)
   * psql olist_db < sql/ddl/create_tables.sql
   * Update `config.yaml` with your host, port, user, password, and database name.

---

## ETL Pipeline
1. **Extract & Transform**:

   ```bash
   python src/etl.py     # (Reads raw CSVs → cleans & writes to data/processed/)
   ```

2. **Load into Postgres**:

   ```bash
   python src/load.py        # (Loads Parquet → staging.*, then runs CTAS → analytics.*)
   ```
---


## Modeling & Generating Recommendations
1. **Train Models**:

   ```bash
   python src/modeling.py     # (Builds SVD CF model (models/cf_svd.joblib))
                              # (Builds TF-IDF content model & top-N lookup)
   ```

2. **Generate Top-10 Recommendations**:

   ```bash
   python src/generate_recommendations.py        # (Creates/truncates analytics.recommendations)
                                                 # (For each customer, predicts unrated products → top 10 → inserts into Postgres)
   ```

---

## Power BI Dashboards
1. **powerbi/**:

   * 01_SalesOverview.pbix                        (KPI cards (orders, sales, AOV, repeat rate) + time-series charts)                        
   * 02_CustomerInsights.pbix                     (Top customers by orders & spend + distribution of orders per customer)
   * 03_ProductPerformance.pbix                   (Top categories by revenue & units + price vs review scatter)
   * 04_DeliveryAnalysis.pbix                     (Delivery delay histogram + on-time delivery KPI + geographic map)
   * 05_RecommendationExplorer.pbix               (Customer slicer → table of top-10 CF & content-based recommendations)
   * **If it doen't change:** Refresh each report after running the ETL & recommendation scripts.
  
---

## Results
* **Collaborative Filtering RMSE:** ~0.92 on held-out test set
* **Precision@10:** ~0.13 for the baseline SVD model
* Screenshots and sample outputs are available in docs/

---

## Future Enhancements
* **Workflow Orchestration:** Apache Airflow or GitHub Actions for scheduled ETL & retraining
* **Containerization:** Dockerize components for CI/CD and cloud deployment
* **Real-time API:** Serve recommendations via Flask/FastAPI microservice
* **A/B Testing:** Evaluate different model versions in production

---

## Contributing
Contributions are welcome! Please open an issue or submit a pull request following the existing style.

---

## Final Message
Thank you for your time to see the project and contributions. I'll try my best to respond your queries🥇



