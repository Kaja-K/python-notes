from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
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

# ── MISSING VALUES ───────────────────────────────────────────
imputer = SimpleImputer(strategy='mean')     # fill NaN with column mean
# other strategies: 'median', 'most_frequent', 'constant'
X_train = imputer.fit_transform(X_train)     # learn from train, then apply
X_test  = imputer.transform(X_test)          # apply same rule — never fit on test!

# ── SCALING ──────────────────────────────────────────────────
# StandardScaler — mean=0, std=1 — best default choice
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)           # same rule: fit only on train

# MinMaxScaler — squeezes all values to [0, 1]
scaler = MinMaxScaler()                      # good for neural nets

# RobustScaler — uses median, resistant to outliers
scaler = RobustScaler()                      # use when data has extreme values

# why fit only on train?
# fitting on test leaks information → overly optimistic results

# ── ENCODING CATEGORIES ──────────────────────────────────────
# LabelEncoder — 0, 1, 2... — use only for target column or binary
le = LabelEncoder()
le.fit_transform(['cat', 'dog', 'cat', 'bird'])  # [1, 2, 1, 0]
le.inverse_transform([1, 2])                      # ['cat', 'dog']
le.classes_                                       # ['bird', 'cat', 'dog']

# OneHotEncoder — creates binary columns — for non-ordinal categories
ohe = OneHotEncoder(sparse_output=False, drop='first')  # drop='first' avoids multicollinearity
ohe.fit_transform([['red'], ['green'], ['blue']])

# pandas shortcut for one-hot encoding
pd.get_dummies(df, columns=['City'], drop_first=True)

# OrdinalEncoder — ordered numbers — for ordinal categories
from sklearn.preprocessing import OrdinalEncoder
oe = OrdinalEncoder(categories=[['low', 'medium', 'high']])
oe.fit_transform([['low'], ['high'], ['medium']])  # [[0], [2], [1]]

# ── PIPELINE — chain all steps cleanly ───────────────────────
from sklearn.ensemble import RandomForestClassifier

pipe = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler',  StandardScaler()),
    ('model',   RandomForestClassifier(n_estimators=100, random_state=42))
])

pipe.fit(X_train, y_train)      # runs all steps in order
pipe.predict(X_test)            # preprocessing + prediction in one call
pipe.score(X_test, y_test)      # accuracy on test set