import requests
import pandas as pd
import numpy as np
import datetime
from datetime import datetime
from vars import TOKEN
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import argrelextrema


# given a grid history dataset, a valid lat/long tuple, and an
# authentication token, return data as series for that given lat/long
def get_gridhistory_daily_series(dataset: str, latlong: tuple, my_token: str):
    lat = latlong[0]
    long = latlong[1]
    my_url = 'https://api.dclimate.net/apiv3/grid-history/' + dataset + '/' + str(lat) + '_' + str(long)
    head = {"Authorization":TOKEN}
    r = requests.get(my_url, headers=head)
    data = r.json()["data"]
    index = pd.to_datetime(list(data.keys()))
    values = [float(s.split()[0]) if s else None for s in data.values()]
    series = pd.Series(values, index=index)
    return series

def get_gridhistory_daily_series_snapped(dataset: str, latlong: tuple, my_token: str):
    lat = latlong[0]
    long = latlong[1]
    my_url = 'https://api.dclimate.net/apiv3/grid-history/' + dataset + '/' + str(lat) + '_' + str(long)
    head = {"Authorization": TOKEN}
    r = requests.get(my_url, headers=head)
    data = r.json()["data"]
    index = pd.to_datetime(list(data.keys()))
    values = [float(s.split()[0]) if s else None for s in data.values()]
    series = pd.Series(values, index=index)
    snapped = r.json()["snapped to"]
    result = [snapped, series]
    return result

#manually get input frequency
def get_input_frequency(input):
    inputset = get_set_gridhistory_daily_series(input)
    series = inputset[input.latlongset[0]]
    return pd.to_timedelta(np.diff(series.index).min())



#given a series, and a start date and a end date, adjust series
def trim_series(series, start, end):
    series = series[start:end]
    return series

#given a dataset, output valid max/min lat/long

def get_lat_range(dataset: str, my_token: str):
    my_url = 'https://api.dclimate.net/apiv3/metadata/' + dataset + '?full_metadata=true'
    head = {"Authorization": TOKEN}
    r = requests.get(my_url, headers=head)
    data = r.json()['latitude range']
    return data

def get_long_range(dataset: str, my_token: str):
    my_url = 'https://api.dclimate.net/apiv3/metadata/' + dataset + '?full_metadata=true'
    head = {"Authorization": TOKEN}
    r = requests.get(my_url, headers=head)
    data = r.json()['longitude range']
    return data

def get_date_range(dataset: str, my_token: str):
    my_url = 'https://api.dclimate.net/apiv3/metadata/' + dataset + '?full_metadata=true'
    head = {"Authorization": TOKEN}
    r = requests.get(my_url, headers=head)
    if 'api documentation' in r.json().keys():
        data = r.json()['api documentation']
        if 'full date range' in data.keys():
            start_date = data['full date range'][0]
            start_date = start_date.split('-')
            year_start = int(start_date[0])
            month_start = int(start_date[1])
            day_start = start_date[2].split(' ')
            day_start = int(day_start[0])
            start_date = datetime(year_start, month_start, day_start)

            end_date = data['full date range'][1]
            end_date = end_date.split('-')
            year_end = int(end_date[0])
            month_end = int(end_date[1])
            day_end = end_date[2].split(' ')
            day_end = int(day_end[0])
            end_date = datetime(year_end, month_end, day_end)

            return [start_date, end_date]

        else:
            return [datetime(2000, 1, 1), datetime.today()]
        #deal with gridhistory datasets that dont have API documentation for daterange in metadata
    else:
        return [datetime(2000, 1, 1), datetime.today()]

def get_dataset_freq(dataset: str, my_token: str):
    my_url = 'https://api.dclimate.net/apiv3/metadata/' + dataset + '?full_metadata=true'
    head = {"Authorization": TOKEN}
    r = requests.get(my_url, headers=head)
    data = r.json()
    if 'update frequency' in data.keys():
        return data['update frequency']
    #deal with gridhistory datasets that dont update frequency in metadata
    else:
        return ''

def get_state_counties(state: str):
    my_url = 'https://api.dclimate.net/apiv3/rma-code-lookups/valid_counties/' + state
    head = {"Authorization": TOKEN}
    r = requests.get(my_url, headers=head)
    data = r.json()
    print(data)


def get_station_variable_series(dataset: str, station: str, variable: str, my_token:str):
    if dataset == 'Dutch Station History':
        my_url = 'https://api.dclimate.net/apiv3/dutch-station-history/'
    elif dataset == 'CME Station History':
        my_url = 'https://api.dclimate.net/apiv3/cme-history/'
    elif dataset == 'GHCN Dataset History':
        my_url = 'https://api.dclimate.net/apiv3/ghcn-history/'
    elif dataset == 'German Station History':
        my_url = 'https://api.dclimate.net/apiv3/german-station-history/'

    my_url = my_url + station + '/' + variable
    head = {"Authorization": TOKEN}
    r = requests.get(my_url, headers=head)
    data = r.json()["data"]
    index = pd.to_datetime(list(data.keys()))
    values = [float(s.split()[0]) if s else None for s in data.values()]
    series = pd.Series(values, index=index)
    return series


def get_gridfile_frame(lat_slctd, long_slctd, dataset_slctd, start_date_slctd, end_date_slctd):

    latlong = (lat_slctd, long_slctd)
    data_pulled = get_gridhistory_daily_series_snapped(dataset_slctd, latlong, TOKEN)
    dff = trim_series(data_pulled[1], start_date_slctd, end_date_slctd)

    snapped_lat = str(data_pulled[0][0])
    snapped_long = str(data_pulled[0][1])

    title = 'Dataset: {}'.format(dataset_slctd) + \
                '. Start date: {}'.format(start_date_slctd) + \
                '. End date: {}'.format(end_date_slctd) + \
                '. Snapped to Latitude: {}'.format(snapped_lat) + \
                '. Snapped to Longitude: {}'.format(snapped_long)

    dff = dff.to_frame(name='Value')
    dff['Datetime'] = dff.index

    return [dff, title]

def get_station_frame(dataset_type_slctd, station_slctd, variable_slctd, start_date_slctd, end_date_slctd):

    title = 'Dataset: {}'.format(dataset_type_slctd) + \
                '. Station ID: {}'.format(station_slctd) + \
                '. Weather Variable: {}'.format(variable_slctd)
    data_pulled = get_station_variable_series(dataset_type_slctd, station_slctd, variable_slctd, TOKEN)
    dff = trim_series(data_pulled, start_date_slctd, end_date_slctd)

    dff = dff.to_frame(name='Value')
    dff['Datetime'] = dff.index

    return [dff, title]


def make_sma_frame(frame, wind):
    frame['Value'] = frame.rolling(window=wind).mean()
    return frame

def get_single_plot(inputquery):

    info = get_graph_object_and_title(inputquery.data_query1, inputquery.analysis_query1, 'Primary dataset')

    go1 = info[0]
    title = info[1]

    analysis_title = ''

    # get title
    if inputquery.analysis_query1.analysis_or_raw == "Raw element":
        analysis_title = ''
    if inputquery.analysis_query1.analysis_or_raw == "Analysis of an element":
        analysis_title = inputquery.analysis_query1.anal_type + ' '

    if inputquery.data_query1.dataset_type == "Grid File Dataset History":
        dataset_title = inputquery.data_query1.gridfile_dataset
    else:
        dataset_title = inputquery.data_query1.dataset_type

    fig = make_subplots(specs=[[{"secondary_y": False}]])

    # Add traces
    fig.add_trace(
        go1
    )

    # Add figure title
    fig.update_layout(
        title_text=analysis_title + dataset_title
    )

    # Set x-axis title
    fig.update_xaxes(title_text='Datetime')

    # Set y-axes titles
    fig.update_yaxes(title_text='Value')

    return fig

def get_double_plot(inputquery):

    info1 = get_graph_object_and_title(inputquery.data_query1, inputquery.analysis_query1, 'Primary dataset')

    info2 = get_graph_object_and_title(inputquery.data_query2, inputquery.analysis_query2, 'Secondary dataset')

    go1 = info1[0]
    title1 = info1[1]

    go2 = info2[0]
    title2 = info2[1]

    analysis_title = ''
    analysis_title2 = ''

    #get title
    if inputquery.analysis_query1.analysis_or_raw == "Raw element":
        analysis_title = ''
    if inputquery.analysis_query1.analysis_or_raw == "Analysis of an element":
        analysis_title = inputquery.analysis_query1.anal_type + ' '

    if inputquery.analysis_query2.analysis_or_raw == "Raw element":
        analysis_title = ''
    if inputquery.analysis_query2.analysis_or_raw == "Analysis of an element":
        analysis_title2 = inputquery.analysis_query2.anal_type + ' '

    if inputquery.data_query1.dataset_type == "Grid File Dataset History":
        dataset_title = inputquery.data_query1.gridfile_dataset
    else:
        dataset_title = inputquery.data_query1.dataset_type

    if inputquery.data_query2.dataset_type == "Grid File Dataset History":
        dataset_title2 = inputquery.data_query2.gridfile_dataset
    else:
        dataset_title2 = inputquery.data_query2.dataset_type

    if inputquery.axis_status in ['Use secondary axis']:

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        fig.add_trace(
            go1,
            secondary_y=False
        )

        # Add traces
        fig.add_trace(
            go2,
            secondary_y=True
        )

        # Add figure title
        fig.update_layout(
            title_text='Primary: ' + analysis_title + dataset_title + ', Secondary: ' + analysis_title2 + dataset_title2
        )

        # Set x-axis title
        fig.update_xaxes(title_text='Datetime')

        # Set y-axes titles
        fig.update_yaxes(title_text='Value')



        return fig

    if inputquery.axis_status in ['Use same axis']:
        fig = make_subplots(specs=[[{"secondary_y": False}]])

        # Add traces
        fig.add_trace(
            go1
        )

        # Add traces
        fig.add_trace(
            go2
        )

        # Add figure title
        fig.update_layout(
            title_text='Primary: ' + analysis_title + dataset_title + ', Secondary: ' + analysis_title2 + dataset_title2
        )

        # Set x-axis title
        fig.update_xaxes(title_text='Datetime')

        # Set y-axes titles
        fig.update_yaxes(title_text='Value')

        return fig

def get_graph_object_and_title(dataquery, analysisquery, primary_or_secondary):

    #dataquery = DataQuery(dataset_type_slctd, start_date_slctd, end_date_slctd, dataset_slctd, lat_slctd, long_slctd, station_slctd, variable_slctd)

    #data = get_data(dataquery.dataset_type, dataquery.gridfile_dataset, dataquery.start_date, dataquery.end_date, dataquery.lat, dataquery.long, dataquery.station, dataquery.variable)

    data = dataquery.data

    frame = data[0]
    title = data[1]

    if analysisquery.analysis_or_raw in ['Raw element']:
        go1 = go.Scatter(x=frame['Datetime'], y=frame['Value'], name=primary_or_secondary + '')

    if analysisquery.analysis_or_raw in ['Analysis of an element']:

        if analysisquery.anal_type in ['Histogram - sum']:
            result = pd.DataFrame(frame)

            bucketed = result.resample(analysisquery.bin_size, on='Datetime').Value.sum()
            bucketed = pd.DataFrame(bucketed, columns=['Value'])

            go1 = go.Bar(x=bucketed.index, y=bucketed['Value'], name=primary_or_secondary + '')

        if analysisquery.anal_type in ['Histogram - average']:
            result = pd.DataFrame(frame)

            bucketed = result.resample(analysisquery.bin_size, on='Datetime').Value.mean()
            bucketed = pd.DataFrame(bucketed, columns=['Value'])

            go1 = go.Bar(x=bucketed.index, y=bucketed['Value'], name=primary_or_secondary + '')

        if analysisquery.anal_type in ['Interval scatterplot - sum']:
            result = pd.DataFrame(frame)

            bucketed = result.resample(analysisquery.scatter_size, on='Datetime').Value.sum()
            bucketed = pd.DataFrame(bucketed, columns=['Value'])

            go1 = go.Scatter(x=bucketed.index, y=bucketed['Value'], name=primary_or_secondary + '')

        if analysisquery.anal_type in ['Interval scatterplot - average']:
            result = pd.DataFrame(frame)

            bucketed = result.resample(analysisquery.scatter_size, on='Datetime').Value.mean()
            bucketed = pd.DataFrame(bucketed, columns=['Value'])

            go1 = go.Scatter(x=bucketed.index, y=bucketed['Value'], name=primary_or_secondary + '')


        if analysisquery.anal_type in ['Simple Moving Average']:

            result = pd.DataFrame(frame)

            window = int(analysisquery.sma_size)
            result[str(window) + ' moving average'] = result['Value'].rolling(window=window).mean()

            go1 = go.Scatter(x=result['Datetime'], y=result[str(window) + ' moving average'], name=primary_or_secondary + '')


    return go1, title


def get_data(dataset_type_slctd, dataset_slctd, start_date_slctd, end_date_slctd, lat_slctd, long_slctd,
                 station_slctd, variable_slctd):

    if dataset_type_slctd in ['Grid File Dataset History']:
        result = get_gridfile_frame(lat_slctd, long_slctd, dataset_slctd, start_date_slctd, end_date_slctd)


    if dataset_type_slctd in ['Dutch Station History', 'CME Station History', 'German Station History']:
        result = get_station_frame(dataset_type_slctd, station_slctd, variable_slctd, start_date_slctd,
                                          end_date_slctd)

    return result


#for plotting extrema
#Enter number of points to check for extrema in each direction
