from apirest.fitting.serializers import model_metric_value
from apirest.restplus import api
from data.repositories import ModelMetricValueRepository
from flask import request
from flask_restplus import Resource

ns = api.namespace('fitting_modelmetricvalues', path='/fitting/modelmetricvalues', description='Operations related to Model metric value')

_modelMetricValueRep = ModelMetricValueRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'


@ns.route('',)
class ModelMetricValue(Resource):
    @api.marshal_with(model_metric_value)
    def get(self):
        """
        Returns a model metric values list.
        """
        request_data = dict(request.args)
        page_start = int(request_data.get('_start')[0]) if request_data.get('_start', None) else None
        page_end = int(request_data.get('_end')[0]) if request_data.get('_end', None) else None

        model_metric_value_obj = _modelMetricValueRep.get({})
        return (model_metric_value_obj[page_start:page_end], 200, {'X-Total-Count': len(model_metric_value_obj)}) if model_metric_value_obj else ([], 200, {'X-Total-Count': 0})

    @api.expect(model_metric_value)
    def post(self):
        """
        Api method to create model metric value.
        """
        model_metric_value_obj = _modelMetricValueRep.add(request.json, result_JSON=True)
        return model_metric_value_obj


@ns.route('/<string:id>')
class ModelMetricValueItem(Resource):
    @api.expect(model_metric_value)
    def put(self, id):
        """
        Api method to update model metric value.
        """
        model_metric_value_obj = _modelMetricValueRep.update({'@rid': id}, request.json)[0]
        return {'@rid': model_metric_value_obj._id}, 201

    @api.response(204, 'Model metric value successfully deleted.')
    def delete(self, id):
        """
        Api method to delete model metric value.
        """
        _modelMetricValueRep.delete({'@rid': id})
        return None, 204
