#Implementing trading strategy

'''
The implement_strategy function is used to implement the trading strategy using the donchian channels.
The function takes two parameters: dataframe and investment.
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
from data_fetch import result_data
from wordconvert import result_word


def implement_strategy(dataframe, investment, output_file, output_file1):
    in_position = False
    equity = investment
    signals = []  # List to store buy and sell signals
    previous_price = None  # Variable to store the previous price

    # Iterate over the index values of the DataFrame
    for i in dataframe.index:
        if dataframe.at[i, 'high'] == dataframe.at[i, 'dcu'] and not in_position:
            no_of_shares = math.floor(equity / dataframe.at[i, 'close'])
            equity -= (no_of_shares * dataframe.at[i, 'close'])
            in_position = True
            signals.append((str(i)[:10], 'BUY', no_of_shares, dataframe.at[i, 'close']))
            previous_price = dataframe.at[i, 'close']  # Set previous price
        elif dataframe.at[i, 'low'] == dataframe.at[i, 'dcl'] and in_position:
            equity += (no_of_shares * dataframe.at[i, 'close'])
            in_position = False
            signals.append((str(i)[:10], 'SELL', no_of_shares, dataframe.at[i, 'close']))
            previous_price = None  # Reset previous price
    # If still in position at the end
    if in_position:
        equity += (no_of_shares * dataframe.at[i, 'close'])
        signals.append((str(i)[:10], 'CLOSE', no_of_shares, dataframe.at[i, 'close']))

    earning = round(equity - investment, 2)
    roi = round(earning / investment * 100, 2)
    print(f'Earnings: ${earning}')
    print(f'Return on Investment: {roi}%')

    # Save results to a CSV file
    results_df = pd.DataFrame(signals, columns=['Date', 'Action', 'Shares', 'Price'])
    result_data(output_file, results_df)

    # Save results to a Word file with formatting
    result_word(results_df, output_file1)

    return earning, roi


