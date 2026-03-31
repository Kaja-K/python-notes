s = "Hello World"
x, y = 10, 20
 
# ── FORMATTING ───────────────────────────────────────────────
print(f"Result: {x}")                    # f-string — modern, recommended
print(f"Pi is approx {3.14159:.2f}")     # f-string with format spec (2 decimal places)
print(f"{x + y = }")                     # debug shortcut — prints "x + y = 30"
print("Result: {} and {}".format(x, y)) # .format() — older but still common
print("Result: %s %s" % (x, y))         # %-style — legacy, avoid in new code
 
# ── CASE ─────────────────────────────────────────────────────
s.upper()           # "HELLO WORLD"    — all uppercase
s.lower()           # "hello world"    — all lowercase
s.title()           # "Hello World"    — first letter of each word capitalised
s.capitalize()      # "Hello world"    — only very first letter capitalised
s.swapcase()        # "hELLO wORLD"    — flips upper ↔ lower
 
# ── SEARCH & CHECK ───────────────────────────────────────────
s.find("World")         # 6   — index of first match; -1 if not found
s.index("World")        # 6   — same as find() but raises ValueError if missing
s.rfind("l")            # 9   — index of LAST match
s.count("l")            # 3   — number of non-overlapping occurrences
s.startswith("Hello")   # True
s.endswith("World")     # True
"World" in s            # True — simplest membership check
 
# ── VALIDATE (is* methods) ────────────────────────────────────
"123".isnumeric()   # True  — all chars are numeric (includes ², ½ etc.)
"123".isdigit()     # True  — all chars are digits (0-9 and some unicode)
"123".isdecimal()   # True  — strictest: only 0-9  ← use this for user input
"abc".isalpha()     # True  — all chars are letters
"abc123".isalnum()  # True  — letters or digits, no spaces/symbols
"  ".isspace()      # True  — only whitespace
"Hello W ".istitle()# True  — each word starts with uppercase
"hello".islower()   # True
"HELLO".isupper()   # True
"hello".isascii()   # True  — all chars are ASCII (no accents, emoji etc.)
 
# ── STRIP / TRIM ─────────────────────────────────────────────
"  hello  ".strip()     # "hello"   — removes whitespace from both sides
"  hello  ".lstrip()    # "hello  " — removes from left only
"  hello  ".rstrip()    # "  hello" — removes from right only
"...hello...".strip(".")# "hello"  — strips specific characters too
 
# ── REPLACE & SPLIT ──────────────────────────────────────────
s.replace(" ", ";")          # "Hello;World" — replace all occurrences
s.replace("l", "L", 1)       # "HeLlo World" — third arg limits replacements

s.partition(" ")             # ("Hello", " ", "World") — splits on FIRST match, always returns 3-tuple
s.rpartition(" ")            # ("Hello", " ", "World") — splits on LAST match
"hello".partition("x")       # ("hello", "", "")       — separator not found: original in [0], rest empty

cities = "WRO\nWAW\nKRK"
cities.split("\n")           # ["WRO", "WAW", "KRK"] — split on newline
"a,b,,c".split(",")          # ["a", "b", "", "c"]   — split on comma
"a,b,,c".split(",", 2)       # ["a", "b", ",c"]      — limit number of splits
" - ".join(["WRO", "WAW"])   # "WRO - WAW"           — join list into string
 
# ── PADDING & ALIGNMENT ──────────────────────────────────────
"hi".center(10)         # "    hi    "  — centered in 10 chars
"hi".ljust(10)          # "hi        "  — left-aligned, padded with spaces
"hi".ljust(10, "-")     # "hi--------"  — custom fill character
"hi".rjust(10)          # "        hi"  — right-aligned
"42".zfill(5)           # "00042"        — zero-pad (useful for numbers)
 
# ── SLICING ──────────────────────────────────────────────────
s[0]        # "H"         — first character
s[-1]       # "d"         — last character
s[0:5]      # "Hello"     — characters from index 0 to 4
s[6:]       # "World"     — from index 6 to end
s[:5]       # "Hello"     — from start to index 4
s[::-1]     # "dlroW olleH" — reverse the string
 
# ── MISC ─────────────────────────────────────────────────────
len(s)          # 11        — number of characters
s.encode()      # b'Hello World' — convert to bytes (useful for files/network)
ord("A")        # 65        — unicode code point of a character
chr(65)         # "A"       — character from code point

# ── DUNDER METHODS ───────────────────────────────────────────
# called implicitly by Python operators — rarely used directly
s.__contains__("Hello")  # True  — same as "Hello" in s
s.__len__()              # 11    — same as len(s)
s.__add__(" !")          # "Hello World !" — same as s + " !"
s.__mul__(3)             # "Hello WorldHello WorldHello World" — same as s * 3
s.__getitem__(0)         # "H"   — same as s[0]
s.__iter__()             # iterator over characters — used in for loops
s.__repr__()             # "'Hello World'" — unambiguous representation
s.__eq__("Hello World")  # True  — same as s == "Hello World"
s.__ne__("Hello")        # True  — same as s != "Hello"
s.__hash__()             # hash value of the string (used in sets/dicts)