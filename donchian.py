''' 
Our trading strategy follows the principle of simplicity yet a very effective breakout strategy.
We enter the market if: the stock’s current high exceeds the 50-week high
We exit the market if: the stock’s current low sinks below the 40-week low
We’ll be using the Donchian Channel indicator in order to keep track of the 50-week high and the 40-week low. This strategy is a weekly trading system, so, we’ll be backtesting it on the weekly timeframe.
'''

# Import the libraries
import pandas as pd
import requests
import pandas_ta as ta
import matplotlib.pyplot as plt
from termcolor import colored as cl
import math
from docx import Document
from wordconvert import to_word
from data_fetch import get_data


# Load the data
plt.rcParams['figure.figsize'] = (20, 10)
plt.style.use('fivethirtyeight')

# Get the data
#Extract the historical data using Benzinga API




def get_historical_data(symbol,start_date,interval):

    """
The get_historical_data function is used to extract the historical data of a stock.
The function takes three parameters: symbol, start_date, and interval.
The symbol parameter is the stock ticker of the company whose historical data we want to extract.
The start_date parameter is the date from which we want to extract the historical data.
The interval parameter is the frequency of the data we want to extract. The frequency can be daily, weekly, or monthly.
The function returns a pandas dataframe containing the historical data of the stock.
The historical data contains the open, high, low, close, and volume of the stock for each day, week, or month, depending on the interval parameter.
    """
    
    try:
        url = "https://api.benzinga.com/api/v2/bars"  # The URL of the API endpoint
        querstring = {
            "token": "ff9b415f27594cb7becd93e108504055",
            "symbols": symbol,
            "from": start_date,
            "interval": interval
        }  # The query string containing the parameters of the request
        response = requests.get(url, params=querstring)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            hist_json = response.json()
            df = pd.DataFrame(hist_json[0]['candles'])
            return df  #The dataframe is returned

        else:
            print(f"Error: Failed to fetch data from API. Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return None

#taking the historical data of apple's stock here
symbol = 'AAPL'
start_date = '2022-01-01' #when changing the start date also consider to change the output file format
interval = '1W'
aapl = get_historical_data(symbol,start_date,interval)

# Calculate the 50-week high and the 40-week low using donchian channels

'''
The donchian function is used to calculate the 50-week high and the 40-week low of the stock.
The function takes two parameters: lower_length and upper_length.
The lower_length parameter is the length of the lower band of the donchian channel, which is used to calculate the 40-week low.
The upper_length parameter is the length of the upper band of the donchian channel, which is used to calculate the 50-week high.
The function returns a pandas dataframe containing the 50-week high, the 40-week low, and the 20-week midline of the stock.
The 50-week high is stored in the dcl column, the 40-week low is stored in the dcm column, and the 20-week midline is stored in the dcu column.
'''

aapl[['dcl', 'dcm', 'dcu']] = aapl.ta.donchian(lower_length = 40, upper_length = 50)
aapl = aapl.dropna().drop('time', axis = 1).rename(columns = {'dateTime':'date'})
aapl = aapl.set_index('date')
aapl.index = pd.to_datetime(aapl.index,utc=True).date

aapl.tail()

#PLotting the donchian channels

plt.plot(aapl[-300:].close,label='Close Price',color='blue')
plt.plot(aapl[-300:].dcl,color='black',linestyle='--',alpha=0.3)
plt.plot(aapl[-300:].dcm,color='orange',label='DCM')
plt.plot(aapl[-300:].dcu,color='black',linestyle='--',alpha=0.3,label='DCL,DCU')
plt.legend()
plt.title('AAPL stock price with Donchian Channels')
plt.xlabel('Date')
plt.ylabel('Close')

#Extracting the data in both word and text format
to_word(aapl,'output/historical_data.docx') # if want to get more data please consider changing the code so as to convert to a text file else the code will be slow to run
get_data(aapl) 


