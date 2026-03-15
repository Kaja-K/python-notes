import pandas as pd

df1 = pd.DataFrame({'ID': [1, 2, 3], 'City': ['Wroclaw', 'Warsaw', 'Krakow']})
df2 = pd.DataFrame({'ID': [2, 3, 4], 'Load': [40, 95, 50]})

# ── MERGE (SQL-style joins) ───────────────────────────────────
pd.merge(df1, df2, on='ID')                    # inner join — only matching IDs
pd.merge(df1, df2, on='ID', how='inner')       # explicit inner join
pd.merge(df1, df2, on='ID', how='left')        # LEFT join — all df1 rows, NaN if no match
pd.merge(df1, df2, on='ID', how='right')       # RIGHT join — all df2 rows
pd.merge(df1, df2, on='ID', how='outer')       # FULL OUTER — all rows from both

# merge on different column names
pd.merge(df1, df2, left_on='ID', right_on='ID')

# merge on multiple keys
pd.merge(df1, df2, on=['ID', 'City'])

# show which rows have/don't have a match (indicator column)
pd.merge(df1, df2, on='ID', how='outer', indicator=True)
# _merge column: 'both', 'left_only', 'right_only'

# ── JOIN — index-based merge ─────────────────────────────────
df1.set_index('ID').join(df2.set_index('ID'))           # inner join on index
df1.set_index('ID').join(df2.set_index('ID'), how='left')  # left join

# ── CONCAT — stack DataFrames ────────────────────────────────
pd.concat([df1, df2])                   # stack vertically (add rows)
pd.concat([df1, df2], ignore_index=True)  # reset index after stacking
pd.concat([df1, df2], axis=1)           # stack horizontally (add columns)
pd.concat([df1, df2], axis=1, join='inner')  # only keep rows present in both

# ── PRACTICAL PATTERNS ───────────────────────────────────────
# anti-join — rows in df1 NOT in df2
merged = pd.merge(df1, df2, on='ID', how='left', indicator=True)
anti = merged[merged['_merge'] == 'left_only'].drop(columns='_merge')

# combine monthly reports stacked vertically
import glob
files = glob.glob('reports/*.csv')
all_dfs = [pd.read_csv(f) for f in files]
combined = pd.concat(all_dfs, ignore_index=True)