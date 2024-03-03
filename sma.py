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


to_word(aapl,'output/historical_data.docx') # if want to get more data please consider changing the code so as to convert to a text file else the code will be slow to run
get_data(aapl) 

 #The dataframe is converted to a Word document using the to_word function
#Convert the dataframe to a table
# doc = Document()

# table = doc.add_table(rows=1, cols=len(aapl.columns))
# for i, column in enumerate(aapl.columns):
#     table.cell(0, i).text = column

# for _, row in aapl.iterrows():
#     row_cells = table.add_row().cells
#     for i, value in enumerate(row):
#         row_cells[i].text = str(value)

# # Save the document as a Word file
# doc.save('output/historical_data.docx') # if want to get more data please consider changing the code so as to convert to a text file else the code will be slow to run

# Calculate the 50-week high and the 40-week low using donchian channels


