from data.models.User import User
from .base import RepositoryBase


class UsersRepository(RepositoryBase):

    def __init__(self):
        super().__init__(User)
