"""01-06 Histograms and scatter plots."""

from util import get_data, plot_data

#-----------Function to compute daily returns----------------
def compute_daily_returns(df):
    """Compute and return daily return values."""
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:] / df[:-1].values) - 1
    daily_returns.ix[0, :] = 0 # set daily returns for row 0 to 0
    return daily_returns

#-----------test run------------------------------------------
def test_run():
    #Read the data into a dataframe
    dates = pd.date_range('2009-01-01', '2012-12-31')
    symbols = ['SPY', 'XOM']
    df = get_data(symbols, dates)
    
    #Plot the dataframe data
    plot_data(df)
    
    #Compute and plot daily returns
    daily_returns = compute_daily_returns(df)
    plot_data(daily_returns, title = 'Daily returns', ylabel = 'Daily returns')

    #Plot both histograms on the same plot
    daily_returns['SPY'].hist(bins = 20, label = 'SPY')
    daily_returns['XOM'].hist(bins = 20, label = 'XOM')
    plt.legend(loc = 'upper right')
    
    #Get mean, std dev and kurtosis
    mean = daily_returns['SPY'].mean()
    print('mean = ' + str(mean))
    std_dev = daily_returns['SPY'].std()
    print('std_dev = ' + str(std_dev))
    print('kurtosis = ' + str(daily_returns.kurtosis()))
    
    #show the mean value on the plot
    plt.axvline(mean, color = 'w', linestyle = 'dashed', linewidth = 2)
    
    #show the std dev on theplot
    plt.axvline(std_dev, color = 'r', linestyle = 'dashed', linewidth = 2)
    plt.axvline(-std_dev, color = 'r', linestyle = 'dashed', linewidth = 2)
    #plt.show()


    
#-----------run------------------------------------------------
if __name__ == '__main__':
    test_run()