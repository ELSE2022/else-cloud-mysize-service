from apirest.fitting.serializers import scanner_model
from apirest.restplus import api
from data.repositories import ScannerModelRepository
from flask import request
from flask_restplus import Resource

ns = api.namespace('fitting_scannermodels', path='/fitting/scannermodels', description='Operations related to Scanner models')

_scannerModelRep = ScannerModelRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'


@ns.route('')
class ScannerModels(Resource):
    @api.marshal_with(scanner_model)
    def get(self):
        """
        Returns a scanner models list.
        """
        request_data = dict(request.args)
        page_start = int(request_data.get('_start')[0]) if request_data.get('_start', None) else None
        page_end = int(request_data.get('_end')[0]) if request_data.get('_end', None) else None

        scanner_model_obj = _scannerModelRep.get({})
        return (scanner_model_obj[page_start:page_end], 200, {'X-Total-Count': len(scanner_model_obj)}) if scanner_model_obj else ([], 200, {'X-Total-Count': 0})

    @api.expect(scanner_model)
    def post(self):
        """
        Api method to create size.
        """
        scanner_model_obj = _scannerModelRep.add(request.json, result_JSON=True)
        return scanner_model_obj


@ns.route('/<string:id>')
class ScannerModelItem(Resource):
    @api.expect(scanner_model)
    def put(self, id):
        """
        Api method to update scanner model.
        """
        scanner_model_obj = _scannerModelRep.update({'@rid': id}, request.json)[0]
        return {'@rid': scanner_model_obj._id, 'name': scanner_model_obj.name}, 201

    @api.response(204, 'Scanner model successfully deleted.')
    def delete(self, id):
        """
        Api method to delete scanner model.
        """
        _scannerModelRep.delete({'@rid': id})
        return None, 204
