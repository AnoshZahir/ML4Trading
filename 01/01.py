import pandas as pd
import matplotlib.pyplot as plt

'''
def test_run():
    symbol = 'AAPL'
    df = pd.read_csv("data/{}.csv".format(symbol))
    adj_close = df['Adj Close']
    print(adj_close)
    adj_close.plot()
    plt.show()

if __name__ == '__main__':
    test_run()
'''

def get_df_column(symbol, column):
    df = pd.read_csv("data/{}.csv".format(symbol))
    return df[column]

def plot_price_data(symbol, column):
    column = get_df_column(symbol, column)
    column.plot()
    plt.show

def test_run():
    for symbol in ['AAPL', 'IBM']:
        plot_price_data(symbol, column = ['Close', 'Adj Close'])

if __name__ == '__main__':
    test_run()


import pandas as pd

def get_mean_volume(symbol):
    """Return the mean volume for stock indicated by symbol.
    Note: Data for a stock is stored in file: data/<symbol>.csv
    """
    df = pd.read_csv("data/{}.csv".format(symbol))
    return df['Volume'].mean()

def test_run():
    """Function called by Test Run."""
    for symbol in ['AAPL', 'IBM']:
        print('Mean volume')
        print(symbol, get_mean_volume(symbol))
if __name__ == "__main__":
    test_run()

import pandas as pd

def get_max_close(symbol):
    """Return the maximum closing value for stock indicated by symbol.
    Note: Data for a stock is stored in file: data/<symbol>.csv
    """
    df = pd.read_csv("data/{}.csv".format(symbol))
    return df['Close'].max()

def test_run():
    """Function called by Test Run."""
    for symbol in ['AAPL', 'IBM']:
        print('Max close')
        print(symbol, get_max_close(symbol))
if __name__ == "__main__":
    test_run()