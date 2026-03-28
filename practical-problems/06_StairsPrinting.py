# ============================================================
# STAR PATTERN PRINTING ALGORITHMS
# Each pattern uses nested logic to control spacing and stars
# ============================================================

# Right-Angled Triangle
# Prints increasing number of stars from 1 to n
n = 5
for i in range(1, n+1):
    print("*" * i)

# Inverted Right-Angled Triangle
# Prints decreasing number of stars from n down to 1
n = 5
for i in range(n, 0, -1):
    print("*" * i)

# Pyramid Pattern
# Centers stars by adding spaces before each row
# Each row has (2*i - 1) stars and (n - i) leading spaces
n = 5
for i in range(1, n+1):
    print(" " * (n-i) + "*" * (2*i-1))

# Inverted Pyramid
# Same as pyramid but printed from bottom to top
# Starts with widest row and narrows down to a single star
n = 5
for i in range(n, 0, -1):
    print(" " * (n-i) + "*" * (2*i-1))

# Diamond Pattern
# Combines pyramid (top half) and inverted pyramid (bottom half)
# Top: grows from 1 star to (2n-1) stars
# Bottom: shrinks back from (2n-3) stars to 1 star
n = 5
for i in range(1, n+1):
    print(" " * (n-1) + "*" * (2*i-1))
for i in range(n-1, 0, -1):
    print(" " * (n-i) + "*" * (2*i-1))

# Hollow Pyramid
# Prints only the outline of a pyramid (no fill inside)
# Top row: single star centered
# Middle rows: two stars with spaces in between
# Bottom row: full solid base of stars
n = 5
for i in range(1, n+1):
    if i == 1:
        print(" " * (n-i) + "*")
    elif i == n:
        print("*" * (2*n-1))
    else:
        print(" " * (n-i) + "*" + " " * (2*i-3) + "*")

# Square Pattern
# Prints a solid n x n square of stars
# Every row has exactly n stars
n = 5
for i in range(n):
    print("*" * n)

# Hollow Square
# Prints only the border of an n x n square
# First and last rows are full, middle rows have stars only at edges
n = 5
for i in range(n):
    if i == 0 or i == n-1:
        print("*" * n)
    else:
        print("*" + " " * (n-2) + "*")

# Right-Angled Triangle Mirrored
# Prints a right-aligned triangle using leading spaces
# Stars increase while spaces decrease each row
n = 5
for i in range(1, n+1):
    print(" " * (n-i) + "*" * i)

# Inverted Mirrored Triangle
# Right-aligned triangle printed upside down
# Stars decrease while spaces increase each row
n = 5
for i in range(n, 0, -1):
    print(" " * (n-i) + "*" * i)

# Hourglass Pattern
# Combines inverted pyramid (top) and pyramid (bottom)
# Starts wide, narrows to a single star, then expands again
n = 5
for i in range(n, 0, -1):
    print(" " * (n-i) + "*" * (2*i-1))
for i in range(2, n+1):
    print(" " * (n-i) + "*" * (2*i-1))

# Hollow Diamond
# Prints only the outline of a diamond shape
# Top half: two stars with growing space between them
# Bottom half: two stars with shrinking space between them
n = 5
for i in range(1, n+1):
    if i == 1:
        print(" " * (n-i) + "*")
    else:
        print(" " * (n-i) + "*" + " " * (2*i-3) + "*")
for i in range(n-1, 0, -1):
    if i == 1:
        print(" " * (n-i) + "*")
    else:
        print(" " * (n-i) + "*" + " " * (2*i-3) + "*")

# Cross / Plus Pattern
# Prints a plus sign shape in the center of an n x n grid
# Stars appear only on the middle row and middle column
n = 5
mid = n // 2
for i in range(n):
    for j in range(n):
        if i == mid or j == mid:
            print("*", end="")
        else:
            print(" ", end="")
    print()

# Checkerboard Pattern
# Alternates stars and spaces like a chessboard
# Even positions get a star, odd positions get a space
n = 5
for i in range(n):
    for j in range(n):
        if (i + j) % 2 == 0:
            print("*", end="")
        else:
            print(" ", end="")
    print()

# Butterfly Pattern
# Prints two triangles mirrored horizontally
# Stars grow outward from both sides row by row
n = 5
for i in range(1, n+1):
    print("*" * i + " " * (2*(n-i)) + "*" * i)
for i in range(n, 0, -1):
    print("*" * i + " " * (2*(n-i)) + "*" * i)