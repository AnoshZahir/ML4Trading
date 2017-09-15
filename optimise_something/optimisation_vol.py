"""ml4t Autumn 2017: optimise_portfolio function to minimise volatility of 
portfolio."""
   
"""ml4t spring 2017: optimise_portfolio function to optimise the sharp 
ratio of a portfolio.
"""
import numpy as np
import pandas as pd
import scipy.optimize as spo
from util import normalise_data, plot_data
from analysis import get_port_SPY, get_portfolio_value, get_portfolio_stats

def find_optimised_alloc(portfolio, func):
    """Function takes a portfolio of stocks and returns list of allocations of
    the stocks in the portfolio optimised based on func."""
    #initial guess to pass to optimiser.  Equal allocattion to all stocks. 
    initial_guess_allocs = [1.0/portfolio.shape[1]]*portfolio.shape[1]
    
    #The allocations must add up to 1.0
    constraints = ({'type': 'eq', 'fun': lambda allocs: 1.0 - np.sum(allocs)})
    
    #Each allocation bounded by 0.0 and 1.0
    bounds = [(0.0, 1.0) for x in range(portfolio.shape[1])]
    
    result = spo.minimize(fun = func, x0 = initial_guess_allocs, 
                            args = (portfolio,), method = 'SLSQP', 
                            bounds = bounds, constraints=(constraints), 
                            options={'disp': True})
    
    return result.x

def error_alloc_vol(allocs, portfolio, start_val = 1):
    """Function that takes allocations and portfolio and returns the
    portfolio's sharpe ratio*(-1).  Used with find_optimsed_alloc."""   
    port_final = get_portfolio_value(portfolio, allocs, start_val)
    cum_ret, ave_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(port_final)
    return cum_ret
      
def optimise_portfolio(sd, ed, syms, rfr = 0.0, sf = 252, gen_plot = True):
    """Find the optimal allocation for a given set of stocks, optimised for 
    volatility (standard deviation of daily return).
    Parameters:
    -----------
    sd: A datetime object that represents the start date
    ed: A datetime object that represents the end date
    syms: A list of symbols that make up the portfolio
    rfr: float - risk free rate, default to 0.0 per day.
    sf: int - sampling frequency per year, default to 252 days
    gen_plot: If True, create a plot named plot.png
    Returns:
    -------
    allocs: A 1-d Numpy ndarray of allocations to the stocks. All the 
    allocations must be between 0.0 and 1.0 and they must sum to 1.0.
    cr: Cumulative return
    adr: Average daily return
    sddr: Standard deviation of daily return
    sr: Sharpe ratio
    """
    #---------Build the portfolio---------------------------------
    joint_df = get_port_SPY(sd, ed, syms) #syms + SPY df
    port = joint_df[0] #portfolio df w/o SPY
    SPY = joint_df[1] #SPY df - used to add to plot later
    normed_SPY = normalise_data(SPY) #Normalise SPY
    
    #Find the optimal allocations
    optimised_alloc = find_optimised_alloc(port, error_alloc_vol)
    
    #portfolio based on optimised allocations
    optimised_port = get_portfolio_value(port, optimised_alloc)
    
    #Get optimised portfolio's performance statistics
    cum_ret, ave_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(optimised_port)
    
    #----------Plot the normalised portfolio and SPY prices--------
    if gen_plot == True:
        df_temp = pd.concat([optimised_port, normed_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_data(df_temp ,title = 'Daily portfolio value and SPY', 
                  fontsize = 2, xlabel = 'Date', ylabel = 'Normalised price')


    return optimised_alloc, cum_ret, ave_daily_ret, std_daily_ret, sharpe_ratio

def test_run():
#---Example 1--------------------------------------------------------------
    sd = '2010-01-01'
    ed = '2010-12-31'
    syms = ['GOOG', 'AAPL', 'GLD', 'XOM'] 
    opt_alloc, cr, adr, sddr, sr = optimise_portfolio(sd, ed, syms, rfr = 0.0, sf = 252, gen_plot = True)
    print('Example 1')
    print('Optimal allocations: ' + str(opt_alloc))
    #print('Sharpe ratios match: ' + str(round(sr, 5) == round(???, 5)))
    print('Sharpe ratio: ' + str(sr))
    #print('Volatilities (sddr) match: ' + str(round(sddr, 5) == round(???, 5)))
    print('Volatility (sddr): ' + str(sddr))
    #print('Average Daily Returns match: ' + str(round(adr, 5) == round(???, 5)))
    print('Average Daily Return: ' + str(adr))
    #print('Cumulative Returns match: ' + str(round(cr, 5) == round(???, 5)))
    print('Cumulative Return: ' + str(cr))

if __name__ == '__main__':
    test_run()