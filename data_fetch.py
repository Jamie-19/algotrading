#Function to read the data

import pandas as pd

def get_data(data):
    data.to_csv('output/historical_data.csv', index=True)

def result_data(filename,data):
    data.to_csv(filename, index=True)