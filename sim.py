from stocks import *

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
    end_index = df[df['Date'] == start].index.values[0]
    print end_index

SPY = import_stock_prices('SPY')
date_list = []

for i  in SPY['Date']:
    date_list.append(i)

symbols = ['TWOC', 'TYBT', 'UBCP']
stock_data = create_stock_dict(symbols)

x = symbol_slice(stock_data['TWOC'], '2005-01-19')