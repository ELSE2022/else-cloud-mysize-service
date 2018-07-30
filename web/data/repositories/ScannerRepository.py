from data.models.Scanner import Scanner
from .BaseRepository import BaseRepository


class ScannerRepository(BaseRepository):

    def __init__(self):
        super().__init__(Scanner)
