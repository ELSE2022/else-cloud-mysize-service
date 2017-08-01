from pyorient.ogm.property import String
from orientdb_data_layer.data_connection import NodeBase


class ModelType(NodeBase):
    element_plural = 'model_types'
    name = String()
