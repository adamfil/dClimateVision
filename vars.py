'''
vars.py is our file for defining all global variables related to dclimatevision and the dclimate api
'''

#api key
TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjI1MzQwMjMwMDc5OSwiaWF0IjoxNjMwNTMwMTgwLCJzdWIiOiJhMDIzYjUwYi0wOGQ2LTQwY2QtODNiMS1iMTExZDA2Mzk1MmEifQ.qHy4B0GK22CkYOTO8gsxh0YzE8oLMMa6My8TvhwhxMk'

### rma variables ###
#rma state codes
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

### all datasets ###
#defining all valid datasets avialable
all_dataset_types = ['Grid File Dataset History', 'GFS Forecasts', 'GHCN Dataset History', 'CME Station History',
                       'Dutch Station History', 'German Station History', 'Tropical Storms Data', 'SCO Yield History',
                       'Transitional Yield Values', 'FSA Irrigation Data', 'Drought Monitor', 'Biomass']

#creating a LIST and a DICT-LIST for the subset of datasets which we want to be available in our app.
VALID_DATASET_TYPES = []
VALID_DATASET_LIST = []
for set in ['Grid File Dataset History', 'CME Station History', 'Dutch Station History', 'GFS Forecasts', 'GHCN Dataset History']:
    VALID_DATASET_TYPES.append({'label': set, 'value': set})
    VALID_DATASET_LIST.append(set)

### gridfile datasets ###
#defining all valid gridfile datasets available
valid_gridfile_set = ['vhi', 'prismc-tmax-daily', 'prismc-tmin-daily', 'prismc-precip-daily', 'rtma_dew_point-hourly',
             'rtma_pcp-hourly', 'rtma_temp-hourly', 'rtma_wind_u-hourly', 'rtma_wind_v-hourly', 'cpcc_precip_us-daily',
             'cpcc_precip_global-daily', 'cpcc_temp_max-daily', 'cpcc_temp_min-daily', 'chirpsc_final_05-daily',
             'chirpsc_final_25-daily',
             'chirpsc_prelim_05-daily', 'era5_land_2m_temp-hourly', 'era5_land_precip-hourly',
             'era5_land_surface_solar_radiation_downwards-hourly',
             'era5_land_snowfall-hourly', 'era5_land_wind_u-hourly', 'era5_land_wind_v-hourly',
             'era5_surface_runoff-hourly', 'era5_wind_100m_u-hourly',
             'era5_wind_100m_v-hourly', 'era5_volumetric_soil_water_layer_1-hourly']

#creating a LIST and a DICT-LIST for the set of gridfile datasets which we want to be available in our app.
VALID_GRIDFILE_DASHSET = []
VALID_GRIDFILE_LIST = []
for set in valid_gridfile_set:
    VALID_GRIDFILE_DASHSET.append({'label': set, 'value': set})
    VALID_GRIDFILE_LIST.append(set)

### gfs datasets###
#defining all valid gfs datasets
valid_gfs_set = ['gfs_10m_wind_u-hourly', 'gfs_10m_wind_v-hourly', 'gfs_pcp_rate-hourly', 'gfs_relative_humidity-hourly',
                 'gfs_tmax-hourly', 'gfs_tmin-hourly', 'gfs_volumetric_soil_moisture-hourly']

#creating a DICT-LIST for the gfs datasets which we will use in our app
VALID_GFS_DASHSET = []
for set in valid_gfs_set:
    VALID_GFS_DASHSET.append({'label': set, 'value': set})



### ghcn datasets###
#ghcn station list --- we can see all ghcn stations here (extremely long list, so currently unused. in the future, one thing which is possible is doing a ghcn input / json lookup to confirm it is a valid station)
ghcn_station_url = 'https://gateway.arbolmarket.com/ipfs/QmXYLinhugGMqgZnzWFQZTG8mJtn93PtrM8E5F27qQ9sf7/stations.json'

#defining all ghcn variables list
valid_ghcn_variables = ['SNWD', 'SNOW', 'WESD', 'TMAX', 'TMIN', 'PRCP']
#creating a DICT-LIST for the ghcn valid variables
VALID_GHCN_VARIABLES = []
for variable in valid_ghcn_variables:
    VALID_GHCN_VARIABLES.append({'label': variable, 'value': variable})

#### cme stations
#defining valid cme stations
VALID_CME_STAT_LIST = ['03927', '13874', '14732', '14922', '23169', '23232', '24229',
                      '93814', '94846', '47662', '03772', '06240']
#creating DICT-LIST for all valid cme stations for use in app
VALID_CME_STATIONS = []
for station in VALID_CME_STAT_LIST:
    VALID_CME_STATIONS.append({'label': station, 'value': station})
#defining valid cme variables
VALID_CME_VAR_LIST = ['TMAX', 'TMIN', 'TAVG']
#creating dict-list of valid cme vars for use in app
VALID_CME_VARIABLES = []
for variable in VALID_CME_VAR_LIST:
    VALID_CME_VARIABLES.append({'label': variable, 'value': variable})

### Dutch Station History ###
#defining valid dutch stations
VALID_DUTCH_STAT_LIST = [209, 210, 215, 225, 229, 235, 240, 242, 248, 249, 251, 257, 258, 260, 265, 267, 269, 270, 273,
                        275, 277, 278, 279, 280, 283, 285, 286, 290, 308, 310, 311, 312, 313, 315, 316, 319, 323, 324,
                        330, 331, 340, 343, 344, 348, 350, 356, 370, 375, 377, 380, 391]
#creating DICT-LIST of valid dutch stats for use in app
VALID_DUTCH_STATIONS = []
for station in VALID_DUTCH_STAT_LIST:
    VALID_DUTCH_STATIONS.append({'label': str(station), 'value': str(station)})
#defining valid dutch variables
VALID_DUTCH_VAR_LIST = ['WINDSPEED', 'RADIATION', 'TMAX', 'TMIN', 'TAVG']
#creating DICT-LIST of valid dutch vars for use in app
VALID_DUTCH_VARIABLES = []
for variable in VALID_DUTCH_VAR_LIST:
    VALID_DUTCH_VARIABLES.append({'label': variable, 'value': variable})

### German Station History ###
#defining valid german variables
valid_german_variables = ['TMAX', 'TMIN', 'TAVG', 'TMINGROUND', 'PRCP']
#creating DICT-LIST for valid german variables for use in app
VALID_GERMAN_VARIABLES = []
for variable in valid_german_variables:
    VALID_GERMAN_VARIABLES.append({'label': variable, 'value': variable})

### Global Variables for Analysis ###
#define all valid analysis types
valid_analysis_types = ['Histogram - sum', 'Histogram - average', 'Interval scatterplot - sum', 'Interval scatterplot - average', 'Simple Moving Average', 'Show Extrema']
#create DICT-LIST for valid analysis types
VALID_ANALYSIS_TYPES = []
for set in valid_analysis_types:
    VALID_ANALYSIS_TYPES.append({'label': set, 'value': set})

#define valid scatterplot intervals with DICT-LIST format for use in app
VALID_SCATTERPLOT_INTERVALS = [{'label': 'Daily', 'value': 'D'}, {'label': 'Weekly', 'value': 'W'}, {'label': 'Monthly', 'value': 'M'}]
#define valid histogram bins with DICT-LIST format for use in app
VALID_HISTOGRAM_BINS = [{'label': 'Daily', 'value': 'D'}, {'label': 'Weekly', 'value': 'W'}, {'label': 'Monthly', 'value': 'M'}]
#define valid histogram val list
VALID_HISTOGRAM_LIST = ['D', 'W', 'M']
#define validscatterplot val list
VALID_SCATTERPLOT_LIST = ['D', 'W', 'M']

VALID_DIFF_INTERVALS = [{'label': 'Last observation', 'value': 'Last observation'}, {'label': '1 year ago', 'value': '1 year ago'}]


