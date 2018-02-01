from data.models.CompareVisualization import CompareVisualization
from orientdb_data_layer.data import RepositoryBase


class CompareVisualizationRepository(RepositoryBase):

    def __init__(self):
        super().__init__(CompareVisualization)
