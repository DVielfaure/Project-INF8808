'''
    Contains the functions to set up the map visualization.

'''

#from turtle import width, window_height, window_width
# from attr import dataclass
import plotly.graph_objects as go
import plotly.express as px



def get_map(data,type,lim=0,last_zoom=None,prev_scale=None):
    """
    Create the map figure on "Arrival" or "Departure" trafic.

        Args:
            data: data of harbour trafic filter on "Arrival" or "Departure"
            type: "Arrival" or "Departure" trafic to show
            lim: minimal number of trafic for each harbour to be shown
            last_zoom: parameter data on last zoom apply to the map, we apply it on uptaded figure so the map is not reset on every updates
        Returns:
            fig: The updated figure 
    
    """
    #filtre des données sur la limite de trafic
    data = data[data["Trafic"]>=lim]

    #création de la figure "Departure" or "Arrival"
    fig = px.scatter_mapbox(
        data,
        lat=type+" Latitude",
        lon=type+" Longitude",
        text= type+" Hardour",
        color=data["Trafic"]
    )

    fig.update_coloraxes(showscale=False)


    #conservation des paramètres de zoom précédent 
    # TODO: reste à conserver la taille de la carte, comment la fixer ?
    #https://dash.gallery/dash-uber-rides-demo/

    if last_zoom != None:
        keys = last_zoom.keys()
        if 'geo.projection.rotation.lon' in keys:
            fig.update_geos(
                projection_rotation_lon = float(last_zoom['geo.projection.rotation.lon'])
            )
        if 'geo.projection.rotation.lat' in keys:
            fig.update_geos(
                projection_rotation_lat = float(last_zoom['geo.projection.rotation.lat'])
            )
        if 'geo.projection.rotation.roll' in keys:
            fig.update_geos(
                projection_rotation_roll = float(last_zoom['geo.projection.rotation.roll'])
            )
        if 'geo.projection.scale' in keys:
            fig.update_geos(
                projection_scale = float(last_zoom['geo.projection.scale'])
            )
        else:
            if prev_scale != None:
                fig.update_geos(
                    projection_scale = float(prev_scale)
            )

        if 'geo.center.lon' in keys:
            fig.update_geos(
                center_lon = float(last_zoom['geo.center.lon'])
            )
        if 'geo.center.lat' in keys:
            fig.update_geos(
                center_lat = float(last_zoom['geo.center.lat'])
            )
                 

    fig.update_traces(marker=dict(size=9))

    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_center=go.layout.mapbox.Center(
            lat=48,
            lon=-100
        ),
    )

       
            
    #faire en sorte qu'il n'y ait pas de superposition de points

    return fig




def get_barchart(data,type,lim=0):

    data_graph = data[data["Trafic"]>lim]
    data_graph = data_graph.sort_values("Trafic", ascending=True)

    fig = go.Figure(
        data=[go.Bar(
            x=data_graph["Trafic"],
            y= data_graph[type+" Hardour"],
            orientation="h",
            #width=5,
            base="overlay",
            

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
        xaxis_autorange=True
    
    )


    return fig

"""

 fig = px.bar(data,y=type+" Hardour",x="Trafic",orientation="h")

"""