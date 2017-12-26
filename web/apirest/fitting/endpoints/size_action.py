from apirest.fitting.serializers import size
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
from pyorient import OrientRecordLink

ns = api.namespace('fitting/sizes/', description='Operations related to Size')

_productRep = ProductRepository()
_modelRep = ModelRepository()
_modelTypeRep = ModelTypeRepository()
_sizeRep = SizeRepository()
_brandRep = BrandRepository()
_compRuleRep = ComparisonRuleRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'


@ns.route('', '/', '/<string:uuid>')
class Sizes(Resource):
    @api.marshal_with(size)
    def get(self):
        """
        Returns a size list.
        """
        request_data = dict(request.args)
        page_start = int(request_data.get('_start')[0]) if request_data.get('_start', None) else None
        page_end = int(request_data.get('_end')[0]) if request_data.get('_end', None) else None

        size_obj = _sizeRep.get({})

        return (size_obj[page_start:page_end], 200, {'X-Total-Count': len(size_obj)}) if size_obj else (None, 404)

    @api.expect(size)
    def put(self, uuid):
        """
        Api method to update size.
        """
        model_type_obj = []
        for x in request.json['model_types']:
            model_type_obj.append(OrientRecordLink(x))

        data_dict = request.json
        data_dict['model_types'] = model_type_obj

        size_obj = _sizeRep.update({'@rid': uuid}, data_dict)[0]
        return {'@rid': size_obj._id, 'name': size_obj.string_value}, 201

    @api.expect(size)
    def post(self):
        """
        Api method to create size.
        """
        model_type_obj = _modelTypeRep.get({'@rid': request.json['model_type']})
        if not model_type_obj:
            abort(400, msg_object_does_not_exist.format('Model type', request.json['model_type']))

        data_dict = request.json
        data_dict['model_type'] = model_type_obj[0]
        size_obj = _sizeRep.add(data_dict, result_JSON=True)
        return size_obj
