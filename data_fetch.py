#Function to read the data

import pandas as pd
from pdf_file import df_to_pdf

def get_data(data):
    df_to_pdf(data, 'output/historical_data.pdf')

def result_data(filename, data):
    df_to_pdf(data, filename)
