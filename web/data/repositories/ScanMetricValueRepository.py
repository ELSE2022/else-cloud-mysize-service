from data.models.ScanMetricValue import ScanMetricValue
from .BaseRepository import BaseRepository


class ScanMetricValueRepository(BaseRepository):

    def __init__(self):
        super().__init__(ScanMetricValue)
