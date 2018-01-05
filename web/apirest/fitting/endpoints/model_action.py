import base64
import os

from apirest.fitting.endpoints.scan_action import create_file
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
from flask_restplus import reqparse
from pathlib import Path
from pyorient import OrientRecordLink
from werkzeug.datastructures import FileStorage

ns = api.namespace('fitting_models', path='/fitting/models', description='Operations related to Size')

_productRep = ProductRepository()
_modelRep = ModelRepository()
_modelTypeRep = ModelTypeRepository()
_sizeRep = SizeRepository()
_brandRep = BrandRepository()
_compRuleRep = ComparisonRuleRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'
upload_parser = reqparse.RequestParser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)


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
        print('POST MODEL')
        attachment_path = None
        product_obj = _productRep.get({'@rid': request.json['product']})
        if not product_obj:
            abort(400, msg_object_does_not_exist.format('Product', request.json['product']))

        model_type_obj = _modelTypeRep.get({'@rid': request.json['model_type']})
        if not model_type_obj:
            abort(400, msg_object_does_not_exist.format('ModelType', request.json['model_type']))

        size_obj = _sizeRep.get({'@rid': request.json['size']})
        if not size_obj:
            abort(400, msg_object_does_not_exist.format('Size', request.json['size']))

        if request.json.get('pictures'):
            filecodestring = request.json['pictures'][0]['src']
            data = base64.b64decode(filecodestring.split(',')[1])
            attachment_name = os.path.sep.join(
                [
                    'Last',
                    product_obj[0].name,
                    '{}.{}'.format(size_obj[0].string_value, 'stl')
                ]
            )
            attachment_path = create_file(attachment_name)
            Path(attachment_path).write_bytes(data)
            print('Path1', attachment_path)

        model_obj = _modelRep.add({'name': request.json['name'], 'product': product_obj[0], 'size': size_obj[0],
                                   'model_type': model_type_obj[0], 'stl_path': attachment_path}, result_JSON=True)
        return model_obj

    # @api.expect(model)
    @api.expect(upload_parser, validate=True)
    def put(self, id):
        """
        Api method to update product.
        """
        print('UPDATE MODEL')
        print(request.json)

        data_dict = request.json
        data_dict['product'] = OrientRecordLink(request.json['product'])
        data_dict['model_type'] = OrientRecordLink(request.json['model_type'])
        data_dict['size'] = OrientRecordLink(request.json['size'])

        model_obj = _modelRep.update({'@rid': id}, data_dict)[0]
        return {'@rid': model_obj._id, 'name': model_obj.name}, 201

    @api.response(204, 'Model successfully deleted.')
    @api.marshal_with(model)
    def delete(self, id):
        """
        Api method to delete model.
        """
        _modelRep.delete({'@rid': id})
        return None, 204
