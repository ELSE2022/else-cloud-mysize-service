from pyorient.ogm.property import String, Link
from .BaseModel import BaseNode, BaseModel
from .Model import Model
from .ModelTypeMetric import ModelTypeMetric


class ModelMetricValue(BaseNode, BaseModel):
    element_plural = 'model_metric_values'
    model = Link(mandatory=True, nullable=False, linked_to=Model)
    metric = Link(mandatory=True, nullable=False, linked_to=ModelTypeMetric)
    value = String()
