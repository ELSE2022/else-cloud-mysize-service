from data.models.User import User
from .BaseRepository import BaseRepository


class UserRepository(BaseRepository):

    def __init__(self):
        super().__init__(User)
