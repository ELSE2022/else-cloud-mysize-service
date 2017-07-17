from data.models.Model import Model
from .base import RepositoryBase


class ModelRepository(RepositoryBase):

    def __init__(self):
        super().__init__(Model)
