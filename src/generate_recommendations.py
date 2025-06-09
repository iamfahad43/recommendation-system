

from loguru import logger
from pathlib import Path
import pandas as pd
import joblib
from sqlalchemy import text
from src.db_utils import get_engine


# Path to your compressed CF model artifact
CF_MODEL_PATH = Path('models/cf_svd.joblib')
# Number of recommendations per user
TOP_N = 10


def main():
    engine = get_engine(schema='analytics')

    # 1) Create the recommendations table if it doesn't exist
    create_tbl = """
    CREATE TABLE IF NOT EXISTS analytics.recommendations (
      customer_id        TEXT,
      product_id         TEXT,
      predicted_rating   DOUBLE PRECISION,
      rank               INTEGER
    );
    """
    with engine.begin() as conn:
        conn.execute(text(create_tbl))
        # Clear out old recommendations
        conn.execute(text("TRUNCATE TABLE analytics.recommendations;"))
    logger.info("Prepared analytics.recommendations table")

    # 2) Load your CF model
    model = joblib.load(CF_MODEL_PATH)
    logger.info("Loaded CF model from {}", CF_MODEL_PATH)

    # 3) Fetch all customers and products
    customers = pd.read_sql('SELECT customer_id FROM analytics.dim_customers', engine)
    products  = pd.read_sql('SELECT product_id FROM analytics.dim_products', engine)
    logger.info("Fetched {} customers and {} products", len(customers), len(products))

    recs = []
    # 4) For each customer, predict for each unrated product
    for uid in customers['customer_id']:
        # which products this user has already rated/purchased?
        rated = pd.read_sql(
            f"SELECT product_id FROM analytics.fact_order_item WHERE customer_id = '{uid}'",
            engine
        )['product_id'].tolist()
        rated_set = set(rated)

        preds = []
        for iid in products['product_id']:
            if iid in rated_set:
                continue
            # Surprise’s SVD predict: returns an object with .est
            pred = model.predict(uid, iid)
            preds.append((iid, pred.est))

        # sort descending by estimated rating
        preds.sort(key=lambda x: x[1], reverse=True)
        for rank, (iid, est) in enumerate(preds[:TOP_N], start=1):
            recs.append({
                'customer_id': uid,
                'product_id': iid,
                'predicted_rating': est,
                'rank': rank
            })

    # 5) Bulk‐insert into Postgres
    recs_df = pd.DataFrame(recs)
    with engine.begin() as conn:
        recs_df.to_sql(
            name='recommendations',
            con=conn,
            schema='analytics',
            if_exists='append',
            index=False
        )
    logger.success("Inserted {} recommendations into analytics.recommendations", len(recs_df))


if __name__ == '__main__':
    main()
