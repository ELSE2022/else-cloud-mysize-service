from data.models.ScanMetricValue import ScanMetricValue
from .base import RepositoryBase


class ScanMetricValueRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ScanMetricValue)