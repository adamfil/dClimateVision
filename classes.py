from vars import VALID_DATASET_LIST, VALID_DUTCH_STAT_LIST, VALID_CME_STAT_LIST, VALID_DUTCH_VAR_LIST, VALID_CME_VAR_LIST, VALID_GRIDFILE_LIST, VALID_SCATTERPLOT_LIST, VALID_HISTOGRAM_LIST, valid_analysis_types
import datagetter
import helper


class DataQuery:

    def __init__(self, dataset_type: str, start_date: str, end_date: str, gridfile_dataset=None, lat=None, long=None, station=None, variable=None):
        # run validations on received parameters
        assert dataset_type in VALID_DATASET_LIST, f'Dataset type {dataset_type} is not a valid dataset type'
        assert station is None or int(station) in VALID_DUTCH_STAT_LIST or station in VALID_CME_STAT_LIST, f'Station {station} is not a valid station type'
        assert variable is None or variable in VALID_DUTCH_VAR_LIST or variable in VALID_CME_VAR_LIST, f'Variable {variable} is not a valid variable'
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
        self.data = DataSet(self).data

    def get_frequency(self):

        pass

    def check_query_completeness(self):

        pass


class DataSet:

    def __init__(self, query=DataQuery):
        self.data = datagetter.get_data(query.dataset_type, query.gridfile_dataset, query.start_date, query.end_date, query.lat,
                        query.long, query.station, query.variable)


class AnalysisQuery:

    def __init__(self, analysis_or_raw=str, anal_type=None, bin_size=None, scatter_size=None, sma_size=None):
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


class InputQuery:

    def __init__(self, single_or_double, dataset_type1: str, start_date1: str, end_date1: str, analysis_or_raw1=str, gridfile_dataset1=None,
                 lat1=None, long1=None, station1=None, variable1=None, anal_type1=None,
                 bin_size1=None, scatter_size1=None, sma_size1=None, analysis_or_raw2=None, dataset_type2=None, start_date2=None, end_date2=None, gridfile_dataset2=None,
                 lat2=None, long2=None, station2=None, variable2=None, anal_type2=None,
                 bin_size2=None, scatter_size2=None, sma_size2=None, axis_status=None):
        # run validations on received parameters
        assert single_or_double in ['Yes', 'No'], f'{single_or_double} is an invalid single/double plot parameter. Valid parameters are "No" (single) or "Yes" (double).'
        assert axis_status is None or axis_status in ['Use secondary axis', 'Use same axis'], f'{axis_status} is an invalid axis status parameter. Valid parameters are "Use secondary axis", "Use same axis", or None.'

        # assign to self object
        self.single_or_double = single_or_double
        self.axis_status = axis_status
        self.data_query1 = DataQuery(dataset_type1, start_date1, end_date1, gridfile_dataset1, lat1, long1, station1, variable1)
        self.analysis_query1 = AnalysisQuery(analysis_or_raw1, anal_type1, bin_size1, scatter_size1, sma_size1)

        if single_or_double in ['Yes']:
            self.data_query2 = DataQuery(dataset_type2, start_date2, end_date2, gridfile_dataset2, lat2, long2, station2, variable2)
            self.analysis_query2 = AnalysisQuery(analysis_or_raw2, anal_type2, bin_size2, scatter_size2, sma_size2)
            self.plot = helper.get_double_plot(self)


        else:
            self.plot = helper.get_single_plot(self)


