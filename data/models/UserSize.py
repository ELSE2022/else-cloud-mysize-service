from pyorient.ogm.property import DateTime, Link
from data.data_connection import NodeBase
from .User import User
from .Size import Size


class UserSize(NodeBase):
    element_plural = 'user_sizes'
    user = Link(indexed=True, mandatory=True, nullable=False, linked_to=User)
    size = Link(indexed=True, mandatory=True, nullable=False, linked_to=Size)
    creation_time = DateTime(mandatory=True)
