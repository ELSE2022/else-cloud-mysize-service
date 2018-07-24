from pyorient.ogm.property import String, Link
from .BaseModel import SoftDeleteModel
from .ScannerModel import ScannerModel


class ScanMetric(SoftDeleteModel):
    element_plural = 'scan_metrics'
    scanner_model = Link(mandatory=True, nullable=False, linked_to=ScannerModel)
    processed_name = String()
    name = String(mandatory=True)
