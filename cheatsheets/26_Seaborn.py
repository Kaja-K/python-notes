import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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

# seaborn wraps matplotlib — always call plt.show() or plt.savefig() at the end
# most functions accept a DataFrame + column names as strings

# ── SETUP & THEMES ───────────────────────────────────────────
sns.set_theme()                                      # apply seaborn defaults globally
sns.set_theme(style='whitegrid')                     # styles: 'white','dark','whitegrid','darkgrid','ticks'
sns.set_theme(palette='husl', font_scale=1.2)

sns.set_palette('tab10')                             # change color palette
# palettes: 'tab10','husl','Set2','pastel','muted','dark','colorblind'
sns.color_palette('Set2', n_colors=5)                # preview palette

# ── DISTRIBUTION PLOTS ───────────────────────────────────────
sns.histplot(df['load_pct'], bins=20, kde=True)                   # histogram + density curve
sns.kdeplot(df['load_pct'], fill=True)                            # density only
sns.kdeplot(data=df, x='load_pct', hue='city')                   # separate curves per group
sns.ecdfplot(df['load_pct'])                                      # cumulative distribution
sns.rugplot(df['load_pct'])                                       # tick marks along axis

sns.displot(df, x='load_pct', kind='hist', kde=True)             # figure-level version
sns.displot(df, x='load_pct', col='city', kind='kde')            # separate panel per city

# ── CATEGORICAL PLOTS ────────────────────────────────────────
sns.barplot(df, x='city', y='load_pct')                          # mean per category + CI
sns.barplot(df, x='city', y='load_pct', estimator='median')      # custom aggregation
sns.countplot(df, x='city')                                       # count of rows per category
sns.boxplot(df, x='city', y='load_pct')                          # median + IQR + outliers
sns.violinplot(df, x='city', y='load_pct')                       # distribution shape per group
sns.stripplot(df, x='city', y='load_pct', jitter=True)           # raw points, jittered
sns.swarmplot(df, x='city', y='load_pct')                        # points non-overlapping
sns.pointplot(df, x='region', y='load_pct', hue='city')          # mean + CI per group

# combine box + raw points
fig, ax = plt.subplots()
sns.boxplot(df, x='city', y='load_pct', ax=ax)
sns.stripplot(df, x='city', y='load_pct', color='black', size=3, alpha=0.5, ax=ax)

# ── RELATIONAL PLOTS ─────────────────────────────────────────
sns.scatterplot(df, x='load_pct', y='temperature',
    hue='city',             # color by category
    size='incidents',       # size by value
    style='device_type',    # marker shape by category
    alpha=0.7
)
sns.lineplot(df, x='date', y='load_pct', errorbar='sd')          # line + shaded CI

# figure-level (creates its own figure with FacetGrid)
sns.relplot(df, x='load_pct', y='temperature', hue='city',
            col='region', kind='scatter')

# ── REGRESSION / TREND ───────────────────────────────────────
sns.regplot(df, x='load_pct', y='temperature')                   # scatter + regression line
sns.regplot(df, x='load_pct', y='temperature', order=2)          # polynomial regression
sns.lmplot(df, x='load_pct', y='temperature', hue='city')        # regression per group
sns.residplot(df, x='load_pct', y='temperature')                 # residuals plot

# ── HEATMAPS & MATRICES ──────────────────────────────────────
corr = df.select_dtypes('number').corr()
sns.heatmap(corr,
    annot=True,             # show correlation values
    fmt='.2f',              # format numbers
    cmap='coolwarm',        # diverging: red=positive, blue=negative
    vmin=-1, vmax=1,        # fix scale
    linewidths=0.5          # cell borders
)

# pivot data into matrix then plot
pivot = df.pivot_table(index='city', columns='region', values='load_pct', aggfunc='mean')
sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlOrRd')

sns.clustermap(corr, cmap='coolwarm', figsize=(8, 8))            # heatmap + hierarchical clustering

# ── PAIRPLOT — all pairs of numeric columns ──────────────────
sns.pairplot(df, hue='city')                                      # scatter matrix
sns.pairplot(df, hue='city', diag_kind='kde')                    # KDE on diagonal
sns.pairplot(df, vars=['load_pct', 'temperature', 'uptime_days']) # select specific columns

# ── FACET GRID — small multiples ─────────────────────────────
# same plot repeated for each group — great for comparing
g = sns.FacetGrid(df, col='region', height=3)
g.map(sns.histplot, 'load_pct')
g.add_legend()

# catplot / displot / relplot all use FacetGrid internally
sns.catplot(df, x='city', y='load_pct', kind='box', col='region')

# ── WORKING WITH MATPLOTLIB ──────────────────────────────────
# seaborn axes are matplotlib axes — all plt/ax methods work
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
sns.boxplot(df, x='city', y='load_pct', ax=axes[0])
sns.histplot(df['load_pct'], bins=20, ax=axes[1])
axes[0].set_title('Load by City')
axes[1].set_xlabel('Load (%)')
plt.tight_layout()

# ── SAVING ───────────────────────────────────────────────────
plt.savefig('chart.png', dpi=150, bbox_inches='tight')
plt.show()
plt.close()