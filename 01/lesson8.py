"""Portfolio mean return, cum return, std dev and sharpe ratio.
Need to create a function to do the above for a portfolio.
"""
from util import get_data, normalise_data, compute_daily_returns

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
    
def portfolio_stats(portfolio_df):
    """Takes as input a portfolio dataframe.
    Returns a dictionary with portfolio's mean, std_dev, cum return, and sharpe 
    ratio."""
    #Calculate the daily returns of the portfolio
    daily_returns = compute_daily_returns(portfolio_df)
    
    #Delete the first row which is zero
    daily_returns = daily_returns[1:]
    
    #Calculate statistics
    port_cum_return = (portfolio_df[-1]/portfolio_df[0]) - 1
    avg_daily_return = daily_returns.mean()
    std_dev_daily_return = daily_returns.std()
    sharpe_ratio = avg_daily_return/std_dev_daily_return
    
    results = {'port_cum_return': port_cum_return,
               'ave_daily_return':avg_daily_return,
               'std_dev_daily_return': std_dev_daily_return,
               'sharpe_ratio': sharpe_ratio}
    return results
    
def test_run():
    #arguments for portfolio_builder function.
    dates = pd.date_range('2009-01-01', '2011-12-31')
    symbols = ['SPY', 'XOM', 'GOOG', 'GLD']
    port_allocations = [0.4, 0.4, 0.1, 0.1]
    init_investment = 1000000
    
    df = portfolio_builder(dates, symbols, port_allocations, init_investment)
    print(portfolio_stats(df))


if __name__ == '__main__':
    test_run()