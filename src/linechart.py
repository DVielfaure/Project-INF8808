import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import preprocess


def get_linechart(linechart_data):
    
    fig = px.bar(linechart_data, x="Month", y="Traffic")
    fig.update_layout(
        title="Traffic over the year",
        title_x=0.5,
        margin=dict(l=14, r=14, t=32, b=14, pad=0),
        xaxis_title=None,
        yaxis_title=None,
        #xaxis_range=["January","December"]
    )

    #fig.update_traces(line=dict(color='rgb(13,8,135)',width= 2))
    fig.update_traces(marker_color='rgb(13,8,135)')
    

    return fig
