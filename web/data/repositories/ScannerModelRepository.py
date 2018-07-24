from data.models.ScannerModel import ScannerModel
from .BaseRepository import BaseRepository


class ScannerModelRepository(BaseRepository):

    def __init__(self):
        super().__init__(ScannerModel)
