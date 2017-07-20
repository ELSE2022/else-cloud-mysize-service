from data.models.UserSize import UserSize
from .base import RepositoryBase


class UserSizeRepository(RepositoryBase):

    def __init__(self):
        super().__init__(UserSize)
