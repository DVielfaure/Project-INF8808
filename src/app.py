
# -*- coding: utf-8 -*-


import json
from pydoc import classname
from tarfile import FIFOTYPE
import time
from zipfile import ZIP_MAX_COMMENT
import dash

import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output, State
#from matplotlib.pyplot import bar, figure
from dash.exceptions import PreventUpdate

import plotly.graph_objects as go

import preprocess 
import map_viz
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px

import sankey
import bar_chart
import boxplot
import linechart

import pickle

app = dash.Dash(__name__, prevent_initial_callbacks=True)
app.title = 'Projet Xperts Solutions'

#Hardcoded input
port_central = "Ports du Canada" #"St. John's"

#Read csv and create dataframe
start = time.time()
data = preprocess.create_dataframe_from_csv()
# pickle.dump(data, open("data.p", "wb"))
# data = pickle.load(open("data.p", "rb"))

#print("first data", time.time() - start)

map_data_departure = preprocess.get_map_data(data,"Departure")
barchart_data = preprocess.get_barchart_data(map_data_departure,"Departure")
linechart_data = preprocess.get_linechart_data(data)
# linechart_data = pickle.load(open("linechart-data.p", "rb"))
sankey_data = preprocess.get_sankey_data(data, port_central)
# sankey_data = pickle.load(open("sankey-data.p", "rb"))
bar_traffic_data = preprocess.get_bar_traffic_data(data, time_scale="year", spatial_scale="all", place="")
# bar_traffic_data = pickle.load(open("bar-traffic-data.p", "rb"))
boxplot_data = data.drop_duplicates(subset = ["Id"])


#figures

zoom_init = {'geo.projection.rotation.lon': -92.46259526553834, 'geo.center.lon': -92.46259526553834, 'geo.center.lat': 54.75637743691583, 'geo.projection.scale':3.4822022531844983}

fig_map = map_viz.get_map(map_data_departure,100)

fig_bar = map_viz.get_barchart(barchart_data,100)

fig_bar_traffic = bar_chart.trace_bar_chart(bar_traffic_data, "all")

fig_boxplot = boxplot.trace_boxplot(boxplot_data)

fig_sankey = sankey.trace_sankey(sankey_data[0], sankey_data[1], port_central)

fig_linechart = linechart.get_linechart(linechart_data)


def transform_value(value):
    return 10 ** value


app.layout = \
html.Div([
    # html.Div([
    #     html.P("Loading"),
    #     html.Div([
    #         html.Div(className="loading-bar")
    #     ], className="loading-container"),
    # ], className="fullpage-container"),

    html.Div([
        html.Div([
            html.H2('Trafic maritime', className="titre"),
            html.Div("par Xperts Solutions Technologies"),
        ], className="grow-1"),
        html.H2("Tous les ports",id='selection', className="titre center grow-3"),
    ], className="card m-1 mb-0 d-flex center-items"),

    html.Div([ # container
        html.Div([ # left side

            html.Div([ # dropdown row
                html.Div([dcc.Dropdown(
                    id="region_dropdown",
                    options=[{'label':x, 'value': x} for x in barchart_data["Departure Region"].unique()],
                    placeholder="Region",
                )], className="grow-1"),
                
                html.Div([dcc.Dropdown(
                    id="harbour_dropdown",
                    options=[{'label':x.casefold().title(), 'value': x} for x in barchart_data["Departure Hardour"].unique()],
                    placeholder="Harbour",
                )], className="grow-1"),
                
            ], className="d-flex"),

            html.Div([dcc.Graph(
                id="barchart",
                figure= fig_bar,
            )], className="trafic-port"),

            dcc.Graph(
                figure=fig_map,
                id='map_departure',
                style={'height':'fit-content','width' : '100%'}
            ),
            
            html.H4(
                "Ports", 
                id='slider_limit_text',
                className="m-1 center"
            ),

            dcc.Slider(
                min=0, 
                max=4, 
                step=0.01,
                id='slider_updatemode',
                marks={i: '{}'.format(10 ** i) for i in range(5)},
                value=2,
                verticalHeight=32,
            ),

        ], className="d-flex flex-column grow-1 card"),
        
        html.Div([ # rigth side
            html.Div([
                dcc.Graph(id="sankey",figure=fig_sankey, className="grow-1 card"),
                dcc.Graph(id="bar_chart_traffic", figure=fig_bar_traffic, className="grow-1 card"),
            ], className="d-flex grow-1"),

            html.Div([
                dcc.Graph(id='linechart', figure=fig_linechart, className="grow-1 card"),
                dcc.Graph(id="boxplot", figure=fig_boxplot, className="grow-2 card"),

            ], className="d-flex grow-1"),

        ], className="d-flex flex-column grow-3"),

    ], className="d-flex grow-1 m-1 mt-0"),

    dcc.Store(id="store_prev_zoom",data = zoom_init['geo.projection.scale'], storage_type='memory'),
    dcc.Store(id="selection_data",data = {"type":"All","value":"All","slider":100}, storage_type='memory')

], className="d-flex flex-column content")


#https://www.somesolvedproblems.com/2021/08/how-to-add-vertical-scrollbar-to-plotly.html
#https://community.plotly.com/t/how-to-add-vertical-scroll-bar-on-horizontal-bar-chart/12342


##### CALLBACKS #####


#update selection 
@app.callback(Output('selection_data','data'),
             [Input('slider_updatemode', 'value'),
              Input('region_dropdown','value'),
              Input('harbour_dropdown','value')],
              [State('selection_data','data')])
def update_selection(slider_value, region_value, harbour_value,selection):

        ctx = dash.callback_context
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]

        #si le slider est utilisé
        if input_id == "slider_updatemode":
            selection["slider"] = int(10**slider_value)

        #si un port est sélectionné
        if input_id == "harbour_dropdown":
            selection["type"] = "Harbour"
            selection["value"] = harbour_value
            selection["slider"] = 100

        #si region sélectionnée
        if input_id == "region_dropdown":
            selection["type"] = "Region"
            selection["value"] = region_value

        #si rien de sélectionné

        if selection["value"] == None:
            selection["type"] = "All"

        print(selection)
        return selection


#affichage texte de la sélection (region, port ou all (Canada)) 
@app.callback(Output('selection','children'),
            [Input('selection_data','data')])
def affichage_selection(selection_data):

    if selection_data["type"] == "Region": 
        return "Ports de la region:  "+ selection_data["value"]

    if selection_data["type"] == "Harbour":
        port_central = selection_data["value"]
        return "Port "+  selection_data["value"].casefold().title()
    
    if selection_data["type"] == "All":
        return "Tous les ports du Canada"


#update viz lorsque selection change
@app.callback([Output('boxplot', 'figure'),
            Output('sankey','figure'),
            Output('bar_chart_traffic','figure'),
            Output('linechart','figure')],
            [Input('selection_data','data')])
def update_viz(selection_data):
    print(selection_data["slider"])
    
    if selection_data["type"] == "Region":
        
        fig__boxplot = boxplot.update_traces_boxplot(data, fig_boxplot, selection_data["value"], None)

        return fig__boxplot, dash.no_update, dash.no_update, dash.no_update

    if selection_data["type"] == "Harbour":
        
        fig__boxplot = boxplot.update_traces_boxplot(data, fig_boxplot, None, selection_data["value"])

        sankey_data = preprocess.get_sankey_data(data,selection_data["value"])
        fig__sankey = sankey.trace_sankey(sankey_data[0],sankey_data[1],selection_data["value"])

        bar_traffic_data = preprocess.get_bar_traffic_data(data, time_scale="year", spatial_scale="harbour", place=selection_data["value"])
        fig__bar_traffic = bar_chart.trace_bar_chart(bar_traffic_data, selection_data["value"])

        fig__linechart = linechart.get_linechart(linechart_data, selection_data["value"])

        return fig__boxplot, fig__sankey, fig__bar_traffic, fig__linechart
    
    if selection_data["type"] == "All":

        fig__boxplot = boxplot.update_traces_boxplot(boxplot_data, fig_boxplot, None, None)

        fig__linechart = linechart.get_linechart(linechart_data)

        return fig__boxplot, dash.no_update, dash.no_update, fig__linechart


### callback pour la map

#conserver la valeur du précédent zoom dans prev_zoom_h4
@app.callback(Output('store_prev_zoom', 'data'),
              [Input('map_departure', 'relayoutData')]
              )
def update_zoom(relayoutData):
    print("update_zoom",relayoutData)
    if relayoutData != None and relayoutData != {'autosize': True}:
        if 'geo.projection.scale' in relayoutData.keys():
            return(relayoutData['geo.projection.scale'])
        else:
            raise PreventUpdate
    else:
        return zoom_init['geo.projection.scale']



zooms = {
    'Central Region': {
        'lon': -85.70231819775765, 
        'lat': 44.96680548384988, 
        'scale':24.25146506416641
    }, 
    'Newfoundland Region': {
        'lon': -54.85859988413813, 
        'lat': 51.81629585581253,
        'scale':10.556063286183166
    },
    'East Canadian Water Region': {
        'lon': -95.13396524228548, 
        'lat': 73.25566470759851,
        'scale': 4.000000000000003
    }, 
    'Maritimes Region': {
        'lon': -63.1261460700024, 
        'lat': 44.8202886873768,
        'scale': 32.00000000000006
    },
    'St. Lawrence Seaway Region': {
        'lon': -77.30560743930843, 
        'lat': 44.01540087191435, 
        'scale': 36.75834735990517
    }, 
    'Quebec Region': {
        'lon': -65.68478238605977, 
        'lat': 48.94642841990159,
        'scale': 21.112126572366343
    }, 
    'Pacific Region': {
        'lon': -127.36955114924267, 
        'lat': 51.378282668463775,
        'scale': 27.857618025476015
    },
    'West Canadian Water Region': {
        'lon': -95.13396524228548, 
        'lat': 73.25566470759851,
        'scale': 4.000000000000003
    }, 
    'Arctic Region': {
        'lon': -95.13396524228548, 
        'lat': 73.25566470759851,
        'scale': 4.000000000000003
    }
}
       

@app.callback([Output('slider_limit_text', 'children'),
                Output('map_departure','figure')],
              [Input('slider_updatemode', 'value'),
              Input('region_dropdown','value'),
              Input('harbour_dropdown','value')],
              [State('map_departure', 'relayoutData'),
                State('store_prev_zoom','data'),
                State('map_departure','figure')])
def update_map(slider_value,region_dropdown, harbour_dropdown,relayoutData,prev_zoom,figure):
    
    print("on est dans update_map")

    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    print(input_id)
    
    # #si le slider est utilisé
    # if input_id == "slider_updatemode":
    #     print("update map",relayoutData)
    #     #évite que le zoom inital ne se perde au chargement
    #         #si pas de région de sélectionnée, on update la map avec les ports au dessus de la limite et le même zoom
    #     if relayoutData != None and region_dropdown == None:
    #         fig = map_viz.get_map(map_data_departure,int(10**slider_value),relayoutData,prev_zoom)
    #         #si il y a une région de sélectionnée, on update la map avec les ports au dessus de la limite et le zoom de la région
    #     elif relayoutData != None and region_dropdown != None:
    #         fig = map_viz.get_map(map_data_departure,int(10**slider_value),zooms[region_dropdown],prev_zoom)
    #     else : #cas où relayoutData= None, à l'initialisation par exemple
    #         fig = map_viz.get_map(map_data_departure, int(10**slider_value))
    #     return "Ports avec plus de {0} bateaux en trafic".format(int(transform_value(slider_value))), fig
    

    if input_id == "slider_updatemode":

        if harbour_dropdown != None: 
            harbour_data = map_data_departure[map_data_departure["Departure Hardour"]==harbour_dropdown]

            lat = harbour_data.iloc[0]["Departure Latitude"]
            lon = harbour_data.iloc[0]["Departure Longitude"]

            figure = map_viz.get_map(map_data_departure,lim= int(10**slider_value),lat=lat, lon= lon, zoom=7)
        
        elif region_dropdown != None and harbour_dropdown == None :
            zoom = zooms[region_dropdown]
            figure = map_viz.get_map(map_data_departure,lim= int(10**slider_value), lat=zoom["lat"], lon= zoom['lon'],zoom = 3)
        
        elif region_dropdown == None and harbour_dropdown == None :

            figure = map_viz.get_map(map_data_departure,lim= int(10**slider_value))
        
        return "Ports avec plus de {0} bateaux en trafic".format(int(transform_value(slider_value))), figure


    #si une region est sélectionnée
    if input_id == "region_dropdown":
        print("region_dropdown")
        if region_dropdown != None:
            zoom = zooms[region_dropdown]
            figure = map_viz.get_map(map_data_departure,lim= int(10**slider_value), lat=zoom["lat"], lon= zoom['lon'],zoom = 3)
            return dash.no_update, figure

        else:
            figure = map_viz.get_map(map_data_departure,lim= int(10**slider_value))

            return "Ports avec plus de {0} bateaux en trafic".format(int(transform_value(slider_value))), figure
   
    #si un port est sélectionné
    ##centre la carte sur le port sélectionné + TODO mise en couleur/augmentation taille
    if input_id == "harbour_dropdown":
        print("update zoom port")
        if harbour_dropdown != None:

            harbour_data = map_data_departure[map_data_departure["Departure Hardour"]==harbour_dropdown]

            lat = harbour_data.iloc[0]["Departure Latitude"]
            lon = harbour_data.iloc[0]["Departure Longitude"]

            figure = map_viz.get_map(map_data_departure,lim= int(10**slider_value),lat=lat, lon= lon, zoom=7)

        else: 
            figure = map_viz.get_map(map_data_departure,lim= int(10**slider_value), zoom = 7)

        return dash.no_update, figure

    # else:

    #     figure = map_viz.get_map(map_data_departure,lim= int(10**slider_value), zoom = 7)

    #     return "Ports avec plus de {0} bateaux en trafic".format(int(transform_value(slider_value))), figure


#filtre du bar chart sur les ports de la région sélectionnée
@app.callback([Output("barchart","figure"),
                Output("barchart",'style')],
            [Input('region_dropdown','value'),
            Input('slider_updatemode','value')
            #,Input('map_chart','relayoutData')
            ])
def update_barchart(region_dropdown,slider_value):

    #clear value du dropdown

    #s'il y a une région de sélectionnée
    if region_dropdown != None:

        filtered_data = barchart_data[barchart_data["Departure Region"]==region_dropdown]
        fig = map_viz.get_barchart(filtered_data,"Departure",lim=int(10**slider_value))

        style={'height':max(25*(len(fig.data[0]['y'])),200)}

        return fig, style

    #pas de région de sélectionnée, filtre selon les ports affichés
    else:

        fig = map_viz.get_barchart(barchart_data,"Departure",lim=int(10**slider_value))

        style={'height':max(25*(len(fig.data[0]['y'])),200)}

        return fig, style


#filtre les valeurs du dropdown des ports si une région est sélectionnée 
@app.callback(Output('harbour_dropdown','options'),
                [Input('region_dropdown', 'value')])
def update_dropdown_harbour(region_value):

    if region_value == None:
        options = [{'label':x.casefold().title(), 'value': x} for x in barchart_data["Departure Hardour"].unique()]
    else:
        options = [{'label':x.casefold().title(), 'value': x} for x in barchart_data[barchart_data["Departure Region"]==region_value]["Departure Hardour"].unique()]

    return options