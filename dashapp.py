import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
#import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from vars import VALID_DATASET_TYPES
from vars import VALID_GRIDFILE_DASHSET
from vars import VALID_GFS_DASHSET
from vars import VALID_DUTCH_STATIONS, VALID_DUTCH_VARIABLES
from vars import VALID_CME_STATIONS, VALID_CME_VARIABLES
from vars import VALID_GHCN_STATIONS, VALID_GHCN_VARIABLES
from vars import TOKEN
import helper
from datetime import datetime
import requests




app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[


    html.H1("dClimate Data Visualization", style={
        'text-align': 'center'
    }),

    dcc.Dropdown(
        id='slct_dataset_type',
        options=VALID_DATASET_TYPES,
        placeholder="Select a dataset type",
        multi=False,
        value='',
        style={'width': '40%'}
                 ),
    #datasets to hide
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Dropdown(
            id='datasets-to-hide',
            options=[],
            placeholder='Select a dataset',
            value='Can you see datasets?',
        )
    ], style={'display': 'block'}),  # <-- This is the line that will be changed by the dropdown callback

    #lat
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Input(
            id='lat-to-hide',
            placeholder='something',
            value='Enter a latitude',
            size='50',
        )
    ], style={'display': 'block'}),  # <-- This is the line that will be changed by the dropdown callback

    # long
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Input(
            id='long-to-hide',
            placeholder='something',
            value='Enter a longitude',
            size='50',
        )
    ], style={'display': 'block'}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # normal date range
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.DatePickerRange(
            id='daterange-to-hide',
            min_date_allowed=datetime(1980, 1, 1),
            max_date_allowed=datetime.today(),
            start_date=datetime(2000, 1, 1),
            end_date=datetime.today()

        ),
    ], style={'display': 'block'}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # weather variable
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Dropdown(
            id='variable-to-hide',
            options=[],
            placeholder='Select a weather variable',
            value='Can you see variable?',
        )
    ], style={'display': 'block'}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # station id
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Dropdown(
            id='station-to-hide',
            options=[],
            placeholder='Select a station id',
            value='Can you see station id?',
        )
    ], style={'display': 'block'}  # <-- This is the line that will be changed by the dropdown callback
    ),

    html.Div(id='output_container', children=[], style={
        'textAlign': 'center'
    }),
    html.Br(),

    dcc.Graph(id='my_series_graph', figure={})

])


@app.callback(
   [
       Output(component_id='datasets-to-hide', component_property='style'),
       Output(component_id='lat-to-hide', component_property='style'),
       Output(component_id='long-to-hide', component_property='style'),
       Output(component_id='daterange-to-hide', component_property='style'),
       Output(component_id='variable-to-hide', component_property='style'),
       Output(component_id='station-to-hide', component_property='style')
   ],

   [Input(component_id='slct_dataset_type', component_property='value')])


def show_hide_element(slctd_dataset_type):

    if slctd_dataset_type in ['GFS Forecasts', 'Grid File Dataset History', '']:
        return {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'none'}, {'display': 'none'}

    if slctd_dataset_type in ['Dutch Station History', 'CME Station History', 'GHCN Dataset History', 'German Station History']:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}

@app.callback(
   [
       Output(component_id='datasets-to-hide', component_property='options'),
   ],

   [Input(component_id='slct_dataset_type', component_property='value')])


def update_dataset_input(slctd_dataset_type):

    if slctd_dataset_type in ['Grid File Dataset History']:
        return [VALID_GRIDFILE_DASHSET]

    if slctd_dataset_type in ['GFS Forecasts']:
        return [VALID_GFS_DASHSET]
    else:
        pass

@app.callback(
   [
       Output(component_id='station-to-hide', component_property='options'),
       Output(component_id='variable-to-hide', component_property='options'),
   ],

   [Input(component_id='slct_dataset_type', component_property='value')])


def update_statvariable_input(slctd_dataset_type):

    if slctd_dataset_type in ['Dutch Station History']:
        return [VALID_DUTCH_STATIONS, VALID_DUTCH_VARIABLES]
    if slctd_dataset_type in ['GHCN Dataset History']:
        return [VALID_GHCN_STATIONS, VALID_GHCN_VARIABLES]
    if slctd_dataset_type in ['CME Station History']:
        return [VALID_CME_STATIONS, VALID_CME_VARIABLES]
    if slctd_dataset_type in ['German Station History']:
        pass
    else:
        pass

@app.callback(
    [
        Output(component_id='lat-to-hide', component_property='placeholder'),
        Output(component_id='long-to-hide', component_property='placeholder'),
        Output(component_id='lat-to-hide', component_property='value'),
        Output(component_id='long-to-hide', component_property='value'),
    ],
    [
        Input(component_id='datasets-to-hide', component_property='value'),
    ]
)

def update_latlong(dataset_slctd):

    lat_pull = helper.get_lat_range(dataset_slctd, TOKEN)
    lat_min = lat_pull[0]
    lat_max = lat_pull[1]

    long_pull = helper.get_long_range(dataset_slctd, TOKEN)
    long_min = long_pull[0]
    long_max = long_pull[1]

    lat_info = 'Enter lat. Min: ' + str(lat_min) + '. Max: ' + str(lat_max) + '.'
    long_info = 'Enter long. Min: ' + str(long_min) + '. Max: ' + str(long_max) + '.'

    lat_slctd = ''
    long_slctd = ''

    return lat_info, long_info, lat_slctd, long_slctd

@app.callback(
    [
        Output(component_id='daterange-to-hide', component_property='min_date_allowed'),
        Output(component_id='daterange-to-hide', component_property='max_date_allowed'),
        Output(component_id='daterange-to-hide', component_property='start_date'),
        Output(component_id='daterange-to-hide', component_property='end_date'),
    ],
    [
        Input(component_id='slct_dataset_type', component_property='value'),
        Input(component_id='datasets-to-hide', component_property='value'),
    ]
)

def update_daterange(slctd_dataset_type, slctd_dataset):

    if slctd_dataset_type in ['Grid File Dataset History', 'GFS Forecasts']:
        daterange = helper.get_date_range(slctd_dataset, TOKEN)

        mindr = daterange[0]
        maxdr = daterange[1]

        return mindr, maxdr, mindr, maxdr

    if slctd_dataset_type in ['Dutch Station History', 'CME Station History', 'German Station History', 'GHCN Dataset History']:

        return datetime(2000, 1, 1), datetime.today(), datetime(2000, 1, 1), datetime.today()

    else:
        pass

#callback to produce graph
@app.callback(
    [
        Output(component_id='output_container', component_property='children'),
        Output(component_id='my_series_graph', component_property='figure')
    ],
    [
        Input(component_id='slct_dataset_type', component_property='value'),
        Input(component_id='datasets-to-hide', component_property='value'),
        Input(component_id='daterange-to-hide', component_property='start_date'),
        Input(component_id='daterange-to-hide', component_property='end_date'),
        Input(component_id='lat-to-hide', component_property='value'),
        Input(component_id='long-to-hide', component_property='value'),
        Input(component_id='station-to-hide', component_property='value'),
        Input(component_id='variable-to-hide', component_property='value'),
    ]
)

# change # of arguments based on number of inputs in below func and add input above
def update_graph(dataset_type_slctd, dataset_slctd, start_date_slctd, end_date_slctd, lat_slctd, long_slctd, station_slctd, variable_slctd):

    if dataset_type_slctd in ['Grid File Dataset History']:

        latlong = (lat_slctd, long_slctd)
        data_pulled = helper.get_gridhistory_daily_series_snapped(dataset_slctd, latlong, TOKEN)
        dff = helper.trim_series(data_pulled[1], start_date_slctd, end_date_slctd)

        snapped_lat = str(data_pulled[0][0])
        snapped_long = str(data_pulled[0][1])

        container = 'Dataset: {}'.format(dataset_slctd) +\
                    '. Start date: {}'.format(start_date_slctd) + \
                    '. End date: {}'.format(end_date_slctd) +\
                    '. Snapped to Latitude: {}'.format(snapped_lat) + \
                    '. Snapped to Longitude: {}'.format(snapped_long)

        dff = dff.to_frame(name='Value')
        dff['Datetime'] = dff.index
        fig = px.line(dff, x='Datetime', y='Value', title=container)
        container = ''

        return container, fig

    if dataset_type_slctd in ['Dutch Station History', 'CME Station History', 'German Station History', 'GHCN Dataset History']:
        container = 'Dataset: {}'.format(dataset_type_slctd) +\
                    '. Station ID: {}'.format(station_slctd) + \
                    '. Weather Variable: {}'.format(variable_slctd)
        data_pulled = helper.get_station_variable_series(dataset_type_slctd, station_slctd, variable_slctd, TOKEN)
        dff = helper.trim_series(data_pulled, start_date_slctd, end_date_slctd)

        dff = dff.to_frame(name='Value')
        dff['Datetime'] = dff.index
        fig = px.line(dff, x='Datetime', y='Value', title=container)
        container = ''

        return container, fig
    else:
        pass


if __name__ == '__main__':
    app.run_server(debug=True)
