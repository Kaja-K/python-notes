import time
import functools

# a decorator wraps a function to add behaviour before/after it runs
# @decorator is syntactic sugar for: func = decorator(func)

# ── BASIC DECORATOR ──────────────────────────────────────────
def timer(func):
    @functools.wraps(func)          # preserves original function name and docstring
    def wrapper(*args, **kwargs):
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        end    = time.perf_counter()
        print(f"{func.__name__} took {end-start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(0.1)
    return 42

slow_function()     # prints "slow_function took 0.1002s", returns 42

# ── DECORATOR WITH ARGUMENTS ─────────────────────────────────
def repeat(n):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hello():
    print("Hello!")

say_hello()         # prints "Hello!" three times

# ── PRACTICAL DECORATORS ─────────────────────────────────────
def log_calls(func):
    """logs every call with args and return value"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}({args}, {kwargs})")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

def retry(times=3, exceptions=(Exception,)):
    """retries a function if it raises an exception"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == times - 1:
                        raise
                    print(f"Attempt {attempt+1} failed: {e}")
        return wrapper
    return decorator

@retry(times=3, exceptions=(ConnectionError,))
def fetch_data(url):
    pass    # would make an HTTP request in real code

def validate_positive(func):
    """ensures all numeric arguments are positive"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg <= 0:
                raise ValueError(f"Expected positive number, got {arg}")
        return func(*args, **kwargs)
    return wrapper

@validate_positive
def sqrt(x):
    return x ** 0.5

# stacking decorators — applied bottom to top
@timer
@log_calls
def compute(x, y):
    return x + y

# ── CLASS-BASED DECORATORS (built-in) ────────────────────────
class Station:
    def __init__(self, station_id, city):
        self._station_id = station_id
        self._city       = city
        self._load       = 0

    @property                       # getter — s.load
    def load(self): return self._load

    @load.setter                    # setter — s.load = 80
    def load(self, v):
        if not 0 <= v <= 100: raise ValueError("Load must be 0-100")
        self._load = v

    @staticmethod                   # no self/cls — utility function
    def validate_id(sid): return sid.startswith('ST_')

    @classmethod                    # receives class — alternative constructor
    def from_string(cls, s):
        sid, city = s.split(',')
        return cls(sid.strip(), city.strip())

# ── FUNCTOOLS EXTRAS ─────────────────────────────────────────
from functools import lru_cache, partial, reduce

# lru_cache — memoisation: cache results, skip recomputation
@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2: return n
    return fibonacci(n-1) + fibonacci(n-2)

fibonacci(50)           # fast — cached results reused
fibonacci.cache_info()  # CacheInfo(hits=..., misses=..., maxsize=128, currsize=...)
fibonacci.cache_clear() # clear the cache

# partial — pre-fill some arguments of a function
def power(base, exp): return base ** exp

square = partial(power, exp=2)
cube   = partial(power, exp=3)
square(5)   # 25
cube(3)     # 27

# reduce — fold: apply function cumulatively
reduce(lambda a, b: a + b, [1, 2, 3, 4, 5])    # 15
reduce(lambda a, b: a * b, [1, 2, 3, 4, 5])    # 120
