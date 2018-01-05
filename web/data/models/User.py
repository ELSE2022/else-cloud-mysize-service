from settings import SCANNER_STORAGE_BASE_URL
from pyorient.ogm.property import String, Integer, LinkSet
from orientdb_data_layer.data_connection import NodeBase


class User(NodeBase):
    element_plural = 'users'
    uuid = String(unique=True, mandatory=True, nullable=False)
    num_id = Integer()
    base_url = String(default=SCANNER_STORAGE_BASE_URL)
