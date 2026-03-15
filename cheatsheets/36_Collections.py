from collections import Counter, defaultdict, deque, namedtuple, OrderedDict, ChainMap
import numpy as np

# ── COUNTER — count occurrences ──────────────────────────────
# like a dict but auto-initialises missing keys to 0

words  = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']
c      = Counter(words)
# Counter({'apple': 3, 'banana': 2, 'cherry': 1})

c['apple']              # 3
c['missing']            # 0  — no KeyError!
c.most_common(2)        # [('apple',3), ('banana',2)] — top n
c.most_common()[:-3:-1] # least common (last 2)

# arithmetic
c1 = Counter({'a': 3, 'b': 2})
c2 = Counter({'a': 1, 'b': 4})
c1 + c2     # Counter({'b':6, 'a':4})
c1 - c2     # Counter({'a':2})   — removes zeros and negatives
c1 & c2     # Counter({'a':1, 'b':2}) — min of each
c1 | c2     # Counter({'b':4, 'a':3}) — max of each

# count characters in a string
Counter('abracadabra')  # Counter({'a':5,'b':2,'r':2,'c':1,'d':1})

# count values in a DataFrame column
import pandas as pd
np.random.seed(42)
df = pd.DataFrame({
    'city':   np.random.choice(['Warsaw','Krakow','Wroclaw'], 20),
    'status': np.random.choice(['Active','Inactive'], 20),
})
Counter(df['city'])             # count rows per city
Counter(df['city']).most_common(3)

# ── DEFAULTDICT — dict with auto-default ─────────────────────
# never raises KeyError — creates missing key with a default value

# group items by key without checking if key exists
dd = defaultdict(list)          # default value is an empty list
for city, station in [('Warsaw','ST_01'),('Krakow','ST_02'),('Warsaw','ST_03')]:
    dd[city].append(station)    # no need to check if key exists first
# defaultdict(list, {'Warsaw':['ST_01','ST_03'], 'Krakow':['ST_02']})

dd = defaultdict(int)           # default value is 0
for word in ['a','b','a','c','b','a']:
    dd[word] += 1               # same as Counter but manual
# defaultdict(int, {'a':3,'b':2,'c':1})

dd = defaultdict(set)
for city, tag in [('Warsaw','bts'),('Warsaw','router'),('Krakow','bts')]:
    dd[city].add(tag)

# nested defaultdict
nested = defaultdict(lambda: defaultdict(int))
nested['Warsaw']['BTS'] += 1
nested['Warsaw']['Router'] += 2

# convert back to regular dict
dict(dd)

# ── DEQUE — double-ended queue ───────────────────────────────
# like a list but O(1) append/pop from BOTH ends
# lists are O(n) for insert/pop at position 0

d = deque([1, 2, 3])

d.append(4)         # add to right  → deque([1,2,3,4])
d.appendleft(0)     # add to left   → deque([0,1,2,3,4])
d.pop()             # remove right  → 4, deque([0,1,2,3])
d.popleft()         # remove left   → 0, deque([1,2,3])

d.extend([4, 5])    # add multiple to right
d.extendleft([0])   # add multiple to left (each is prepended)
d.rotate(1)         # shift right by 1
d.rotate(-1)        # shift left by 1

# maxlen — fixed-size sliding window
recent = deque(maxlen=3)
for x in range(6):
    recent.append(x)
    print(list(recent))
# [0] [0,1] [0,1,2] [1,2,3] [2,3,4] [3,4,5]
# oldest item auto-dropped when maxlen exceeded

# useful for: last N logs, moving average, BFS queue
from collections import deque as Queue
queue = Queue(['a','b','c'])
queue.appendleft('d')   # enqueue front
queue.pop()             # dequeue back → 'c'

# ── NAMEDTUPLE — tuple with field names ──────────────────────
# immutable like tuple, but fields accessed by name — no class needed

Station = namedtuple('Station', ['station_id', 'city', 'load'])
s = Station('ST_001', 'Warsaw', 75.5)

s.station_id    # 'ST_001' — access by name
s.city          # 'Warsaw'
s[0]            # 'ST_001' — access by index still works
s._asdict()     # OrderedDict([('station_id','ST_001'), ...])
s._replace(load=80)  # new instance with one field changed

# unpack like a tuple
sid, city, load = s

# use in list of records (lightweight alternative to DataFrame for small data)
stations = [
    Station('ST_001', 'Warsaw', 75.5),
    Station('ST_002', 'Krakow', 42.0),
    Station('ST_003', 'Wroclaw', 91.3),
]
max(stations, key=lambda s: s.load)      # Station with highest load
sorted(stations, key=lambda s: s.city)  # sort by city

# typed version (Python 3.6+) — with defaults and type hints
from typing import NamedTuple

class Station(NamedTuple):
    station_id: str
    city:       str
    load:       float = 0.0     # default value supported

s = Station('ST_001', 'Warsaw')     # load defaults to 0.0

# ── ORDEREDDICT ──────────────────────────────────────────────
# regular dict preserves insertion order since Python 3.7
# OrderedDict has extra methods for order-based operations

od = OrderedDict([('a',1), ('b',2), ('c',3)])
od.move_to_end('a')         # move 'a' to end
od.move_to_end('c', last=False)  # move 'c' to front
od.popitem(last=True)       # remove and return last item
od.popitem(last=False)      # remove and return first item

# ── CHAINMAP — overlay multiple dicts ────────────────────────
# lookups search through maps in order — first match wins
defaults = {'color': 'blue', 'size': 'M', 'debug': False}
config   = {'color': 'red'}
user     = {'size': 'L'}

combined = ChainMap(user, config, defaults)
combined['color']   # 'red'   — from config
combined['size']    # 'L'     — from user
combined['debug']   # False   — from defaults

# good for: config layering, scope chains, CLI overrides