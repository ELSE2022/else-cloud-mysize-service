from pyorient.ogm.property import String, Link
from data.data_connection import NodeBase
from .Brand import Brand


class Product(NodeBase):
    element_plural = 'products'
    uuid = String(indexed=True, unique=True, mandatory=True, nullable=False)
    brand = Link(indexed=True, mandatory=True, nullable=False, linked_to=Brand)
    name = String()
