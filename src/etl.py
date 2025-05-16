import os
from pathlib import Path
import pandas as pd
from loguru import logger

# Directories
RAW_DIR = Path('data/raw/olist_public')
PROCESSED_DIR = Path('data/processed')

# List of raw CSV filenames (without extension)
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

def load_and_clean(table_name: str) -> pd.DataFrame:
    """
    Load raw CSV and perform basic cleaning per table.
    """
    file_path = RAW_DIR / f"{table_name}.csv"
    logger.info(f"Loading {file_path}...")
    df = pd.read_csv(file_path)

    # Parse date/time columns
    date_cols = [col for col in df.columns if 'date' in col or 'timestamp' in col]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # Standardize column names to lowercase snake_case
    df.columns = [col.lower() for col in df.columns]

    # Drop duplicates
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    logger.info(f"Dropped {before - after} duplicate rows from {table_name}.")

    logger.info(f"Cleaned {table_name}: {len(df)} rows, {len(df.columns)} columns")
    return df


def main():
    # Ensure processed directory exists
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    for table in TABLES:
        df = load_and_clean(table)
        out_path = PROCESSED_DIR / f"{table}.parquet"
        # Save as Parquet for efficient storage
        df.to_parquet(out_path, index=False)
        logger.info(f"Wrote processed data to {out_path}")

    logger.info("All tables processed and saved to 'data/processed/'.")


if __name__ == "__main__":
    main()
