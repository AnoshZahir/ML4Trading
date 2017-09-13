import numpy as np
import pandas as pd
from util import get_data, normalise_data, compute_daily_returns, plot_data

def assess_portfolio(sd, ed, syms, allocs, sv, rfr, sf, gen_plot):
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
    cr: float - cumulative return
    adr: int - Average period return (if sf == 252 this is daily return)
    sddr: float - Standard deviation of daily returns
    sr: float - Sharpe ratio
    ev: End value of portfolio
    """
    
    dates = pd.date_range(sd, ed) 
    
    #---------Build a portfolio dataframe---------------------------------

    #Start with the stock prices dataframe which also has SPY.
    df = get_data(syms, dates)
    
    #Only SPY dataframe - used to add to plot later
    SPY = df.loc[:, syms[0]:]
    
    #portfolio dataframe without SPY
    port = df.loc[:, syms[1]:]
    
    #Normalise the prices
    normed_port = normalise_data(port)
    normed_SPY = normalise_data(SPY)
    
    #Reflect price changes based on each stock's portfolio allocation.
    allocated_port = normed_port*allocs
    
    #How much each stock(col) in the portfolio is worth on each day(row).
    port_posn_values = allocated_port*sv
    
    #Sum across all stocks(cols)to show portfolio's value for each day(row).
    portfolio = port_posn_values.sum(axis = 1)
    
    #----------Calculate the portfolio's daily returns
    
    #Calculate the daily returns of the portfolio
    daily_returns = compute_daily_returns(portfolio)
    
    #Delete the first row which is zero
    daily_returns = daily_returns[1:]
    
    #Calculate statistics
    cr = (portfolio[-1]/portfolio[0]) - 1
    adr = daily_returns.mean()
    sddr = daily_returns.std()
    sr = np.sqrt(sf)*(adr - rfr)/sddr
    #ev = portfolio_df[-1, :]
    
    results = {'cr': cr, 'adr': adr, 'sddr': sddr, 'sr': sr, 'ev': 'test'}
    
    if gen_plot == True:
        
        plot_data(portfolio, title = 'Daily portfolio value and SPY', fontsize = 2, xlabel = 'Dates', 
              ylabel = 'Normalised price')
        

    return results


def test_run():
    sd = '2010-01-01'
    ed = '2010-12-31'
    syms = ['AXP', 'HPQ', 'IBM', 'HNZ']
    allocs = [0.0, 0.0, 0.0, 1.0]
    
    print(assess_portfolio(sd, ed, syms, allocs, sv = 1, rfr = 0.0, sf = 252, gen_plot = True))

if __name__ == '__main__':
    test_run()
