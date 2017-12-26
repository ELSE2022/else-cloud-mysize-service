from apirest.fitting.serializers import brand
from apirest.restplus import api
from data.repositories import ProductRepository
from data.repositories import ModelRepository
from data.repositories import ModelTypeRepository
from data.repositories import SizeRepository
from data.repositories import BrandRepository
from data.repositories import ComparisonRuleRepository
from flask import request
from flask import abort
from flask_restplus import Resource

ns = api.namespace('fitting/brands/', description='Operations related to Brand')

_productRep = ProductRepository()
_modelRep = ModelRepository()
_modelTypeRep = ModelTypeRepository()
_sizeRep = SizeRepository()
_brandRep = BrandRepository()
_compRuleRep = ComparisonRuleRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'


@ns.route('', '/', '/<string:uuid>')
class Brands(Resource):
    @api.marshal_with(brand)
    def get(self):
        """
        Returns a brands list.
        """
        request_data = dict(request.args)
        page_start = int(request_data.get('_start')[0]) if request_data.get('_start', None) else None
        page_end = int(request_data.get('_end')[0]) if request_data.get('_end', None) else None

        brand_obj = _brandRep.get({})
        return (brand_obj[page_start:page_end], 200, {'X-Total-Count': len(brand_obj)}) if brand_obj else ([], 200, {'X-Total-Count': 0})

    @api.expect(brand)
    def post(self):
        """
        Api method to create brand.
        """
        brand_obj = _brandRep.add(request.json, result_JSON=True)
        return brand_obj
