from flask import Blueprint, jsonify, request, abort

from data.repositories import UserRepository
from data.repositories import ScanRepository
from orientdb_data_layer import data_connection

import logging

logger = logging.getLogger(__name__)

_userRep = UserRepository()
_scanRep = ScanRepository()

set_default_scan_action = Blueprint('set_default_scan_action', __name__)


@set_default_scan_action.route('/fitting/set_default_scan')
def set_default_scan():
    user_uuid = request.args.get('user')
    scan_id = request.args.get('scan')

    user = get_user(user_uuid)
    scans = _scanRep.get({'user': user, 'scan_id': scan_id})

    for scan in scans:
        set_scan(user, scan)

    return jsonify([str(scan) for scan in scans])


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


def set_scan(user, scan):
    graph = data_connection.get_graph()
    model_type = graph.element_from_link(scan.model_type)

    default_scans = _scanRep.get({
        'user': user,
        'model_type': model_type,
    })

    for default_scan in default_scans:
        _scanRep.update({'@rid': default_scan._id}, {'is_default': False})

    _scanRep.update({'@rid': scan._id}, {'is_default': True})
