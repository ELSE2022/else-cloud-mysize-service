from flask import Blueprint, jsonify, request, abort

from data.repositories import UserRepository
from data.repositories import ScanRepository
from data.repositories import ScanMetricValueRepository

from orientdb_data_layer import data_connection

import logging

_userRep = UserRepository()
_scanRep = ScanRepository()
_scanMetricValueRep = ScanMetricValueRepository()

logger = logging.getLogger(__name__)

get_user_profile_action = Blueprint('get_user_profile_action', __name__)


@get_user_profile_action.route('/fitting/get_user_profile')
def get_user_profile():
    user_uuid = request.args.get('user')
    scan_id = request.args.get('scan')

    user = get_user(user_uuid)
    scans = get_scans(user, scan_id)
    user_profile = create_json(scans)

    return jsonify(user_profile)


def get_user(user_uuid):
    if user_uuid is None:
        abort(400, 'Request malformed: \'user\' argument not passed')
    user = _userRep.get({
        'uuid': user_uuid,
    })
    if len(user) == 0:
        abort(404, 'User not found')
    if len(user) > 1:
        abort(400, 'Too many ({}) users with the same user_uuid: {}'.format(len(user), user_uuid))
    return user[0]


def get_scans(user, scan_id):
    if scan_id is None:
        abort(400, 'Request malformed: \'scan\' argument not passed')
    return _scanRep.get({
        'user': user,
        'scan_id': scan_id,
    })


def create_json(scans):
    user_profile = {
        'Name': {},
        'Sex': {},
        'scan_image': {}
    }
    for scan in scans:
        scan_metrics = get_metrics(scan)
        model_type_name = get_model_type_name(scan)

        user_profile['Name'][model_type_name] = scan.name
        user_profile['Sex'][model_type_name] = scan.sex
        user_profile['scan_image'][model_type_name] = scan.img_path

        for scan_metric in scan_metrics:
            name = get_metric_name(scan_metric)
            if name not in user_profile:
                user_profile[name] = {}
            user_profile[name][model_type_name] = scan_metric.value

    return user_profile if scans else {}


def get_metrics(scan):
    return _scanMetricValueRep.get({
        'scan': scan,
    })


def get_metric_name(scan_metric):
    graph = data_connection.get_graph()
    metric = graph.element_from_link(scan_metric.metric)
    return metric.name


def get_model_type_name(scan):
    graph = data_connection.get_graph()
    model_type = graph.element_from_link(scan.model_type)
    return model_type.name
