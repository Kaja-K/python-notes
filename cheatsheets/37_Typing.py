from typing import (
    Optional, Union, List, Dict, Tuple, Set,
    Any, Callable, Iterator, Generator,
    TypeVar, Generic, TypedDict, Literal,
    Final, ClassVar, overload
)
from typing import get_type_hints
from dataclasses import dataclass

# ── WHY TYPE HINTS ───────────────────────────────────────────
# - documentation that can't go out of date
# - IDE autocomplete and warnings
# - static analysis with mypy / pyright
# Python does NOT enforce them at runtime — purely informational

# ── BASIC ANNOTATIONS ────────────────────────────────────────
x: int = 10
name: str = 'Anna'
pi: float = 3.14
active: bool = True

def greet(name: str) -> str:            # arg type → return type
    return f"Hello, {name}"

def add(a: int, b: int) -> int:
    return a + b

def process() -> None:                  # function returns nothing
    print("done")

# ── COLLECTIONS ──────────────────────────────────────────────
# Python 3.9+ — use built-in types directly (lowercase)
nums:   list[int]        = [1, 2, 3]
lookup: dict[str, int]   = {'a': 1}
pair:   tuple[int, str]  = (1, 'hi')
tags:   set[str]         = {'a', 'b'}

# fixed-length tuple
point:  tuple[float, float]       = (1.5, 2.5)
record: tuple[str, int, float]    = ('ST_001', 5, 75.5)

# Python 3.8 and earlier — use typing module
nums:   List[int]        = [1, 2, 3]
lookup: Dict[str, int]   = {'a': 1}

# nested
matrix:   list[list[float]]       = [[1.0, 2.0], [3.0, 4.0]]
registry: dict[str, list[str]]    = {'Warsaw': ['ST_001', 'ST_002']}

# ── OPTIONAL — value or None ─────────────────────────────────
def find_station(sid: str) -> Optional[str]:    # returns str or None
    if sid == 'ST_001': return 'Warsaw'
    return None

# Optional[X] is shorthand for Union[X, None]
def set_city(city: Optional[str] = None) -> None:
    pass

# Python 3.10+ shorthand
def find(sid: str) -> str | None:
    pass

# ── UNION — one of several types ─────────────────────────────
def parse_id(value: Union[int, str]) -> str:
    return str(value)

# Python 3.10+ shorthand
def parse(value: int | str | float) -> str:
    return str(value)

# ── ANY — opt out of type checking ───────────────────────────
def log(value: Any) -> None:            # accepts literally anything
    print(value)

# ── CALLABLE ─────────────────────────────────────────────────
# Callable[[arg_types], return_type]
def apply(func: Callable[[int], int], x: int) -> int:
    return func(x)

apply(lambda x: x**2, 5)               # fine — lambda matches Callable[[int],int]

transform: Callable[[str, int], bool]   # function taking str and int, returning bool

# ── ITERATOR & GENERATOR ─────────────────────────────────────
def count_up(n: int) -> Iterator[int]:
    for i in range(n):
        yield i

def gen() -> Generator[int, None, None]:  # yield type, send type, return type
    yield 1
    yield 2

# ── LITERAL — specific allowed values ────────────────────────
def set_status(status: Literal['Active', 'Inactive', 'Maintenance']) -> None:
    pass

Direction = Literal['North', 'South', 'East', 'West']
def move(d: Direction) -> None:
    pass

# ── FINAL — constant, cannot be reassigned ───────────────────
MAX_LOAD: Final[int]   = 100
VERSION:  Final        = '1.0.0'

# ── TYPEDDICT — dict with known keys and types ───────────────
class StationRecord(TypedDict):
    station_id: str
    city:       str
    load:       float

def process_record(r: StationRecord) -> None:
    print(r['city'])        # IDE knows this is a str

record: StationRecord = {'station_id': 'ST_001', 'city': 'Warsaw', 'load': 75.5}

# with optional keys
from typing import NotRequired
class Config(TypedDict):
    host:    str
    port:    int
    debug:   NotRequired[bool]      # this key is optional

# ── TYPEVAR — generic type placeholder ───────────────────────
T = TypeVar('T')

def first(items: list[T]) -> T:     # works for any list type
    return items[0]

first([1, 2, 3])        # returns int
first(['a', 'b'])       # returns str

# constrained TypeVar
Number = TypeVar('Number', int, float)

def double(x: Number) -> Number:
    return x * 2

# ── CLASS VARIABLES ──────────────────────────────────────────
class Station:
    company: ClassVar[str] = 'TeleCorp'     # class variable (shared by all instances)
    station_id: str                          # instance variable (per instance)
    load: float = 0.0

# ── ANNOTATING FUNCTIONS IN PRACTICE ────────────────────────
import pandas as pd
import numpy as np

def clean_load(df: pd.DataFrame, col: str = 'load_pct') -> pd.DataFrame:
    """removes rows where load column is NaN or out of 0-100 range"""
    df = df.dropna(subset=[col])
    return df[(df[col] >= 0) & (df[col] <= 100)]

def top_n_stations(
    df:     pd.DataFrame,
    n:      int = 10,
    metric: str = 'load_pct',
    asc:    bool = False
) -> pd.DataFrame:
    return df.nlargest(n, metric) if not asc else df.nsmallest(n, metric)

def load_summary(loads: list[float]) -> dict[str, float]:
    return {
        'mean':   float(np.mean(loads)),
        'max':    float(np.max(loads)),
        'min':    float(np.min(loads)),
    }

# ── RUNTIME INTROSPECTION ────────────────────────────────────
get_type_hints(greet)           # {'name': <class 'str'>, 'return': <class 'str'>}
greet.__annotations__           # same, raw dict