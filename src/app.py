import json

import dash
from dash import dcc
from dash import html

import pandas as pd
from bar_chart import trace_bar_chart
import preprocess
from sankey import trace_sankey
from bar_chart import trace_bar_chart

#Hardcoded input
port_central = "St. John's"

#Read csv file 
dataframe = pd.read_csv('./data/TRIP.csv')


# REMARQUE: Fait ça dans ton fichier, pas ici :)
# Le drop transforme la dataframe

# Get dataframes for Sankey diagram
# dataframe1, dataframe2 = preprocess.get_sankey_data(dataframe, port_central)

#Call function to trace sankey
# trace_sankey(dataframe1, dataframe2, port_central)

trace_bar_chart(dataframe, "year", "all", "")