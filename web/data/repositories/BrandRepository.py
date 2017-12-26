from data.models.Brand import Brand
from orientdb_data_layer.data import RepositoryBase


class BrandRepository(RepositoryBase):

    def __init__(self):
        super().__init__(Brand)
