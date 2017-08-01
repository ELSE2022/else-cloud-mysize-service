from pyorient.ogm.property import String, Link
from orientdb_data_layer.data_connection import NodeBase
from .ScannerModel import ScannerModel


class Scanner(NodeBase):
    element_plural = 'scanners'
    model = Link(mandatory=True, nullable=False, linked_to=ScannerModel)
    name = String()
