
# -*- coding: utf-8 -*-


import json
from pydoc import classname
from tarfile import FIFOTYPE
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



app = dash.Dash(__name__)
app.title = 'Projet Xperts Solutions'

#Hardcoded input
port_central = "St. John's"

#Read csv and create dataframe
data = preprocess.create_dataframe_from_csv().head(5000)

#données preprocess
map_data_departure = preprocess.get_map_data(data,"Departure")
map_data_arrival = preprocess.get_map_data(data,"Arrival")

barchart_data = preprocess.get_barchart_data(data,"Departure")


#preprocess lineshart
dff=preprocess.traffic_per_time(data, scale="day")
dff = dff.groupby('Date')['Traffic'].sum().reset_index()
dff["Departure Year"] = pd.to_datetime(dff["Date"]).dt.year.astype('str')
years = dff['Departure Year'].drop_duplicates().sort_values().tolist()


# #Get dataframes for Sankey diagram
sankey_data = preprocess.get_sankey_data(data, port_central)

bar_traffic_data = preprocess.get_bar_traffic_data(data, time_scale="year", spatial_scale="all", place="")

# #Call function to trace sankey
fig_sankey = sankey.trace_sankey(sankey_data[0], sankey_data[1], port_central)

#figures

zoom_init = {'geo.projection.rotation.lon': -92.46259526553834, 'geo.center.lon': -92.46259526553834, 'geo.center.lat': 54.75637743691583, 'geo.projection.scale':3.4822022531844983}

fig_departure = map_viz.get_map(map_data_departure,"Departure",100,last_zoom=zoom_init,prev_scale=None)
#fig_arrival = map_viz.get_map(map_data_arrival,"Arrival",0,last_zoom=None,prev_scale=None)

fig_bar = map_viz.get_barchart(barchart_data,"Departure",100)

fig_bar_traffic = bar_chart.trace_bar_chart(bar_traffic_data, "all")

fig_boxplot = boxplot.trace_boxplot(data)


def transform_value(value):
    return 10 ** value

# Le tooltip du slider affiche la valeur non log, apparemment impossible de modifier cette valeur
# tooltip={"placement": "bottom", "always_visible": True})

app.layout = \
html.Div([
    html.H1('Trafic maritime par Xperts Solutions Technologies', className="titre"),
    html.H2("Tous les ports",id='selection', className="titre"),
    html.H4(id='slider_limit_text'),
    html.H4(id='update_relayoutData'),

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
                style={'height':max(4*(len(fig_bar.data[0]['y']) - 14), 100)},
            )], className="trafic-port"),

            html.Div([dcc.Graph(
                figure=fig_departure,
                id='map_departure',
            )], className="h-100"),

            dcc.Slider(
                min=0, 
                max=4, 
                step=0.01,
                id='slider_updatemode',
                marks={i: '{}'.format(10 ** i) for i in range(5)},
                value=2,
                updatemode='drag'
            ),

        ], className="w-40 d-flex flex-column"),
        
        html.Div([ # rigth side

            html.Div([
                dcc.Graph(id="sankey",figure=fig_sankey),
                dcc.Graph(id="bar_chart_traffic", figure=fig_bar_traffic),
            ], className="d-flex h-100"),

            html.Div([
                html.Div([
                    dcc.Dropdown(
                        options=[{'value':year, 'label':year} for year in years], 
                        # value=years[0], 
                        id='year-dropdown',
                        optionHeight=35,                    #height/space between dropdown options
                        disabled=False,                     #disable dropdown value selection
                        multi=False,                        #allow multiple dropdown values to be selected
                        searchable=True,                    #allow user-searching of dropdown values
                        search_value='',                    #remembers the value searched in dropdown
                        placeholder='Selectionnez une année',     #gray, default text shown when no option is selected
                        clearable=True,                     #allow user to removes the selected value
                        # style={'width':"60%", "align":"center"},             #use dictionary to define CSS styles of your dropdown
                    ),
                    
                    dcc.Graph(id='linechart'),
                ], className="w-100"),
                dcc.Graph(id="boxplot", figure=fig_boxplot, className="w-100"),

            ], className="d-flex h-100"),

        ], className="d-flex flex-column"),

    ], className="d-flex space-between grow-1")
], className="h-100 d-flex flex-column")


app.layout2 = \
html.Div([
    html.H1('Trafic maritime par Xperts Solutions Technologies', className="titre"),

        html.Div([
            html.H2("Tous les ports",id='selection', 
            style={
                'margin-top': 0, 
                "margin-left":0,
                "font-family": 'verdana',
                'textAlign': 'center'}),
            html.H4(id='slider_limit_text', style={'margin-top': 20}),
            html.H4(id='update_relayoutData', style={'margin-top': 20}),
            #html.H4(children=zoom_init['geo.projection.scale'],id='prev_zoom_h4', style={'margin-top': 20})
                   
        ]),

        #div row 1
        html.Div([
            
            #div dropdown et barchart
            html.Div([
                #ligne dropdown
                html.Div([
                    #dropdown Region
                    html.Div([ 
                        dcc.Dropdown(
                            id="region_dropdown",
                            options=[
                                {'label':x, 'value': x} for x in barchart_data["Departure Region"].unique()
                            ],
                            placeholder="Region"
                            
                        )
                    ], style={'flex':3, 'margin-right':'1em'}),

                    #dropdown Harbour
                    html.Div([ 
                        dcc.Dropdown(
                            id="harbour_dropdown",
                            options=[
                                {'label':x.casefold().title(), 'value': x} for x in barchart_data["Departure Hardour"].unique()
                            ],
                            placeholder="Harbour"
                        )
                    ], style={'flex':3})
                ], style={'display':'flex', 'justify-content':'space-between'}
                ),

                #ligne barchart
                html.Div([
                    html.Div([ 
                        #html.H3('Column 2'),
                        #gérer la taille du bar chart en fonction du nombre de ligne de la figure (mais il faut sélectionner la bonne)
                        dcc.Graph(id="barchart",figure= fig_bar, style={'height':max(4*(len(fig_bar.data[0]['y'])-14),100)}
                            )]
                            ,style={'max-height':150, 'overflow-y': "scroll", 'position': "relative",'margin-top': 5}        
                    ),
                ])
            ], style = {'margin-bottom':25}),

            #div map et slider
            html.Div([
                dcc.Graph(figure=fig_departure, id='map_departure'),
                dcc.Slider(
                    min=0, 
                    max=4, 
                    step=0.01,
                    id='slider_updatemode',
                    marks={i: '{}'.format(10 ** i) for i in range(5)},
                    value=2,
                    updatemode='drag'
                )
            ])

        ], id='first_row', style={'display':'flex', 'width':'30%','flex-direction':'column'}),
        
        #html.H4(id='coord', style={'margin-top': 20}),

        html.Div([
            html.Div([
                        dcc.Graph(id="sankey",figure=fig_sankey) 
                    ], style={'flex':1}),

            html.Div([
                dcc.Graph(id="bar_chart_traffic", figure=fig_bar_traffic) 
            ], style={'flex':1}),
            
        ], id='second_row', style={'display':'flex', 'width':'100%'}),


        html.Div([
            html.Div([
                        dcc.Dropdown(options=[{'value':year, 'label':year} for year in years], 
                                        # value=years[0], 
                                        id='year-dropdown',
                                        optionHeight=35,                    #height/space between dropdown options
                                        disabled=False,                     #disable dropdown value selection
                                        multi=False,                        #allow multiple dropdown values to be selected
                                        searchable=True,                    #allow user-searching of dropdown values
                                        search_value='',                    #remembers the value searched in dropdown
                                        placeholder='Selectionnez une année',     #gray, default text shown when no option is selected
                                        clearable=True,                     #allow user to removes the selected value
                                        style={'width':"60%",
                                        "align":"center"},             #use dictionary to define CSS styles of your dropdown
                            ),
                        dcc.Graph(id='linechart')
                    ], style={'flex':1}),

            html.Div([
                dcc.Graph(id="boxplot", figure=fig_boxplot)
            ], style={'flex':2})
        ], id='third_row', style={'display':'flex', "width":'100%'}),


    
        dcc.Store(id="store_prev_zoom",data = zoom_init['geo.projection.scale'], storage_type='memory'),
        dcc.Store(id="selection_data",data = {"type":"All","value":"All","slider":100}, storage_type='memory')

       
], id='global', style={'display':'flex', 'align_items':'center', 'flex-direction':'column', 'width':'100%'})

#html.H4(id='slider_limit_text', style={'margin-top': 20}-),
#hidden div , style={‘display’:‘none’}

#https://www.somesolvedproblems.com/2021/08/how-to-add-vertical-scrollbar-to-plotly.html
#https://community.plotly.com/t/how-to-add-vertical-scroll-bar-on-horizontal-bar-chart/12342

'''
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
'''
##### CALLBACKS #####


#update selection et data
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
            Output('bar_chart_traffic','figure')],
            [Input('selection_data','data')])
def update_viz(selection_data):

    if selection_data["type"] == "Region":
        
        fig__boxplot = boxplot.update_traces_boxplot(data, fig_boxplot, selection_data["value"], None)

        return fig__boxplot, dash.no_update, dash.no_update

    if selection_data["type"] == "Harbour":
        
        fig__boxplot = boxplot.update_traces_boxplot(data, fig_boxplot, None, selection_data["value"])

        sankey_data = preprocess.get_sankey_data(data,selection_data["value"])
        fig__sankey = sankey.trace_sankey(sankey_data[0],sankey_data[1],selection_data["value"])

        bar_traffic_data = preprocess.get_bar_traffic_data(data, time_scale="year", spatial_scale="harbour", place=selection_data["value"])
        fig__bar_traffic = bar_chart.trace_bar_chart(bar_traffic_data, selection_data["value"])

        return fig__boxplot, fig__sankey, fig__bar_traffic
    
    if selection_data["type"] == "All":

        fig__boxplot = boxplot.update_traces_boxplot(data, fig_boxplot, None, None)

        return fig__boxplot, dash.no_update, dash.no_update


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


zooms = {'Central Region': {'geo.projection.rotation.lon': -85.70231819775765, 'geo.center.lon': -85.70231819775765, 'geo.center.lat': 44.96680548384988,'geo.projection.scale':24.25146506416641} , 
        'Newfoundland Region':{'geo.projection.rotation.lon': -54.85859988413813, 'geo.center.lon': -54.85859988413813, 'geo.center.lat': 51.81629585581253,'geo.projection.scale':10.556063286183166},
       'East Canadian Water Region': {'geo.projection.rotation.lon': -95.13396524228548, 'geo.center.lon': -95.13396524228548, 'geo.center.lat': 73.25566470759851,'geo.projection.scale': 4.000000000000003}, 
       'Maritimes Region': {'geo.projection.rotation.lon': -63.1261460700024, 'geo.center.lon': -63.1261460700024, 'geo.center.lat': 44.8202886873768,'geo.projection.scale': 32.00000000000006},
       'St. Lawrence Seaway Region': {'geo.projection.rotation.lon': -77.30560743930843, 'geo.center.lon': -77.30560743930843, 'geo.center.lat': 44.01540087191435, 'geo.projection.scale': 36.75834735990517}, 
       'Quebec Region': {'geo.projection.rotation.lon': -65.68478238605977, 'geo.center.lon': -65.68478238605977, 'geo.center.lat': 48.94642841990159,'geo.projection.scale': 21.112126572366343}, 
       'Pacific Region': {'geo.projection.rotation.lon': -127.36955114924267, 'geo.center.lon': -127.36955114924267, 'geo.center.lat': 51.378282668463775,'geo.projection.scale': 27.857618025476015},
       'West Canadian Water Region': {'geo.projection.rotation.lon': -95.13396524228548, 'geo.center.lon': -95.13396524228548, 'geo.center.lat': 73.25566470759851,'geo.projection.scale': 4.000000000000003}, 
       'Arctic Region': {'geo.projection.rotation.lon': -95.13396524228548, 'geo.center.lon': -95.13396524228548, 'geo.center.lat': 73.25566470759851,'geo.projection.scale': 4.000000000000003}
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
    
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]

    #si le slider est utilisé
    if input_id == "slider_updatemode":
        print("update map",relayoutData)
        #évite que le zoom inital ne se perde au chargement
            #si pas de région de sélectionnée, on update la map avec les ports au dessus de la limite et le même zoom
        if relayoutData != None and region_dropdown == None:
            fig = map_viz.get_map(map_data_departure,"Departure",int(10**slider_value),relayoutData,prev_zoom)
            #si il y a une région de sélectionnée, on update la map avec les ports au dessus de la limite et le zoom de la région
        elif relayoutData != None and region_dropdown != None:
            fig = map_viz.get_map(map_data_departure,"Departure",int(10**slider_value),zooms[region_dropdown],prev_zoom)
        else : #cas où relayoutData= None, à l'initialisation par exemple
            fig = figure
        return "Ports avec plus de {0} bateaux en trafic".format(int(transform_value(slider_value))), fig
    
    #si une region est sélectionnée
    if input_id == "region_dropdown":
        print("region_dropdown")
        if region_dropdown != None:
            zoom = zooms[region_dropdown]
            figure = go.Figure(figure)
            #on ajuste la figure avec le zoom sur la région
            figure.update_geos(
                projection_rotation_lon= zoom['geo.projection.rotation.lon'],
                center_lon= zoom['geo.center.lon'],
                center_lat= zoom['geo.center.lat'],
                projection_scale= zoom['geo.projection.scale']
                )
            return dash.no_update, figure

        else:
            return "Ports avec plus de {0} bateaux en trafic".format(int(transform_value(slider_value))), figure
   
    #si un port est sélectionné
    ##centre la carte sur le port sélectionné + TODO mise en couleur/augmentation taille
    if input_id == "harbour_dropdown":
        print("update zoom port")
        harbour_data = map_data_departure[map_data_departure["Departure Hardour"]==harbour_dropdown]

        figure = map_viz.get_map(map_data_departure,"Departure",min(harbour_data["Trafic"].values[0],int(10**slider_value)),None,None)
        #upadte du zoom centré sur les lat et lon du port
        figure.update_geos(
                #projection_rotation_lon= zoom['geo.projection.rotation.lon'],
                center_lon= harbour_data["Departure Longitude"].values[0],
                center_lat= harbour_data["Departure Latitude"].values[0],
                projection_scale= 60
                )
        return dash.no_update, figure

    else:
        return "Ports avec plus de {0} bateaux en trafic".format(int(transform_value(slider_value))), figure





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




#Callback lineshart

@app.callback(
    Output('linechart', 'figure'),
    [Input('year-dropdown', 'value'),
    Input('harbour_dropdown','value')]
)
def update_output(year,harbour_value):

    print('year', year)
    dff1 = dff[dff['Departure Year'] == year].sort_values('Date')
    
    if harbour_value == None:
        

        fig = px.line(dff1,
            x='Date',
            y='Traffic',
            title=f"Evolution du trafic par mois")
                                #hover_data={'BUSINESS_NAME': True, 'LATITUDE': False, 'LONGITUDE': False,
                                            #'APP_SQ_FT': True})

    else:
        dff2 = preprocess.traffic_per_time(data, scale="day")
        dff2 = dff2[dff2["Departure Hardour"]== harbour_value]
        dff2 = dff2.groupby(['Date'])['Traffic'].sum().reset_index()
        
        print(dff2.columns)

        dff2["Departure Year"] = pd.to_datetime(dff2["Date"]).dt.year.astype('str')
        dff2 = dff2[dff2['Departure Year'] == year].sort_values('Date')
    


        fig = px.line(dff2,
            x='Date',
            y='Traffic',
            title=f"Evolution du trafic journalier",
                                #hover_data={'BUSINESS_NAME': True, 'LATITUDE': False, 'LONGITUDE': False,
                                            #'APP_SQ_FT': True}) 
            )

    
    fig.update_layout(title_x=0.5, font_size=15)
    return fig