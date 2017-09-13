"""01-06 Histograms and scatter plots."""

from util import get_data, plot_data

#-----------test run------------------------------------------
def test_run():
    #Read the data into a dataframe
    dates = pd.date_range('2009-01-01', '2012-12-31')
    symbols = ['SPY', 'XOM', 'GLD']
    df = get_data(symbols, dates)
    
    #Plot the dataframe data
    plot_data(df)
    
    #Compute and plot daily returns
    daily_returns = compute_daily_returns(df)
    #plot_data(daily_returns, title = 'Daily returns', ylabel = 'Daily returns')

    #Scatterplot SPY vs XOM
    daily_returns.plot(kind = 'scatter', x = 'SPY', y = 'XOM')
    #using numpy return alpha and beta of a polynomial of degree 1.
    beta_XOM, alpha_XOM = np.polyfit(daily_returns['SPY'], daily_returns['XOM'], 1)
    print('beta_XOM(slope of the line): ' + str(beta_XOM))
    print('alpha_XOM(intercept of the lines): ' + str(alpha_XOM))
    #plot the line using the values calculated above.
    plt.plot(daily_returns['SPY'], beta_XOM*daily_returns['SPY'] + alpha_XOM, 
             '-', color = 'r')
    plt.show()
    
    #Scatterplot SPY vs GLD
    daily_returns.plot(kind = 'scatter', x = 'SPY', y = 'GLD')
    beta_GLD, alpha_GLD = np.polyfit(daily_returns['SPY'], daily_returns['GLD'], 1)
    print('beta_GLD(slope of the line): ' + str(beta_GLD))
    print('alpha_GLD(intercept of the lines): ' + str(alpha_GLD))
    #plot the line using the values calculated above.
    plt.plot(daily_returns['SPY'], beta_GLD*daily_returns['SPY'] + alpha_GLD, 
             '-', color = 'r')
    plt.show()
    
    #Calculate correlation coefficient
    print('Pearson corr. coeff. of daily returns:')
    print(str(daily_returns.corr(method = 'pearson')))
    
    '''
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
    '''


    
#-----------run------------------------------------------------
if __name__ == '__main__':
    test_run()