from pyorient.ogm.property import String, DateTime, Link, Boolean, Integer
from data.data_connection import NodeBase
from .User import User
from .Scanner import Scanner
from .ModelType import ModelType


class Scan(NodeBase):
    element_plural = 'scans'
    user = Link(indexed=True, mandatory=True, nullable=False, linked_to=User)
    scanner = Link(indexed=True, mandatory=True, nullable=False, linked_to=Scanner)
    model_type = Link(indexed=True, mandatory=True, nullable=False, linked_to=ModelType)
    is_default = Boolean(default=False)
    creation_time = DateTime()
    scan_id = String()
    num_id = Integer(unique=True)

    name = String()
    sex = String()
    stl_path = String()
    img_path = String()

