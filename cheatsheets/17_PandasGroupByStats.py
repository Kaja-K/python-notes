import pandas as pd

data = {'ID':[1,2,3,4,5,6], 'City':['Wroclaw','Warsaw','Krakow','Wroclaw','Warsaw','Krakow'],
        'Load':[85,40,95,20,50,30], 'Date':['2026-03-01','2026-03-01','2026-03-01',
                                             '2026-03-02','2026-03-02','2026-03-02']}
df = pd.DataFrame(data)

# ── STATISTICS ───────────────────────────────────────────────
df['Load'].mean()               # average of one column
df['Load'].median()             # median of one column
df['Load'].std()                # standard deviation
df['Load'].var()                # variance
df['Load'].sum()                # total
df['Load'].min()                # minimum
df['Load'].max()                # maximum
df['Load'].count()              # count of non-null values
df['Load'].quantile(0.75)       # 75th percentile

df.mean(numeric_only=True)      # column-wise mean for all numeric columns
df.describe()                   # count/mean/std/min/max in one call
df.corr(numeric_only=True)      # correlation matrix between numeric columns

# ── GROUPBY ──────────────────────────────────────────────────
# split → apply → combine
df.groupby('City')['Load'].mean()       # average load per city
df.groupby('City')['Load'].sum()        # total load per city
df.groupby('City')['Load'].count()      # non-null rows per city
df.groupby('City')['Load'].max()        # max load per city
df.groupby('City')['Load'].min()        # min load per city

# group by multiple columns
df.groupby(['City', 'Date'])['Load'].mean()

# multiple aggregations at once
df.groupby('City')['Load'].agg(['mean', 'max', 'count'])

# different aggregation per column
df.groupby('City').agg({'Load': 'mean', 'ID': 'count'})

# custom agg with named output columns
df.groupby('City')['Load'].agg(
    avg_load='mean',
    max_load='max',
    count='count'
)

# ── APPLY & TRANSFORM ────────────────────────────────────────
df['Load'].apply(lambda x: x * 2)          # apply function to each value
df.apply(lambda col: col.max(), axis=0)    # apply to each column
df.apply(lambda row: row['Load'] * 2, axis=1)  # apply to each row

# transform — like apply but returns same-length result (useful for adding back)
df['Load_zscore'] = df.groupby('City')['Load'].transform(
    lambda x: (x - x.mean()) / x.std()     # z-score within each city group
)

# ── PIVOT TABLE ──────────────────────────────────────────────
# like Excel pivot — summarise by row/column categories
df.pivot_table(index='City', values='Load', aggfunc='sum')
df.pivot_table(index='City', columns='Date', values='Load', aggfunc='mean')
df.pivot_table(index='City', values='Load',
               aggfunc=['mean', 'sum'], fill_value=0)

# ── VALUE COUNTS & CROSS-TAB ─────────────────────────────────
df['City'].value_counts()               # frequency of each city
df['City'].value_counts(normalize=True) # as proportions (0–1)
pd.crosstab(df['City'], df['Date'])     # count co-occurrences of two columns