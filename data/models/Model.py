from pyorient.ogm.property import String, Link
from data.data_connection import NodeBase
from .Product import Product
from .Size import Size
from .ModelType import ModelType


class Model(NodeBase):
    element_plural = 'models'
    product = Link(mandatory=True, nullable=False, linked_to=Product)
    model_type = Link(mandatory=True, nullable=False, linked_to=ModelType)
    size = Link(mandatory=True, nullable=False, linked_to=Size)
    name = String()
