# ── ENUMERATE ────────────────────────────────────────────────
# adds an index counter to any iterable
cities = ["Warsaw", "Krakow", "Wroclaw"]

for i, city in enumerate(cities):
    print(i, city)              # 0 Warsaw / 1 Krakow / 2 Wroclaw

for i, city in enumerate(cities, start=1):
    print(i, city)              # 1 Warsaw / 2 Krakow / 3 Wroclaw

# useful to avoid manual counter variables
for i, char in enumerate("hello"):
    print(f"[{i}] = {char}")   # [0]=h  [1]=e ...

# ── ZIP ──────────────────────────────────────────────────────
# pairs elements from multiple iterables together
names = ["Anna", "Jan", "Eva"]
ages  = [25, 30, 22]
cities = ["Warsaw", "Krakow", "Gdansk"]

list(zip(names, ages))               # [('Anna',25), ('Jan',30), ('Eva',22)]
list(zip(names, ages, cities))       # can zip 3+ iterables at once

for name, age in zip(names, ages):
    print(f"{name} is {age}")

# zip stops at the shortest iterable
list(zip([1, 2, 3], ["a", "b"]))    # [(1,'a'), (2,'b')] — 3 is dropped

# zip_longest — keeps going, fills missing with a default
from itertools import zip_longest
list(zip_longest([1, 2, 3], ["a", "b"], fillvalue="-"))
# [(1,'a'), (2,'b'), (3,'-')]

# unzipping — transpose a list of tuples back into separate lists
pairs = [("Anna", 25), ("Jan", 30)]
names, ages = zip(*pairs)           # names=('Anna','Jan')  ages=(25,30)

# build a dict from two lists — classic pattern
d = dict(zip(names, ages))          # {"Anna": 25, "Jan": 30}

# ── ANY ──────────────────────────────────────────────────────
# returns True if at least one element is truthy
any([True, False, False])   # True
any([False, False])         # False
any([])                     # False — empty iterable

# works with expressions (short-circuits on first True)
nums = [3, -1, 7, -2]
any(x < 0 for x in nums)   # True  — at least one negative

# ── ALL ──────────────────────────────────────────────────────
# returns True only if every element is truthy
all([True, True, True])     # True
all([True, False])          # False
all([])                     # True — vacuously true (no element to fail)

# works with expressions (short-circuits on first False)
all(x > 0 for x in nums)   # False — not all are positive

# practical example — validate a list of inputs
data = ["Anna", "Jan", ""]
all(name.strip() for name in data)  # False — empty string is falsy

# ── MAP ──────────────────────────────────────────────────────
# applies a function to every element, returns an iterator
list(map(str, [1, 2, 3]))           # ["1", "2", "3"]
list(map(lambda x: x**2, [1,2,3])) # [1, 4, 9]
# usually cleaner as a list comprehension: [x**2 for x in [1,2,3]]

# ── FILTER ───────────────────────────────────────────────────
# keeps only elements where function returns True
list(filter(lambda x: x > 0, [-1, 2, -3, 4]))  # [2, 4]
# list comprehension equivalent: [x for x in nums if x > 0]

# ── SORTED WITH KEY ──────────────────────────────────────────
words = ["banana", "fig", "apple", "kiwi"]
sorted(words, key=len)                  # ["fig","kiwi","apple","banana"]
sorted(words, key=lambda w: w[-1])      # sort by last character

# ── ITERTOOLS EXTRAS ─────────────────────────────────────────
from itertools import chain, product, combinations, permutations

list(chain([1,2], [3,4], [5]))          # [1,2,3,4,5] — flatten iterables
list(combinations([1,2,3], 2))          # [(1,2),(1,3),(2,3)]
list(permutations([1,2,3], 2))          # [(1,2),(1,3),(2,1),...]
list(product([0,1], repeat=3))          # all 3-bit combinations