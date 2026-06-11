import pandas as pd
import numpy as np

df = pd.read_csv('ecommerce.csv')

print("=== RAW DATASET ===")
print(df.shape)
print(df.head())
print()

df['total_cost']      = df['price'] * df['quantity']
df['discount_amount'] = df['total_cost'] * df['discount_percent'] / 100
df['final_price']     = df['total_cost'] - df['discount_amount']
df['price_per_unit']  = df['final_price'] / df['quantity']

print("=== After Mathematical Transform ===")
print(df[['order_id', 'product', 'price', 'quantity',
          'total_cost', 'discount_amount', 'final_price']].head())
print()

df['order_date']    = pd.to_datetime(df['order_date'])
df['order_month']   = df['order_date'].dt.month
df['order_year']    = df['order_date'].dt.year
df['order_day']     = df['order_date'].dt.day_name()
df['order_quarter'] = df['order_date'].dt.quarter

print("=== After Date/Time Extraction ===")
print(df[['order_id', 'order_date', 'order_month',
          'order_year', 'order_day', 'order_quarter']].head())
print()

df['is_senior']        = np.where(df['customer_age'] >= 65, 1, 0)
df['high_value_order'] = np.where(df['final_price'] > 50000, 1, 0)
df['heavy_discount']   = np.where(df['discount_percent'] >= 20, 1, 0)

print("=== After Conditional Logic ===")
print(df[['order_id', 'product', 'customer_age', 'is_senior',
          'final_price', 'high_value_order', 'heavy_discount']].head(10))
print()

print("=== FINAL DATASET ===")
print(df.head(10))
print("\nShape:", df.shape)
print("\nAll Columns:", df.columns.tolist())
