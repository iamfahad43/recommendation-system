# src/modeling.py

"""
Train and evaluate recommendation models:
  1) Collaborative Filtering (Surprise SVD)
  2) Content-Based (TF-IDF + cosine similarity)
"""
import sys, os
from pathlib import Path
# Ensure local src/ is on path for helper imports
sys.path.append(str(Path(__file__).resolve().parent))
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from sqlalchemy import create_engine
from src.db_utils import get_db_url
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def get_engine(schema: str = 'analytics'):
    """Create SQLAlchemy engine for given schema"""
    url = get_db_url(schema)
    return create_engine(url)


def collaborative_filtering(model_path: str = 'models/cf_svd.joblib'):
    """
    1) Load ratings from analytics.fact_order_item
    2) Train/test split & train SVD
    3) Evaluate RMSE
    4) Save model
    """
    engine = get_engine('analytics')
    df = pd.read_sql(
        'SELECT customer_id AS user_id, product_id AS item_id, review_score AS rating FROM fact_order_item',
        engine
    )
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[['user_id', 'item_id', 'rating']], reader)

    trainset, testset = train_test_split(data, test_size=0.2)
    algo = SVD(n_factors=50, lr_all=0.005, reg_all=0.02)
    algo.fit(trainset)

    predictions = algo.test(testset)
    rmse = accuracy.rmse(predictions)
    print(f"CF SVD RMSE: {rmse:.4f}")

    joblib.dump(algo, model_path)
    print(f"Model saved to {model_path}")


def content_based(k: int = 10):
    """
    1) Build TF-IDF matrix on product categories
    2) Compute cosine similarity
    3) Return function to get top-k similar items
    """
    engine = get_engine('analytics')
    prod = pd.read_sql('SELECT product_id, product_category_name FROM dim_products', engine)
    prod['cat_str'] = prod['product_category_name'].fillna('').apply(lambda x: x.replace('|', ' '))

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(prod['cat_str'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(prod.index, index=prod['product_id']).drop_duplicates()

    def get_similar(item_id: str, top_n: int = k):
        idx = indices[item_id]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
        return [
            (prod['product_id'].iloc[i], prod['product_category_name'].iloc[i], float(score))
            for i, score in sim_scores
        ]

    joblib.dump(tfidf, 'models/tfidf_vectorizer.joblib')
    joblib.dump(cosine_sim, 'models/cosine_sim.joblib')
    print("Content-based model artifacts saved to models/")

    return get_similar


if __name__ == '__main__':
    collaborative_filtering()
    get_sim = content_based()
    # Sample usage
    engine = get_engine('analytics')
    prod_ids = pd.read_sql('SELECT product_id FROM dim_products', engine)['product_id']
    sample = get_sim(prod_ids.iloc[0], top_n=5)
    print("Sample recommendations:", sample)