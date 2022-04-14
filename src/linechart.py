import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def get_linechart(linechart_data,harbour=None):

    if harbour == None:
        #tous les ports confondus
        df = linechart_data.groupby(["month-day"]).sum().reset_index()
        
        fig = px.line(df, x="month-day", y="Traffic")

        return fig

    if harbour != None:
        
        df = linechart_data[linechart_data["Departure Hardour"]== harbour]
        df = df.groupby(["month-day"]).sum().reset_index()
        
        fig = px.line(df, x="month-day", y="Traffic")

        return fig