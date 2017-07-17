from data.models.ModelMetric import ModelMetric
from .base import RepositoryBase


class ModelMetricRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ModelMetric)