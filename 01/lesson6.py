""" 01-05 Missing data """

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from util import symbol_to_path, get_data, plot_data



#---------Fill missing na values in df_final-------------------
def fill_missing_values(df_data):
    """Fill missing values in df, forward and then backward fill, in place."""
    df_data.fillna(method = 'ffill', inplace = 'True')
    df_data.fillna(method = 'bfill', inplace = 'True')

#---------------test_run function------------------------------
def test_run():
    """Function called by Test Run."""    
    
    #list of symbols
    symbolList = ['PSX', 'Fake1', 'FAKE2'] 
    
    #create date range
    start_date = '2005-12-31'
    end_date = '2014-12-07'
    idx = pd.date_range(start_date, end_date) 
    
    #get adjusted close for each symbol
    df_data = get_data(symbolList, idx)
    
    #forward fill and then back fill na's
    fill_missing_values(df_data)

    #plot the data
    plot_data(df_data, title = 'Incomplete Data')
    
#--------------run--------------------------------------
if __name__ == '__main__':
    test_run()
    