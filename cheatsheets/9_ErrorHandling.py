# ── BASIC TRY / EXCEPT ───────────────────────────────────────
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Can't divide by zero!")
except Exception as e:
    print(f"Error: {e}")       # e contains the error message

# ── MULTIPLE EXCEPTIONS ──────────────────────────────────────
try:
    x = int(input("Enter number: "))
    print(10 / x)
except ValueError:
    print("That's not a number!")
except ZeroDivisionError:
    print("Can't divide by zero!")

# catch multiple in one line
except (ValueError, TypeError):
    print("Bad input!")

# ── ELSE & FINALLY ───────────────────────────────────────────
try:
    result = 10 / 2
except ZeroDivisionError:
    print("Error!")
else:
    print(f"Success: {result}")  # runs only if NO exception occurred
finally:
    print("Always runs")         # runs no matter what — good for cleanup

# ── RAISING EXCEPTIONS ───────────────────────────────────────
def divide(a, b):
    if b == 0:
        raise ValueError("b cannot be zero")  # raise manually
    return a / b

# re-raise after catching (keeps original traceback)
try:
    divide(1, 0)
except ValueError as e:
    print(f"Caught: {e}")
    raise                        # re-raises the same exception

# ── COMMON BUILT-IN EXCEPTIONS ───────────────────────────────
# ValueError      — right type, wrong value:  int("hello")
# TypeError       — wrong type entirely:      "2" + 2
# KeyError        — dict key not found:       d["missing"]
# IndexError      — list index out of range:  [1,2,3][9]
# AttributeError  — object has no attribute:  "hi".explode()
# FileNotFoundError — file doesn't exist:     open("nope.txt")
# ZeroDivisionError — division by zero:       10 / 0
# NameError       — variable not defined:     print(undefined_var)
# RecursionError  — too many nested calls:    infinite recursion
# StopIteration   — iterator is exhausted:    next() on empty iterator

# ── CUSTOM EXCEPTIONS ────────────────────────────────────────
class NegativeValueError(ValueError):
    pass

def sqrt(n):
    if n < 0:
        raise NegativeValueError(f"Cannot take sqrt of {n}")
    return n ** 0.5

try:
    sqrt(-4)
except NegativeValueError as e:
    print(e)                     # "Cannot take sqrt of -4"

# ── EXCEPTION HIERARCHY ──────────────────────────────────────
# BaseException
#   └── Exception              ← catch-all for normal errors
#         ├── ValueError
#         ├── TypeError
#         ├── KeyError
#         ├── IndexError
#         └── ...              ← always catch specific before general

# catching bare Exception is OK — catching BaseException is not
# (BaseException includes KeyboardInterrupt and SystemExit)

# ── CONTEXT MANAGER AS SAFE GUARD ────────────────────────────
# with open() handles exceptions and always closes the file
with open("file.txt", "w") as f:
    f.write("hello")            # no need for try/finally around file ops

# ── PRACTICAL PATTERNS ───────────────────────────────────────

# safe dict access
try:
    val = d["key"]
except KeyError:
    val = None
# cleaner: val = d.get("key")

# safe type conversion
def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

safe_int("42")      # 42
safe_int("hello")   # 0
safe_int(None)      # 0

# assert — lightweight check during development
def process(data):
    assert isinstance(data, list), "data must be a list"
    assert len(data) > 0, "data cannot be empty"
    # ... rest of function
# AssertionError is raised if condition is False
# Note: asserts can be disabled with python -O, don't use for real validation