# generator expression — like list comp but with ()
# does NOT compute all values at once — produces one at a time
gen     = (x**2 for x in range(1_000_000))   # no memory used yet
next(gen)           # 0 — compute first value
next(gen)           # 1 — compute second value

# use in functions that accept iterables — no list needed
total   = sum(x**2 for x in range(1000))     # sum without building list
maximum = max(len(w) for w in ['hi','hello','hey'])
any_big = any(x > 90 for x in [10,50,95])   # short-circuits on first True

# ── GENERATOR FUNCTION — yield ────────────────────────────────
# function that produces values one at a time
# pauses at each yield, resumes on next()

def count_up(start, stop):
    while start <= stop:
        yield start             # pause here, return value, resume next call
        start += 1

gen = count_up(1, 5)
next(gen)       # 1
next(gen)       # 2
list(gen)       # [3, 4, 5] — consume the rest

for n in count_up(1, 5):
    print(n)                    # 1 2 3 4 5

# ── PRACTICAL GENERATOR — read large file line by line ───────
def read_large_file(path):
    with open(path) as f:
        for line in f:
            yield line.strip()  # one line at a time — never loads full file

for line in read_large_file('data.txt'):
    print(line)

# ── GENERATOR WITH SEND ───────────────────────────────────────
def accumulator():
    total = 0
    while True:
        value = yield total     # yield current total, receive next value
        total += value

acc = accumulator()
next(acc)           # prime the generator — runs to first yield → 0
acc.send(10)        # total = 10
acc.send(5)         # total = 15

# ── ITERTOOLS — generator-based tools ────────────────────────
from itertools import (
    chain, islice, takewhile, dropwhile,
    groupby, accumulate, repeat, cycle, count
)

list(chain([1,2],[3,4],[5]))                # [1,2,3,4,5] — flatten iterables
list(islice(range(100), 5))                # [0,1,2,3,4] — take first 5
list(takewhile(lambda x: x < 5, range(10)))  # [0,1,2,3,4] — stop at first False
list(dropwhile(lambda x: x < 5, range(10))) # [5,6,7,8,9] — skip until first True

list(accumulate([1,2,3,4,5]))              # [1,3,6,10,15] — running total

# groupby — group consecutive equal elements (sort first!)
data   = [('Warsaw','BTS'),('Warsaw','Router'),('Krakow','Switch')]
data   = sorted(data, key=lambda x: x[0])
groups = {k: list(v) for k, v in groupby(data, key=lambda x: x[0])}

list(islice(cycle([1,2,3]), 8))            # [1,2,3,1,2,3,1,2] — infinite cycle, take 8
list(islice(count(10, 2), 5))              # [10,12,14,16,18] — infinite counter, take 5