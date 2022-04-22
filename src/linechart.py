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
        margin=dict(l=14, r=14, t=32, b=14, pad=0),
        xaxis_title=None,
        yaxis_title=None
        
        
    )

    fig.update_traces(line=dict(color='rgb(13,8,135)',width= 2))

    

    return fig
