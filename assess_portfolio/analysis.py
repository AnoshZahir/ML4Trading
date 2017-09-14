import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from util import get_data, normalise_data, compute_daily_returns

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
    SPY = df.loc[:, syms[0]]
    
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
    
    if gen_plot == True:
         ax = portfolio.plot(title = 'Daily portfolio value and SPY', 
                             fontsize = 2, label = 'Portfolio')
         normed_SPY.plot(label = 'SPY')
         ax.set_xlabel('Date')
         ax.set_ylabel('Normalised price')
         plt.legend(loc = 'upper left')
         plt.show()

    return cr, adr, sddr, sr

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
