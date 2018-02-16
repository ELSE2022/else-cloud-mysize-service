from pyorient.ogm.property import String
from .BaseModel import BaseNode, BaseModel


class ScannerModel(BaseNode, BaseModel):
    element_plural = 'scanner_models'
    name = String()
