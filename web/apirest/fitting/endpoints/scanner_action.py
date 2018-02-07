from apirest.fitting.serializers import scanner
from apirest.restplus import api
from data.repositories import ScannerRepository
from data.repositories import ScannerModelRepository
from flask import request
from flask import abort
from flask_restplus import Resource

ns = api.namespace('fitting_scanners', path='/fitting/scanners', description='Operations related to Scanner')

_scannerRep = ScannerRepository()
_scannerModelRep = ScannerModelRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'


@ns.route('')
class Scanners(Resource):
    @api.marshal_with(scanner)
    def get(self):
        """
        Returns a scanners list.
        """
        request_data = dict(request.args)
        page_start = int(request_data.get('_start')[0]) if request_data.get('_start', None) else None
        page_end = int(request_data.get('_end')[0]) if request_data.get('_end', None) else None

        scanner_obj = _scannerRep.get({})
        return (scanner_obj[page_start:page_end], 200, {'X-Total-Count': len(scanner_obj)}) if scanner_obj else ([], 200, {'X-Total-Count': 0})

    @api.expect(scanner)
    def post(self):
        """
        Api method to create scanner
        """
        print(request.json)
        scanner_model_obj = _scannerModelRep.get({'@rid': request.json['model']})
        if not scanner_model_obj:
            abort(400, msg_object_does_not_exist.format('Scanner model', request.json['model']))

        scanner_obj = _scannerRep.add({'name': request.json['name'], 'model': scanner_model_obj[0]}, result_JSON=True)
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
        scanner_obj = _scannerRep.update({'@rid': id}, request.json)[0]
        return {'@rid': scanner_obj._id, 'name': scanner_obj.name}, 201

    @api.response(204, 'Scanner successfully deleted.')
    @api.marshal_with(scanner)
    def delete(self, id):
        """
        Api method to delete scanner.
        """
        _scannerRep.delete({'@rid': id})
        return None, 204
