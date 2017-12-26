import datetime
from pyorient.ogm.property import Float
from pyorient.ogm.property import Link
from pyorient.ogm.property import DateTime
from orientdb_data_layer.data_connection import NodeBase
from .Scan import Scan
from .Size import Size
from .ModelType import ModelType


class ComparisonResult(NodeBase):
    element_plural = 'comparison_result'
    model_type = Link(mandatory=True, nullable=False, linked_to=ModelType)
    scan = Link(mandatory=True, nullable=False, linked_to=Scan)
    size = Link(mandatory=True, nullable=False, linked_to=Size)
    creation_time = DateTime(mandatory=True, nullable=False, default=datetime.datetime.utcnow())
    value = Float()
