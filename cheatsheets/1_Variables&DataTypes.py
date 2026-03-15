
print("Hello World")
 
# ── DATA TYPES ───────────────────────────────────────────────
x = 10                          # int
y = 3.14                        # float
text = "hello"                  # string
is_active = True                # bool
nothing = None                  # absence of value
 
# ── TYPE CONVERSION ──────────────────────────────────────────
int("10")                       # str → int
int(3.9)                        # float → int (truncates, does NOT round!)
int(float("3.14"))              # str → float → int (safe way to convert "3.14")
float("10")                     # str → float
str(5.75)                       # float → str
bool(0)                         # 0, "", [], None → False; everything else → True
 
# ── TYPE CHECKING ────────────────────────────────────────────
type(x)                         # returns the type of x → <class 'int'>
id(x)                           # returns memory address of x → e.g. 140234567
isinstance(x, int)              # checks if x is an int → True
isinstance(x, (int, float))     # checks against multiple types at once → True
 
# ── FALSY VALUES ─────────────────────────────────────────────
# all of these evaluate to False in an if-statement
bool(0)         # False — zero
bool("")        # False — empty string
bool([])        # False — empty list
bool({})        # False — empty dict
bool(None)      # False — no value
 
# ── USER INPUT ───────────────────────────────────────────────
name = input("Enter name: ")        # input() pauses the program and waits; always returns a string
age  = int(input("Enter age: "))    # convert immediately after reading

try:                                # safe version — handles invalid input
    score = float(input("Enter score: "))
except ValueError:
    score = 0.0                     # fallback if user types non-number
 
# ── INSPECTION & HELP ────────────────────────────────────────
dir(x)                          # lists all methods/attributes of x
dir()                           # lists all names in current scope
help(str)                       # shows full docs for a type or function
help(isinstance)                # works on any built-in