from apirest.fitting.serializers import scan
from apirest.restplus import api
from data.repositories import ScannerRepository
from data.repositories import ScanRepository
from data.repositories import UserRepository
from data.repositories import ModelTypeRepository
from flask import request
from flask import abort
from flask_restplus import Resource

ns = api.namespace('fitting/scans/', description='Operations related to Scan')

_scannerRep = ScannerRepository()
_scanRep = ScanRepository()
_userRep = UserRepository()
_modelTypeRep = ModelTypeRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'


@ns.route('', '/', '/<string:id>')
class Scans(Resource):
    @api.marshal_with(scan)
    def get(self):
        """
        Returns a scans list.
        """
        print('get scans')
        request_data = dict(request.args)
        page_start = int(request_data.get('_start')[0]) if request_data.get('_start', None) else None
        page_end = int(request_data.get('_end')[0]) if request_data.get('_end', None) else None
        print('get scans2')
        print(request_data)
        scan_obj = _scanRep.get({})
        return (scan_obj[page_start:page_end], 200, {'X-Total-Count': len(scan_obj)}) if scan_obj else ([], 200, {'X-Total-Count': 0})

    @api.expect(scan)
    def post(self):
        """
        Api method to create scan.
        """
        user_obj = _userRep.get({'@rid': request.json['user']})
        if not user_obj:
            abort(400, msg_object_does_not_exist.format('User', request.json['user']))

        scanner_obj = _scannerRep.get({'@rid': request.json['scanner']})
        if not scanner_obj:
            abort(400, msg_object_does_not_exist.format('Scanner', request.json['scanner']))

        model_type_obj = _modelTypeRep.get({'@rid': request.json['model_type']})
        if not model_type_obj:
            abort(400, msg_object_does_not_exist.format('Model type', request.json['model_type']))

        data_dict = request.json
        data_dict['user'] = user_obj[0]
        data_dict['scanner'] = scanner_obj[0]
        data_dict['model_type'] = model_type_obj[0]
        scanner_obj = _scannerRep.add(data_dict, result_JSON=True)
        return scanner_obj

    @api.expect(scan)
    def put(self, id):
        """
        Api method to update scan.
        """
        scan_obj = _scanRep.update({'@rid': id}, request.json)[0]
        return {'@rid': scan_obj._id, 'name': scan_obj.name}, 201

    @api.response(204, 'Scan successfully deleted.')
    @api.marshal_with(scan)
    def delete(self, id):
        """
        Api method to delete scan.
        """
        _scanRep.delete({'@rid': id})
        return None, 204
