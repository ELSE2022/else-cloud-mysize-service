from apirest.fitting.serializers import comparison_rule
from apirest.fitting.serializers import model
from apirest.restplus import api
from data.repositories import ProductRepository
from data.repositories import ModelRepository
from data.repositories import ModelTypeRepository
from data.repositories import SizeRepository
from data.repositories import BrandRepository
from data.repositories import ComparisonRuleRepository
from data.repositories import ScannerModelRepository
from flask import request
from flask import abort
from flask_restplus import Resource
from pyorient import OrientRecordLink

ns = api.namespace('fitting/comparisonrules/', description='Operations related to Comparison rule')

_productRep = ProductRepository()
_modelRep = ModelRepository()
_modelTypeRep = ModelTypeRepository()
_sizeRep = SizeRepository()
_brandRep = BrandRepository()
_compRuleRep = ComparisonRuleRepository()
_scannerModelRep = ScannerModelRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'


@ns.route('', '/', '/<string:uuid>')
class ComparisonRule(Resource):
    @api.marshal_with(comparison_rule)
    def get(self):
        """
        Returns a comparison rules list.
        """
        request_data = dict(request.args)
        page_start = int(request_data.get('_start')[0]) if request_data.get('_start', None) else None
        page_end = int(request_data.get('_end')[0]) if request_data.get('_end', None) else None

        rule_obj = _compRuleRep.get({})

        return (rule_obj[page_start:page_end], 200, {'X-Total-Count': len(rule_obj)}) if rule_obj else ([], 200, {'X-Total-Count': 0})

    @api.expect(comparison_rule)
    def put(self, uuid):
        """
        Api method to update comparison rule.
        """
        model_type_obj = []
        for x in request.json['model_types']:
            model_type_obj.append(OrientRecordLink(x))

        data_dict = request.json
        data_dict['model_types'] = model_type_obj
        data_dict['scanner_model'] = OrientRecordLink(request.json['scanner_model'])

        rule_obj = _compRuleRep.update({'@rid': uuid}, data_dict)[0]
        return {'@rid': rule_obj._id, 'name': rule_obj.name}, 201

    @api.expect(comparison_rule)
    def post(self):
        """
        Api method to comparison rule.
        """
        model_type_obj = []
        for x in request.json['model_types']:
            model_type_obj.append(_modelTypeRep.get({'@rid': x})[0])

        if not model_type_obj:
            abort(400, msg_object_does_not_exist.format('Model type', request.json['model_type']))

        scanner_model_obj = _scannerModelRep.get({'@rid': request.json['scanner_model']})
        if not scanner_model_obj:
            abort(400, msg_object_does_not_exist.format('Scanner model', request.json['scanner_model']))

        data_dict = request.json
        data_dict['model_types'] = model_type_obj
        data_dict['scanner_model'] = scanner_model_obj[0]
        rule_obj = _compRuleRep.add(data_dict, result_JSON=True)
        return rule_obj
