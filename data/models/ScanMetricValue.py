from pyorient.ogm.property import String, Link
from data.data_connection import NodeBase
from .ScanMetric import ScanMetric


class ScanMetricValue(NodeBase):
    element_plural = 'scan_metric_values'
    metric = Link(indexed=True, mandatory=True, nullable=False, linked_to=ScanMetric)
    value = String()
