from pyorient.ogm.property import String, DateTime, Link, Boolean, Integer
from orientdb_data_layer.data_connection import NodeBase
from .User import User
from .Scanner import Scanner
from .ModelType import ModelType


class Scan(NodeBase):
    element_plural = 'scans'
    user = Link(mandatory=True, nullable=False, linked_to=User)
    scanner = Link(mandatory=True, nullable=False, linked_to=Scanner)
    model_type = Link(mandatory=True, nullable=False, linked_to=ModelType)
    is_default = Boolean(default=False)
    creation_time = DateTime()
    scan_id = String()
    num_id = Integer()

    name = String()
    sex = String()
    stl_path = String()
    img_path = String()

    def __str__(self):
        from orientdb_data_layer import data_connection
        graph = data_connection.get_graph()

        user = graph.element_from_link(self.user).uuid
        model_type = graph.element_from_link(self.model_type).name
        scanner = graph.element_from_link(self.scanner).name
        creation_time = str(self.creation_time)

        return 'scan_id: {}, user: {}, scanner: {}, type: {}, '\
            'created_date: {}'.format(self.scan_id,
            user, scanner, model_type, creation_time)
