from pyorient.ogm.property import String, Link
from data.data_connection import NodeBase
from .ScannerModel import ScannerModel


class ScanMetric(NodeBase):
    element_plural = 'scan_metrics'
    scanner_model = Link(indexed=True, mandatory=True, nullable=False, linked_to=ScannerModel)
    name = String()
