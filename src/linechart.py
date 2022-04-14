import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def get_linechart(linechart_data,harbour=None):

    if harbour == None:
        #tous les ports confondus
        df = linechart_data.groupby(["month-day"]).sum().reset_index()


    if harbour != None:
        df = linechart_data[linechart_data["Departure Hardour"]== harbour]
        df = df.groupby(["month-day"]).sum().reset_index()
        

    fig = px.line(df, x="month-day", y="Traffic")
    fig.update_layout(
        title="Évolution du traffic sur l'année",
        title_x=0.5,
        margin=dict(l=0, r=0, t=26, b=0, pad=0)
    )

    return fig
