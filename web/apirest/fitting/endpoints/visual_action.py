import requests

from apirest.restplus import api
from data.repositories import ScannerRepository
from data.repositories import ScanRepository
from data.repositories import UserRepository
from data.repositories import ModelTypeRepository
from data.repositories import ScanMetricValueRepository
from data.repositories import ScanMetricRepository
from data.repositories import ProductRepository
from data.repositories import ScannerModelRepository
from data.repositories import ModelRepository
from flask import request
from flask import abort
from flask_restplus import Resource
from flask_restplus import reqparse
from settings import ELSE_3D_SERVICE_URL
from orientdb_data_layer import data_connection

ns = api.namespace('fitting_visualization', path='/fitting/visualization', description='Operations related to Visualization')

_scannerRep = ScannerRepository()
_scannerModelRep = ScannerModelRepository()
_scanMetricRep = ScanMetricRepository()
_scanMetricValueRep = ScanMetricValueRepository()
_scanRep = ScanRepository()
_productRep = ProductRepository()
_userRep = UserRepository()
_modelTypeRep = ModelTypeRepository()
_modelRep = ModelRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'

update_compare_arguments = reqparse.RequestParser()
update_compare_arguments.add_argument('product_uuid', type=str, required=True)
update_compare_arguments.add_argument('size', type=str, required=True)
update_compare_arguments.add_argument('scan_id', type=str, required=True)
update_compare_arguments.add_argument('environment_uuid', type=str, required=False)

update_scan_arguments = reqparse.RequestParser()
update_scan_arguments.add_argument('scan_id', type=str, required=True)


@ns.route('/compare')
class VisualizationItem(Resource):
    @api.expect(update_compare_arguments, validate=True)
    def post(self):
        """
        Compare visualization
        """
        _graph = data_connection.get_graph()

        request_data = dict(request.args)
        product_uuid = request_data.get('product_uuid')[0]
        size = request_data.get('size')[0]
        scan_id = request_data.get('scan_id')[0]

        scans = _scanRep.get(dict(scan_id=scan_id))
        if not scans:
            return abort(400)
        all_requests = []
        for scan in scans:
            scan_model_type = _graph.element_from_link(scan.model_type)
            last = _modelRep.get_by_tree(dict(product=dict(uuid=product_uuid),
                                              size=dict(string_value=size),
                                              model_type=scan_model_type._id))
            if not last:
                return abort(400)
            else: last = last[0]
            files = {'last': open(last.stl_path, 'rb'), 'scan': open('attachments/' + scan.stl_path, 'rb')}
            values = {'user_uuid': _graph.element_from_link(scan.user).uuid}
            url = f'{ELSE_3D_SERVICE_URL}visualization/compare_visualization/'
            if request_data.get('environment_uuid'):
                values['environment_uuid'] = request_data.get('environment_uuid')[0]
            req = requests.post(url, files=files, data=values)
            all_requests.append(req.json())
        return all_requests


@ns.route('/scan')
class VisualizationItem(Resource):
    @api.expect(update_scan_arguments, validate=True)
    def get(self):
        """
        User scan visualization
        """
        _graph = data_connection.get_graph()
        request_data = dict(request.args)

        scan_id = request_data.get('scan_id')[0]

        scans = _scanRep.get(dict(scan_id=scan_id))
        if not scans:
            return abort(400)
        all_requests = []
        for scan in scans:
            files = {'scan': open('attachments/' + scan.stl_path, 'rb')}
            values = {'user_uuid': _graph.element_from_link(scan.user).uuid}
            url = f'{ELSE_3D_SERVICE_URL}visualization/scan/'
            req = requests.post(url, files=files, data=values)
            all_requests.append(req.json())
        return all_requests
