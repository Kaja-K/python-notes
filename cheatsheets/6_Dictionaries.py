# ── CREATING ─────────────────────────────────────────────────
d = {"key": "value", "id": 101}    # standard dict
d = dict(key="value", id=101)      # using constructor
d = dict([("key", "value")])       # from list of tuples
d = {}                             # empty dict

# ── ACCESSING ────────────────────────────────────────────────
d["key"]                # "value"  — raises KeyError if missing
d.get("key")            # "value"  — returns None if missing (safe)
d.get("missing", 0)     # 0        — custom default if key not found

# ── VIEWS ────────────────────────────────────────────────────
d.keys()                # all keys   → dict_keys(["key", "id"])
d.values()              # all values → dict_values(["value", 101])
d.items()               # all pairs  → dict_items([("key","value"), ...])

# ── ADDING & UPDATING ────────────────────────────────────────
d["new"] = 99           # add or overwrite a key
d.update({"a": 1, "b": 2})   # merge another dict in (modifies in place)
d.update(a=1, b=2)           # same with keyword args

# ── REMOVING ─────────────────────────────────────────────────
d.pop("key")            # removes key and returns its value
d.pop("key", None)      # safe version — no error if key missing
d.popitem()             # removes and returns last inserted (key, value) pair
del d["key"]            # removes key, no return value
d.clear()               # removes everything → {}

# ── CHECKING MEMBERSHIP ──────────────────────────────────────
"key" in d              # True  — checks keys only
"value" in d.values()   # True  — check values (slower, scans all)

# ── DEFAULTS ─────────────────────────────────────────────────
d.setdefault("key", 0)  # returns value if key exists, otherwise sets it to 0

# ── LOOPING ──────────────────────────────────────────────────
for key in d:                       # iterate over keys
    print(key)

for key, value in d.items():        # iterate over key-value pairs
    print(f"{key}: {value}")

# ── MERGING ──────────────────────────────────────────────────
d1 = {"a": 1}
d2 = {"b": 2}
merged = {**d1, **d2}               # {"a": 1, "b": 2}  — new dict
merged = d1 | d2                    # same, Python 3.9+ syntax
d1 |= d2                            # merge d2 into d1 in place (3.9+)

# last one wins on duplicate keys:
{**{"a": 1}, **{"a": 99}}           # {"a": 99}

# ── DICT COMPREHENSION ───────────────────────────────────────
squares = {x: x**2 for x in range(5)}       # {0:0, 1:1, 2:4, 3:9, 4:16}
filtered = {k: v for k, v in d.items() if v > 0}  # keep positive values only

# ── DUNDER METHODS ───────────────────────────────────────────
d.__getitem__("key")    # same as d["key"]
d.__setitem__("k", 1)   # same as d["k"] = 1
d.__delitem__("key")    # same as del d["key"]
d.__contains__("key")   # same as "key" in d
d.__len__()             # same as len(d)