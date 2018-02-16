from pyorient.ogm.property import DateTime, Link, String
from .BaseModel import BaseNode, BaseModel
from .Scan import Scan


class ScanVisualization(BaseNode, BaseModel):
    element_plural = 'scan_visualization'
    scan = Link(mandatory=True, nullable=False, linked_to=Scan)
    output_model = String()
    output_model_3d = String()
    creation_time = DateTime(mandatory=True)
