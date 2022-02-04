TOKEN = 'REDACTED'

state_codes = {
  "10": "Delaware", "12": "Florida", "13": "Georgia", "15": "Hawaii", "16": "Idaho", "17": "Illinois", "18": "Indiana",
  "19": "Iowa", "20": "Kansas", "21": "Kentucky", "22": "Louisiana", "23": "Maine", "24": "Maryland",
  "25": "Massachusetts", "26": "Michigan", "27": "Minnesota", "28": "Mississippi", "29": "Missouri", "30": "Montana",
  "31": "Nebraska", "32": "Nevada", "33": "New Hampshire", "34": "New Jersey", "35": "New Mexico", "36": "New York",
  "37": "North Carolina", "38": "North Dakota", "39": "Ohio", "40": "Oklahoma", "41": "Oregon", "42": "Pennsylvania",
  "44": "Rhode Island", "45": "South Carolina", "46": "South Dakota", "47": "Tennessee", "48": "Texas", "49": "Utah",
  "50": "Vermont", "51": "Virginia", "53": "Washington", "54": "West Virginia", "55": "Wisconsin", "56": "Wyoming",
  "01": "Alabama", "02": "Alaska", "04": "Arizona", "05": "Arkansas", "06": "California", "08": "Colorado",
  "09": "Connecticut"
}

#define valid types of datasets

all_dataset_types = ['Grid File Dataset History', 'GFS Forecasts', 'GHCN Dataset History', 'CME Station History',
                       'Dutch Station History', 'German Station History', 'Tropical Storms Data', 'SCO Yield History',
                       'Transitional Yield Values', 'FSA Irrigation Data', 'Drought Monitor', 'Biomass']

VALID_DATASET_TYPES = []

VALID_DATASET_LIST = []

for set in all_dataset_types:
    if set in ['Grid File Dataset History', 'CME Station History', 'Dutch Station History']:
        VALID_DATASET_TYPES.append({'label': set, 'value': set})
        VALID_DATASET_LIST.append(set)
#usda rma codes currently left off valid dataset types

#'Grid File Dataset History', \
#need 1. dataset, 2. lat/long
valid_gridfile_set = ['vhi', 'prismc-tmax-daily', 'prismc-tmin-daily', 'prismc-precip-daily', 'rtma_dew_point-hourly',
             'rtma_pcp-hourly', 'rtma_temp-hourly', 'rtma_wind_u-hourly', 'rtma_wind_v-hourly', 'cpcc_precip_us-daily',
             'cpcc_precip_global-daily', 'cpcc_temp_max-daily', 'cpcc_temp_min-daily', 'chirpsc_final_05-daily',
             'chirpsc_final_25-daily',
             'chirpsc_prelim_05-daily', 'era5_land_2m_temp-hourly', 'era5_land_precip-hourly',
             'era5_land_surface_solar_radiation_downwards-hourly',
             'era5_land_snowfall-hourly', 'era5_land_wind_u-hourly', 'era5_land_wind_v-hourly',
             'era5_surface_runoff-hourly', 'era5_wind_100m_u-hourly',
             'era5_wind_100m_v-hourly', 'era5_volumetric_soil_water_layer_1-hourly']

VALID_GRIDFILE_DASHSET = []
VALID_GRIDFILE_LIST = []

for set in valid_gridfile_set:
    VALID_GRIDFILE_DASHSET.append({'label': set, 'value': set})
    VALID_GRIDFILE_LIST.append(set)

#'GFS Forecasts',\
#need 1. dataset, 2. lat/long

#valid GFS datasets

valid_gfs_set = ['gfs_10m_wind_u-hourly', 'gfs_10m_wind_v-hourly', 'gfs_pcp_rate-hourly', 'gfs_relative_humidity-hourly',
                 'gfs_tmax-hourly', 'gfs_tmin-hourly', 'gfs_volumetric_soil_moisture-hourly']

VALID_GFS_DASHSET = []

for set in valid_gfs_set:
    VALID_GFS_DASHSET.append({'label': set, 'value': set})



#'GHCN Dataset History', \
#need 1. station id and 2. weather variable

ghcn_station_url = 'https://gateway.arbolmarket.com/ipfs/QmXYLinhugGMqgZnzWFQZTG8mJtn93PtrM8E5F27qQ9sf7/stations.json'

valid_ghcn_stations = ['USW00003016']


VALID_GHCN_STATIONS = []
for station in valid_ghcn_stations:
    VALID_GHCN_STATIONS.append({'label': station, 'value': station})

valid_ghcn_variables = ['SNWD', 'SNOW', 'WESD', 'TMAX', 'TMIN', 'PRCP']

VALID_GHCN_VARIABLES = []
for variable in valid_ghcn_variables:
    VALID_GHCN_VARIABLES.append({'label': variable, 'value': variable})

#'CME Station History',
#need 1. station id and 2. weather variable
VALID_CME_STAT_LIST = ['03927', '13874', '14732', '14922', '23169', '23232', '24229',
                      '93814', '94846', '47662', '03772', '06240']

VALID_CME_STATIONS = []
for station in VALID_CME_STAT_LIST:
    VALID_CME_STATIONS.append({'label': station, 'value': station})

VALID_CME_VAR_LIST = ['TMAX', 'TMIN', 'TAVG']

VALID_CME_VARIABLES = []
for variable in VALID_CME_VAR_LIST:
    VALID_CME_VARIABLES.append({'label': variable, 'value': variable})
#'Dutch Station History',\
#need 1. station id and 2. weather variable
VALID_DUTCH_STAT_LIST = [209, 210, 215, 225, 229, 235, 240, 242, 248, 249, 251, 257, 258, 260, 265, 267, 269, 270, 273,
                        275, 277, 278, 279, 280, 283, 285, 286, 290, 308, 310, 311, 312, 313, 315, 316, 319, 323, 324,
                        330, 331, 340, 343, 344, 348, 350, 356, 370, 375, 377, 380, 391]

VALID_DUTCH_STATIONS = []
for station in VALID_DUTCH_STAT_LIST:
    VALID_DUTCH_STATIONS.append({'label': str(station), 'value': str(station)})

VALID_DUTCH_VAR_LIST = ['WINDSPEED', 'RADIATION', 'TMAX', 'TMIN', 'TAVG']

VALID_DUTCH_VARIABLES = []
for variable in VALID_DUTCH_VAR_LIST:
    VALID_DUTCH_VARIABLES.append({'label': variable, 'value': variable})

#'German Station History', \
#need 1. station id and 2. weather variable
valid_german_variables = ['TMAX', 'TMIN', 'TAVG', 'TMINGROUND', 'PRCP']

VALID_GERMAN_VARIABLES = []
for variable in valid_german_variables:
    VALID_GERMAN_VARIABLES.append({'label': variable, 'value': variable})

#'Tropical Storms Data', \
#need 1. source and 2. basin

#'SCO Yield History', \
#select 1. a state and 2. a county and THEN select a 3. commodity (use USDA RMA codes to get counties)

#'Transitional Yield Values', \
#select 1. a state and 2. a county and THEN select a 3. commodity (use USDA RMA codes to get counties)

#'FSA Irrigation Data', \
#slect 1. a commodity

#'Drought Monitor',
#select a state-county

#'Biomass'
# select a 1. year 2. lat/long and 3. unit

#Valid Analysis Types
valid_analysis_types = ['Histogram - sum', 'Histogram - average', 'Interval scatterplot - sum', 'Interval scatterplot - average', 'Simple Moving Average']

VALID_ANALYSIS_TYPES = []

for set in valid_analysis_types:
    VALID_ANALYSIS_TYPES.append({'label': set, 'value': set})



#Valid scatter sizes
VALID_SCATTERPLOT_INTERVALS = [{'label': 'Daily', 'value': 'D'}, {'label': 'Weekly', 'value': 'W'}, {'label': 'Monthly', 'value': 'M'}]

#Valid Histogram Bin Sizes
VALID_HISTOGRAM_BINS = [{'label': 'Daily', 'value': 'D'}, {'label': 'Weekly', 'value': 'W'}, {'label': 'Monthly', 'value': 'M'}]

VALID_HISTOGRAM_LIST = ['D', 'W', 'M']

VALID_SCATTERPLOT_LIST = ['D', 'W', 'M']

VALID_DIFF_INTERVALS = [{'label': 'Last observation', 'value': 'Last observation'}, {'label': '1 year ago', 'value': '1 year ago'}]


# to do:
#add seondaxisorno as var
