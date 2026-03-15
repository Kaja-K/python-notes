import pandas as pd

data = {'ID':[1,2,2,3,4,5], 'City':['Wroclaw','Warsaw','Warsaw','Krakow','Wroclaw',None],
        'Load':[85,40,40,95,20,50], 'Date':['2026-03-01']*6}
df = pd.DataFrame(data)

# ── MISSING VALUES ───────────────────────────────────────────
df.isnull()                          # True where NaN
df.isnull().sum()                    # count NaN per column
df.isnull().sum() / len(df) * 100    # percentage missing
df.notnull()                         # True where NOT NaN

df.dropna()                          # drop rows with any NaN
df.dropna(subset=['City'])           # drop only where City is NaN
df.dropna(thresh=3)                  # keep rows with at least 3 non-NaN values
df.dropna(axis=1)                    # drop columns with any NaN

df.fillna('Unknown')                 # replace all NaN with a value
df.fillna({'City': 'Unknown', 'Load': 0})  # different fill per column
df['Load'].fillna(df['Load'].mean(), inplace=True)  # fill with column mean
df.fillna(method='ffill')            # forward fill — use previous row's value
df.fillna(method='bfill')            # backward fill — use next row's value

# ── DUPLICATES ───────────────────────────────────────────────
df.duplicated()                      # True for each duplicate row
df.duplicated().sum()                # count of duplicate rows
df.duplicated(subset=['City'])       # duplicates based on one column only
df.drop_duplicates()                 # remove duplicates, keep first
df.drop_duplicates(keep='last')      # keep last occurrence instead
df.drop_duplicates(subset=['City'])  # deduplicate by specific column

# ── RENAME & REORDER ─────────────────────────────────────────
df.rename(columns={'Load': 'Load_%', 'City': 'Location'})  # rename columns
df.rename(columns=str.lower)         # lowercase all column names at once
df.columns = ['id', 'city', 'load', 'date']   # set all names at once
df[['id', 'load', 'city', 'date']]  # reorder columns

# ── TYPE CONVERSION ──────────────────────────────────────────
df['ID'].astype('int')              # convert column to int
df['Load'].astype('float32')        # smaller float type — less memory
df['City'].astype('category')       # category type — saves memory for repeated strings
pd.to_datetime(df['Date'])          # parse string column as datetime
pd.to_numeric(df['Load'], errors='coerce')  # convert to number, NaN if fails

# ── REPLACE VALUES ───────────────────────────────────────────
df.replace(40, 0)                   # replace a specific value everywhere
df['City'].replace('Warsaw', 'WAW') # replace in one column
df.replace({'City': {'Warsaw': 'WAW', 'Krakow': 'KRK'}})  # multiple replacements

# ── ADD & DROP COLUMNS ───────────────────────────────────────
df['Double_Load'] = df['Load'] * 2             # new column from expression
df['Label'] = df['Load'].apply(lambda x: 'High' if x > 70 else 'Low')  # apply function
df.drop(columns=['Double_Load'])               # remove a column
df.drop(columns=['col1', 'col2'])              # remove multiple columns
df.insert(1, 'Region', 'PL')                  # insert at specific position

# ── INDEX ────────────────────────────────────────────────────
df.reset_index(drop=True)           # reset to 0,1,2,... (drop=True removes old index)
df.set_index('ID')                  # use a column as index
df.set_index('ID', drop=False)      # keep column AND use as index