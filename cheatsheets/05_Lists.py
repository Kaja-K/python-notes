lst = [1, 2, 3, 4, 5]

# ── INDEXING ─────────────────────────────────────────────────
lst[0]          # 1    — first element
lst[-1]         # 5    — last element (counts from end)
lst[-2]         # 4    — second to last

# ── SLICING ──────────────────────────────────────────────────
lst[1:4]        # [2, 3, 4]  — index 1 up to (not including) 4
lst[:2]         # [1, 2]     — from start up to index 2
lst[2:]         # [3, 4, 5]  — from index 2 to end
lst[-2:]        # [4, 5]     — last two elements
lst[::2]        # [1, 3, 5]  — every second element (step)
lst[::-1]       # [5, 4, 3, 2, 1] — reversed copy

# ── ADDING ELEMENTS ──────────────────────────────────────────
lst.append(6)           # adds single element to end → [1,2,3,4,5,6]
lst.extend([7, 8])      # adds multiple elements to end → [...,7,8]
lst.insert(0, 99)       # inserts 99 at index 0, shifts rest right
lst.insert(2, 99)       # inserts 99 at index 2

# ── REMOVING ELEMENTS ────────────────────────────────────────
lst.remove(3)           # removes first occurrence of value 3
lst.pop()               # removes & returns last element
lst.pop(0)              # removes & returns element at index 0
lst.clear()             # removes everything → []
del lst[1]              # removes element at index 1 (no return value)
del lst[1:3]            # removes a slice

# ── SEARCHING ────────────────────────────────────────────────
lst.index(3)            # index of first occurrence of 3 (raises ValueError if missing)
lst.index(3, 2)         # search starting from index 2
lst.count(2)            # how many times 2 appears
3 in lst                # True — simplest membership check
all(lst)                # True if every element is truthy (empty list → True)

# ── SORTING ──────────────────────────────────────────────────
lst.sort()                          # sorts in place, modifies original
lst.sort(reverse=True)              # sorts in place, descending
sorted(lst)                         # returns new sorted list, original unchanged
sorted(lst, reverse=True)           # new list, descending
sorted(lst, key=lambda x: -x)       # custom sort key

# sort by length (works on any type with a key)
words = ["banana", "fig", "apple"]
sorted(words, key=len)              # ["fig", "apple", "banana"]

# ── REVERSING ────────────────────────────────────────────────
lst.reverse()           # reverses in place, modifies original
lst[::-1]               # returns reversed copy, original unchanged

# ── COPY ─────────────────────────────────────────────────────
b = lst.copy()          # shallow copy — safe to modify independently
b = lst[:]              # same as .copy() using slice
b = list(lst)           # same again using constructor

# why copy matters:
a = [1, 2, 3]
b = a               # b points to SAME list — changing b changes a too!
b = a.copy()        # b is independent — changing b leaves a alone

# ── BUILDING LISTS ───────────────────────────────────────────
list("Hey")             # ['H', 'e', 'j'] — string to list of chars
list(range(5))          # [0, 1, 2, 3, 4]
[0] * 5                 # [0, 0, 0, 0, 0] — repeat an element

# list comprehension — compact way to build a list
squares = [x**2 for x in range(6)]         # [0, 1, 4, 9, 16, 25]
evens   = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]

# ── AGGREGATES ───────────────────────────────────────────────
sum(lst)            # sum of all elements
len(lst)            # number of elements
min(lst)            # smallest value
max(lst)            # largest value

# ── UNPACKING ────────────────────────────────────────────────
a, b, c = [1, 2, 3]        # assign each element to a variable
first, *rest = [1, 2, 3, 4] # first=1, rest=[2,3,4]
*init, last = [1, 2, 3, 4]  # init=[1,2,3], last=4

# ── DUNDER METHODS ───────────────────────────────────────────
lst.__len__()           # same as len(lst)
lst.__getitem__(0)      # same as lst[0]
lst.__contains__(3)     # same as 3 in lst
lst.__add__([6, 7])     # same as lst + [6, 7]  — returns new list
lst.__iadd__([6, 7])    # same as lst += [6, 7] — extends in place