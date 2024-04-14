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
from termcolor import colored as cl
from data_fetch import result_data
from wordconvert import result_word

def implement_strategy(dataframe, investment, output_file, output_file1):
  
    in_position = False
    equity = investment
    
    for i in range(3, len(dataframe)):
        if dataframe['high'][i] == dataframe['dcu'][i] and in_position == False:
            no_of_shares = math.floor(equity/dataframe.close[i])
            equity -= (no_of_shares * dataframe.close[i])
            in_position = True
            print(cl('BUY: ', color = 'green', attrs = ['bold']), f'{no_of_shares} Shares are bought at ${dataframe.close[i]} on {str(dataframe.index[i])[:10]}')
        elif dataframe['low'][i] == dataframe['dcl'][i] and in_position == True:
            equity += (no_of_shares * dataframe.close[i])
            in_position = False
            print(cl('SELL: ', color = 'red', attrs = ['bold']), f'{no_of_shares} Shares are bought at ${dataframe.close[i]} on {str(dataframe.index[i])[:10]}')
    if in_position == True:
        equity += (no_of_shares * dataframe.close[i])
        print(cl(f'\nClosing position at {dataframe.close[i]} on {str(dataframe.index[i])[:10]}', attrs = ['bold']))
        in_position = False

    earning = round(equity - investment, 2)
    roi = round(earning / investment * 100, 2)
    print(cl(f'EARNING: ${earning} ; ROI: {roi}%', attrs = ['bold']))

    # Save results to a CSV file
    results_df = pd.DataFrame({'Earnings': [earning], 'ROI': [roi]})
    result_data(output_file,results_df)

    # Save results to a Word file with formatting
    result_word(results_df, output_file1)
    print("Results saved to", output_file)