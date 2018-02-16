from settings import SCANNER_STORAGE_BASE_URL
from pyorient.ogm.property import String, Link
from .BaseModel import BaseNode, BaseModel
from .ScannerModel import ScannerModel


class Scanner(BaseNode, BaseModel):
    element_plural = 'scanners'
    model = Link(mandatory=True, nullable=False, linked_to=ScannerModel)
    name = String()
    base_url = String(default=SCANNER_STORAGE_BASE_URL)
