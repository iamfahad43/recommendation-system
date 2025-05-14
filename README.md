# E-Commerce Recommendation Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> A full-scale data engineering and data science project showcasing an end-to-end recommendation system built on the Olist E-Commerce dataset, complete with ETL pipelines, SQL star schema, collaborative- and content-based models, and interactive Power BI dashboards.

---

## Table of Contents

* [Project Overview](#project-overview)
* [Dataset](#dataset)
* [Architecture](#architecture)
* [Folder Structure](#folder-structure)
* [Installation](#installation)
* [ETL Pipeline](#etl-pipeline)
* [Modeling](#modeling)
* [Power BI Dashboard](#power-bi-dashboard)
* [Results](#results)
* [Future Enhancements](#future-enhancements)
* [Contributing](#contributing)
* [License](#license)

---

## Project Overview

This repository contains a professional-grade recommendation system built for a real-world e-commerce scenario. It demonstrates:

* **Data Engineering**: Automated ETL of raw CSVs into a staging schema, transformation into an analytics star schema in PostgreSQL.
* **Data Science**: Collaborative filtering (SVD) and content-based recommendation models.
* **Business Intelligence**: Interactive multi-page Power BI dashboard presenting KPIs, customer segments, and personalized recommendations.

The project is designed for easy setup on a local PC and is fully reproducible end-to-end.

---

## Dataset

We leverage the [Olist E-Commerce Public Dataset](https://www.kaggle.com/olistbr/brazilian-ecommerce) from Kaggle, which includes:

* **Orders** (timestamps, status)
* **Order items**, **payments**, **reviews**
* **Customer** demographics
* **Product** metadata and categories
* **Seller** locations and geospatial data

This multi-table schema enables rich analytics and recommendation modeling.

---

## Architecture

```text
            +----------------------+      +-------------------+
 Raw CSVs  |  data/raw/olist/      | ---> | staging schema    |
           +----------------------+      | PostgreSQL        |
                                            |     
                                            |     +-------------------+
                                            +-->  | analytics schema  |
                                                  | (star schema)     |
                                                  +-------------------+
                                                           |
                                                           v
                                                    +-------------+
                                                    | Modeling    |
                                                    | (Python)    |
                                                    +-------------+
                                                           |
                                                           v
                                                  +-------------------+
                                                  | Power BI Reports  |
                                                  +-------------------+
```

---

## Folder Structure

```text
recommendation-system/
├── data/
│   ├── raw/                # Original Olist CSV files
│   └── processed/          # Cleaned & joined parquet or CSV files
├── sql/
│   ├── ddl/                # CREATE TABLE scripts (staging & analytics)
│   └── dml/                # Transformation SQL (CTAS for analytics)
├── src/
│   ├── etl.py              # Ingest & transform raw data into Postgres
│   ├── modeling.py         # Train & evaluate recommendation models
│   └── utils.py            # DB connector, logging, helpers
├── notebooks/              # EDA: customer segments, rating distributions
├── powerbi/                # Power BI .pbix file & usage guide
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/iamfahad43/recommendation-system.git
   cd recommendation-system
   ```

2. **Python environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Database setup**

   ```bash
   # Create PostgreSQL database
   createdb olist_db

   # Apply DDL scripts
   psql olist_db < sql/ddl/create_tables.sql
   ```

4. **Download and place raw data**

   * Download all CSVs from Kaggle and place them in `data/raw/olist/`.

5. **Run ETL**

   ```bash
   python src/etl.py
   ```

6. **Train models**

   ```bash
   python src/modeling.py
   ```

7. **Open Power BI report**

   * Open `powerbi/olist_recommendation.pbix` in Power BI Desktop.
   * Connect to the `analytics` schema in `olist_db`.

---

## ETL Pipeline

* **`src/etl.py`**:

  * Reads raw CSVs, casts timestamps, and loads into `staging` schema.
  * Executes `sql/dml/transform_analytics.sql` to build the `analytics` star schema (fact & dimension tables).

* **Staging Schema** mirrors raw data for full auditability.

* **Analytics Schema** uses CTAS to create a fact table (`fact_order_item`) and dimensions (`dim_customers`, `dim_products`, etc.).

---

## Modeling

* **Collaborative Filtering**:

  * Uses [Surprise](https://surprise.readthedocs.io/) SVD on user–product ratings.
  * Train/test split with RMSE evaluation.

* **Content-Based**:

  * TF-IDF vectorization of product categories.
  * Cosine similarity for item-to-item recommendations.

Models are serialized under `models/` for downstream production use.

---

## Power BI Dashboard

The Power BI report (`powerbi/olist_recommendation.pbix`) contains:

1. **Sales Overview**: Total orders, revenue trends, average basket size.
2. **Customer Insights**: Order frequency distribution, CLV segmentation.
3. **Product Analytics**: Top categories by revenue, average review scores.
4. **Recommendation Explorer**:

   * Parameterized by `customer_id`.
   * Side-by-side CF vs. content-based top‑N predictions.

Use slicers and KPI cards for interactive analysis. Screenshots are in the `docs/` folder.

---

## Results

* **Baseline RMSE** for SVD: \~0.92 on held-out test set.
* **Top-10 recommendations** accuracy: Precision\@10 \~ 0.13.

*Screenshots and sample queries can be found in the `docs/` directory.*

---

## Future Enhancements

* **Workflow Orchestration**: Integrate Apache Airflow for daily ETL and model retraining.
* **Containerization**: Dockerize services for CI/CD and cloud deployment.
* **Real-time API**: Serve recommendations via a Flask/FastAPI microservice.
* **A/B Testing**: Evaluate model variants in production.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
