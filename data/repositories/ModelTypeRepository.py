from data.models.ModelType import ModelType
from .base import RepositoryBase


class ModelTypeRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ModelType)