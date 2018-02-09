from apirest.fitting.serializers import scan_metric
from apirest.fitting.mixins import ListModelMixin
from apirest.restplus import api
from data.repositories import ScanMetricRepository
from data.models import ScanMetric
from flask import request
from flask_restplus import Resource

ns = api.namespace('fitting_scanmetrics', path='/fitting/scanmetrics', description='Operations related to Scan metrics')

_scanMetricRep = ScanMetricRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'


@ns.route('',)
class ScanMetrics(Resource, ListModelMixin):
    model = ScanMetric
    serializer = scan_metric

    def get(self):
        return super().get()

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
