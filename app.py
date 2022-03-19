import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from vars import VALID_DATASET_TYPES
from vars import VALID_GRIDFILE_DASHSET
from vars import VALID_GFS_DASHSET
from vars import VALID_DUTCH_STATIONS, VALID_DUTCH_VARIABLES
from vars import VALID_CME_STATIONS, VALID_CME_VARIABLES
from vars import VALID_GHCN_VARIABLES
from vars import TOKEN
from vars import VALID_ANALYSIS_TYPES, VALID_HISTOGRAM_BINS, VALID_SCATTERPLOT_INTERVALS, VALID_DIFF_INTERVALS
import helper
from datetime import datetime
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from classes import InputQuery

INPUT_WIDTH = '340px'

theme = [dbc.themes.SLATE]

app = dash.Dash(__name__, external_stylesheets=theme)
server = app.server

app.layout = html.Div(

    style={
        #"background-image": "url('assets/greenbrier2.jpg')",
        "background-color": "#666666",
        "background-size": "100%",
        "color": "white",
        "display": "flex",
        "justify-content": "center",
        "align-items": "top",
        "min-height" : "100vh",
        "font-size": "16px",
        "padding": "12px"
    },

    children=[

    html.Div(

    children=[

    # title
    html.H1("dClimateVision", style={
        "text-align": "center",
        'fontSize': 42,
    }),


    # secondary dataset plot text
    html.H1("Plot primary element or analysis", style={
        'text-align': 'center',
        'fontSize': 16,
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
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",
              }
    ),

    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Dropdown(
            id='slct-dataset-type',
            options=VALID_DATASET_TYPES,
            placeholder="Select a primary dataset type",
            multi=False,
            value='',
            style={"display": "flex",
                    "justify-content": "center",
                    "align-items": "center",
                    "width" : "340px"
              }

        )
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",
              }),  # <-- This is the line that will be changed by the dropdown callback

    # if type of dataset selected has subsections, select specific dataset
    html.Div([
        dcc.Dropdown(
            id='datasets-to-hide',
            options=[],
            placeholder='Select a dataset',
            value=None,
            style={"display": "flex",
                   "justify-content": "center",
                   "align-items": "center",
                   "width": "60vh"
                   }
        )
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}),

        # if type of dataset selected has subsections, select specific dataset
    html.Div([
        dcc.Dropdown(
            id='forecasts-to-hide',
            options=[],
            placeholder='Select a forecast',
            value=None,
            style={"display": "flex",
                    "justify-content": "center",
                    "align-items": "center",
                    "width": "60vh"
                    }
        )
    ], style={"display": "flex",
                  "justify-content": "center",
                  "align-items": "center", }),

        # select sma interval size
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Input(
            id='slct-forecast_date',
            placeholder='Input a forecast date (YYYY-MM-DD)',
            value=None,
            size='50',
        )
    ], style={"display": "flex",
                "justify-content": "center",
                "align-items": "center", }  # <-- This is the line that will be changed by the dropdown callback
    ),

    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Input(
            id='slct-ghcn',
            placeholder='Input a GHCN Station',
            value=None,
            size='50',
        )
    ], style={"display": "flex",
              "justify-content": "center",
              "align-items": "center", }  # <-- This is the line that will be changed by the dropdown callback
    ),

    # lat
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Input(
            id='lat-to-hide',
            placeholder='Enter a Latitude',
            value=None,
            size='50',
        )
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}),  # <-- This is the line that will be changed by the dropdown callback

    # long
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Input(
            id='long-to-hide',
            placeholder='Enter a longitude',
            value=None,
            size='50',
        )
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # normal date range
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.DatePickerRange(
            id='daterange-to-hide',
            min_date_allowed=datetime(1980, 1, 1),
            max_date_allowed=datetime.today(),
            start_date=None,
            end_date=datetime.today()

        ),
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # weather variable
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Dropdown(
            id='variable-to-hide',
            options=[],
            placeholder='Select a weather variable',
            value=None,
        )
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # station id
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Dropdown(
            id='station-to-hide',
            options=[],
            placeholder='Select a station id',
            value=None,
        )
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # select analysis type dcc
    html.Div([
        dcc.Dropdown(
            id='slct-analysis-type',
            options=VALID_ANALYSIS_TYPES,
            placeholder="Select an analysis type",
            multi=False,
            value=None,
        ),
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}
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
        ),
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}  # <-- This is the line that will be changed by the dropdown callback
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
        ),
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # select sma interval size
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Input(
            id='slct-sma-size',
            placeholder='Input # of points to average',
            value=None,
            size='50',
        )
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # select sma interval size
    html.Div([
            # Create element to hide/show, in this case an 'Input Component'
        dcc.Input(
            id='slct-extrema-size',
            placeholder='Input # of points to check',
            value=None,
            size='50',
    )
    ], style={"display": "flex",
              "justify-content": "center",
              "align-items": "center", }  # <-- This is the line that will be changed by the dropdown callback
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
        ),
    ], style={'display': 'None'}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # secondary dataset plot text
    html.H1("Plot secondary element or analysis?", style={
        'text-align': 'center',
        'fontSize': 16,

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
    ], style={ "display": "flex",
        "justify-content": "center",
        "align-items": "center",
              }
    ),

    # select whether to plot analysis OR raw element
    html.Div([
        dcc.RadioItems(
            id='secondary-analysis-or-raw',
            options=[
                {'label': 'Raw element', 'value': 'Raw element'},
                {'label': 'Analysis of an element', 'value': 'Analysis of an element'},
            ],
            value='Raw element',
        )
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}
    ),

    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Dropdown(
            id='slct-dataset-type2',
            options=VALID_DATASET_TYPES,
            placeholder="Select a secondary dataset type",
            multi=False,
            value='',
        )
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}),  # <-- This is the line that will be changed by the dropdown callback

    # if type of dataset selected has subsections, select specific dataset
    html.Div([
        dcc.Dropdown(
            id='datasets-to-hide2',
            options=[],
            placeholder='Select a dataset',
            value=None,
        )
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}),

    # if type of dataset selected has subsections, select specific dataset
    html.Div([
        dcc.Dropdown(
            id='forecasts-to-hide2',
            options=[],
            placeholder='Select a forecast',
            value=None,
            style={"display": "flex",
                    "justify-content": "center",
                    "align-items": "center",
                    "width": "60vh"
                    }
        )
    ], style={"display": "flex",
                "justify-content": "center",
                "align-items": "center", }),

    # select sma interval size
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Input(
            id='slct-forecast_date2',
            placeholder='Input a forecast date (YYYY-MM-DD format)',
            value=None,
            size='50',
        )
    ], style={"display": "flex",
              "justify-content": "center",
              "align-items": "center", }  # <-- This is the line that will be changed by the dropdown callback
        ),

    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Input(
            id='slct-ghcn2',
            placeholder='Input a GHCN Station',
            value=None,
            size='50',
         )
    ], style={"display": "flex",
              "justify-content": "center",
              "align-items": "center", }  # <-- This is the line that will be changed by the dropdown callback
        ),

        # lat
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Input(
            id='lat-to-hide2',
            placeholder='Enter a latitude',
            value=None,
            size='50',
        )
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}),  # <-- This is the line that will be changed by the dropdown callback

    # long
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Input(
            id='long-to-hide2',
            placeholder='Enter a longitude',
            value=None,
            size='50',
        )
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # normal date range
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.DatePickerRange(
            id='daterange-to-hide2',
            min_date_allowed=datetime(1980, 1, 1),
            max_date_allowed=datetime.today(),
            start_date=None,
            end_date=datetime.today()

        ),
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # weather variable
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Dropdown(
            id='variable-to-hide2',
            options=[],
            placeholder='Select a weather variable',
            value=None,
        )
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # station id
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Dropdown(
            id='station-to-hide2',
            options=[],
            placeholder='Select a station id',
            value=None,
        )
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # select analysis type dcc
    html.Div([
        dcc.Dropdown(
            id='slct-analysis-type2',
            options=VALID_ANALYSIS_TYPES,
            placeholder="Select an analysis type",
            multi=False,
            value=None,
        ),
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}
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
        ),
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}  # <-- This is the line that will be changed by the dropdown callback
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
        ),
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # select sma interval size
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Input(
            id='slct-sma-size2',
            placeholder='Input a number of points to average',
            value=None,
            size='50',
        )
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}  # <-- This is the line that will be changed by the dropdown callback
    ),

    # select sma interval size
    html.Div([
        # Create element to hide/show, in this case an 'Input Component'
        dcc.Input(
            id='slct-extrema-size2',
            placeholder='Input a number of points to check',
            value=None,
            size='50',
        )
    ], style={"display": "flex",
              "justify-content": "center",
              "align-items": "center", }  # <-- This is the line that will be changed by the dropdown callback
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
        ),
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center",}  # <-- This is the line that will be changed by the dropdown callback
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
    ], style={"display": "flex",
        "justify-content": "center",
        "align-items": "center"}
    ),

    html.Div([
        # plot figure
        html.H3("Incomplete query. Fill all fields to fetch data.", id="warning", style={'fontSize': 16}),
    ], style={
        'display': 'flex', "justify-content": "center", "align-items": "center",
    }
    ),

    html.Div([
        # plot figure
        dcc.Graph(id='my_series_graph', style={'width': '90vw', 'height': '64vh', 'textAlign': 'center', "border":"1px black solid"}, figure={}),

    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', "border":"2px white solid"}),

    html.Div([
        # plot figure
        html.A("github.com/adamfil/dclimatevision", href='https://github.com/adamfil/dclimatevision'),
        ], style={
            'display': 'flex', "justify-content": "center", "align-items": "center"
        }
    ),



])])

@app.callback(
   [
       Output(component_id='datasets-to-hide', component_property='style'),
       Output(component_id='forecasts-to-hide', component_property='style'),
       Output(component_id='lat-to-hide', component_property='style'),
       Output(component_id='long-to-hide', component_property='style'),
       Output(component_id='daterange-to-hide', component_property='style'),
       Output(component_id='variable-to-hide', component_property='style'),
       Output(component_id='station-to-hide', component_property='style'),
       Output(component_id='slct-ghcn', component_property='style'),
   ],

   [Input(component_id='slct-dataset-type', component_property='value')])


def show_relevant_parameters_primary(slctd_dataset_type):

    if slctd_dataset_type in ['Grid File Dataset History']:
        return {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'none'}, {"display": "flex",
        "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}


    if slctd_dataset_type in ['GFS Forecasts']:
        return {'display': 'none'}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {"display": "flex",
        "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

    if slctd_dataset_type in ['Dutch Station History', 'CME Station History', 'German Station History']:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'none'}

    if slctd_dataset_type in ['GHCN Dataset History']:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'none'}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}

    else:
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

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
       Output(component_id='forecasts-to-hide', component_property='options'),
   ],

   [Input(component_id='slct-dataset-type', component_property='value')])


def update_forecast_input_primary(slctd_dataset_type):

    if slctd_dataset_type in ['GFS Forecasts']:
        return [VALID_GFS_DASHSET]
    else:
        pass

@app.callback(
   [
       Output(component_id='forecasts-to-hide2', component_property='options'),
   ],

   [Input(component_id='slct-dataset-type2', component_property='value')])


def update_forecast_input_secondary(slctd_dataset_type):

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

#update input parameters based on analysis type selected
@app.callback(
   [
       Output(component_id='slct-forecast_date', component_property='style'),
   ],

   [Input(component_id='slct-dataset-type', component_property='value')])


def update_forecast_input(input):

    #select parameters to display for histograms
    if input in ['GFS Forecasts']:
        return [{'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}]

    else:
        return [{'display': 'none'}]

#update input parameters based on analysis type selected
@app.callback(
   [
       Output(component_id='slct-forecast_date2', component_property='style'),
   ],

   [Input(component_id='slct-dataset-type2', component_property='value'),
    Input(component_id='secondary-or-no', component_property='value')])


def update_forecast_input2(input1, input2):
    if input2 in ["No"]:
        return [{'display': 'none'}]

    #select parameters to display for histograms
    elif input1 in ['GFS Forecasts']:
        return [{'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}]

    else:
        return [{'display': 'none'}]

#update primary input based on whether analysis or raw element is selected
@app.callback(
   [
       Output(component_id='slct-analysis-type', component_property='style')
   ],

   [Input(component_id='primary-analysis-or-raw', component_property='value')])


def update_analysis_or_raw(input):

    if input in ['Analysis of an element']:
        return [{'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}]

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
        return [{'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}]

    if input1 in ['Raw element']:
        return [{'display': 'none'}]

#update input parameters based on analysis type selected
@app.callback(
   [
       Output(component_id='slct-bin-size', component_property='style'),
       Output(component_id='slct-scatterplot-size', component_property='style'),
       Output(component_id='slct-sma-size', component_property='style'),
       Output(component_id='slct-extrema-size', component_property='style'),
       Output(component_id='slct-diff-size', component_property='style'),
   ],

   [Input(component_id='slct-analysis-type', component_property='value'),
    Input(component_id='primary-analysis-or-raw', component_property='value')])


def update_analysis_or_raw1(input1, input2):

    #show no parameters if raw element is selected
    if input2 in ['Raw element']:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]

    #select parameters to display for histograms
    if input1 in ['Histogram - sum', 'Histogram - average']:
        return [{'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]

    #select parameters to display for scatterplots
    if input1 in ['Interval scatterplot - sum', 'Interval scatterplot - average']:
        return [{'display': 'none'},{'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]

    #select parameters to display for SMA
    if input1 in ['Simple Moving Average']:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'none'}, {'display': 'none'}]

    #select parameters to display for diff plot
    if input1 in ['Difference of element']:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}]

    #select parameters to display for diff plot
    if input1 in ['Show Extrema']:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'none'}]

    #display no parameters
    if input1 in ['']:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]

#update input parameters based on analysis type selected
@app.callback(
   [
       Output(component_id='slct-bin-size2', component_property='style'),
       Output(component_id='slct-scatterplot-size2', component_property='style'),
       Output(component_id='slct-sma-size2', component_property='style'),
       Output(component_id='slct-extrema-size2', component_property='style'),
       Output(component_id='slct-diff-size2', component_property='style'),
   ],

   [Input(component_id='slct-analysis-type2', component_property='value'),
    Input(component_id='secondary-analysis-or-raw', component_property='value'),
    Input(component_id='secondary-or-no', component_property='value')])


def update_analysis_or_raw2(input1, input2, input3):

    #show no parameters if raw element is selected
    if input3 in ['No']:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]

    #show no parameters if raw element is selected
    if input2 in ['Raw element']:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]

    #select parameters to display for histograms
    if input1 in ['Histogram - sum', 'Histogram - average']:
        return [{'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]

    #select parameters to display for scatterplots
    if input1 in ['Interval scatterplot - sum', 'Interval scatterplot - average']:
        return [{'display': 'none'}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]

    #select parameters to display for SMA
    if input1 in ['Simple Moving Average']:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'none'}, {'display': 'none'}]

    #select parameters to display for diff plot
    if input1 in ['Difference of element']:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}]

    #select parameters to display for diff plot
    if input1 in ['Show Extrema']:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'none'}]

    #display no parameters
    if input1 in ['']:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]

#show/hide secondary selection of raw element vs analysis of an element
@app.callback(
   [
       Output(component_id='secondary-analysis-or-raw', component_property='style')
   ],

   [Input(component_id='secondary-or-no', component_property='value')])


def update_analysis_or_raw(input):

    if input in ['Yes']:
        return [{'display': 'flex', "justify-content": "center", "align-items": "center"}]

    if input in ['No']:
        return [{'display': 'none'}]


@app.callback(
   [
       Output(component_id='datasets-to-hide2', component_property='style'),
       Output(component_id='forecasts-to-hide2', component_property='style'),
       Output(component_id='lat-to-hide2', component_property='style'),
       Output(component_id='long-to-hide2', component_property='style'),
       Output(component_id='daterange-to-hide2', component_property='style'),
       Output(component_id='variable-to-hide2', component_property='style'),
       Output(component_id='station-to-hide2', component_property='style'),
       Output(component_id='slct-dataset-type2', component_property='style'),
       Output(component_id='axis-or-no', component_property='style'),
       Output(component_id='slct-ghcn2', component_property='style'),
   ],

   [Input(component_id='slct-dataset-type2', component_property='value'),
    Input(component_id='secondary-or-no', component_property='value')])


def show_relevant_parameters_secondary(slctd_dataset_type, second_input):
    # if no secondary input is selected, show no parameters
    if second_input == 'No':
        return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

    else:
        # show relevant parameters for dataset type
        if slctd_dataset_type in ['Grid File Dataset History']:
            return {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'none'}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'none'}, {'display': 'none'}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'none'}

        if slctd_dataset_type in ['GFS Forecasts']:
            return {'display': 'none'}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'none'}

        # show relevant parameters for dataset type
        if slctd_dataset_type in ['Dutch Station History', 'CME Station History', 'German Station History']:
            return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH},{'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'none'}

        # show relevant parameters for dataset type
        if slctd_dataset_type in ['GHCN Dataset History']:
            return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH},{'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'none'}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}

        # if no data type is selected but secondary input is yes, only show option to select data type
        if slctd_dataset_type in ['']:
            return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'flex', "justify-content": "center", "align-items": "center", "width": INPUT_WIDTH}, {'display': 'none'}

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
        Input(component_id='slct-dataset-type', component_property='value'),
        Input(component_id='datasets-to-hide', component_property='value'),
    ]
)

def update_daterange1(slctd_dataset_type, slctd_dataset):

    if slctd_dataset_type in ['Grid File Dataset History', 'GFS Forecasts']:
        daterange = helper.get_date_range(slctd_dataset, TOKEN)

        mindr = daterange[0]
        maxdr = daterange[1]

        return mindr, maxdr, mindr, maxdr

    if slctd_dataset_type in ['Dutch Station History', 'CME Station History', 'German Station History', 'GHCN Dataset History']:

        return None, datetime.today(), None, datetime.today()

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

        return None, datetime.today(), None, datetime.today()

    else:
        pass

#callback to produce graph
@app.callback(
    [
        Output(component_id='warning', component_property='style'),
    ],
    [
        Input(component_id='primary-analysis-or-raw', component_property='value'),
        Input(component_id='secondary-analysis-or-raw', component_property='value'),
        Input(component_id='slct-dataset-type', component_property='value'),
        Input(component_id='datasets-to-hide', component_property='value'),
        Input(component_id='forecasts-to-hide', component_property='value'),
        Input(component_id='slct-forecast_date', component_property='value'),
        Input(component_id='slct-ghcn', component_property='value'),
        Input(component_id='lat-to-hide', component_property='value'),
        Input(component_id='long-to-hide', component_property='value'),
        Input(component_id='station-to-hide', component_property='value'),
        Input(component_id='variable-to-hide', component_property='value'),
        Input(component_id='slct-dataset-type2', component_property='value'),
        Input(component_id='datasets-to-hide2', component_property='value'),
        Input(component_id='forecasts-to-hide2', component_property='value'),
        Input(component_id='slct-forecast_date2', component_property='value'),
        Input(component_id='slct-ghcn2', component_property='value'),
        Input(component_id='lat-to-hide2', component_property='value'),
        Input(component_id='long-to-hide2', component_property='value'),
        Input(component_id='station-to-hide2', component_property='value'),
        Input(component_id='variable-to-hide2', component_property='value'),
        Input(component_id='slct-analysis-type', component_property='value'),
        Input(component_id='slct-analysis-type2', component_property='value'),
        Input(component_id='slct-bin-size', component_property='value'),
        Input(component_id='slct-scatterplot-size', component_property='value'),
        Input(component_id='slct-sma-size', component_property='value'),
        Input(component_id='slct-extrema-size', component_property='value'),
        Input(component_id='slct-diff-size', component_property='value'),
        Input(component_id='slct-bin-size2', component_property='value'),
        Input(component_id='slct-scatterplot-size2', component_property='value'),
        Input(component_id='slct-sma-size2', component_property='value'),
        Input(component_id='slct-extrema-size2', component_property='value'),
        Input(component_id='slct-diff-size2', component_property='value'),
        Input(component_id='secondary-or-no', component_property='value'),
        Input(component_id='axis-or-no', component_property='value'),
        Input(component_id='primary-analysis-or-raw', component_property='style'),
        Input(component_id='secondary-analysis-or-raw', component_property='style'),
        Input(component_id='slct-dataset-type', component_property='style'),
        Input(component_id='datasets-to-hide', component_property='style'),
        Input(component_id='forecasts-to-hide', component_property='style'),
        Input(component_id='slct-forecast_date', component_property='style'),
        Input(component_id='slct-ghcn', component_property='style'),
        Input(component_id='lat-to-hide', component_property='style'),
        Input(component_id='long-to-hide', component_property='style'),
        Input(component_id='station-to-hide', component_property='style'),
        Input(component_id='variable-to-hide', component_property='style'),
        Input(component_id='slct-dataset-type2', component_property='style'),
        Input(component_id='datasets-to-hide2', component_property='style'),
        Input(component_id='forecasts-to-hide2', component_property='style'),
        Input(component_id='slct-forecast_date2', component_property='style'),
        Input(component_id='slct-ghcn2', component_property='style'),
        Input(component_id='lat-to-hide2', component_property='style'),
        Input(component_id='long-to-hide2', component_property='style'),
        Input(component_id='station-to-hide2', component_property='style'),
        Input(component_id='variable-to-hide2', component_property='style'),
        Input(component_id='slct-analysis-type', component_property='style'),
        Input(component_id='slct-analysis-type2', component_property='style'),
        Input(component_id='slct-bin-size', component_property='style'),
        Input(component_id='slct-scatterplot-size', component_property='style'),
        Input(component_id='slct-sma-size', component_property='style'),
        Input(component_id='slct-extrema-size', component_property='style'),
        Input(component_id='slct-diff-size', component_property='style'),
        Input(component_id='slct-bin-size2', component_property='style'),
        Input(component_id='slct-scatterplot-size2', component_property='style'),
        Input(component_id='slct-sma-size2', component_property='style'),
        Input(component_id='slct-extrema-size2', component_property='style'),
        Input(component_id='slct-diff-size2', component_property='style'),
    ]
)
def update_warning(analysis_or_raw1, analysis_or_raw2, dataset_type_slctd1, dataset_slctd1, forecast_slctd1, forecast_date_slctd1, ghcn_slctd1, lat_slctd1, long_slctd1,
                 station_slctd1, variable_slctd1, dataset_type_slctd2, dataset_slctd2, forecast_slctd2, forecast_date_slctd2, ghcn_slctd2,
                 lat_slctd2, long_slctd2, station_slctd2, variable_slctd2, anal_type_1, anal_type_2, bin_size1, scatter_size1, sma_size1, extrema_size1, diff_size1, bin_size2, scatter_size2, sma_size2, extrema_size2, diff_size2,
                 second_or_no, axis_or_no, analysis_or_raw1s=None, analysis_or_raw2s=None, dataset_type_slctd1s=None, dataset_slctd1s=None, forecast_slctd1s=None, forecast_date_slctd1s=None, ghcn_slctd1s=None, lat_slctd1s=None, long_slctd1s=None,
                 station_slctd1s=None, variable_slctd1s=None, dataset_type_slctd2s=None, dataset_slctd2s=None, forecast_slctd2s=None, forecast_date_slctd2s=None, ghcn_slctd2s=None,
                 lat_slctd2s=None, long_slctd2s=None, station_slctd2s=None, variable_slctd2s=None, anal_type_1s=None, anal_type_2s=None, bin_size1s=None, scatter_size1s=None, sma_size1s=None, extrema_size1s=None, diff_size1s=None, bin_size2s=None, scatter_size2s=None, sma_size2s=None, extrema_size2s=None, diff_size2s=None):

    values = [analysis_or_raw1, analysis_or_raw2, dataset_type_slctd1, dataset_slctd1, forecast_slctd1, forecast_date_slctd1, ghcn_slctd1, lat_slctd1, long_slctd1,
                 station_slctd1, variable_slctd1, dataset_type_slctd2, dataset_slctd2, forecast_slctd2, forecast_date_slctd2, ghcn_slctd2,
                 lat_slctd2, long_slctd2, station_slctd2, variable_slctd2, anal_type_1, anal_type_2, bin_size1, scatter_size1, sma_size1, extrema_size1, diff_size1, bin_size2, scatter_size2, sma_size2, extrema_size2, diff_size2]

    styles = [analysis_or_raw1s, analysis_or_raw2s, dataset_type_slctd1s, dataset_slctd1s, forecast_slctd1s, forecast_date_slctd1s, ghcn_slctd1s, lat_slctd1s, long_slctd1s,
                 station_slctd1s, variable_slctd1s, dataset_type_slctd2s, dataset_slctd2s, forecast_slctd2s, forecast_date_slctd2s, ghcn_slctd2s,
                 lat_slctd2s, long_slctd2s, station_slctd2s, variable_slctd2s, anal_type_1s, anal_type_2s, bin_size1s, scatter_size1s, sma_size1s, extrema_size1s, diff_size1s, bin_size2s, scatter_size2s, sma_size2s, extrema_size2s, diff_size2s]

    for i in range(len(values)):
        if styles[i] in [{'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'width': '340px'}]:
            if values[i] in [None, '']:
                return [{'display': 'flex', "justify-content": "center", "align-items": "center", "font-size": "16px"}]
            else:
                pass
        else:
            pass
    return [{'display': 'none'}]

#callback to produce graph
@app.callback(
    [
        Output(component_id='my_series_graph', component_property='figure'),
        Output(component_id='my_series_graph', component_property='style')
    ],
    [
        Input(component_id='primary-analysis-or-raw', component_property='value'),
        Input(component_id='secondary-analysis-or-raw', component_property='value'),
        Input(component_id='slct-dataset-type', component_property='value'),
        Input(component_id='datasets-to-hide', component_property='value'),
        Input(component_id='forecasts-to-hide', component_property='value'),
        Input(component_id='slct-forecast_date', component_property='value'),
        Input(component_id='slct-ghcn', component_property='value'),
        Input(component_id='daterange-to-hide', component_property='start_date'),
        Input(component_id='daterange-to-hide', component_property='end_date'),
        Input(component_id='lat-to-hide', component_property='value'),
        Input(component_id='long-to-hide', component_property='value'),
        Input(component_id='station-to-hide', component_property='value'),
        Input(component_id='variable-to-hide', component_property='value'),
        Input(component_id='slct-dataset-type2', component_property='value'),
        Input(component_id='datasets-to-hide2', component_property='value'),
        Input(component_id='forecasts-to-hide2', component_property='value'),
        Input(component_id='slct-forecast_date2', component_property='value'),
        Input(component_id='slct-ghcn2', component_property='value'),
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
        Input(component_id='slct-extrema-size', component_property='value'),
        Input(component_id='slct-diff-size', component_property='value'),
        Input(component_id='slct-bin-size2', component_property='value'),
        Input(component_id='slct-scatterplot-size2', component_property='value'),
        Input(component_id='slct-sma-size2', component_property='value'),
        Input(component_id='slct-extrema-size2', component_property='value'),
        Input(component_id='slct-diff-size2', component_property='value'),
        Input(component_id='secondary-or-no', component_property='value'),
        Input(component_id='axis-or-no', component_property='value'),
    ]
)

def update_graph(analysis_or_raw1, analysis_or_raw2, dataset_type_slctd1, dataset_slctd1, forecast_slctd1, forecast_date_slctd1, ghcn_slctd1, start_date_slctd1, end_date_slctd1, lat_slctd1, long_slctd1,
                 station_slctd1, variable_slctd1, dataset_type_slctd2, dataset_slctd2, forecast_slctd2, forecast_date_slctd2, ghcn_slctd2, start_date_slctd2, end_date_slctd2,
                 lat_slctd2, long_slctd2, station_slctd2, variable_slctd2, anal_type_1, anal_type_2, bin_size1, scatter_size1, sma_size1, extrema_size1, diff_size1, bin_size2, scatter_size2, sma_size2, extrema_size2, diff_size2,
                 second_or_no, axis_or_no):

    #1st thing to do, check query completeness. if incomplete return no graph. do the same thing in the parameter update column
    #status = QueryChecker()
    #if status is True:
        #input = InputQuery()
        #return [input.plot, {'display': 'flex', "justify-content": "center", "align-items": "center"}]
    #elif status is False:
        #return [None, {'display': 'None']

    input = InputQuery(second_or_no, dataset_type_slctd1, start_date_slctd1, end_date_slctd1, analysis_or_raw1, dataset_slctd1, forecast_slctd1, lat_slctd1, long_slctd1, station_slctd1, variable_slctd1, forecast_date_slctd1, ghcn_slctd1, anal_type_1, bin_size1,
                        scatter_size1, sma_size1, extrema_size1, analysis_or_raw2, dataset_type_slctd2, start_date_slctd2, end_date_slctd2, dataset_slctd2, forecast_slctd2, lat_slctd2, long_slctd2, station_slctd2, variable_slctd2, forecast_date_slctd2, ghcn_slctd2,
                        anal_type_2, bin_size2, scatter_size2, sma_size2, extrema_size2, axis_or_no)

    return [input.plot, {'display': 'flex', "justify-content": "center", "align-items": "center"}]

#add to above callback: if query_completeness = incomplete -> return graph display none, return container text "incomplete query". if query complete, return graph display flex + input.plot



if __name__ == '__main__':
    app.run_server(debug=False)
