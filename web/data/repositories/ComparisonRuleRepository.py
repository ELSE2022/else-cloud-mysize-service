from data.models.ComparisonRule import ComparisonRule
from .BaseRepository import BaseRepository


class ComparisonRuleRepository(BaseRepository):

    def __init__(self):
        super().__init__(ComparisonRule)
