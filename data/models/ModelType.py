from pyorient.ogm.property import String
from data.data_connection import NodeBase


class ModelType(NodeBase):
    element_plural = 'model_types'
    name = String()
