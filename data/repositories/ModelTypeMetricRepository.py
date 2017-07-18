from data.models.ModelTypeMetric import ModelTypeMetric
from .base import RepositoryBase


class ModelTypeMetricRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ModelTypeMetric)
