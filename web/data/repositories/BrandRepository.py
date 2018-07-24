from data.models.Brand import Brand
from .BaseRepository import BaseRepository


class BrandRepository(BaseRepository):

    def __init__(self):
        super().__init__(Brand)
