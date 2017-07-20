from pyorient.ogm.property import String
from data.data_connection import NodeBase


class Brand(NodeBase):
    element_plural = 'brands'
    uuid = String(indexed=True, unique=True, mandatory=True, nullable=False)
    name = String()