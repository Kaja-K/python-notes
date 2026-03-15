import pandas as pd
import numpy as np

np.random.seed(42)
n = 100
df = pd.DataFrame({
    'customer_id': range(1, n+1),
    'city':        np.random.choice(['Warsaw','Krakow','Wroclaw','Gdansk'], n),
    'category':    np.random.choice(['Electronics','Clothing','Food','Sports'], n),
    'sales':       np.round(np.random.uniform(10, 2000, n), 2),
    'quantity':    np.random.randint(1, 20, n),
    'date':        pd.date_range('2026-01-01', periods=n, freq='D'),
    'status':      np.random.choice(['Active','Inactive'], n, p=[0.8, 0.2]),
})
df.loc[np.random.choice(df.index, 8, replace=False), 'sales'] = np.nan
df.loc[np.random.choice(df.index, 5, replace=False), 'city']  = None

# How do you filter rows based on a condition?
df[df['sales'] > 1000]

# How do you apply multiple filter conditions?
df[(df['sales'] > 100) & (df['sales'] < 500)]       # AND
df[(df['city'] == 'Warsaw') | (df['sales'] > 1500)]  # OR
df[~(df['status'] == 'Inactive')]                    # NOT

# How do you filter using a list of values?
df[df['city'].isin(['Warsaw', 'Krakow'])]
df[~df['city'].isin(['Gdansk'])]                     # NOT in list

# How do you filter using string patterns?
df[df['city'].str.startswith('W', na=False)]
df[df['city'].str.contains('aw', na=False)]

# What is the query() method and when is it useful?
df.query('sales > 1000')
df.query('city == "Warsaw" and sales > 500')
threshold = 500
df.query('sales > @threshold')   # reference external variable with @

# How do you detect missing values in a DataFrame?
df.isnull().sum()                          # count NaN per column
df.isnull().sum() / len(df) * 100          # percentage missing — check this first

# What are the different strategies for handling missing values?
df.dropna()                                # drop rows with ANY NaN
df.dropna(subset=['sales'])                # drop only where sales is NaN
df['sales'].fillna(df['sales'].mean())     # fill with mean
df['sales'].fillna(df['sales'].median())   # fill with median (robust to outliers)
df['sales'].fillna(method='ffill')         # forward fill — best for time series
df['sales'].fillna(method='bfill')         # backward fill
df['sales'].interpolate()                  # linear interpolation

# When would you use interpolate() instead of fillna()?
# fillna() fills with a fixed or computed constant — good for general NaN
# interpolate() estimates based on surrounding values — good for time series
# where the trend matters and NaN values logically sit between known values

# How do you find and remove duplicate rows?
df.duplicated().sum()                       # count duplicates
df.drop_duplicates()                        # remove, keep first occurrence
df.drop_duplicates(keep='last')             # keep last
df.drop_duplicates(subset=['customer_id'])  # deduplicate by specific column

# How do you convert column data types?
df['quantity'].astype('float32')
df['status'].astype('category')            # saves memory for repeated strings
pd.to_datetime(df['date'])
pd.to_numeric(df['sales'], errors='coerce') # NaN if conversion fails

# How do you clean string columns?
df['city'].str.strip()                      # remove whitespace
df['city'].str.lower()
df['city'].str.replace('old', 'new')
df['city'].str.contains('aw', na=False)

# clean pipeline — chain multiple operations
df['city'] = df['city'].str.strip().str.title()

# How do you replace specific values in a column?
df['status'].replace('Inactive', 'Churned')
df.replace({'status': {'Inactive': 'Churned', 'Active': 'Current'}})
df['city'].replace('', np.nan)             # turn empty strings into NaN