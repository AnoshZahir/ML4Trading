"""01-04 Statistcal analysis of time series"""

from util import symbol_to_path, get_data, plot_data, plot_selected 
from util import normalise_data




def get_rolling_mean(values, window):
    """Return  rolling mean of values with specified rolling window."""
    return pd.rolling_mean(values, window = window)

def get_rolling_std(values, window):
    """Return  rolling standard dev of values with specified rolling window."""
    return pd.rolling_std(values, window = window)

def get_bollinger_bands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    upper_band = rm + 2*rstd
    lower_band = rm - 2*rstd 
    return (upper_band, lower_band)

def compute_daily_returns(df):
    """Return the daily return values."""
    daily_returns = (df/df.shift(1)) - 1
    daily_returns.ix[0,:] = 0 #set daily returns for row 0 to 0
    '''
    Below code uses numpy
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:]/df[:-1].values) - 1
    daily_returns.ix[0,:] = 0 #set daily returns for row 0 to 0
    '''
    return daily_returns

def test_run():
    symbols = ['SPY', 'XOM'] #'GOOG', 'GLD']
    dates = pd.date_range('2012-01-01', '2012-12-31')
    df =  get_data(symbols, dates)
    
    daily_returns = compute_daily_returns(df)
    plot_data(daily_returns, title = 'Daily returns')
    
    '''
    #Compute bollinger bands
    #1. Compute rolling mean
    rm_SPY = get_rolling_mean(df['SPY'], window = 20)
    
    #2. Compute rolling sd
    rstd_SPY = get_rolling_std(df['SPY'], window = 20)
    
    #3. Compute upper and lower bands
    upper_band, lower_band = get_bollinger_bands(rm_SPY, rstd_SPY)
    
    
    #Plot raw SPY data, rolling mean and Bollinger bands
    ax = df['SPY'].plot(title = 'Bollinger Bands', label = 'SPY')
    
    #Add rolling mean to the same plot as SPY plot created above
    rm_SPY.plot(label = 'Rolling mean', ax = ax)
    
    #Add bands to the same plot as SPY plot created above
    upper_band.plot(label = 'upper band', ax = ax)
    lower_band.plot(label = 'lower band', ax = ax)
    
    #Add axis labels and legend
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend(loc = 'upper left')
    plt.show()
    '''
if __name__ == '__main__':
    df = test_run()