import requests
import json
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
from services.scan_actions import ScanActionService

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


def update_foot_scans(user, scanner, scan_id, scan_types, is_scan_default):
    scans = []
    for scan_type in scan_types:
        try:
            scan = ScanActionService.update_user_scan(
                user,
                scanner,
                scan_id,
                scan_type['name'],
                is_scan_default,
                '{}{}/{}/{}'.format(scanner.base_url, scanner.name, scan_id, scan_type['stl_name'])
            )
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
