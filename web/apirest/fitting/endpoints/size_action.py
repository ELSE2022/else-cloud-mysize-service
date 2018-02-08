from apirest.fitting.serializers import size
from apirest.fitting.mixins import ListModelMixin
from apirest.restplus import api
from data.repositories import ProductRepository
from data.repositories import ModelRepository
from data.repositories import ModelTypeRepository
from data.repositories import SizeRepository
from data.repositories import BrandRepository
from data.repositories import ComparisonRuleRepository
from data.models import Size
from flask import request
from flask import abort
from flask_restplus import Resource
from pyorient import OrientRecordLink

ns = api.namespace('fitting_sizes', path='/fitting/sizes', description='Operations related to Size')

_productRep = ProductRepository()
_modelRep = ModelRepository()
_modelTypeRep = ModelTypeRepository()
_sizeRep = SizeRepository()
_brandRep = BrandRepository()
_compRuleRep = ComparisonRuleRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'


@ns.route('', '/')
class Sizes(Resource, ListModelMixin):
    model = Size
    serializer = size

    def get(self):
        return super().get()

    @api.expect(size)
    def post(self):
        """
        Api method to create size.
        """
        model_type_obj = []
        for x in request.json['model_types']:
            model_type_obj.append(_modelTypeRep.get({'@rid': x})[0])

        data_dict = request.json
        data_dict['model_types'] = model_type_obj
        size_obj = _sizeRep.add(data_dict, result_JSON=True)
        return size_obj


@ns.route('/<string:id>')
class SizeItem(Resource):
    @api.expect(size)
    def delete(self, id):
        """
        Api method to delete size
        """
        _sizeRep.delete({'@rid': id})
        return None, 204

    @api.expect(size)
    def put(self, id):
        """
        Api method to update size.
        """
        model_type_obj = []
        for x in request.json['model_types']:
            model_type_obj.append(OrientRecordLink(x))

        data_dict = request.json
        data_dict['model_types'] = model_type_obj

        size_obj = _sizeRep.update({'@rid': id}, data_dict)[0]
        return {'@rid': size_obj._id, 'name': size_obj.string_value}, 201
