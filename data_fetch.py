#Function to read the data

import pandas as pd

def get_data(data):
    data.to_csv('output/historical_data.csv', index=False)