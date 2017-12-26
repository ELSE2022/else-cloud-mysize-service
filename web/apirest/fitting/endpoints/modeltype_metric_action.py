from apirest.fitting.serializers import model_type_metric
from apirest.restplus import api
from data.repositories import ModelTypeMetricRepository
from flask import request
from flask_restplus import Resource

ns = api.namespace('fitting/modelmetrics/', description='Operations related to Model metrics')

_modelTypeMetricRep = ModelTypeMetricRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'


@ns.route('', '/', '/<string:uuid>')
class ModelMetrics(Resource):
    @api.marshal_with(model_type_metric)
    def get(self):
        """
        Returns a model metrics list.
        """
        request_data = dict(request.args)
        page_start = int(request_data.get('_start')[0]) if request_data.get('_start', None) else None
        page_end = int(request_data.get('_end')[0]) if request_data.get('_end', None) else None

        model_metric_obj = _modelTypeMetricRep.get({})
        return (model_metric_obj[page_start:page_end], 200, {'X-Total-Count': len(model_metric_obj)}) if model_metric_obj else ([], 200, {'X-Total-Count': 0})

    @api.expect(model_type_metric)
    def post(self):
        """
        Api method to create model metric.
        """
        model_metric_obj = _modelTypeMetricRep.add(request.json, result_JSON=True)
        return model_metric_obj

    @api.expect(model_type_metric)
    def put(self, uuid):
        """
        Api method to update scan metric.
        """
        model_metric_obj = _modelTypeMetricRep.update({'@rid': uuid}, request.json)[0]
        return {'@rid': model_metric_obj._id, 'name': model_metric_obj.name}, 201

    @api.response(204, 'Model metric successfully deleted.')
    def delete(self, uuid):
        """
        Api method to delete scan metric.
        """
        _modelTypeMetricRep.delete({'@rid': uuid})
        return None, 204
