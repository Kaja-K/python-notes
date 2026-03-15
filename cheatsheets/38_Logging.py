import logging
import sys
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

# ── WHY LOGGING OVER PRINT ───────────────────────────────────
# print()   — no timestamps, no severity, can't filter, can't redirect easily
# logging   — timestamps, levels, multiple handlers, easy to silence in production

# ── LOG LEVELS (low → high) ──────────────────────────────────
# DEBUG    10  — detailed diagnostic info (dev only)
# INFO     20  — confirms things are working as expected
# WARNING  30  — something unexpected but not breaking (default threshold)
# ERROR    40  — something failed, but program continues
# CRITICAL 50  — serious failure, program may not continue

# ── BASIC SETUP ──────────────────────────────────────────────
logging.basicConfig(level=logging.DEBUG)    # show everything from DEBUG up

logging.debug('detailed info for debugging')
logging.info('station ST_001 processed')
logging.warning('load above 80%')
logging.error('connection failed')
logging.critical('system shutdown')

# ── FORMATTING ───────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
# output: 2026-03-14 09:30:00 | INFO     | root | message

# useful format fields:
# %(asctime)s    — timestamp
# %(levelname)s  — DEBUG / INFO / WARNING etc.
# %(name)s       — logger name
# %(filename)s   — source file
# %(funcName)s   — function name
# %(lineno)d     — line number
# %(message)s    — the log message

# ── NAMED LOGGERS — recommended approach ─────────────────────
# each module gets its own logger — easy to filter by module
logger = logging.getLogger(__name__)        # use module name as logger name
logger.setLevel(logging.DEBUG)

logger.debug('debug message')
logger.info('info message')
logger.warning('warning message')
logger.error('error message')
logger.critical('critical message')

# log exceptions with traceback
try:
    1 / 0
except ZeroDivisionError:
    logger.exception('division failed')     # logs ERROR + full traceback automatically
    # or:
    logger.error('division failed', exc_info=True)  # same result

# log with extra context
logger.info('station processed', extra={'station_id': 'ST_001', 'city': 'Warsaw'})

# ── HANDLERS — where logs go ─────────────────────────────────
logger = logging.getLogger('my_app')
logger.setLevel(logging.DEBUG)

# console handler
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)              # only INFO+ to console

# file handler
file_h = logging.FileHandler('app.log', encoding='utf-8')
file_h.setLevel(logging.DEBUG)             # everything to file

# shared formatter
fmt = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s',
                         datefmt='%Y-%m-%d %H:%M:%S')
console.setFormatter(fmt)
file_h.setFormatter(fmt)

logger.addHandler(console)
logger.addHandler(file_h)
# now logger writes to BOTH console AND file simultaneously

# ── ROTATING FILE HANDLER — auto-manage file size ────────────
rotating = RotatingFileHandler(
    'app.log',
    maxBytes=5 * 1024 * 1024,      # rotate when file reaches 5 MB
    backupCount=3                   # keep 3 old files: app.log.1, .2, .3
)

# or rotate by time
timed = TimedRotatingFileHandler(
    'app.log',
    when='midnight',                # rotate at midnight
    interval=1,
    backupCount=7                   # keep 7 days of logs
)

# ── PRACTICAL PATTERN ────────────────────────────────────────
def setup_logger(name: str, log_file: str = None, level=logging.INFO):
    """create a logger that writes to console + optionally a file"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(fmt)
    logger.addHandler(console)

    if log_file:
        fh = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger

logger = setup_logger('data_pipeline', log_file='pipeline.log')

# ── USING IN DATA PIPELINE ───────────────────────────────────
import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    'station_id': [f'ST_{str(i).zfill(3)}' for i in range(1, 101)],
    'load_pct':   np.round(np.random.uniform(5, 100, 100), 1),
})

def process_stations(df: pd.DataFrame) -> pd.DataFrame:
    logger.info(f"Starting pipeline — {len(df)} stations")

    original = len(df)
    df = df.dropna(subset=['load_pct'])
    dropped = original - len(df)
    if dropped:
        logger.warning(f"Dropped {dropped} rows with missing load_pct")

    high = df[df['load_pct'] > 90]
    if len(high):
        logger.warning(f"{len(high)} stations above 90% load: {high['station_id'].tolist()}")

    try:
        df['load_norm'] = (df['load_pct'] - df['load_pct'].mean()) / df['load_pct'].std()
    except Exception as e:
        logger.exception(f"Normalisation failed: {e}")
        raise

    logger.info(f"Pipeline complete — {len(df)} stations processed")
    return df

df_clean = process_stations(df)

# ── FILTER — silence noisy libraries ─────────────────────────
logging.getLogger('matplotlib').setLevel(logging.WARNING)   # silence matplotlib debug
logging.getLogger('urllib3').setLevel(logging.WARNING)       # silence requests library

# ── QUICK ONE-LINER SETUP (scripts) ──────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('run.log')
    ]
)