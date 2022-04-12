from datetime import datetime as dt
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import preprocess

def trace_bar_chart(df):

    df_counts = df.groupby(['Date', 'Vessel Type']).agg('count').reset_index()

    fig = px.bar(df_counts, x="Date", y="Traffic", color="Vessel Type", title="Evolution du traffic du port")
    
    return fig