import json

import dash
import dash_html_components as html
import dash_core_components as dcc

import pandas as pd
import preprocess

#Hardcoded input
port_central = "St. John's"

#Read csv file 
dataframe = pd.read_csv('./data/TRIP.csv')

#Get dataframes for Sankey diagram
dataframe1, dataframe2 = preprocess.get_sankey_data(dataframe, port_central)

