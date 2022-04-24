'''
    Contains the functions to set up the map visualization.

'''

#from turtle import width, window_height, window_width
# from attr import dataclass
import plotly.graph_objects as go
import plotly.express as px



def get_map(data,lim=0, lat=64.1446450744138, lon=-93.05198935160519, zoom=1.7852661802888283):
    """
    Create the map figure Departure traffic.

        Args:
            data: data of harbour traffic filter on "Arrival" or "Departure"
            lim: minimal number of traffic for each harbour to be shown
            
        Returns:
            fig: The updated figure 
    
    """
    #filtre des données sur la limite de traffic
    data = data[data["Trafic"]>=lim]
    
    #création de la figure "Departure" or "Arrival"
    fig = px.scatter_mapbox(
        data,
        lat="Departure Latitude",
        lon="Departure Longitude",
        text= "Departure Harbour",
        #color=data["Departure Region"]
        color=data["Trafic"],
        #color=["rgb(255,127,80)" if x > 5000 else "rgb(13,8,135)" for x in data["Trafic"]],
    
    )

    fig.update_coloraxes(showscale=False)

    fig.update_traces(marker=dict(size=9))

    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_center=go.layout.mapbox.Center(
            lat=lat,
            lon=lon
        ),
        mapbox_zoom = zoom,
        uirevision = 'something',
        showlegend=False
    )
            
    #faire en sorte qu'il n'y ait pas de superposition de points

    return fig




def get_barchart(data,lim=0):

    data_graph = data[data["Trafic"]>lim]
    data_graph = data_graph.sort_values("Trafic", ascending=True)

    fig = go.Figure(
        data=[go.Bar(
            x=data_graph["Trafic"],
            y= data_graph["Departure Harbour"],
            orientation="h",
            #width=5,
            base="overlay",
            marker_color = "rgb(13,8,135)"
          )]
        )

    fig.update_layout(
        bargap=0.5,
        # width=300,
        #height=400,
        margin={"r": 0, "t": 20, "l": 200, "b": 0, "pad":4 , "autoexpand":True},

        xaxis_anchor="free",
        xaxis_position=1,
        yaxis_automargin=True,
        xaxis_autorange=True,
        plot_bgcolor= "rgba(0, 0, 0, 0)",
        
    
    )

    fig.update_traces(
        hovertemplate=
            "Traffic : %{x}"
            + "<extra></extra>"
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightblue')

    return fig
