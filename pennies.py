from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import pandas as pd
import numpy as np

train = pd.read_csv('local_train.csv')
test = pd.read_csv('local_test.csv')

train = train.replace([np.inf, -np.inf], np.nan)
test = test.replace([np.inf, -np.inf], np.nan)

train = train.dropna(axis=0)
test = test.dropna(axis=0)

print 'Fitting\n'
m = RandomForestRegressor(n_estimators=1000, n_jobs=10 ,verbose=1)
m.fit(train.ix[:,6:], train.ix[:,5])
print 'Predicting\n'
preds = m.predict(test.ix[:,6:])

result = test.ix[:,:6]
result['Prediction'] = preds
result.to_csv('temp_results/pennies_result.csv', sep = ',', index = False)