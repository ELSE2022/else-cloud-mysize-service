from data.models.Scanner import Scanner
from .base import RepositoryBase


class ScannerRepository(RepositoryBase):

    def __init__(self):
        super().__init__(Scanner)
