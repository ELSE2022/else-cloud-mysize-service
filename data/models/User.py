from pyorient.ogm.property import String, Integer, LinkSet
from data.data_connection import NodeBase


class User(NodeBase):
    element_plural = 'users'
    uuid = String(indexed=True, unique=True, mandatory=True, nullable=False)
    num_id = Integer(unique=True)
    base_url = String()
