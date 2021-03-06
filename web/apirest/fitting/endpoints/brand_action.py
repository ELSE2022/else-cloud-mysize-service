from apirest.fitting.serializers import brand
from apirest.fitting.mixins import ListModelMixin
from apirest.restplus import api
from data.repositories import ProductRepository
from data.repositories import ModelRepository
from data.repositories import ModelTypeRepository
from data.repositories import SizeRepository
from data.repositories import BrandRepository
from data.repositories import ComparisonRuleRepository
from data.models import Brand
from flask import request
from flask import abort
from flask_restplus import Resource

ns = api.namespace('fitting_brands', path='/fitting/brands', description='Operations related to Brand')

_productRep = ProductRepository()
_modelRep = ModelRepository()
_modelTypeRep = ModelTypeRepository()
_sizeRep = SizeRepository()
_brandRep = BrandRepository()
_compRuleRep = ComparisonRuleRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'


@ns.route('')
class Brands(Resource, ListModelMixin):
    model = Brand
    serializer = brand

    def get(self):
        return super().get()

    @api.expect(brand)
    def post(self):
        """
        Api method to create brand.
        """
        brand_obj = _brandRep.add(request.json, result_JSON=True)
        return brand_obj


@ns.route('/<string:id>')
class BrandItem(Resource):
    @api.expect(brand)
    def delete(self, id):
        """
        Api method to delete brand.
        """
        _brandRep.delete({'@rid': id})
        return None, 204

    @api.expect(brand)
    def put(self, id):
        """
        Api method to update brand
        """
        brand_obj = _brandRep.update({'@rid': id}, request.json)
        return {'@rid': brand_obj[0]._id, 'name': brand_obj[0].name}, 201
