import base64
import os

from apirest.fitting.endpoints.scan_action import create_file
from apirest.fitting.serializers import model
from apirest.fitting.mixins import ListModelMixin
from apirest.restplus import api
from data.repositories import ProductRepository
from data.repositories import ModelRepository
from data.repositories import ModelTypeRepository
from data.repositories import SizeRepository
from data.repositories import BrandRepository
from data.repositories import ComparisonRuleRepository
from data.models import Model
from flask import request
from flask import abort
from flask_restplus import Resource
from flask_restplus import reqparse
from pathlib import Path
from pyorient import OrientRecordLink
from werkzeug.datastructures import FileStorage
from orientdb_data_layer import data_connection

ns = api.namespace('fitting_models', path='/fitting/models', description='Operations related to Model')

_productRep = ProductRepository()
_modelRep = ModelRepository()
_modelTypeRep = ModelTypeRepository()
_sizeRep = SizeRepository()
_brandRep = BrandRepository()
_compRuleRep = ComparisonRuleRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'
upload_parser = reqparse.RequestParser()
# upload_parser.add_argument('product', type=str, required=True)
upload_parser.add_argument('file', location='json', type=FileStorage, required=True)


@ns.route('',)
class Models(Resource, ListModelMixin):
    model = Model
    serializer = model

    def get(self):
        return super().get()

    @api.expect(model)
    def post(self):
        """
        Api method to create model.
        """
        print('POST MODEL', request.json)
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

        files = request.json.get('files')
        if files:
            filecodestring = files[0]['src']
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

        model_obj = _modelRep.add({'name': request.json['name'], 'product': product_obj[0], 'size': size_obj[0],
                                   'model_type': model_type_obj[0], 'stl_path': attachment_path}, result_JSON=True)
        return model_obj


@ns.route('/<string:id>')
class ModelItem(Resource):
    @api.expect(model)
    def put(self, id):
        """
        Api method to update model.
        """
        data_dict = request.json
        data_dict['product'] = OrientRecordLink(request.json['product'])
        data_dict['model_type'] = OrientRecordLink(request.json['model_type'])
        data_dict['size'] = OrientRecordLink(request.json['size'])

        files = request.json.get('files')
        if files:
            filecodestring = files[0]['src']
            data = base64.b64decode(filecodestring.split(',')[1])
            size_obj = _sizeRep.get({'@rid': data_dict['size'].get()})
            product_obj = _productRep.get({'@rid': data_dict['product'].get()})

            attachment_name = os.path.sep.join(
                [
                    'Last',
                    product_obj[0].uuid,
                    '{}.{}'.format(size_obj[0].string_value, 'stl')
                ]
            )
            attachment_path = create_file(attachment_name)
            Path(attachment_path).write_bytes(data)
            data_dict['stl_path'] = attachment_path

        model_obj = _modelRep.update({'@rid': id}, data_dict)[0]
        return {'@rid': model_obj._id, 'name': model_obj.name}, 201

    @api.marshal_with(model)
    def delete(self, id):
        """
        Api method to delete model.
        """
        _modelRep.delete({'@rid': id})
        return None, 200
