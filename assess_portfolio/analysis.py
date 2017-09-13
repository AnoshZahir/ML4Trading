"""ML4Trading project 1: assess_portfolio 

Overview:
---------
A portfolio is a collection of stocks (or other assets) and corresponding 
allocations of funds to each of them. In order to evaluate and compare 
different portfolios, we first need to compute certain metrics, based on 
available historical data.

The primary goal of this assignment is to introduce you to this form of 
portfolio analysis. You will use pandas for reading in data, calculating 
various statistics and plotting a comparison graph.

Task:
-----    
Create a function called assess_portfolio() that takes as input a description 
of a portfolio and computes important statistics about it. You are given the 
following inputs for analyzing a portfolio:
    
    * A date range to select the historical data to use (specified by a start and 
end date). You should consider performance from close of the start date to 
close of the end date.

    * Symbols for equities (e.g., GOOG, AAPL, GLD, XOM). Note: You should support 
any symbol in the data directory.

    * Allocations to the equities at the beginning of the simulation (e.g., 0.2, 0.3, 0.4, 0.1), should sum to 1.0.
    
    *Total starting value of the portfolio (e.g. $1,000,000)

Your goal is to compute the daily portfolio value over given date range, and 
then the following statistics for the overall portfolio:
    * Cumulative return
    * Average period return (if sampling frequency == 252 then this is average 
    daily return)
    * Standard deviation of daily returns
    * Sharpe ratio of the overall portfolio, given daily risk free rate (usually 0), and yearly sampling frequency (usually 252, the no. of trading days in a year)
    * Ending value of the portfolio

"""
from files.util import get_data, normalise_data, compute_daily_returns

def assess_portfolio(sd, ed, syms, allocs, sv, rfr, sf, gen_plot):
    """Function 
    
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
    
    Return a dictionary with the following:
    -------
    cr: float - cumulative return
    adr: int - Average period return (if sf == 252 this is daily return)
    sddr: float - Standard deviation of daily returns
    sr: float - Sharpe ratio
    ev: End value of portfolio
    """
    
    dates = pd.date_range(sd, ed) 

    def portfolio_builder(dates, symbols, port_allocations, init_investment):
        """Based on dates, symbols and portfolio allocations, return a dataframe
        which shows the normalised daily value of a portfolio.
        """
        #Start with the stock prices dataframe.
        df = get_data(symbols, dates)
        #Normalise the prices
        normed_df = normalise_data(df)
        #Reflect price changes based on each stock's portfolio allocation.
        allocated_df = normed_df*port_allocations
        #How much each stock(col) in the portfolio is worth on each day(row).
        posnValues_df = allocated_df*init_investment
        #Sum across all stocks(cols)to show portfolio's value for each day(row).
        portfolioValue_df = posnValues_df.sum(axis = 1)
        return portfolioValue_df
    
    #build a portfolio
    portfolio_df = portfolio_builder(dates, syms, allocs, sv)
    
    #Calculate the daily returns of the portfolio
    daily_returns = compute_daily_returns(portfolio_df)
    
    #Delete the first row which is zero
    daily_returns = daily_returns[1:]
    
    #Calculate statistics
    cr = (portfolio_df[-1]/portfolio_df[0]) - 1
    adr = daily_returns.mean()
    sddr = daily_returns.std()
    sr = np.sqrt(sf)*(adr - rfr)/sddr
    ev = portfolio_df[-1, :]
    
    results = {'cr': cr, 'adr': adr, 'sddr': sddr, 'sr': sr, 'ev': ev}
    return results
