from data.models.ModelType import ModelType
from .BaseRepository import BaseRepository


class ModelTypeRepository(BaseRepository):

    def __init__(self):
        super().__init__(ModelType)
