from pyorient.ogm.declarative import declarative_node
from pyorient.ogm.property import String
from .BaseModel import BaseNode, BaseModel


class Brand(BaseNode, BaseModel):
    element_plural = 'brands'
    uuid = String(unique=True, mandatory=True, nullable=False)
    name = String()
