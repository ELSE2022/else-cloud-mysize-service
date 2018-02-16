from pyorient.ogm.property import String, Link, LinkSet
from .BaseModel import BaseNode, BaseModel
from .ModelType import ModelType
from .ScannerModel import ScannerModel


class ComparisonRule(BaseNode, BaseModel):
    element_plural = 'comparison_rules'
    model_types = LinkSet(mandatory=True, nullable=False, linked_to=ModelType)
    scanner_model = Link(mandatory=True, nullable=False, linked_to=ScannerModel)
    name = String()
