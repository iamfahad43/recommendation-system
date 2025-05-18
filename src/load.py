# src/load.py

from pathlib import Path
import pandas as pd
from loguru import logger
from .db_utils import get_engine
from sqlalchemy import text

# Directory containing processed Parquet files
PROCESSED_DIR = Path('data/processed')

# List of tables matching processed filenames
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

    # 2) Load each Parquet into staging tables
    for table in TABLES:
        file_path = PROCESSED_DIR / f"{table}.parquet"
        logger.info(f"Loading `{table}` from {file_path}")
        df = pd.read_parquet(file_path)

        # Write to staging schema, replacing existing data
        df.to_sql(
            name=table,
            con=engine,
            schema='staging',
            if_exists='replace',
            index=False
        )
        logger.info(f"Inserted {len(df)} rows into staging.{table}")

    # 3) Read the analytics-schema SQL script
    sql_path = Path('sql/dml/transform_analytics.sql')
    transform_sql = sql_path.read_text()

    # 4) Remove comment lines and empty lines
    lines = transform_sql.splitlines()
    no_comments = [line for line in lines if not line.strip().startswith('--')]
    clean_sql = '\n'.join(no_comments)

    # 5) Split into individual statements
    statements = [
        stmt.strip() for stmt in clean_sql.split(';')
        if stmt.strip()
    ]

    # 6) Execute each DDL/CTAS statement
    with engine.begin() as conn:
        for stmt in statements:
            first_line = stmt.splitlines()[0]
            logger.info(f"Executing SQL: {first_line} ...")
            conn.execute(text(stmt))

    logger.success("Analytics star-schema populated successfully!")

if __name__ == '__main__':
    main()
