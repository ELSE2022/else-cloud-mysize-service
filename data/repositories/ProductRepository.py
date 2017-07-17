from data.models.Product import Product
from .base import RepositoryBase


class ProductRepository(RepositoryBase):

    def __init__(self):
        super().__init__(Product)
