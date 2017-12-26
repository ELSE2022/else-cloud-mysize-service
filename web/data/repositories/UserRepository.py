from data.models.User import User
from orientdb_data_layer.data import RepositoryBase


class UserRepository(RepositoryBase):

    def __init__(self):
        super().__init__(User)
