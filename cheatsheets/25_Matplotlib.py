import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
 
np.random.seed(42)
n = 100
 
df = pd.DataFrame({
    'station_id':  [f'ST_{str(i).zfill(3)}' for i in range(1, n+1)],
    'city':        np.random.choice(['Warsaw','Krakow','Wroclaw','Gdansk','Poznan'], n),
    'device_type': np.random.choice(['Router','Switch','BTS','Repeater'], n),
    'status':      np.random.choice(['Active','Inactive','Maintenance'], n, p=[0.7,0.2,0.1]),
    'load_pct':    np.round(np.random.uniform(5, 100, n), 1),
    'uptime_days': np.random.randint(1, 730, n),
    'incidents':   np.random.poisson(lam=1.5, size=n),
    'temperature': np.round(np.random.normal(45, 10, n), 1),
    'date':        pd.date_range(start='2026-01-01', periods=n, freq='D'),
    'region':      np.random.choice(['North','South','East','West'], n),
})

x = np.linspace(0, 10, 100)
y = np.sin(x)

# ── BASIC PLOTS ──────────────────────────────────────────────
plt.plot(x, y)                                                  # line plot
plt.scatter(x, y)                                               # scatter plot
plt.bar(['A', 'B', 'C'], [3, 7, 5])                             # bar chart
plt.barh(['A', 'B', 'C'], [3, 7, 5])                            # horizontal bar chart
plt.hist(np.random.randn(1000), bins=30)                        # histogram
plt.boxplot([np.random.randn(100), np.random.randn(100)])       # box plot
plt.pie([30, 40, 30], labels=['X','Y','Z'], autopct='%1.1f%%')  # pie chart
plt.imshow(np.random.rand(10, 10), cmap='viridis')              # heatmap / image

# ── LABELS & TITLES ──────────────────────────────────────────
plt.title('My Chart', fontsize=16, fontweight='bold')
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.legend(['series 1', 'series 2'])    # needs labels on plots first
plt.legend(loc='upper right')           # location: 'best', 'upper left', etc.

# ── STYLING A LINE ───────────────────────────────────────────
plt.plot(x, y,
    color='steelblue',      # color name, hex '#1f77b4', or rgb (0.1, 0.5, 0.9)
    linewidth=2,            # line thickness
    linestyle='--',         # '--' dashed, ':' dotted, '-.' dash-dot, '-' solid
    marker='o',             # 'o' circle, 's' square, '^' triangle, 'x' cross
    markersize=5,
    alpha=0.8,              # transparency 0 (invisible) to 1 (opaque)
    label='sin(x)'          # label for legend
)

# ── AXES LIMITS & TICKS ──────────────────────────────────────
plt.xlim(0, 10)
plt.ylim(-1.5, 1.5)
plt.xticks([0, 2, 4, 6, 8, 10])
plt.yticks([-1, 0, 1], ['-1', 'zero', '+1'])   # custom tick labels
plt.xticks(rotation=45)                          # rotate labels

# ── GRID & REFERENCE LINES ───────────────────────────────────
plt.grid(True, linestyle='--', alpha=0.5)
plt.axhline(y=0, color='black', linewidth=0.8)  # horizontal reference line
plt.axvline(x=5, color='red', linestyle=':')    # vertical reference line
plt.axhspan(ymin=-0.5, ymax=0.5, alpha=0.1, color='green')  # shaded band

# ── ANNOTATIONS ──────────────────────────────────────────────
plt.text(3, 0.5, 'some text', fontsize=12, color='red')   # text at position
plt.annotate('peak',
    xy=(np.pi/2, 1),            # point to annotate
    xytext=(3, 1.2),            # where to put the text
    arrowprops=dict(arrowstyle='->')
)

# ── FIGURE & SUBPLOTS ────────────────────────────────────────
fig, ax = plt.subplots()                        # single plot — recommended API
fig, axes = plt.subplots(2, 2, figsize=(10, 8)) # 2x2 grid of subplots
axes[0, 0].plot(x, y)                           # access each subplot
axes[0, 1].scatter(x, y)
axes[1, 0].hist(y, bins=20)
axes[1, 1].bar(['A','B','C'], [3,7,5])

plt.tight_layout()              # auto-fix spacing between subplots

# ── FIGURE SIZE & DPI ────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 5))         # width x height in inches
fig.set_dpi(150)

# ── OO API (recommended for anything non-trivial) ────────────
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y, color='steelblue', label='sin(x)')
ax.plot(x, np.cos(x), color='tomato', label='cos(x)')
ax.set_title('Trig functions')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 10)
# difference: plt.title() vs ax.set_title() — OO is better for subplots

# ── MULTIPLE LINES ON ONE PLOT ───────────────────────────────
fig, ax = plt.subplots()
for col in df.select_dtypes('number').columns:
    ax.plot(df.index, df[col], label=col)
ax.legend()

# ── TWIN AXES — two y-scales ─────────────────────────────────
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()               # share x axis, separate y axis
ax1.plot(x, y, color='blue', label='sin')
ax2.plot(x, np.exp(x/10), color='red', label='exp')
ax1.set_ylabel('sin', color='blue')
ax2.set_ylabel('exp', color='red')

# ── COLORMAPS & COLORBAR ─────────────────────────────────────
sc = plt.scatter(x, y, c=y, cmap='RdYlGn', s=20)  # color by value
plt.colorbar(sc, label='value')
# popular cmaps: 'viridis', 'plasma', 'RdBu', 'coolwarm', 'Blues'

# ── STYLES ───────────────────────────────────────────────────
plt.style.use('seaborn-v0_8-whitegrid')     # clean background
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (10, 5)    # global default size
plt.rcParams['font.size'] = 12

# ── SAVING & SHOWING ─────────────────────────────────────────
plt.savefig('chart.png', dpi=150, bbox_inches='tight')   # save to file
plt.savefig('chart.pdf')                                  # vector PDF
plt.show()                                                # display in notebook/window
plt.close()                                               # free memory
plt.clf()                                                 # clear current figure