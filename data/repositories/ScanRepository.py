from data.models.Scan import Scan
from .base import RepositoryBase


class ScanRepository(RepositoryBase):

    def __init__(self):
        super().__init__(Scan)
