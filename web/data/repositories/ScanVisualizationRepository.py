from data.models.ScanVisualization import ScanVisualization
from .BaseRepository import BaseRepository


class ScanVisualizationRepository(BaseRepository):

    def __init__(self):
        super().__init__(ScanVisualization)
