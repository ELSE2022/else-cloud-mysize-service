from data.models.ScannerModel import ScannerModel
from .base import RepositoryBase


class ScannerModelRepository(RepositoryBase):

    def __init__(self):
        super().__init__(ScannerModel)
