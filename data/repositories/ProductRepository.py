from data.models.Product import Product
from orientdb_data_layer.data import RepositoryBase


class ProductRepository(RepositoryBase):

    def __init__(self):
        super().__init__(Product)
