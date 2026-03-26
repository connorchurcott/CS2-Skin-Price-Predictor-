import joblib as jl 
import helpers
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


MAX_DEPTH = 20
RANDOM_STATE = 67
TEST_SPLIT = 0.20

X = helpers.getFeaturesAsMatrix()
y = helpers.getValuesAsArray()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SPLIT, random_state=RANDOM_STATE)

model = RandomForestRegressor(max_depth=MAX_DEPTH, random_state=RANDOM_STATE)
model.fit(X_train, y_train)

y_predicted = model.predict(X_test)
mae = helpers.getMAE(y_predicted, y_test)
rmse = helpers.getRMSE(y_predicted, y_test)
mape = helpers.getMAPE(y_predicted, y_test)
cross_val = helpers.getcrossvalidation(X,y,5,model)
print(mae)
print(rmse) 
print(mape)
#cross_val is the r2 value
print(cross_val)
# about $14 off on avg, still need cross validation, parameter tunning, hook up to GUIi
# gui needs way to convert user entered things into the ID's the model is using


