from pyorient.ogm.property import String
from orientdb_data_layer.data_connection import NodeBase


class Brand(NodeBase):
    element_plural = 'brands'
    uuid = String(unique=True, mandatory=True, nullable=False)
    name = String()
