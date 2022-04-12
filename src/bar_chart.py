import plotly.express as px


def trace_bar_chart(df):

    fig = px.bar(df, x="Date", y="Traffic", color="Vessel Type", title="Evolution du traffic du port")
    
    return fig