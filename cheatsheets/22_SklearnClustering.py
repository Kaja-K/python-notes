from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

# ── TRAIN / TEST SPLIT ───────────────────────────────────────
# X = features (everything except target), y = what we predict
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
X = df.drop(columns='target')
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,      # 20% test, 80% train
    random_state=42,    # fixed seed — same split every run
    stratify=y          # keep class ratio in both splits (classification only)
)

# always scale before clustering — distances are sensitive to scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ── K-MEANS ──────────────────────────────────────────────────
# partition into k clusters by minimising within-cluster variance
# requires: you specify k upfront

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans.fit(X_scaled)

kmeans.labels_              # cluster label (0,1,2) for each row
kmeans.cluster_centers_     # centroid of each cluster
kmeans.inertia_             # total within-cluster sum of squares (lower = better)

df['cluster'] = kmeans.labels_

# finding the right k — elbow method
inertias = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)
# plot inertias — look for the "elbow" where curve flattens

# ── DBSCAN ───────────────────────────────────────────────────
# density-based — finds clusters of arbitrary shape
# automatically detects noise points (label = -1)
# no need to specify k — but needs eps and min_samples tuning

dbscan = DBSCAN(eps=0.5, min_samples=5)
dbscan.fit(X_scaled)
dbscan.labels_              # -1 = noise/outlier

n_clusters = len(set(dbscan.labels_)) - (1 if -1 in dbscan.labels_ else 0)
n_noise = (dbscan.labels_ == -1).sum()

# ── HIERARCHICAL CLUSTERING ──────────────────────────────────
# builds a tree of clusters — no need to specify k upfront
agg = AgglomerativeClustering(n_clusters=3, linkage='ward')
agg.fit(X_scaled)
agg.labels_

# ── EVALUATION ───────────────────────────────────────────────
# silhouette score — how similar each point is to its own cluster vs others
# range: -1 to 1 — higher is better — 0.5+ is decent
silhouette_score(X_scaled, kmeans.labels_)

# davies-bouldin score — ratio of within-cluster to between-cluster distances
# lower is better — 0 is perfect
davies_bouldin_score(X_scaled, kmeans.labels_)

# inspect cluster profiles
df['cluster'] = kmeans.labels_
df.groupby('cluster').mean(numeric_only=True)  # average features per cluster