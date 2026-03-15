import pandas as pd
import numpy as np

np.random.seed(42)
n = 100
df = pd.DataFrame({
    'customer_id': range(1, n+1),
    'name':        [f'Customer_{i}' for i in range(1, n+1)],
    'city':        np.random.choice(['Warsaw','Krakow','Wroclaw','Gdansk'], n),
    'category':    np.random.choice(['Electronics','Clothing','Food','Sports'], n),
    'sales':       np.round(np.random.uniform(10, 2000, n), 2),
    'quantity':    np.random.randint(1, 20, n),
    'date':        pd.date_range('2026-01-01', periods=n, freq='D'),
    'status':      np.random.choice(['Active','Inactive'], n, p=[0.8, 0.2]),
})
df.loc[np.random.choice(df.index, 8, replace=False), 'sales'] = np.nan
df.loc[np.random.choice(df.index, 5, replace=False), 'city']  = None

# How do you get a quick overview of a DataFrame?
df.head()            # first 5 rows
df.shape             # (rows, columns)
df.dtypes            # data type per column
df.info()            # types + non-null counts + memory usage
df.describe()        # stats for numeric columns

# What is the difference between loc and iloc?
df.loc[0:4, 'city':'sales'] # loc  → label-based: use column/row NAMES, end is INCLUSIVE
df.iloc[0:5, 0:3]           # iloc → position-based: use integer positions, end is EXCLUSIVE

# How do you select multiple columns from a DataFrame?
df[['name', 'city', 'sales']]

# How do you add a new column?
df['revenue'] = df['sales'] * df['quantity']           # from expression
df['is_high_value'] = df['sales'] > 1000               # boolean column

# How do you rename columns?
df.rename(columns={'sales': 'Sales_EUR', 'city': 'City'}, inplace=True)
df.columns = [c.lower().replace(' ', '_') for c in df.columns]  # lowercase all at once

# How do you remove a column?
df.drop(columns=['revenue'])                           # returns new DataFrame
df.drop(columns=['revenue'], inplace=True)             # modifies in place

# How do you sort a DataFrame?
df.sort_values('sales', ascending=False)
df.sort_values(['city', 'sales'], ascending=[True, False])

# How do you get the top 5 rows by sales?
df.nlargest(5, 'sales')
# alternative: df.sort_values('sales', ascending=False).head(5)

# How do you count unique values in a column?
df['city'].nunique()
df['city'].value_counts()
df['city'].value_counts(normalize=True)   # as proportions

# How do you reset the index after filtering or sorting?
df.sort_values('sales').reset_index(drop=True)