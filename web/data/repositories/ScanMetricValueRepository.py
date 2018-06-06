from data.models.ScanMetricValue import ScanMetricValue
from orientdb_data_layer.data import RepositoryBase


class ScanMetricValueRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ScanMetricValue)
