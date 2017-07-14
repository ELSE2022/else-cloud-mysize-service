from pyorient.ogm.property import String
from data.data_connection import NodeBase


class User(NodeBase):
    element_plural = 'users'
    uuid = String(indexed=True, unique=True, mandatory=True, nullable=False)
    name = String()
    base_url = String()

