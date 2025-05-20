# notebooks/exploratory_analysis.py
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#   kernelspec:
#     name: python3
#     display_name: Python 3
# ---

import sys
from pathlib import Path
# Ensure src/ is on path BEFORE local imports
sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))

import os
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from db_utils import get_db_url  # now resolvable

# Project root and docs directory
project_root = Path(__file__).resolve().parent.parent
docs_dir = project_root / 'docs'
docs_dir.mkdir(exist_ok=True)

# Load environment variables
dotenv_path = project_root / '.env'
load_dotenv(dotenv_path)

# Create engines for staging and analytics schemas
staging_engine = create_engine(get_db_url(schema='staging'))
analytics_engine = create_engine(get_db_url(schema='analytics'))

# Load dataframes
fact = pd.read_sql('SELECT * FROM fact_order_item', analytics_engine)
orders_info = pd.read_sql(
    'SELECT order_id, order_purchase_timestamp, order_delivered_customer_date FROM staging.orders',
    staging_engine
)

# #1 Figure: Distribution of review scores
plt.figure()
fact['review_score'].hist(bins=5)
plt.title('Distribution of Review Scores')
plt.xlabel('Review Score')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig(docs_dir / 'fig1_review_score_dist.png')

# #2 Figure: Daily order counts over time
orders = fact[['order_id', 'purchase_ts']].drop_duplicates()
orders['purchase_date'] = pd.to_datetime(orders['purchase_ts']).dt.date
daily_orders = orders.groupby('purchase_date').size()
plt.figure()
daily_orders.plot()
plt.title('Daily Order Count')
plt.xlabel('Date')
plt.ylabel('Number of Orders')
plt.tight_layout()
plt.savefig(docs_dir / 'fig2_daily_order_count.png')

# #3 Figure: Monthly revenue trend
fact['purchase_month'] = pd.to_datetime(fact['purchase_ts']).dt.to_period('M')
monthly_rev = fact.groupby('purchase_month').agg(
    item_price_sum=('item_price', 'sum'),
    freight_value_sum=('freight_value', 'sum')
)
monthly_rev['total_revenue'] = monthly_rev['item_price_sum'] + monthly_rev['freight_value_sum']
plt.figure()
monthly_rev['total_revenue'].plot()
plt.title('Monthly Total Revenue')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.tight_layout()
plt.savefig(docs_dir / 'fig3_monthly_revenue.png')

# #4 Figure: Delivery delay distribution
orders_info['delay_days'] = (
    pd.to_datetime(orders_info['order_delivered_customer_date']) - 
    pd.to_datetime(orders_info['order_purchase_timestamp'])
).dt.days
plt.figure()
orders_info['delay_days'].dropna().hist(bins=20)
plt.title('Delivery Delay (Days) Distribution')
plt.xlabel('Days')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig(docs_dir / 'fig4_delivery_delay.png')

# #5 Figure: Top 10 customers by order count
top_cust_count = fact.groupby('customer_id')['order_id'].nunique().nlargest(10)
plt.figure()
top_cust_count.plot(kind='barh')
plt.title('Top 10 Customers by Order Count')
plt.xlabel('Number of Orders')
plt.ylabel('Customer ID')
plt.tight_layout()
plt.savefig(docs_dir / 'fig5_top_customers_orders.png')

# #6 Figure: Top 10 customers by total spend
total_spend = fact.groupby('customer_id').agg(total_spent=('item_price', 'sum'))
top_spend = total_spend['total_spent'].nlargest(10)
plt.figure()
top_spend.plot(kind='barh')
plt.title('Top 10 Customers by Total Spend')
plt.xlabel('Total Spend')
plt.ylabel('Customer ID')
plt.tight_layout()
plt.savefig(docs_dir / 'fig6_top_customers_spend.png')

# #7 Figure: Top 10 product categories by sales volume
query_cat = '''
SELECT dp.product_category_name, COUNT(*) AS sales_count
FROM fact_order_item f
JOIN dim_products dp USING(product_id)
GROUP BY dp.product_category_name
ORDER BY sales_count DESC LIMIT 10
'''
prod_cat = pd.read_sql(query_cat, analytics_engine)
plt.figure()
prod_cat.set_index('product_category_name')['sales_count'].plot(kind='barh')
plt.title('Top 10 Product Categories by Sales Volume')
plt.xlabel('Sales Count')
plt.ylabel('Category')
plt.tight_layout()
plt.savefig(docs_dir / 'fig7_top_categories.png')

# #8 Figure: Payment type distribution
query_pay = '''
SELECT payment_type, COUNT(*) AS cnt
FROM fact_order_item
GROUP BY payment_type;
'''
pay_dist = pd.read_sql(query_pay, analytics_engine)
plt.figure()
pay_dist.set_index('payment_type')['cnt'].plot(kind='pie', autopct='%1.1f%%')
plt.title('Payment Type Distribution')
plt.ylabel('')
plt.tight_layout()
plt.savefig(docs_dir / 'fig8_payment_dist.png')

# #9 Figure: Customer geographic distribution (top 10 states)
cust_states = pd.read_sql('SELECT customer_state FROM dim_customers', analytics_engine)
state_counts = cust_states['customer_state'].value_counts().nlargest(10)
plt.figure()
state_counts.plot(kind='bar')
plt.title('Top 10 Customer States')
plt.xlabel('State')
plt.ylabel('Number of Customers')
plt.tight_layout()
plt.savefig(docs_dir / 'fig9_customer_states.png')

# #10 Figure: Order frequency distribution
order_freq = orders.groupby('order_id').size()  # corrected grouping
freq_counts = order_freq.value_counts().sort_index()
plt.figure()
freq_counts.plot(kind='bar')
plt.title('Order Frequency Distribution')
plt.xlabel('Number of Orders per Customer')
plt.ylabel('Count of Instances')
plt.tight_layout()
plt.savefig(docs_dir / 'fig10_order_frequency.png')

# Print summary tables
print('Top 10 customers by order count:')
print(top_cust_count)
print('\nTop 10 customers by total spend:')
print(top_spend)
print('\nTop 10 product categories by sales volume:')
print(prod_cat)
