import requests
import pandas as pd
import numpy as np
import datetime
from datetime import datetime
from vars import TOKEN


# given a grid history dataset, a valid lat/long tuple, and an
# authentication token, return data as series for that given lat/long
def get_gridhistory_daily_series(dataset: str, latlong: tuple, my_token: str):
    lat = latlong[0]
    long = latlong[1]
    my_url = 'https://api.dclimate.net/apiv3/grid-history/' + dataset + '/' + str(lat) + '_' + str(long)
    head = {"Authorization": my_token}
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
    head = {"Authorization": my_token}
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

def get_date_range(dataset: str, my_token: str):
    my_url = 'https://api.dclimate.net/apiv3/metadata/' + dataset + '?full_metadata=true'
    head = {"Authorization": my_token}
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
    head = {"Authorization": my_token}
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
    head = {"Authorization": my_token}
    r = requests.get(my_url, headers=head)
    data = r.json()["data"]
    index = pd.to_datetime(list(data.keys()))
    values = [float(s.split()[0]) if s else None for s in data.values()]
    series = pd.Series(values, index=index)
    return series
