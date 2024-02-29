#Function to read the data

import pandas as pd

def get_data():
    data = pd.read_csv('data/data.csv')
    return data