from data.models.ModelType import ModelType
from orientdb_data_layer.data import RepositoryBase


class ModelTypeRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ModelType)
