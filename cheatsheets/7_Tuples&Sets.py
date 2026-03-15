# ════════════════════════════════════════════
#  TUPLES
# ════════════════════════════════════════════

# ── CREATING ─────────────────────────────────────────────────
t = (1, 2, 3)           # standard tuple
t = 1, 2, 3             # parentheses optional — same result
t = (42,)               # single-element — the comma is required!
t = ()                  # empty tuple
t = tuple([1, 2, 3])    # convert list → tuple

# ── ACCESSING ────────────────────────────────────────────────
t[0]                    # 1       — same indexing as lists
t[-1]                   # 3       — last element
t[1:3]                  # (2, 3)  — slicing works too

# ── IMMUTABLE — cannot change after creation ─────────────────
# t[0] = 99             # TypeError  — assignment not allowed
# t.append(4)           # AttributeError — no append on tuples

# ── METHODS (only two) ───────────────────────────────────────
t.count(2)              # number of occurrences of 2
t.index(2)              # index of first occurrence of 2

# ── UNPACKING ────────────────────────────────────────────────
a, b, c = (1, 2, 3)         # assign each element to a variable
a, *rest = (1, 2, 3, 4)     # a=1, rest=[2, 3, 4]
x, y = y, x                 # swap variables — uses tuple under the hood

# ── WHY USE TUPLES OVER LISTS ────────────────────────────────
# - slightly faster and less memory (fixed size)
# - can be used as dict keys (lists cannot — mutable = not hashable)
# - signals intent: "this data should not change"
location = {(52.2, 21.0): "Warsaw"}  # tuple as dict key — works!
# {[52.2, 21.0]: "Warsaw"}           # TypeError — list as key — fails

# ── NAMED TUPLE — tuple with field names ─────────────────────
from collections import namedtuple
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
p.x             # 3   — access by name
p[0]            # 3   — access by index still works


# ════════════════════════════════════════════
#  SETS
# ════════════════════════════════════════════

# ── CREATING ─────────────────────────────────────────────────
s = {1, 2, 3}               # standard set — no duplicates, unordered
s = set([1, 2, 2, 3])       # convert list → set → {1, 2, 3}
s = set("hello")            # convert string → {'h','e','l','o'} (unique chars)
s = set()                   # empty set — NOT {} (that's an empty dict!)

# ── ADDING & REMOVING ────────────────────────────────────────
s.add(4)                    # adds single element
s.update([4, 5, 6])         # adds multiple elements
s.remove(3)                 # removes 3 — raises KeyError if missing
s.discard(3)                # removes 3 — no error if missing (safe)
s.pop()                     # removes and returns a random element
s.clear()                   # empties the set

# ── MEMBERSHIP ───────────────────────────────────────────────
3 in s                      # True  — O(1), much faster than list search

# ── SET OPERATIONS ───────────────────────────────────────────
a = {1, 2, 3}
b = {2, 3, 4}

a | b                       # {1,2,3,4}  — union (all elements)
a & b                       # {2,3}      — intersection (shared elements)
a - b                       # {1}        — difference (in a but not b)
a ^ b                       # {1,4}      — symmetric difference (not in both)

a.issubset(b)               # True if all of a is in b
a.issuperset(b)             # True if a contains all of b
a.isdisjoint(b)             # True if no elements in common

# ── COMMON USE CASE — remove duplicates from a list ──────────
names = ["Anna", "Jan", "Anna", "Eva"]
unique = list(set(names))   # ["Jan", "Anna", "Eva"] — order not guaranteed

# ── DUNDER METHODS ───────────────────────────────────────────
s.__contains__(3)           # same as 3 in s
s.__len__()                 # same as len(s)
s.__or__(b)                 # same as s | b  (union)
s.__and__(b)                # same as s & b  (intersection)
s.__sub__(b)                # same as s - b  (difference)