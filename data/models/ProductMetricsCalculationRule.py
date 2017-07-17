from pyorient.ogm.property import String, Link, LinkMap
from data.data_connection import NodeBase
from .Product import Product
from .ModelMetric import ModelMetric
from .ScanMetric import ScanMetric


class ProductMetricsCalculationRule(NodeBase):
    element_plural = 'product_metrics_calculation_rule'
    product = Link(indexed=True, mandatory=True, nullable=False, linked_to=Product)
    name = String()
    model_metrics = LinkMap(indexed=True, nullable=True, linked_to=ModelMetric)
    scan_metrics = LinkMap(indexed=True, nullable=True, linked_to=ScanMetric)
