import pandas as pd
import numpy as np

np.random.seed(42)

df_orders = pd.DataFrame({
    'order_id':    range(1, 101),
    'customer_id': np.random.randint(1, 21, 100),
    'amount':      np.round(np.random.uniform(50, 2000, 100), 2),
    'date':        pd.date_range('2026-01-01', periods=100, freq='D'),
    'status':      np.random.choice(['Completed','Pending','Cancelled'], 100),
})
df_customers = pd.DataFrame({
    'customer_id': range(1, 21),
    'name':        [f'Customer_{i}' for i in range(1, 21)],
    'city':        np.random.choice(['Warsaw','Krakow','Wroclaw'], 20),
    'tier':        np.random.choice(['Gold','Silver','Bronze'], 20),
})

# What is the difference between merge(), join() and concat()?
# merge()  → SQL-style join on column values — most flexible
# join()   → merges on the index — shorthand for index-based merge
# concat() → just stacks DataFrames without key matching (adds rows or columns)

# How do you perform different types of joins in pandas?
pd.merge(df_orders, df_customers, on='customer_id')                       # inner (default)
pd.merge(df_orders, df_customers, on='customer_id', how='left')           # left join
pd.merge(df_orders, df_customers, on='customer_id', how='right')          # right join
pd.merge(df_orders, df_customers, on='customer_id', how='outer')          # full outer

# How do you find rows that exist in one DataFrame but not the other (anti-join)?
merged = pd.merge(df_orders, df_customers, on='customer_id', how='left', indicator=True)
no_match = merged[merged['_merge'] == 'left_only'].drop(columns='_merge')

# How do you stack multiple DataFrames vertically?
df1 = df_orders.iloc[:50]
df2 = df_orders.iloc[50:]
pd.concat([df1, df2], ignore_index=True)    # reset index after stacking

# How do you combine multiple CSV files into one DataFrame?
import glob
# files = glob.glob('data/*.csv')
# df_all = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

# How do you convert a string column to datetime?
df_orders['date'] = pd.to_datetime(df_orders['date'])
pd.to_datetime('14/03/2026', dayfirst=True)

# How do you extract date components from a datetime column?
df_orders['year']      = df_orders['date'].dt.year
df_orders['month']     = df_orders['date'].dt.month
df_orders['day']       = df_orders['date'].dt.day
df_orders['dayofweek'] = df_orders['date'].dt.dayofweek   # 0=Monday, 6=Sunday
df_orders['day_name']  = df_orders['date'].dt.day_name()
df_orders['quarter']   = df_orders['date'].dt.quarter

# How do you filter rows by date range?
df_orders[df_orders['date'] >= '2026-03-01']
df_orders[df_orders['date'].dt.month == 3]    # only March rows

# What is resample() and when would you use it?
# resample() regroups time series data into new time buckets — like groupby for time
# requires the date column to be set as the index
df_ts = df_orders.set_index('date')
df_ts['amount'].resample('W').sum()    # weekly total
df_ts['amount'].resample('ME').mean()  # monthly average
df_ts['amount'].resample('QE').sum()   # quarterly total

# How do you calculate the number of days between two dates?
(pd.Timestamp('2026-12-31') - df_orders['date']).dt.days

# How do you find customers who haven't ordered in the last 30 days?
last_order = df_orders.groupby('customer_id')['date'].max()
churned    = last_order[last_order < pd.Timestamp.now() - pd.DateOffset(days=30)]

# How do you format a datetime column as a string?
df_orders['date'].dt.strftime('%Y-%m')    # '2026-03'
df_orders['date'].dt.strftime('%d/%m/%Y') # '14/03/2026'