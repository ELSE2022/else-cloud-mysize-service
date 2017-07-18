from data.models.ScanMetric import ScanMetric
from .base import RepositoryBase


class ScanMetricRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ScanMetric)