# ── MATH ─────────────────────────────────────────────────────
sum([1, 2, 3, 4])           # 10    — sum of iterable
sum([1, 2, 3], 10)          # 16    — with starting value
len([1, 2, 3, 4])           # 4     — number of elements
round(3.14159, 2)           # 3.14  — round to N decimal places
round(3.5)                  # 4     — rounds to nearest even (banker's rounding!)
round(2.5)                  # 2     — not 3! use math.ceil if you need "normal" rounding
abs(-7)                     # 7     — absolute value
pow(2, 10)                  # 1024  — same as 2**10
pow(2, 10, 1000)            # 24    — modular exponentiation: (2**10) % 1000
divmod(17, 5)               # (3, 2) — quotient and remainder at once
min(3, 1, 4, 1, 5)          # 1     — smallest of args
max(3, 1, 4, 1, 5)          # 5     — largest of args
min([3, 1, 4], key=abs)     # 1     — with custom key function

import math
math.floor(3.9)             # 3     — round down always
math.ceil(3.1)              # 4     — round up always
math.sqrt(16)               # 4.0
math.pi                     # 3.141592653589793
math.inf                    # infinity (useful for default min/max)

# ── SEQUENCES ────────────────────────────────────────────────
range(5)                    # 0 1 2 3 4
range(1, 6)                 # 1 2 3 4 5
range(0, 10, 2)             # 0 2 4 6 8
list(reversed([1, 2, 3]))   # [3, 2, 1] — reversed iterator
list(enumerate(["a","b"]))  # [(0,'a'), (1,'b')]
sorted([3, 1, 2])           # [1, 2, 3] — new list
list(zip([1,2], ["a","b"])) # [(1,'a'), (2,'b')]

# ── TYPE CONSTRUCTORS ────────────────────────────────────────
int("10")                   # string → int
float("3.14")               # string → float
str(42)                     # anything → string
bool(0)                     # 0 / None / "" / [] → False
list("abc")                 # ['a','b','c']
tuple([1, 2, 3])            # (1, 2, 3)
set([1, 2, 2, 3])           # {1, 2, 3}
dict(a=1, b=2)              # {"a": 1, "b": 2}

# ── INPUT / OUTPUT ───────────────────────────────────────────
print("a", "b", "c")               # a b c         — space-separated
print("a", "b", sep="-")           # a-b            — custom separator
print("done", end="!\n")           # done!          — custom line ending
print("x =", 10, "y =", 20)        # x = 10 y = 20

input("Enter value: ")              # always returns string

# ── OBJECTS & INSPECTION ─────────────────────────────────────
x=10
type(42)                    # <class 'int'>
isinstance(42, int)         # True
isinstance(42, (int,float)) # True — check multiple types
id(x)                       # memory address of object
hash("hello")               # hash value (used in dicts/sets)
dir(x)                      # list all attributes and methods of x
dir()                       # list all names in current scope
vars(x)                     # __dict__ of x — instance attributes
callable(print)             # True  — can it be called as a function?
hasattr(x, "append")        # True if x has attribute "append"
getattr(x, "append")        # same as x.append — useful dynamically
setattr(x, "name", "Anna")  # same as x.name = "Anna"

# ── HELP & DOCS ──────────────────────────────────────────────
help(sum)                   # full docstring in terminal
help(str.split)             # works on methods too
help()                      # opens interactive help
sum.__doc__                 # docstring as raw string

# ── FUNCTIONAL ───────────────────────────────────────────────
list(map(str, [1, 2, 3]))           # ["1","2","3"] — apply fn to each
list(filter(None, [0,1,2,None]))    # [1, 2] — keep truthy values
from functools import reduce
reduce(lambda a,b: a+b, [1,2,3,4]) # 10  — fold left

# ── MISC ─────────────────────────────────────────────────────
open("file.txt")            # open a file — see file_handling.py
format(3.14159, ".2f")      # "3.14" — format a value
chr(65)                     # "A"   — int → character
ord("A")                    # 65    — character → int
bin(10)                     # "0b1010" — int → binary string
hex(255)                    # "0xff"   — int → hex string
oct(8)                      # "0o10"   — int → octal string
bytes([72, 101, 108])       # b'Hel'  — list of ints → bytes