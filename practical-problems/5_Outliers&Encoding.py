import pandas as pd
import numpy as np
from scipy import stats

np.random.seed(42)
n = 200
df = pd.DataFrame({
    'customer_id': range(1, n+1),
    'city':        np.random.choice(['Warsaw','Krakow','Wroclaw','Gdansk','Poznan'], n),
    'category':    np.random.choice(['Electronics','Clothing','Food','Sports'], n),
    'sales':       np.round(np.random.uniform(10, 2000, n), 2),
    'quantity':    np.random.randint(1, 20, n),
    'age':         np.random.randint(18, 70, n),
    'status':      np.random.choice(['Active','Inactive','Churned'], n, p=[0.7,0.2,0.1]),
})
df.loc[0, 'sales'] = 50000    # artificial outlier
df.loc[1, 'sales'] = -500     # artificial outlier

# How do you detect outliers using the IQR method?
# IQR is robust — it doesn't assume normal distribution
Q1  = df['sales'].quantile(0.25)
Q3  = df['sales'].quantile(0.75)
IQR = Q3 - Q1
outliers_iqr = df[(df['sales'] < Q1 - 1.5 * IQR) | (df['sales'] > Q3 + 1.5 * IQR)]
print(f"IQR outliers: {len(outliers_iqr)}")

# How do you detect outliers using Z-score?
# Z-score assumes normal distribution — flag anything > 3 std from mean
z_scores    = np.abs(stats.zscore(df['sales']))
outliers_z  = df[z_scores > 3]
print(f"Z-score outliers: {len(outliers_z)}")

# When would you use IQR vs Z-score?
# IQR  → skewed distributions, data with extreme outliers — more robust
# Z-score → when data is approximately normally distributed

# How do you handle outliers once detected?
df['sales_clipped'] = df['sales'].clip(lower=0, upper=Q3 + 1.5 * IQR)   # cap at boundary
median = df['sales'].median()
df['sales_clean']   = df['sales'].where(z_scores <= 3, median)           # replace with median

# How do you calculate descriptive statistics for a column?
df['sales'].mean()
df['sales'].median()
df['sales'].mode()[0]
df['sales'].std()
df['sales'].skew()     # >0 right-skewed, <0 left-skewed
df['sales'].kurt()     # >0 heavy tails vs normal
df['sales'].describe()

# How do you compute a correlation matrix?
df[['sales','quantity','age']].corr()                         # Pearson (linear)
df[['sales','quantity','age']].corr(method='spearman')        # Spearman (rank-based)

# When would you use Spearman instead of Pearson correlation?
# Pearson measures linear relationship — assumes normal data
# Spearman measures monotonic relationship — robust, works for skewed data

# How do you perform label encoding in pandas?
# Use when the category is ordinal (has a meaningful order) or binary
codes, uniques = pd.factorize(df['status'])
df['status_code'] = codes
mapping = dict(enumerate(uniques))   # {0: 'Active', 1: 'Inactive', 2: 'Churned'}

# explicit ordered encoding
order = pd.CategoricalDtype(['Active', 'Inactive', 'Churned'], ordered=True)
df['status_ordered'] = df['status'].astype(order).cat.codes

# How do you perform one-hot encoding in pandas?
# Use for nominal (unordered) categories to avoid implying order
dummies = pd.get_dummies(df, columns=['category', 'city'], drop_first=True)
# drop_first=True avoids multicollinearity (drops one dummy per group)

# How do you reduce a DataFrame's memory usage?
print("Before:", df.memory_usage(deep=True).sum() // 1024, "KB")
df['category'] = df['category'].astype('category')   # biggest win for repeated strings
df['city']     = df['city'].astype('category')
df['sales']    = df['sales'].astype('float32')        # halves float memory
df['quantity'] = df['quantity'].astype('int16')
print("After:", df.memory_usage(deep=True).sum() // 1024, "KB")

# How do you handle large datasets that don't fit in memory?
# 1. Load in chunks: pd.read_csv('file.csv', chunksize=10000)
# 2. Optimise dtypes before loading (use category, float32)
# 3. Use dask for parallel processing
# 4. Load only needed columns: pd.read_csv('file.csv', usecols=['a','b'])
# 5. Use parquet format — columnar, compressed, type-preserving

# How do you bin a continuous variable into buckets?
df['sales_band'] = pd.cut(df['sales'],
    bins  = [0, 200, 500, 1000, 2000],
    labels= ['Low', 'Medium', 'High', 'Very High']
)

# equal-size groups (by frequency)
df['sales_quartile'] = pd.qcut(df['sales_clean'], q=4, labels=['Q1','Q2','Q3','Q4'])

# What is the difference between pd.cut() and pd.qcut()?
# pd.cut()  → equal-width bins — based on value range
# pd.qcut() → equal-frequency bins — based on percentiles (same number of rows per bin)

# How do you create a frequency cross-table between two columns?
pd.crosstab(df['city'], df['status'])
pd.crosstab(df['city'], df['status'], normalize='index').round(2)  # row percentages