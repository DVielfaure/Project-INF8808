import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import preprocess


def get_linechart(linechart_data):
    
    fig = px.line(linechart_data, x="month-day", y="Traffic")
    fig.update_layout(
        title="Périodes d'achalandage",
        title_x=0.5,
        margin=dict(l=14, r=14, t=32, b=14, pad=0),
        xaxis_title=None,
        yaxis_title=None        
    )

    fig.update_traces(line=dict(color='rgb(13,8,135)',width= 2))

    

    return fig
