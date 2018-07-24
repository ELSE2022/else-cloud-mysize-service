from data.models.Model import Model
from .BaseRepository import BaseRepository


class ModelRepository(BaseRepository):

    def __init__(self):
        super().__init__(Model)
