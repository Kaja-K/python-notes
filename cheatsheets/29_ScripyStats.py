import numpy as np
import pandas as pd
from scipy import stats

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
    'region':      np.random.choice(['North','South','East','West'], n),
})

# ── DESCRIPTIVE STATISTICS ───────────────────────────────────
stats.describe(df['load_pct'])          # n, min, max, mean, variance, skewness, kurtosis

stats.skew(df['load_pct'])              # skewness: 0=symmetric, >0=right tail, <0=left tail
stats.kurtosis(df['load_pct'])          # kurtosis: 0=normal, >0=heavy tails
stats.sem(df['load_pct'])               # standard error of the mean
stats.iqr(df['load_pct'])              # interquartile range (Q3 - Q1)
stats.variation(df['load_pct'])        # coefficient of variation (std/mean)

# ── NORMALITY TEST ───────────────────────────────────────────
# before many tests you need to check if data is normally distributed
stat, p = stats.shapiro(df['load_pct'])
print(f"Shapiro-Wilk: stat={stat:.4f}, p={p:.4f}")
# p > 0.05 → fail to reject normality (data looks normal)
# p < 0.05 → data is NOT normally distributed

stat, p = stats.normaltest(df['load_pct'])  # D'Agostino-Pearson (better for n>50)

# ── ONE-SAMPLE T-TEST ────────────────────────────────────────
# question: is the mean load significantly different from 50?
stat, p = stats.ttest_1samp(df['load_pct'], popmean=50)
print(f"One-sample t-test: stat={stat:.3f}, p={p:.4f}")
# p < 0.05 → mean is significantly different from 50

# ── TWO-SAMPLE T-TEST (independent) ─────────────────────────
# question: is load in Warsaw different from Krakow?
warsaw = df[df['city'] == 'Warsaw']['load_pct']
krakow = df[df['city'] == 'Krakow']['load_pct']

stat, p = stats.ttest_ind(warsaw, krakow)
print(f"Independent t-test: stat={stat:.3f}, p={p:.4f}")

# Welch's t-test — use when groups have different variances (safer default)
stat, p = stats.ttest_ind(warsaw, krakow, equal_var=False)

# ── PAIRED T-TEST ────────────────────────────────────────────
# question: did load change before vs after an intervention?
# data must be same samples measured twice
before = df['load_pct'][:50].values
after  = before + np.random.normal(2, 5, 50)    # simulate small increase
stat, p = stats.ttest_rel(before, after)
print(f"Paired t-test: stat={stat:.3f}, p={p:.4f}")

# ── MANN-WHITNEY U — non-parametric alternative to t-test ────
# use when data is NOT normally distributed
stat, p = stats.mannwhitneyu(warsaw, krakow, alternative='two-sided')
print(f"Mann-Whitney U: stat={stat:.1f}, p={p:.4f}")

# ── ANOVA — compare means across 3+ groups ───────────────────
# question: is load different across all cities?
groups = [df[df['city'] == c]['load_pct'] for c in df['city'].unique()]
stat, p = stats.f_oneway(*groups)
print(f"One-way ANOVA: F={stat:.3f}, p={p:.4f}")
# p < 0.05 → at least one group mean is different
# ANOVA doesn't tell you WHICH groups differ — use post-hoc test for that

# Kruskal-Wallis — non-parametric ANOVA
stat, p = stats.kruskal(*groups)
print(f"Kruskal-Wallis: stat={stat:.3f}, p={p:.4f}")

# ── CHI-SQUARE TEST — categorical independence ───────────────
# question: is device_type independent of region?
ct = pd.crosstab(df['device_type'], df['region'])
stat, p, dof, expected = stats.chi2_contingency(ct)
print(f"Chi-square: stat={stat:.3f}, p={p:.4f}, dof={dof}")
# p < 0.05 → the two variables are NOT independent (there's a relationship)

# ── PEARSON CORRELATION ──────────────────────────────────────
# measures linear relationship between two continuous variables
r, p = stats.pearsonr(df['load_pct'], df['temperature'])
print(f"Pearson r={r:.3f}, p={p:.4f}")
# r: -1 = perfect negative, 0 = no linear, +1 = perfect positive

# Spearman — non-parametric, works for monotonic (not just linear) relationships
r, p = stats.spearmanr(df['load_pct'], df['temperature'])
print(f"Spearman r={r:.3f}, p={p:.4f}")

# ── LINEAR REGRESSION ────────────────────────────────────────
slope, intercept, r_value, p_value, std_err = stats.linregress(
    df['uptime_days'], df['load_pct']
)
print(f"slope={slope:.4f}, intercept={intercept:.2f}, R²={r_value**2:.4f}")

# ── CONFIDENCE INTERVALS ─────────────────────────────────────
mean = df['load_pct'].mean()
se   = stats.sem(df['load_pct'])
ci   = stats.t.interval(confidence=0.95, df=len(df)-1, loc=mean, scale=se)
print(f"95% CI: ({ci[0]:.2f}, {ci[1]:.2f})")
# "we are 95% confident the true mean lies between these values"

# ── EFFECT SIZE — how big is the difference? ─────────────────
# Cohen's d — standardised difference between two means
def cohen_d(a, b):
    pooled_std = np.sqrt((a.std()**2 + b.std()**2) / 2)
    return (a.mean() - b.mean()) / pooled_std

d = cohen_d(warsaw, krakow)
print(f"Cohen's d = {d:.3f}")
# rule of thumb: 0.2 small, 0.5 medium, 0.8 large

# ── OUTLIER DETECTION ────────────────────────────────────────
# Z-score method — flag values more than 3 std from mean
z_scores = np.abs(stats.zscore(df['load_pct']))
outliers = df[z_scores > 3]

# IQR method — more robust, doesn't assume normality
Q1  = df['load_pct'].quantile(0.25)
Q3  = df['load_pct'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['load_pct'] < Q1 - 1.5*IQR) | (df['load_pct'] > Q3 + 1.5*IQR)]

# ── DISTRIBUTIONS — generate / fit ───────────────────────────
# generate random samples from distributions
stats.norm.rvs(loc=50, scale=10, size=100)      # normal
stats.uniform.rvs(loc=0, scale=100, size=100)   # uniform
stats.poisson.rvs(mu=1.5, size=100)             # poisson
stats.expon.rvs(scale=10, size=100)             # exponential

# PDF / CDF / PPF (inverse CDF)
stats.norm.pdf(x=60, loc=50, scale=10)          # probability density at x=60
stats.norm.cdf(x=60, loc=50, scale=10)          # P(X <= 60)
stats.norm.ppf(q=0.95, loc=50, scale=10)        # value at 95th percentile

# fit a distribution to your data
loc, scale = stats.norm.fit(df['load_pct'])     # estimate mean and std from data
loc, scale = stats.expon.fit(df['load_pct'])