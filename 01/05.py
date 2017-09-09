""" 01-05 Missing data """

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#---------function to get path of the symbol---------------
def symbol_to_path(symbol, base_dir = os.path.dirname(os.getcwd()) + '/data'):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))

#---------Reads csv-----------------------------------------
def get_data(symbollist, dates):
    """Read stock data(adjusted close) for given symbols from csv files.
        Return df_final with data for adj Close and dates as index."""     
    df_final = pd.DataFrame(index = dates)
    if 'SPY' not in symbollist:
        symbollist.insert(0, 'SPY')
    for symbol in symbollist:
        file_path = symbol_to_path(symbol)
        df_temp = pd.read_csv(file_path, parse_dates = True, index_col = 'Date',
                              usecols = ['Date', 'Adj Close'], 
                                na_values = ['nan'])
        df_temp = df_temp.rename(columns = {'Adj Close': symbol})
        df_final = df_final.join(df_temp)
        if symbol == 'SPY':
            df_final = df_final.dropna(subset = ['SPY'])
    return df_final

#---------Fill missing na values in df_final-------------------
def fill_missing_values(df_data):
    """Fill missing values in df, forward and then backward fill, in place."""
    df_data.fillna(method = 'ffill', inplace = 'True')
    df_data.fillna(method = 'bfill', inplace = 'True')
    
#---------------plot function----------------------------------
def plot_data(df_data):
    """Plot stock data with appropriate axis labels."""
    ax = df_data.plot(title = 'Incomplete Data', fontsize = 2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Prices')
    plt.show()
    
#---------------test_run function------------------------------
def test_run():
    """Function called by Test Run."""    
    
    #list of symbols
    symbollist = ['PSX', 'Fake1', 'FAKE2'] 
    
    #create date range
    start_date = '2005-12-31'
    end_date = '2014-12-07'
    idx = pd.date_range(start_date, end_date) 
    
    #get adjusted close for each symbol
    df_data = get_data(symbollist, idx)
    
    #forward fill and then back fill na's
    fill_missing_values(df_data)

    #plot the data
    plot_data(df_data)
    
#--------------run the code--------------------------------------
if __name__ == '__main__':
    test_run()
    