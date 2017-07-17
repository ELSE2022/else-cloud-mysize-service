from data.models.Brand import Brand
from .base import RepositoryBase


class BrandRepository(RepositoryBase):

    def __init__(self):
        super().__init__(Brand)
