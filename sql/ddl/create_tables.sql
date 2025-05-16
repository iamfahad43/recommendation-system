-- Create staging tables (mirror raw CSVs)
CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.orders (
order_id TEXT PRIMARY KEY,
customer_id TEXT,
order_status TEXT,
order_purchase_timestamp TIMESTAMP,
order_approved_at TIMESTAMP,
order_delivered_carrier_date TIMESTAMP,
order_delivered_customer_date TIMESTAMP,
order_estimated_delivery_date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.order_items (
order_id TEXT,
order_item_id INTEGER,
product_id TEXT,
seller_id TEXT,
shipping_limit_date TIMESTAMP,
price NUMERIC,
freight_value NUMERIC
);

CREATE TABLE IF NOT EXISTS staging.order_payments (
order_id TEXT,
payment_sequential INTEGER,
payment_type TEXT,
payment_installments INTEGER,
payment_value NUMERIC
);

CREATE TABLE IF NOT EXISTS staging.order_reviews (
review_id TEXT PRIMARY KEY,
order_id TEXT,
review_score INTEGER,
review_comment_title TEXT,
review_comment_message TEXT,
review_creation_date TIMESTAMP,
review_answer_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS staging.customers (
customer_id TEXT PRIMARY KEY,
customer_unique_id TEXT,
customer_zip_code_prefix TEXT,
customer_city TEXT,
customer_state TEXT
);

CREATE TABLE IF NOT EXISTS staging.products (
product_id TEXT PRIMARY KEY,
product_category_name TEXT,
product_name_lenght INTEGER,
product_description_lenght INTEGER,
product_photos_qty INTEGER
);

CREATE TABLE IF NOT EXISTS staging.sellers (
seller_id TEXT PRIMARY KEY,
seller_zip_code_prefix TEXT,
seller_city TEXT,
seller_state TEXT
);

CREATE TABLE IF NOT EXISTS staging.geolocation (
geolocation_zip_code_prefix TEXT,
geolocation_latitude NUMERIC,
geolocation_longitude NUMERIC,
geolocation_city TEXT,
geolocation_state TEXT
);