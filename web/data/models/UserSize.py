from pyorient.ogm.property import DateTime, Link
from orientdb_data_layer.data_connection import NodeBase
from .User import User
from .Size import Size
from .ModelType import ModelType


class UserSize(NodeBase):
    element_plural = 'user_sizes'
    user = Link(mandatory=True, nullable=False, linked_to=User)
    size = Link(mandatory=True, nullable=False, linked_to=Size)
    model_type = Link(mandatory=True, nullable=False, linked_to=ModelType)
    creation_time = DateTime(mandatory=True)
