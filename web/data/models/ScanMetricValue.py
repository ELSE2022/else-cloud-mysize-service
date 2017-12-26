from pyorient.ogm.property import String, Link
from orientdb_data_layer.data_connection import NodeBase
from .Scan import Scan
from .ScanMetric import ScanMetric


class ScanMetricValue(NodeBase):
    element_plural = 'scan_metric_values'
    scan = Link(mandatory=True, nullable=False, linked_to=Scan)
    metric = Link(mandatory=True, nullable=False, linked_to=ScanMetric)
    value = String()
