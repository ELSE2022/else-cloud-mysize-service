from data.models.UserSize import UserSize
from .BaseRepository import BaseRepository


class UserSizeRepository(BaseRepository):

    def __init__(self):
        super().__init__(UserSize)
