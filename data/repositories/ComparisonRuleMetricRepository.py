from data.models.ComparisonRuleMetric import ComparisonRuleMetric
from .base import RepositoryBase


class ComparisonRuleMetricRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ComparisonRuleMetric)
