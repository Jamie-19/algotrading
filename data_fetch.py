#Function to read the data

import pandas as pd

def get_data(data):
    data.to_csv('output/historical_data.csv', index=True)

def result_data(data):
    data.to_csv('output/result/strategy_results.csv', index=True)