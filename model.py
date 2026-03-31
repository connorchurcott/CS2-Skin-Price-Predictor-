import joblib as jl
import helpers
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import numpy as np


ESTIMATORS = 800
MAX_DEPTH = 8
LEARNING_RATE = 0.05
SUBSAMPLE = 0.8
RANDOM_STATE = 42
TEST_SPLIT = 0.20

X = helpers.getFeaturesAsMatrix()
y = helpers.getValuesAsArray()

y_log = np.log1p(y)

X_train, X_test, y_train_log, y_test_log = train_test_split(
    X, y_log, test_size=TEST_SPLIT, random_state=RANDOM_STATE
)

_, _, _, y_test_original = train_test_split(
    X, y, test_size=TEST_SPLIT, random_state=RANDOM_STATE
)

model = GradientBoostingRegressor(
    n_estimators=ESTIMATORS,
    max_depth=MAX_DEPTH,
    learning_rate=LEARNING_RATE,
    subsample=SUBSAMPLE,
    random_state=RANDOM_STATE,
)
model.fit(X_train, y_train_log)

y_predicted_log = model.predict(X_test)
y_predicted = np.expm1(y_predicted_log)
# y_test = np.expm1(y_test_log)


mae = helpers.getMAE(y_predicted, y_test_original)
rmse = helpers.getRMSE(y_predicted, y_test_original)
mape = helpers.getMAPE(y_predicted, y_test_original)
cross_val = helpers.getcrossvalidation(X, y_log, 5, model)

print("=" * 60)
print("MODEL PERFORMANCE METRICS (LOG TRANSFORM)")
print("=" * 60)
print(f"Mean Absolute Error (MAE):        ${mae:.2f}")
print(f"Root Mean Squared Error (RMSE):   ${rmse:.2f}")
print(f"Mean Absolute Percentage Error:   {mape:.2f}%")
print(f"Cross-Validation R² Score:        {cross_val:.3f}")
print("=" * 60)


metrics = {
    "MAE": round(mae, 4),
    "RMSE": round(rmse, 4),
    "MAPE": round(mape, 4),
    "CROSSVAL": round(cross_val, 4),
}

jl.dump(model, "model.joblib")
jl.dump(metrics, "metrics.joblib")
