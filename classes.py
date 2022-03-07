from vars import VALID_DATASET_LIST, VALID_DUTCH_STAT_LIST, VALID_CME_STAT_LIST, VALID_DUTCH_VAR_LIST, VALID_CME_VAR_LIST, VALID_GRIDFILE_LIST, VALID_SCATTERPLOT_LIST, VALID_HISTOGRAM_LIST, valid_analysis_types
import datagetter
import helper
from functools import wraps
import inspect

def query_completeness_check(dataset_type, start_date, end_date, analysis_or_raw, gridfile_dataset, forecast_dataset,
                 lat, long, station, variable, forecast_date, anal_type, bin_size, scatter_size, sma_size, extrema_size):
    #make sure dataset is complete
    #deal with gridfile
    if dataset_type in ['Gridfile Dataset History']:
        if type(start_date) == str and type(end_date) == str and type(lat) == str and type(long) == str and type(gridfile_dataset) == str:
            status = True
        else:
            status = False

    #deal with stat/var dataset
    elif dataset_type in ['Dutch Station History', 'CME Station History']:
        if type(start_date) == str and type(end_date) == str and type(station) == str and type(variable) == str:
            status = True
        else:
            status = False
    #deal with gfs
    elif dataset_type in ['GFS Forecasts']:
        if type(forecast_date) == str and type(forecast_dataset) == str and type(lat) == str and type(long) == str:
            status = True
        else:
            status = False
    else:
        status = False

    #check if analysis or raw
    if analysis_or_raw in ['Raw Element']:
        pass
    elif analysis_or_raw is 'Analysis of an Element':
        #check input completeness
        if anal_type in [None]:
            status = False

        elif anal_type in ['Histogram - average', 'Histogram - sum']:
            if bin_size in ['D', 'W', 'M']:
                status = True
            else:
                status = False

        elif anal_type in ['Interval scatterplot - average', 'Interval scatterplot - sum']:
            if scatter_size in ['D', 'W', 'M']:
                status = True
            else:
                status = False

        elif anal_type in ['Simple Moving Average']:
            if type(sma_size) == str:
                status = True
            else:
                status = False

        elif anal_type in ['Show Extrema']:
            if type(extrema_size) == str:
                status = True
            else:
                status = False
    else:
        status = False


        #if analysis, make sure analysis query is complete
    return status


print(query_completeness_check('Gridfile Dataset History', '2000-12-12', '2001-12-12', 'Analysis of an Element', 'vhi', None, '40', '-120', None, None, None, 'Simple Moving Average', None, None, '20', None))

class QueryChecker:
    def __init__(self, single_or_double, dataset_type1: str, start_date1: str, end_date1: str, analysis_or_raw1=str, gridfile_dataset1=None, forecast_dataset1=None,
                 lat1=None, long1=None, station1=None, variable1=None, forecast_date1=None, anal_type1=None,
                 bin_size1=None, scatter_size1=None, sma_size1=None, extrema_size1=None, analysis_or_raw2=None, dataset_type2=None, start_date2=None, end_date2=None, gridfile_dataset2=None, forecast_dataset2=None,
                 lat2=None, long2=None, station2=None, variable2=None, forecast_date2=None, anal_type2=None,
                 bin_size2=None, scatter_size2=None, sma_size2=None, extrema_size2=None, axis_status=None):
        self.single_or_double = single_or_double
        self.dataset_type1 = dataset_type1
        self.start_date1 = start_date1
        self.end_date1 = end_date1
        self.analysis_or_raw1 = analysis_or_raw1
        self.gridfile_dataset1 = gridfile_dataset1
        self.forecast_dataset1 = forecast_dataset1
        self.lat1 = lat1
        self.long1 = long1
        self.station1 = station1
        self.variable1 = variable1
        self.forecast_date1 = forecast_date1
        self.anal_type1 = anal_type1
        self.bin_size1 = bin_size1
        self.scatter_size1 = scatter_size1
        self.sma_size1 = sma_size1
        self.analysis_or_raw2 = analysis_or_raw2
        self.dataset_type2 = dataset_type2
        self.start_date2 = start_date2
        self.end_date2 = end_date2
        self.gridfile_dataset2 = gridfile_dataset2
        self.forecast_dataset2 = forecast_dataset2
        self.lat2 = lat2
        self.long2 = long2
        self.station2 = station2
        self.variable2 = variable2
        self.forecast_date2 = forecast_date2
        self.anal_type2 = anal_type2
        self.bin_size2 = bin_size2
        self.scatter_size2 = scatter_size2
        self.sma_size2 = sma_size2
        self.axis_status = axis_status

    def check_completeness(self):


        if self.single_or_double is 'Yes':
            pass

        if self.single_or_double is 'No':
            status = query_completeness_check()

        return status

class DataQuery:

    def __init__(self, dataset_type: str, start_date: str, end_date: str, gridfile_dataset=None, forecast_dataset=None, lat=None, long=None, station=None, variable=None, forecast_date=None, ghcn=None):
        # run validations on received parameters
        assert dataset_type in VALID_DATASET_LIST, f'Dataset type {dataset_type} is not a valid dataset type'
        assert station is None or int(station) in VALID_DUTCH_STAT_LIST or station in VALID_CME_STAT_LIST, f'Station {station} is not a valid station type'
        #assert variable is None or variable in VALID_DUTCH_VAR_LIST or variable in VALID_CME_VAR_LIST, f'Variable {variable} is not a valid variable'
        assert gridfile_dataset is None or gridfile_dataset in VALID_GRIDFILE_LIST, f'Gridfile dataset {gridfile_dataset} is not a valid gridfile dataset'
        # to do, add assert lat/long.... im not sure i want to do this now, because this would use a station metadata
        # api call, and sometimes the station metadata api call will say [0,360] as valid lat/long, but in reality, -180
        # is a valid lat/long

        # assign to self object
        self.dataset_type = dataset_type
        self.start_date = start_date
        self.end_date = end_date
        self.gridfile_dataset = gridfile_dataset
        self.lat = lat
        self.long = long
        self.station = station
        self.variable = variable
        self.forecast_date = forecast_date
        self.forecast_dataset = forecast_dataset
        self.ghcn = ghcn
        self.data = DataSet(self).data

    def get_frequency(self):

        pass


class DataSet:

    def __init__(self, query=DataQuery):
        self.data = datagetter.get_data(query.dataset_type, query.gridfile_dataset, query.start_date, query.end_date, query.lat,
                        query.long, query.station, query.variable, query.forecast_date, query.forecast_dataset, query.ghcn)

class AnalysisQuery:

    def __init__(self, analysis_or_raw=str, anal_type=None, bin_size=None, scatter_size=None, sma_size=None, extrema_size=None):
        # run validations on received parameters
        assert analysis_or_raw in ['Raw element', 'Analysis of an element'], f'{analysis_or_raw} is an invalid analysis/raw parameter. Valid parameters are "Raw element", "Analysis of an element".'
        assert anal_type is None or anal_type in valid_analysis_types, f'Analysis type {anal_type} is an invalid analysis type.'
        assert bin_size is None or bin_size in VALID_HISTOGRAM_LIST, f'Histogram bin size {bin_size} is an invalid histogram bin size'
        assert scatter_size is None or scatter_size in VALID_SCATTERPLOT_LIST, f'Scatterplot bin size {scatter_size} is an invalid scatterplot bin size.'
        # to do, add assert sma_size.... not going to do yet since sma input format is likely to be changed

        self.analysis_or_raw = analysis_or_raw
        self.anal_type = anal_type
        self.bin_size = bin_size
        self.scatter_size = scatter_size
        self.sma_size = sma_size
        self.extrema_size = extrema_size


class InputQuery:

    def __init__(self, single_or_double, dataset_type1: str, start_date1: str, end_date1: str, analysis_or_raw1=str, gridfile_dataset1=None, forecast_dataset1=None,
                 lat1=None, long1=None, station1=None, variable1=None, forecast_date1=None, ghcn1=None, anal_type1=None,
                 bin_size1=None, scatter_size1=None, sma_size1=None, extrema_size1=None, analysis_or_raw2=None, dataset_type2=None, start_date2=None, end_date2=None, gridfile_dataset2=None, forecast_dataset2=None,
                 lat2=None, long2=None, station2=None, variable2=None, forecast_date2=None, ghcn2=None, anal_type2=None,
                 bin_size2=None, scatter_size2=None, sma_size2=None, extrema_size2=None, axis_status=None):
        # run validations on received parameters
        assert single_or_double in ['Yes', 'No'], f'{single_or_double} is an invalid single/double plot parameter. Valid parameters are "No" (single) or "Yes" (double).'
        assert axis_status is None or axis_status in ['Use secondary axis', 'Use same axis'], f'{axis_status} is an invalid axis status parameter. Valid parameters are "Use secondary axis", "Use same axis", or None.'

        # assign to self object
        self.single_or_double = single_or_double
        self.axis_status = axis_status
        self.data_query1 = DataQuery(dataset_type1, start_date1, end_date1, gridfile_dataset1, forecast_dataset1, lat1, long1, station1, variable1, forecast_date1, ghcn1)
        self.analysis_query1 = AnalysisQuery(analysis_or_raw1, anal_type1, bin_size1, scatter_size1, sma_size1, extrema_size1)

        if single_or_double in ['Yes']:
            self.data_query2 = DataQuery(dataset_type2, start_date2, end_date2, gridfile_dataset2, forecast_dataset2, lat2, long2, station2, variable2, forecast_date2, ghcn2)
            self.analysis_query2 = AnalysisQuery(analysis_or_raw2, anal_type2, bin_size2, scatter_size2, sma_size2, extrema_size2)
            self.plot = helper2.get_double_plot(self)


        else:
            self.plot = helper2.get_single_plot(self)


