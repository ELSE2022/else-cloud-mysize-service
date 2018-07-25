from pyorient.ogm.property import String
from .BaseModel import BaseModel


class ModelType(BaseModel):
    element_plural = 'model_types'
    name = String()
