import plotly.express as px


def trace_bar_chart(df, port):
    

    fig = px.bar(df, 
                    x="Date", 
                    y="Traffic", 
                    color="Vessel Type", 
                    hover_data=['Traffic', 'Vessel Type'],
                    title="Evolution du traffic du port", 
                    )
    fig.update_layout( title_text="Evolution du traffic du port " + port, title_x=0.5, font_size=15)
    fig.update_xaxes(range = [2010,2022])

    if port == "all":
         fig.update_layout( title_text="Evolution du trafic du Canada", title_x=0.5, font_size=15)
    
    return fig