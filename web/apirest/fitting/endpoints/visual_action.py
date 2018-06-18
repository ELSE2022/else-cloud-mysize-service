import requests
import os
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
from flask import abort
from flask_restplus import Resource
from flask_restplus import reqparse
from settings import ELSE_3D_SERVICE_FULL
from orientdb_data_layer import data_connection
from data.models import User
from data.models import CompareVisualization
from data.models import Scan
import logging

logger = logging.getLogger('rest_api_demo')

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
update_compare_arguments.add_argument('env', type=str, required=False)

update_scan_arguments = reqparse.RequestParser()
update_scan_arguments.add_argument('user', type=str, required=True)
update_scan_arguments.add_argument('scan_id', type=str, required=False)
update_scan_arguments.add_argument('env', type=str, required=False)


@ns.route('/compare')
class VisualizationItem(Resource):
    @api.expect(update_compare_arguments, validate=True)
    def get(self):
        """
        Compare visualization
        """
        _graph = data_connection.get_graph()
        logger.info('VISUALIZATION COMPARE')
        logger.debug('VISUALIZATION COMPARE DEBUG')
        args = update_compare_arguments.parse_args()
        product_uuid = args.get('product_uuid')
        user_uuid = args.get('user')
        size = args.get('size')
        scan_id = args.get('scan_id', None)
        environment_uuid = args.get('environment_uuid')

        user = User.query_set.filter_by(uuid=user_uuid).first()

        if user is None:
            abort(404, 'User not found')

        if scan_id:
            scans = Scan.query_set.filter_by(user=user, scan_id=scan_id)
        else:
            scans = Scan.query_set.filter_by(user=user, is_default=True)
        if scans.count() == 0:
            return abort(400)
        all_requests = {}
        for scan in scans:
            scan_model_type = _graph.element_from_link(scan.model_type)
            last = _modelRep.get_by_tree(dict(product=dict(uuid=product_uuid),
                                              size=dict(string_value=size),
                                              model_type=scan_model_type._id))
            if not last:
                return abort(400)
            else:
                last = last[0]
            compare_visual = CompareVisualization.query_set.filter_by(scan=scan, model=last).first()
            if compare_visual is None:
                if last.stl_path and scan.stl_path:
                    if os.path.isfile(last.stl_path) and os.path.isfile('attachments/' + scan.stl_path):
                        file_last = open(last.stl_path, 'rb')
                        file_scan = open('attachments/' + scan.stl_path, 'rb')
                        files = {'last': file_last, 'scan': file_scan}
                        values = {'user_uuid': _graph.element_from_link(scan.user).uuid}
                        url = f'{ELSE_3D_SERVICE_FULL}/visualization/compare_visualization/'
                        if environment_uuid:
                            values['environment_uuid'] = environment_uuid
                        logger.debug('LOG BEFORE REQUEST')
                        req = requests.post(url, files=files, data=values)
                        logger.debug('LOG AFTER REQUEST')
                        result_json = req.json()
                        file_last.close()
                        file_scan.close()
                        all_requests[_graph.element_from_link(scan.model_type).name] = result_json
                        # _compareVisualRep.add(dict(scan=scan, model=last,
                        #                            output_model=result_json.get('output_model'),
                        #                            output_model_3d=result_json.get('output_model_3d'),
                        #                            creation_time=datetime.now()))
            else:
                all_requests[_graph.element_from_link(scan.model_type).name] = {
                    'output_model': compare_visual.output_model, 'output_model_3d': compare_visual.output_model_3d}
        return all_requests


@ns.route('/scan')
class VisualizationItem(Resource):
    @api.expect(update_scan_arguments, validate=True)
    def get(self):
        """
        User scan visualization
        """
        _graph = data_connection.get_graph()

        args = update_scan_arguments.parse_args()

        user = get_user(args.get('user'))
        scan_id = args.get('scan_id', None)

        if scan_id:
            scans = _scanRep.get(dict(user=user, scan_id=scan_id))
            if not scans:
                return abort(400)
        else:
            scans = _scanRep.get(dict(user=user, is_default=True))
        all_requests = {}
        for scan in scans:
            scan_visual = _scanVisualRep.get({'scan': scan})
            if not scan_visual:
                if scan.stl_path and os.path.isfile('attachments/' + scan.stl_path):
                    files = {'scan': open('attachments/' + scan.stl_path, 'rb')}
                    values = {'user_uuid': _graph.element_from_link(scan.user).uuid}
                    url = f'{ELSE_3D_SERVICE_FULL}/visualization/scan/'
                    req = requests.post(url, files=files, data=values)
                    result_json = req.json()
                    all_requests[_graph.element_from_link(scan.model_type).name] = result_json
                    _scanVisualRep.add(dict(scan=scan,
                                            output_model=result_json.get('output_model'),
                                            output_model_3d=result_json.get('output_model_3d'),
                                            creation_time=datetime.now()))
            else:
                scan_visual = scan_visual[0]
                all_requests[_graph.element_from_link(scan.model_type).name] = {
                    'output_model': scan_visual.output_model,
                    'output_model_3d': scan_visual.output_model_3d}
        return all_requests
