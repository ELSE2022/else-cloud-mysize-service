from apirest.fitting.serializers import comparison_rule_metric
from apirest.restplus import api
from data.repositories import ComparisonRuleMetricRepository
from flask import request
from flask_restplus import Resource

ns = api.namespace('fitting/comparisonrulemetric/', description='Operations related to Comparison rule metrics')

_compRuleMetricRep = ComparisonRuleMetricRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'


@ns.route('', '/', '/<string:uuid>')
class ComparisonRuleMetrics(Resource):
    @api.marshal_with(comparison_rule_metric)
    def get(self):
        """
        Returns a model metrics list.
        """
        request_data = dict(request.args)
        page_start = int(request_data.get('_start')[0]) if request_data.get('_start', None) else None
        page_end = int(request_data.get('_end')[0]) if request_data.get('_end', None) else None

        comp_rule_metric_obj = _compRuleMetricRep.get({})
        return (comp_rule_metric_obj[page_start:page_end], 200, {'X-Total-Count': len(comp_rule_metric_obj)}) if comp_rule_metric_obj else ([], 200, {'X-Total-Count': 0})

    @api.expect(comparison_rule_metric)
    def post(self):
        """
        Api method to create model metric.
        """
        comp_rule_metric_obj = _compRuleMetricRep.add(request.json, result_JSON=True)
        return comp_rule_metric_obj

    @api.expect(comparison_rule_metric)
    def put(self, uuid):
        """
        Api method to update scan metric.
        """
        comp_rule_metric_obj = _compRuleMetricRep.update({'@rid': uuid}, request.json)[0]
        return {'@rid': comp_rule_metric_obj._id, 'name': comp_rule_metric_obj.name}, 201

    @api.response(204, 'Comparison rule metric successfully deleted.')
    def delete(self, uuid):
        """
        Api method to delete scan metric.
        """
        _compRuleMetricRep.delete({'@rid': uuid})
        return None, 204
