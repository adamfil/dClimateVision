import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from vars import VALID_DASHSET
from vars import TOKEN
import helper
from datetime import datetime



app = dash.Dash(__name__)
server = app.server

# import data

app.layout = html.Div(children=[


    html.H1("dClimate  Gridhistory Data Visualization", style={
        'text-align': 'center'
    }),

    dcc.Dropdown(
        id='slct_dataset',
        options=VALID_DASHSET,
        placeholder="Select a dataset",
        multi=False,
        value='vhi',
        style={'width': '40%'}
                 ),

    dcc.DatePickerRange(
        id='slct_date',
        min_date_allowed=datetime(1980, 1, 1),
        max_date_allowed=datetime(2021, 1, 1),
        start_date=datetime(2000, 1, 1),
        end_date=datetime(2017, 8, 25)

    ),

    dcc.Input(
        id='slct_lat',
        placeholder='',
        size='35',
    ),
    dcc.Input(
        id='slct_long',
        placeholder='',
        size='35',
    ),

    html.Div(id='output_container', children=[], style={
        'textAlign': 'center'
    }),
    html.Br(),

    dcc.Graph(id='my_series_graph', figure={})

])

#callback to produce graph
@app.callback(
    [
        Output(component_id='output_container', component_property='children'),
        Output(component_id='my_series_graph', component_property='figure')
    ],
    [
        Input(component_id='slct_dataset', component_property='value'),
        Input(component_id='slct_date', component_property='start_date'),
        Input(component_id='slct_date', component_property='end_date'),
        Input(component_id='slct_lat', component_property='value'),
        Input(component_id='slct_long', component_property='value')

    ]
)

# change # of arguments based on number of inputs in below func and add input above
def update_graph(dataset_slctd, start_date_slctd, end_date_slctd, lat_slctd, long_slctd):

    #call function to adjust to date range
    container = 'Dataset: {}'.format(dataset_slctd) +\
                '. Start date: {}'.format(start_date_slctd) + \
                '. End date: {}'.format(end_date_slctd) +\
                '. Latitude: {}'.format(lat_slctd) + \
                '. Longitude: {}'.format(long_slctd)

    latlong = (lat_slctd, long_slctd)
    data_pulled = helper.get_gridhistory_daily_series_snapped(dataset_slctd, latlong, TOKEN)
    dff = helper.trim_series(data_pulled[1], start_date_slctd, end_date_slctd)

    snapped_lat = str(data_pulled[0][0])
    snapped_long = str(data_pulled[0][1])

    dff = dff.to_frame(name='Value')
    dff['Datetime'] = dff.index
    fig = px.line(dff, x='Datetime', y='Value', title=dataset_slctd + ' snapped to lat: ' + snapped_lat + ' long: ' + snapped_long)

    return container, fig

@app.callback(
    [
        Output(component_id='slct_date', component_property='min_date_allowed'),
        Output(component_id='slct_date', component_property='max_date_allowed'),
        Output(component_id='slct_date', component_property='start_date'),
        Output(component_id='slct_date', component_property='end_date'),
        Output(component_id='slct_lat', component_property='placeholder'),
        Output(component_id='slct_long', component_property='placeholder'),
    ],
    [
        Input(component_id='slct_dataset', component_property='value'),
    ]
)

def update_inputs(dataset_slctd):

    #to do: improve efficiency below, combine into 1 API pull for date range, lat/long range
    daterange = helper.get_date_range(dataset_slctd, TOKEN)

    mindr = daterange[0]
    maxdr = daterange[1]

    lat_pull = helper.get_lat_range(dataset_slctd, TOKEN)
    lat_min = lat_pull[0]
    lat_max = lat_pull[1]

    long_pull = helper.get_long_range(dataset_slctd, TOKEN)
    long_min = long_pull[0]
    long_max = long_pull[1]

    lat_info = 'Enter lat. Min: ' + str(lat_min) + '. Max: ' + str(lat_max) + '.'
    long_info = 'Enter long. Min: ' + str(long_min) + '. Max: ' + str(long_max) + '.'

    return mindr, maxdr, mindr, maxdr, lat_info, long_info

def get_lat_range(dataset: str, my_token: str):
    my_url = 'https://api.dclimate.net/apiv3/metadata/' + dataset + '?full_metadata=true'
    head = {"Authorization": my_token}
    r = requests.get(my_url, headers=head)
    data = r.json()['latitude range']
    return data

def get_long_range(dataset: str, my_token: str):
    my_url = 'https://api.dclimate.net/apiv3/metadata/' + dataset + '?full_metadata=true'
    head = {"Authorization": my_token}
    r = requests.get(my_url, headers=head)
    data = r.json()['longitude range']
    return data

if __name__ == '__main__':
    app.run_server(debug=True)
