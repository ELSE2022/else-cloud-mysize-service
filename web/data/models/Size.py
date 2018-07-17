from pyorient.ogm.property import String, Integer, LinkSet
from .BaseModel import BaseNode, BaseModel
from .ModelType import ModelType


class Size(BaseNode, BaseModel):
    element_plural = 'sizes'
    model_types = LinkSet(mandatory=True, nullable=False, linked_to=ModelType)
    processed_value = String()
    string_value = String()
    order = Integer(default=0)
