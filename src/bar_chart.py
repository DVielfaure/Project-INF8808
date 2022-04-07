from datetime import datetime as dt
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import preprocess

def trace_bar_chart(df, time_scale, spatial_scale, place):
    
    df = preprocess.correct_data(df)

    df = preprocess.filter_df(df, spatial_scale, place)
    df = preprocess.traffic_per_time(df, time_scale)
    df = df.drop(df.columns[0], axis=1)

    df_counts = df.groupby(['Date', 'Vessel Type']).agg('count').reset_index()

    fig = px.bar(df_counts, x="Date", y="Traffic", color="Vessel Type", title="oui")
    fig.show()