from pyorient.ogm.property import String, Integer, Link
from data.data_connection import NodeBase, RelationshipBase


class UserLike(NodeBase):
    element_plural = 'userLikes'
    id = Integer()
    name = String()


class User(NodeBase):
    element_plural = 'users'
    id = Integer()
    name = String()
    userLike = Link(linked_to=UserLike)
