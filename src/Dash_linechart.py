from datetime import datetime as dt
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import preprocess
import pandas as pd

df = pd.read_csv("data/TRIP.csv")


dff=preprocess.traffic_per_time(df, scale="day")
dff = dff.groupby('Departure Day')['Traffic'].sum().reset_index()
print(dff['Departure Day'].value_counts())
dff["Departure Year"] = pd.to_datetime(dff["Departure Day"]).dt.year.astype('str')
years = dff['Departure Year'].drop_duplicates().sort_values().tolist()
print(dff[dff['Departure Year'] == '2017'].head())

print(years)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    
    dcc.Dropdown(options=[{'value':year, 'label':year} for year in years], 
            value=years[0], 
            id='year-dropdown',
            optionHeight=35,                    #height/space between dropdown options
            disabled=False,                     #disable dropdown value selection
            multi=False,                        #allow multiple dropdown values to be selected
            searchable=True,                    #allow user-searching of dropdown values
            search_value='',                    #remembers the value searched in dropdown
            placeholder='Please select...',     #gray, default text shown when no option is selected
            clearable=True,                     #allow user to removes the selected value
            style={'width':"100%"},             #use dictionary to define CSS styles of your dropdown
        ),
    html.H3("Evolution du trafic par mois", style={'textAlign': 'center'}),
    dcc.Graph(id='linechart')
])



@app.callback(
    Output('linechart', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_output(year):

    print('year', year)
    dff1 = dff[dff['Departure Year'] == year].sort_values('Departure Day')

    fig = px.line(dff1,
        x='Departure Day',
        y='Traffic',
        title=f"Evolution du traffic par mois")
                               #hover_data={'BUSINESS_NAME': True, 'LATITUDE': False, 'LONGITUDE': False,
                                        #'APP_SQ_FT': True})
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False)
