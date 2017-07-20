from pyorient.ogm.property import String, Link
from data.data_connection import NodeBase
from .Model import Model
from .ModelTypeMetric import ModelTypeMetric


class ModelMetricValue(NodeBase):
    element_plural = 'model_metric_values'
    model = Link(indexed=True, mandatory=True, nullable=False, linked_to=Model)
    metric = Link(indexed=True, mandatory=True, nullable=False, linked_to=ModelTypeMetric)
    value = String()