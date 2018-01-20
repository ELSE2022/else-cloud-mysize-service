from apirest.fitting.serializers import scan_metric
from apirest.restplus import api
from data.repositories import ScanMetricRepository
from flask import request
from flask_restplus import Resource

ns = api.namespace('fitting_scanmetrics', path='/fitting/scanmetrics', description='Operations related to Scan metrics')

_scanMetricRep = ScanMetricRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'


@ns.route('',)
class ScanMetrics(Resource):
    @api.marshal_with(scan_metric)
    def get(self):
        """
        Returns a scan metrics list.
        """
        request_data = dict(request.args)
        page_start = int(request_data.get('_start')[0]) if request_data.get('_start', None) else None
        page_end = int(request_data.get('_end')[0]) if request_data.get('_end', None) else None

        scan_metric_obj = _scanMetricRep.get({})
        return (scan_metric_obj[page_start:page_end], 200, {'X-Total-Count': len(scan_metric_obj)}) if scan_metric_obj else ([], 200, {'X-Total-Count': 0})

    @api.expect(scan_metric)
    def post(self):
        """
        Api method to create scan metric.
        """
        scan_metric_obj = _scanMetricRep.add(request.json, result_JSON=True)
        return scan_metric_obj


@ns.route('/<string:id>')
class ScanMetricItem(Resource):
    @api.expect(scan_metric)
    def put(self, id):
        """
        Api method to update scan metric.
        """
        scan_metric_obj = _scanMetricRep.update({'@rid': id}, request.json)[0]
        return {'@rid': scan_metric_obj._id, 'name': scan_metric_obj.name}, 201

    @api.response(204, 'Scan metric successfully deleted.')
    def delete(self, id):
        """
        Api method to delete scan metric.
        """
        _scanMetricRep.delete({'@rid': id})
        return None, 204
