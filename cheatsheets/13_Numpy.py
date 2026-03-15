import numpy as np

# ── CREATING ARRAYS ──────────────────────────────────────────
# NumPy arrays are faster and use less memory than Python lists
# all elements must be the same type (unlike lists)
arr = np.array([1, 2, 3, 4, 5, 6])
matrix = np.array([[1, 2, 3], [4, 5, 6]])  # 2D array

np.zeros((3, 3))            # 3x3 filled with 0.0
np.ones((2, 2))             # 2x2 filled with 1.0
np.full((3, 3), 7)          # 3x3 filled with 7
np.eye(3)                   # 3x3 identity matrix (1s on diagonal)
np.empty((2, 3))            # uninitialized — fast but values are garbage

np.arange(0, 10, 2)         # [0, 2, 4, 6, 8] — like range() but returns array
np.linspace(0, 1, 100)      # 100 evenly spaced values from 0 to 1
np.logspace(0, 3, 4)        # [1, 10, 100, 1000] — log scale

# random
np.random.rand(5)           # 5 random floats [0, 1)
np.random.randint(0, 10, 5) # 5 random ints between 0 and 9
np.random.randn(3, 3)       # 3x3 from standard normal distribution
np.random.seed(42)          # fix seed for reproducibility

# ── SHAPE & RESHAPING ────────────────────────────────────────
arr.shape           # (6,)   — dimensions as tuple
arr.ndim            # 1      — number of dimensions
arr.size            # 6      — total number of elements
arr.dtype           # dtype('int64') — element type

arr.reshape((2, 3)) # change shape — total elements must stay the same
arr.reshape(-1, 2)  # -1 lets NumPy figure out that dimension automatically
arr.flatten()       # always returns a copy as 1D array
arr.ravel()         # like flatten but returns view when possible (faster)
arr[np.newaxis, :]  # add a new axis → shape (1, 6)

# ── INDEXING & SLICING ───────────────────────────────────────
a = np.array([10, 20, 30, 40, 50])
a[0]                # 10    — first element
a[-1]               # 50    — last element
a[1:4]              # [20, 30, 40]
a[::2]              # [10, 30, 50] — every second

m = np.array([[1, 2, 3], [4, 5, 6]])
m[0, 1]             # 2     — row 0, col 1
m[:, 1]             # [2, 5] — entire column 1
m[1, :]             # [4, 5, 6] — entire row 1

# boolean indexing — filter by condition
a[a > 25]           # [30, 40, 50] — elements where condition is True
a[(a > 15) & (a < 45)]  # [20, 30, 40] — combine conditions with & and |

# fancy indexing — pick elements by index list
a[[0, 2, 4]]        # [10, 30, 50]

# ── MATH & VECTORIZED OPERATIONS ────────────────────────────
# operations apply to every element — no loop needed
arr * 2             # [2, 4, 6, 8, 10, 12]
arr + 10            # [11, 12, 13, 14, 15, 16]
arr ** 2            # [1, 4, 9, 16, 25, 36]
np.sqrt(arr)        # element-wise square root
np.log(arr)         # element-wise natural log
np.exp(arr)         # element-wise e^x
np.abs(arr)         # element-wise absolute value

# element-wise between two arrays (same shape)
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
a + b               # [[6,8],[10,12]] — element-wise
a * b               # [[5,12],[21,32]] — element-wise (NOT matrix multiply)
np.dot(a, b)        # [[19,22],[43,50]] — true matrix multiplication
a @ b               # same as np.dot — cleaner syntax (Python 3.5+)
a.T                 # transpose — swap rows and columns

# ── STATISTICS ───────────────────────────────────────────────
data = np.array([10, 20, 30, 40, 50, 60])
np.mean(data)       # 35.0  — average
np.median(data)     # 35.0  — middle value
np.std(data)        # standard deviation — spread around mean
np.var(data)        # variance — std squared
np.min(data)        # 10
np.max(data)        # 60
np.sum(data)        # 210
np.cumsum(data)     # [10, 30, 60, 100, 150, 210] — running total
np.unique(data)     # sorted unique values
np.percentile(data, 75)  # 75th percentile — useful for outlier detection

# axis argument — 0 = column-wise (vertical), 1 = row-wise (horizontal)
m = np.array([[1, 2], [3, 4]])
np.sum(m, axis=0)   # [4, 6]  — sum each column
np.sum(m, axis=1)   # [3, 7]  — sum each row
np.mean(m, axis=0)  # [2., 3.] — mean of each column

# ── LOGIC & SEARCH ───────────────────────────────────────────
np.argmax(data)     # index of max value
np.argmin(data)     # index of min value
np.argsort(data)    # indices that would sort the array

# np.where(condition, value_if_true, value_if_false)
np.where(data > 30, 1, -1)  # [−1,−1,−1,1,1,1]
np.where(data > 30)          # just the indices where True: (array([3,4,5]),)

np.isnan(data)      # True where value is NaN (Not a Number)
np.isinf(data)      # True where value is infinity
np.any(data > 50)   # True if at least one element > 50
np.all(data > 0)    # True if all elements > 0

# ── CLEANING & CLIPPING ──────────────────────────────────────
np.clip(data, 15, 45)   # values below 15 → 15, above 45 → 45
                        # useful for capping outliers

# handle NaN — NaN poisons calculations
arr_with_nan = np.array([1.0, np.nan, 3.0])
np.nanmean(arr_with_nan)    # 2.0 — ignores NaN
np.nansum(arr_with_nan)     # 4.0 — ignores NaN

# ── COMBINING & SPLITTING ────────────────────────────────────
np.concatenate([arr, arr])          # join along existing axis
np.stack([[1, 2], [3, 4]])          # stack into 2D from list of 1D
np.vstack([a, b])                   # vertical stack (row-wise)
np.hstack([a, b])                   # horizontal stack (column-wise)
np.split(arr, 3)                    # split into 3 equal parts

# ── DTYPE & MEMORY ───────────────────────────────────────────
np.array([1, 2, 3], dtype=np.float32)   # specify element type
np.array([1, 2, 3], dtype=np.int8)      # smaller type → less memory
arr.astype(np.float64)                   # convert dtype

# ── SAVING & LOADING ─────────────────────────────────────────
np.save('array.npy', arr)           # save single array
np.load('array.npy')                # load it back
np.savetxt('data.csv', m, delimiter=',')  # save as CSV
np.loadtxt('data.csv', delimiter=',')     # load from CSV