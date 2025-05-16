import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from loguru import logger
# Load .env variables
load_dotenv()
def get_db_url(schema: str = 'public') -> str:
    """
    Build a Postgres URL (with search_path set to schema) using:
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
    """
    user     = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host     = os.getenv('DB_HOST', 'localhost')
    port     = os.getenv('DB_PORT', '5432')
    name     = os.getenv('DB_NAME')
    if not all([user, password, name]):
        logger.error("Missing DB_USER, DB_PASSWORD or DB_NAME in .env")
        raise RuntimeError("Database credentials incomplete")
    return (
        f"postgresql://{user}:{password}@{host}:{port}/{name}"
        f"?options=-csearch_path%3D{schema}"
    )
def get_engine(schema: str = 'public'):
    """Return a SQLAlchemy engine for the given schema."""
    url = get_db_url(schema)
    logger.info(f"Creating engine for schema `{schema}`")
    return create_engine(url)

def log(msg: str):
    """Alias for structured logging in ETL scripts."""
    logger.info(msg)
