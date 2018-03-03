import logging
from flask import Blueprint, jsonify, request, abort
from ..authentication import requires_auth

from data.repositories import UserRepository
from data.repositories import ScanRepository
from orientdb_data_layer import data_connection
from data.models import User
from data.models import Scan

logger = logging.getLogger(__name__)

_userRep = UserRepository()
_scanRep = ScanRepository()

get_user_scans_action = Blueprint('get_user_scans_action', __name__)


def get_foot_scans(scans):
    result = {}
    graph = data_connection.get_graph()
    for scan in scans:
        result[scan.scan_id] = {
            'scan_id': scan.scan_id,
            'scanner': graph.element_from_link(scan.scanner).name,
            'created_date': scan.creation_time.strftime("%A, %d. %B %Y %I:%M%p")
        }
    return result.values()


@get_user_scans_action.route('/fitting/user_scans')
@requires_auth
def get_user_scans():
    user_uuid = request.args.get('user')
    user = User.query_set.filter_by(uuid=user_uuid).first()

    if user is None:
        abort(404, 'User not found')

    scans = Scan.query_set.filter_by(user=user)
    user_scans = list(get_foot_scans(scans))

    return jsonify({'user_scans': user_scans})
