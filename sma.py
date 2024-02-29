#develop a trading strategy using tBefore moving to the coding part, 
#it’s essential to have a good background on the strategy we’re going to build in this article. 
#Our trading strategy follows the principle of simplicity yet a very effective breakout strategy.
#We enter the market if: the stock’s current high exceeds the 50-week high
#We exit the market if: the stock’s current low sinks below the 40-week low
#We’ll be using the Donchian Channel indicator in order to keep track of the 50-week high and the 40-week low. This strategy is a weekly trading system, so, we’ll be backtesting it on the weekly timeframe.


# Import the libraries
import pandas as pd
import requests
import pandas_ta as ta
import matplotlib.pyplot as plt
from termcolor import colored as cl
import math

# Load the data
plt.rcParams['figure.figsize'] = (20, 10)
plt.style.use('fivethrityeight')

# Get the data
#Extract the historical data using Benzinga API




def get_historical_data(symbol,start_date,interval):

#The get_historical_data function is used to extract the historical data of a stock.
#The function takes three parameters: symbol, start_date, and interval.
#The symbol parameter is the stock ticker of the company whose historical data we want to extract.
#The start_date parameter is the date from which we want to extract the historical data.
#The interval parameter is the frequency of the data we want to extract. The frequency can be daily, weekly, or monthly.
#The function returns a pandas dataframe containing the historical data of the stock.
#The historical data contains the open, high, low, close, and volume of the stock for each day, week, or month, depending on the interval parameter.
    
    url=f"https://api.benzinga.com/api/v2/bars" #The URL of the API endpoint
    querstring={"token":"ff9b415f27594cb7becd93e108504055","symbols":f"{symbol}","from":f"{start_date}","interval":f"{interval}"} #The query string containing the parameters of the request
    hist_json=requests.get(url,params=querstring).json() #The response of the request is converted to a JSON object
    df = pd.DataFrame(hist_json[0]['candles']) #The JSON object is converted to a pandas dataframe

    return df #The dataframe is returned

#taking an example of apple's stock here
symbol = 'AAPL'
start_date = '1993-01-01'
interval = '1W'
aapl = get_historical_data(symbol,start_date,interval)
aapl.tail()
