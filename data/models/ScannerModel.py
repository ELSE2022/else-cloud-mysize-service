from pyorient.ogm.property import String
from orientdb_data_layer.data_connection import NodeBase


class ScannerModel(NodeBase):
    element_plural = 'scanner_models'
    name = String()
