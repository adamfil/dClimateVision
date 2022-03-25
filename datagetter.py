from vars import TOKEN
import pandas as pd
import requests
from datetime import datetime
import pytz


# given a series, and a start date and a end date, adjust series
#given a series, and a start date and a end date, adjust series
def trim_series(series, start, end):

    #deal with trimming timezone aware series... sloppy code as is
    if len(str(series.index[0])) == 25:

        start_year = int(start[0:4])
        start_month = int(start[5:7])
        start_day = int(start[8:10])
        end_year = int(end[0:4])
        end_month = int(end[5:7])
        end_day = int(end[8:10])

        start = datetime(start_year, start_month, start_day, 0, 0, 0, tzinfo=pytz.UTC)
        end = datetime(end_year, end_month, end_day, 0, 0, 0, tzinfo=pytz.UTC)
        series = series[start:end]
    else:
        series = series[start:end]
    return series


# get gridhistory series
def get_gridhistory_daily_series_snapped(dataset: str, latlong: tuple, my_token:str):
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

def get_gfs_series_snapped(dataset: str, latlong: tuple, my_token:str, forecast_date):
    print(dataset)
    print(latlong)
    print(forecast_date)
    lat = latlong[0]
    long = latlong[1]
    my_url = 'https://api.dclimate.net/apiv3/forecasts/' + dataset + '/' + str(lat) + '_' + str(long) + '?forecast_date=' + str(forecast_date)
    head = {"Authorization": TOKEN}
    r = requests.get(my_url, headers=head)
    data = r.json()["data"]
    index = pd.to_datetime(list(data.keys()))
    values = [float(s.split()[0]) if s else None for s in data.values()]
    series = pd.Series(values, index=index)
    snapped = r.json()["snapped to"]
    result = [snapped, series]
    return result

# get gridfile frame
def get_gfs_frame(lat_slctd, long_slctd, dataset_slctd, start_date_slctd, end_date_slctd, forecast_date):
    print('get gfs frame')
    print(lat_slctd)
    print(long_slctd)
    print(dataset_slctd)
    print(forecast_date)
    latlong = (lat_slctd, long_slctd)
    data_pulled = get_gfs_series_snapped(dataset_slctd, latlong, TOKEN, forecast_date)
    #dff = trim_series(data_pulled[1], start_date_slctd, end_date_slctd)
    dff = data_pulled

    snapped_lat = str(data_pulled[0][0])
    snapped_long = str(data_pulled[0][1])

    title = 'Dataset: {}'.format(dataset_slctd) + \
                '. Start date: {}'.format(start_date_slctd) + \
                '. End date: {}'.format(end_date_slctd) + \
                '. Snapped to Latitude: {}'.format(snapped_lat) + \
                '. Snapped to Longitude: {}'.format(snapped_long) + \
                '. Forecast date: {}'.format(forecast_date)

    dff = dff.to_frame(name='Value')
    dff['Datetime'] = dff.index

    return [dff, title]

# get station/variable series
def get_station_variable_series(dataset: str, station: str, variable: str, my_token:str):
    if dataset == 'Dutch Station History':
        my_url = 'https://api.dclimate.net/apiv3/dutch-station-history/'
    elif dataset == 'CME Station History':
        my_url = 'https://api.dclimate.net/apiv3/cme-history/'
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


def get_ghcn_series(ghcn, variable, my_token):
    my_url = 'https://api.dclimate.net/apiv3/ghcn-history/' + ghcn + '/' + variable
    head = {"Authorization": TOKEN}
    r = requests.get(my_url, headers=head)
    data = r.json()["data"]
    index = pd.to_datetime(list(data.keys()))
    values = [float(s.split()[0]) if s else None for s in data.values()]
    series = pd.Series(values, index=index)
    return series

# get gridfile frame
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


# get station frame
def get_station_frame(dataset_type_slctd, station_slctd, variable_slctd, start_date_slctd, end_date_slctd):

    title = 'Dataset: {}'.format(dataset_type_slctd) + \
                '. Station ID: {}'.format(station_slctd) + \
                '. Weather Variable: {}'.format(variable_slctd)
    data_pulled = get_station_variable_series(dataset_type_slctd, station_slctd, variable_slctd, TOKEN)
    dff = trim_series(data_pulled, start_date_slctd, end_date_slctd)

    dff = dff.to_frame(name='Value')
    dff['Datetime'] = dff.index

    return [dff, title]

def get_ghcn_frame(ghcn_slctd, variable_slctd, start_date_slctd, end_date_slctd):
    title = 'Dataset: {}'.format(ghcn_slctd) + \
                '. Weather Variable: {}'.format(variable_slctd)
    data_pulled = get_ghcn_series(ghcn_slctd, variable_slctd, TOKEN)
    dff = trim_series(data_pulled, start_date_slctd, end_date_slctd)

    dff = dff.to_frame(name='Value')
    dff['Datetime'] = dff.index

    return [dff, title]

# get data
def get_data(dataset_type_slctd, dataset_slctd, start_date_slctd, end_date_slctd, lat_slctd, long_slctd,
                 station_slctd, variable_slctd, forecast_date, forecast_slctd, ghcn_slctd):

    if dataset_type_slctd in ['Grid File Dataset History']:
        result = get_gridfile_frame(lat_slctd, long_slctd, dataset_slctd, start_date_slctd, end_date_slctd)

    if dataset_type_slctd in ['Dutch Station History', 'CME Station History', 'German Station History']:
        result = get_station_frame(dataset_type_slctd, station_slctd, variable_slctd, start_date_slctd,
                                          end_date_slctd)

    if dataset_type_slctd in ['GFS Forecasts']:
        result = get_gfs_frame(lat_slctd, long_slctd, forecast_slctd, start_date_slctd, end_date_slctd, forecast_date)

    if dataset_type_slctd in ['GHCN Dataset History']:
        result = get_ghcn_frame(ghcn_slctd, variable_slctd, start_date_slctd, end_date_slctd)

    return result
