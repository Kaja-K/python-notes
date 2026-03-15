import pandas as pd
import numpy as np

np.random.seed(42)
n = 200
df = pd.DataFrame({
    'customer_id': range(1, n+1),
    'city':        np.random.choice(['Warsaw','Krakow','Wroclaw','Gdansk','Poznan'], n),
    'category':    np.random.choice(['Electronics','Clothing','Food','Sports'], n),
    'sales':       np.round(np.random.uniform(10, 2000, n), 2),
    'quantity':    np.random.randint(1, 20, n),
    'discount':    np.round(np.random.uniform(0, 0.3, n), 2),
    'status':      np.random.choice(['Active','Inactive'], n, p=[0.8, 0.2]),
})

# How does groupby() work? Explain the Split-Apply-Combine pattern.
# Split: divide data into groups based on a column
# Apply: apply a function (sum/mean/count) to each group independently
# Combine: merge group results into a single output
df.groupby('city')['sales'].sum()
df.groupby('city')['sales'].mean()
df.groupby('city')['sales'].agg(['sum', 'mean', 'count', 'max'])

# How do you apply different aggregations to different columns?
df.groupby('city').agg(
    total_sales  = ('sales',       'sum'),
    avg_sales    = ('sales',       'mean'),
    order_count  = ('customer_id', 'count'),
    avg_qty      = ('quantity',    'mean')
).reset_index()

# How do you group by multiple columns?
df.groupby(['city', 'category'])['sales'].sum().reset_index()

# What is the difference between groupby() and pivot_table()?
# groupby() returns a GroupBy object, then you apply aggregation
# pivot_table() gives you a 2D summary table directly — row AND column dimensions
# groupby is more flexible; pivot_table is better for visual cross-tab analysis

pd.pivot_table(df,
    values    = 'sales',
    index     = 'city',
    columns   = 'category',
    aggfunc   = 'sum',
    fill_value= 0
)

# What is transform() and how is it different from agg()?
# agg() collapses groups to one row per group (reduces rows)
# transform() returns same-length result — every row stays
# use transform when you want to ADD a group statistic as a new column

df['city_avg_sales'] = df.groupby('city')['sales'].transform('mean')
df['diff_from_city_avg'] = df['sales'] - df['city_avg_sales']

# z-score within each city
df['sales_zscore'] = df.groupby('city')['sales'].transform(
    lambda x: (x - x.mean()) / x.std()
)

# What is the difference between map(), apply() and applymap()?
# map()      → element-wise on a Series (fastest for simple replacements)
# apply()    → row-wise or column-wise on DataFrame, or element-wise on Series
# applymap() → element-wise on entire DataFrame (deprecated in newer pandas → use map())
tier_map = {'Active': 1, 'Inactive': 0}
df['status_code'] = df['status'].map(tier_map)  # map: replace values using a dict
df['revenue'] = df.apply(lambda row: row['sales'] * (1 - row['discount']), axis=1) 
# apply: custom function across rows (slow — avoid for numeric ops)
df['revenue'] = df['sales'] * (1 - df['discount'])   # same result, much faster
# vectorised is always faster than apply for numeric operations

# How do you keep only groups with more than 30 rows?
df.groupby('city').filter(lambda x: len(x) > 30)

# How do you calculate percentage of total for each category?
cat_sales = df.groupby('category')['sales'].sum()
(cat_sales / cat_sales.sum() * 100).round(1)

# How do you rank rows within a group?
df['rank_in_city'] = df.groupby('city')['sales'].rank(ascending=False)

# How do you calculate a cumulative sum within each group?
df['cumulative_sales'] = df.groupby('city')['sales'].cumsum()