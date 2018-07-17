from pyorient.ogm.property import String, Link
from .BaseModel import BaseNode, BaseModel
from .ModelType import ModelType


class ModelTypeMetric(BaseNode, BaseModel):
    element_plural = 'modeltype_metrics'
    model_type = Link(mandatory=True, nullable=False, linked_to=ModelType)
    processed_name = String()
    name = String()
