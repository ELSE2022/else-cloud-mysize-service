from pyorient.ogm.property import String, Link
from data.data_connection import NodeBase
from .ScannerModel import ScannerModel


class Scanner(NodeBase):
    element_plural = 'scanners'
    model = Link(indexed=True, mandatory=True, nullable=False, linked_to=ScannerModel)
    name = String()
