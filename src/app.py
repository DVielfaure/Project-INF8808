
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
from os.path import exists

app = dash.Dash(__name__, prevent_initial_callbacks=True)
app.title = 'Projet Xperts Solutions'

#Read csv and create dataframe

if (not exists("./data.p")):
    data = preprocess.create_dataframe_from_csv()
    pickle.dump(data, open("data.p", "wb"))

data = pickle.load(open("data.p", "rb"))

if (not exists("./map_data_departure.p")):
    map_data_departure = preprocess.get_map_data(data)
    pickle.dump(map_data_departure, open("map_data_departure.p", "wb"))

map_data_departure = pickle.load(open("map_data_departure.p", "rb"))
fig_map = map_viz.get_map(map_data_departure)

if (not exists("./barchart_data.p")):
    barchart_data = preprocess.get_barchart_data(map_data_departure)
    pickle.dump(barchart_data, open("barchart_data.p", "wb"))

barchart_data = pickle.load(open("map_data_departure.p", "rb"))
fig_bar = map_viz.get_barchart(barchart_data,100)


if (not exists("./boxplot_data.p")):
    boxplot_data = data.drop_duplicates(subset = ["Id"])
    pickle.dump(boxplot_data, open("boxplot_data.p", "wb"))

boxplot_data = pickle.load(open("boxplot_data.p", "rb"))
fig_boxplot = boxplot.trace_boxplot(boxplot_data)


if (not exists("./linechart_data.p")):
    linechart_data = preprocess.get_linechart_data(data)
    pickle.dump(linechart_data, open("linechart_data.p", "wb"))

linechart_data = pickle.load(open("linechart_data.p", "rb"))
fig_linechart = linechart.get_linechart(linechart_data)

if (not exists("./bar_traffic_data.p")):
    bar_traffic_data = preprocess.get_bar_traffic_data(data, time_scale="year")
    pickle.dump(bar_traffic_data, open("bar_traffic_data.p", "wb"))

bar_traffic_data = pickle.load(open("bar_traffic_data.p", "rb"))
fig_bar_traffic = bar_chart.trace_bar_chart(bar_traffic_data, "All")

if (not exists("./sankey_data.p")):
    sankey_data = preprocess.get_sankey_data(data, type="All", value= "Ports du Canada")
    pickle.dump(sankey_data, open("sankey_data.p", "wb"))

sankey_data = pickle.load(open("sankey_data.p", "rb"))
fig_sankey = sankey.trace_sankey(sankey_data[0], sankey_data[1], sankey_data[2])


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
                    options=[{'label':x.casefold().title(), 'value': x} for x in barchart_data["Departure Harbour"].unique()],
                    placeholder="Harbour",
                )], className="grow-1"),
                
            ], className="d-flex"),


            html.Div([dcc.Graph(
                id="barchart",
                figure= fig_bar,
                style={'height':max(25*(len(fig_bar.data[0]['y'])),200)}
            )], className="trafic-port"),

            dcc.Graph(
                figure=fig_map,
                id='map_departure',
                style={'height':'fit-content','width' : '100%'}
            ),
            
            html.H4(
                "Ports avec plus de 1 bateaux en trafic", 
                id='slider_limit_text',
                className="m-1 center"
            ),

            dcc.Slider(
                min=0, 
                max=4, 
                step=0.01,
                id='slider_updatemode',
                marks={i: '{}'.format(10 ** i) for i in range(5)},
                value=0,
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

    dcc.Store(id="selection_data",data = {"type":"All","value":"All","slider":100}, storage_type='memory')

], className="d-flex flex-column content")


#https://www.somesolvedproblems.com/2021/08/how-to-add-vertical-scrollbar-to-plotly.html
#https://community.plotly.com/t/how-to-add-vertical-scroll-bar-on-horizontal-bar-chart/12342


##### CALLBACKS #####


#update selection 
@app.callback(Output('selection_data','data'),
             [Input('slider_updatemode', 'value'),
              Input('region_dropdown','value'),
              Input('harbour_dropdown','value'),
              Input('map_departure','clickData'),
              Input("barchart", "clickData")],
              [State('selection_data','data')])
def update_selection(slider_value, region_value, harbour_value, clickData, clickData_bar, selection_data):

        ctx = dash.callback_context
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]

        print("update selection : ")

        #selection sur le bargraph
        if input_id == "barchart":
            print("clickData",clickData_bar)
            if clickData_bar != None:
                
                selection_data["type"] = "Harbour"
                selection_data["value"] = clickData_bar["points"][0]['y']

        #clickData ne fonctionne pas et je ne sais pas pourquoi
        #si on a cliqué sur un port sur le carte
        if input_id == "map_departure":
            print("clickData =",clickData)

            if clickData != None:

                selection_data["type"] = "Harbour"
                selection_data["value"] = clickData["points"][0]['y']


        #si le slider est utilisé
        if input_id == "slider_updatemode":
            selection_data["slider"] = int(10**slider_value)

        #si un port est sélectionné
        if input_id == "harbour_dropdown":
            selection_data["type"] = "Harbour"
            selection_data["value"] = harbour_value
            selection_data["slider"] = 0

        #si region sélectionnée
        if input_id == "region_dropdown":
            selection_data["type"] = "Region"
            selection_data["value"] = region_value

        #si rien de sélectionné
        if selection_data["value"] == None:
            selection_data["type"] = "All"

        print(selection_data)
        return selection_data


#affichage texte de la sélection (region, port ou all (Canada)) 
@app.callback(Output('selection','children'),
            [Input('selection_data','data')])
def affichage_selection(selection_data):

    if selection_data["type"] == "Region": 
        return "Ports de la region:  "+ selection_data["value"]

    if selection_data["type"] == "Harbour":
        
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
    filtered_df = preprocess.filter_df(data, selection_data["type"], selection_data["value"])

    fig__boxplot = draw_boxplot(filtered_df, selection_data["type"])

    linechart_data = preprocess.get_linechart_data(filtered_df)
    fig__linechart = linechart.get_linechart(linechart_data)

    bar_traffic_data = preprocess.get_bar_traffic_data(filtered_df, time_scale="year")
    fig__bar_traffic = bar_chart.trace_bar_chart(bar_traffic_data, selection_data["type"])

    sankey_data = preprocess.get_sankey_data(data, type= selection_data["type"], value=selection_data["value"])
    fig__sankey = sankey.trace_sankey(sankey_data[0],sankey_data[1], sankey_data[2])

    return fig__boxplot, fig__sankey, fig__bar_traffic, fig__linechart


def draw_boxplot(data, selection_type):
    if selection_type == "All":
        return boxplot.update_traces_boxplot(boxplot_data, fig_boxplot)
    
    return boxplot.update_traces_boxplot(data.drop_duplicates(subset = ["Id"]), fig_boxplot)

### callback pour la map

zooms = {
    'Central Region': {
        'lon': -86.03716131691169, 
        'lat':  44.8757690195437, 
        'scale':4.549238272376499
    }, 
    'Newfoundland Region': {
        'lon': -56.86825526312134, 
        'lat': 52.30221689542523,
        'scale': 3.4710642576083917
    },
    'East Canadian Water Region': {
        'lon': -50.60547699495851, 
        'lat': 39.014505666286226,
        'scale': 3.6400346415240223
    }, 
    'Maritimes Region': {
        'lon': -63.21373574246451, 
        'lat': 44.86450606292661,
        'scale': 5.136598326358074
    },
    'St. Lawrence Seaway Region': {
        'lon': -77.29317178943415, 
        'lat': 44.1313321077491, 
        'scale': 5.306299212717266
    }, 
    'Quebec Region': {
        'lon': -66.22551661883136, 
        'lat': 49.04376027084436,
        'scale': 4.397095581864786
    }, 
    'Pacific Region': {
        'lon': -127.64865991705307, 
        'lat': 51.562194852405185,
        'scale': 4.66553406874969
    },
    'West Canadian Water Region': {
        'lon': -135.78570315586165, 
        'lat': 49.20609502785169,
        'scale': 4.228855700392709
    }, 
    'Arctic Region': {
        'lon': -96.25971498970875, 
        'lat': 71.77299208643322,
        'scale': 1.823818887149733
    }
}
       

@app.callback([Output('slider_limit_text', 'children'),
                Output('map_departure','figure')],
              [Input('slider_updatemode', 'value'),
              Input('region_dropdown','value'),
              Input('harbour_dropdown','value'),
               Input("barchart", "clickData")],
              [State('map_departure','figure')])
def update_map(slider_value,region_dropdown, harbour_dropdown, clickData_bar, figure):
    print("zoom =",figure["layout"]["mapbox"]["zoom"])

    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    #si sélection sur le barchart
    if input_id == "barchart":
        print("clickData =",clickData_bar)

        if clickData_bar != None:
            harbour_value = clickData_bar["points"][0]['y']
            harbour_data = map_data_departure[map_data_departure["Departure Harbour"]==harbour_value]
            
            lat = harbour_data.iloc[0]["Departure Latitude"]
            lon = harbour_data.iloc[0]["Departure Longitude"]

            figure = map_viz.get_map(map_data_departure,lim= int(10**slider_value),lat=lat, lon= lon, zoom=8.7)

        return dash.no_update, figure

    #si le slider est modifié
    if input_id == "slider_updatemode":

        if harbour_dropdown != None: 
            harbour_data = map_data_departure[map_data_departure["Departure Harbour"]==harbour_dropdown]

            lat = harbour_data.iloc[0]["Departure Latitude"]
            lon = harbour_data.iloc[0]["Departure Longitude"]
            #pour garder le même zoom
            zoom_prec = figure["layout"]["mapbox"]["zoom"]

            figure = map_viz.get_map(map_data_departure,lim= int(10**slider_value),lat=lat, lon= lon, zoom=zoom_prec)
        
        elif region_dropdown != None and harbour_dropdown == None :
            zoom = zooms[region_dropdown]
            figure = map_viz.get_map(map_data_departure,lim= int(10**slider_value), lat=zoom["lat"], lon= zoom['lon'],zoom = zoom["scale"])
        
        elif region_dropdown == None and harbour_dropdown == None :

            figure = map_viz.get_map(map_data_departure,lim= int(10**slider_value))
        
        return "Ports avec plus de {0} bateaux en trafic".format(int(transform_value(slider_value))), figure


    #si une region est sélectionnée
    if input_id == "region_dropdown":
        print("region_dropdown")
        if region_dropdown != None:
            zoom = zooms[region_dropdown]
            figure = map_viz.get_map(map_data_departure,lim= int(10**slider_value), lat=zoom["lat"], lon= zoom['lon'],zoom = zoom["scale"])
            return dash.no_update, figure

        else:
            figure = map_viz.get_map(map_data_departure,lim= int(10**slider_value))

            return "Ports avec plus de {0} bateaux en trafic".format(int(transform_value(slider_value))), figure
   
    #si un port est sélectionné
    ##centre la carte sur le port sélectionné + TODO mise en couleur/augmentation taille
    if input_id == "harbour_dropdown":
        print("update zoom port")
        if harbour_dropdown != None:

            harbour_data = map_data_departure[map_data_departure["Departure Harbour"]==harbour_dropdown]

            lat = harbour_data.iloc[0]["Departure Latitude"]
            lon = harbour_data.iloc[0]["Departure Longitude"]

            figure = map_viz.get_map(map_data_departure,lim= int(10**slider_value),lat=lat, lon= lon, zoom=8.7)

        else: 
            figure = map_viz.get_map(map_data_departure,lim= int(10**slider_value), zoom = 8.7)

        return dash.no_update, figure

 

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
        fig = map_viz.get_barchart(filtered_data,lim=int(10**slider_value))

        style={'height':max(25*(len(fig.data[0]['y'])),200)}

        return fig, style

    #pas de région de sélectionnée, filtre selon les ports affichés
    else:

        fig = map_viz.get_barchart(barchart_data,lim=int(10**slider_value))

        style={'height':max(25*(len(fig.data[0]['y'])),200)}

        return fig, style


#filtre les valeurs du dropdown des ports si une région est sélectionnée 
@app.callback(Output('harbour_dropdown','options'),
                [Input('region_dropdown', 'value')])
def update_dropdown_harbour(region_value):

    if region_value == None:
        options = [{'label':x.casefold().title(), 'value': x} for x in barchart_data["Departure Harbour"].unique()]
    else:
        options = [{'label':x.casefold().title(), 'value': x} for x in barchart_data[barchart_data["Departure Region"]==region_value]["Departure Harbour"].unique()]

    return options




