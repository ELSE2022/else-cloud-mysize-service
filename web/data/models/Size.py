from pyorient.ogm.property import String, Integer, LinkSet
from .BaseModel import SoftDeleteModel
from .ModelType import ModelType


class Size(SoftDeleteModel):
    element_plural = 'sizes'
    model_types = LinkSet(mandatory=True, nullable=False, linked_to=ModelType)
    processed_value = String()
    string_value = String()
    order = Integer(default=0)
