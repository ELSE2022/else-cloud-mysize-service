from data.models.User import UserLike
from .base import RepositoryBase


class UserLikesRepository(RepositoryBase):

    def __init__(self):
        super().__init__(UserLike)
