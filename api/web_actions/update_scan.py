from flask import Blueprint
from flask import jsonify
from flask import request
from flask import abort

from data.repositories import UserRepository
from data.repositories import ScanRepository
from data.repositories import ScannerRepository
from data.repositories import ModelTypeRepository
from data.repositories import ScanMetricRepository
from data.repositories import ScanMetricValueRepository

from orientdb_data_layer import data_connection
from data import cloud_object_storage

import requests
import csv


update_scan_action = Blueprint('update_scan_action', __name__)

_userRep = UserRepository()
_scanRep = ScanRepository()
_scannerRep = ScannerRepository()
_modelTypeRep = ModelTypeRepository()
_scanMetricRep = ScanMetricRepository()
_scanMetricValueRep = ScanMetricValueRepository()


@update_scan_action.route('/fitting/update_scan')
def update_scan():
    user_uuid = request.args.get('user')
    scanner_id = request.args.get('scanner')
    scan_id = request.args.get('scan')
    scan_type = request.args.get('type', 'FOOT').upper()
    brand_id = request.args.get('brand')
    is_scan_default = request.args.get('is_default', 'false')

    # TODO: if the user doesn't exist, create a new one
    user = get_user(user_uuid)
    scanner = get_scanner(scanner_id)

    scans = update_foot_scans(user, scanner, scan_id)

    # TODO: start comparison
    # TODO: save new links to scans on cloud
    # TODO: What is there's only one scan?
    if is_scan_default or not has_default_scans(user):
        set_default_scan(user, scans[0])
        set_default_scan(user, scans[1])

    return jsonify(
        [scan_to_string(scan) for scan in scans]
    )


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


def get_scanner(scanner_id):
    if scanner_id is None:
        abort(400, 'Request malformed: \'scanner\' argument not passed')
    scanner = _scannerRep.get({
        'name': scanner_id,
    })
    if not scanner:
        abort(404, 'Scanner does not exist: {}'.format(scanner_id))
    return scanner[0]


def set_default_scan(user, scan):
    graph = data_connection.get_graph()
    model_type = graph.element_from_link(scan.model_type)

    default_scans = _scanRep.get({
        'user': user,
        'model_type': model_type,
    })

    for default_scan in default_scans:
        _scanRep.update({'@rid': default_scan._id}, {'is_default': False})

    _scanRep.update({'@rid': scan._id}, {'is_default': True})


def has_default_scans(user):
    scans = _scanRep.get({
        'user': user,
    })
    result = False
    for scan in scans:
        if scan.is_default:
            result = True
            break
    return result


def scan_to_string(scan):
    graph = data_connection.get_graph()

    scan_id = scan.scan_id
    user_uuid = graph.element_from_link(scan.user).uuid
    scanner = graph.element_from_link(scan.scanner).name
    model_type = graph.element_from_link(scan.model_type).name
    date = str(scan.creation_time)

    return 'scan_id: {}, user: {}, scanner: {}, type: {}, created_date: {}'\
        .format(scan_id, user_uuid, scanner, model_type, date)


def update_foot_scans(user, scanner, scan_id):
    left_scan = update_scan_attributes(user, scanner, scan_id, 'LEFT_FOOT',
                                       '{}{}/{}/model_l.stl'.format(user.base_url, scanner, scan_id))
    right_scan = update_scan_attributes(user, scanner, scan_id, 'RIGHT_FOOT',
                                        '{}{}/{}/model_r.stl'.format(user.base_url, scanner, scan_id))
    return [left_scan, right_scan]


def download_scan(scan_path):
    scan = requests.head(scan_path)
    if scan.status_code >= 400:
        abort(scan.status_code, 'Can\'t download the scan: {}'.format(scan_path))
    scan = requests.get(scan_path)
    return scan.content


def update_scan_attributes(user, scanner, scan_id, scan_type, scan_path):
    model_type = _modelTypeRep.get({
        'name': scan_type,
    })[0]

    scan = _scanRep.get({
        'user': user,
        'model_type': model_type,
        'scan_id': scan_id,
    })[0]

    # TODO: catch the exception
    # if not scan:
    #     _scanRep.add({
    #         'user': user,
    #         'model_type': model_type,
    #         'scan_id': scan_id,
    #         'scanner': scanner,
    #     })
    # else:
    #     _scanRep.update({
    #         'user': user,
    #         'model_type': model_type,
    #         'scan_id': scan_id,
    #     }, {
    #         'scanner': scanner,
    #     })

    scan_content = download_scan(scan_path)
    filename = generate_filename(scan_path)

    scan_container = cloud_object_storage.get_container('scans')
    scan_container.add_object(filename, scan_content)
    # TODO: ADD NEW NAME INSTEAD OF LINK
    # scan.attachment = attachment_name
    update_metrics(user.base_url, scan, scan_type)
    return scan


def update_metrics(base_url, scan, model_type):
    profile = download_csv(base_url, scan, model_type)
    update_metric_values(scan, profile)


def download_csv(base_url, scan, model_type):
    graph = data_connection.get_graph()

    url = base_url
    scanner_name = graph.element_from_link(scan.scanner).name
    scan_id = scan.scan_id
    scan_type = 'right' if model_type == 'RIGHT_FOOT' else 'left'

    csv_path = '{}{}/{}/{}_{}_mes.csv'.format(
        url,
        scanner_name,
        scan_id,
        scan_id,
        scan_type,
    )

    csv_file = requests.head(csv_path)
    if csv_file.status_code >= 400:
        abort(csv_file.status_code, 'Can\'t get csv')
    csv_file = requests.get(csv_path)

    return list(csv_file.iter_lines(decode_unicode=True))[1:]


def update_metric_values(scan, profile):
    for row in csv.DictReader(profile, delimiter=';'):
        for key, value in row.items():
            if not key:
                continue
            name = key.strip()

            scan_metric = _scanMetricRep.get({
                'name': name,
            })

            _scanMetricValueRep.update({
                'scan': scan,
                'metric': scan_metric[0],
            }, {
                'value': value,
            })


def generate_filename(file_path):
    values = file_path.split('/')[-3:]
    filename = '_'.join(values)
    return filename
