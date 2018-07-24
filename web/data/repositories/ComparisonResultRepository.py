from data.models.ComparisonResult import ComparisonResult
from .BaseRepository import BaseRepository


class ComparisonResultRepository(BaseRepository):

    def __init__(self):
        super().__init__(ComparisonResult)
