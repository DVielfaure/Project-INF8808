import json

import dash
import dash_html_components as html
import dash_core_components as dcc

import pandas as pd
import preprocess
from sankey import trace_sankey

#Hardcoded input
port_central = "St. John's"

#Read csv file 
list_csv = ['Departure Date', 
        'Departure Hardour', 'Departure Region', 
        'Departure Latitude', 'Departure Longitude', 
        'Arrival Date', 'Arrival Hardour', 
        'Arrival Region', 'Arrival Latitude', 
        'Arrival Longitude', 'Vessel Type', 
        'Lenght', 'Width', 
        'DeadWeight Tonnage', 'Maximum Draugth']

#Initial dataframe
dataframe = pd.read_csv('./data/Id.csv')

#Combine dataframes
for file in list_csv:
    file_name = "data/" + file + ".csv"
    dataframe_temporary = pd.read_csv(file_name)
    dataframe = dataframe.join(dataframe_temporary)


#Get dataframes for Sankey diagram
dataframe1, dataframe2 = preprocess.get_sankey_data(dataframe, port_central)

#Call function to trace sankey
trace_sankey(dataframe1, dataframe2, port_central)



