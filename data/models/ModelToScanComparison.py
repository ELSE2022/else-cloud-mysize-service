from pyorient.ogm.property import String, DateTime
from orientdb_data_layer.data_connection import RelationshipBase


class ModelToScanComparison(RelationshipBase):
    label = 'model_to_scan_comparison'

    # from_vertex = Model
    # to_vertex = Scan

    creation_time = DateTime(mandatory=True, nullable=False)
    preview_image = String(mandatory=True, nullable=False)
