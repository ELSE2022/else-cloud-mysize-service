from apirest.fitting.serializers import model
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

ns = api.namespace('fitting/models/', description='Operations related to Size')

_productRep = ProductRepository()
_modelRep = ModelRepository()
_modelTypeRep = ModelTypeRepository()
_sizeRep = SizeRepository()
_brandRep = BrandRepository()
_compRuleRep = ComparisonRuleRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'


@ns.route('', '/', '/<string:id>')
class Models(Resource):
    @api.marshal_with(model)
    def get(self, id=None):
        """
        Returns a models list.
        """
        request_data = dict(request.args)
        page_start = int(request_data.get('_start')[0]) if request_data.get('_start', None) else None
        page_end = int(request_data.get('_end')[0]) if request_data.get('_end', None) else None

        model_obj = _modelRep.get({})

        return (model_obj[page_start:page_end], 200, {'X-Total-Count': len(model_obj)}) if model_obj else ([], 200, {'X-Total-Count': 0})

    @api.expect(model)
    def post(self):
        """
        Api method to create model.
        """
        product_obj = _productRep.get({'@rid': request.json['product']})
        if not product_obj:
            abort(400, msg_object_does_not_exist.format('Product', request.json['product']))

        model_type_obj = _modelTypeRep.get({'@rid': request.json['model_type']})
        if not model_type_obj:
            abort(400, msg_object_does_not_exist.format('ModelType', request.json['model_type']))

        size_obj = _sizeRep.get({'@rid': request.json['size']})
        if not size_obj:
            abort(400, msg_object_does_not_exist.format('Size', request.json['size']))

        model_obj = _modelRep.add({'name': request.json['name'], 'product': product_obj[0], 'size': size_obj[0],
                                   'model_type': model_type_obj[0]}, result_JSON=True)
        return model_obj

    # @api.marshal_with(model)
    # def get(self, id):
    #     """
    #     Returns a model object.
    #     """
    #     model_obj = _modelRep.get({'@rid': id})
    #     return model_obj[0] if model_obj else (None, 404)

    @api.response(204, 'Model successfully deleted.')
    @api.marshal_with(model)
    def delete(self, id):
        """
        Api method to delete model.
        """
        _modelRep.delete({'@rid': id})
        return None, 204

#
# @ns.route('/models/<string:id>')
# @api.response(404, 'Model not found.')
# class ModelItem(Resource):
#
#     @api.marshal_with(model)
#     def get(self, id):
#         """
#         Returns a model object.
#         """
#         model_obj = _modelRep.get({'@rid': id})
#         return model_obj[0] if model_obj else (None, 404)
#
#     @api.response(204, 'Model successfully deleted.')
#     @api.marshal_with(model)
#     def delete(self, id):
#         """
#         Api method to delete model.
#         """
#         _modelRep.delete({'@rid': id})
#         return None, 204
