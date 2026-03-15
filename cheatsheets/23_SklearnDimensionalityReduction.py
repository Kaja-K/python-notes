from sklearn.decomposition import PCA, NMF
from sklearn.manifold import TSNE
from sklearn.feature_selection import (
    SelectKBest, f_classif, RFE, SelectFromModel
)
from sklearn.ensemble import RandomForestClassifier
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

# always scale before PCA — variance is sensitive to scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ── PCA — Principal Component Analysis ───────────────────────
# finds directions of maximum variance — reduces dimensions linearly
pca = PCA(n_components=2)               # reduce to 2 dimensions
X_pca = pca.fit_transform(X_scaled)

pca.explained_variance_ratio_           # % variance explained by each component
pca.explained_variance_ratio_.cumsum()  # cumulative — helpful to pick n_components

# how many components to keep?
pca_full = PCA()
pca_full.fit(X_scaled)
# keep enough to explain 95% variance
n = (pca_full.explained_variance_ratio_.cumsum() < 0.95).sum() + 1

pca = PCA(n_components=0.95)            # shortcut: keep 95% variance automatically
X_pca = pca.fit_transform(X_scaled)

# ── t-SNE — visualisation only ───────────────────────────────
# great for 2D/3D visualisation — NOT for training models on
# non-linear, preserves local structure
tsne = TSNE(n_components=2, perplexity=30, random_state=42)
X_tsne = tsne.fit_transform(X_scaled)   # note: no transform() — fit only

# ── NMF — Non-negative Matrix Factorisation ───────────────────
# requires non-negative data — good for text, images, audio
nmf = NMF(n_components=5, random_state=42)
X_nmf = nmf.fit_transform(X)           # no scaling needed (must be >= 0)

# ── FEATURE SELECTION ────────────────────────────────────────
# SelectKBest — pick k features with highest statistical score
selector = SelectKBest(score_func=f_classif, k=10)  # f_classif for classification
X_best = selector.fit_transform(X_train, y_train)
selected_cols = X_train.columns[selector.get_support()]

# RFE — Recursive Feature Elimination — fits model, removes weakest features
from sklearn.linear_model import LogisticRegression
rfe = RFE(estimator=LogisticRegression(max_iter=1000), n_features_to_select=10)
rfe.fit(X_train, y_train)
X_rfe = rfe.transform(X_train)
X_train.columns[rfe.support_]          # selected feature names

# SelectFromModel — keep features above importance threshold
sfm = SelectFromModel(RandomForestClassifier(n_estimators=100, random_state=42))
sfm.fit(X_train, y_train)
X_sfm = sfm.transform(X_train)