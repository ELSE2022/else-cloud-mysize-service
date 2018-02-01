from pyorient.ogm.property import DateTime, Link, String
from orientdb_data_layer.data_connection import NodeBase
from .Scan import Scan
from .Model import Model


class CompareVisualization(NodeBase):
    element_plural = 'compare_visualization'
    scan = Link(mandatory=True, nullable=False, linked_to=Scan)
    model = Link(mandatory=True, nullable=False, linked_to=Model)
    output_model = String()
    output_model_3d = String()
    creation_time = DateTime(mandatory=True)
