from pyorient.ogm.property import String, Integer, LinkSet
from data.data_connection import NodeBase
from .ModelType import ModelType


class Size(NodeBase):
    element_plural = 'sizes'
    model_types = LinkSet(indexed=True, mandatory=True, nullable=False, linked_to=ModelType)
    string_value = String()
    order = Integer(default=0)
