from vars import VALID_DATASET_LIST, VALID_DUTCH_STAT_LIST, VALID_CME_STAT_LIST, VALID_DUTCH_VAR_LIST, VALID_CME_VAR_LIST, VALID_GRIDFILE_LIST


class DataQuery:

    def __init__(self, dataset_type: str, start_date: str, end_date: str, gridfile_dataset=None, lat=None, long=None, station=None, variable=None):
        # run validations on received parameters
        assert dataset_type in VALID_DATASET_LIST, f'Dataset type {dataset_type} is not a valid dataset type'
        assert station is None or station in VALID_DUTCH_STAT_LIST or station in VALID_CME_STAT_LIST, f'Station {station} is not a valid station type'
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

    def get_frequency(self):

        pass

    def check_query_completeness(self):

        pass

class AnalysisQuery:

    def check_query_completeness(self):

        pass

    pass


class InputQuery:

    def check_query_completeness(self):

        pass

    pass

