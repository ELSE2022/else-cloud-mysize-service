from pyorient.ogm.property import String, Integer
from data.data_connection import NodeBase, RelationshipBase


class User(NodeBase):
    element_plural = 'users'
    id = Integer()
    name = String()
