from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, classification_report,
    confusion_matrix, roc_auc_score, ConfusionMatrixDisplay
)
from sklearn.model_selection import cross_val_score
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

# ── ALGORITHMS ───────────────────────────────────────────────
# all share the same API: fit() → predict()

# Logistic Regression — fast, interpretable, good first baseline
# C = inverse regularisation strength: higher C = less regularisation
model = LogisticRegression(max_iter=1000, C=1.0, random_state=42)

# Decision Tree — fully interpretable, but overfits easily
# max_depth limits tree size — key hyperparameter to tune
model = DecisionTreeClassifier(max_depth=5, min_samples_leaf=5, random_state=42)

# Random Forest — many trees voting together, much harder to overfit
# n_estimators: more trees = more stable, but slower
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)

# Gradient Boosting — builds trees sequentially, each fixing previous errors
# usually best accuracy, but slow and needs careful tuning
model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1,
                                    max_depth=3, random_state=42)

# SVM — works well in high-dimensional spaces (text, images)
# kernel='rbf' handles non-linear boundaries; probability=True enables predict_proba
model = SVC(kernel='rbf', C=1.0, probability=True, random_state=42)

# KNN — classifies by majority vote of k nearest neighbours
# no training phase, but slow at prediction — must scale features first!
model = KNeighborsClassifier(n_neighbors=5, metric='euclidean')

# Naive Bayes — assumes features are independent (naive), but very fast
# best for text classification and high-dimensional sparse data
model = GaussianNB()

# ── TRAIN & PREDICT ──────────────────────────────────────────
model.fit(X_train, y_train)              # learn patterns from training data
y_pred  = model.predict(X_test)          # predict class labels
y_proba = model.predict_proba(X_test)    # probability for each class
y_proba[:, 1]                            # probability of positive class (binary)

# single new prediction
model.predict([[5.1, 3.5, 1.4, 0.2]])    # one sample — returns array
model.predict_proba([[5.1, 3.5, 1.4, 0.2]])[0]  # probabilities for that sample

# ── EVALUATION ───────────────────────────────────────────────
accuracy_score(y_test, y_pred)           # fraction correct — misleading on imbalanced data!

# precision  = of all predicted positive, how many actually were? (avoid false alarms)
# recall     = of all actual positive, how many did we catch?     (avoid misses)
# f1-score   = harmonic mean of precision and recall
# support    = number of actual samples in each class
print(classification_report(y_test, y_pred))

# confusion matrix — rows = actual, cols = predicted
cm = confusion_matrix(y_test, y_pred)
# binary layout:
# [[TN, FP],     TN = correctly predicted negative
#  [FN, TP]]     TP = correctly predicted positive
#                FP = false alarm      FN = missed positive

# visualise confusion matrix
ConfusionMatrixDisplay(cm).plot()

# ROC-AUC — area under the ROC curve
# 1.0 = perfect separation, 0.5 = no better than random guessing
roc_auc_score(y_test, y_proba[:, 1])

# for multi-class
roc_auc_score(y_test, y_proba, multi_class='ovr', average='macro')

# cross-validated score — more reliable than single split
cv_scores = cross_val_score(model, X, y, cv=5, scoring='f1_weighted')
print(f"CV F1: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

# ── FEATURE IMPORTANCE ───────────────────────────────────────
# tree-based models (DecisionTree, RandomForest, GradientBoosting)
importances = pd.Series(
    model.feature_importances_,
    index=X_train.columns
).sort_values(ascending=False)
print(importances.head(10))              # top 10 most important features

# Logistic Regression — abs(coefficients) as proxy for importance
# only comparable when features are scaled
coefs = pd.Series(
    model.coef_[0],
    index=X_train.columns
).abs().sort_values(ascending=False)

# permutation importance — model-agnostic, works for any estimator
from sklearn.inspection import permutation_importance
result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)
perm_imp = pd.Series(result.importances_mean, index=X_train.columns).sort_values(ascending=False)

# ── THRESHOLD TUNING ─────────────────────────────────────────
# default threshold is 0.5 — adjust to trade precision vs recall
threshold = 0.3                           # lower = catch more positives (higher recall)
y_pred_custom = (y_proba[:, 1] >= threshold).astype(int)
print(classification_report(y_test, y_pred_custom))