from pyorient.ogm.property import String, DateTime, Link, Boolean, Integer
from .BaseModel import BaseNode, BaseModel
from .Scanner import Scanner
from .ModelType import ModelType
from .User import User


class Scan(BaseNode, BaseModel):
    element_plural = 'scans'
    user = Link(mandatory=True, nullable=False, linked_to=User)
    scanner = Link(mandatory=True, nullable=False, linked_to=Scanner)
    model_type = Link(mandatory=True, nullable=False, linked_to=ModelType)
    is_default = Boolean(default=False)
    creation_time = DateTime()
    scan_id = String()
    num_id = Integer()

    name = String()
    sex = String()
    stl_path = String()
    img_path = String()
