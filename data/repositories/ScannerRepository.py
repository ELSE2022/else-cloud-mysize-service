from data.models.Scanner import Scanner
from orientdb_data_layer.data import RepositoryBase


class ScannerRepository(RepositoryBase):

    def __init__(self):
        super().__init__(Scanner)
