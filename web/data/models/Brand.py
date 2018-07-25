from pyorient.ogm.property import String
from .BaseModel import BaseModel


class Brand(BaseModel):
    element_plural = 'brands'
    uuid = String(unique=True, mandatory=True, nullable=False)
    name = String()
