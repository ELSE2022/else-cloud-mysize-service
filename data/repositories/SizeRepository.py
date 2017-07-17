from data.models.Size import Size
from .base import RepositoryBase


class SizeRepository(RepositoryBase):

    def __init__(self):
        super().__init__(Size)
