# ── DEFINITION & RETURN ──────────────────────────────────────
def greet(name, greeting="Hi"):  # greeting has a default value
    return f"{greeting}, {name}!"

greet("Anna")           # "Hi, Anna!"    — uses default
greet("Jan", "Hello")   # "Hello, Jan!"  — overrides default

# function without return gives back None implicitly
def say_hi():
    print("hi")

result = say_hi()       # prints "hi"
print(result)           # None

# ── MULTIPLE RETURN VALUES ───────────────────────────────────
# Python returns a tuple — unpack on the receiving end
def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([3, 1, 9, 2])   # lo=1, hi=9

# ── *args — variable positional arguments ────────────────────
# collects any extra positional args into a tuple
def func(name, *args, **kwargs):
    print(args)     # tuple of extra positional args
    print(kwargs)   # dict of named args

func("x", 1, 2, color="red")
# args   → (1, 2)
# kwargs → {"color": "red"}

def add(*numbers):                # accept any number of args
    return sum(numbers)

add(1, 2, 3)        # 6
add(1, 2, 3, 4, 5)  # 15

# ── **kwargs — variable keyword arguments ────────────────────
def display(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

display(name="Anna", age=25, city="Warsaw")

# ── ARGUMENT ORDER RULE ──────────────────────────────────────
# must follow: positional → *args → keyword defaults → **kwargs
def full(a, b, *args, option=True, **kwargs):
    pass

# ── UNPACKING WHEN CALLING ───────────────────────────────────
# use * and ** to unpack a list/dict into function arguments
def add3(a, b, c):
    return a + b + c

nums = [1, 2, 3]
add3(*nums)             # same as add3(1, 2, 3)

settings = {"b": 2, "c": 3}
add3(1, **settings)     # same as add3(1, b=2, c=3)

# ── LAMBDA — anonymous one-liner function ────────────────────
square = lambda x: x ** 2
square(4)               # 16

# lambdas shine as short callbacks
nums = [3, 1, 4, 1, 5]
sorted(nums, key=lambda x: -x)   # [5, 4, 3, 1, 1] — sort descending

# ── SCOPE ────────────────────────────────────────────────────
total = 0

def add_to_total(n):
    global total        # without this, assignment creates a local variable
    total += n

add_to_total(5)
print(total)            # 5

# ── DOCSTRINGS ───────────────────────────────────────────────
def divide(a, b):
    """
    Divides a by b and returns the result.
    Raises ZeroDivisionError if b is 0.
    """
    return a / b

help(divide)            # prints the docstring
divide.__doc__          # access docstring as a stringq
