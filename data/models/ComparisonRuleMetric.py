from pyorient.ogm.property import String, Link, Float
from data.data_connection import NodeBase
from .ComparisonRule import ComparisonRule
from .Size import Size
from .ModelTypeMetric import ModelTypeMetric
from .ScanMetric import ScanMetric


class ComparisonRuleMetric(NodeBase):
    element_plural = 'comparisonrule_metrics'
    rule = Link(mandatory=True, nullable=False, linked_to=ComparisonRule)
    size = Link(mandatory=True, nullable=False, linked_to=Size)
    model_metric = Link(mandatory=True, nullable=False, linked_to=ModelTypeMetric)
    scan_metric = Link(mandatory=True, nullable=False, linked_to=ScanMetric)

    f1 = Float()
    shift = Float()
    f2 = Float()
