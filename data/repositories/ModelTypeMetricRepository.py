from data.models.ModelTypeMetric import ModelTypeMetric
from orientdb_data_layer.data import RepositoryBase


class ModelTypeMetricRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ModelTypeMetric)
