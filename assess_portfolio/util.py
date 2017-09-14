"""assess_portfolio util file"""

import os
import numpy as np
import pandas as pd
 
#---------Get path of the symbol. Used by get_data function---------
def symbol_to_path(symbol, base_dir = os.path.dirname(os.getcwd()) + '/data'):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))

#---------Reads csv-----------------------------------------
def get_data(symbolList, dates):
    """Read stock data(adjusted close) for given symbols from csv files.
        Return df_final with data for adj Close and dates as index."""     
    df_final = pd.DataFrame(index = dates)
    if 'SPY' not in symbolList:
        symbolList.insert(0, 'SPY')
    for symbol in symbolList:
        file_path = symbol_to_path(symbol)
        df_temp = pd.read_csv(file_path, parse_dates = True, index_col = 'Date',
                              usecols = ['Date', 'Adj Close'], 
                                na_values = ['nan'])
        df_temp = df_temp.rename(columns = {'Adj Close': symbol})
        df_final = df_final.join(df_temp)
        if symbol == 'SPY':
            df_final = df_final.dropna(subset = ['SPY'])
    return df_final

#-------------Function to normalise data------------------------------
def normalise_data(df):
    """Normalise stock prices using the first row of the dataframe."""
    return df/df.ix[0,:]

#-----------Function to compute daily returns----------------
def compute_daily_returns(df):
    """Compute and return daily return values."""
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:] / df[:-1].values) - 1
    #daily_returns.ix[0, :] = 0 # set daily returns for row 0 to 0
    daily_returns.ix[0] = 0 #for lesson8 the above does not work.  Get error
    # msg raise IndexingError(key), IndexingError: (0, slice(None, None, None))
    return daily_returns