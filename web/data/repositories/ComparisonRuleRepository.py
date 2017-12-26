from data.models.ComparisonRule import ComparisonRule
from orientdb_data_layer.data import RepositoryBase


class ComparisonRuleRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ComparisonRule)
