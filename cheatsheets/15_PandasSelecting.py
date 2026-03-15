import pandas as pd

data = {'ID':[1,2,3,4,5], 'City':['Wroclaw','Warsaw','Krakow','Wroclaw','Gdansk'],
        'Load':[85,40,95,20,50], 'Date':['2026-03-01']*5}
df = pd.DataFrame(data)

# ── SELECTING COLUMNS ────────────────────────────────────────
df['City']                      # single column → Series
df[['City', 'Load']]            # multiple columns → DataFrame
df.City                         # dot notation — only works for simple names

# ── LOC — label-based ────────────────────────────────────────
# uses column/row NAMES — end index is INCLUSIVE
df.loc[0]                       # row with label 0
df.loc[0:2]                     # rows 0, 1, 2 (all inclusive!)
df.loc[0:2, 'City':'Load']      # rows 0-2, columns City through Load
df.loc[:, 'Load']               # all rows, Load column
df.loc[0, 'City']               # single cell by label
df.set_index('ID')              # set a column as the index
df.set_index('ID').loc[3]       # then use loc with the new index

# ── ILOC — position-based ────────────────────────────────────
# uses integer positions — end index is EXCLUSIVE (like Python slices)
df.iloc[0]                      # first row
df.iloc[0:3]                    # rows at positions 0, 1, 2
df.iloc[0:5, 0:2]               # rows 0-4, columns 0-1
df.iloc[-1]                     # last row
df.iloc[:, -1]                  # last column
df.iloc[[0, 2, 4]]              # specific rows by position
df.iloc[0, 0]                   # single cell by position

# loc vs iloc — key difference:
# df.loc[0:2]   → rows LABELED 0, 1, 2  — end INCLUSIVE
# df.iloc[0:2]  → rows at POSITIONS 0, 1 — end EXCLUSIVE

# ── FILTERING ROWS ───────────────────────────────────────────
df[df['Load'] > 80]                                  # single condition
df[(df['Load'] > 30) & (df['Load'] < 90)]            # AND — use & not 'and'
df[(df['City'] == 'Wroclaw') | (df['Load'] > 80)]    # OR  — use | not 'or'
df[~(df['Load'] > 50)]                               # NOT — use ~

df[df['City'].isin(['Wroclaw', 'Krakow'])]           # match list of values
df[~df['City'].isin(['Warsaw'])]                     # NOT in list
df[df['City'].str.contains('raw', na=False)]         # substring match
df[df['City'].str.startswith('W')]                   # starts with

df[df['City'].isna()]                                # rows where value is NaN
df[df['City'].notna()]                               # rows where value is not NaN

# ── QUERY — SQL-like syntax ──────────────────────────────────
df.query('Load > 50')
df.query('City == "Wroclaw" and Load > 30')
threshold = 50
df.query('Load > @threshold')                        # reference variable with @

# ── SORT & TOP N ─────────────────────────────────────────────
df.sort_values('Load')                               # ascending (default)
df.sort_values('Load', ascending=False)              # descending
df.sort_values(['City', 'Load'], ascending=[True, False])  # multi-column sort
df.nlargest(3, 'Load')                               # top 3 rows by Load
df.nsmallest(3, 'Load')                              # bottom 3 rows by Load
df.filter(like='oa', axis=1)                         # columns whose name contains 'oa'