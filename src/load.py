from pathlib import Path
import pandas as pd
from loguru import logger
from .db_utils import get_engine

# Where our Parquet lives
PROCESSED_DIR = Path('data/processed')

# These correspond to your processed filenames: orders.parquet, customers.parquet, etc.
TABLES = [
    'orders',
    'order_items',
    'order_payments',
    'order_reviews',
    'customers',
    'products',
    'sellers',
    'geolocation'
]

def main():
    # 1) Connect to the staging schema
    engine = get_engine(schema='staging')

    # 2) Loop over each table, load Parquet → write to Postgres
    for tbl in TABLES:
        path = PROCESSED_DIR / f"{tbl}.parquet"
        logger.info(f"Loading `{tbl}` from {path} …")
        df = pd.read_parquet(path)

        # Overwrite any existing data in staging
        df.to_sql(tbl, con=engine, schema='staging',
                  if_exists='replace', index=False)
        logger.info(f"  ↳ {len(df)} rows inserted into staging.{tbl}")

    # 3) Once staging is full, run our analytics transforms
    #    (this file should contain your CTAS statements)
    transform_sql = Path('sql/dml/transform_analytics.sql').read_text()
    with engine.begin() as conn:
        conn.execute(transform_sql)
    logger.success("Analytics star‐schema populated successfully!")

if __name__ == '__main__':
    main()
