from flask import Blueprint, jsonify, Response
from data.repositories.UsersRepository import UsersRepository
from data.repositories.UserLikesRepository import UserLikesRepository

users_controller = Blueprint('users_controller', __name__)

__repository = UsersRepository()

@users_controller.route('/api/model/users/id/<int:user_id>')
def getuser_by_id(user_id):
    users = __repository.get(dict(id=user_id), result_JSON=True)
    return Response(users, 'application/json')


@users_controller.route('/api/model/users/name/<string:user_name>')
def getuser_by_name(user_name):
    users = __repository.get(dict(name=user_name), result_JSON=True)
    return Response(users, 'application/json')


@users_controller.route('/api/model/users/add/<string:user_name>')
def adduser_by_name(user_name):
    _usersRep = UsersRepository()
    _userLikeRep = UserLikesRepository()
    like = _userLikeRep.add(dict(name=user_name))
    user = _usersRep.add(dict(name=user_name, userLike=like), result_JSON= True)
    return Response(user, 'application/json')
