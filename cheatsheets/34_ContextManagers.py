from contextlib import contextmanager
import time

# context manager = object that sets up and tears down a resource
# used with the 'with' statement — teardown happens even if an exception occurs

# ── BUILT-IN CONTEXT MANAGERS ────────────────────────────────
with open('file.txt', 'w') as f:
    f.write('hello')            # file is always closed, even on exception

import threading
lock = threading.Lock()
with lock:
    pass                        # lock is always released

# ── CONTEXTLIB — easiest way to write one ────────────────────
@contextmanager
def timer_ctx(label=''):
    start = time.perf_counter()
    try:
        yield                   # code inside 'with' block runs here
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label} took {elapsed:.4f}s")

with timer_ctx('data loading'):
    time.sleep(0.1)             # prints "data loading took 0.1002s"

@contextmanager
def temp_directory():
    """creates a temp dir, yields its path, cleans up on exit"""
    import tempfile, shutil
    tmpdir = tempfile.mkdtemp()
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)   # always cleaned up

with temp_directory() as tmpdir:
    print(f"Working in {tmpdir}")
    # tmpdir is deleted automatically after this block

# ── CLASS-BASED CONTEXT MANAGER ──────────────────────────────
# implement __enter__ and __exit__
class DatabaseConnection:
    def __init__(self, host):
        self.host = host
        self.conn = None

    def __enter__(self):
        print(f"Connecting to {self.host}")
        self.conn = object()    # would be real connection
        return self.conn        # assigned to 'as' variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing connection")
        self.conn = None
        return False            # False = don't suppress exceptions

with DatabaseConnection('localhost') as conn:
    pass                        # connection always closed after

# ── SUPPRESS — ignore specific exceptions ────────────────────
from contextlib import suppress

with suppress(FileNotFoundError):
    open('nonexistent.txt')     # silently ignored — no try/except needed

# ── REDIRECT STDOUT ──────────────────────────────────────────
from contextlib import redirect_stdout
import io

buffer = io.StringIO()
with redirect_stdout(buffer):
    print("this goes to buffer, not terminal")
output = buffer.getvalue()      # "this goes to buffer, not terminal\n"