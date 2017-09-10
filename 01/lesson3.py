"""
01-02 Working with multiple stocks
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

from util import symbol_to_path, get_data, plot_data, plot_selected 
from util import normalise_data

#-----------test_run function-----------------------------------------
def test_run():
    symbols = ['SPY', 'XOM', 'GOOG', 'GLD']
    dates = pd.date_range('2010-01-01', '2010-12-31')
    df =  get_data(symbols, dates)
    plot_data(df)
    #plot_selected(df, ['SPY', 'GOOG', 'IBM', 'GLD'], '2010-03-01', '2010-04-01')
    print(df.mean())
    
#-------------run-------------------------------------------------
if __name__ == '__main__':
    df = test_run()