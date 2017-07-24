import sys
import logging
from flask import Blueprint, jsonify, request, abort

sys.path.append('/')
from data.repositories import UserRepository, ScanRepository
from data.models import Scan

logger = logging.getLogger(__name__)

_userRep = UserRepository()
_scanRep = ScanRepository()


def get_best_foot_scan(user):
    scans_data = {}

    return 1,1,1,1


best_scan_action = Blueprint('best_scan_action', __name__)


@best_scan_action.route('/fitting/best_scan')
def best_scan():
    user_uuid = request.args.get('user')
    user = _userRep.get(dict(uuid=user_uuid))
    if len(user) == 0:
        abort(404, 'user not found')
    else:
        user = user[0]

    sc = _scanRep.get(dict(user=user))

    get_best_foot_scan(user)

    return 'test'
