from stocks import *
from pandas import DataFrame
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def get_data(symbol_list, n = 15, flag = 1, blag = 10):
    train = DataFrame()
    test = DataFrame()
    for i in symbol_list:
        print i

        try:
            data = import_stock_prices(i)
            forward = forward_lag(data, i, flag)
            back = back_lag(data, i, blag)
            combined = combine_lags(forward, back)

            #Train------------------------------------------------------------------
            random_sample = []
            for j in range(n):
                random_sample.append(random.randint(0,(len(combined) - 2)))
            data_slice = combined.ix[random_sample,:].reset_index()
            if len(train) == 0:
                train = data_slice
            else:
                train = pd.concat([train, data_slice], axis = 0)

            #Test-------------------------------------------------------------------
            data_slice = DataFrame(back.ix[len(back) - 1,:]).T

            if len(test) == 0:
                test = data_slice
            else:
                test = pd.concat([test, data_slice], axis = 0)
        except:
            print '\tSkipped'
            pass

    train = train.reset_index()
    del train['level_0']
    del train['index']

    test = test.reset_index()  
    del test['level_0']
    del test['index']

    return train, test

def main():
    fi = open('25-75_microcap_list.txt', 'r')
    symbols = []
    for i in fi:
        symbols.append(i.strip())
    #symbols = symbols[0:6]

    train, test = get_data(symbols, n = 30, flag = 1, blag = 12)

    train = train.replace([np.inf, -np.inf], np.nan)
    test = test.replace([np.inf, -np.inf], np.nan)

    train = train.dropna(axis=0)
    test = test.dropna(axis=0)

    print 'Fitting\n'
    m = RandomForestRegressor(n_estimators=250, n_jobs=1)
    m.fit(train.ix[:,6:], train.ix[:,5])
    print 'Predicting\n'
    preds = m.predict(test.ix[:,5:])

    result = test.ix[:,:4]
    result['Prediction'] = preds
    result = result.sort('Prediction', ascending=False)
    print result.head()
    result.to_csv('trade_result.csv', sep = ',', index = False)

if __name__ == '__main__':
    status = main()
    exit(status)