from pyorient.ogm.property import String, Link
from data.data_connection import NodeBase
from .Product import Product


class ModelMetric(NodeBase):
    element_plural = 'model_metrics'
    product = Link(indexed=True, mandatory=True, nullable=False, linked_to=Product)
    name = String()
