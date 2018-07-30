from data.models.Product import Product
from .BaseRepository import BaseRepository


class ProductRepository(BaseRepository):

    def __init__(self):
        super().__init__(Product)
