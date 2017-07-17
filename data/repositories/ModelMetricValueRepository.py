from data.models.ModelMetricValue import ModelMetricValue
from .base import RepositoryBase


class ModelMetricValueRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ModelMetricValue)