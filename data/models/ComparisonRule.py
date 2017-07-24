from pyorient.ogm.property import String, Link
from data.data_connection import NodeBase
from .ModelType import ModelType
from .ScannerModel import ScannerModel


class ComparisonRule(NodeBase):
    element_plural = 'comparison_rules'
    model_type = Link(mandatory=True, nullable=False, linked_to=ModelType)
    scanner_model = Link(mandatory=True, nullable=False, linked_to=ScannerModel)
    name = String()
