from flask import json

from apirest.fitting.serializers import scanner
from apirest.fitting.mixins import ListModelMixin
from apirest.fitting.mixins import CreateModelMixin
from apirest.fitting.mixins import RetrieveModelMixin
from apirest.fitting.mixins import DestroyModelMixin
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
class Scanners(Resource, ListModelMixin, CreateModelMixin):
    model = Scanner
    serializer = scanner

    def get(self):
        return super().get()

    # @api.expect(scanner)
    # def post(self):
    #     """
    #     Api method to create scanner.
    #     """
    #     scanner_obj = Scanner.add(request.json, result_as_json=True)
    #     return scanner_obj

    @api.expect(scanner)
    def post(self):
        """
        Api method to create scanner.
        """
        return super().post()


@ns.route('/<string:id>')
@api.response(404, 'Scanner not found.')
class ScannerItem(Resource, RetrieveModelMixin, DestroyModelMixin):
    model = Scanner
    serializer = scanner

    # @api.marshal_with(scanner)
    # def get(self, id):
    #     """
    #     Returns a scanner object.
    #     """
    #     scanner_obj = _scannerRep.get({'@rid': id})
    #     return scanner_obj[0] if scanner_obj else (None, 404)
    def get(self, id):
        return super().get(id)

    @api.expect(scanner)
    def put(self, id):
        """
        Api method to update scanner.
        """
        # data_dict = request.json
        # data_dict['model'] = OrientRecordLink(request.json.get('model'))
        # print(data_dict)
        scanner_obj = Scanner.update(id, request.json)
        print(scanner_obj)
        # scanner_obj = _scannerRep.update({'@rid': id}, data_dict)[0]
        return {'@rid': id}, 201

    def delete(self, id):
        return super().delete(id)

    # @api.response(204, 'Scanner successfully deleted.')
    # @api.marshal_with(scanner)
    # def delete(self, id):
    #     """
    #     Api method to delete scanner.
    #     """
    #     _scannerRep.delete({'@rid': id})
    #     return None, 200
