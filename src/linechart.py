import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import preprocess


def get_linechart(linechart_data,type, value=None):

    print("get_linechart : ", type, value )
    if type == "All":
        df = linechart_data.groupby(["month-day"]).sum().reset_index()

    if type == "Harbour":
        if value == None:
            #tous les ports confondus
            df = linechart_data.groupby(["month-day"]).sum().reset_index()

        if value != None:
            df = linechart_data[linechart_data["Departure Harbour"]== value]
            df = df.groupby(["month-day"]).sum().reset_index()
    
    if type == "Region":
        
        if value == None:
            #tous les ports confondus
            df = linechart_data.groupby(["month-day"]).sum().reset_index()

        if value != None:
            df = linechart_data[linechart_data["Departure Region"]== value]
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
