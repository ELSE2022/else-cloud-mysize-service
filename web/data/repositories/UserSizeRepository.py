from data.models.UserSize import UserSize
from orientdb_data_layer.data import RepositoryBase


class UserSizeRepository(RepositoryBase):

    def __init__(self):
        super().__init__(UserSize)
