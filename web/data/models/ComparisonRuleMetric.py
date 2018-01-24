from pyorient.ogm.property import String, Link, Float
from orientdb_data_layer.data_connection import NodeBase
from .ComparisonRule import ComparisonRule
from .Model import Model
from .ModelTypeMetric import ModelTypeMetric
from .ScanMetric import ScanMetric


class ComparisonRuleMetric(NodeBase):
    element_plural = 'comparisonrule_metrics'
    rule = Link(mandatory=True, nullable=False, linked_to=ComparisonRule)
    model = Link(mandatory=True, nullable=False, linked_to=Model)
    model_metric = Link(mandatory=True, nullable=False, linked_to=ModelTypeMetric)
    scan_metric = Link(mandatory=True, nullable=False, linked_to=ScanMetric)

    f1 = Float()
    shift = Float()
    f2 = Float()