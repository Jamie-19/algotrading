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

    for i in range(3, len(dataframe)):
        if dataframe['high'][i] == dataframe['dcu'][i] and not in_position:
            no_of_shares = math.floor(equity / dataframe.close[i])
            equity -= (no_of_shares * dataframe.close[i])
            in_position = True
            signals.append((str(dataframe.index[i])[:10], 'BUY', no_of_shares, dataframe.close[i]))
        elif dataframe['low'][i] == dataframe['dcl'][i] and in_position:
            equity += (no_of_shares * dataframe.close[i])
            in_position = False
            signals.append((str(dataframe.index[i])[:10], 'SELL', no_of_shares, dataframe.close[i]))

    # If still in position at the end
    if in_position:
        equity += (no_of_shares * dataframe.close[i])
        signals.append((str(dataframe.index[i])[:10], 'CLOSE', no_of_shares, dataframe.close[i]))

    earning = round(equity - investment, 2)
    roi = round(earning / investment * 100, 2)
    print(f'EARNING: ${earning} ; ROI: {roi}%')

    # Save results to a CSV file
    results_df = pd.DataFrame(signals, columns=['Date', 'Action', 'Shares', 'Price'])
    result_data(output_file, results_df)

    # Save results to a Word file with formatting
    result_word(results_df, output_file1)

    print("Results saved to", output_file, "and", output_file1)
