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

    model_type = _modelTypeRep.get({
        'name': model,
    })

    if len(model_type) < 1:
        left_foot = _modelTypeRep.get({
            'name': 'LEFT_FOOT',
        })[0]
        right_foot = _modelTypeRep.get({
            'name': 'RIGHT_FOOT',
        })[0]
        model_type = [left_foot, right_foot]

    size = _sizeRep.get({
        'string_value': size_value,
        'model_types': model_type,
    })

    if len(size) < 1:
        size = _sizeRep.add({
            'string_value': size_value,
            'model_types': model_type,
        })
    else:
        size = size[0]

    user = _userRep.add({
        'uuid': user_uuid,
    })

    user_sizes = _userSizeRep.get({
        'user': user,
        'size': size,
    })

    if len(user_sizes) < 1:
        user_sizes = _userSizeRep.add({
            'user': user,
            'size': size,
            'creation_time': str(datetime.now()),
        })

    return jsonify({
        'default_size': 'FOOT - ' + size_value,
    })
