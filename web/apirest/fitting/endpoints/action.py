import operator
from collections import defaultdict

from api.web_actions.best_size import get_foot_best_size
from api.web_actions.best_size import generate_result
from apirest.fitting.serializers import fitting_user
from apirest.fitting.serializers import profile_user
from apirest.fitting.serializers import size
from apirest.fitting.serializers import user_scans
from apirest.fitting.serializers import user_size
from apirest.fitting.endpoints.product_action import msg_object_does_not_exist
from apirest.restplus import api
from apirest.restplus import auth_required
# from api.web_actions.get_user_profile import get_user
from data.repositories import UserRepository
from data.repositories import ScanRepository
from data.repositories import ModelTypeRepository
from data.repositories import SizeRepository
from data.repositories import UserSizeRepository
from data.repositories import ScanMetricValueRepository
from data.repositories import ProductRepository
from data.repositories import ComparisonResultRepository
from datetime import datetime
from flask import request
from flask import abort
from flask_restplus import Resource
from flask_restplus import reqparse
from orientdb_data_layer import data_connection
from pyorient import OrientRecordLink

from settings import SCANNER_STORAGE_BASE_URL

ns = api.namespace('fitting_users', path='/fitting/users', description='Operations related to User')

_userRep = UserRepository()
_scanRep = ScanRepository()
_modelTypeRep = ModelTypeRepository()
_sizeRep = SizeRepository()
_userSizeRep = UserSizeRepository()
_scanMetricValueRep = ScanMetricValueRepository()
_productRep = ProductRepository()
_comparisonResRep = ComparisonResultRepository()

default_size_arguments = reqparse.RequestParser()
default_size_arguments.add_argument('type', type=str, required=False)

best_style_arguments = reqparse.RequestParser()
best_style_arguments.add_argument('size', type=str, required=False)

default_scan_arguments = reqparse.RequestParser()
default_scan_arguments.add_argument('scan', type=str, required=True)


def get_user(user_uuid):
    if user_uuid is None:
        abort(400, 'Request malformed: \'user\' argument not passed')
    user = _userRep.get({
        'uuid': user_uuid,
    })
    if len(user) == 0:
        abort(404, 'User not found')
    if len(user) > 1:
        abort(400, 'Too many ({}) users with '
            'the same user_uuid: {}'.format(len(user), user_uuid))
    return user[0]


def get_objects(graph, user_uuid, product_uuid):
    user_obj = _userRep.get({'uuid': user_uuid})
    if not user_obj:
        abort(400, msg_object_does_not_exist.format('User', user_uuid))

    product_obj = _productRep.get({'uuid': product_uuid})
    if not product_obj:
        abort(400, msg_object_does_not_exist.format('Product', product_uuid))

    model_types = graph.elements_from_links(
        graph.element_from_link(product_obj[0].default_comparison_rule).model_types)

    scans = []
    for ty in model_types:
        scans += _scanRep.get(dict(user=user_obj[0], is_default=True, model_type=ty))
    if not scans:
        abort(400, 'User with uuid {} does not have any scans'.format(user_uuid))
    return user_obj[0], product_obj[0], model_types, scans


@ns.route('',)
class Users(Resource):
    @api.marshal_with(fitting_user)
    def get(self):
        """
        Returns a users list.
        """
        request_data = dict(request.args)
        page_start = int(request_data.get('_start')[0]) if request_data.get('_start', None) else None
        page_end = int(request_data.get('_end')[0]) if request_data.get('_end', None) else None

        user_obj = _userRep.get({})
        return (user_obj[page_start:page_end], 200, {'X-Total-Count': len(user_obj)}) if user_obj else (None, 404)

    @api.expect(fitting_user)
    def post(self):
        """
        Api method to create user.
        """
        user_uuid = request.json.get('uuid')
        base_url = request.json.get('base_url', SCANNER_STORAGE_BASE_URL)
        size_value = request.json.get('size')
        user_obj = _userRep.add({'uuid': user_uuid, 'base_url': base_url}, result_JSON=True)

        if size_value:
            left_foot = _modelTypeRep.get(dict(name='LEFT_FOOT'))
            right_foot = _modelTypeRep.get(dict(name='RIGHT_FOOT'))
            if len(left_foot) == 0 and len(right_foot) == 0:
                left_foot = _modelTypeRep.add(dict(name='LEFT_FOOT'))
                right_foot = _modelTypeRep.add(dict(name='RIGHT_FOOT'))
            else:
                left_foot = left_foot[0]
                right_foot = right_foot[0]

            foot_types = [left_foot, right_foot]

            size_obj = _sizeRep.get({'string_value': size_value, 'model_types': foot_types})
            if not size_obj:
                size_obj = _sizeRep.add(dict(string_value=size_value, model_types=foot_types))
            else: size_obj = size_obj[0]
            _userSizeRep.add({'user': user_obj, 'size': size_obj, 'creation_time': str(datetime.now())})

        return user_obj


@ns.route('/<string:uuid>')
@api.response(404, 'User not found.')
class UserItem(Resource):
    @api.expect(fitting_user)
    def put(self, uuid):
        """
        Api method to update user.
        """
        user_obj = _userRep.update({'uuid': uuid}, request.json)[0]
        return {'@rid': user_obj._id, 'uuid': user_obj.uuid}, 201

    @api.response(204, 'User successfully deleted.')
    @api.marshal_with(fitting_user)
    def delete(self, uuid):
        """
        Api method to delete user.
        """
        _userRep.delete({'uuid': uuid})
        return None, 204

    @api.marshal_with(fitting_user)
    @auth_required
    def get(self, uuid):
        """
        Returns a user object.
        """
        user = _userRep.get({'uuid': uuid})
        return user[0] if user else (None, 404)


@ns.route('/<string:uuid>/profile')
class UserProfile(Resource):
    @api.marshal_with(profile_user)
    @api.expect(default_scan_arguments)
    def get(self, uuid):
        """
        Api method to get user profile.
        """
        scans_list = []
        user = get_user(uuid)
        scans = _scanRep.get({'user': user, 'scan_id': request.json.get('scan')})
        for sc in scans:
            metric = _scanMetricValueRep.get({
                'scan': sc,
            })
            scans_with_metrics = sc._props
            scans_with_metrics['metric'] = metric
            scans_list.append(scans_with_metrics)
        return {'uuid': uuid, 'scans': scans_list}


@ns.route('/<string:uuid>/scans')
class Scans(Resource):
    @api.marshal_with(user_scans)
    def get(self, uuid):
        """
        Api method to get user scans.
        """
        # scans_list = []
        # user = _userRep.get({'uuid': uuid})
        scans = _scanRep.get_by_tree({'user': {'uuid': uuid}})
        # for sc in scans:
        #     metric = _scanMetricValueRep.get({
        #         'scan': sc,
        #     })
        #     scans_with_metrics = sc._props
        #     scans_with_metrics['metric'] = metric
        #     scans_list.append(scans_with_metrics)
        return scans


@ns.route('/<string:uuid>/scans/set_default')
class DefaultScan(Resource):
    @api.expect(default_scan_arguments)
    def post(self, uuid):
        """
        Api method to set default user scan.
        """
        scan_id = request.json.get('scan')
        user = get_user(uuid)
        scans = _scanRep.update({'user': user, 'scan_id': scan_id}, {'is_default': True})

        return scans


@ns.route('/<string:uuid>/size')
class Size(Resource):
    @api.marshal_with(size)
    @api.expect(default_size_arguments)
    def get(self, uuid):
        """
        Api method to get default user size
        """
        user_obj = get_user(uuid)
        args = default_size_arguments.parse_args()

        model_type = args.get('type', 'LEFT_FOOT')
        model_type_obj = _modelTypeRep.get(dict(name=model_type))
        if not model_type_obj:
            abort(400)
        user_size_obj = _userSizeRep.get_by_tree(dict(user=user_obj, size=dict(model_types=model_type_obj)))
        if not user_size_obj:
            return abort(400, 'User doesn\'t have default size')
        return user_size_obj[0].size

    @api.expect(size)
    @api.marshal_with(user_size)
    def post(self, uuid):
        """
        Api method to set default user size.
        """
        model_type_objects = []
        user = get_user(uuid)
        print(request.json)
        for mt in request.json['model_types']:
            model_type_obj = _modelTypeRep.get({'name': mt})
            if not model_type_obj:
                abort(400)
            else: model_type_obj = model_type_obj[0]
            model_type_objects.append(model_type_obj._id)

            size_object = _sizeRep.sql_command("select @rid as _id, string_value, model_types from size where {0} IN model_types AND string_value={1}".format(model_type_obj._id, request.json['string_value']), result_as_dict=True)
            user_size_rep = _userSizeRep.get({
                'user': user,
                'size': size_object[0].get('_id'),
            })
            if not user_size_rep:
                user_size_rep = _userSizeRep.add({
                    'user': user,
                    'size': size_object[0].get('_id'),
                    'model_type': model_type_obj._id,
                    'creation_time': str(datetime.now()),
                })
            else: user_size_rep = user_size_rep[0]
        return {'user': user, 'size': size_object[0]}


@ns.route('/<string:user_uuid>/products/<string:product_uuid>/best_size')
class BestSize(Resource):
    def get(self, user_uuid, product_uuid):
        """
        Api method to get best user size.
        """
        _graph = data_connection.get_graph()

        user_obj, product_obj, model_types, scans = get_objects(_graph, user_uuid, product_uuid)

        comparison_results = _comparisonResRep.get_by_tree({'scan': dict(user=user_obj, is_default=True),})
        if not comparison_results:
            comparison_results = get_foot_best_size(product_obj, model_types, scans)
        print("Results")
        print(comparison_results)
        dct = defaultdict(int)
        types = []
        for x in comparison_results:
            dct[x.size] += x.value
            if str(x.model_type) not in types:
                types.append(str(x.model_type))
        print(dct)
        results = {k: v / len(types) for k, v in dct.items()}
        max_result = max(results.items(), key=operator.itemgetter(1))
        print(max_result)
        return {
            'score': round(max_result[1], 2),
            'output_model': '',
            'size': _graph.element_from_link(max_result[0]).string_value,
            'size_type': 'FOOT'
        }


@ns.route('/<string:user_uuid>/products/<string:product_uuid>/best_style')
class BestStyle(Resource):
    @api.expect(best_style_arguments, validate=True)
    def get(self, user_uuid, product_uuid):
        """
        Api method to get best user style.
        """
        _graph = data_connection.get_graph()

        user_obj, product_obj, model_types, scans = get_objects(_graph, user_uuid, product_uuid)

        args = best_style_arguments.parse_args()
        if not args.get('size'):
            user_size_obj = _userSizeRep.get(dict(user=user_obj))
            size_obj = None
            for s in user_size_obj:
                _size = _graph.element_from_link(s.size)
                if _graph.elements_from_links(_size.model_types) == model_types:
                    size_obj = _size
            if size_obj is None:
                abort(404, 'user\'s size not found')
        else:
            size_obj = _sizeRep.get(dict(string_value=args.get('size')))[0]
        comparison_results = _comparisonResRep.get_by_tree({'scan': dict(user=user_obj, is_default=True),
                                                            'size': size_obj})
        if not comparison_results:
            results = get_foot_best_size(product_obj, model_types, scans)
            comparison_results = [x for x in results if str(x.size) == size_obj._id]

        avg_res = sum(c.value for c in comparison_results) / float(len(comparison_results))
        return {
            'score': round(avg_res, 2),
            'output_model': '',
            'size': size_obj.string_value,
            'size_type': 'FOOT'
        }