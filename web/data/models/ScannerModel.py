from pyorient.ogm.property import String
from .BaseModel import BaseModel


class ScannerModel(BaseModel):
    element_plural = 'scanner_models'
    name = String()
