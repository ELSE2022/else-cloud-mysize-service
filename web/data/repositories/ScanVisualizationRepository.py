from data.models.ScanVisualization import ScanVisualization
from orientdb_data_layer.data import RepositoryBase


class ScanVisualizationRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ScanVisualization)
