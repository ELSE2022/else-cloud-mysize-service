from data.models.Model import Model
from orientdb_data_layer.data import RepositoryBase


class ModelRepository(RepositoryBase):

    def __init__(self):
        super().__init__(Model)
