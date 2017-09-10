"""Util file that contains all the utility functions used in part 01 of
 ML4Trading."""

import os
import pandas as pd
import matplotlib.pyplot as plt
 
#---------function to get path of the symbol---------------
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

#---------------plot function----------------------------------
def plot_data(df_data ,title = 'Stock prices', fontsize = 2, xlabel = 'Dates', 
              ylabel = 'Prices'):
    """Plot stock data with appropriate axis labels."""
    ax = df_data.plot(title = title, fontsize = fontsize)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()
    
#---------Plot function with custom columms and indices.-------------
def plot_selected(df, columns, start_index, end_index):
    """Plot the desired columns over index values in the given range
    """
    df_temp = df.ix[start_index:end_index, columns]
    return plot_data(df_temp, title = 'Selected data')