-- Create analytics schema and star schema tables
CREATE SCHEMA IF NOT EXISTS analytics;

-- FACT table: each order item with payment and review
CREATE TABLE IF NOT EXISTS analytics.fact_order_item AS
SELECT
oi.order_id,
oi.order_item_id,
oi.product_id,
o.customer_id,
oi.seller_id,
oi.price AS item_price,
oi.freight_value,
pay.payment_type,
pay.payment_installments,
rev.review_score,
o.order_purchase_timestamp AS purchase_ts
FROM staging.order_items oi
JOIN staging.orders o        ON oi.order_id = o.order_id
LEFT JOIN staging.order_payments pay ON oi.order_id = pay.order_id
LEFT JOIN staging.order_reviews rev  ON oi.order_id = rev.order_id;

-- DIMENSION tables
CREATE TABLE IF NOT EXISTS analytics.dim_customers AS
SELECT DISTINCT customer_id,
customer_unique_id,
customer_zip_code_prefix,
customer_city,
customer_state
FROM staging.customers;

CREATE TABLE IF NOT EXISTS analytics.dim_products AS
SELECT DISTINCT product_id,
product_category_name,
product_name_lenght,
product_description_lenght,
product_photos_qty
FROM staging.products;

CREATE TABLE IF NOT EXISTS analytics.dim_sellers AS
SELECT DISTINCT seller_id,
seller_zip_code_prefix,
seller_city,
seller_state
FROM staging.sellers;

-- TIME dimension
CREATE TABLE IF NOT EXISTS analytics.dim_date AS
SELECT DISTINCT
CAST(o.order_purchase_timestamp AS DATE) AS dt,
EXTRACT(YEAR FROM o.order_purchase_timestamp) AS year,
EXTRACT(MONTH FROM o.order_purchase_timestamp) AS month,
EXTRACT(DAY FROM o.order_purchase_timestamp) AS day,
TO_CHAR(o.order_purchase_timestamp, 'Day') AS weekday
FROM staging.orders o;