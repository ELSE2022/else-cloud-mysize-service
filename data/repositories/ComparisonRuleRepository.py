from data.models.ComparisonRule import ComparisonRule
from .base import RepositoryBase


class ComparisonRuleRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ComparisonRule)
