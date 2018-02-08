from apirest.fitting.serializers import scanner
from apirest.fitting.mixins import ListModelMixin
from apirest.restplus import api
from data.repositories import ScannerRepository
from data.repositories import ScannerModelRepository
from data.models import Scanner
from flask import request
from flask import abort
from flask_restplus import Resource
from pyorient import OrientRecordLink
from settings import SCANNER_STORAGE_BASE_URL

ns = api.namespace('fitting_scanners', path='/fitting/scanners', description='Operations related to Scanner')

_scannerRep = ScannerRepository()
_scannerModelRep = ScannerModelRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'


@ns.route('')
class Scanners(Resource, ListModelMixin):
    model = Scanner
    serializer = scanner

    def get(self):
        return super().get()

    @api.expect(scanner)
    def post(self):
        """
        Api method to create scanner
        """
        data_dict = request.json
        scanner_model_obj = _scannerModelRep.get({'@rid': request.json['model']})
        if not scanner_model_obj:
            abort(400, msg_object_does_not_exist.format('Scanner model', request.json['model']))
        scanner_obj = _scannerRep.add(data_dict, result_JSON=True)
        return scanner_obj


@ns.route('/<string:id>')
@api.response(404, 'Scanner not found.')
class ScannerItem(Resource):

    @api.marshal_with(scanner)
    def get(self, id):
        """
        Returns a scanner object.
        """
        scanner_obj = _scannerRep.get({'@rid': id})
        return scanner_obj[0] if scanner_obj else (None, 404)

    @api.expect(scanner)
    def put(self, id):
        """
        Api method to update scanner.
        """
        data_dict = request.json
        data_dict['model'] = OrientRecordLink(request.json.get('model'))

        scanner_obj = _scannerRep.update({'@rid': id}, data_dict)[0]
        return {'@rid': scanner_obj._id, 'name': scanner_obj.name}, 201

    @api.response(204, 'Scanner successfully deleted.')
    @api.marshal_with(scanner)
    def delete(self, id):
        """
        Api method to delete scanner.
        """
        _scannerRep.delete({'@rid': id})
        return None, 204
