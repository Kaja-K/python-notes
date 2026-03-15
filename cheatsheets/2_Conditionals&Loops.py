# ── IF / ELIF / ELSE ─────────────────────────────────────────
# runs the first block whose condition is True
a = 10

if a > 0:
    print("positive")
elif a == 0:               # checked only if the above was False
    print("zero")
else:                      # fallback if nothing matched
    print("negative")

# one-liner (ternary) — for simple cases
label = "positive" if a > 0 else "non-positive"

# chaining comparisons — more readable than a and b
x = 5
print(1 < x < 10)         # True — Python allows this, most languages don't

# ── FOR LOOP ─────────────────────────────────────────────────
# iterates over any sequence (list, string, range, ...)
for i in range(5):         # 0 → 4
    print(i)

for i in range(1, 6):      # 1 → 5  (start, stop — stop is excluded)
    print(i)

for i in range(0, 10, 2):  # 0 2 4 6 8  (start, stop, step)
    print(i)

for i in range(5, 0, -1):  # 5 4 3 2 1  (counting down)
    print(i)

# looping over a list directly — no need for range
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# break — exits the loop early
for i in range(10):
    if i == 3:
        break              # stops at 3, never reaches 4+

# continue — skips the rest of this iteration, moves to next
for i in range(5):
    if i == 2:
        continue           # skips 2, keeps going
    print(i)               # prints 0 1 3 4

# ── WHILE LOOP ───────────────────────────────────────────────
# keeps running as long as the condition stays True
count = 0
while count < 3:
    print("looping...")
    count += 1             # without this → infinite loop!

# useful when you don't know in advance how many iterations you need
user_input = ""
while user_input != "quit":
    user_input = input("Type something (or 'quit' to stop): ")

# while True — runs forever until an explicit break
while True:
    answer = input("Guess the number: ")
    if answer == "7":
        print("Correct!")
        break              # exits the loop