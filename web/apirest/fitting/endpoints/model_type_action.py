from apirest.fitting.serializers import model_type
from apirest.restplus import api
from data.repositories import ProductRepository
from data.repositories import ModelRepository
from data.repositories import ModelTypeRepository
from data.repositories import SizeRepository
from data.repositories import BrandRepository
from data.repositories import ComparisonRuleRepository
from flask import request, jsonify
from flask_restplus import Resource

ns = api.namespace('fitting_modeltypes', path='/fitting/modeltypes',  description='Operations related to Model Type')

_productRep = ProductRepository()
_modelRep = ModelRepository()
_modelTypeRep = ModelTypeRepository()
_sizeRep = SizeRepository()
_brandRep = BrandRepository()
_compRuleRep = ComparisonRuleRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'


@ns.route('')
class ModelTypes(Resource):
    @api.marshal_with(model_type)
    def get(self):
        """
        Returns a model types list.
        """
        request_data = dict(request.args)
        pagination_start = int(request_data.get('_start')[0]) if request_data.get('_start', None) else None
        pagination_end = int(request_data.get('_end')[0]) if request_data.get('_end', None) else None

        model_type_obj = _modelTypeRep.get({})

        return (model_type_obj[pagination_start:pagination_end], 200, {'X-Total-Count': len(model_type_obj)}) if model_type_obj else ([], 200, {'X-Total-Count': 0})

    @api.expect(model_type)
    def post(self):
        """
        Api method to create model type.
        """
        model_type_obj = _modelTypeRep.add({'name': request.json['name']}, result_JSON=True)
        return model_type_obj


@ns.route('/<string:id>')
class ModelTypesItem(Resource):
    def delete(self, id):
        """
        Api method to delete model type.
        """
        _modelTypeRep.delete({'@rid': id})
        return None, 204
