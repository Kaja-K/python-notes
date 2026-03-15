from sklearn.model_selection import (
    cross_val_score, KFold, StratifiedKFold,
    GridSearchCV, RandomizedSearchCV
)
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import make_scorer, f1_score
from sklearn.model_selection import train_test_split
import numpy as np

# ── TRAIN / TEST SPLIT ───────────────────────────────────────
# X = features (everything except target), y = what we predict
df = ["data"]
X = df.drop(columns='target')
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,      # 20% test, 80% train
    random_state=42,    # fixed seed — same split every run
    stratify=y          # keep class ratio in both splits (classification only)
)

# ── CROSS VALIDATION ─────────────────────────────────────────
# more reliable than a single train/test split
model = RandomForestClassifier(n_estimators=100, random_state=42)

scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"CV accuracy: {scores.mean():.3f} ± {scores.std():.3f}")

# StratifiedKFold — keeps class ratio in each fold (use for classification)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=skf, scoring='f1_weighted')

# common scoring strings:
# 'accuracy', 'f1', 'f1_weighted', 'roc_auc',
# 'r2', 'neg_mean_absolute_error', 'neg_root_mean_squared_error'

# custom scorer
custom = make_scorer(f1_score, average='macro')
cross_val_score(model, X, y, cv=5, scoring=custom)

# ── GRID SEARCH — exhaustive ─────────────────────────────────
# tries every combination of params — slow but thorough
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth':    [3, 5, None],
    'min_samples_split': [2, 5]
}

grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,          # use all CPU cores
    verbose=1
)
grid.fit(X_train, y_train)

grid.best_params_       # best combination found
grid.best_score_        # CV score with best params
grid.best_estimator_    # fitted model with best params — ready to predict

# ── RANDOMIZED SEARCH — faster ───────────────────────────────
# samples random combinations — much faster than grid search
# use when search space is large
from scipy.stats import randint, uniform

param_dist = {
    'n_estimators':     randint(50, 500),
    'max_depth':        randint(2, 20),
    'min_samples_split': randint(2, 20),
    'max_features':     uniform(0.1, 0.9)
}

random_search = RandomizedSearchCV(
    RandomForestClassifier(random_state=42),
    param_dist,
    n_iter=50,          # try 50 random combinations
    cv=5,
    scoring='accuracy',
    random_state=42,
    n_jobs=-1
)
random_search.fit(X_train, y_train)
random_search.best_params_

# ── COMPARING MODELS ─────────────────────────────────────────
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000),
    'Random Forest':       RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting':   GradientBoostingClassifier(n_estimators=100, random_state=42),
}

results = {}
for name, m in models.items():
    scores = cross_val_score(m, X, y, cv=5, scoring='accuracy')
    results[name] = {'mean': scores.mean(), 'std': scores.std()}
    print(f"{name:25s}: {scores.mean():.3f} ± {scores.std():.3f}")

# ── LEARNING CURVE — diagnose over/underfitting ───────────────
from sklearn.model_selection import learning_curve

train_sizes, train_scores, val_scores = learning_curve(
    model, X, y, cv=5,
    train_sizes=np.linspace(0.1, 1.0, 10),
    scoring='accuracy'
)
# if train score >> val score → overfitting (need more data or regularisation)
# if both scores low → underfitting (need more complex model or features)