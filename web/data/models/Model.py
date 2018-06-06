from pyorient.ogm.property import String, Link
from .BaseModel import BaseNode, BaseModel
from .Product import Product
from .Size import Size
from .ModelType import ModelType


class Model(BaseNode, BaseModel):
    element_plural = 'models'
    product = Link(mandatory=True, nullable=False, linked_to=Product)
    model_type = Link(mandatory=True, nullable=False, linked_to=ModelType)
    size = Link(mandatory=True, nullable=False, linked_to=Size)
    name = String()
    stl_path = String()

    def __str__(self):

        return f'<Model: {self._id}>'
