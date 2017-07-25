import logging
from flask import Blueprint, jsonify, request, abort
from ..authentication import requires_auth

from data.repositories import UserRepository, ScanRepository, ScannerModelRepository, ScanMetricRepository, ScanMetricValueRepository
from data import data_connection
from calculations.fitting_algorithms.get_best_scan import get_best_scan

logger = logging.getLogger(__name__)

_userRep = UserRepository()
_scanRep = ScanRepository()
_scanModelRep = ScannerModelRepository()
_scanMetricRep = ScanMetricRepository()
_scanMetricValueRep = ScanMetricValueRepository()


def extract_calculation_attributes(scan, metrics):
    attrs = {}
    for metr in metrics:
        val = _scanMetricValueRep.get(dict(scan=scan, metric=metr))
        if len(val) > 0:
            val = val[0]
            try:
                attrs[metr.name] = float(val.value)
            except ValueError:
                False

    return attrs


def get_best_foot_scan(user, scanner_model):
    scans_data = {}
    _graph = data_connection.get_graph()
    scans = _scanRep.get_scans(user, scanner_model)
    metrics = _scanMetricRep.get(dict(scanner_model=scanner_model))

    for scan in scans:
        if not scan.scan_id in scans_data:
            scans_data[scan.scan_id] = {}

        if _graph.element_from_link(scan.model_type).name == 'LEFT_FOOT':
            scans_data[scan.scan_id]['LEFT'] = extract_calculation_attributes(scan, metrics)
        elif _graph.element_from_link(scan.model_type).name == 'RIGHT_FOOT':
            scans_data[scan.scan_id]['RIGHT'] = extract_calculation_attributes(scan, metrics)

    return get_best_scan(scans_data)


best_scan_action = Blueprint('best_scan_action', __name__)


@best_scan_action.route('/fitting/best_scan')
@requires_auth
def best_scan():
    user_uuid = request.args.get('user')
    user = _userRep.get(dict(uuid=user_uuid))
    if len(user) == 0:
        abort(404, 'user not found')
    else:
        user = user[0]

    model = request.args.get('scanner_model')
    scanner_model = _scanModelRep.get(dict(name=model))
    if len(scanner_model) == 0:
        abort(404, 'scanner_model not found')
    else:
        scanner_model = scanner_model[0]

    user_best_scan, user_best_scan_dist, scans_count, metrics_count = get_best_foot_scan(user, scanner_model)

    return jsonify({'scan_id': user_best_scan,
                    'distance': user_best_scan_dist,
                    'scans_processed': scans_count,
                    'metrics_count': metrics_count
                    })
