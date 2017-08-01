from pyorient.ogm.property import String, Integer, LinkSet
from orientdb_data_layer.data_connection import NodeBase
from .ModelType import ModelType


class Size(NodeBase):
    element_plural = 'sizes'
    model_types = LinkSet(mandatory=True, nullable=False, linked_to=ModelType)
    string_value = String()
    order = Integer(default=0)
