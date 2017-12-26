from data.models.Size import Size
from orientdb_data_layer.data import RepositoryBase


class SizeRepository(RepositoryBase):

    def __init__(self):
        super().__init__(Size)
