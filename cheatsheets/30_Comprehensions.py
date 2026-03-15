# ── LIST COMPREHENSION ───────────────────────────────────────
# [expression for item in iterable]
# [expression for item in iterable if condition]

squares      = [x**2 for x in range(10)]                    # [0,1,4,9,16,25,36,49,64,81]
evens        = [x for x in range(20) if x % 2 == 0]         # [0,2,4,6,8,10,12,14,16,18]
words_upper  = [w.upper() for w in ['hello','world']]        # ['HELLO','WORLD']
no_spaces    = [x.strip() for x in ['  a ',' b','c ']]      # ['a','b','c']
lengths      = [len(w) for w in ['cat','elephant','ox']]     # [3,8,2]
flat         = [x for row in [[1,2],[3,4],[5,6]] for x in row]  # [1,2,3,4,5,6]

# with if/else (ternary) — note: condition goes BEFORE for
labels       = ['High' if x > 70 else 'Low' for x in [80,30,90,20]]  # ['High','Low','High','Low']
abs_vals     = [x if x >= 0 else -x for x in [-3, 1, -5, 2]]         # [3,1,5,2]

# nested — all combinations
pairs        = [(x, y) for x in [1,2,3] for y in ['a','b']]
# [(1,'a'),(1,'b'),(2,'a'),(2,'b'),(3,'a'),(3,'b')]

# with enumerate
indexed      = [(i, v) for i, v in enumerate(['a','b','c'])]  # [(0,'a'),(1,'b'),(2,'c')]

# with zip
summed       = [a + b for a, b in zip([1,2,3],[10,20,30])]   # [11,22,33]

# filter Nones
cleaned      = [x for x in [1, None, 2, None, 3] if x is not None]  # [1,2,3]

# ── DICT COMPREHENSION ───────────────────────────────────────
# {key: value for item in iterable}

squares_d    = {x: x**2 for x in range(6)}              # {0:0,1:1,2:4,3:9,4:16,5:25}
upper_map    = {w: w.upper() for w in ['a','b','c']}     # {'a':'A','b':'B','c':'C'}
word_lengths = {w: len(w) for w in ['cat','dog','bird']} # {'cat':3,'dog':3,'bird':4}
filtered_d   = {k: v for k, v in {'a':1,'b':2,'c':3}.items() if v > 1}  # {'b':2,'c':3}
inverted     = {v: k for k, v in {'a': 1, 'b': 2}.items()}  # {1:'a', 2:'b'}

# from two lists
keys   = ['name', 'age', 'city']
values = ['Anna', 25, 'Warsaw']
record = {k: v for k, v in zip(keys, values)}    # {'name':'Anna','age':25,'city':'Warsaw'}

# ── SET COMPREHENSION ────────────────────────────────────────
unique_lengths = {len(w) for w in ['cat','dog','elephant','ox']}  # {2,3,8}
unique_first   = {w[0] for w in ['apple','avocado','banana']}     # {'a','b'}

# ── NESTED LIST COMPREHENSION ────────────────────────────────
# transpose a matrix
matrix     = [[1,2,3],[4,5,6],[7,8,9]]
transposed = [[row[i] for row in matrix] for i in range(3)]
# [[1,4,7],[2,5,8],[3,6,9]]

# flatten nested list
nested  = [[1,2,3],[4,5],[6,7,8,9]]
flat    = [x for sublist in nested for x in sublist]   # [1,2,3,4,5,6,7,8,9]

# ── WALRUS OPERATOR := (Python 3.8+) ────────────────────────
# assign and use a value in one expression — avoids calling a function twice
data    = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
results = [y for x in data if (y := x**2) > 25]   # [36,49,64,81,100]

# ── ONE-LINER PATTERNS ───────────────────────────────────────
# remove duplicates, preserve order
seen    = set()
unique  = [x for x in [3,1,2,1,3,4] if not (x in seen or seen.add(x))]  # [3,1,2,4]

# chunk a list into groups of n
n       = 3
lst     = list(range(10))
chunks  = [lst[i:i+n] for i in range(0, len(lst), n)]  # [[0,1,2],[3,4,5],[6,7,8],[9]]

# all values from a column in list of dicts
records = [{'name':'Anna','age':25},{'name':'Jan','age':30}]
names   = [r['name'] for r in records]              # ['Anna','Jan']

# flatten dict values
d       = {'a':[1,2],'b':[3,4],'c':[5]}
all_v   = [v for vals in d.values() for v in vals]  # [1,2,3,4,5]
