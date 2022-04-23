import plotly.express as px


def trace_bar_chart(df, type):
    colors_prism = px.colors.qualitative.Prism
    colors = ['#0b2e88'] + colors_prism[:5] + ['#ffee6f'] + colors_prism[5:8] + ['#d192f0'] + [colors_prism[8]]

    fig = px.bar(
         df, 
         x="Date", 
         y="Traffic", 
         color="Vessel Type", 
         hover_data=['Traffic', 'Vessel Type'],
         title="Evolution du traffic du port",
         color_discrete_sequence=colors
    )
    fig.update_layout(
        title_text="Evolution du traffic",
        title_x=0.5,
        margin=dict(l=14, r=14, t=32, b=14, pad=0),
    )
    fig.update_xaxes(range = [2010,2022])

    if type == "All":
        fig.update_layout(
            title_text="Evolution du trafic au Canada", 
            title_x=0.5,
            margin=dict(l=14, r=14, t=32, b=14, pad=0),
        )
    
    return fig