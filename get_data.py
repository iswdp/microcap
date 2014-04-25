from stocks import *
from pandas import DataFrame

fi = open('500-800list.txt', 'r')
symbols = []
for i in fi:
    symbols.append(i.strip())
#symbols = symbols[0:5]

for i in symbols:
    print i
    try:
        current = import_stock_prices(i)
        path = 'Small_Caps/' + i + '.csv'
        current.to_csv(path, sep = ',', index = False)
    except:
        pass