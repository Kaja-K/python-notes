from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
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

# ── ALGORITHMS ───────────────────────────────────────────────

# Linear Regression — fast, interpretable, assumes linear relationship
model = LinearRegression()

# Ridge — Linear + L2 penalty — shrinks coefficients, handles multicollinearity
model = Ridge(alpha=1.0)                # higher alpha = stronger regularisation

# Lasso — Linear + L1 penalty — can zero out irrelevant features (feature selection)
model = Lasso(alpha=0.1)

# ElasticNet — mix of Ridge and Lasso
model = ElasticNet(alpha=0.1, l1_ratio=0.5)

# Random Forest Regressor — robust, handles non-linear patterns
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Gradient Boosting Regressor — usually best accuracy
model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)

# SVR — good for small datasets with non-linear patterns
model = SVR(kernel='rbf', C=1.0, epsilon=0.1)

# KNN Regressor — predicts average of k nearest neighbours
model = KNeighborsRegressor(n_neighbors=5)

# ── TRAIN & PREDICT ──────────────────────────────────────────
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# ── EVALUATION ───────────────────────────────────────────────
mae  = mean_absolute_error(y_test, y_pred)      # average absolute error — same unit as target
mse  = mean_squared_error(y_test, y_pred)       # penalises large errors more
rmse = np.sqrt(mse)                             # root MSE — same unit as target
r2   = r2_score(y_test, y_pred)                 # 1.0 = perfect, 0 = baseline mean, <0 = bad

print(f"MAE:  {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R²:   {r2:.4f}")

# interpret R²:
# 0.9+ excellent, 0.7-0.9 good, 0.5-0.7 moderate, <0.5 poor

# residuals — look for patterns (there should be none)
residuals = y_test - y_pred