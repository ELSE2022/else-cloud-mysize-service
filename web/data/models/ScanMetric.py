from pyorient.ogm.property import String, Link
from .BaseModel import BaseNode, BaseModel
from .ScannerModel import ScannerModel


class ScanMetric(BaseNode, BaseModel):
    element_plural = 'scan_metrics'
    scanner_model = Link(mandatory=True, nullable=False, linked_to=ScannerModel)
    name = String()
