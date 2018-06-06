from flask import Blueprint, jsonify, request, abort
from datetime import datetime

from data.repositories import UserRepository
from data.repositories import SizeRepository
from data.repositories import UserSizeRepository
from data.repositories import ModelTypeRepository

import logging

logger = logging.getLogger(__name__)

_userRep = UserRepository()
_sizeRep = SizeRepository()
_userSizeRep = UserSizeRepository()
_modelTypeRep = ModelTypeRepository()

create_user_action = Blueprint('create_user_action', __name__)


@create_user_action.route('/fitting/create_user')
def create_user():
    user_uuid = request.args.get('user')
    size_value = request.args.get('size', '35')
    model = request.args.get('type')

    user = check_user(user_uuid)
    model_type = get_model_type(model)
    size = get_size(size_value, model_type)
    check_user_sizes(user, size)

    return jsonify({'default_size': 'FOOT - ' + size_value})


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


def get_size(size_value, model_type):
    size = _sizeRep.get({
        'string_value': size_value,
        'model_types': model_type,
    })

    if len(size) != 0:
        return size[0]
    else:
        return _sizeRep.add({
            'string_value': size_value,
            'model_types': model_type,
        })


def check_user_sizes(user, size):
    user_sizes = _userSizeRep.get({
        'user': user,
        'size': size,
    })
    if len(user_sizes) != 0:
        return False
    else:
        _userSizeRep.add({
            'user': user,
            'size': size,
            'creation_time': str(datetime.now()),
        })
        return True


def check_user(user_uuid):
    if user_uuid is None:
        abort(400, 'Request malformed: \'user\' argument not passed')

    user = _userRep.get({'uuid': user_uuid})

    if len(user) == 0:
        return _userRep.add({'uuid': user_uuid}, result_JSON=True)
    else:
        abort(400, 'User with uuid=\'{}\' already exists'.format(user_uuid))
