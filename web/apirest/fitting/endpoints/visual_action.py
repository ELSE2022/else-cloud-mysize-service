import requests
from pathlib import Path
from apirest.fitting.endpoints.action import get_user
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
from data.repositories import ScanVisualizationRepository
from data.repositories import CompareVisualizationRepository
from datetime import datetime
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
_scanVisualRep = ScanVisualizationRepository()
_compareVisualRep = CompareVisualizationRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'

update_compare_arguments = reqparse.RequestParser()
update_compare_arguments.add_argument('product_uuid', type=str, required=True)
update_compare_arguments.add_argument('size', type=str, required=True)
update_compare_arguments.add_argument('user', type=str, required=True)
update_compare_arguments.add_argument('scan_id', type=str, required=False)
update_compare_arguments.add_argument('environment_uuid', type=str, required=False)

update_scan_arguments = reqparse.RequestParser()
update_scan_arguments.add_argument('user', type=str, required=True)
update_scan_arguments.add_argument('scan_id', type=str, required=False)


@ns.route('/compare')
class VisualizationItem(Resource):
    @api.expect(update_compare_arguments, validate=True)
    def get(self):
        """
        Compare visualization
        """
        _graph = data_connection.get_graph()

        request_data = dict(request.args)
        product_uuid = request_data.get('product_uuid')[0]
        user_uuid = request_data.get('user')[0]
        size = request_data.get('size')[0]
        scan_id = request_data.get('scan_id', None)

        if scan_id:
            scans = _scanRep.get(dict(scan_id=scan_id))
            if not scans:
                return abort(400)
        else:
            scans = _scanRep.get_by_tree({'is_default': True, 'user': {'uuid': user_uuid}})
        all_requests = {}
        for scan in scans:
            scan_model_type = _graph.element_from_link(scan.model_type)
            last = _modelRep.get_by_tree(dict(product=dict(uuid=product_uuid),
                                              size=dict(string_value=size),
                                              model_type=scan_model_type._id))
            if not last:
                return abort(400)
            else: last = last[0]
            compare_visual = _compareVisualRep.get({'scan': scan, 'model': last})
            if not compare_visual:
                if last.stl_path and scan.stl_path:
                    last_stl_file = Path(last.stl_path)
                    scan_stl_file = Path(scan.stl_path)
                    if last_stl_file.is_file() and scan_stl_file.is_file():
                        files = {'last': open(last.stl_path, 'rb'), 'scan': open('attachments/' + scan.stl_path, 'rb')}
                        values = {'user_uuid': _graph.element_from_link(scan.user).uuid}
                        url = f'{ELSE_3D_SERVICE_URL}visualization/compare_visualization/'
                        if request_data.get('environment_uuid'):
                            values['environment_uuid'] = request_data.get('environment_uuid')[0]
                        req = requests.post(url, files=files, data=values)
                        all_requests[_graph.element_from_link(scan.model_type).name] = req.json()
                        _compareVisualRep.add(dict(scan=scan, model=last,
                                                   output_model=req.json().get('output_model'),
                                                   output_model_3d=req.json().get('output_model_3d'),
                                                   creation_time=datetime.now()))
            else:
                compare_visual = compare_visual[0]
                all_requests[_graph.element_from_link(scan.model_type).name] = {'output_model': compare_visual.output_model,
                                     'output_model_3d': compare_visual.output_model_3d}
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

        user = get_user(request_data.get('user')[0])
        scan_id = request_data.get('scan_id', None)

        if scan_id:
            scans = _scanRep.get(dict(user=user, scan_id=scan_id[0]))
            if not scans:
                return abort(400)
        else:
            scans = _scanRep.get(dict(user=user, is_default=True))
        all_requests = {}
        for scan in scans:
            scan_visual = _scanVisualRep.get({'scan': scan})
            if not scan_visual:
                files = {'scan': open('attachments/' + scan.stl_path, 'rb')}
                values = {'user_uuid': _graph.element_from_link(scan.user).uuid}
                url = f'{ELSE_3D_SERVICE_URL}visualization/scan/'
                req = requests.post(url, files=files, data=values)
                all_requests[_graph.element_from_link(scan.model_type).name] = req.json()
                _scanVisualRep.add(dict(scan=scan,
                                        output_model=req.json().get('output_model'),
                                        output_model_3d=req.json().get('output_model_3d'),
                                        creation_time=datetime.now()))
            else:
                scan_visual = scan_visual[0]
                all_requests[_graph.element_from_link(scan.model_type).name] = {'output_model': scan_visual.output_model,
                                                                                'output_model_3d': scan_visual.output_model_3d}
        return all_requests
