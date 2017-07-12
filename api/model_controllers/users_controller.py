from flask import Blueprint, jsonify
from data.repositories.UsersRepository import UsersRepository

users_controller = Blueprint('users_controller', __name__)

__repository = UsersRepository()


def get_json(users):
    result = [user._props for user in users]
    return jsonify(result)


@users_controller.route('/api/model/users/id/<int:user_id>')
def getuser_by_id(user_id):
    users = __repository.get(dict(id=user_id))
    return get_json(users)


@users_controller.route('/api/model/users/name/<string:user_name>')
def getuser_by_name(user_name):
    users = __repository.get(dict(name=user_name))
    return get_json(users)