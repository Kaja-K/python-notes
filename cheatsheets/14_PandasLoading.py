import pandas as pd

# ── READING FILES ────────────────────────────────────────────
df = pd.read_csv('data.csv')                          # basic CSV
df = pd.read_csv('data.csv', sep=';')                 # semicolon-separated
df = pd.read_csv('data.csv', encoding='utf-8')        # specify encoding
df = pd.read_csv('data.csv', index_col='ID')          # set column as index
df = pd.read_csv('data.csv', usecols=['A', 'B'])      # load specific columns only
df = pd.read_csv('data.csv', nrows=1000)              # load only first 1000 rows
df = pd.read_csv('data.csv', skiprows=2)              # skip first 2 rows
df = pd.read_csv('data.csv', na_values=['N/A', '-'])  # treat these as NaN

df = pd.read_table('data.txt', sep='\t')              # delimited text file
df = pd.read_excel('data.xlsx', sheet_name='Sheet1') # Excel workbook
df = pd.read_json('data.json')                        # JSON file or string
df = pd.read_html('https://example.com')[0]           # first table from HTML page
df = pd.read_parquet('data.parquet')                  # fast columnar format
df = pd.read_sql('SELECT * FROM table', connection)   # SQL query result

# ── CREATE FROM DICT ─────────────────────────────────────────
# keys become column names, values become lists of rows
data = {
    'ID':   [1, 2, 2, 3, 4, 5],
    'City': ['Wroclaw', 'Warsaw', 'Warsaw', 'Krakow', 'Wroclaw', None],
    'Load': [85, 40, 40, 95, 20, 50],
    'Date': ['2026-03-01', '2026-03-01', '2026-03-01',
             '2026-03-02', '2026-03-02', '2026-03-02']
}
df = pd.DataFrame(data)

# ── INSPECT ──────────────────────────────────────────────────
df.head()               # first 5 rows
df.head(3)              # first 3 rows
df.tail(3)              # last 3 rows
df.sample(n=2)          # 2 random rows — good sanity check
df.sample(frac=0.1)     # random 10% of rows

df.shape                # (rows, columns) as tuple
df.columns              # all column names
df.index                # row labels (range by default)
df.dtypes               # data type of each column
df.info()               # types + non-null counts + memory usage
df.describe()           # count/mean/std/min/max for numeric columns
df.describe(include='all')   # include non-numeric columns too
df.memory_usage()       # memory per column in bytes
df.nunique()            # count of unique values per column
df['City'].value_counts()    # frequency of each value in a column

# ── EXPORT ───────────────────────────────────────────────────
df.to_csv('output.csv', index=False)                   # index=False skips row numbers
df.to_excel('output.xlsx', index=False, sheet_name='Report')
df.to_json('output.json', orient='records')            # each row as a JSON object
df.to_parquet('output.parquet')
df.to_sql('table_name', connection, if_exists='replace', index=False)