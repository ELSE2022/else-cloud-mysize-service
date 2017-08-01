from data.models.ScannerModel import ScannerModel
from orientdb_data_layer.data import RepositoryBase


class ScannerModelRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ScannerModel)
