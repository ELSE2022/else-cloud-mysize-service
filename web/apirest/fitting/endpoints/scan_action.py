import csv
import os
import requests
import settings
import json
import ast
from apirest.fitting.serializers import scan as scan_serializer
from apirest.fitting.mixins import ListModelMixin
from apirest.restplus import api
from bs4 import BeautifulSoup
from data.repositories import ScannerRepository
from data.repositories import ScanRepository
from data.repositories import UserRepository
from data.repositories import ModelTypeRepository
from data.repositories import ScanMetricValueRepository
from data.repositories import ScanMetricRepository
from data.repositories import ProductRepository
from data.repositories import ScannerModelRepository
from data.models import Scan
from datetime import datetime
from datetime import timedelta
from flask import request
from flask import abort
from flask_restplus import Resource
from flask_restplus import reqparse
from orientdb_data_layer import data_connection
from pathlib import Path

ns = api.namespace('fitting_scans', path='/fitting/scans', description='Operations related to Scan')

_scannerRep = ScannerRepository()
_scannerModelRep = ScannerModelRepository()
_scanMetricRep = ScanMetricRepository()
_scanMetricValueRep = ScanMetricValueRepository()
_scanRep = ScanRepository()
_productRep = ProductRepository()
_userRep = UserRepository()
_modelTypeRep = ModelTypeRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'
attribute_urls_type = {
    'LEFT_FOOT': 'left',
    'RIGHT_FOOT': 'right',
}
scan_type_dict = {
    'FOOT': [{'name': 'LEFT_FOOT', 'stl_name': 'model_l.stl'},
             {'name': 'RIGHT_FOOT', 'stl_name': 'model_r.stl'}]
}

update_scan_arguments = reqparse.RequestParser()
update_scan_arguments.add_argument('user_uuid', type=str, required=True)
update_scan_arguments.add_argument('scanner', type=str, required=True)
update_scan_arguments.add_argument('type', type=str, required=True)
update_scan_arguments.add_argument('time', type=int, required=False)


@ns.route('')
class Scans(Resource, ListModelMixin):
    model = Scan
    serializer = scan_serializer
    filter_field = 'scan_id'

    def get(self):
        return super().get()

    @api.expect(scan_serializer)
    def post(self):
        """
        Api method to create scan.
        """
        user_obj = _userRep.get({'@rid': request.json['user']})
        if not user_obj:
            abort(400, msg_object_does_not_exist.format('User', request.json['user']))

        scanner_obj = _scannerRep.get({'@rid': request.json['scanner']})
        if not scanner_obj:
            abort(400, msg_object_does_not_exist.format('Scanner', request.json['scanner']))

        model_type_obj = _modelTypeRep.get({'@rid': request.json['model_type']})
        if not model_type_obj:
            abort(400, msg_object_does_not_exist.format('Model type', request.json['model_type']))

        data_dict = request.json
        data_dict['user'] = user_obj[0]
        data_dict['scanner'] = scanner_obj[0]
        data_dict['model_type'] = model_type_obj[0]
        scanner_obj = _scannerRep.add(data_dict, result_JSON=True)
        return scanner_obj


@ns.route('/<string:id>')
class ScanItem(Resource):
    @api.expect(scan_serializer)
    def put(self, id):
        """
        Api method to update scan.
        """
        scan_obj = _scanRep.update({'@rid': id}, request.json)[0]
        return {'@rid': scan_obj._id, 'name': scan_obj.name}, 201

    @api.response(204, 'Scan successfully deleted.')
    @api.marshal_with(scan_serializer)
    def delete(self, id):
        """
        Api method to delete scan.
        """
        _scanRep.delete({'@rid': id})
        return None, 204


def upload(url):
    request = requests.get(
        url=url,
    )
    request.raise_for_status()
    return request.content


def create_file(file_name):
    print(settings.MEDIA_ROOT, file_name)
    file_path = os.path.join(
        # os.sep,
        settings.MEDIA_ROOT.strip('/'),
        file_name
    )
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    Path(file_path).touch()
    return file_path


def update_scan_attributes(scan, scan_type):
    _graph = data_connection.get_graph()
    scanner_obj = _graph.element_from_link(scan.scanner)
    path_to_csv = '{}{}/{}/{}_{}_mes.csv'.format(scanner_obj.base_url, scanner_obj.name, scan.scan_id, scan.scan_id, attribute_urls_type[scan_type.name])
    request = requests.get(path_to_csv)
    first_row = next(request.iter_lines(decode_unicode=True))
    profile = request.iter_lines(decode_unicode=True)
    if first_row.startswith('DOMESCAN'):
        next(profile)
    request.raise_for_status()
    for row in csv.DictReader(profile, delimiter=';'):
        for key, value in row.items():
            if key != '':
                name = key.strip()
                print('PARSE METRIC1', name, value)
                scan_metric = _scanMetricRep.get(dict(name=name, scanner_model=scanner_obj.model))
                if not scan_metric:
                    scan_metric = _scanMetricRep.add(dict(name=name, scanner_model=_graph.element_from_link(scanner_obj.model)))
                else:
                    scan_metric = scan_metric[0]
                results = _scanMetricValueRep.update(dict(scan=scan, metric=scan_metric), dict(value=value))
                if not results:
                    _scanMetricValueRep.add(dict(scan=scan, metric=scan_metric, value=value))


def str2bool(in_str):
    return in_str in ['true', 'True', 'yes']


def get_last_scan_id(scanner, interval):
    url = f'{scanner.base_url}{scanner.name}/?C=M;O=D'
    request = requests.get(
        url=url,
    )
    request_date = datetime.strptime(request.headers['Date'].strip(), '%a, %d %b %Y %H:%M:%S %Z')
    bs = BeautifulSoup(request.text, 'html.parser')
    image_tag = bs.find('img', alt='[DIR]')
    row = None
    if image_tag is not None:
        row = image_tag.find_parent('tr')
    scan_id = None
    if row is not None:
        date_tag = row.find('td', attrs={'align': 'right'},)
        string_date = None
        date = None
        if date_tag is not None:
            string_date = date_tag.string
        if string_date is not None:
            date = datetime.strptime(string_date.strip(), '%Y-%m-%d %H:%M')
        if request_date and date:
            diff = request_date - date
            if diff < timedelta(minutes=interval):
                scan_id = row.find('a', href=True,).string.split('/')[0]
    return scan_id


def update_scan(user, scanner, scan_id, scan_model_type, is_scan_default, scan_path):
    print(user, scanner, scan_model_type, scan_id)
    data_connection.get_graph()
    # scanner_model = _scannerModelRep.get({})
    # if not scanner_model:
    #     scanner_model = _scannerModelRep.add(dict(name=scanner_name))
    # else: scanner_model = scanner_model[0]

    # scanner = _scannerRep.get({'name': scanner_name})
    # if not scanner:
    #     scanner = _scannerRep.add(dict(name=scanner_name, model=scanner_model))
    # else:
    #     scanner = scanner[0]

    scan_type = _modelTypeRep.get({'name': scan_model_type})
    if not scan_type:
        scan_type = _modelTypeRep.add(dict(name=scan_model_type))
    else:
        scan_type = scan_type[0]

    # scan = _scanRep.get(dict(user=user, model_type=scan_type, scan_id=scan_id))
    # if not scan:
    #     scan = _scanRep.add(dict(user=user, model_type=scan_type, scan_id=scan_id, scanner=scanner, creation_time=datetime.now(), is_default=is_scan_default))
    # else: scan = scan[0]

    foot_attachment_content = upload(scan_path)
    attachment_name = os.path.sep.join(
        [
            'Scan',
            user.uuid,
            '{}-{}-{}'.format(datetime.now().year, datetime.now().month, datetime.now().day),
            '{}.{}'.format(scan_type.name, 'stl')
        ]
    )

    # attachment_name = gen_file_name(scan, '{}.{}'.format(scan_type, STL_EXTENSION))
    attachment_path = create_file(attachment_name)
    Path(attachment_path).write_bytes(foot_attachment_content)
    print('Path', attachment_path)
    # scan = _scanRep.update(dict(user=user, model_type=scan_type, scan_id=scan_id), dict(stl_path=attachment_name, is_default=is_scan_default))[0]
    scan = _scanRep.get(dict(user=user, model_type=scan_type, scan_id=scan_id))
    if not scan:
        scan = _scanRep.add(dict(user=user, model_type=scan_type, scan_id=scan_id, scanner=scanner, stl_path=attachment_name, creation_time=datetime.now(), is_default=is_scan_default))
    else:
        scan = _scanRep.update(dict(user=user, model_type=scan_type, scan_id=scan_id), dict(stl_path=attachment_name, is_default=is_scan_default))[0]
    if is_scan_default:
        _scanRep.update({'user': user}, {'is_default': False})
        _scanRep.update({'user': user, 'scan_id': scan_id}, {'is_default': True})

    _scanMetricValueRep.delete(dict(scan=scan))

    try:
        update_scan_attributes(scan, scan_type)
    except requests.HTTPError:
        print('HTTPError')
    return scan


def update_foot_scans(user, scanner, scan_id, scan_types, is_scan_default):
    scans = []
    for scan_type in scan_types:
        try:
            scan = update_scan(user, scanner, scan_id, scan_type['name'], is_scan_default, '{}{}/{}/{}'.format(scanner.base_url, scanner.name, scan_id, scan_type['stl_name']))
        except requests.HTTPError:
            scan = None
        scans.append(scan) if scan else None
    return scans


@ns.route('/<string:scan_id>/update_user_scan', '/update_last_scan')
@api.response(404, 'Scan not found.')
class ScanItem(Resource):
    @api.expect(update_scan_arguments, validate=True)
    def post(self, scan_id=None):
        """
        Returns a scans.
        """
        request_data = dict(request.args)
        user_uuid = request_data.get('user_uuid')[0]
        scanner = request_data.get('scanner')[0]
        interval = request_data.get('time', None)
        # scan_obj_id = scan_id

        scan_type = request_data.get('type')[0].upper()
        is_scan_default = str2bool(request.args.get('is_default', 'false'))
        request_data.get('brand', None)
        user = _userRep.get(dict(uuid=user_uuid))
        if not user:
            user = _userRep.add(dict(uuid=user_uuid))
        else:
            user = user[0]

        scanner = _scannerRep.get(dict(name=scanner))
        if not scanner:
            abort(400, msg_object_does_not_exist.format('Scanner', scanner))
        else:
            scanner = scanner[0]

        if interval:
            scan_id = get_last_scan_id(scanner, int(interval[0]))
            if scan_id is None:
                return abort(400)
        scans = update_foot_scans(user, scanner, scan_id, scan_type_dict[scan_type], is_scan_default)
        if len(scans) == 0:
            return abort(400)
        return json.dumps([str(scan.scan_id) for scan in scans])
