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
from vars import VALID_ANALYSIS_TYPES, VALID_HISTOGRAM_BINS, VALID_SCATTERPLOT_INTERVALS, VALID_DIFF_INTERVALS
import helper
from datetime import datetime
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from classes import InputQuery

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[

    # title
    html.H1("dClimate Data Visualization", style={
        'text-align': 'center'
    }),

    # secondary dataset plot text
    html.H1("Plot primary element or analysis", style={
        'text-align': 'left',
        'fontSize': 18
    }),

    # select whether to plot analysis or raw element
    html.Div([
        dcc.RadioItems(
            id='primary-analysis-or-raw',
            options=[
                {'label': 'Raw element', 'value': 'Raw element'},
                {'label': 'Analysis of an element', 'value': 'Analysis of an element'},
            ],
            value='Raw element',
        )
    ], style={'display': 'block'}
    ),

    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Dropdown(
            id='slct-dataset-type',
            options=VALID_DATASET_TYPES,
            placeholder="Select a primary dataset type",
            multi=False,
            value='',
            style={'width': '40%'}
        )
    ], style={'display': 'block'}),  # <-- This is the line that will be changed by the dropdown callback

    # if type of dataset selected has subsections, select specific dataset
    html.Div([
        dcc.Dropdown(
            id='datasets-to-hide',
            options=[],
            placeholder='Select a dataset',
            value=None,
            style={'width': '40%'},
        )
    ], style={'display': 'block'}),

    # lat
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
            value=None,
            style={'width': '40%'},
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
            value=None,
            style={'width': '40%'},
        )
    ], style={'display': 'block'}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # select analysis type dcc
    html.Div([
        dcc.Dropdown(
            id='slct-analysis-type',
            options=VALID_ANALYSIS_TYPES,
            placeholder="Select an analysis type",
            multi=False,
            value=None,
            style={'width': '40%'}
        ),
    ], style={'display': 'block'}
    ),

    # select histogram bin size
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Dropdown(
            id='slct-bin-size',
            options=VALID_HISTOGRAM_BINS,
            placeholder="Select a histogram bin size",
            multi=False,
            value=None,
            style={'width': '40%'}
        ),
    ], style={'display': 'block'}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # select scatterplot interval size
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Dropdown(
            id='slct-scatterplot-size',
            options=VALID_SCATTERPLOT_INTERVALS,
            placeholder="Select a scatterplot interval size",
            multi=False,
            value=None,
            style={'width': '40%'}
        ),
    ], style={'display': 'block'}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # select sma interval size
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Input(
            id='slct-sma-size',
            placeholder='something',
            value='Select SMA interval size in units of dataset frequency',
            size='50',
        )
    ], style={'display': 'block'}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # select scatterplot interval size
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Dropdown(
            id='slct-diff-size',
            options=VALID_DIFF_INTERVALS,
            placeholder="Select difference interval",
            multi=False,
            value=None,
            style={'width': '40%'}
        ),
    ], style={'display': 'None'}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # secondary dataset plot text
    html.H1("Plot secondary element or analysis?", style={
        'text-align': 'left',
        'fontSize': 18
    }),

    # select whether to plot analysis AND raw element or NOT
    html.Div([
        dcc.RadioItems(
            id='secondary-or-no',
            options=[
                {'label': 'Yes', 'value': 'Yes'},
                {'label': 'No', 'value': 'No'},
            ],
            value='No',
        )
    ], style={'display': 'block'}
    ),

    # select whether to plot analysis OR raw element
    html.Div([
        dcc.RadioItems(
            id='secondary-analysis-or-raw',
            options=[
                {'label': 'Raw element', 'value': 'Raw element'},
                {'label': 'Analysis of an element', 'value': 'Analysis of an element'},
            ],
            value=None,
        )
    ], style={'display': 'block'}
    ),

    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Dropdown(
            id='slct-dataset-type2',
            options=VALID_DATASET_TYPES,
            placeholder="Select a secondary dataset type",
            multi=False,
            value='',
            style={'width': '40%'}
        )
    ], style={'display': 'block'}),  # <-- This is the line that will be changed by the dropdown callback

    # if type of dataset selected has subsections, select specific dataset
    html.Div([
        dcc.Dropdown(
            id='datasets-to-hide2',
            options=[],
            placeholder='Select a dataset',
            value=None,
            style={'width': '40%'},
        )
    ], style={'display': 'block'}),

    # lat
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Input(
            id='lat-to-hide2',
            placeholder='something',
            value='Enter a latitude',
            size='50',
        )
    ], style={'display': 'block'}),  # <-- This is the line that will be changed by the dropdown callback

    # long
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Input(
            id='long-to-hide2',
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
            id='daterange-to-hide2',
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
            id='variable-to-hide2',
            options=[],
            placeholder='Select a weather variable',
            value=None,
            style={'width': '40%'},
        )
    ], style={'display': 'block'}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # station id
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Dropdown(
            id='station-to-hide2',
            options=[],
            placeholder='Select a station id',
            value=None,
            style={'width': '40%'},
        )
    ], style={'display': 'block'}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # select analysis type dcc
    html.Div([
        dcc.Dropdown(
            id='slct-analysis-type2',
            options=VALID_ANALYSIS_TYPES,
            placeholder="Select an analysis type",
            multi=False,
            value=None,
            style={'width': '40%'}
        ),
    ], style={'display': 'block'}
    ),

    # select histogram bin size
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Dropdown(
            id='slct-bin-size2',
            options=VALID_HISTOGRAM_BINS,
            placeholder="Select a histogram bin size",
            multi=False,
            value=None,
            style={'width': '40%'}
        ),
    ], style={'display': 'block'}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # select scatterplot interval size
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Dropdown(
            id='slct-scatterplot-size2',
            options=VALID_SCATTERPLOT_INTERVALS,
            placeholder="Select a scatterplot interval size",
            multi=False,
            value=None,
            style={'width': '40%'}
        ),
    ], style={'display': 'block'}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # select sma interval size
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Input(
            id='slct-sma-size2',
            placeholder='something',
            value='Select SMA interval size in units of dataset frequency',
            size='50',
        )
    ], style={'display': 'block'}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # select difference interval size
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Dropdown(
            id='slct-diff-size2',
            options=VALID_DIFF_INTERVALS,
            placeholder="Select difference interval",
            multi=False,
            value=None,
            style={'width': '40%'}
        ),
    ], style={'display': 'None'}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # select whether to plot analysis AND raw element or NOT
    html.Div([
        dcc.RadioItems(
            id='axis-or-no',
            options=[
                {'label': 'Use same axis', 'value': 'Use same axis'},
                {'label': 'Use secondary axis', 'value': 'Use secondary axis'},
            ],
            value='Use same axis',
        )
    ], style={'display': 'block'}
    ),

    # plot figure
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

   [Input(component_id='slct-dataset-type', component_property='value')])


def show_relevant_parameters_primary(slctd_dataset_type):

    if slctd_dataset_type in ['GFS Forecasts', 'Grid File Dataset History']:
        return {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'none'}, {'display': 'none'}

    if slctd_dataset_type in ['Dutch Station History', 'CME Station History', 'GHCN Dataset History', 'German Station History']:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}

    else:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

@app.callback(
   [
       Output(component_id='datasets-to-hide', component_property='options'),
   ],

   [Input(component_id='slct-dataset-type', component_property='value')])


def update_dataset_input_primary(slctd_dataset_type):

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

   [Input(component_id='slct-dataset-type', component_property='value')])


def update_statvariable_input_primary(slctd_dataset_type):

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

#update primary input based on whether analysis or raw element is selected
@app.callback(
   [
       Output(component_id='slct-analysis-type', component_property='style')
   ],

   [Input(component_id='primary-analysis-or-raw', component_property='value')])


def update_analysis_or_raw(input):

    if input in ['Analysis of an element']:
        return [{'display': 'block'}]

    if input in ['Raw element']:
        return [{'display': 'none'}]

#update primary input based on whether analysis or raw element is selected
@app.callback(
   [
       Output(component_id='slct-analysis-type2', component_property='style')
   ],

   [Input(component_id='secondary-analysis-or-raw', component_property='value'),
    Input(component_id='secondary-or-no', component_property='value')])


def update_analysis_or_raw(input1, input2):

    if input2 in ['No']:
        return [{'display': 'none'}]

    if input1 in ['Analysis of an element']:
        return [{'display': 'block'}]

    if input1 in ['Raw element']:
        return [{'display': 'none'}]

#update input parameters based on analysis type selected
@app.callback(
   [
       Output(component_id='slct-bin-size', component_property='style'),
       Output(component_id='slct-scatterplot-size', component_property='style'),
       Output(component_id='slct-sma-size', component_property='style'),
       Output(component_id='slct-diff-size', component_property='style'),
   ],

   [Input(component_id='slct-analysis-type', component_property='value'),
    Input(component_id='primary-analysis-or-raw', component_property='value')])


def update_analysis_or_raw1(input1, input2):

    #show no parameters if raw element is selected
    if input2 in ['Raw element']:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]

    #select parameters to display for histograms
    if input1 in ['Histogram - sum', 'Histogram - average']:
        return [{'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]

    #select parameters to display for scatterplots
    if input1 in ['Interval scatterplot - sum', 'Interval scatterplot - average']:
        return [{'display': 'none'}, {'display': 'block'}, {'display': 'none'}, {'display': 'none'}]

    #select parameters to display for SMA
    if input1 in ['Simple Moving Average']:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'block'}, {'display': 'none'}]

    #select parameters to display for diff plot
    if input1 in ['Difference of element']:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'block'}]

    #display no parameters
    if input1 in ['']:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]

#update input parameters based on analysis type selected
@app.callback(
   [
       Output(component_id='slct-bin-size2', component_property='style'),
       Output(component_id='slct-scatterplot-size2', component_property='style'),
       Output(component_id='slct-sma-size2', component_property='style'),
       Output(component_id='slct-diff-size2', component_property='style'),
   ],

   [Input(component_id='slct-analysis-type2', component_property='value'),
    Input(component_id='secondary-analysis-or-raw', component_property='value'),
    Input(component_id='secondary-or-no', component_property='value')])


def update_analysis_or_raw2(input1, input2, input3):

    #show no parameters if raw element is selected
    if input3 in ['No']:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]

    #show no parameters if raw element is selected
    if input2 in ['Raw element']:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]

    #select parameters to display for histograms
    if input1 in ['Histogram - sum', 'Histogram - average']:
        return [{'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]

    #select parameters to display for scatterplots
    if input1 in ['Interval scatterplot - sum', 'Interval scatterplot - average']:
        return [{'display': 'none'}, {'display': 'block'}, {'display': 'none'}, {'display': 'none'}]

    #select parameters to display for SMA
    if input1 in ['Simple Moving Average']:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'block'}, {'display': 'none'}]

    #select parameters to display for diff plot
    if input1 in ['Difference of element']:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'block'}]

    #display no parameters
    if input1 in ['']:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]

#show/hide secondary selection of raw element vs analysis of an element
@app.callback(
   [
       Output(component_id='secondary-analysis-or-raw', component_property='style')
   ],

   [Input(component_id='secondary-or-no', component_property='value')])


def update_analysis_or_raw(input):

    if input in ['Yes']:
        return [{'display': 'block'}]

    if input in ['No']:
        return [{'display': 'none'}]


@app.callback(
   [
       Output(component_id='datasets-to-hide2', component_property='style'),
       Output(component_id='lat-to-hide2', component_property='style'),
       Output(component_id='long-to-hide2', component_property='style'),
       Output(component_id='daterange-to-hide2', component_property='style'),
       Output(component_id='variable-to-hide2', component_property='style'),
       Output(component_id='station-to-hide2', component_property='style'),
       Output(component_id='slct-dataset-type2', component_property='style'),
       Output(component_id='axis-or-no', component_property='style'),
   ],

   [Input(component_id='slct-dataset-type2', component_property='value'),
    Input(component_id='secondary-or-no', component_property='value')])


def show_relevant_parameters_secondary(slctd_dataset_type, second_input):
    # if no secondary input is selected, show no parameters
    if second_input == 'No':
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

    else:
        # show relevant parameters for dataset type
        if slctd_dataset_type in ['GFS Forecasts', 'Grid File Dataset History']:
            return {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, {'display': 'block'}

        # show relevant parameters for dataset type
        if slctd_dataset_type in ['Dutch Station History', 'CME Station History', 'GHCN Dataset History', 'German Station History']:
            return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'}

        # if no data type is selected but secondary input is yes, only show option to select data type
        if slctd_dataset_type in ['']:
            return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, {'display': 'block'}

@app.callback(
   [
       Output(component_id='datasets-to-hide2', component_property='options'),
   ],

   [Input(component_id='slct-dataset-type2', component_property='value')])


def update_dataset_input_primary(slctd_dataset_type):

    if slctd_dataset_type in ['Grid File Dataset History']:
        return [VALID_GRIDFILE_DASHSET]

    if slctd_dataset_type in ['GFS Forecasts']:
        return [VALID_GFS_DASHSET]
    else:
        pass

@app.callback(
   [
       Output(component_id='station-to-hide2', component_property='options'),
       Output(component_id='variable-to-hide2', component_property='options'),
   ],

   [Input(component_id='slct-dataset-type2', component_property='value')])


def update_statvariable_input_secondary(slctd_dataset_type):

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

def update_latlong1(dataset_slctd):

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
        Output(component_id='lat-to-hide2', component_property='placeholder'),
        Output(component_id='long-to-hide2', component_property='placeholder'),
        Output(component_id='lat-to-hide2', component_property='value'),
        Output(component_id='long-to-hide2', component_property='value'),
    ],
    [
        Input(component_id='datasets-to-hide2', component_property='value'),
    ]
)

def update_latlong2(dataset_slctd):

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
        Input(component_id='slct-dataset-type2', component_property='value'),
        Input(component_id='datasets-to-hide2', component_property='value'),
    ]
)

def update_daterange1(slctd_dataset_type, slctd_dataset):

    if slctd_dataset_type in ['Grid File Dataset History', 'GFS Forecasts']:
        daterange = helper.get_date_range(slctd_dataset, TOKEN)

        mindr = daterange[0]
        maxdr = daterange[1]

        return mindr, maxdr, mindr, maxdr

    if slctd_dataset_type in ['Dutch Station History', 'CME Station History', 'German Station History', 'GHCN Dataset History']:

        return datetime(2000, 1, 1), datetime.today(), datetime(2000, 1, 1), datetime.today()

    else:
        pass

@app.callback(
    [
        Output(component_id='daterange-to-hide2', component_property='min_date_allowed'),
        Output(component_id='daterange-to-hide2', component_property='max_date_allowed'),
        Output(component_id='daterange-to-hide2', component_property='start_date'),
        Output(component_id='daterange-to-hide2', component_property='end_date'),
    ],
    [
        Input(component_id='slct-dataset-type2', component_property='value'),
        Input(component_id='datasets-to-hide2', component_property='value'),
    ]
)

def update_daterange2(slctd_dataset_type, slctd_dataset):

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
        Output(component_id='my_series_graph', component_property='figure')
    ],
    [
        Input(component_id='primary-analysis-or-raw', component_property='value'),
        Input(component_id='secondary-analysis-or-raw', component_property='value'),
        Input(component_id='slct-dataset-type', component_property='value'),
        Input(component_id='datasets-to-hide', component_property='value'),
        Input(component_id='daterange-to-hide', component_property='start_date'),
        Input(component_id='daterange-to-hide', component_property='end_date'),
        Input(component_id='lat-to-hide', component_property='value'),
        Input(component_id='long-to-hide', component_property='value'),
        Input(component_id='station-to-hide', component_property='value'),
        Input(component_id='variable-to-hide', component_property='value'),
        Input(component_id='slct-dataset-type2', component_property='value'),
        Input(component_id='datasets-to-hide2', component_property='value'),
        Input(component_id='daterange-to-hide2', component_property='start_date'),
        Input(component_id='daterange-to-hide2', component_property='end_date'),
        Input(component_id='lat-to-hide2', component_property='value'),
        Input(component_id='long-to-hide2', component_property='value'),
        Input(component_id='station-to-hide2', component_property='value'),
        Input(component_id='variable-to-hide2', component_property='value'),
        Input(component_id='slct-analysis-type', component_property='value'),
        Input(component_id='slct-analysis-type2', component_property='value'),
        Input(component_id='slct-bin-size', component_property='value'),
        Input(component_id='slct-scatterplot-size', component_property='value'),
        Input(component_id='slct-sma-size', component_property='value'),
        Input(component_id='slct-diff-size', component_property='value'),
        Input(component_id='slct-bin-size2', component_property='value'),
        Input(component_id='slct-scatterplot-size2', component_property='value'),
        Input(component_id='slct-sma-size2', component_property='value'),
        Input(component_id='slct-diff-size2', component_property='value'),
        Input(component_id='secondary-or-no', component_property='value'),
        Input(component_id='axis-or-no', component_property='value'),
    ]
)

def update_graph(analysis_or_raw1, analysis_or_raw2, dataset_type_slctd1, dataset_slctd1, start_date_slctd1, end_date_slctd1, lat_slctd1, long_slctd1,
                 station_slctd1, variable_slctd1, dataset_type_slctd2, dataset_slctd2, start_date_slctd2, end_date_slctd2,
                 lat_slctd2, long_slctd2, station_slctd2, variable_slctd2, anal_type_1, anal_type_2, bin_size1, scatter_size1, sma_size1, diff_size1, bin_size2, scatter_size2, sma_size2, diff_size2,
                 second_or_no, axis_or_no):

    #1st thing to do, check query completeness. if incomplete return no graph. do the same thing in the parameter update column

    input = InputQuery(second_or_no, dataset_type_slctd1, start_date_slctd1, end_date_slctd1, analysis_or_raw1, dataset_slctd1, lat_slctd1, long_slctd1, station_slctd1, variable_slctd1, anal_type_1, bin_size1,
                        scatter_size1, sma_size1, analysis_or_raw2, dataset_type_slctd2, start_date_slctd2, end_date_slctd2, dataset_slctd2, lat_slctd2, long_slctd2, station_slctd2, variable_slctd2,
                        anal_type_2, bin_size2, scatter_size2, sma_size2, axis_or_no)


    return [input.plot]


if __name__ == '__main__':
    app.run_server(debug=True)
