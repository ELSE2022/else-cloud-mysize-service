from pyorient.ogm.property import String
from data.data_connection import NodeBase


class ScannerModel(NodeBase):
    element_plural = 'scanner_models'
    name = String()
