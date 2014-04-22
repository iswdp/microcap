from stocks import *
import dateutil, datetime
import pandas as pd

def create_stock_dict(symbols):
    stock_data = {}

    for i in symbols:
        print i
        data = import_stock_prices(i)
        forward = forward_lag(data, i, 1)
        back = back_lag(data, i, 10)
        stock_data[i] = combine_lags(forward, back)

    return stock_data

def symbol_slice(df, start):
    #slices data for a single symbol up to the current test date
    start = dateutil.parser.parse(start)
    delta = datetime.timedelta(days=1)

    for i in range(50):
        try:
            end_index = df[df['Date'] == start.strftime('%Y-%m-%d')].index.values[0]
            break
        except:
            if i == 49:
                print '\tSymbol could not be sliced.'
                return DataFrame()
            pass
        start -= delta

    result = df.ix[:end_index,:]
    return result

def construct_rolling_model_data(stock_dict, start, n = 15):
    #returns a model dataframe and a feature vector for a prediction test set
    train = DataFrame()
    test = DataFrame()
    print 'Constructing model data.'

    pop_list = []
    for i in stock_dict:
        print 'Slicing ' + str(i)
        stock_dict[i] = symbol_slice(stock_dict[i], start)

        if len(stock_dict[i]) == 0:
            pop_list.append(i)
    for i in pop_list:
        stock_dict.pop(i)

    for i in stock_dict:
        print i

        if len(train) == 0:
            train = stock_dict[i].ix[:(len(stock_dict[i])-2),:]
        else:
            train = pd.concat([train, stock_dict[i].ix[:(len(stock_dict[i])-2),:]], axis = 0)

        if len(test) == 0:
            test = DataFrame(stock_dict[i].ix[(len(stock_dict[i])-1),:]).T
        else:
            test = pd.concat([test, DataFrame(stock_dict[i].ix[(len(stock_dict[i])-1),:]).T], axis = 0)

    train = train.reset_index()
    test = test.reset_index()
    return train, test

SPY = import_stock_prices('SPY')
date_list = []

for i  in SPY['Date']:
    date_list.append(i)

symbols = ['TWOC', 'ACY']
stock_data = create_stock_dict(symbols)

#x = symbol_slice(stock_data['TYBT'], '2014-01-21')
x, y = construct_rolling_model_data(stock_data, '2013-01-18', n = 15)