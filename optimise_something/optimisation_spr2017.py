"""ml4t spring 2017: optimise_portfolio function to optimise the sharp 
ratio of a portfolio.
"""
   
import datetime as dt
#from optimisation_util import get_port, alloc_port
import scipy.optimize as spo


     
def alloc_port(alloc, portfolio, sv = 1, sf = 252, rfr = 0.0):
#Reflect price changes based on each stock's portfolio allocation.
        
    #Normalise the prices
    normed_port = normalise_data(port)
    normed_SPY = normalise_data(SPY)

    allocated_port = normed_port*alloc
    
    #How much each stock(col) in the portfolio is worth on each day(row).
    port_posn_values = allocated_port*sv
    
    #Sum across all stocks(cols)to show portfolio's value for each day(row).
    portfolio = port_posn_values.sum(axis = 1)
    
    #Calculate the daily returns of the portfolio
    daily_returns = compute_daily_returns(portfolio)
    
    #Delete the first row which is zero
    daily_returns = daily_returns[1:]
    
    #Calculate std dev

    sddr = daily_returns.std()
    
    cr = (portfolio[-1]/portfolio[0]) - 1
    adr = daily_returns.mean()
    sddr = daily_returns.std()
    sr = np.sqrt(sf)*(adr - rfr)/sddr
    
    return sr*(1)

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
    
    my_port = get_port(sd, ed, syms)[0]  
    
    constraints = ({'type': 'eq', 'fun': lambda allocs: 1.0 - np.sum(allocs)})
    initial_guess_allocs = [0.25, 0.25, 0.25, 0.25]
    result = spo.minimize(fun = alloc_port, x0 = initial_guess_allocs, 
                            args = (my_port,), method = 'SLSQP', 
                            bounds = [(0.0,1.0), (0.0,1.0), (0.0,1.0), (0.0,1.0)], 
                            constraints=(constraints), options={'disp': True})
    

    return result.x

def test_run():
#---Example1--------------------------------------------------------------
    sd = '2010-01-01'
    ed = '2010-12-31'
    syms = ['GOOG', 'AAPL', 'GLD', 'XOM'] 
    
    print(optimise_portfolio(sd=sd, ed=ed, syms=['AXP', 'HPQ', 'IBM', 'HNZ'], gen_plot=True))
    #[5.38105153e-16, 3.96661695e-01, 6.03338305e-01, -5.42000166e-17]
if __name__ == '__main__':
    test_run()