from pyorient.ogm.property import String, Link
from orientdb_data_layer.data_connection import NodeBase
from .Brand import Brand
from .ComparisonRule import ComparisonRule


class Product(NodeBase):
    element_plural = 'products'
    uuid = String(unique=True, mandatory=True, nullable=False)
    brand = Link(mandatory=True, nullable=False, linked_to=Brand)
    sku = String()
    name = String()

    default_comparison_rule = Link(mandatory=True, nullable=False, linked_to=ComparisonRule)
