
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
int("1A", 16)                   # Hex str → int (dec 26)

# ── NUMBER SYSTEMS: TO INT ────────────────────────────────────
int("0b1010", 2)                # binary str → int  (10)
int("1010",   2)                # binary str no prefix → int  (10)
int("0o17",   8)                # octal str → int  (15)
int("17",     8)                # octal str no prefix → int  (15)
int("0xFF",  16)                # hex str → int  (255)
int("FF",    16)                # hex str no prefix → int  (255)
int("z",     36)                # base-36 → int  (35) — max base is 36

# ── INT → OTHER SYSTEMS ───────────────────────────────────────
bin(10)                         # int → binary str    "0b1010"
oct(8)                          # int → octal str     "0o10"
hex(255)                        # int → hex str       "0xff"

bin(10)[2:]                     # strip "0b" prefix   →  "1010"
oct(8)[2:]                      # strip "0o" prefix   →  "10"
hex(255)[2:]                    # strip "0x" prefix   →  "ff"
hex(255)[2:].upper()            # →  "FF"

format(255, "b")                # int → binary no prefix      "11111111"
format(255, "o")                # int → octal no prefix       "377"
format(255, "x")                # int → hex lowercase         "ff"
format(255, "X")                # int → hex uppercase         "FF"
format(255, "08b")              # zero-padded to 8 digits     "11111111"
format(10,  "08b")              # →  "00001010"

f"{255:b}"                      # f-string binary             "11111111"
f"{255:o}"                      # f-string octal              "377"
f"{255:x}"                      # f-string hex                "ff"
f"{255:#x}"                     # f-string hex with prefix    "0xff"
f"{255:#010b}"                  # with prefix + zero-padding  "0b11111111"

# ── QUICK CROSS-BASE CONVERSIONS ─────────────────────────────
# binary → hex  (int as a bridge)
hex(int("1010", 2))             # "0xa"
# hex → binary
bin(int("FF", 16))              # "0b11111111"
# octal → binary
bin(int("17", 8))               # "0b1111"

# ── BIT / BYTE LISTS ─────────────────────────────────────────
list(bin(42)[2:])               # ['1','0','1','0','1','0']  — list of bit chars
[int(b) for b in bin(42)[2:]]   # [1, 0, 1, 0, 1, 0]        — list of ints
(255).to_bytes(2, "big")        # int → bytes  b'\x00\xff'
int.from_bytes(b'\x00\xff', "big")  # bytes → int  (255)
 
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