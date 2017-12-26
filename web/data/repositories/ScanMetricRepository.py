from data.models.ScanMetric import ScanMetric
from orientdb_data_layer.data import RepositoryBase


class ScanMetricRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ScanMetric)