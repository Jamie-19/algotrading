#Implementing trading strategy

'''
The implement_strategy function is used to implement the trading strategy using the donchian channels.
The function takes two parameters: aapl and investment.
The aapl parameter is a pandas dataframe containing the historical data of the stock.
The investment parameter is the amount of money to be invested in the stock.
The function initializes the trading signal to 0 and loops through each row in the historical data.
If the stock's current high exceeds the 50-week high, the function buys the stock.
If the stock's current low falls below the 40-week low, the function sells the stock.
The function calculates the earnings and return on investment (ROI) of the trading strategy.
The function prints the buy and sell signals along with the earnings and ROI.

Parameters:
aapl (pandas dataframe): Historical data of the stock.
investment (float): Amount of money to be invested in the stock.
'''

import pandas as pd
import math
from termcolor import colored as cl
from data_fetch import result_data
from wordconvert import result_word

def implement_strategy(csv_file, investment, output_file, output_file1):
    aapl = pd.read_csv(csv_file)
    aapl['dcu'] = aapl['high'].rolling(window=20).max()
    aapl['dcl'] = aapl['low'].rolling(window=10).min()

    in_position = False
    equity = investment
    results = []

    for i in range(3, len(aapl)): 
        if aapl['high'].iloc[i] == aapl['dcu'].iloc[i] and not in_position:
            no_of_shares = math.floor(equity / aapl.close.iloc[i]) 
            equity -= (no_of_shares * aapl.close.iloc[i]) 
            in_position = True
            results.append((aapl.index[i], 'BUY', no_of_shares, aapl.close.iloc[i], 'green'))  # Color green for BUY
        elif aapl['low'].iloc[i] == aapl['dcl'].iloc[i] and in_position:
            equity += (no_of_shares * aapl.close.iloc[i])
            in_position = False
            results.append((aapl.index[i], 'SELL', no_of_shares, aapl.close.iloc[i], 'red'))  # Color red for SELL

    if in_position:
        equity += (no_of_shares * aapl.close.iloc[i])
        results.append((aapl.index[i], 'CLOSE', no_of_shares, aapl.close.iloc[i], 'red' if earning < 0 else 'green'))  # Color red if earning is negative, else green
        in_position = False

    earning = round(equity - investment, 2)
    roi = round(earning / investment * 100, 2)
    results.append(('EARNING:', earning, 'ROI:', roi, 'red' if roi < 0 else 'green'))  # Color red if ROI is negative, else green

    # Save results to CSV file
    results_df = pd.DataFrame(results, columns=['Date', 'Action', 'Shares', 'Price', 'Color'])
    result_data(results_df)

    # Save results to Word file
    result_word(results_df, output_file1)