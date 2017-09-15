import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from util import get_data, normalise_data, compute_daily_returns, plot_data


#--------Get to portfolio value from stock prices----------------------
def get_portfolio_value(data_df, allocs, start_val = 1):
    """ Function that takes a dataframe of stock prices and allocation
    for each stock and returns a dataframe of portfolio value for each date.
    """
    #Normalise the stock prices
    normed_port = normalise_data(data_df)
    
    #Reflect price changes based on each stock's portfolio allocation.
    allocated_port = normed_port*allocs
    
    #How much each stock(col) in the portfolio is worth on each day(row).
    port_posn_values = allocated_port*start_val
    
    #Sum across all stocks(cols)to show portfolio's value for each day(row).
    portfolio = port_posn_values.sum(axis = 1)
    
    return portfolio
    
#---------Get a portfolio's performance stats------------------------
def get_portfolio_stats(portfolio, rfr = 0.0, sf = 252):
    """Take a portfolio dataframe  as input and return its cumulative 
    return, average daily return, standard deviation and sharpe ratio.
    
    Parameters:
    ----------
    portfolio: dataframe containing prices of the portfolio.
    rfr: float - risk free rate
    sf: int - sampling frequency per year, needed to calculate shapre ratio.
    
    Return cumulative return, average daily return, standard deviation and sharpe ratio
    """
    #Cumulative return
    cum_ret = (portfolio[-1]/portfolio[0]) - 1
    
    #Daily returns and delete row 1 = zero because it affects calculations.
    daily_returns = compute_daily_returns(portfolio)
    daily_returns = daily_returns[1:]
    
    #Average daily return
    ave_daily_ret = daily_returns.mean()
    
    #Std dev of daily returns
    std_daily_ret = daily_returns.std()
    
    #Sharp ratio of portfolio
    sharpe_ratio = np.sqrt(sf)*((daily_returns - rfr).mean())/std_daily_ret
    
    #end value of portfolio
    #end_val = portfolio[-1]
    
    return cum_ret, ave_daily_ret, std_daily_ret, sharpe_ratio

#----------...----------------------------------------
def assess_portfolio(sd, ed, syms, allocs, rfr = 0.0, sf = 252, gen_plot = True, sv = 1):
    """Function takes a number of paarameters and returns numerous statistics
    to assess a portfolio's performance.
    
    Parameters:
    -----------
    - sd: string - start date of the historical data.
    - ed:string - end date of the historical data.
    - syms: list/tuple/array of symbols of equities
    - allocs: list/tuple/array of same length as syms, allocating proportion
            of starting value (sv) to each equity.
    - sv: float - starting value of the investment.
    - rfr: float - risk free rate
    - sf: int - sampling frequency per year, needed to calculate shapre ratio.
    - gen_plot: boolean - if False do not create any output. If True output a
                plot.png
    
    Return a dictionary with:
    -------
    cum_ret: float - cumulative return
    ave_daily_ret: int - Average period return (if sf == 252 this is daily return)
    std_daily_ret: float - Standard deviation of daily returns
    sharpe_ratio: float - Sharpe ratio
    #ev: End value of portfolio
    """  
    #---------Build the portfolio---------------------------------
    #Start with the stock prices dataframe which also has SPY.
    dates = pd.date_range(sd, ed)
    df = get_data(syms, dates)
    #Only SPY dataframe - used to add to plot later
    SPY = df.loc[:, syms[0]]
    normed_SPY = normalise_data(SPY)
    #portfolio dataframe without SPY
    port = df.loc[:, syms[1]:]
    #Get the portfolio's value from the individual stocks in port.
    port_final = get_portfolio_value(port, allocs, start_val = sv)
    #
    
    #----------Get portfolio's performance statistics--------
    cum_ret, ave_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(port_final)
    
    #----------Plot the normalised portfolio and SPY prices--------
    if gen_plot == True:
        df_temp = pd.concat([port_final, normed_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_data(df_temp ,title = 'Daily portfolio value and SPY', 
                  fontsize = 2, xlabel = 'Dates', ylabel = 'Normalised price')

    return cum_ret, ave_daily_ret, std_daily_ret, sharpe_ratio

def test_run():
#---Example1--------------------------------------------------------------
    sd = '2010-01-01'
    ed = '2010-12-31'
    syms = ['GOOG', 'AAPL', 'GLD', 'XOM'] 
    allocs = [0.2, 0.3, 0.4, 0.1]
    
    cr, adr, sddr, sr = assess_portfolio(sd = sd, ed = ed, syms = syms, allocs = allocs)
    print('Example 1')
    print('Sharpe ratio: ' + str(sr))
    print('Volatility (sddr): ' + str(sddr))
    print('Average Daily Return: ' + str(adr))
    print('Cumulative Return: ' + str(cr))
    #print('end val' + str(end_val))
    
    #Correct results to check against:
    #Sharpe Ratio: 1.51819243641
    #Volatility (stdev of daily returns): 0.0100104028
    #Average Daily Return: 0.000957366234238
    #Cumulative Return: 0.255646784534
    
#---Example2--------------------------------------------------------------
    sd = '2010-01-01'
    ed = '2010-12-31'
    syms = ['AXP', 'HPQ', 'IBM', 'HNZ'] 
    allocs = [0.0, 0.0, 0.0, 1.0]
    
    cr, adr, sddr, sr = assess_portfolio(sd = sd, ed = ed, syms = syms, allocs = allocs)
    print('Example 2')
    print('Sharpe ratio: ' + str(sr))
    print('Volatility (sddr): ' + str(sddr))
    print('Average Daily Return: ' + str(adr))
    print('Cumulative Return: ' + str(cr))
    
    #Correct results to check against:
    #Sharpe Ratio: 1.30798398744
    #Volatility (stdev of daily returns): 0.00926153128768
    #Average Daily Return: 0.000763106152672
    #Cumulative Return: 0.198105963655
    
#---Example3--------------------------------------------------------------
    sd = '2010-06-01'
    ed = '2010-12-31'
    syms = ['GOOG', 'AAPL', 'GLD', 'XOM'] 
    allocs = [0.2, 0.3, 0.4, 0.1]
    
    cr, adr, sddr, sr = assess_portfolio(sd = sd, ed = ed, syms = syms, allocs = allocs)
    print('Example 3')
    print('Sharpe ratio: ' + str(sr))
    print('Volatility (sddr): ' + str(sddr))
    print('Average Daily Return: ' + str(adr))
    print('Cumulative Return: ' + str(cr))  
    
    #Correct results to check against:
    #Sharpe Ratio: 2.21259766672
    #Volatility (stdev of daily returns): 0.00929734619707
    #Average Daily Return: 0.00129586924366
    #Cumulative Return: 0.205113938792
        
if __name__ == '__main__':
    test_run()
