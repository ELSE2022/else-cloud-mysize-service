from pyorient.ogm.property import DateTime, Link, String
from orientdb_data_layer.data_connection import NodeBase
from .Scan import Scan


class ScanVisualization(NodeBase):
    element_plural = 'scan_visualization'
    scan = Link(mandatory=True, nullable=False, linked_to=Scan)
    output_model = String()
    output_model_3d = String()
    creation_time = DateTime(mandatory=True)
