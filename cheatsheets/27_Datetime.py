import datetime as dt
from datetime import date, time, timedelta, timezone

# ── CREATING ─────────────────────────────────────────────────
now   = dt.datetime.now()                       # current local datetime
today = dt.date.today()                         # current date only
utc   = dt.datetime.now(timezone.utc)           # current UTC datetime

d = dt.datetime(2026, 3, 14, 9, 30, 0)         # specific datetime
d = dt.date(2026, 3, 14)                        # date only
t = dt.time(9, 30, 0)                           # time only

# ── PARSING — string → datetime ──────────────────────────────
d = dt.datetime.strptime('2026-03-14', '%Y-%m-%d')
d = dt.datetime.strptime('14/03/2026 09:30', '%d/%m/%Y %H:%M')

# common format codes:
# %Y  4-digit year     %m  month 01-12    %d  day 01-31
# %H  hour 00-23       %M  minute 00-59   %S  second 00-59
# %A  weekday name     %B  month name     %j  day of year

# pandas is often easier for bulk parsing
import pandas as pd
pd.to_datetime('2026-03-14')
pd.to_datetime(['2026-03-01', '2026-03-02'])
pd.to_datetime('14/03/2026', dayfirst=True)

# ── FORMATTING — datetime → string ───────────────────────────
now.strftime('%Y-%m-%d')                        # '2026-03-14'
now.strftime('%d %B %Y')                        # '14 March 2026'
now.strftime('%Y%m%d_%H%M%S')                  # '20260314_093000' — good for filenames

# ── ACCESSING PARTS ──────────────────────────────────────────
now.year                # 2026
now.month               # 3
now.day                 # 14
now.hour                # 9
now.weekday()           # 0=Monday ... 6=Sunday
now.isoweekday()        # 1=Monday ... 7=Sunday
now.date()              # extract date part only
now.time()              # extract time part only

# ── ARITHMETIC ───────────────────────────────────────────────
delta = timedelta(days=7, hours=3, minutes=30)
next_week = now + delta                         # add time
yesterday = now - timedelta(days=1)

diff = dt.datetime(2026, 12, 31) - now         # difference → timedelta
diff.days                                       # total days
diff.total_seconds()                            # total seconds

# ── DATE RANGES (pandas) ─────────────────────────────────────
pd.date_range(start='2026-01-01', end='2026-12-31', freq='D')   # daily
pd.date_range(start='2026-01-01', periods=12, freq='MS')         # 12 month starts
pd.date_range(start='2026-01-01', periods=52, freq='W')          # 52 weeks

# ── DATETIME IN DATAFRAMES ───────────────────────────────────
import numpy as np
np.random.seed(42)
df = pd.DataFrame({
    'station_id': [f'ST_{str(i).zfill(3)}' for i in range(1, 101)],
    'date':       pd.date_range(start='2026-01-01', periods=100, freq='D'),
    'load_pct':   np.round(np.random.uniform(5, 100, 100), 1),
})

df['date'] = pd.to_datetime(df['date'])
df['year']    = df['date'].dt.year
df['month']   = df['date'].dt.month
df['day']     = df['date'].dt.day
df['weekday'] = df['date'].dt.day_name()        # 'Monday', 'Tuesday'...
df['week']    = df['date'].dt.isocalendar().week
df['quarter'] = df['date'].dt.quarter

# filter by date
df[df['date'] >= '2026-03-01']
df[df['date'].dt.month == 3]                    # only March rows
df.set_index('date').resample('W').mean()       # weekly average (resample)
df.set_index('date').resample('ME').sum()       # monthly total

# ── TIMEZONES ────────────────────────────────────────────────
import pytz
warsaw = pytz.timezone('Europe/Warsaw')
now_utc    = dt.datetime.now(timezone.utc)
now_warsaw = now_utc.astimezone(warsaw)

