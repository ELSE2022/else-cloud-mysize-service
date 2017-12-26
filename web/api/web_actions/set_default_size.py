from flask import Blueprint, jsonify, request, abort

from data.repositories import UserRepository
from data.repositories import SizeRepository
from data.repositories import UserSizeRepository
from data.repositories import ModelTypeRepository

from orientdb_data_layer import data_connection

from datetime import datetime
import logging

logger = logging.getLogger(__name__)

_userRep = UserRepository()
_sizeRep = SizeRepository()
_userSizeRep = UserSizeRepository()
_modelTypeRep = ModelTypeRepository()

set_default_size_action = Blueprint('set_default_size_action', __name__)


@set_default_size_action.route('/fitting/set_default_size')
def set_default_size():
    user_uuid = request.args.get('user')
    size_value = request.args.get('size')
    model = request.args.get('type')

    user = get_user(user_uuid)
    model_types = get_model_type(model)
    print(model_types)
    size = get_size(size_value, model_types)

    remove_excess_sizes(user, model_types)
    rid = add_user_size(user, size)

    return jsonify({'default_size': 'FOOT - ' + size.string_value})


def remove_excess_sizes(user, model_types):
    user_sizes = _userSizeRep.get_by_tree({
        'user': user,
        'size': {
            'model_types': model_types,
        }
    })

    for user_size in user_sizes:
        _userSizeRep.delete({
            '@rid': user_size._id
        })


def get_user(user_uuid):
    if user_uuid is None:
        abort(400, 'Request malformed: \'user\' argument not passed')
    user = _userRep.get({
        'uuid': user_uuid,
    })
    if len(user) == 0:
        abort(404, 'User not found')
    if len(user) > 1:
        abort(400, 'Too many ({}) users with '
            'the same user_uuid: {}'.format(len(user), user_uuid))
    return user[0]


def get_size(size_value, model_types):
    size = _sizeRep.get({
        'string_value': size_value,
        'model_types': model_types,
    })
    if len(size) == 0:
        abort(404, 'Size not found')
    if len(size) > 1:
        abort(400, 'Too many ({}) sizes'.format(len(size)))
    return size[0]


def get_model_type(model):
    if model is not None:
        return _modelTypeRep.get({'name': model})
    else:
        left_foot = _modelTypeRep.get({'name': 'LEFT_FOOT'})
        right_foot = _modelTypeRep.get({'name': 'RIGHT_FOOT'})
        if len(left_foot) == 0:
            abort(404, 'ModelType \'LEFT_FOOT\' not exist')
        if len(right_foot) == 0:
            abort(404, 'ModelType \'RIGHT_FOOT\' not exist')
        return [left_foot[0], right_foot[0]]


def add_user_size(user, size):
    user_size = _userSizeRep.get({
        'user': user,
        'size': size,
    })
    if len(user_size) != 0:
        return user_size[0]._id
    else:
        user_size = _userSizeRep.add({
            'user': user,
            'size': size,
            'creation_time': str(datetime.now()),
        })
        return user_size._id
