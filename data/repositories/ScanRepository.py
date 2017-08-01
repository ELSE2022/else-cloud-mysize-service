from data.models.Scan import Scan
from orientdb_data_layer.data import RepositoryBase


class ScanRepository(RepositoryBase):

    def __init__(self):
        super().__init__(Scan)

    def get_scans(self, user, scanner_model):
        from .ScannerRepository import ScannerRepository
        from orientdb_data_layer import data_connection

        graph = data_connection.get_graph()
        _scannerRep = ScannerRepository()
        scanners = [scanner._id for scanner in _scannerRep.get(dict(model=scanner_model))]

        scans = self.get(dict(user=user))
        return [scan for scan in scans if graph.element_from_link(scan.scanner)._id in scanners]
