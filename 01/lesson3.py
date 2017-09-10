"""
01-02 Working with multiple stocks
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

def symbol_to_path(symbol, base_dir = os.path.dirname(os.getcwd()) + '/data'):
    """Return CSV file path given ticker symbol.
    """
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def get_data(symbols, dates):
    """Read stock data(adj Close) for given symbols from CSV files.
    """
    df = pd.DataFrame(index = dates)
    if 'SPY' not in symbols:
        symbols.insert(0, 'SPY')
    
    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col = 'Date', 
                              parse_dates = True, usecols = ['Date', 'Adj Close'],
                              na_values = ['nan'])
        df_temp = df_temp.rename(columns = {'Adj Close': symbol})
        df = df.join(df_temp, how = 'left')
        '''inner join gets rid of the na's in df_temp but retains the reverse
        date order.  Left join retains df_temps's date order but also its na 
        values.  So we need more code to get rid of na's
        '''
        if symbol == 'SPY':
            df = df.dropna(subset=['SPY'])
    return df

def normalise_data(df):
    """Normalise stock prices using the first row of the dataframe."""
    return df/df.ix[0,:]

def plot_data(df, title = 'Stock prices'):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title = title, fontsize = 2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    plt.show()

def plot_selected(df, columns, start_index, end_index):
    """Plot the desired columns over index values in the given range
    """
    df_temp = df.ix[start_index:end_index, columns]
    return plot_data(df_temp, title = 'Selected data')

def test_run():
    symbols = ['SPY', 'XOM', 'GOOG', 'GLD']
    dates = pd.date_range('2010-01-01', '2010-12-31')
    df =  get_data(symbols, dates)
    plot_data(df)
    #plot_selected(df, ['SPY', 'GOOG', 'IBM', 'GLD'], '2010-03-01', '2010-04-01')
    
    print(df.mean())
if __name__ == '__main__':
    df = test_run()