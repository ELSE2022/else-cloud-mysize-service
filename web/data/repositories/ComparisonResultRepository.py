from data.models.ComparisonResult import ComparisonResult
from orientdb_data_layer.data import RepositoryBase


class ComparisonResultRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ComparisonResult)
