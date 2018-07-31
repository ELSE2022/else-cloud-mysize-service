from data.models.CompareVisualization import CompareVisualization
from .BaseRepository import BaseRepository


class CompareVisualizationRepository(BaseRepository):

    def __init__(self):
        super().__init__(CompareVisualization)
