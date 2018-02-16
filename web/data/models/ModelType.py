from pyorient.ogm.property import String
from .BaseModel import BaseNode, BaseModel


class ModelType(BaseNode, BaseModel):
    element_plural = 'model_types'
    name = String()
