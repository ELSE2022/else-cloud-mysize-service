import ast

from apirest.fitting.serializers import comparison_result
from apirest.restplus import api
from data.repositories import ComparisonResultRepository
from data.repositories import UserRepository
from flask import request
from flask import abort
from flask_restplus import Resource

ns = api.namespace('fitting/comparisonresults/', description='Operations related to Comparison result')

_comparisonResRep = ComparisonResultRepository()
_userRep = UserRepository()

msg_object_does_not_exist = '{} object with id "{}" not found'


@ns.route('', '/')
class ComparisonResults(Resource):
    @api.marshal_with(comparison_result)
    def get(self):
        """
        Returns a comparison results list.
        """
        request_data = dict(request.args)
        page_start = int(request_data.get('_start')[0]) if request_data.get('_start', None) else None
        page_end = int(request_data.get('_end')[0]) if request_data.get('_end', None) else None

        filter = ast.literal_eval(request_data.get('filter')[0])
        user_uuid = filter.get('user_id', None)
        if user_uuid:
            user_obj = _userRep.get({'uuid': user_uuid})
            if not user_obj:
                result_obj = _comparisonResRep.get({})
            else:
                result_obj = _comparisonResRep.get_by_tree({'scan': dict(user=user_obj[0], is_default=True), })
        else:
            result_obj = _comparisonResRep.get({})
        return (result_obj[page_start:page_end], 200, {'X-Total-Count': len(result_obj)}) if result_obj else ([], 200, {'X-Total-Count': 0})
