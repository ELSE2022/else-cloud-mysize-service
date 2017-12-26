from pyorient.ogm.property import String, Link
from orientdb_data_layer.data_connection import NodeBase
from .ModelType import ModelType


class ModelTypeMetric(NodeBase):
    element_plural = 'modeltype_metrics'
    model_type = Link(mandatory=True, nullable=False, linked_to=ModelType)
    name = String()
