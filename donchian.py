''' 
Our trading strategy follows the principle of simplicity yet a very effective breakout strategy.
We enter the market if: the stock's current high exceeds the 50-week high
We exit the market if: the stock's current low sinks below the 40-week low
We'll be using the Donchian Channel indicator in order to keep track of the 50-week high and the 40-week low. 
This strategy is a weekly trading system, so, we'll be backtesting it on the weekly timeframe.
'''

# Import the libraries
import pandas as pd
import os
import requests
import pandas_ta as ta
import matplotlib.pyplot as plt
from termcolor import colored as cl
from docx import Document
from wordconvert import to_word
from data_fetch import get_data
from plot import plot_graph
from strategy import implement_strategy
from dotenv import load_dotenv
from whatsapp_quickstart import send_document,upload_media,send_whatsapp_message,send_message,get_text_message_input
load_dotenv()

token = os.getenv('TOKEN')
print(token)
recepieint_waid = os.getenv('RECIPIENT_WAID')

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
            "token": token,
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
start_date = '2020-01-01' #when changing the start date also consider to change the output file format
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
aapl.index = pd.to_datetime(aapl.index,utc=True)
aapl.tail()

#PLotting the donchian channels
'''
The plot function is used to plot the stock's price along with the donchian channels.
The function takes a pandas dataframe containing the stock's price and the donchian channels as input.
The function plots the stock's price along with the donchian channels in a graph format.
The stock's price is plotted as a line graph, and the donchian channels are plotted as dashed lines.
The function also adds a legend to the graph to indicate the stock's price and the donchian channels.
Basically plotting the dcl dcm dcu we got in a graph format for better understanding
'''

plot_graph(aapl,'output/donchian_channels.png')


#Extracting the data in both word and text format
'''
The to_word function is used to convert the historical data of the stock to a word document.
the get_data function is used to convert the historical data of the stock to a text file.
'''
to_word(aapl,'output/historical_data.docx') # if want to get more data please consider changing the code so as to convert to a text file else the code will be slow to run
get_data(aapl)

send_whatsapp_message()
file_path = 'output/historical_data.pdf'
upload_media(file_path)
media_response = upload_media(file_path)
print(media_response)
if 'id' in media_response:
    media_id = media_response['id']
    send_document(media_id,os.getenv('RECIPIENT_WAID')) 


# Implementing the trading strategy
# The function is imported from strategy.py

''' 
The trading strategy is implemented using the following steps:
1. Initialize the trading signal to 0.
2. Loop through each row in the historical data.
3. If the stock's current high exceeds the 50-week high, set the trading signal to 1.
'''

earning,roi=implement_strategy(aapl, 100000, "output/result/result_pdf.pdf","output/result/result_word.docx") #initial investment of 10000 dollars


data = get_text_message_input(
    recipient=os.getenv('RECIPIENT_WAID'), text=f"The earning is : {earning} , The ROI is : {roi}%"
)
send_message(data)

send_whatsapp_message()
file_path = 'output/result/result_pdf.pdf'
upload_media(file_path)
media_response = upload_media(file_path)
print(media_response)
if 'id' in media_response:
    media_id = media_response['id']
send_document(media_id,os.getenv('RECIPIENT_WAID')) 